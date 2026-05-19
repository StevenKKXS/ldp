import argparse
import json
import math
import os
import pathlib
import sys

import dill
import hydra
import numpy as np
import torch
from omegaconf import OmegaConf

from diffusion_policy.common.pytorch_util import dict_apply


def run_reward_only(policy, runner):
    env = runner.env
    n_envs = len(runner.env_fns)
    n_inits = len(runner.env_init_fn_dills)
    n_chunks = math.ceil(n_inits / n_envs)
    all_rewards = [None] * n_inits

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

            rewards = env.call("get_attr", "reward")[:active]
            all_rewards[start:end] = rewards
    finally:
        try:
            env.close()
        except Exception:
            pass

    return [float(np.max(x)) for x in all_rewards]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--n-test", type=int, default=10)
    parser.add_argument("--n-envs", type=int, default=10)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--dataset-path", default=None)
    parser.add_argument("--use-model", action="store_true")
    args = parser.parse_args()

    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = torch.load(open(args.checkpoint, "rb"), pickle_module=dill, map_location="cpu")
    cfg = payload["cfg"]
    OmegaConf.set_struct(cfg, False)

    cfg.task.env_runner.n_train = 0
    cfg.task.env_runner.n_train_vis = 0
    cfg.task.env_runner.n_test = args.n_test
    cfg.task.env_runner.n_test_vis = 0
    cfg.task.env_runner.n_envs = args.n_envs
    cfg.task.env_runner.tqdm_interval_sec = 1.0
    if args.max_steps is not None:
        cfg.task.env_runner.max_steps = args.max_steps
    if args.dataset_path is not None:
        cfg.task.dataset_path = args.dataset_path
        cfg.task.env_runner.dataset_path = args.dataset_path

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
    scores = run_reward_only(policy, runner)
    result = {
        "checkpoint": os.path.abspath(args.checkpoint),
        "output_dir": str(output_dir),
        "policy_source": policy_source,
        "n_test": args.n_test,
        "n_envs": args.n_envs,
        "max_steps": int(cfg.task.env_runner.max_steps),
        "scores": scores,
        "mean_score": float(np.mean(scores)) if scores else None,
    }

    with open(output_dir / "eval_log.json", "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
