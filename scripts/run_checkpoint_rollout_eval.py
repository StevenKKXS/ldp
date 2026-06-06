#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import sys

import dill
import hydra
import torch
import wandb
from omegaconf import open_dict

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
os.chdir(ROOT_DIR)


def _jsonify(value):
    if isinstance(value, wandb.sdk.data_types.video.Video):
        return value._path
    if hasattr(value, "item"):
        return value.item()
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--n-train", type=int, default=0)
    parser.add_argument("--n-test", type=int, default=1)
    parser.add_argument("--n-envs", type=int, default=1)
    parser.add_argument("--n-train-vis", type=int, default=0)
    parser.add_argument("--n-test-vis", type=int, default=0)
    parser.add_argument("--max-steps", type=int, default=50)
    parser.add_argument("--num-inference-steps", type=int, default=None)
    args = parser.parse_args()

    os.environ.setdefault("WANDB_MODE", "disabled")
    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = torch.load(open(args.checkpoint, "rb"), pickle_module=dill)
    cfg = payload["cfg"]

    with open_dict(cfg):
        cfg.task.env_runner.n_train = args.n_train
        cfg.task.env_runner.n_test = args.n_test
        cfg.task.env_runner.n_envs = args.n_envs
        cfg.task.env_runner.n_train_vis = args.n_train_vis
        cfg.task.env_runner.n_test_vis = args.n_test_vis
        cfg.task.env_runner.max_steps = args.max_steps

    cls = hydra.utils.get_class(cfg._target_)
    workspace = cls(cfg, output_dir=str(output_dir))
    workspace.load_payload(payload, exclude_keys=None, include_keys=None)

    policy = workspace.ema_model if cfg.training.use_ema else workspace.model
    if args.num_inference_steps is not None:
        policy.num_inference_steps = args.num_inference_steps
    policy.to(torch.device(args.device))
    policy.eval()

    wandb.init(
        dir=str(output_dir),
        project="ptp_encoder_rollout_eval",
        mode=os.environ.get("WANDB_MODE", "disabled"),
        config={
            "checkpoint": args.checkpoint,
            "n_train": args.n_train,
            "n_test": args.n_test,
            "n_envs": args.n_envs,
            "max_steps": args.max_steps,
            "num_inference_steps": policy.num_inference_steps,
        },
    )

    env_runner = hydra.utils.instantiate(cfg.task.env_runner, output_dir=str(output_dir))
    runner_log = env_runner.run(policy)
    json_log = {key: _jsonify(value) for key, value in runner_log.items()}
    with open(output_dir / "eval_log.json", "w") as f:
        json.dump(json_log, f, indent=2, sort_keys=True)
    print(json.dumps(json_log, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
