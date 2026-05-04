# Figure 9 Multistage Reproduction Plan

## Purpose

This is the proposed replacement plan for reproducing the paper's Figure 9 protocol directly.

Current raw-image runs are intentionally excluded from the main Figure 9 result plan. They remain useful as pilot evidence, but they should not be reported as Figure 9-aligned results unless separately labeled as raw-image / protocol-deviated.

No currently running jobs should be stopped until this plan is accepted.

## Protocol Interpretation

Figure 9 should be treated as a comparison under the paper's default training protocol:

- history-conditioned policies use long visual/proprioceptive context
- `no-PTP` and `PTP` differ by the past-token-prediction objective
- unless otherwise specified, policies use the multistage recipe with feature caching
- evaluation is over the simulation tasks in Figure 9

Canonical method mapping:

| Table Row | Meaning | PTP Objective | Training Recipe |
|---|---|---|---|
| `short-hist DP` | no-history / short-context diffusion baseline | off | multistage/cached where applicable |
| `long-hist DP` | long-context diffusion baseline without PTP | off | multistage/cached |
| `long-hist PTP` | paper method | on | multistage/cached |

Important distinction:

- `PTP` is the algorithmic objective: `policy.past_action_pred=true`
- `multistage` is the training recipe: short-context encoder, cached embeddings, long-context policy-head training
- Figure 9-aligned `PTP` requires both of those when reproducing the paper row

## In-Scope Tasks

| Task Column | Dataset | Encoder Asset | Config Family | Status Before Launch |
|---|---|---|---|---|
| `Square` | `robomimic/datasets/square/mh/image_abs.hdf5` | `square_encoder.ckpt` | `experiment_configs/square` | data and encoder present |
| `Tool-Hang` | `robomimic/datasets/tool_hang/ph/image_abs.hdf5` | `tool_hang_encoder.ckpt` | `experiment_configs/tool` | data and encoder present |
| `Transport` | `robomimic/datasets/transport/mh/image_abs.hdf5` | `transport_encoder.ckpt` | `experiment_configs/transport` | data and encoder present |
| `Push-T` | `pusht/pusht_cchi_v7_replay.zarr` | needs validation | `experiment_configs` | config exists; encoder path needs validation |
| `ALOHA / Cube` | `aloha_twomodes_single/demos.hdf5` | `aloha_encoder.ckpt` | `experiment_configs/aloha` | data and encoder present |
| `Long Square` | `longhistsquare100/demos.hdf5` | `longhist_encoder.ckpt` | `experiment_configs/longhist` | data and encoder present |

## Stage 0: Freeze Current Runs

Decision point:

- keep current raw-image jobs running until this plan is accepted
- after acceptance, stop raw-image jobs that compete for GPU budget
- preserve their output directories as pilot evidence

Current raw-image jobs are not part of the Figure 9 main result table.

## Stage 1: Build And Validate Embedding Caches

For each task:

1. Select the official encoder checkpoint.
2. Run `rewrite_with_embeddings.py` on the raw dataset.
3. Produce a task-specific cached / embedding dataset.
4. Validate loader compatibility with the corresponding `_emb` config.
5. Verify a sample batch contains embeddings and can run a forward/loss step.

Required validation before launching full jobs:

- cached dataset file exists and is readable
- dataset length matches the source dataset's episode/step count
- `_emb` config instantiates successfully
- `policy.use_embed_if_present=true` is active
- `obs_encoder_freeze=true` is active where expected
- one minibatch `compute_loss` succeeds

Push-T is a special case:

- `transformer_pusht_emb.yaml` exists
- but the observed config has `obs_encoder_dir: null`
- do not launch Push-T as Figure 9-aligned until the intended encoder/cache path is confirmed

## Stage 2: Smoke-Test One Complete Cell Pair

Start with `Square` because it is smallest and already has the most local history.

Smoke pair:

- `Square long-hist DP`
- `Square long-hist PTP`

Required settings:

- cached embeddings active
- `_emb` config active
- `global_obs=16`
- `policy.past_action_pred=false` for DP
- `policy.past_action_pred=true` for PTP
- output directories clearly named `fig9_*`

Success criteria:

- both jobs enter training
- both write `logs.json.txt`
- both pass at least one validation epoch
- checkpoint / rollout cadence does not crash on missing `test_mean_score`

## Stage 3: Launch Figure 9 Main Rows

For each task column, run the three canonical rows:

- `short-hist DP`
- `long-hist DP`
- `long-hist PTP`

Launch priority:

1. `Square`
2. `Long Square`
3. `Tool-Hang`
4. `Transport`
5. `ALOHA / Cube`
6. `Push-T`

Rationale:

- `Square` validates the cached pipeline cheaply
- `Long Square` is the most direct history-critical simulation target
- `Tool-Hang` and `Transport` are already data-ready and central to the current work
- `ALOHA / Cube` has a large paper-side gain and should follow once the pipeline is stable
- `Push-T` should wait until its encoder/cache path is verified

## Stage 4: Seeds And Evaluation

Paper-facing target:

- evaluate each task-method pair over `100` episodes
- aggregate across `3` seeds where feasible

Practical first pass:

- one seed for all task-method cells
- confirm metric direction and pipeline stability
- then add seeds for the most important cells:
- `Long Square long-hist DP/PTP`
- `Tool-Hang long-hist DP/PTP`
- `Transport long-hist DP/PTP`
- `ALOHA / Cube long-hist DP/PTP`

Do not mix pilot raw-image values into the aggregate table.

## Stage 5: Result Table Rules

Every filled result must record:

- task
- row name
- seed
- config name
- dataset path
- encoder checkpoint
- cached dataset path
- checkpoint path
- evaluation command
- number of eval episodes
- whether it is `Figure 9-aligned`

Allowed labels:

- `fig9-aligned`
- `pilot/raw-image`
- `failed`
- `smoke-only`

Main result table should only aggregate `fig9-aligned` cells.

## Stage 6: Ablations After Main Protocol

Ablations should come after the Figure 9 protocol is launched, not before.

Useful ablations:

- raw-image versus cached embeddings
- early checkpoint versus later checkpoint trend
- `Tool-Hang batch_size=32` memory ablation
- test-time PTP verification

These should be reported separately from the Figure 9 main table.

## Immediate Next Actions After Approval

1. Stop current raw-image jobs that compete for GPU budget.
2. Generate / validate cached embeddings for `Square`.
3. Run `Square long-hist DP/PTP` smoke pair under `_emb` configs.
4. If smoke succeeds, cache `Long Square`, `Tool-Hang`, and `Transport`.
5. Launch the first Figure 9-aligned batch of main-row runs.

