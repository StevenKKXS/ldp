# Experiments

## Exp ID Naming

Suggested names:

```text
A_square_b1_ptp_baseline
A_square_b2_same_encoder_no_pretrain
A_square_o1_contrastive_frozen
A_square_o2_contrastive_finetune
A_toolhang_o1_contrastive_frozen
A_toolhang_o2_contrastive_finetune
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

### Exp ID: A_square_contrastive_smoke

- Direction: A
- Task: Square
- Method: future-action soft contrastive encoder pretraining smoke
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/square_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: policy future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: batch 4, diagonal-masked soft CE, normalized future action L2, adaptive sigma, 1 train step
- Start date: 2026-05-18
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 0
- Status: completed smoke
- Notes: First attempt produced NaN due diagonal `0 * -inf`; commit `7dcc632` fixed this. Rerun train loss `1.2313`, val loss `1.2405`; downstream policy result not available.

### Exp ID: A_toolhang_contrastive_smoke

- Direction: A
- Task: ToolHang
- Method: future-action soft contrastive encoder pretraining smoke
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/tool_hang_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: policy future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: batch 4, diagonal-masked soft CE, normalized future action L2, adaptive sigma, 1 train step
- Start date: 2026-05-18
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 0
- Status: completed smoke
- Notes: Train loss `1.3928`, val loss `1.1212`; raw image startup took several minutes; downstream policy result not available.

### Exp ID: A_square_future_seed42

- Direction: A
- Task: Square
- Method: future-action soft contrastive encoder pretraining
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/square_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: config `contrastive_square`, seed 42, default batch 32, max 200 train steps per epoch, 10 epochs
- Start date: 2026-05-18
- End date: N/A while running
- Best score: N/A
- Best epoch: N/A
- Current epoch: running
- Status: running
- Notes: Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_square_future_seed42`.

### Exp ID: A_square_future_seed43

- Direction: A
- Task: Square
- Method: future-action soft contrastive encoder pretraining
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/square_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: config `contrastive_square`, seed 43, default batch 32, max 200 train steps per epoch, 10 epochs
- Start date: 2026-05-18
- End date: N/A while running
- Best score: N/A
- Best epoch: N/A
- Current epoch: running
- Status: running
- Notes: Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_square_future_seed43`.

### Exp ID: A_tool_hang_future_seed42

- Direction: A
- Task: ToolHang
- Method: future-action soft contrastive encoder pretraining
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/tool_hang_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: config `contrastive_tool_hang`, seed 42, default batch 16, max 100 train steps per epoch, 10 epochs
- Start date: 2026-05-18
- End date: N/A while running
- Best score: N/A
- Best epoch: N/A
- Current epoch: running
- Status: running
- Notes: Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_tool_hang_future_seed42`.

### Exp ID: A_tool_hang_future_seed43

- Direction: A
- Task: ToolHang
- Method: future-action soft contrastive encoder pretraining
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, `7dcc632`
- Dataset version: `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- Checkpoint: `/mnt/nfs/tingwen/ldp/runtime_data/obs_encoders/obs_encoders/tool_hang_encoder.ckpt`
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: config `contrastive_tool_hang`, seed 43, default batch 16, max 100 train steps per epoch, 10 epochs
- Start date: 2026-05-18
- End date: N/A while running
- Best score: N/A
- Best epoch: N/A
- Current epoch: running
- Status: running
- Notes: Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_tool_hang_future_seed43`.
