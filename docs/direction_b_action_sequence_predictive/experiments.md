# Experiments

## Exp ID Naming

Suggested names:

```text
B_square_b1_ptp_baseline
B_square_b2_same_encoder_no_pretrain
B_square_o1_future_predictive_frozen
B_square_o2_past_future_predictive_finetune
B_toolhang_o1_future_predictive_frozen
B_toolhang_o2_past_future_predictive_finetune
```

## Experiment Template

### Exp ID:

- Direction:
- Task:
- Method:
- Code branch / commit:
- Dataset version:
- Checkpoint:
- Encoder input:
- History length H:
- Action horizon K:
- Frozen or finetuned:
- Key hyperparameters:
- Start date:
- End date:
- Best score:
- Best epoch:
- Current epoch:
- Status:
- Notes:

## Recorded Experiments

### Exp ID: B_square_predictive_smoke

- Direction: B
- Task: Square
- Method: predictive encoder pretraining smoke
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/square_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: full action sequence, `horizon=32`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: batch 2, small MLP decoder, Huber loss in normalized action space, 1 train step
- Start date: 2026-05-18
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 0
- Status: completed smoke
- Notes: Train loss `0.4260`, val loss `0.4002`; downstream policy result not available.

### Exp ID: B_toolhang_predictive_smoke

- Direction: B
- Task: ToolHang
- Method: predictive encoder pretraining smoke
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/tool_hang_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: full action sequence, `horizon=32`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: batch 1, small MLP decoder, Huber loss in normalized action space, 1 train step
- Start date: 2026-05-18
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 0
- Status: completed smoke
- Notes: Train loss `0.4394`, val loss `0.3929`; raw image startup took about 4 minutes; downstream policy result not available.

### Exp ID: B_square_full_seed42

- Direction: B
- Task: Square
- Method: predictive encoder pretraining, full action sequence target
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/square_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: full action sequence, `horizon=32`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: config `predictive_square`, seed 42, default batch 16, max 200 train steps per epoch, 10 epochs
- Start date: 2026-05-18
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 9
- Status: completed
- Notes: Final train loss `0.0167`, val loss `0.0373`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_square_full_seed42`.

### Exp ID: B_square_future_seed42

- Direction: B
- Task: Square
- Method: predictive encoder pretraining, future-only action target
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/square_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: config `predictive_square`, override `pretrain.target_mode=future`, seed 42, default batch 16, max 200 train steps per epoch, 10 epochs
- Start date: 2026-05-18
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 9
- Status: completed
- Notes: Final train loss `0.0164`, val loss `0.0426`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_square_future_seed42`.

### Exp ID: B_tool_hang_full_seed42

- Direction: B
- Task: ToolHang
- Method: predictive encoder pretraining, full action sequence target
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/tool_hang_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: full action sequence, `horizon=32`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: config `predictive_tool_hang`, seed 42, default batch 8, max 100 train steps per epoch, 10 epochs
- Start date: 2026-05-18
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 9
- Status: completed
- Notes: Final train loss `0.0243`, val loss `0.0494`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_tool_hang_full_seed42`.

### Exp ID: B_tool_hang_future_seed42

- Direction: B
- Task: ToolHang
- Method: predictive encoder pretraining, future-only action target
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/tool_hang_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: config `predictive_tool_hang`, override `pretrain.target_mode=future`, seed 42, default batch 8, max 100 train steps per epoch, 10 epochs
- Start date: 2026-05-18
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 9
- Status: completed
- Notes: Final train loss `0.0252`, val loss `0.0420`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_tool_hang_future_seed42`.

### Exp ID: B_downstream_session10_main

- Direction: B
- Task: Square / ToolHang
- Method: exact-PTP downstream training from full-action predictive-pretrained encoder
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, running from Session 10 workspace
- Dataset version: Square `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5`; ToolHang `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- Checkpoint: `B_square_full_seed42/checkpoints/latest.ckpt`, `B_tool_hang_full_seed42/checkpoints/latest.ckpt`
- Encoder input: exact PTP raw-image observations, cached embeddings disabled
- History length H: downstream config `n_obs_steps=2`
- Action horizon K: unchanged PTP config per task
- Frozen or finetuned: frozen and finetuned rows
- Key hyperparameters: 50 epochs, Square max 200 train steps / 20 val steps per epoch, ToolHang max 100 train steps / 10 val steps per epoch, rollout disabled
- Start date: 2026-05-19
- End date: running
- Best score: N/A
- Best epoch: N/A
- Current epoch: Square 17-18, ToolHang 6
- Status: running
- Notes: Latest poll: Square `B_full_frozen` val `0.0933`, `B_full_finetune` `0.0865`, original `0.0965`; ToolHang `B_full_frozen` `0.1585`, `B_full_finetune` `0.1566`, original `0.1568`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10`.

### Exp ID: B_downstream_session10_extra

- Direction: B
- Task: Square / ToolHang
- Method: exact-PTP downstream training from future-only predictive-pretrained encoder
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, running from Session 10 workspace
- Dataset version: same raw-image datasets as main matrix
- Checkpoint: `B_square_future_seed42/checkpoints/latest.ckpt`, `B_tool_hang_future_seed42/checkpoints/latest.ckpt`
- Encoder input: exact PTP raw-image observations, cached embeddings disabled
- History length H: downstream config `n_obs_steps=2`
- Action horizon K: unchanged PTP config per task
- Frozen or finetuned: frozen and finetuned rows
- Key hyperparameters: same as main matrix, rollout disabled
- Start date: 2026-05-19
- End date: running
- Best score: N/A
- Best epoch: N/A
- Current epoch: Square 7-8, ToolHang 2
- Status: running
- Notes: Latest poll: Square `B_future_frozen` val `0.1012`, `B_future_finetune` `0.1144`; ToolHang `B_future_frozen` val `0.2668`, `B_future_finetune` `0.2624`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10_extra`.
