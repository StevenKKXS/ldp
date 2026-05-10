# Session 131 Phase 1 Closeout Notes

<!-- METADATA:SESSION=131 -->

## Phase 1 Status

Phase 1 can be closed as a first-pass reproduction / diagnosis stage.

The useful outcome is not a full final paper reproduction, but a clear isolation result:

- The modern H200 stack (`/root/venv`, robomimic `0.3.0`, robosuite `1.4.1`) produced mostly zero success.
- Action horizon `1` vs `8` did not explain the failures.
- The PTP-aligned py39 stack (`/root/ptp_ldp_py39`, robomimic `0.2.0`, robosuite source version `1.2.0`) recovered strong Square and Tool-Hang PTP results.
- Current Phase 2 should focus on `global_action=8` only, because `a1` is slower and not changing the current conclusions.

The primary Phase 1 report is:

- `workspace/tasks/task001_reproduce_ldp_ptp_baseline_h200/session126_4x2x2_report.md`

## Environment Requirements For Phase 2

Use the PTP-compatible environment as the default for Phase 2:

| Component | Required / Known-Good Value |
|---|---|
| Python env | `/root/ptp_ldp_py39` |
| Python | `3.9.25` |
| torch / torchvision | `2.5.1` / `0.20.1` |
| robomimic | `0.2.0` |
| robosuite | pinned `cheng-chi/robosuite@277ab9588ad7a4f4b55cf75508b44aa67ec171f0`, source version `1.2.0` |
| mujoco / mujoco-py | `2.3.7` / `2.1.2.14` |
| gym | `0.21.0` |
| diffusers | `0.11.1` |
| huggingface-hub | `0.10.1` |

Avoid using `/root/venv` for the main reproduction line unless the explicit goal is to compare against the failed modern stack. That environment reports Python `3.12.3`, robomimic `0.3.0`, robosuite `1.4.1`, MuJoCo `3.8.0`, gym `0.25.2`, and was the stack that produced the near-zero results.

## Code / Branch Requirements

Phase 2 should start from the runtime-patched training branch rather than a clean `main` checkout on the GPU machine:

- branch: `intern_ldp_explorer/task001_ptp_py39_rerun`
- recorded commit: `529857fa8bab663510d88c5c7b72b973f4c37104`

The important runtime patches are:

- `diffusion_policy/dataset/robomimic_replay_image_dataset.py`
- `diffusion_policy/env_runner/robomimic_image_runner.py`
- `diffusion_policy/env_runner/robomimic_longhist_image_runner.py`
- `diffusion_policy/env_runner/robomimic_square_long_image_runner.py`
- `diffusion_policy/gym_util/async_vector_env.py`
- `diffusion_policy/gym_util/sync_vector_env.py`

The most critical compatibility point is Gym vector concatenation: `/root/ptp_ldp_py39` uses Gym `0.21.0`, where `gym.vector.utils.concatenate` uses the `(items, out, space)` argument order. Without the wrapper patch in the vector env files, rollout can fail at the first evaluation boundary.

## Dataset / Encoder Requirements

Keep training and rollout paths separate for the compact embedding datasets:

| Task | Training HDF5 | Rollout / env HDF5 | Encoder |
|---|---|---|---|
| Square | `.../square/mh/image_abs_emb.hdf5` | `.../square/mh/image_abs.hdf5` | `square_encoder.ckpt` |
| Tool-Hang | `.../tool_hang/ph/image_abs_emb_compact.hdf5` | `.../tool_hang/ph/image_abs.hdf5` | `tool_hang_encoder.ckpt` |
| Transport | `.../transport/mh/image_abs_emb_compact.hdf5` | `.../transport/mh/image_abs.hdf5` | `transport_encoder.ckpt` |
| Long Square | `.../longhistsquare100/image.hdf5` | same file | `longhist_encoder.ckpt` |

Compact embedding HDF5 files are for cached training. Do not use compact embedding files as raw rollout sources, because raw rollout should use the HDF5 with full image / env metadata.

## Phase 2 Experiment Defaults

Use these defaults unless the new task explicitly changes them:

- `global_obs=16`
- `global_horizon=32`
- `global_action=8`
- `policy.past_steps_reg=-1`
- DP / no-PTP: `policy.past_action_pred=false`
- PTP: `policy.past_action_pred=true`
- cached embeddings enabled for training
- frozen released visual encoders
- final comparison eval: `n_test=100`, `n_samples=1`, saved mp4

Do not spend new GPU time on `global_action=1` in the main loop. Existing a1 results are enough to support the claim that action horizon was not the main failure cause.

## Phase 2 Priorities

1. Square PTP a8 and Tool-Hang PTP a8: fixed selected-checkpoint eval with `n_test=100` and mp4 artifacts.
2. Transport a8: focused continuation / rerun because PTP a8 reached only `0.30` from an early checkpoint.
3. Long Square a8: focused continuation / rerun because PTP a8 reached only `0.24` and the task is long-horizon.
4. DP baselines: keep a8-only unless a reviewer asks for action-horizon ablation.

## Operational Notes

- The most recent known GPU SSH entries `10.100.0.29:36645` and `10.100.0.29:30103` are currently unreachable from this workspace with `Connection refused`.
- Shared storage remains readable under `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer`.
- GPU training machines may be offline / no-network; push code and records from the CPU workspace.
- If a rollout lane fails with MuJoCo or IK instability, prefer lowering rollout parallelism for diagnostic reruns before discarding the checkpoint.
