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

No experiments recorded.

### Exp ID: A_square_contrastive_smoke

- Direction: A
- Task: Square
- Method: future-action soft contrastive encoder pretraining smoke
- Code branch / commit: pending
- Dataset version: robomimic square mh image_abs, exact path pending
- Checkpoint: initial PTP obs encoder checkpoint, path pending
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: policy future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: diagonal-masked soft CE, normalized future action L2, adaptive sigma
- Start date: pending
- End date: pending
- Best score: N/A
- Best epoch: N/A
- Current epoch: N/A
- Status: planned
- Notes: implementation feasibility smoke only; downstream policy result not available.

### Exp ID: A_toolhang_contrastive_smoke

- Direction: A
- Task: ToolHang
- Method: future-action soft contrastive encoder pretraining smoke
- Code branch / commit: pending
- Dataset version: robomimic tool_hang ph image_abs, exact path pending
- Checkpoint: initial PTP obs encoder checkpoint, path pending
- Encoder input: same observation keys as PTP, cached embeddings disabled
- History length H: `n_obs_steps=16`
- Action horizon K: policy future slice, `n_action_steps=8`
- Frozen or finetuned: pretraining updates obs encoder
- Key hyperparameters: diagonal-masked soft CE, normalized future action L2, adaptive sigma
- Start date: pending
- End date: pending
- Best score: N/A
- Best epoch: N/A
- Current epoch: N/A
- Status: planned
- Notes: implementation feasibility smoke only; downstream policy result not available.
