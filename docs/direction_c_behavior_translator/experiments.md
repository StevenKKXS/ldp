# Direction C Experiments

No experiments have been run.

## Planned Stage 1 Offline Translation

| ID | Task | Setting | Status | Result |
|---|---|---|---|---|
| C1-T1 | Square | single-frame -> future | deferred | N/A |
| C1-T2 | Square | history -> future | implemented config | N/A |
| C1-T3 | Square | history -> past+future | implemented config and CPU smoke passed | one-step smoke only |
| C1-T4 | Square | shuffled history -> past+future | planned | N/A |
| C1-T5 | ToolHang | history -> future | planned | N/A |
| C1-T6 | ToolHang | history -> past+future | planned | N/A |
| C1-T7 | Square | history -> past | implemented config | N/A |

## Planned Stage 2a Frozen-Head Probe

| ID | Task | Context | Frozen | Status | Result |
|---|---|---|---:|---|---|
| C2-H1 | Square | random translator | yes | planned | N/A |
| C2-H2 | Square | pretrained translator | yes | planned | N/A |
| C2-H3 | Square | pretrained translator | no | planned | N/A |
| C2-H4 | ToolHang | random translator | yes | planned | N/A |
| C2-H5 | ToolHang | pretrained translator | yes | planned | N/A |

## Selected First Run Parameters

| Field | Value |
|---|---|
| First run set | Square `past`, `future`, `past_future` |
| Obs horizon H | 16 |
| Past action horizon P | 16 |
| Future action horizon K | 8 |
| Loss | SmoothL1 over each config's target |
| Checkpoint metric | `val/loss_total` |
| Smoke batch | 8 |
| First real batch | 32 |
| Epochs | 1000 |
| Periodic checkpoint | every 50 epochs |

## Implemented Stage 1 Configs

| Config | Target Mode | Output |
|---|---|---|
| `experiment_configs/square/behavior_translator_square_past.yaml` | `past` | `a[t-16:t-1]` |
| `experiment_configs/square/behavior_translator_square_future.yaml` | `future` | `a[t:t+7]` |
| `experiment_configs/square/behavior_translator_square_past_future.yaml` | `past_future` | both |

## Smoke Result

`behavior_translator_square_past_future` CPU smoke:

| Metric | Value |
|---|---:|
| `train/loss_total` | 0.3429 |
| `val/loss_total` | 0.1543 |
| `val/future_l1` | 0.3619 |
| `val/gripper_acc` | 1.0000 |

This is a one-step smoke result only; it should not be interpreted as model quality.
