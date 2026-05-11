# task002_remaining_baselines_push_t_aloha_longsquare_transport - History Log

<!-- METADATA:SESSION=2 -->

## Session 2 - 2026-05-11 - Push-T / LH-ALOHA 2x2 a8 Launch

**Executor**: intern_ldp_explorer

- Launched the p39-style 2x2 a8 baseline batch requested by the user:
- Push-T DP / PTP
- LH-ALOHA DP / PTP
- Launch script:
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/scripts/session136_launch_ptp_py39_pusht_aloha_2x2_a8_2000ep.sh`
- Output root:
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/outputs/session136_ptp_py39_pusht_aloha_2x2_a8_2000ep_20260511_084500`
- Log root:
- `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session136_ptp_py39_pusht_aloha_2x2_a8_2000ep_20260511_084500`
- Common settings:
- `global_obs=16`, `global_horizon=32`, `global_action=8`
- `training.num_epochs=2000`
- `training.rollout_every=100`, `training.checkpoint_every=100`
- `task.env_runner.n_test=100`, `task.env_runner.n_test_vis=4`
- `dataloader.batch_size=64`
- PTP uses `policy.past_action_pred=true`, DP uses `policy.past_action_pred=false`, and both use `policy.past_steps_reg=-1`.
- Preflight issues fixed:
- Push-T needed `+policy.use_embed_if_present=false`.
- LH-ALOHA needed `threadpoolctl==3.1.0` installed into `/root/ptp_ldp_py39`.
- Current progress sample:
- LH-ALOHA DP/PTP reached epoch `99` and are in their first `n_test=100` rollout; each has generated `4` mp4 files but has not written `test_mean_score` yet.
- Push-T DP/PTP reached epoch `67`; no rollout score yet.

## Session 1 - 2026-05-10 - Push-T / LH-ALOHA Environment Setup

**Executor**: intern_ldp_explorer

- Configured the PTP-style Python 3.9 environment on two new servers dedicated to Push-T and LH-ALOHA:
- `10.100.2.35:33486`
- `10.100.16.46:36566`
- Both servers have `2 x NVIDIA H200` with `143771 MiB` each and were idle after setup.
- Installed `/root/ptp_ldp_py39` with Python `3.9.25`, torch `2.5.1`, robomimic `0.2.0`, robosuite `1.2.0`, `mujoco-py==2.1.2.14`, `mujoco==2.3.7`, `dm-control==1.0.9`, `gym==0.21.0`, and Push-T/LH-ALOHA extras.
- Applied required compatibility fixes:
- install robosuite with `--no-deps` to avoid the wrong `mujoco-py==2.0.2.9` dependency
- pin `Cython==0.29.32`, `numpy==1.23.3`, and `setuptools==65.5.0`
- copy the local pure-Python `pytorch3d.transforms` stub into the venv
- Passed Push-T import and dataset smoke on both servers.
- Passed LH-ALOHA import, HDF5 structure, and `make_sim_env("sim_singlearm_pickandplace_twomodes_scripted").reset()` smoke on both servers.
- Reusable setup note:
- `workspace/tasks/task002_remaining_baselines_push_t_aloha_longsquare_transport/session001_push_t_lh_aloha_env_setup.md`

---

## Session 0 - 2026-05-10 - Initialization

**Executor**: intern_ldp_explorer

- Created the task at the user's request after closing the first-stage reproduction task.
- Task objective:
- run the remaining baselines and improve them into usable comparison baselines where possible.
- Initial target set:
- Push-T
- LH-ALOHA
- Long Square
- Transport
- Initial operating assumption:
- use the PTP-compatible Python 3.9 / robomimic 0.2.0 / robosuite 1.2.0 environment for Robomimic-style tasks unless a task requires a separate stack.

---
