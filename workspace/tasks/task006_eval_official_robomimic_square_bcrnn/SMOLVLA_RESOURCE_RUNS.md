# SmolVLA Resource Runs

Date: 2026-05-07

## Data

- LDP-MH absolute dataset: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`
- Official Square(PH) v141 image dataset: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_v141.hdf5`
- Official Square(PH) v141 absolute dataset generated for SmolVLA: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_abs_v141.hdf5`

## Schedule

All runs target 1000 epochs with offline action evaluation at epochs `10,20,...,100,200,...,1000`.

Run base:

`/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/smolvla_resource_1000ep_early10_20260507_122849`

## Runs

| Run | GPU | PID | Dataset | Model |
| --- | --- | --- | --- | --- |
| `ldp_mh_abs10_seed42` | 0 | 1939085 | LDP-MH abs | emb 256, layers 6 |
| `official_ph_v141_abs10_seed43` | 1 | 1939084 | official PH v141 abs | emb 256, layers 6 |
| `ldp_mh_abs10_big384_seed44` | 1 | 1947319 | LDP-MH abs | emb 384, layers 8 |

## First Metrics

- `ldp_mh_abs10_seed42`, epoch 10: `val_loss=0.1608908474`, `val_sample_action_mse=0.1463506222`
- `official_ph_v141_abs10_seed43`, epoch 10: `val_loss=0.2338462323`, `val_sample_action_mse=0.1962940693`
- `official_ph_v141_abs10_seed43`, epoch 20: `val_loss=0.2210917920`, `val_sample_action_mse=0.1815359592`
- `official_ph_v141_abs10_seed43`, epoch 30: `val_loss=0.2227935046`, `val_sample_action_mse=0.1762230098`
- `official_ph_v141_abs10_seed43`, epoch 40: `val_loss=0.2306858152`, `val_sample_action_mse=0.1765893400`
- `official_ph_v141_abs10_seed43`, epoch 50: `val_loss=0.2374282479`, `val_sample_action_mse=0.1726914048`
- `ldp_mh_abs10_big384_seed44`, epoch 10: `val_loss=0.1848952621`, `val_sample_action_mse=0.1609523296`

Latest sampled GPU utilization after all three SmolVLA jobs were running: GPU0 91%, GPU1 59%.

## Completion Metrics

Checked on 2026-05-08 02:28 UTC. Both H200 GPUs were idle and no training processes remained.

| Run | Final epoch | Final `val_sample_action_mse` | Best epoch | Best `val_sample_action_mse` | `latest.pt` |
| --- | ---: | ---: | ---: | ---: | --- |
| `ldp_mh_abs10_seed42` | 1000 | 0.1309051514 | 600 | 0.1279252321 | present |
| `official_ph_v141_abs10_seed43` | 1000 | 0.1680839658 | 1000 | 0.1680839658 | present |
| `ldp_mh_abs10_big384_seed44` | 1000 | 0.1530992389 | 1000 | 0.1530992389 | present |

These are offline action metrics only; robosuite rollout success still needs to be run from selected checkpoints.
