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
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 9
- Status: completed
- Notes: Final train loss `3.3737`, val loss `3.3962`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_square_future_seed42`.

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
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 9
- Status: completed
- Notes: Final train loss `3.3742`, val loss `3.3965`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_square_future_seed43`.

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
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 9
- Status: completed
- Notes: Final train loss `2.6360`, val loss `2.6933`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_tool_hang_future_seed42`.

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
- End date: 2026-05-18
- Best score: N/A
- Best epoch: N/A
- Current epoch: 9
- Status: completed
- Notes: Final train loss `2.6395`, val loss `2.6921`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_tool_hang_future_seed43`.

### Exp ID: A_downstream_session10_main

- Direction: A
- Task: Square / ToolHang
- Method: exact-PTP downstream training from contrastive-pretrained encoder
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, running from Session 10 workspace
- Dataset version: Square `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/square/mh/image_abs.hdf5`; ToolHang `/mnt/nfs/tingwen/ldp/runtime_data/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`
- Checkpoint: `A_square_future_seed42/checkpoints/latest.ckpt`, `A_tool_hang_future_seed42/checkpoints/latest.ckpt`
- Encoder input: exact PTP raw-image observations, cached embeddings disabled
- History length H: downstream config `n_obs_steps=2`
- Action horizon K: unchanged PTP config per task
- Frozen or finetuned: finetuned in main matrix
- Key hyperparameters: 50 epochs, Square max 200 train steps / 20 val steps per epoch, ToolHang max 100 train steps / 10 val steps per epoch, rollout disabled
- Start date: 2026-05-19
- End date: running
- Best score: N/A
- Best epoch: N/A
- Current epoch: Square 17, ToolHang 6
- Status: running
- Notes: Latest poll: Square `A_future_finetune` val loss `0.0866` vs original `0.0965`; ToolHang `A_future_finetune` val loss `0.1572` vs original `0.1568`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10`.

### Exp ID: A_downstream_session10_extra

- Direction: A
- Task: Square / ToolHang
- Method: exact-PTP downstream frozen and seed-sensitivity probe
- Code branch / commit: `intern_method_developer/task002_flow_matching_square_toolhang`, running from Session 10 workspace
- Dataset version: same raw-image datasets as main matrix
- Checkpoint: `A_square_future_seed42`, `A_square_future_seed43`, `A_tool_hang_future_seed42`, `A_tool_hang_future_seed43`
- Encoder input: exact PTP raw-image observations, cached embeddings disabled
- History length H: downstream config `n_obs_steps=2`
- Action horizon K: unchanged PTP config per task
- Frozen or finetuned: frozen for seed42 frozen rows; finetuned for seed43 rows
- Key hyperparameters: same as main matrix, rollout disabled
- Start date: 2026-05-19
- End date: running
- Best score: N/A
- Best epoch: N/A
- Current epoch: Square 7-8, ToolHang 1-2
- Status: running
- Notes: Latest poll: Square `A_future_frozen` val `0.1001`, `A_future_seed43_finetune` val `0.1126`; ToolHang `A_future_frozen` val `0.2679`, `A_future_seed43_finetune` val `0.3481`. Output path `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10_extra`.
