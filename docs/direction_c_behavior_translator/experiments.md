# Direction C Experiments

No experiments have been run.

## Planned Stage 1 Offline Translation

| ID | Task | Setting | Status | Result |
|---|---|---|---|---|
| C1-T1 | Square | single-frame -> future | planned | N/A |
| C1-T2 | Square | history -> future | planned | N/A |
| C1-T3 | Square | history -> past+future | selected first | N/A |
| C1-T4 | Square | shuffled history -> past+future | planned | N/A |
| C1-T5 | ToolHang | history -> future | planned | N/A |
| C1-T6 | ToolHang | history -> past+future | planned | N/A |

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
| First run | `C1-T3-square-history-past-future` |
| Obs horizon H | 16 |
| Past action horizon P | 16 |
| Future action horizon K | 8 |
| Loss | SmoothL1 past + SmoothL1 future |
| Checkpoint metric | `val/future_l1` |
| Smoke batch | 8 |
| First real batch | 32 |
| Epochs | 20 |
