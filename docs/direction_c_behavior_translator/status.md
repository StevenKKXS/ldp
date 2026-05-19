# Direction C Status

Last updated: 2026-05-19

## Current State

Status: active for `intern_ldp_explorer`; Stage 1 implementation smoke passed.

Owner: `intern_ldp_explorer`.

## Active Plan

- `docs/direction_c_behavior_translator/plan_review_2026-05-19.md`
- `docs/direction_c_behavior_translator/stage1_training_plan_2026-05-19.md`

## Current Decision

Proceed with a minimal offline pipeline before DP/PTP integration:

```text
raw obs history -> existing robomimic obs_encoder -> BehaviorTranslator -> past/future action sketch
```

The first go/no-go is Stage 2a:

```text
frozen pretrained translator context > frozen random translator context
```

## Stage 1 Training Decision

Train three first-round Stage 1 translator objectives on Square:

```text
H=16, P=16, K=8
raw Square obs history -> trainable robomimic obs_encoder -> BehaviorTranslator
```

Objectives:

```text
past:        predict a[t-16:t-1]
future:      predict a[t:t+7]
past_future: predict both
```

Each config trains for `1000` epochs and saves `latest`, `best`, and `epoch_0050`, `epoch_0100`, ... checkpoints. The monitor metric is `val/loss_total`.

The runs use explicit anchor slicing, not the default PTP action-window slicing.

## Implemented Files

```text
diffusion_policy/dataset/behavior_translation_dataset.py
diffusion_policy/model/behavior_translator.py
diffusion_policy/workspace/train_behavior_translator_workspace.py
experiment_configs/square/behavior_translator_square_past.yaml
experiment_configs/square/behavior_translator_square_future.yaml
experiment_configs/square/behavior_translator_square_past_future.yaml
```

## Verification

- `py_compile` passed for the new dataset/model/workspace and the patched robomimic dataset.
- Hydra `--cfg job` parses for all three Square configs.
- Dataset shape smoke passed: obs keys have `[16, ...]`, `act_past` is `[16, 10]`, `act_future` is `[8, 10]`.
- CPU one-step forward/backward smoke passed for `behavior_translator_square_past_future`; it wrote `latest.ckpt`, `best.ckpt`, `logs.json.txt`, `metrics.csv`, and `env.json`.

## Next Step

Launch the three 1000-epoch Square Stage 1 jobs on an assigned H200 GPU node using py39 / `robomimic==0.2.0`.
