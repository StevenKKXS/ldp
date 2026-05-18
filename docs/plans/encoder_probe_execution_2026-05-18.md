# Encoder Probe Execution Plan

Date: 2026-05-18

## Goal

Explore whether Direction A / Direction B are technically feasible before the next progress sync. The first target is useful observation, not a final method claim.

## Resource

- GPU node: `10.100.2.4`
- SSH port: `35140`
- GPUs observed: 8x NVIDIA H200

## Environment Priority

1. Prefer a PTP/release-like environment with RoboMimic `0.2.0`.
2. If not present on this node, use the closest available environment only for code smoke and record the mismatch.
3. Do not use GPU-node external network operations. Stage code from this CPU workspace to the node.

Current observation:

- `gmp-py310` exists and has torch/hydra/diffusers/robomimic, but RoboMimic is `0.4.0`.
- The documented py39/RoboMimic `0.2.0` venv `/root/ptp_ldp_py39` was not present on this node during initial check.

## Execution Order

### Stage 1: Code Feasibility

1. Implement one reusable encoder-pretraining workspace.
2. Support Direction B predictive objective:
   - same PTP obs inputs first,
   - small MLP decoder,
   - Huber loss on normalized action sequence,
   - decoder discarded after pretraining,
   - checkpoint compatible with existing `obs_encoder_dir` loading.
3. Support Direction A soft contrastive objective:
   - normalized action future slice,
   - diagonal-masked soft future-action contrastive loss,
   - projection head discarded after pretraining.

### Stage 2: Smoke Runs

Run small GPU smoke jobs:

1. `B_square_predictive`
2. `B_toolhang_predictive`
3. `A_square_contrastive`
4. `A_toolhang_contrastive`

Success criteria:

- dataset loads,
- forward/backward succeeds,
- logs contain finite train/val metrics,
- encoder checkpoint is written with `obs_encoder.*` keys.

### Stage 3: Parallel Short Probes

If smoke passes, run short exploratory pretraining on all available GPUs:

- Direction B square/tool_hang, past+future predictive,
- Direction A square/tool_hang, future-action contrastive,
- optional duplicated seeds or future-only variants if spare GPUs remain.

Do not interpret pretraining loss as policy success.

### Stage 4: Checkpoint Compatibility

For any successful pretraining run, run a one-batch exact PTP load smoke:

```text
pretrained encoder checkpoint -> existing PTP config -> obs_encoder_dir -> forward/backward
```

### Stage 5: Documentation

Record:

- environment versions,
- exact commands,
- GPU allocation,
- process ids,
- log paths,
- failures,
- first metrics,
- checkpoint compatibility result.

## Known Risk

Existing high-throughput PTP scripts use cached embedding datasets and `use_embed_if_present=true`, which bypasses `obs_encoder`. Encoder pretraining will not affect those runs unless embeddings are regenerated or cached embeddings are disabled. First smoke uses online obs encoder paths.
