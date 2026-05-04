# Figure 9 Multistage Reproduction Plan

## Purpose

This is the proposed replacement plan for reproducing the paper's Figure 9 protocol directly.

Current raw-image runs are intentionally excluded from the main Figure 9 result plan. They remain useful as pilot evidence, but they should not be reported as Figure 9-aligned results unless separately labeled as raw-image / protocol-deviated.

No currently running jobs should be stopped until this plan is accepted.

## Official Encoder First Decision

Use the official `obs_encoders.zip` checkpoints as the initial Stage 1 assets instead of retraining short-history encoders first.

This does not remove the short-history stage from the protocol. It treats the released short-history encoders as the paper-provided output of that stage, then uses them to generate or validate frozen observation embeddings for long-history training.

Operationally:

- the first Figure 9-aligned pass should prioritize official encoder reuse
- short-hist DP remains a separate baseline row to evaluate or backfill
- end-to-end short-hist encoder retraining becomes an audit / ablation step after the main cached runs are moving
- every long-hist DP/PTP result must still record the encoder checkpoint used to produce its embeddings

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
- `long-hist DP` / `no-PTP` uses the same official-encoder cached recipe as `long-hist PTP`; the controlled difference is only `policy.past_action_pred`

## In-Scope Tasks

| Task Column | Dataset | Encoder Asset | Config Family | Status Before Launch |
|---|---|---|---|---|
| `Square` | `robomimic/datasets/square/mh/image_abs.hdf5` | `square_encoder.ckpt` | `experiment_configs/square` | encoder loads; embedding still must be generated |
| `Tool-Hang` | `robomimic/datasets/tool_hang/ph/image_abs.hdf5` | `tool_hang_encoder.ckpt` | `experiment_configs/tool` | encoder loads; embedding still must be generated |
| `Transport` | `robomimic/datasets/transport/mh/image_abs.hdf5` | `transport_encoder.ckpt` | `experiment_configs/transport` | encoder loads; `_emb` config needs embedding-shape/use-embed fixes |
| `Push-T` | `pusht/pusht_cchi_v7_replay.zarr` | `pusht_encoder.ckpt` | `experiment_configs` | encoder loads with override; cache path unsupported by current HDF5 rewrite script |
| `ALOHA / Cube` | `aloha_twomodes_single/demos.hdf5` | `aloha_encoder.ckpt` | `experiment_configs/aloha` | encoder loads; dataset already contains embeddings |
| `Long Square` | `longhistsquare100/demos.hdf5` | `longhist_encoder.ckpt` | `experiment_configs/longhist` | encoder loads; dataset already contains embeddings |

## Encoder And Cache Compatibility Snapshot

Validation performed on the 96h H200 node using the released checkpoints in `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/obs_encoders/obs_encoders`.

| Task | Encoder Load Check | Feature Dim | Data / Cache State | Required Before Figure 9 Launch |
|---|---:|---:|---|---|
| `Square` | OK | 137 | raw HDF5 present; `image_abs_emb.hdf5` exists but currently has no `obs/embedding` key | run `rewrite_with_embeddings.py` on a derived HDF5; set policy and dataset `use_embed_if_present=true`; use `global_obs=16` for long-hist rows |
| `Tool-Hang` | OK | 137 | raw HDF5 present; no embedding copy found yet | create derived HDF5, run rewrite, then set policy and dataset `use_embed_if_present=true` |
| `Transport` | OK | 274 | raw HDF5 present; current `_emb` config lacks `embedding` in dataset shape_meta and has no dataset `use_embed_if_present` | add `embedding.shape=[274]`, set dataset `use_embed_if_present=true`, prefer HDF5 embedding path with `use_cache=false` until a zarr cache is rebuilt |
| `Long Square` | OK | 137 | `demos.hdf5` already contains `obs/embedding` with 100 demos / 44,220 steps; configured `demos_emb.hdf5` path is absent | override dataset and env runner paths to `data/longhistsquare100/demos.hdf5`, or create the expected derived file before launch |
| `ALOHA / Cube` | OK | 135 | `demos.hdf5` already contains `obs/embedding` with 50 demos / 25,000 steps | set policy `use_embed_if_present=true`; override `past_action_pred` per DP/PTP row |
| `Push-T` | OK with `obs_encoder_dir=pusht_encoder.ckpt` override | 66 | zarr dataset present; current `_emb` config has `obs_encoder_dir: null` and no embedding dataset schema | keep out of main Figure 9 batch until Push-T zarr embedding rewrite or an equivalent cache path is implemented |

Notes:

- the official encoder dry-run loaded each checkpoint into the matching policy and froze the observation encoder successfully
- ALOHA's released checkpoint has a different original action head shape, but only the observation encoder state is reused; the target policy dry-run still loads with `obs_feature_dim=135`
- config placeholders such as `{REMINDER TO INSERT CACHE EMBEDDINGS}` must be replaced by explicit `true` overrides before launch

## Stage 0: Freeze Current Runs

Decision point:

- keep current raw-image jobs running until this plan is accepted
- after acceptance, stop raw-image jobs that compete for GPU budget
- preserve their output directories as pilot evidence

Current raw-image jobs are not part of the Figure 9 main result table.

## Stage 1: Build And Validate Embedding Caches

For each task:

1. Select the official encoder checkpoint.
2. If the HDF5 already contains a validated `obs/embedding` key, use it directly with explicit config overrides.
3. Otherwise run `rewrite_with_embeddings.py` on a derived HDF5, not the canonical raw dataset.
4. Produce or select a task-specific embedding dataset.
5. Validate loader compatibility with the corresponding `_emb` config.
6. Verify a sample batch contains embeddings and can run a forward/loss step.

Required validation before launching full jobs:

- cached dataset file exists and is readable
- dataset length matches the source dataset's episode/step count
- `_emb` config instantiates successfully
- `policy.use_embed_if_present=true` is active
- `task.dataset.use_embed_if_present=true` is active for HDF5 embedding datasets
- `obs_encoder_freeze=true` is active where expected
- embedding width matches policy `obs_feature_dim`
- one minibatch `compute_loss` succeeds

Push-T is a special case:

- `transformer_pusht_emb.yaml` exists
- official `pusht_encoder.ckpt` exists and loads into the policy with feature dim 66
- but the current config has `obs_encoder_dir: null`
- `rewrite_with_embeddings.py` only handles HDF5-style `data/demo_*` files, not the Push-T zarr replay directly
- do not launch Push-T as Figure 9-aligned until a Push-T embedding rewrite/cache path is implemented and smoke-tested

## Stage 2: Smoke-Test One Complete Cell Pair

Use two smoke checks:

1. `Long Square` cached-training smoke because its current `demos.hdf5` already contains embeddings and directly targets the history-critical task.
2. `Square` cache-generation smoke because it validates the official `rewrite_with_embeddings.py` path on the smallest RoboMimic task.

Smoke pair for each selected task:

- `long-hist DP`
- `long-hist PTP`

Required settings:

- cached embeddings active
- `_emb` config active
- `global_obs=16`
- `policy.past_action_pred=false` for DP
- `policy.past_action_pred=true` for PTP
- policy shape metadata remains raw-image-compatible so the official image encoder checkpoint loads
- dataset shape metadata should keep `embedding + lowdim` and omit image keys, so training avoids image preload while rollout keeps lowdim normalizer statistics
- image range normalizers must be present for online raw-observation rollout even when image arrays are omitted from the cached replay buffer
- output directories clearly named `fig9_*`

Success criteria:

- both jobs enter training
- both write `logs.json.txt`
- both pass at least one validation epoch
- checkpoint / rollout cadence does not crash on missing `test_mean_score`
- a sampled batch contains `obs["embedding"]` and does not carry raw image tensors when `use_embed_if_present=true`

## Stage 3: Launch Figure 9 Main Rows

For each task column, run the three canonical rows:

- `short-hist DP`
- `long-hist DP`
- `long-hist PTP`

Launch priority:

1. `Long Square`
2. `ALOHA / Cube`
3. `Square`
4. `Tool-Hang`
5. `Transport`
6. `Push-T`

Rationale:

- `Long Square` and `ALOHA / Cube` already contain embeddings and can validate cached training fastest
- `Square` validates the embedding-generation pipeline cheaply
- `Long Square` is the most direct history-critical simulation target
- `Tool-Hang` and `Transport` are already data-ready and central to the current work
- `Transport` needs a small `_emb` config repair before it is a true cached-embedding run
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
2. Run `Long Square long-hist DP/PTP` smoke using existing `demos.hdf5` embeddings and explicit path/use-embed overrides.
3. In parallel, generate / validate `Square` embeddings on a derived HDF5.
4. If both smoke checks succeed, generate `Tool-Hang` and `Transport` embeddings.
5. Repair Transport `_emb` config overrides before launching its cached runs.
6. Launch the first Figure 9-aligned batch of main-row runs.
