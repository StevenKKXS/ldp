# Direction C Status

Last updated: 2026-05-20

## Current State

Status: active for `intern_ldp_explorer`; Stage 1 Square comparison is running on GPU with `py39` and `robomimic==0.2.0`.

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

## Active Runs

Run root:

```text
/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage1_square_20260519_143020
```

After Session 32 recovery:

```text
past:        GPU0, pid 1086376, resumed at epoch 44
future:      GPU1, pid 1086384, resumed at epoch 44
past_future: GPU2, pid 26885, reached epoch 44
```

The resume fix in `TrainBehaviorTranslatorWorkspace` moves optimizer state to CUDA after loading checkpoint state, matching the base workspace convention that checkpoints are saved on CPU.

## CPU Benchmark

GPU3 benchmark root:

```text
/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/benchmarks/stage1_square_past_cpu_extreme_20260520_020004_v2
```

Key results for the Square `past` objective:

| Batch | Workers | Status | Samples/s | Projected min/epoch | Avg GPU3 util |
|---:|---:|---|---:|---:|---:|
| 32 | 8 | ok | 48.30 | 27.36 | 2.8% |
| 32 | 64 | ok | 80.59 | 16.40 | 13.2% |
| 64 | 96 | ok | 104.43 | 12.65 | 10.5% |
| 32 | 144 | failed | - | - | - |
| 128 | 96 | failed | - | - | - |

The node has 192 logical CPUs, but `/dev/shm` is only 16G. High worker and large batch settings hit DataLoader worker failures before the node can use 90% CPU.

## Next Step

Use the current formal runs to reach the epoch-50 checkpoint, then compare `best`, epoch-50, and best-future-L1 checkpoints in the frozen-head probe.
