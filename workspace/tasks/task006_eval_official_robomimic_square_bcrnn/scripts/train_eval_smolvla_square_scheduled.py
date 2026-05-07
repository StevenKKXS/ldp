#!/usr/bin/env python3
"""Formal train/eval for a compact SmolVLA-like policy on square HDF5.

This is an isolated experiment script. It does not import or edit the LDP repo.
It mirrors the SmolVLA training structure at small scale:
  image/state/language prefix tokens condition an action expert that predicts
  the flow-matching velocity for a continuous action chunk.

The main loop is epoch-based to match the LDP training convention. It supports
1000 epochs, dense early evaluation, sparse late evaluation, checkpointing, and
resume.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import h5py
import numpy as np
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, Dataset, DistributedSampler


STATE_KEYS = (
    "robot0_eef_pos",
    "robot0_eef_quat",
    "robot0_gripper_qpos",
)

IMAGE_KEYS = (
    "agentview_image",
    "robot0_eye_in_hand_image",
)


@dataclass
class Stats:
    action_repr: str
    state_mean: list[float]
    state_std: list[float]
    action_mean: list[float]
    action_std: list[float]


def is_dist() -> bool:
    return int(os.environ.get("WORLD_SIZE", "1")) > 1


def rank0() -> bool:
    return int(os.environ.get("RANK", "0")) == 0


def setup_dist() -> tuple[int, int, torch.device]:
    if not is_dist():
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        return 0, 1, device
    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    return dist.get_rank(), dist.get_world_size(), torch.device(f"cuda:{local_rank}")


def cleanup_dist() -> None:
    if dist.is_available() and dist.is_initialized():
        dist.destroy_process_group()


def seed_everything(seed: int, rank: int) -> None:
    seed = seed + rank * 1009
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def matrix_to_rotation_6d(matrix: np.ndarray) -> np.ndarray:
    # Match pytorch3d.transforms.matrix_to_rotation_6d used by LDP.
    return matrix[..., :2, :].reshape(*matrix.shape[:-2], 6)


def convert_actions(raw_actions: np.ndarray, action_repr: str) -> np.ndarray:
    if action_repr == "raw7":
        return raw_actions.astype(np.float32)
    if action_repr != "ldp_abs10":
        raise ValueError(f"Unsupported action_repr: {action_repr}")
    from scipy.spatial.transform import Rotation

    pos = raw_actions[..., :3]
    rotvec = raw_actions[..., 3:6]
    gripper = raw_actions[..., 6:]
    rot_matrix = Rotation.from_rotvec(rotvec.reshape(-1, 3)).as_matrix()
    rot6d = matrix_to_rotation_6d(rot_matrix).reshape(*rotvec.shape[:-1], 6)
    return np.concatenate([pos, rot6d, gripper], axis=-1).astype(np.float32)


def load_or_compute_stats(dataset_path: Path, stats_path: Path, action_repr: str) -> Stats:
    if stats_path.exists():
        with stats_path.open("r", encoding="utf-8") as f:
            stats = Stats(**json.load(f))
        if stats.action_repr != action_repr:
            raise ValueError(f"Stats at {stats_path} are for {stats.action_repr}, not {action_repr}")
        return stats

    state_sum = None
    state_sq_sum = None
    action_sum = None
    action_sq_sum = None
    count = 0

    with h5py.File(dataset_path, "r") as f:
        demos = sorted(f["data"].keys())
        for demo in demos:
            g = f["data"][demo]
            state = np.concatenate([g["obs"][k][()] for k in STATE_KEYS], axis=-1).astype(np.float64)
            action = convert_actions(g["actions"][()].astype(np.float32), action_repr).astype(np.float64)
            if state_sum is None:
                state_sum = np.zeros(state.shape[-1], dtype=np.float64)
                state_sq_sum = np.zeros(state.shape[-1], dtype=np.float64)
                action_sum = np.zeros(action.shape[-1], dtype=np.float64)
                action_sq_sum = np.zeros(action.shape[-1], dtype=np.float64)
            state_sum += state.sum(axis=0)
            state_sq_sum += np.square(state).sum(axis=0)
            action_sum += action.sum(axis=0)
            action_sq_sum += np.square(action).sum(axis=0)
            count += state.shape[0]

    assert state_sum is not None and action_sum is not None
    state_mean = state_sum / count
    action_mean = action_sum / count
    state_std = np.sqrt(np.maximum(state_sq_sum / count - np.square(state_mean), 1e-8))
    action_std = np.sqrt(np.maximum(action_sq_sum / count - np.square(action_mean), 1e-8))
    stats = Stats(
        action_repr=action_repr,
        state_mean=state_mean.tolist(),
        state_std=state_std.tolist(),
        action_mean=action_mean.tolist(),
        action_std=action_std.tolist(),
    )
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with stats_path.open("w", encoding="utf-8") as f:
        json.dump(asdict(stats), f, indent=2)
    return stats


class SquareChunkDataset(Dataset):
    def __init__(
        self,
        dataset_path: Path,
        stats: Stats,
        chunk_size: int,
        action_repr: str,
        split: str,
        val_ratio: float,
        seed: int,
        max_sequences: int | None,
    ) -> None:
        self.dataset_path = str(dataset_path)
        self.stats = stats
        self.chunk_size = chunk_size
        self.action_repr = action_repr
        self._h5 = None

        with h5py.File(dataset_path, "r") as f:
            demos = sorted(f["data"].keys())
            rng = np.random.default_rng(seed)
            perm = np.array(demos)
            rng.shuffle(perm)
            n_val = max(1, int(round(len(perm) * val_ratio)))
            selected = set(perm[:n_val] if split == "val" else perm[n_val:])
            index = []
            for demo in demos:
                if demo not in selected:
                    continue
                length = int(f["data"][demo].attrs.get("num_samples", f["data"][demo]["actions"].shape[0]))
                # Keep only starts with at least one real future action.
                for t in range(length):
                    index.append((demo, t, length))
        if max_sequences is not None and len(index) > max_sequences:
            rng = np.random.default_rng(seed + (17 if split == "val" else 0))
            keep = rng.choice(len(index), size=max_sequences, replace=False)
            index = [index[i] for i in sorted(keep.tolist())]
        self.index = index

    def __len__(self) -> int:
        return len(self.index)

    @property
    def h5(self):
        if self._h5 is None:
            self._h5 = h5py.File(self.dataset_path, "r", swmr=True)
        return self._h5

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        demo, t, length = self.index[idx]
        g = self.h5["data"][demo]

        images = []
        for key in IMAGE_KEYS:
            img = g["obs"][key][t]  # HWC uint8
            img = torch.from_numpy(np.asarray(img)).permute(2, 0, 1).float().div_(255.0)
            images.append(img)

        state_np = np.concatenate([g["obs"][k][t] for k in STATE_KEYS], axis=-1).astype(np.float32)
        state = (state_np - np.asarray(self.stats.state_mean, dtype=np.float32)) / np.asarray(
            self.stats.state_std, dtype=np.float32
        )

        action_dim = len(self.stats.action_mean)
        actions = np.zeros((self.chunk_size, action_dim), dtype=np.float32)
        action_is_pad = np.ones((self.chunk_size,), dtype=bool)
        end = min(length, t + self.chunk_size)
        valid = end - t
        if valid > 0:
            raw = convert_actions(g["actions"][t:end].astype(np.float32), self.action_repr)
            raw = (raw - np.asarray(self.stats.action_mean, dtype=np.float32)) / np.asarray(
                self.stats.action_std, dtype=np.float32
            )
            actions[:valid] = raw
            action_is_pad[:valid] = False

        return {
            "image0": images[0],
            "image1": images[1],
            "state": torch.from_numpy(state),
            "action": torch.from_numpy(actions),
            "action_is_pad": torch.from_numpy(action_is_pad),
        }


class SinusoidalTimeEmbedding(nn.Module):
    def __init__(self, dim: int, min_period: float = 4e-3, max_period: float = 4.0) -> None:
        super().__init__()
        self.dim = dim
        self.min_period = min_period
        self.max_period = max_period

    def forward(self, time_tensor: torch.Tensor) -> torch.Tensor:
        if self.dim % 2 != 0:
            raise ValueError("time embedding dim must be even")
        fraction = torch.linspace(0.0, 1.0, self.dim // 2, device=time_tensor.device, dtype=torch.float32)
        period = self.min_period * (self.max_period / self.min_period) ** fraction
        arg = time_tensor[:, None] * (2.0 * math.pi / period[None, :])
        return torch.cat([torch.sin(arg), torch.cos(arg)], dim=-1)


class ImageEncoder(nn.Module):
    def __init__(self, emb_dim: int) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, 5, stride=2, padding=2),
            nn.GroupNorm(8, 32),
            nn.SiLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),
            nn.GroupNorm(8, 64),
            nn.SiLU(),
            nn.Conv2d(64, 128, 3, stride=2, padding=1),
            nn.GroupNorm(16, 128),
            nn.SiLU(),
            nn.Conv2d(128, 192, 3, stride=2, padding=1),
            nn.GroupNorm(16, 192),
            nn.SiLU(),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(192, emb_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class SmolVLALikePolicy(nn.Module):
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        chunk_size: int,
        emb_dim: int,
        expert_layers: int,
        n_heads: int,
        dropout: float,
    ) -> None:
        super().__init__()
        self.chunk_size = chunk_size
        self.action_dim = action_dim
        self.image_encoder = ImageEncoder(emb_dim)
        self.image_view_embed = nn.Parameter(torch.randn(2, emb_dim) * 0.02)
        self.lang_embed = nn.Parameter(torch.randn(1, emb_dim) * 0.02)
        self.state_proj = nn.Sequential(nn.Linear(state_dim, emb_dim), nn.SiLU(), nn.Linear(emb_dim, emb_dim))
        self.action_in_proj = nn.Linear(action_dim, emb_dim)
        self.time_emb = SinusoidalTimeEmbedding(emb_dim)
        self.action_time_mlp = nn.Sequential(nn.Linear(emb_dim * 2, emb_dim), nn.SiLU(), nn.Linear(emb_dim, emb_dim))
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=emb_dim,
            nhead=n_heads,
            dim_feedforward=emb_dim * 4,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.action_expert = nn.TransformerDecoder(decoder_layer, num_layers=expert_layers)
        self.out_norm = nn.LayerNorm(emb_dim)
        self.action_out_proj = nn.Linear(emb_dim, action_dim)

    def embed_prefix(self, image0: torch.Tensor, image1: torch.Tensor, state: torch.Tensor) -> torch.Tensor:
        img0 = self.image_encoder(image0) + self.image_view_embed[0]
        img1 = self.image_encoder(image1) + self.image_view_embed[1]
        lang = self.lang_embed.expand(state.shape[0], -1)
        state_emb = self.state_proj(state)
        return torch.stack([img0, img1, lang, state_emb], dim=1)

    def predict_velocity(self, image0, image1, state, noisy_action, time_tensor) -> torch.Tensor:
        prefix = self.embed_prefix(image0, image1, state)
        action_emb = self.action_in_proj(noisy_action)
        time_emb = self.time_emb(time_tensor).to(dtype=action_emb.dtype)
        time_emb = time_emb[:, None, :].expand_as(action_emb)
        suffix = self.action_time_mlp(torch.cat([action_emb, time_emb], dim=-1))
        suffix = self.action_expert(tgt=suffix, memory=prefix)
        return self.action_out_proj(self.out_norm(suffix))

    def flow_loss(self, batch: dict[str, torch.Tensor]) -> torch.Tensor:
        action = batch["action"]
        noise = torch.randn_like(action)
        beta = torch.distributions.Beta(1.5, 1.0)
        time_tensor = beta.sample((action.shape[0],)).to(action.device, dtype=action.dtype)
        time_tensor = time_tensor * 0.999 + 0.001
        x_t = time_tensor[:, None, None] * noise + (1.0 - time_tensor[:, None, None]) * action
        target_v = noise - action
        pred_v = self.predict_velocity(batch["image0"], batch["image1"], batch["state"], x_t, time_tensor)
        losses = F.mse_loss(pred_v, target_v, reduction="none")
        valid = ~batch["action_is_pad"]
        denom = (valid.sum() * action.shape[-1]).clamp_min(1)
        return (losses * valid.unsqueeze(-1)).sum() / denom

    @torch.no_grad()
    def sample_actions(self, batch: dict[str, torch.Tensor], steps: int) -> torch.Tensor:
        bsz = batch["state"].shape[0]
        x_t = torch.randn(bsz, self.chunk_size, self.action_dim, device=batch["state"].device)
        dt = -1.0 / steps
        for i in range(steps):
            t = torch.full((bsz,), 1.0 + i * dt, device=x_t.device)
            v_t = self.predict_velocity(batch["image0"], batch["image1"], batch["state"], x_t, t)
            x_t = x_t + dt * v_t
        return x_t


def move_batch(batch: dict[str, torch.Tensor], device: torch.device) -> dict[str, torch.Tensor]:
    return {k: v.to(device, non_blocking=True) for k, v in batch.items()}


def reduce_mean(value: torch.Tensor) -> torch.Tensor:
    if dist.is_available() and dist.is_initialized():
        dist.all_reduce(value, op=dist.ReduceOp.SUM)
        value = value / dist.get_world_size()
    return value


def evaluate(model: nn.Module, loader: DataLoader, device: torch.device, sample_steps: int, max_batches: int | None) -> dict:
    model.eval()
    losses = []
    sample_mses = []
    with torch.no_grad():
        for idx, batch in enumerate(loader):
            batch = move_batch(batch, device)
            loss = model.flow_loss(batch)
            losses.append(loss.detach())
            if sample_steps > 0:
                pred = model.sample_actions(batch, steps=sample_steps)
                valid = ~batch["action_is_pad"]
                mse = F.mse_loss(pred, batch["action"], reduction="none")
                denom = (valid.sum() * batch["action"].shape[-1]).clamp_min(1)
                sample_mses.append((mse * valid.unsqueeze(-1)).sum() / denom)
            if max_batches is not None and idx + 1 >= max_batches:
                break
    if not losses:
        return {}
    val_loss = torch.stack(losses).mean()
    val_loss = reduce_mean(val_loss)
    out = {"val_loss": float(val_loss.cpu())}
    if sample_mses:
        sample_mse = reduce_mean(torch.stack(sample_mses).mean())
        out["val_sample_action_mse"] = float(sample_mse.cpu())
    model.train()
    return out


def should_run_epoch_event(epoch: int, args: argparse.Namespace) -> bool:
    if epoch == args.epochs:
        return True
    if epoch <= args.eval_early_until_epochs:
        return epoch % args.eval_early_every_epochs == 0
    return epoch % args.eval_late_every_epochs == 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--chunk-size", type=int, default=16)
    p.add_argument("--batch-size", type=int, default=128)
    p.add_argument("--epochs", type=int, default=1000)
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--emb-dim", type=int, default=256)
    p.add_argument("--expert-layers", type=int, default=6)
    p.add_argument("--heads", type=int, default=8)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--num-workers", type=int, default=4)
    p.add_argument("--max-train-sequences", type=int, default=None)
    p.add_argument("--max-val-sequences", type=int, default=None)
    p.add_argument("--val-ratio", type=float, default=0.05)
    p.add_argument("--eval-every-epochs", type=int, default=None, help="Legacy fixed eval period.")
    p.add_argument("--eval-early-every-epochs", type=int, default=10)
    p.add_argument("--eval-early-until-epochs", type=int, default=100)
    p.add_argument("--eval-late-every-epochs", type=int, default=100)
    p.add_argument("--checkpoint-every-epochs", type=int, default=25)
    p.add_argument("--log-every-steps", type=int, default=100)
    p.add_argument("--max-val-batches", type=int, default=0, help="0 means evaluate the full validation loader.")
    p.add_argument("--sample-steps", type=int, default=10)
    p.add_argument("--action-repr", choices=["raw7", "ldp_abs10"], default="raw7")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--amp", action="store_true")
    p.add_argument("--resume", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.eval_every_epochs is not None:
        args.eval_early_every_epochs = args.eval_every_epochs
        args.eval_late_every_epochs = args.eval_every_epochs
        args.eval_early_until_epochs = args.epochs
    rank, world_size, device = setup_dist()
    seed_everything(args.seed, rank)

    args.output.mkdir(parents=True, exist_ok=True)
    stats_path = args.output / "normalization_stats.json"
    if rank0():
        stats = load_or_compute_stats(args.dataset, stats_path, args.action_repr)
    if dist.is_available() and dist.is_initialized():
        dist.barrier()
    stats = load_or_compute_stats(args.dataset, stats_path, args.action_repr)

    train_ds = SquareChunkDataset(
        args.dataset,
        stats,
        chunk_size=args.chunk_size,
        action_repr=args.action_repr,
        split="train",
        val_ratio=args.val_ratio,
        seed=args.seed,
        max_sequences=args.max_train_sequences,
    )
    val_ds = SquareChunkDataset(
        args.dataset,
        stats,
        chunk_size=args.chunk_size,
        action_repr=args.action_repr,
        split="val",
        val_ratio=args.val_ratio,
        seed=args.seed,
        max_sequences=args.max_val_sequences,
    )
    train_sampler = DistributedSampler(train_ds, shuffle=True, seed=args.seed) if world_size > 1 else None
    val_sampler = DistributedSampler(val_ds, shuffle=False, seed=args.seed) if world_size > 1 else None
    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        shuffle=train_sampler is None,
        sampler=train_sampler,
        num_workers=args.num_workers,
        pin_memory=True,
        persistent_workers=args.num_workers > 0,
        drop_last=True,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=args.batch_size,
        shuffle=False,
        sampler=val_sampler,
        num_workers=max(1, args.num_workers // 2),
        pin_memory=True,
        persistent_workers=args.num_workers > 0,
        drop_last=False,
    )

    state_dim = len(stats.state_mean)
    action_dim = len(stats.action_mean)
    model = SmolVLALikePolicy(
        state_dim=state_dim,
        action_dim=action_dim,
        chunk_size=args.chunk_size,
        emb_dim=args.emb_dim,
        expert_layers=args.expert_layers,
        n_heads=args.heads,
        dropout=args.dropout,
    ).to(device)
    if world_size > 1:
        model = DDP(model, device_ids=[device.index], output_device=device.index)

    optim = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, 0.95))
    scaler = torch.cuda.amp.GradScaler(enabled=args.amp and device.type == "cuda")
    log_path = args.output / "train_log.jsonl"
    metrics_path = args.output / "eval_metrics.jsonl"
    latest_path = args.output / "latest.pt"
    start_epoch = 1
    global_step = 0

    if args.resume and latest_path.exists():
        payload = torch.load(latest_path, map_location=device)
        eval_model = model.module if isinstance(model, DDP) else model
        eval_model.load_state_dict(payload["model"])
        optim.load_state_dict(payload["optimizer"])
        if "scaler" in payload:
            scaler.load_state_dict(payload["scaler"])
        start_epoch = int(payload.get("epoch", 0)) + 1
        global_step = int(payload.get("global_step", 0))
        if rank0():
            print(json.dumps({
                "event": "resume",
                "checkpoint": str(latest_path),
                "start_epoch": start_epoch,
                "global_step": global_step,
            }), flush=True)

    if rank0():
        meta = {
            "args": vars(args) | {"dataset": str(args.dataset), "output": str(args.output)},
            "world_size": world_size,
            "device": str(device),
            "num_train_sequences": len(train_ds),
            "num_val_sequences": len(val_ds),
            "state_dim": state_dim,
            "action_dim": action_dim,
            "model_params": sum(p.numel() for p in model.parameters()),
            "steps_per_epoch_rank": len(train_loader),
            "eval_batches_rank": len(val_loader),
            "start_epoch": start_epoch,
            "timestamp": time.time(),
        }
        with (args.output / "run_meta.json").open("w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    model.train()
    t0 = time.time()
    for epoch in range(start_epoch, args.epochs + 1):
        if train_sampler is not None:
            train_sampler.set_epoch(epoch)
        train_losses = []
        last_grad_norm = torch.tensor(0.0, device=device)
        for batch_idx, batch in enumerate(train_loader, start=1):
            batch = move_batch(batch, device)
            optim.zero_grad(set_to_none=True)
            with torch.cuda.amp.autocast(enabled=args.amp and device.type == "cuda", dtype=torch.bfloat16):
                loss = model.module.flow_loss(batch) if isinstance(model, DDP) else model.flow_loss(batch)
            scaler.scale(loss).backward()
            scaler.unscale_(optim)
            last_grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 10.0)
            scaler.step(optim)
            scaler.update()
            global_step += 1
            train_losses.append(loss.detach())

            if global_step == 1 or global_step % args.log_every_steps == 0:
                step_loss = reduce_mean(loss.detach())
                if rank0():
                    log = {
                        "event": "step",
                        "epoch": epoch,
                        "batch": batch_idx,
                        "global_step": global_step,
                        "train_loss": float(step_loss.cpu()),
                        "lr": optim.param_groups[0]["lr"],
                        "elapsed_sec": time.time() - t0,
                    }
                    print(json.dumps(log), flush=True)
                    with log_path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(log) + "\n")

        epoch_loss = reduce_mean(torch.stack(train_losses).mean())
        should_eval = should_run_epoch_event(epoch, args)
        should_ckpt = should_eval or (epoch % args.checkpoint_every_epochs == 0)
        log = {
            "event": "epoch",
            "epoch": epoch,
            "global_step": global_step,
            "train_loss": float(epoch_loss.cpu()),
            "grad_norm": float(last_grad_norm.detach().cpu()),
            "lr": optim.param_groups[0]["lr"],
            "elapsed_sec": time.time() - t0,
        }

        if should_eval:
            eval_model = model.module if isinstance(model, DDP) else model
            max_val_batches = None if args.max_val_batches == 0 else args.max_val_batches
            eval_log = evaluate(eval_model, val_loader, device, sample_steps=args.sample_steps, max_batches=max_val_batches)
            log.update(eval_log)
            log["eval_type"] = "offline_square_action"
            if rank0():
                with metrics_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(log) + "\n")

        if should_ckpt and rank0():
            eval_model = model.module if isinstance(model, DDP) else model
            ckpt = {
                "model": eval_model.state_dict(),
                "optimizer": optim.state_dict(),
                "scaler": scaler.state_dict(),
                "epoch": epoch,
                "global_step": global_step,
                "args": vars(args) | {"dataset": str(args.dataset), "output": str(args.output)},
                "stats": asdict(stats),
            }
            torch.save(ckpt, latest_path)
            if should_eval:
                torch.save(ckpt, args.output / f"epoch_{epoch:04d}.pt")

        if rank0():
            print(json.dumps(log), flush=True)
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(log) + "\n")

    cleanup_dist()


if __name__ == "__main__":
    main()
