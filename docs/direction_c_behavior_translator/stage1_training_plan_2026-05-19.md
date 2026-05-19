# Direction C Stage 1 Training Plan

## 0. Goal

Train the first Behavior Translator with offline action reconstruction:

```text
raw obs history -> existing robomimic obs_encoder -> BehaviorTranslator -> past/future action sketch
```

Stage 1 does not run environment rollout and does not modify DP/PTP policy code.

The first checkpoint is meant to answer:

```text
Can a translator trained from history observations predict past/future expert actions well enough to produce a useful behavior context?
```

The downstream go/no-go is still Stage 2a:

```text
frozen pretrained translator context > frozen random translator context
```

## 1. First Run Set

Start with three Square translator objectives that share the same architecture and windowing:

| Experiment ID | Target | Purpose |
|---|---|---|
| `behavior_translator_square_past` | `a[t-16:t-1]` | Checks whether obs history can reconstruct historical behavior |
| `behavior_translator_square_future` | `a[t:t+7]` | Checks direct future translation |
| `behavior_translator_square_past_future` | both | Main representation objective |

Shared setup:

| Field | Value |
|---|---|
| Task | Square `mh` |
| Dataset | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image_abs.hdf5` |
| Environment | Python 3.9 + `robomimic==0.2.0` |
| Input | raw image/proprio history |
| Rollout | disabled |
| Epochs | `1000` |
| Periodic checkpoint | every `50` epochs |
| Monitor | `val/loss_total` |

The existing verified env is:

```text
/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020
```

Before any run, log:

```text
sys.executable
robomimic.__version__
robomimic.__file__
torch.__version__
```

## 2. Window Definition

Use a center time `t`.

```text
obs_hist   = o[t-H+1 : t]
act_past   = a[t-P : t-1]
act_future = a[t : t+K-1]
```

Initial values:

```yaml
obs_horizon: 16
past_action_horizon: 16
future_action_horizon: 8
```

Important implementation detail:

The existing PTP dataset returns action windows aligned for PTP, not this exact translator target. The BehaviorTranslationDataset should slice from a sampled contiguous sequence explicitly.

For `H=16`, `P=16`, `K=8`:

```text
sequence offsets: 0 ... 23
anchor t offset: 16
obs_hist:   offsets 1 ... 16
act_past:   offsets 0 ... 15
act_future: offsets 16 ... 23
```

General formula:

```python
anchor = max(past_action_horizon, obs_horizon - 1)
sequence_length = anchor + future_action_horizon
obs_start = anchor - obs_horizon + 1
obs_end = anchor + 1
past_start = anchor - past_action_horizon
past_end = anchor
future_start = anchor
future_end = anchor + future_action_horizon
```

Use episode-boundary padding by repeating edge samples, consistent with the existing `SequenceSampler` convention.

## 3. Model Parameters

Initial model:

```yaml
obs_encoder: existing robomimic obs encoder architecture from the Square PTP config
train_obs_encoder: true
translator:
  d_model: 256
  n_encoder_layers: 4
  n_decoder_layers: 2
  n_heads: 4
  ff_dim: 1024
  dropout: 0.1
  context_dim: 512
  causal_obs_encoder: true
  decoder_cross_attn_mask: none
```

Rationale:

- The dataloader returns raw images/proprio, so the obs encoder must be part of Stage 1 training.
- Freezing a randomly initialized obs encoder would make the first run meaningless.
- Cross-attention masking is useful, but the first run should prove shape/loss correctness with the simpler full-history cross-attention path.

## 4. Normalization

Use the same dataset normalizer as PTP.

Training procedure:

```text
normalizer = dataset.get_normalizer()
normalized_obs = normalizer.normalize(obs_hist)
normalized_actions = normalizer["action"].normalize(action_targets)
```

Loss is computed in normalized action space.

For robomimic `abs_action=true`, this means:

```text
position action dims -> range-normalized to [-1, 1]
other action dims -> identity
```

## 5. Loss

Use SmoothL1:

```python
loss_past = smooth_l1(pred[:, :P], act_past)
loss_future = smooth_l1(pred[:, P:], act_future)
loss_total = w_past * loss_past + w_future * loss_future
```

Initial weights:

```yaml
w_past: 1.0
w_future: 1.0
```

Checkpoint selection:

```text
best by val/loss_total
```

Reason: the three objectives have different supervised targets, so their own eval loss is the cleanest first comparison. Future L1 is still logged for all variants.

## 6. Optimization

Smoke run:

```yaml
batch_size: 8
max_train_steps: 20
max_val_batches: 4
num_workers: 2
```

First real Square run:

```yaml
batch_size: 32
gradient_accumulate_every: 1
epochs: 1000
optimizer: AdamW
lr: 1.0e-4
weight_decay: 1.0e-4
grad_clip: 1.0
num_workers: 8
mixed_precision: false
checkpoint_every: 50
monitor_key: val/loss_total
```

If H200 memory is underused and dataloading is stable, increase batch size to 64. Do not start with batch 256 because raw image history means each batch contains `B * H` image observations through the robomimic encoder.

## 7. Metrics

Log every epoch:

```text
train/loss_total
train/loss_past
train/loss_future
val/loss_total
val/loss_past
val/loss_future
val/future_l1
val/future_mse
val/past_l1
val/per_horizon_future_l1_00 ... val/per_horizon_future_l1_07
val/gripper_acc
```

For Square action dim 10, use the last action dim as the gripper metric candidate and record sign agreement:

```text
sign(pred[..., -1]) == sign(target[..., -1])
```

If inspection shows the gripper dimension differs for a task, update the metric before reporting it.

## 8. Output Layout

Use NFS task output:

```text
/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/
```

Suggested run paths:

```text
/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/behavior_translator_square_past_YYYYMMDD_HHMMSS/
/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/behavior_translator_square_future_YYYYMMDD_HHMMSS/
/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/behavior_translator_square_past_future_YYYYMMDD_HHMMSS/
```

Keep only:

```text
config.yaml
env.json
logs.jsonl
metrics.csv
checkpoints/latest.ckpt
checkpoints/best.ckpt
checkpoints/epoch_0050.ckpt
checkpoints/epoch_0100.ckpt
...
```

Do not archive checkpoints to CephFS unless requested.

## 9. Controls After First Run Set

After the three Square objectives train and validate cleanly, run these controls:

| ID | Change |
|---|---|
| `C1-T1` | single-frame obs, future-only target |
| `C1-T4` | shuffled obs history, past+future target |

Only move to ToolHang after Square training and validation are stable.

## 10. My Execution Sequence

1. Implement `BehaviorTranslationDataset` with explicit anchor slicing.
2. Implement `BehaviorTranslator`.
3. Implement `TrainBehaviorTranslatorWorkspace`.
4. Add Square configs for `past`, `future`, and `past_future`.
5. Run `py_compile` and Hydra config parse.
6. Run local dataset shape inspection.
7. Run GPU smoke in py39 / `robomimic==0.2.0`.
8. Start the three 1000-epoch Square runs.
9. Report eval-loss curves and checkpoint paths every 50 epochs.
