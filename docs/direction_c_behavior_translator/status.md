# Direction C Status

Last updated: 2026-05-19

## Current State

Status: active for `intern_ldp_explorer`, planned, reviewed, not implemented.

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

Train the first Stage 1 run as `C1-T3-square-history-past-future`:

```text
H=16, P=16, K=8
raw Square obs history -> trainable robomimic obs_encoder -> BehaviorTranslator -> past+future actions
```

The run should use explicit anchor slicing, not the default PTP action-window slicing.

## Next Step

Implement `BehaviorTranslationDataset`, `BehaviorTranslator`, and one Square T3 config, then run shape and forward/backward smoke checks in py39 / `robomimic==0.2.0`.
