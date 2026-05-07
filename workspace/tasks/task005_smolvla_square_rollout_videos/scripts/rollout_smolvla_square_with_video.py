#!/usr/bin/env python3
"""Run compact SmolVLA-style square rollouts and save side-by-side videos.

This script is stored in the repo for reproducibility. The actual generated
MP4 files are written under the task-owned `/mnt/3fs2/.../task005...` path.
"""

from __future__ import annotations

import argparse
import collections
import copy
import importlib.util
import json
import random
import sys
import time
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


def load_train_module(path: Path):
    spec = importlib.util.spec_from_file_location("smolvla_formal_train", str(path))
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
    img = obs[key]
    if img.shape[0] == 3:
        img = np.moveaxis(img, 0, -1)
    if img.dtype != np.uint8:
        if img.max() <= 2.0:
            img = img * 255.0
        img = np.clip(img, 0, 255).astype(np.uint8)
    return img


def make_frame(obs: dict) -> np.ndarray:
    return np.concatenate([obs_image_to_uint8(obs, IMAGE_KEYS[0]), obs_image_to_uint8(obs, IMAGE_KEYS[1])], axis=1)


def obs_to_batch(obs: dict, stats: dict, device: torch.device) -> dict[str, torch.Tensor]:
    images = []
    for key in IMAGE_KEYS:
        img = obs[key]
        if img.shape[-1] == 3:
            img = np.moveaxis(img, -1, 0)
        img = img.astype(np.float32)
        if img.max() > 2.0:
            img = img / 255.0
        images.append(torch.from_numpy(img).unsqueeze(0).to(device=device, dtype=torch.float32))
    state = np.concatenate([np.asarray(obs[k], dtype=np.float32) for k in STATE_KEYS], axis=-1)
    state = (state - np.asarray(stats["state_mean"], dtype=np.float32)) / np.asarray(stats["state_std"], dtype=np.float32)
    return {"image0": images[0], "image1": images[1], "state": torch.from_numpy(state).unsqueeze(0).to(device=device)}


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
    env = EnvUtils.create_env_from_metadata(env_meta=env_meta, render=False, render_offscreen=True, use_image_obs=True)
    env.env.hard_reset = False
    return env


def load_policy(args: argparse.Namespace, device: torch.device):
    module = load_train_module(args.train_module)
    payload = torch.load(args.checkpoint, map_location=device)
    stats = payload["stats"]
    ckpt_args = payload["args"]
    model = module.SmolVLALikePolicy(
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
    return model, stats


@torch.no_grad()
def predict_chunk(model, obs: dict, stats: dict, device: torch.device, sample_steps: int) -> np.ndarray:
    batch = obs_to_batch(obs, stats, device)
    norm_action = model.sample_actions(batch, steps=sample_steps)[0].detach().cpu().numpy()
    return ldp_abs10_to_abs7(norm_action, stats)


def run_episode(model, env, stats: dict, args: argparse.Namespace, seed: int, device: torch.device) -> dict:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)
    tmp_video = args.video_dir / f"seed_{seed}_tmp.mp4"
    writer = imageio.get_writer(str(tmp_video), fps=args.fps, codec="libx264", quality=8, macro_block_size=1)
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
    final_video = args.video_dir / f"seed_{seed}_{'success' if success else 'fail'}_{steps}steps.mp4"
    if final_video.exists():
        final_video.unlink()
    tmp_video.rename(final_video)
    return {"seed": seed, "success": success, "steps": steps, "max_reward": max(rewards) if rewards else 0.0, "elapsed_sec": time.time() - t0, "video": str(final_video), "first_action": first_action}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--train-module", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--video-dir", type=Path, required=True)
    parser.add_argument("--num-rollouts", type=int, default=20)
    parser.add_argument("--start-seed", type=int, default=10000)
    parser.add_argument("--max-steps", type=int, default=400)
    parser.add_argument("--action-horizon", type=int, default=8)
    parser.add_argument("--sample-steps", type=int, default=10)
    parser.add_argument("--fps", type=int, default=20)
    parser.add_argument("--device", type=str, default="cuda:0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.video_dir.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    device = torch.device(args.device if torch.cuda.is_available() and args.device.startswith("cuda") else "cpu")
    model, stats = load_policy(args, device)
    env = create_square_env(args.dataset)
    results = []
    with args.manifest.open("w", encoding="utf-8") as f:
        for idx in range(args.num_rollouts):
            result = run_episode(model, env, stats, args, args.start_seed + idx, device)
            results.append(result)
            line = {"event": "episode", **result}
            print(json.dumps(line), flush=True)
            f.write(json.dumps(line) + "\n")
            f.flush()
        successes = sum(int(r["success"]) for r in results)
        summary = {"event": "summary", "num_rollouts": args.num_rollouts, "successes": successes, "success_rate": successes / max(args.num_rollouts, 1), "mean_steps": float(np.mean([r["steps"] for r in results])), "video_dir": str(args.video_dir), "checkpoint": str(args.checkpoint), "dataset": str(args.dataset)}
        print(json.dumps(summary), flush=True)
        f.write(json.dumps(summary) + "\n")


if __name__ == "__main__":
    main()
