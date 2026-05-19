# Direction C Experiments

Stage 1 Square comparison jobs are running on `10.100.2.35:25076` in py39 / `robomimic==0.2.0`.

## Planned Stage 1 Offline Translation

| ID | Task | Setting | Status | Result |
|---|---|---|---|---|
| C1-T1 | Square | single-frame -> future | deferred | N/A |
| C1-T2 | Square | history -> future | implemented config | N/A |
| C1-T3 | Square | history -> past+future | GPU smoke passed; formal run started | one-step GPU smoke only so far |
| C1-T4 | Square | shuffled history -> past+future | planned | N/A |
| C1-T5 | ToolHang | history -> future | planned | N/A |
| C1-T6 | ToolHang | history -> past+future | planned | N/A |
| C1-T7 | Square | history -> past | formal run started | N/A |

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

`behavior_translator_square_past_future` GPU smoke:

| Field | Value |
|---|---|
| Node | `10.100.2.35:25076` |
| Env | `/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020` |
| Run dir | `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/smoke/gpu_smoke_20260519_142812` |
| Setting | 1 epoch, 2 train steps, 1 val batch, batch size 2 |
| Result | completed; wrote `best.ckpt`, `latest.ckpt`, `metrics.csv`, `logs.json.txt`, and `env.json` |

## Active Formal Runs

Run root:

```text
/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage1_square_20260519_143020
```

| ID | Config | GPU | PID | Status |
|---|---|---:|---:|---|
| C1-T7 | `behavior_translator_square_past` | 0 | 26881 | epoch 1 running |
| C1-T2 | `behavior_translator_square_future` | 1 | 26883 | epoch 1 running |
| C1-T3 | `behavior_translator_square_past_future` | 2 | 26885 | epoch 1 running |
