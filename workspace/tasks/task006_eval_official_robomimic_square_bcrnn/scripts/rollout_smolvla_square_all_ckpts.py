#!/usr/bin/env python3
"""Roll out all saved SmolVLA-style Square checkpoints.

The script is intentionally self-contained so it can run from the shared task
directory on the GPU host. It discovers named epoch checkpoints under the
SmolVLA resource run base, assigns jobs by worker id, runs Robosuite rollouts,
and writes one manifest per checkpoint plus an aggregate summary.
"""

from __future__ import annotations

import argparse
import collections
import copy
import importlib.util
import json
import random
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import imageio
import numpy as np
import torch
from scipy.spatial.transform import Rotation

import robomimic.utils.env_utils as EnvUtils
import robomimic.utils.file_utils as FileUtils
import robomimic.utils.obs_utils as ObsUtils


STATE_KEYS = ("robot0_eef_pos", "robot0_eef_quat", "robot0_gripper_qpos")
IMAGE_KEYS = ("agentview_image", "robot0_eye_in_hand_image")
EPOCH_RE = re.compile(r"epoch_(\d+)\.pt$")


@dataclass(frozen=True)
class RolloutJob:
    index: int
    run_name: str
    dataset: Path
    checkpoint: Path
    epoch: int


def load_train_module(path: Path):
    spec = importlib.util.spec_from_file_location("smolvla_scheduled_train", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import training module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rotation_6d_to_matrix(d6: np.ndarray) -> np.ndarray:
    a1 = d6[..., 0:3]
    a2 = d6[..., 3:6]
    b1 = a1 / np.clip(np.linalg.norm(a1, axis=-1, keepdims=True), 1e-8, None)
    b2_raw = a2 - np.sum(b1 * a2, axis=-1, keepdims=True) * b1
    b2 = b2_raw / np.clip(np.linalg.norm(b2_raw, axis=-1, keepdims=True), 1e-8, None)
    b3 = np.cross(b1, b2)
    return np.stack([b1, b2, b3], axis=-2)


def ldp_abs10_to_abs7(norm_action: np.ndarray, stats: dict) -> np.ndarray:
    mean = np.asarray(stats["action_mean"], dtype=np.float32)
    std = np.asarray(stats["action_std"], dtype=np.float32)
    action10 = norm_action * std + mean
    pos = action10[..., :3]
    rot6d = action10[..., 3:9]
    gripper = action10[..., 9:10]
    rot_mat = rotation_6d_to_matrix(rot6d)
    rotvec = Rotation.from_matrix(rot_mat.reshape(-1, 3, 3)).as_rotvec().reshape(*rot6d.shape[:-1], 3)
    action7 = np.concatenate([pos, rotvec, gripper], axis=-1).astype(np.float32)
    action7[..., -1] = np.clip(action7[..., -1], -1.0, 1.0)
    return action7


def obs_image_to_uint8(obs: dict, key: str) -> np.ndarray:
    img = np.asarray(obs[key])
    if img.shape[0] == 3:
        img = np.moveaxis(img, 0, -1)
    if img.dtype != np.uint8:
        if img.max() <= 2.0:
            img = img * 255.0
        img = np.clip(img, 0, 255).astype(np.uint8)
    return img


def make_frame(obs: dict) -> np.ndarray:
    agent = obs_image_to_uint8(obs, "agentview_image")
    wrist = obs_image_to_uint8(obs, "robot0_eye_in_hand_image")
    if agent.shape != wrist.shape:
        raise RuntimeError(f"Image shapes differ: {agent.shape} vs {wrist.shape}")
    return np.concatenate([agent, wrist], axis=1)


def obs_to_batch(obs: dict, stats: dict, device: torch.device) -> dict[str, torch.Tensor]:
    images = []
    for key in IMAGE_KEYS:
        img = np.asarray(obs[key])
        if img.shape[-1] == 3:
            img = np.moveaxis(img, -1, 0)
        img = img.astype(np.float32)
        if img.max() > 2.0:
            img = img / 255.0
        images.append(torch.from_numpy(img).unsqueeze(0).to(device=device, dtype=torch.float32))
    state = np.concatenate([np.asarray(obs[k], dtype=np.float32) for k in STATE_KEYS], axis=-1)
    state = (state - np.asarray(stats["state_mean"], dtype=np.float32)) / np.asarray(
        stats["state_std"], dtype=np.float32
    )
    return {
        "image0": images[0],
        "image1": images[1],
        "state": torch.from_numpy(state).unsqueeze(0).to(device=device, dtype=torch.float32),
    }


def create_square_env(dataset_path: Path):
    modality_mapping = collections.defaultdict(list)
    for key in IMAGE_KEYS:
        modality_mapping["rgb"].append(key)
    for key in STATE_KEYS:
        modality_mapping["low_dim"].append(key)
    ObsUtils.initialize_obs_modality_mapping_from_dict(modality_mapping)

    env_meta = FileUtils.get_env_metadata_from_dataset(str(dataset_path))
    env_meta = copy.deepcopy(env_meta)
    env_meta["env_kwargs"]["controller_configs"]["control_delta"] = False
    env = EnvUtils.create_env_from_metadata(
        env_meta=env_meta,
        render=False,
        render_offscreen=True,
        use_image_obs=True,
    )
    env.env.hard_reset = False
    return env


def load_policy(train_module, checkpoint: Path, device: torch.device):
    payload = torch.load(checkpoint, map_location=device)
    stats = payload["stats"]
    ckpt_args = payload["args"]
    model = train_module.SmolVLALikePolicy(
        state_dim=len(stats["state_mean"]),
        action_dim=len(stats["action_mean"]),
        chunk_size=int(ckpt_args.get("chunk_size", 16)),
        emb_dim=int(ckpt_args.get("emb_dim", 256)),
        expert_layers=int(ckpt_args.get("expert_layers", 6)),
        n_heads=int(ckpt_args.get("heads", 8)),
        dropout=float(ckpt_args.get("dropout", 0.1)),
    ).to(device)
    model.load_state_dict(payload["model"])
    model.eval()
    return model, stats, ckpt_args


@torch.no_grad()
def predict_chunk(model, obs: dict, stats: dict, device: torch.device, sample_steps: int) -> np.ndarray:
    batch = obs_to_batch(obs, stats, device)
    norm_action = model.sample_actions(batch, steps=sample_steps)[0].detach().cpu().numpy()
    return ldp_abs10_to_abs7(norm_action, stats)


def run_episode(
    model,
    env,
    stats: dict,
    args: argparse.Namespace,
    seed: int,
    device: torch.device,
    video_dir: Path,
) -> dict:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)

    tmp_video = video_dir / f"seed_{seed}_tmp.mp4"
    writer = imageio.get_writer(str(tmp_video), fps=args.fps, codec="libx264", quality=args.video_quality, macro_block_size=1)
    obs = env.reset()
    writer.append_data(make_frame(obs))

    success = bool(env.is_success().get("task", False))
    steps = 0
    rewards = []
    first_action = None
    t0 = time.time()
    while steps < args.max_steps and not success:
        chunk = predict_chunk(model, obs, stats, device, sample_steps=args.sample_steps)
        if first_action is None:
            first_action = chunk[0].tolist()
        horizon = min(args.action_horizon, chunk.shape[0], args.max_steps - steps)
        for idx in range(horizon):
            obs, reward, done, _ = env.step(chunk[idx])
            steps += 1
            rewards.append(float(reward))
            writer.append_data(make_frame(obs))
            success = bool(env.is_success().get("task", False))
            if success or done or steps >= args.max_steps:
                break
    writer.close()

    final_video = video_dir / f"seed_{seed}_{'success' if success else 'fail'}_{steps}steps.mp4"
    if final_video.exists():
        final_video.unlink()
    tmp_video.rename(final_video)
    return {
        "seed": seed,
        "success": success,
        "steps": steps,
        "max_reward": max(rewards) if rewards else 0.0,
        "elapsed_sec": time.time() - t0,
        "video": str(final_video),
        "first_action": first_action,
    }


def read_completed_summary(manifest: Path, num_rollouts: int) -> dict | None:
    if not manifest.exists():
        return None
    summary = None
    try:
        with manifest.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                if item.get("event") == "summary":
                    summary = item
    except (json.JSONDecodeError, OSError):
        return None
    if summary is not None and int(summary.get("num_rollouts", -1)) == num_rollouts:
        return summary
    return None


def checkpoint_epoch(path: Path) -> int:
    match = EPOCH_RE.search(path.name)
    if not match:
        raise ValueError(f"Not an epoch checkpoint: {path}")
    return int(match.group(1))


def discover_jobs(run_base: Path, limit_jobs: int | None) -> list[RolloutJob]:
    jobs = []
    for run_dir in sorted([p for p in run_base.iterdir() if p.is_dir()]):
        meta_path = run_dir / "run_meta.json"
        if not meta_path.exists():
            continue
        with meta_path.open("r", encoding="utf-8") as f:
            meta = json.load(f)
        dataset = Path(meta["args"]["dataset"])
        ckpts = sorted(run_dir.glob("epoch_*.pt"), key=checkpoint_epoch)
        for ckpt in ckpts:
            jobs.append(
                RolloutJob(
                    index=len(jobs),
                    run_name=run_dir.name,
                    dataset=dataset,
                    checkpoint=ckpt,
                    epoch=checkpoint_epoch(ckpt),
                )
            )
    if limit_jobs is not None:
        jobs = jobs[:limit_jobs]
    return jobs


def output_paths(output_root: Path, job: RolloutJob) -> tuple[Path, Path]:
    job_root = output_root / job.run_name / f"epoch_{job.epoch:04d}"
    return job_root / "manifest.jsonl", job_root / "videos"


def run_worker(args: argparse.Namespace) -> None:
    device = torch.device(args.device if torch.cuda.is_available() and args.device.startswith("cuda") else "cpu")
    jobs = discover_jobs(args.run_base, args.limit_jobs)
    assigned = [job for job in jobs if job.index % args.num_workers == args.worker_id]
    args.output_root.mkdir(parents=True, exist_ok=True)
    train_module = load_train_module(args.train_module)
    env_cache = {}
    worker_log = args.output_root / f"worker_{args.worker_id}.jsonl"

    with worker_log.open("a", encoding="utf-8") as log_f:
        for job in assigned:
            manifest, video_dir = output_paths(args.output_root, job)
            summary = read_completed_summary(manifest, args.num_rollouts)
            if summary is not None and args.resume:
                line = {"event": "skip_completed", "worker_id": args.worker_id, **summary}
                print(json.dumps(line), flush=True)
                log_f.write(json.dumps(line) + "\n")
                log_f.flush()
                continue

            manifest.parent.mkdir(parents=True, exist_ok=True)
            video_dir.mkdir(parents=True, exist_ok=True)
            start_line = {
                "event": "job_start",
                "worker_id": args.worker_id,
                "device": str(device),
                "run_name": job.run_name,
                "epoch": job.epoch,
                "checkpoint": str(job.checkpoint),
                "dataset": str(job.dataset),
            }
            print(json.dumps(start_line), flush=True)
            log_f.write(json.dumps(start_line) + "\n")
            log_f.flush()

            model, stats, ckpt_args = load_policy(train_module, job.checkpoint, device)
            dataset_key = str(job.dataset)
            if dataset_key not in env_cache:
                env_cache[dataset_key] = create_square_env(job.dataset)
            env = env_cache[dataset_key]

            results = []
            t0 = time.time()
            with manifest.open("w", encoding="utf-8") as f:
                for idx in range(args.num_rollouts):
                    seed = args.start_seed + idx
                    result = run_episode(model, env, stats, args, seed, device, video_dir)
                    results.append(result)
                    line = {
                        "event": "episode",
                        "run_name": job.run_name,
                        "epoch": job.epoch,
                        "worker_id": args.worker_id,
                        **result,
                    }
                    print(json.dumps(line), flush=True)
                    f.write(json.dumps(line) + "\n")
                    f.flush()
                successes = sum(int(r["success"]) for r in results)
                summary = {
                    "event": "summary",
                    "run_name": job.run_name,
                    "epoch": job.epoch,
                    "num_rollouts": args.num_rollouts,
                    "successes": successes,
                    "success_rate": successes / max(args.num_rollouts, 1),
                    "mean_steps": float(np.mean([r["steps"] for r in results])),
                    "mean_elapsed_sec": float(np.mean([r["elapsed_sec"] for r in results])),
                    "wall_time_sec": time.time() - t0,
                    "video_dir": str(video_dir),
                    "manifest": str(manifest),
                    "checkpoint": str(job.checkpoint),
                    "dataset": str(job.dataset),
                    "worker_id": args.worker_id,
                    "device": str(device),
                    "max_steps": args.max_steps,
                    "action_horizon": args.action_horizon,
                    "sample_steps": args.sample_steps,
                    "start_seed": args.start_seed,
                    "ckpt_args": {
                        "emb_dim": ckpt_args.get("emb_dim"),
                        "expert_layers": ckpt_args.get("expert_layers"),
                        "chunk_size": ckpt_args.get("chunk_size"),
                        "action_repr": ckpt_args.get("action_repr"),
                    },
                }
                print(json.dumps(summary), flush=True)
                f.write(json.dumps(summary) + "\n")
                log_f.write(json.dumps(summary) + "\n")
                log_f.flush()
            del model
            if device.type == "cuda":
                torch.cuda.empty_cache()


def collect_summaries(output_root: Path) -> list[dict]:
    summaries = []
    for manifest in sorted(output_root.glob("*/*/manifest.jsonl")):
        with manifest.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                if item.get("event") == "summary":
                    summaries.append(item)
    summaries.sort(key=lambda x: (x["run_name"], int(x["epoch"])))
    return summaries


def write_summary(output_root: Path) -> None:
    summaries = collect_summaries(output_root)
    json_path = output_root / "summary.json"
    jsonl_path = output_root / "summary.jsonl"
    csv_path = output_root / "summary.csv"
    md_path = output_root / "SUMMARY.md"

    by_run = collections.defaultdict(list)
    for item in summaries:
        by_run[item["run_name"]].append(item)

    payload = {
        "event": "aggregate_summary",
        "num_checkpoints": len(summaries),
        "runs": {
            run_name: {
                "num_checkpoints": len(items),
                "best_epoch": max(items, key=lambda x: (x["success_rate"], -x["mean_steps"]))["epoch"],
                "best_success_rate": max(x["success_rate"] for x in items),
                "final_epoch_success_rate": items[-1]["success_rate"],
            }
            for run_name, items in sorted(by_run.items())
        },
        "summaries": summaries,
    }
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    with jsonl_path.open("w", encoding="utf-8") as f:
        for item in summaries:
            f.write(json.dumps(item) + "\n")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("run_name,epoch,num_rollouts,successes,success_rate,mean_steps,manifest,video_dir,checkpoint\n")
        for item in summaries:
            f.write(
                f"{item['run_name']},{item['epoch']},{item['num_rollouts']},{item['successes']},"
                f"{item['success_rate']},{item['mean_steps']},{item['manifest']},"
                f"{item['video_dir']},{item['checkpoint']}\n"
            )
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# SmolVLA Square All-Checkpoint Rollout Summary\n\n")
        f.write(f"- Output root: `{output_root}`\n")
        f.write(f"- Completed checkpoints: {len(summaries)}\n")
        f.write("- Each checkpoint uses the same start seed and rollout count recorded in its manifest.\n\n")
        for run_name, items in sorted(by_run.items()):
            best = max(items, key=lambda x: (x["success_rate"], -x["mean_steps"]))
            f.write(f"## {run_name}\n\n")
            f.write(
                f"- Best: epoch {best['epoch']}, {best['successes']}/{best['num_rollouts']} "
                f"= {best['success_rate']:.3f}\n"
            )
            f.write(
                f"- Final: epoch {items[-1]['epoch']}, {items[-1]['successes']}/{items[-1]['num_rollouts']} "
                f"= {items[-1]['success_rate']:.3f}\n\n"
            )
            f.write("| Epoch | Successes | Rollouts | Success rate | Mean steps |\n")
            f.write("| ---: | ---: | ---: | ---: | ---: |\n")
            for item in items:
                f.write(
                    f"| {item['epoch']} | {item['successes']} | {item['num_rollouts']} | "
                    f"{item['success_rate']:.3f} | {item['mean_steps']:.2f} |\n"
                )
            f.write("\n")
    print(json.dumps(payload), flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-base", type=Path, required=True)
    parser.add_argument("--train-module", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--mode", choices=["worker", "summarize"], default="worker")
    parser.add_argument("--num-workers", type=int, default=1)
    parser.add_argument("--worker-id", type=int, default=0)
    parser.add_argument("--num-rollouts", type=int, default=20)
    parser.add_argument("--start-seed", type=int, default=10000)
    parser.add_argument("--max-steps", type=int, default=400)
    parser.add_argument("--action-horizon", type=int, default=8)
    parser.add_argument("--sample-steps", type=int, default=10)
    parser.add_argument("--fps", type=int, default=20)
    parser.add_argument("--video-quality", type=int, default=6)
    parser.add_argument("--device", type=str, default="cuda:0")
    parser.add_argument("--limit-jobs", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.worker_id < 0 or args.worker_id >= args.num_workers:
        raise ValueError("--worker-id must be in [0, --num-workers)")
    return args


def main() -> None:
    args = parse_args()
    if args.mode == "summarize":
        write_summary(args.output_root)
    else:
        run_worker(args)


if __name__ == "__main__":
    main()
