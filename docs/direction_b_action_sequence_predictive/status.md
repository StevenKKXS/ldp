# Direction B Status

Last updated: 2026-05-19

## Active Plan

- Active plan: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_b_action_sequence_predictive/review_2026-05-18.md`

## Current Stage

- Downstream exact-PTP probes running on Square and ToolHang

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
| square_B_full_frozen | Square | exact PTP, `B_square_full_seed42` encoder, frozen | 18 | val loss `0.0933` | Running | Main matrix; below original val `0.0965` at latest poll. |
| square_B_full_finetune | Square | exact PTP, `B_square_full_seed42` encoder, finetune | 17 | val loss `0.0865` | Running | Main matrix; currently close to `A_future_finetune`. |
| square_B_future_frozen | Square | exact PTP, `B_square_future_seed42` encoder, frozen | 8 | val loss `0.1012` | Running | Extra matrix; still earlier in training than main matrix. |
| square_B_future_finetune | Square | exact PTP, `B_square_future_seed42` encoder, finetune | 7 | val loss `0.1144` | Running | Extra matrix. |
| tool_hang_B_full_frozen | ToolHang | exact PTP, `B_tool_hang_full_seed42` encoder, frozen | 6 | val loss `0.1585` | Running | Main matrix; currently above original val `0.1568`. |
| tool_hang_B_full_finetune | ToolHang | exact PTP, `B_tool_hang_full_seed42` encoder, finetune | 6 | val loss `0.1566` | Running | Main matrix; close to original val `0.1568`. |
| tool_hang_B_future_frozen | ToolHang | exact PTP, `B_tool_hang_future_seed42` encoder, frozen | 2 | val loss `0.2668` | Running | Extra matrix. |
| tool_hang_B_future_finetune | ToolHang | exact PTP, `B_tool_hang_future_seed42` encoder, finetune | 2 | val loss `0.2624` | Running | Extra matrix. |

## Key Observations

- Initial direction document created.
- Detailed Direction B plan saved.
- Review recommends exact-PTP-compatible encoder pretraining first: auxiliary action decoder is discarded, and the existing PTP policy loads the pretrained encoder.
- Predictive pretraining smoke can run on raw image Square and ToolHang and writes compatible encoder checkpoints.
- Raw-image dataset configs must not include stale `embedding` under dataset-side `shape_meta`.
- Four long-run predictive pretraining probes completed 10 epochs and wrote `latest.ckpt`.
- Session 10 exact-PTP downstream probes are running from those checkpoints.
- Early Direction B downstream train/val diffusion losses are close to original encoder baselines; no rollout success-rate score exists.

## Current Decision

- Direction B remains the lower-risk pretraining probe; downstream policy remains exact PTP in the first pass. Continue comparing full-target vs future-only and frozen vs finetuned loss curves before any rollout request.

## Next Step

- Poll Session 10 downstream jobs and compare completed Square / ToolHang loss curves against original encoder baselines.
