# Direction B Status

Last updated: 2026-05-18

## Active Plan

- Active plan: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_b_action_sequence_predictive/review_2026-05-18.md`

## Current Stage

- Encoder pretraining probes completed on Square and ToolHang

## Completed Experiments

| Exp ID | Task | Setting | Best Score | Best Epoch | Status | Notes |
|---|---|---|---:|---:|---|---|
| B_square_predictive_smoke | Square | raw image, `n_obs_steps=16`, full action predictive Huber, batch 2, 1 train step | N/A | N/A | Completed | Smoke passed. Train loss `0.4260`, val loss `0.4002`. |
| B_toolhang_predictive_smoke | ToolHang | raw image, `n_obs_steps=16`, full action predictive Huber, batch 1, 1 train step | N/A | N/A | Completed | Smoke passed. Train loss `0.4394`, val loss `0.3929`. |
| B_square_full_seed42 | Square | predictive pretraining, full action sequence target, seed 42 | N/A | N/A | Completed | 10 epochs, final train loss `0.0167`, final val loss `0.0373`; checkpoint written. |
| B_square_future_seed42 | Square | predictive pretraining, future-only target, seed 42 | N/A | N/A | Completed | 10 epochs, final train loss `0.0164`, final val loss `0.0426`; checkpoint written. |
| B_tool_hang_full_seed42 | ToolHang | predictive pretraining, full action sequence target, seed 42 | N/A | N/A | Completed | 10 epochs, final train loss `0.0243`, final val loss `0.0494`; checkpoint written. |
| B_tool_hang_future_seed42 | ToolHang | predictive pretraining, future-only target, seed 42 | N/A | N/A | Completed | 10 epochs, final train loss `0.0252`, final val loss `0.0420`; checkpoint written. |

## Running Experiments

| Exp ID | Task | Setting | Current Epoch | Current Score | Status | Notes |
|---|---|---|---:|---:|---|---|

## Key Observations

- Initial direction document created.
- Detailed Direction B plan saved.
- Review recommends exact-PTP-compatible encoder pretraining first: auxiliary action decoder is discarded, and the existing PTP policy loads the pretrained encoder.
- Predictive pretraining smoke can run on raw image Square and ToolHang and writes compatible encoder checkpoints.
- Raw-image dataset configs must not include stale `embedding` under dataset-side `shape_meta`.
- Four long-run predictive pretraining probes completed 10 epochs and wrote `latest.ckpt`.
- No downstream PTP policy score exists.

## Current Decision

- Direction B remains the lower-risk pretraining probe; downstream policy should remain exact PTP in the first pass.

## Next Step

- Use resulting encoder checkpoints for exact-PTP downstream frozen/finetune ablation on Square and ToolHang.
