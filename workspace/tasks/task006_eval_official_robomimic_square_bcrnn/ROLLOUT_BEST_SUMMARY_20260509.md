# Best Rollout Summary

Date: 2026-05-09 UTC; final DP update: 2026-05-11 UTC

This table summarizes the best available closed-loop Square rollout result by setting, model, data version, and runtime version. `Final 50` means the selected checkpoint was evaluated with 50 rollouts and videos. `Scheduled 50, complete` means a training-scheduled 50-rollout eval from a completed 1000-epoch run.

| Status | Runtime version | Setting / model | Data version | Best checkpoint / epoch | Best rollout |
| --- | --- | --- | --- | --- | ---: |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Official low-dim BC-RNN model-zoo checkpoint | Official Square PH low-dim v0.1 checkpoint data lineage | epoch 1850 checkpoint | 33/50 = 0.66 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Issue #157 image BC-RNN reproduction | Official-PH image v1.4.1 | epoch 540 | 40/50 = 0.80 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | SmolVLA small, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 200 | 9/50 = 0.18 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | SmolVLA big384, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 1000 | 13/50 = 0.26 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | SmolVLA small, ldp_abs10 | Official-PH image_abs v1.4.1 | epoch 600 | 7/50 = 0.14 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Four-way SmolVLA small, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 700 | 5/50 = 0.10 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Four-way SmolVLA big384, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 700 | 9/50 = 0.18 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Four-way SmolVLA small, ldp_abs10 | Official-PH image_abs v1.4.1 | epoch 600 | 7/50 = 0.14 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Four-way SmolVLA big384, ldp_abs10 | Official-PH image_abs v1.4.1 | epoch 600 | 12/50 = 0.24 |
| Scheduled 50, complete | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | DP no-hist UNet | PTP / LDP-MH image_abs | epoch 500 | 5/50 = 0.10 |
| Scheduled 50, complete | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | DP no-hist DiT | PTP / LDP-MH image_abs | epoch 20 / 40 / 70 / 200 | 2/50 = 0.04 |
| Scheduled 50, complete | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | DP no-hist UNet | Official-PH image_abs v1.4.1 | epoch 90 | 34/50 = 0.68 |
| Scheduled 50, complete | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | DP no-hist DiT | Official-PH image_abs v1.4.1 | epoch 70 | 30/50 = 0.60 |
| Final 50 | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | SmolVLA small, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 700 | 12/50 = 0.24 |
| Final 50 | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | SmolVLA big384, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 400 | 16/50 = 0.32 |
| Final 50 | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | SmolVLA small, ldp_abs10 | Official-PH image_abs v1.4.1 | epoch 90 | 2/50 = 0.04 |
| Final 50 | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | SmolVLA big384, ldp_abs10 | Official-PH image_abs v1.4.1 | epoch 800 | 5/50 = 0.10 |
| Scheduled 50, complete | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | DP no-hist UNet | PTP / LDP-MH image_abs | epoch 900 | 25/50 = 0.50 |
| Scheduled 50, complete | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | DP no-hist DiT | PTP / LDP-MH image_abs | epoch 600 / 700 | 12/50 = 0.24 |
| Scheduled 50, complete | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | DP no-hist UNet | Official-PH image_abs v1.4.1 | epoch 400 | 10/50 = 0.20 |
| Scheduled 50, complete | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | DP no-hist DiT | Official-PH image_abs v1.4.1 | epoch 60 | 24/50 = 0.48 |

## Pending / Active

No active Square training or rollout jobs remain as of 2026-05-11 08:28 UTC.

## Notes

- The official robomimic model-zoo page reports about 84% for the low-dimensional BC-RNN, but the local current-stack evaluation reached 66%.
- DP rows are training-scheduled 50-rollout evaluations. All DP runs listed here have reached epoch 1000.
- SmolVLA rows with `Final 50` are selected from all named checkpoints by a 20-rollout sweep, then re-evaluated with 50 rollouts and videos.
