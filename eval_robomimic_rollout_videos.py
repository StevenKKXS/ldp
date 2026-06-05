"""Generate Robomimic rollout videos from a workspace checkpoint.

This is a video-only companion to eval_flow_matching_rollout.py. It avoids the
runner's online HSIC / wandb logging path and only records rollout scores plus
the generated video files.
"""

import argparse
import json
import math
import os
import pathlib
import shutil
import sys

import dill
import hydra
import numpy as np
import torch
from omegaconf import OmegaConf

from diffusion_policy.common.pytorch_util import dict_apply


def patch_h264_profile(profile):
    """Patch VideoRecorder.create_h264 for PyAV versions that reject profiles."""
    from diffusion_policy.real_world.video_recorder import VideoRecorder

    def create_h264(
        cls,
        fps,
        codec="h264",
        input_pix_fmt="rgb24",
        output_pix_fmt="yuv420p",
        crf=18,
        profile=profile,
        **kwargs,
    ):
        options = {"crf": str(crf)}
        if profile:
            options["profile"] = profile
        return cls(
            fps=fps,
            codec=codec,
            input_pix_fmt=input_pix_fmt,
            pix_fmt=output_pix_fmt,
            options=options,
            **kwargs,
        )

    VideoRecorder.create_h264 = classmethod(create_h264)


def run_video_rollout(policy, runner):
    env = runner.env
    n_envs = len(runner.env_fns)
    n_inits = len(runner.env_init_fn_dills)
    n_chunks = math.ceil(n_inits / n_envs)
    all_rewards = [None] * n_inits
    all_video_paths = [None] * n_inits

    try:
        for chunk_idx in range(n_chunks):
            start = chunk_idx * n_envs
            end = min(n_inits, start + n_envs)
            active = end - start

            init_fns = list(runner.env_init_fn_dills[start:end])
            if len(init_fns) < n_envs:
                init_fns.extend([runner.env_init_fn_dills[0]] * (n_envs - len(init_fns)))
            assert len(init_fns) == n_envs

            env.call_each("run_dill_function", args_list=[(x,) for x in init_fns])
            obs = env.reset()
            past_action = None
            policy.reset()

            done = False
            while not done:
                np_obs_dict = dict(obs)
                if runner.past_action and past_action is not None:
                    np_obs_dict["past_action"] = past_action[
                        :, -(runner.n_obs_steps - 1):
                    ].astype(np.float32)

                device = policy.device
                obs_dict = dict_apply(
                    np_obs_dict,
                    lambda x: torch.from_numpy(x).to(device=device),
                )

                with torch.no_grad():
                    action_dict = policy.predict_action(obs_dict)

                np_action_dict = dict_apply(
                    action_dict,
                    lambda x: x.detach().to("cpu").numpy(),
                )
                action = np_action_dict["action"]
                if not np.all(np.isfinite(action)):
                    raise RuntimeError("policy produced non-finite actions")

                env_action = runner.undo_transform_action(action) if runner.abs_action else action
                obs, reward, done, info = env.step(env_action)
                done = np.all(done)
                past_action = action

            all_video_paths[start:end] = env.render()[:active]
            rewards = env.call("get_attr", "reward")[:active]
            all_rewards[start:end] = rewards

        _ = env.reset()
    finally:
        try:
            env.close()
        except Exception:
            pass

    scores = [float(np.max(x)) for x in all_rewards]
    return scores, all_video_paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--n-test", type=int, default=10)
    parser.add_argument("--n-envs", type=int, default=10)
    parser.add_argument("--n-videos", type=int, default=10)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--dataset-path", default=None)
    parser.add_argument("--test-start-seed", type=int, default=None)
    parser.add_argument("--use-model", action="store_true")
    parser.add_argument(
        "--h264-profile",
        default=None,
        help="H264 profile to pass to PyAV. Default omits profile for av==14.2 compatibility.",
    )
    args = parser.parse_args()

    patch_h264_profile(args.h264_profile)

    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = torch.load(open(args.checkpoint, "rb"), pickle_module=dill, map_location="cpu")
    cfg = payload["cfg"]
    OmegaConf.set_struct(cfg, False)

    cfg.task.env_runner.n_train = 0
    cfg.task.env_runner.n_train_vis = 0
    cfg.task.env_runner.n_test = args.n_test
    cfg.task.env_runner.n_test_vis = args.n_videos
    cfg.task.env_runner.n_envs = args.n_envs
    cfg.task.env_runner.tqdm_interval_sec = 1.0
    if args.max_steps is not None:
        cfg.task.env_runner.max_steps = args.max_steps
    if args.dataset_path is not None:
        cfg.task.dataset_path = args.dataset_path
        cfg.task.env_runner.dataset_path = args.dataset_path
    if args.test_start_seed is not None:
        cfg.task.env_runner.test_start_seed = args.test_start_seed

    workspace_cls = hydra.utils.get_class(cfg._target_)
    workspace = workspace_cls(cfg, output_dir=str(output_dir))
    workspace.load_payload(payload)

    if args.use_model or (not cfg.training.use_ema) or workspace.ema_model is None:
        policy = workspace.model
        policy_source = "model"
    else:
        policy = workspace.ema_model
        policy_source = "ema_model"

    device = torch.device(args.device)
    policy.to(device)
    policy.eval()

    runner = hydra.utils.instantiate(cfg.task.env_runner, output_dir=str(output_dir))
    scores, raw_video_paths = run_video_rollout(policy, runner)

    video_dir = output_dir / "videos"
    video_dir.mkdir(exist_ok=True)
    copied_video_paths = []
    seeds = list(getattr(runner, "env_seeds", []))
    for idx, src in enumerate(raw_video_paths):
        if src is None:
            copied_video_paths.append(None)
            continue
        seed = seeds[idx] if idx < len(seeds) else idx
        score = int(scores[idx]) if idx < len(scores) else -1
        dst = video_dir / f"rollout_{idx:02d}_seed_{seed}_score_{score}.mp4"
        shutil.copy2(src, dst)
        copied_video_paths.append(str(dst))

    result = {
        "checkpoint": os.path.abspath(args.checkpoint),
        "output_dir": str(output_dir),
        "policy_source": policy_source,
        "n_test": args.n_test,
        "n_envs": args.n_envs,
        "n_videos": args.n_videos,
        "max_steps": int(cfg.task.env_runner.max_steps),
        "scores": scores,
        "mean_score": float(np.mean(scores)) if scores else None,
        "raw_video_paths": raw_video_paths,
        "video_paths": copied_video_paths,
    }

    with open(output_dir / "eval_log.json", "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
