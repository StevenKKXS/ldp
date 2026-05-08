# Session 111 Requirement Check: PTP-Version Environment 4x2x2 Rerun

## User Request

Run the same 4x2x2 setup as the stopped Session 89/110 batch, but switch the environment to the PTP-recommended stack before training and rollout.

Interpreted experiment matrix:

- 4 tasks: Square, Tool-Hang, Transport, LongSquare
- 2 methods: DP / no-PTP and PTP
- 2 action horizons: `global_action=8` and `global_action=1`
- Total: 16 runs

## Requirement Check

The request is technically valid and directly targets the main confound identified in Session 110: the previous run used the H200 compatibility environment (`robomimic 0.3.0`, `robosuite 1.4.1`, `mujoco 3.8.0`) instead of the upstream PTP-style environment.

The rerun should be treated as a clean environment-version ablation, not as a continuation of the stopped batch.

## PTP-Version Environment Status

Available on `10.100.0.29:36645`:

- venv: `/root/ptp_ldp_py39`
- Python: `3.9.25`
- Torch: `2.5.1`
- RoboMimic: `0.2.0`
- RoboSuite: pinned `cheng-chi/robosuite@277ab9588ad7a4f4b55cf75508b44aa67ec171f0`, source version `1.2.0`
- MuJoCo binary for `mujoco-py`: `2.1.0`
- `mujoco-py`: `2.1.2.14`
- `mujoco`: `2.3.7`
- `diffusers`: `0.11.1`
- `gym`: `0.21.0`

Important adaptation:

- This is still H200-adapted, not byte-for-byte upstream conda: Torch is `2.5.1/cu124` instead of old `1.12.1/cu116`.
- `av` was adapted to `15.1.0` because Ubuntu 24.04 FFmpeg 6 does not build the old pinned `av 10.0.0`.

GPU status:

- `36645`: 4 x H200, idle at the time of checking.
- `30103`: 4 x H200, idle, but `/root/ptp_ldp_py39` is not present there.

## Items That Need Confirmation

1. GPU placement:
   - Recommended: run all 16 jobs on `36645` using its 4 GPUs, because the PTP-version venv already exists there.
   - Alternative: configure/sync `/root/ptp_ldp_py39` onto `30103` before using all 8 GPUs.

2. Run order:
   - Recommended: PTP first, then DP for each task/action lane, so the main environment-version signal appears earlier.
   - Alternative: DP first, then PTP, matching the original Session 89 launch script order.

3. Training length:
   - Recommended: keep `training.num_epochs=2000`, matching the stopped batch.
   - This is longer than the paper's default 500-epoch statement, but keeps the comparison controlled against Session 110.

4. Rollout and video:
   - Recommended: keep `training.rollout_every=100`, `task.env_runner.n_test=100`, `task.env_runner.n_test_vis=4`, `task.env_runner.n_train_vis=2`.
   - This means training-time rollout every 100 epochs plus saved visual rollouts from the runner, not a separate 3-seed final evaluation.

5. Code state:
   - The remote training repo used by the venv is `/mnt/3fs2/data/tingwen.du/workspace/ldp`.
   - It is currently on `main` at short hash `5113f46` with local modifications in several runtime files.
   - Because `/root/ptp_ldp_py39` was installed editable from this repo and Session 107 smoke passed there, the lowest-risk option is to run from this same code path and record `git status` / `git diff` into the new log directory before launch.

6. Pre-launch smoke:
   - Required before starting 16 training jobs:
   - verify imports under `/root/ptp_ldp_py39`
   - verify Square, Tool-Hang, Transport, and LongSquare dataset open
   - verify env reset and `reset_to` for all four tasks where supported
   - verify one tiny video write/read

## Proposed Execution Plan After Confirmation

1. Create a new launch script, for example `session111_launch_ptp_env_4x2x2_2000ep.sh`.
2. Use output root:
   - `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/outputs/session111_ptp_env_4x2x2_2000ep_<stamp>/`
3. Use log root:
   - `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session111_ptp_env_4x2x2_2000ep_<stamp>/`
4. Run pre-launch smoke under `/root/ptp_ldp_py39`.
5. If smoke passes, launch 16 runs with:
   - `global_obs=16`
   - `global_horizon=32`
   - `global_action in {8,1}`
   - `training.seed=42`
   - `training.num_epochs=2000`
   - `dataloader.batch_size=64`
   - `val_dataloader.batch_size=64`
   - `training.rollout_every=100`
   - `training.checkpoint_every=100`
   - `task.env_runner.n_test=100`
   - `policy.past_steps_reg=-1`
6. Monitor first rollout and report early success-rate / failure signatures.

## Assessment

No conceptual issue with the user's requested experiment. The main operational issue is that the PTP-version venv currently exists only on `36645`, so either run on those 4 GPUs or first install the same venv on `30103`. The main reproducibility issue is the dirty remote repo state; it should be recorded exactly before launch.
