# SmolVLA Best-Checkpoint 50-Rollout Results

Date: 2026-05-08

## Setup

- Output root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_best_ckpts_50rollouts_20260508_0343`
- Rollouts: 50 per selected checkpoint, seeds `10000-10049`, horizon 400, action horizon 8, flow sample steps 10.
- Video saving: enabled for every episode; 150 mp4 videos were saved.
- Video check: sample videos from each selected checkpoint decoded successfully to `uint8` frames with shape `[84, 168, 3]`.
- GPU use: 3 parallel rollout processes across the 2 H200 GPUs; the host was idle again after completion.

## Selected Checkpoints

The selected checkpoints are the best checkpoint from each SmolVLA training run under the prior 20-rollout all-checkpoint sweep.

| Run | Selected checkpoint | Dataset | Prior 20-rollout best | 50-rollout result | Mean steps | Video dir |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `ldp_mh_abs10_big384_seed44` | epoch 1000 | LDP-MH abs | 6/20 = 0.30 | 13/50 = 0.26 | 352.60 | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_best_ckpts_50rollouts_20260508_0343/ldp_mh_abs10_big384_epoch1000/videos` |
| `ldp_mh_abs10_seed42` | epoch 200 | LDP-MH abs | 5/20 = 0.25 | 9/50 = 0.18 | 368.74 | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_best_ckpts_50rollouts_20260508_0343/ldp_mh_abs10_epoch0200/videos` |
| `official_ph_v141_abs10_seed43` | epoch 600 | official PH v1.4.1 abs | 4/20 = 0.20 | 7/50 = 0.14 | 365.36 | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_best_ckpts_50rollouts_20260508_0343/official_ph_v141_abs10_epoch0600/videos` |

## Success Seeds

- `ldp_mh_abs10_big384_seed44` epoch 1000: `10007,10008,10009,10010,10012,10016,10022,10024,10026,10039,10043,10047,10048`
- `ldp_mh_abs10_seed42` epoch 200: `10007,10009,10013,10014,10016,10020,10027,10043,10047`
- `official_ph_v141_abs10_seed43` epoch 600: `10009,10010,10012,10019,10042,10044,10048`

## Interpretation

- The larger LDP-MH SmolVLA run remains the strongest SmolVLA result under the 50-rollout protocol at 26%.
- All three SmolVLA checkpoints drop versus the smaller 20-rollout estimate, which is expected from using 30 additional seeds.
- The BC-RNN issue #157 reference remains much stronger: epoch 540 reached 40/50 = 80%, and epoch 600 reached 27/50 = 54%.
