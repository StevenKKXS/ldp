# SmolVLA All-Checkpoint Square Rollout Results

Date: 2026-05-08

## Setup

- Output root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_all_ckpts_20rollouts_20260508_0255`
- Script: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/scripts/rollout_smolvla_square_all_ckpts.py`
- Repo script: `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/rollout_smolvla_square_all_ckpts.py`
- Rollouts: 20 per checkpoint, seeds `10000-10019`, horizon 400, action horizon 8, flow sample steps 10.
- Parallelism: 4 worker processes across 2 H200 GPUs, 2 workers per GPU.
- Videos: 1140 mp4 files, one per SmolVLA rollout episode. Video decode spot checks returned `uint8` frames with shape `[84, 168, 3]`.
- Aggregate files: `SUMMARY.md`, `summary.csv`, `summary.json`, `summary.jsonl` under the output root.

## Overall Summary

| Training run | Dataset | Checkpoints | Rollouts | Best rollout epoch | Best success | Final epoch success | Total success over curve | Offline best |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ldp_mh_abs10_big384_seed44` | LDP-MH abs | 19 | 380 | 1000 | 6/20 = 0.30 | 6/20 = 0.30 | 51/380 = 0.134 | epoch 1000, MSE 0.1530992389 |
| `ldp_mh_abs10_seed42` | LDP-MH abs | 19 | 380 | 200 | 5/20 = 0.25 | 3/20 = 0.15 | 25/380 = 0.066 | epoch 600, MSE 0.1279252321 |
| `official_ph_v141_abs10_seed43` | official PH v1.4.1 abs | 19 | 380 | 600 | 4/20 = 0.20 | 1/20 = 0.05 | 20/380 = 0.053 | epoch 1000, MSE 0.1680839658 |

BC-RNN issue #157 reference remains much stronger on the same task family: the existing 50-rollout training evals reached best epoch 540 at `40/50 = 0.80`, with final epoch 600 at `27/50 = 0.54`.

## `ldp_mh_abs10_big384_seed44`

| Epoch | Successes | Rollouts | Success rate | Mean steps |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 1 | 20 | 0.050 | 388.90 |
| 20 | 1 | 20 | 0.050 | 391.05 |
| 30 | 2 | 20 | 0.100 | 378.90 |
| 40 | 3 | 20 | 0.150 | 371.00 |
| 50 | 0 | 20 | 0.000 | 400.00 |
| 60 | 4 | 20 | 0.200 | 355.90 |
| 70 | 2 | 20 | 0.100 | 377.35 |
| 80 | 2 | 20 | 0.100 | 390.25 |
| 90 | 1 | 20 | 0.050 | 394.95 |
| 100 | 2 | 20 | 0.100 | 380.60 |
| 200 | 2 | 20 | 0.100 | 382.40 |
| 300 | 3 | 20 | 0.150 | 374.20 |
| 400 | 3 | 20 | 0.150 | 375.65 |
| 500 | 5 | 20 | 0.250 | 362.70 |
| 600 | 2 | 20 | 0.100 | 390.15 |
| 700 | 3 | 20 | 0.150 | 377.95 |
| 800 | 5 | 20 | 0.250 | 354.80 |
| 900 | 4 | 20 | 0.200 | 354.80 |
| 1000 | 6 | 20 | 0.300 | 348.85 |

## `ldp_mh_abs10_seed42`

| Epoch | Successes | Rollouts | Success rate | Mean steps |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 0 | 20 | 0.000 | 400.00 |
| 20 | 0 | 20 | 0.000 | 400.00 |
| 30 | 0 | 20 | 0.000 | 400.00 |
| 40 | 0 | 20 | 0.000 | 400.00 |
| 50 | 1 | 20 | 0.050 | 392.50 |
| 60 | 1 | 20 | 0.050 | 388.25 |
| 70 | 0 | 20 | 0.000 | 400.00 |
| 80 | 0 | 20 | 0.000 | 400.00 |
| 90 | 0 | 20 | 0.000 | 400.00 |
| 100 | 1 | 20 | 0.050 | 399.35 |
| 200 | 5 | 20 | 0.250 | 351.60 |
| 300 | 2 | 20 | 0.100 | 379.85 |
| 400 | 2 | 20 | 0.100 | 382.95 |
| 500 | 2 | 20 | 0.100 | 377.10 |
| 600 | 1 | 20 | 0.050 | 395.20 |
| 700 | 4 | 20 | 0.200 | 362.45 |
| 800 | 2 | 20 | 0.100 | 377.05 |
| 900 | 1 | 20 | 0.050 | 387.25 |
| 1000 | 3 | 20 | 0.150 | 371.55 |

## `official_ph_v141_abs10_seed43`

| Epoch | Successes | Rollouts | Success rate | Mean steps |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 0 | 20 | 0.000 | 400.00 |
| 20 | 0 | 20 | 0.000 | 400.00 |
| 30 | 0 | 20 | 0.000 | 400.00 |
| 40 | 0 | 20 | 0.000 | 400.00 |
| 50 | 1 | 20 | 0.050 | 385.45 |
| 60 | 2 | 20 | 0.100 | 370.90 |
| 70 | 1 | 20 | 0.050 | 385.95 |
| 80 | 0 | 20 | 0.000 | 400.00 |
| 90 | 2 | 20 | 0.100 | 370.80 |
| 100 | 1 | 20 | 0.050 | 386.85 |
| 200 | 1 | 20 | 0.050 | 387.00 |
| 300 | 0 | 20 | 0.000 | 400.00 |
| 400 | 0 | 20 | 0.000 | 400.00 |
| 500 | 1 | 20 | 0.050 | 385.60 |
| 600 | 4 | 20 | 0.200 | 357.10 |
| 700 | 3 | 20 | 0.150 | 356.65 |
| 800 | 2 | 20 | 0.100 | 372.70 |
| 900 | 1 | 20 | 0.050 | 385.75 |
| 1000 | 1 | 20 | 0.050 | 385.55 |

## Interpretation

- All SmolVLA-style policies can produce valid Square rollouts, but their closed-loop success rates remain far below the BC-RNN issue #157 reproduction.
- The larger LDP-MH model is the best SmolVLA run in rollout success, even though its offline action MSE is worse than the smaller LDP-MH baseline.
- The smallest offline action MSE checkpoint is not the best rollout checkpoint: LDP-MH small model has offline best at epoch 600, while rollout best is epoch 200.
- The official PH v1.4.1 SmolVLA run reaches only 20% best success on this 20-rollout protocol, despite improving offline action MSE through epoch 1000.

## 50-Rollout Follow-Up

The best checkpoint from each SmolVLA training run was rerun with 50 rollouts and per-episode video saving under:

`/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_best_ckpts_50rollouts_20260508_0343`

| Run | Selected epoch | 20-rollout result | 50-rollout result | Videos |
| --- | ---: | ---: | ---: | ---: |
| `ldp_mh_abs10_big384_seed44` | 1000 | 6/20 = 0.30 | 13/50 = 0.26 | 50 |
| `ldp_mh_abs10_seed42` | 200 | 5/20 = 0.25 | 9/50 = 0.18 | 50 |
| `official_ph_v141_abs10_seed43` | 600 | 4/20 = 0.20 | 7/50 = 0.14 | 50 |
