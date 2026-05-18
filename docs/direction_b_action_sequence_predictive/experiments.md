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

No experiments recorded.

### Exp ID: B_square_predictive_smoke

- Direction: B
- Task: Square
- Method: predictive encoder pretraining smoke
- Code branch / commit: pending
- Dataset version: robomimic square mh image_abs, exact path pending
- Checkpoint: initial PTP obs encoder checkpoint, path pending
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: full action sequence, `horizon=32`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: small MLP decoder, Huber loss in normalized action space
- Start date: pending
- End date: pending
- Best score: N/A
- Best epoch: N/A
- Current epoch: N/A
- Status: planned
- Notes: implementation feasibility smoke only; downstream policy result not available.

### Exp ID: B_toolhang_predictive_smoke

- Direction: B
- Task: ToolHang
- Method: predictive encoder pretraining smoke
- Code branch / commit: pending
- Dataset version: robomimic tool_hang ph image_abs, exact path pending
- Checkpoint: initial PTP obs encoder checkpoint, path pending
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: full action sequence, `horizon=32`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: small MLP decoder, Huber loss in normalized action space
- Start date: pending
- End date: pending
- Best score: N/A
- Best epoch: N/A
- Current epoch: N/A
- Status: planned
- Notes: implementation feasibility smoke only; downstream policy result not available.
