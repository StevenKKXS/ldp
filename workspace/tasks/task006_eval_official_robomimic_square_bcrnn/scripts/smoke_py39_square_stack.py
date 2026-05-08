#!/usr/bin/env python3
"""Smoke test for the py39 / robomimic 0.2 Square stack."""

from __future__ import annotations

import argparse
import collections
import copy
import importlib
import importlib.metadata as md
import json
from pathlib import Path

import h5py
import imageio
import numpy as np
import torch

import robomimic.utils.env_utils as EnvUtils
import robomimic.utils.file_utils as FileUtils
import robomimic.utils.obs_utils as ObsUtils


STATE_KEYS = ("robot0_eef_pos", "robot0_eef_quat", "robot0_gripper_qpos")
IMAGE_KEYS = ("agentview_image", "robot0_eye_in_hand_image")


def package_version(name: str) -> str:
    try:
        return md.version(name)
    except md.PackageNotFoundError:
        return "not-installed"


def inspect_dataset(path: Path) -> dict:
    with h5py.File(path, "r") as f:
        demos = sorted(f["data"].keys())
        steps = sum(int(f["data"][demo].attrs.get("num_samples", f["data"][demo]["actions"].shape[0])) for demo in demos)
        first = f["data"][demos[0]]
        env_args = json.loads(f["data"].attrs.get("env_args", "{}"))
        return {
            "path": str(path),
            "demos": len(demos),
            "steps": steps,
            "first_demo": demos[0],
            "action_shape": list(first["actions"].shape),
            "obs_keys": sorted(first["obs"].keys()),
            "env_name": env_args.get("env_name"),
            "env_version": env_args.get("env_version"),
        }


def make_frame(obs: dict) -> np.ndarray:
    frames = []
    for key in IMAGE_KEYS:
        img = np.asarray(obs[key])
        if img.shape[0] == 3:
            img = np.moveaxis(img, 0, -1)
        if img.dtype != np.uint8:
            if img.max() <= 2.0:
                img = img * 255.0
            img = np.clip(img, 0, 255).astype(np.uint8)
        frames.append(img)
    return np.concatenate(frames, axis=1)


def create_env(dataset: Path):
    modality_mapping = collections.defaultdict(list)
    modality_mapping["rgb"].extend(IMAGE_KEYS)
    modality_mapping["low_dim"].extend(STATE_KEYS)
    ObsUtils.initialize_obs_modality_mapping_from_dict(modality_mapping)

    env_meta = copy.deepcopy(FileUtils.get_env_metadata_from_dataset(str(dataset)))
    env_meta["env_kwargs"]["use_object_obs"] = False
    env_meta["env_kwargs"]["controller_configs"]["control_delta"] = False
    env = EnvUtils.create_env_from_metadata(
        env_meta=env_meta,
        render=False,
        render_offscreen=True,
        use_image_obs=True,
    )
    env.env.hard_reset = False
    return env


def run_env_video(dataset: Path, video: Path, steps: int) -> dict:
    with h5py.File(dataset, "r") as f:
        first_demo = sorted(f["data"].keys())[0]
        action_dim = int(f["data"][first_demo]["actions"].shape[-1])

    env = create_env(dataset)
    obs = env.reset()
    video.parent.mkdir(parents=True, exist_ok=True)
    writer = imageio.get_writer(str(video), fps=10, codec="libx264", quality=6, macro_block_size=1)
    writer.append_data(make_frame(obs))
    for _ in range(steps):
        obs, reward, done, _ = env.step(np.zeros((action_dim,), dtype=np.float32))
        writer.append_data(make_frame(obs))
        if done:
            break
    writer.close()
    success = bool(env.is_success().get("task", False))
    return {"video": str(video), "action_dim": action_dim, "success_after_zero_action": success}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--steps", type=int, default=3)
    args = parser.parse_args()

    imports = [
        "diffusion_policy.env_runner.robomimic_image_runner",
        "diffusion_policy.env_runner.robomimic_longhist_image_runner",
        "diffusion_policy.dataset.robomimic_replay_image_dataset",
        "diffusion_policy.policy.diffusion_transformer_hybrid_image_policy",
    ]
    for name in imports:
        module = importlib.import_module(name)
        print("IMPORT_OK", name, getattr(module, "__file__", None))

    print("PYTORCH_CUDA", torch.__version__, torch.cuda.is_available(), torch.cuda.device_count())
    for pkg in ["robomimic", "robosuite", "mujoco", "mujoco-py", "diffusers", "gym"]:
        print("PKG", pkg, package_version(pkg))
    print("DATASET", json.dumps(inspect_dataset(args.dataset), sort_keys=True))
    print("ENV_VIDEO", json.dumps(run_env_video(args.dataset, args.video, args.steps), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
