# Session 113 Remote Training Branch Setup

## Goal

Move the runtime patches from the remote training checkout off `main` and onto a task-specific branch before continuing PTP-version environment tests.

## Remote Training Checkout

- Host: `10.100.0.29:36645`
- Path: `/mnt/3fs2/data/tingwen.du/workspace/ldp`
- Previous branch: `main`
- Previous HEAD: `5113f46`
- New branch: `intern_ldp_explorer/task001_ptp_py39_rerun`
- New commit: `529857f`
- Commit message: `Save H200 runtime patches for PTP py39 rerun`

## Saved Runtime Patch

The new branch commit saves 6 runtime files:

- `diffusion_policy/dataset/robomimic_replay_image_dataset.py`
- `diffusion_policy/env_runner/robomimic_image_runner.py`
- `diffusion_policy/env_runner/robomimic_longhist_image_runner.py`
- `diffusion_policy/env_runner/robomimic_square_long_image_runner.py`
- `diffusion_policy/gym_util/async_vector_env.py`
- `diffusion_policy/gym_util/sync_vector_env.py`

Patch summary:

- Add cached-embedding/image-normalizer compatibility in `robomimic_replay_image_dataset.py`.
- Use `AsyncVectorEnv(..., shared_memory=False)` in RoboMimic image runners.
- Add newer Gym reset/seed compatibility and corrected `concatenate` argument order in vector-env utilities.

The untracked `MUJOCO_LOG.TXT` file was left uncommitted because it is a runtime log, not a source change.

## Push Status

The remote training checkout has `origin=https://github.com/long-context-dp/ldp.git` and a `steven` remote pointing to `git@github.com:StevenKKXS/ldp.git`.

An attempted push of `intern_ldp_explorer/task001_ptp_py39_rerun` from the training host did not return promptly, consistent with SSH/GitHub authentication waiting on the training machine. I terminated that local push process. The branch and commit are saved in the shared training checkout; the task branch in the main work-agent repo contains this record and has been pushed.

## PTP Environment Smoke On New Branch

Checked under `/root/ptp_ldp_py39` on the new remote branch:

- `/root/ptp_ldp_py3` does not exist.
- `/root/ptp_ldp_py39` exists and is the intended PTP-version venv.
- Python `3.9.25`
- Torch `2.5.1`
- RoboMimic `0.2.0`
- RoboSuite `1.2.0`
- MuJoCo `2.3.7`
- `mujoco-py 2.1.2.14`
- Diffusers `0.11.1`
- Gym `0.21.0`

Import smoke passed for:

- `diffusion_policy.env_runner.robomimic_image_runner`
- `diffusion_policy.env_runner.robomimic_longhist_image_runner`
- `diffusion_policy.dataset.robomimic_replay_image_dataset`
- `diffusion_policy.policy.diffusion_transformer_hybrid_image_policy`

RoboSuite registration smoke:

- `ToolHang`: registered
- `TwoArmTransport`: registered

GPU check at the end:

- `36645` has 4 visible H200 GPUs, all idle at about `1 MiB` memory and `0%` utilization.
