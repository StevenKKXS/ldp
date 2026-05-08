# Current Work Handoff

<!-- METADATA:SESSION=21 -->

## Purpose

This file is the durable handoff record for the active Square experiments. It records the GPU entries, running jobs, data versions, output roots, script entry points, and the migration plan for the future H200 Python 3.9 + robomimic 0.2.0 environment.

All paths for this task stay under:

- `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn`
- task scripts under `/work-agents/intern_method_developer/ldp/workspace/tasks/task006_eval_official_robomimic_square_bcrnn`

Do not write experiment outputs to other users' storage.

## Active GPU Inventory

### `10.100.16.46:23989`

- Hostname: `lg-cmc-b7r202-h08u16-h200-000548`
- Visible GPUs: 2x NVIDIA H200, `/mnt/3fs2` mounted.
- Purpose: four-way SmolVLA Square training and automatic post-training rollout.
- Last verified GPU state on 2026-05-08 14:25 UTC:
  - GPU0: about 3431 MiB used, about 93% utilization.
  - GPU1: about 3435 MiB used, about 95% utilization.

Live SmolVLA processes:

| PID | Run |
| --- | --- |
| `27745` | `smolvla_small_ptp_ldp_mh_abs10_seed52` |
| `27774` | `smolvla_big384_ptp_ldp_mh_abs10_seed53` |
| `27801` | `smolvla_big384_official_ph_v141_abs10_seed54` |
| `27816` | `smolvla_small_official_ph_v141_abs10_seed55` |
| `62177` | post-training monitor `monitor_smolvla_fourway_rollout_best50.sh` |

SmolVLA roots:

- Run root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/smolvla_fourway_1000ep_20260508_130111`
- Training log root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/logs/smolvla_fourway_1000ep_20260508_130111`
- Monitor log root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/logs/smolvla_fourway_rollout_after_train_20260508_132807`
- Planned all-checkpoint rollout root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_fourway_all_ckpts_20rollouts_20260508_132807`
- Planned best-checkpoint 50-rollout root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_fourway_best_ckpts_50rollouts_20260508_132807`
- Planned report: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/reports/smolvla_fourway_rollout_after_train_20260508_132807.md`

Latest SmolVLA progress:

| Run | Latest eval epoch | Latest offline metric | Named ckpts |
| --- | ---: | ---: | ---: |
| `smolvla_big384_official_ph_v141_abs10_seed54` | 700 | `val_sample_action_mse=0.16597552597522736` | 16 |
| `smolvla_small_official_ph_v141_abs10_seed55` | 700 | `val_sample_action_mse=0.16855832934379578` | 16 |
| `smolvla_big384_ptp_ldp_mh_abs10_seed53` | 200 | `val_sample_action_mse=0.13580715656280518` | 11 |
| `smolvla_small_ptp_ldp_mh_abs10_seed52` | 200 | `val_sample_action_mse=0.12462320178747177` | 11 |

Completion state:

- `epoch_1000.pt` count: `0/4`.
- The monitor is still waiting; it has not started rollout workers.

SmolVLA script entry points:

- Training and rollout implementation: `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/train_eval_smolvla_square_scheduled.py`
- Four-way launcher: `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/launch_smolvla_fourway_square.sh`
- Post-training rollout monitor: `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/monitor_smolvla_fourway_rollout_best50.sh`

### `10.100.16.46:16139`

- Hostname: `lg-cmc-b7r202-h08u16-h200-000548`
- Visible GPUs: 2x NVIDIA H200, `/mnt/3fs2` mounted.
- Purpose: DP no-hist Square four-way training.
- Last verified GPU state on 2026-05-08 14:25 UTC:
  - GPU0: about 26926 MiB used, about 31% utilization.
  - GPU1: about 27060 MiB used, about 14% utilization.

Live DP no-hist processes:

| PID | Run |
| --- | --- |
| `172304` | `dp_nohist_unet_ldp_mh_seed42` |
| `172310` | `dp_nohist_unet_official_ph_seed43` |
| `176077` | `dp_nohist_dit_ldp_mh_seed44` |
| `176083` | `dp_nohist_dit_official_ph_seed45` |

DP roots:

- Run root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/dp_nohist_unet_dit_20260508_0915`
- Log root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/logs/dp_nohist_unet_dit_20260508_0915`

Latest parsed DP status:

| Run | Last epoch | Last rollout | Best rollout | Named ckpts | Videos |
| --- | ---: | ---: | ---: | ---: | ---: |
| `dp_nohist_unet_ldp_mh_seed42` | 63 | 0.06 at epoch 60 | 0.06 at epoch 60 | 13 | 636 |
| `dp_nohist_unet_official_ph_seed43` | 153 | 0.62 at epoch 100 | 0.68 at epoch 90 | 21 | 1060 |
| `dp_nohist_dit_ldp_mh_seed44` | 69 | 0.00 at epoch 60 | 0.04 at epoch 20 | 13 | 636 |
| `dp_nohist_dit_official_ph_seed45` | 183 | 0.58 at epoch 100 | 0.60 at epoch 70 | 21 | 1060 |

DP script entry points:

- Workspace wrappers: `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/dp_nohist_scheduled_workspaces.py`
- Launcher: `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/launch_dp_nohist_unet_dit_square.sh`

## Data Inventory

| Name | Path | Demos | Steps | Version note |
| --- | --- | ---: | ---: | --- |
| PTP/LDP-MH original data | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5` | 300 | 80,731 | no explicit `env_version` in `env_args` |
| Official-PH v1.4.1 data | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_abs_v141.hdf5` | 200 | 30,154 | `env_version=1.4.1` |
| Raw/generated official data directory | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph` | varies | varies | includes official demo/image conversions |

## Completed Reference Results

- Issue #157 BC-RNN official-PH v1.4.1 image training:
  - Run root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/issue157_v141/issue157_square_ph_image_v141_bc_rnn_600ep_s1/20260507120353`
  - Best checkpoint: `model_epoch_540_NutAssemblySquare_success_0.8.pth`
  - Highlight video: `NutAssemblySquare_epoch_540.mp4`
  - Best 50-rollout success: `0.80`
  - Final epoch 600 success: `0.54`
- Official model-zoo low-dimensional BC-RNN checkpoint evaluation:
  - Current robomimic 0.3 / robosuite 1.4.1 stack with loader patch: `33/50 = 0.66`
  - Strict old-stack reproduction was blocked by mujoco-py/osmesa and old robosuite branch requirements.
- Previous three-run SmolVLA batch:
  - Run root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/smolvla_resource_1000ep_early10_20260507_122849`
  - All-checkpoint rollout root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_all_ckpts_20rollouts_20260508_0255`
  - Best 20-rollout results: big384 LDP-MH epoch 1000 `0.30`; small LDP-MH epoch 200 `0.25`; official-PH v1.4.1 epoch 600 `0.20`
  - Best-checkpoint 50-rollout root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_best_ckpts_50rollouts_20260508_0343`
  - Best-checkpoint 50-rollout results: big384 LDP-MH epoch 1000 `13/50 = 0.26`; small LDP-MH epoch 200 `9/50 = 0.18`; official-PH v1.4.1 epoch 600 `7/50 = 0.14`

## Migration Plan For Future H200 py39 + robomimic 0.2.0 Environment

When the user provides the H200 environment configured with Python 3.9 and robomimic 0.2.0, move the current experiment suite into that environment using this order.

### 1. Environment verification

Run import and runtime checks before starting long jobs:

- `python --version` must be Python 3.9.x.
- Confirm robomimic 0.2.0 and the repository-recommended robosuite version.
- Confirm torch/CUDA can see the H200 GPUs.
- Confirm MuJoCo rendering works with EGL or the configured backend.
- Confirm `/mnt/3fs2/data/tingwen.du` is mounted and writable only under the intern_method_developer task path.

### 2. Dataset and environment smoke tests

- Open both HDF5 files and verify demo counts, step counts, observation keys, action shape, and `env_args`.
- Reset and render `NutAssemblySquare` from both dataset metadata variants.
- Save at least one short rollout video per dataset stack to confirm camera and image observation compatibility.

### 3. Checkpoint compatibility smoke tests

- Load the issue #157 BC-RNN v1.4.1 checkpoint and run a 1-rollout video smoke test.
- Load one completed SmolVLA checkpoint and run a 1-rollout video smoke test.
- Load one DP checkpoint/config from each policy family and run a 1-rollout video smoke test.
- If checkpoint formats are incompatible across stacks, record the exact loader error and start matched-environment retraining instead of altering source weights.

### 4. Reproduce the current experiment matrix

Run the same task matrix under the py39 / robomimic 0.2.0 environment:

- SmolVLA four-way:
  - small PTP/LDP-MH
  - big384 PTP/LDP-MH
  - small official-PH v1.4.1
  - big384 official-PH v1.4.1
- DP no-hist four-way:
  - UNet PTP/LDP-MH
  - UNet official-PH v1.4.1
  - DiT PTP/LDP-MH
  - DiT official-PH v1.4.1
- BC-RNN references:
  - issue #157 image BC-RNN official-PH v1.4.1 checkpoint rollout
  - official model-zoo low-dimensional BC-RNN checkpoint rollout, if the environment supports its loader and robosuite requirements

For SmolVLA and DP training, keep the existing schedule:

- Train for 1000 epochs.
- Save/evaluate at epochs `10,20,...,100,200,...,1000`.
- Run all named checkpoints with 20 rollouts and videos.
- Select the best checkpoint per run by rollout success rate and run 50 rollouts with videos.

### 5. Comparison report

The comparison report should explicitly separate:

- Data effect: PTP/LDP-MH vs official-PH v1.4.1.
- Environment effect: current py3.12 / robomimic 0.3 / robosuite 1.4.1 vs future py3.9 / robomimic 0.2.0 stack.
- Architecture effect: BC-RNN vs SmolVLA vs DP UNet vs DP DiT.
- Observation effect: image + proprioception policies vs the official low-dimensional BC-RNN that also uses `object`.
- Closed-loop success, not offline action MSE, as the main ranking metric.

## Resume Checklist

- Check whether `23989` SmolVLA has all four `epoch_1000.pt` files and whether monitor PID `62177` has generated the rollout report.
- Check whether `16139` DP no-hist runs reached epoch 1000 and gather their scheduled rollout metrics/videos.
- If the future py39 / robomimic 0.2.0 H200 environment is available, start with the smoke tests above before launching long retraining jobs.
- Keep all new outputs under the task-owned `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn` tree.
