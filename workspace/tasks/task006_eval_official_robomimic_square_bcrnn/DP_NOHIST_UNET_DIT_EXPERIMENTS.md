# DP No-Hist UNet and DiT Experiments

<!-- METADATA:SESSION=11 -->

## Goal
- Compare standard DP UNet and DiT-style transformer policies on Square with the same no-history parameters.
- Use the same two datasets already used in this task: LDP-MH Square and official-PH v1.4.1 Square.
- Keep all code, logs, checkpoints, rollout videos, and caches under `tingwen.du` paths.

## Shared Parameters
- Task config: `task=square_image_abs`.
- Observation window: `n_obs_steps=2`.
- Dataset observation steps: `dataset_obs_steps=2`.
- Diffusion trajectory horizon: `horizon=16`.
- Executed action chunk: `n_action_steps=1`.
- Training length: `1000` epochs.
- Scheduled checkpoint and rollout epochs: `10,20,...,100,200,...,1000`.
- Rollout protocol: `50` test rollouts, `n_test_vis=50`, `test_start_seed=100000`.
- Train initial-state rollouts: disabled with `n_train=0`.
- Batch size: `64`.
- Validation and sample logging: every `10` epochs.
- WandB mode: offline.

## Models
- UNet: `DiffusionUnetImagePolicy` via `train_diffusion_unet_image_workspace`.
- DiT: task-local scheduled wrapper around `DiffusionTransformerHybridImagePolicy`, using `TransformerForDiffusion`, with `past_action_pred=false` and `use_embed_if_present=false`.

## Datasets
- LDP-MH: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`.
- Official-PH v1.4.1: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_abs_v141.hdf5`.

## Launched Runs
- Run root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/dp_nohist_unet_dit_20260508_0915`.
- Log root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/logs/dp_nohist_unet_dit_20260508_0915`.
- `dp_nohist_unet_ldp_mh_seed42`: GPU 0, PID `172304`.
- `dp_nohist_unet_official_ph_seed43`: GPU 1, PID `172310`.
- `dp_nohist_dit_ldp_mh_seed44`: GPU 0, PID `176077`.
- `dp_nohist_dit_official_ph_seed45`: GPU 1, PID `176083`.

## Current Verification
- GPU host `10.100.16.46:16139` is reachable.
- `nvidia-smi` reports two NVIDIA H200 GPUs.
- All four run processes are alive as of 2026-05-08 09:25 UTC.
- Current phase is HDF5 to zarr cache construction and cache-lock waiting; GPU utilization is expected to rise after cache loading completes.

## Progress 2026-05-08 12:08 UTC
- GPU state: both H200 GPUs have active DP no-hist processes; GPU0 uses about 26.9GB, GPU1 uses about 27.1GB.
- `dp_nohist_unet_ldp_mh_seed42`: latest epoch 35; rollout scores `e10:0.04, e20:0.00, e30:0.00`; best `0.04`; 168 videos.
- `dp_nohist_dit_ldp_mh_seed44`: latest epoch 38; rollout scores `e10:0.00, e20:0.04, e30:0.00`; best `0.04`; 168 videos.
- `dp_nohist_unet_official_ph_seed43`: latest epoch 71; rollout scores `e10:0.28, e20:0.38, e30:0.58, e40:0.48, e50:0.62, e60:0.54, e70:0.66`; best `0.66`; 392 videos.
- `dp_nohist_dit_official_ph_seed45`: latest epoch 83; rollout scores `e10:0.00, e20:0.06, e30:0.14, e40:0.36, e50:0.50, e60:0.56, e70:0.60, e80:0.46`; best `0.60`; 448 videos.
- Current interpretation: official-PH v1.4.1 is training well for both UNet and DiT under no-history DP. LDP-MH is much slower or mismatched so far under the same protocol and remains near zero through the completed epoch-30 rollout checks.
