# Best Rollout Summary

Date: 2026-05-09 UTC

This table summarizes the best available closed-loop Square rollout result by setting, model, data version, and runtime version. `Final 50` means the selected checkpoint was evaluated with 50 rollouts and videos. `Scheduled 50` means the run is still training and the number is the best scheduled 50-rollout eval observed so far.

| Status | Runtime version | Setting / model | Data version | Best checkpoint / epoch | Best rollout |
| --- | --- | --- | --- | --- | ---: |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Official low-dim BC-RNN model-zoo checkpoint | Official Square PH low-dim v0.1 checkpoint data lineage | epoch 1850 checkpoint | 33/50 = 0.66 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Issue #157 image BC-RNN reproduction | Official-PH image v1.4.1 | epoch 540 | 40/50 = 0.80 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | SmolVLA small, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 200 | 9/50 = 0.18 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | SmolVLA big384, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 1000 | 13/50 = 0.26 |
| Final 50 | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | SmolVLA small, ldp_abs10 | Official-PH image_abs v1.4.1 | epoch 600 | 7/50 = 0.14 |
| Scheduled 50, training | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | DP no-hist UNet | PTP / LDP-MH image_abs | epoch 60 | 3/50 = 0.06 |
| Scheduled 50, training | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | DP no-hist DiT | PTP / LDP-MH image_abs | epoch 20 | 2/50 = 0.04 |
| Scheduled 50, training | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | DP no-hist UNet | Official-PH image_abs v1.4.1 | epoch 90 | 34/50 = 0.68 |
| Scheduled 50, training | py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | DP no-hist DiT | Official-PH image_abs v1.4.1 | epoch 70 | 30/50 = 0.60 |
| Final 50 | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | SmolVLA small, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 700 | 12/50 = 0.24 |
| Final 50 | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | SmolVLA big384, ldp_abs10 | PTP / LDP-MH original image_abs | epoch 400 | 16/50 = 0.32 |
| Final 50 | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | SmolVLA small, ldp_abs10 | Official-PH image_abs v1.4.1 | epoch 90 | 2/50 = 0.04 |
| Final 50 | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | SmolVLA big384, ldp_abs10 | Official-PH image_abs v1.4.1 | epoch 800 | 5/50 = 0.10 |
| Scheduled 50, training | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | DP no-hist UNet | PTP / LDP-MH image_abs | epoch 80 | 18/50 = 0.36 |
| Scheduled 50, training | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | DP no-hist DiT | PTP / LDP-MH image_abs | epoch 40 | 5/50 = 0.10 |
| Scheduled 50, training | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | DP no-hist UNet | Official-PH image_abs v1.4.1 | epoch 200 | 5/50 = 0.10 |
| Scheduled 50, training | py39 / robomimic 0.2 / robosuite 1.2.0 / mujoco-py 2.1 | DP no-hist DiT | Official-PH image_abs v1.4.1 | epoch 60 | 24/50 = 0.48 |

## Pending

| Runtime version | Setting / model | Data version | Current status |
| --- | --- | --- | --- |
| py312 / robomimic 0.3 / robosuite 1.4.1 / mujoco 3.8 | Four-way SmolVLA small / big384 | PTP-LDP-MH and Official-PH v1.4.1 | Training is complete; replacement rollout stamp `20260509_old_smolvla_resume` is running all-checkpoint 20-rollout evaluation before best-50 selection. |

## Notes

- The official robomimic model-zoo page reports about 84% for the low-dimensional BC-RNN, but the local current-stack evaluation reached 66%.
- DP rows are not final training-complete results. They are the best scheduled 50-rollout evaluations observed while the 1000-epoch runs continue.
- SmolVLA rows with `Final 50` are selected from all named checkpoints by a 20-rollout sweep, then re-evaluated with 50 rollouts and videos.
