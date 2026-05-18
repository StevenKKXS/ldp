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
- End date: N/A while running
- Best score: N/A
- Best epoch: N/A
- Current epoch: running
- Status: running
- Notes: Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_square_full_seed42`.

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
- End date: N/A while running
- Best score: N/A
- Best epoch: N/A
- Current epoch: running
- Status: running
- Notes: Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_square_future_seed42`.

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
- End date: N/A while running
- Best score: N/A
- Best epoch: N/A
- Current epoch: running
- Status: running
- Notes: Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_tool_hang_full_seed42`.

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
- End date: N/A while running
- Best score: N/A
- Best epoch: N/A
- Current epoch: running
- Status: running
- Notes: Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_tool_hang_future_seed42`.
