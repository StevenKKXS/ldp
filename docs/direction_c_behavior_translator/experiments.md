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

## Session 70 Input Contract

Current Square image configs use only rollout-observable signals as policy or translator inputs:

| Input group | Config key | Shape | Meaning |
|---|---|---:|---|
| Image 1 | `agentview_image` | `[3,84,84]` | third-person/front RGB camera |
| Image 2 | `robot0_eye_in_hand_image` | `[3,84,84]` | wrist / eye-in-hand RGB camera |
| Proprio | `robot0_eef_pos` | `[3]` | end-effector Cartesian position |
| Proprio | `robot0_eef_quat` | `[4]` | end-effector orientation quaternion |
| Proprio | `robot0_gripper_qpos` | `[2]` | gripper joint positions |

Do not mix in `past_act`, object state, simulator state, reward, or privileged task variables for the Direction C translator unless an ablation explicitly marks them as privileged. The current Stage1 translator configs use `image_abs.hdf5`, not `image_abs_past.hdf5`, and their `shape_meta` does not include `past_act`.

Fast modality checks before more downstream runs:

| Check | Train-time change | Eval-time change | Purpose |
|---|---|---|---|
| Full input | none | none | reference |
| Image masked | none | zero or shuffle both RGB streams | test whether trained model depends on images |
| Proprio masked | none | zero or shuffle all lowdim keys | test whether trained model depends on proprio |
| Lowdim-only retrain | remove RGB keys | none | test whether proprio alone matches full input |
| Image-only retrain | remove lowdim keys | none | test whether images alone learn useful behavior context |

## Session 70 Revised Stage2b Downstream Plan

The downstream matrix is split into two baselines and two translator-integration mechanisms. All rollout-facing policies must use only the observable input contract above.

### Baselines

| ID | Name | Policy family | Condition | Prediction target | Purpose |
|---|---|---|---|---|---|
| B0 | `base_dp_obs2` | default DP | `cond[0..1]`, `n_obs_steps=2` | future action chunk | Standard short-context DP baseline |
| B1 | `base_ptp_obs16_past_future` | proven PTP path | `cond[0..15]`, `n_obs_steps=16` | past + future action objective, rollout uses future action chunk | Strong long-context PTP baseline |

### Translator Projection Path

This keeps the base policy image/proprio encoder and adds frozen translator context through a learned projection. This is the current implemented path.

| ID | Base | Translator | Injection | Control meaning |
|---|---|---|---|---|
| P0 | B1 | frozen random translator | `project(context) -> add_last` | architecture / extra-parameter control |
| P1 | B1 | frozen pretrained translator | `project(context) -> add_last` | low-risk behavior-context injection |
| P2 | B1 | frozen pretrained translator | `project(context) -> add_all` | stronger broadcast injection |

### Translator Encoder Replacement Path

This path directly replaces or initializes the downstream observation encoder from the translator-side encoder, then trains the PTP/DP head on top. It tests whether the useful part is the learned visual/proprio encoder rather than the pooled behavior context.

| ID | Base | Encoder source | Frozen | Purpose |
|---|---|---|---:|---|
| R0 | B1 | random same-architecture encoder | yes | replacement control |
| R1 | B1 | translator pretrained obs encoder | yes | frozen encoder transfer |
| R2 | B1 | translator pretrained obs encoder | no | finetuned encoder transfer |
| R3 | B0 | translator pretrained obs encoder | no | test whether translator encoder helps default DP |

Execution order when more GPUs are available:

1. Run B0 and B1 first to anchor the SR scale.
2. Run P0/P1/P2 with identical seeds and rollout protocol.
3. Run R0/R1/R2 to separate context projection from encoder transfer.
4. Run R3 only after B0 is measured, because it is the DP-side transfer question rather than the main PTP-context question.

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
