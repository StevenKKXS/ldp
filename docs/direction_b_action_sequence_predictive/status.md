# Direction B Status

Last updated: 2026-05-18

## Active Plan

- Active plan: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_b_action_sequence_predictive/review_2026-05-18.md`

## Current Stage

- Encoder pretraining probes running on Square and ToolHang

## Completed Experiments

| Exp ID | Task | Setting | Best Score | Best Epoch | Status | Notes |
|---|---|---|---:|---:|---|---|
| B_square_predictive_smoke | Square | raw image, `n_obs_steps=16`, full action predictive Huber, batch 2, 1 train step | N/A | N/A | Completed | Smoke passed. Train loss `0.4260`, val loss `0.4002`. |
| B_toolhang_predictive_smoke | ToolHang | raw image, `n_obs_steps=16`, full action predictive Huber, batch 1, 1 train step | N/A | N/A | Completed | Smoke passed. Train loss `0.4394`, val loss `0.3929`. |

## Running Experiments

| Exp ID | Task | Setting | Current Epoch | Current Score | Status | Notes |
|---|---|---|---:|---:|---|---|
| B_square_full_seed42 | Square | predictive pretraining, full action sequence target, seed 42 | 1+ | N/A | Running | GPU 0 on `10.100.2.4`; output under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/B_square_full_seed42`. |
| B_square_future_seed42 | Square | predictive pretraining, future-only target, seed 42 | 0+ | N/A | Running | GPU 1 on `10.100.2.4`; compares future-only target against full action sequence target. |
| B_tool_hang_full_seed42 | ToolHang | predictive pretraining, full action sequence target, seed 42 | startup/training | N/A | Running | GPU 4 on `10.100.2.4`; raw image initialization takes several minutes. |
| B_tool_hang_future_seed42 | ToolHang | predictive pretraining, future-only target, seed 42 | startup/training | N/A | Running | GPU 5 on `10.100.2.4`; compares future-only target against full action sequence target. |

## Key Observations

- Initial direction document created.
- Detailed Direction B plan saved.
- Review recommends exact-PTP-compatible encoder pretraining first: auxiliary action decoder is discarded, and the existing PTP policy loads the pretrained encoder.
- Predictive pretraining smoke can run on raw image Square and ToolHang and writes compatible encoder checkpoints.
- Raw-image dataset configs must not include stale `embedding` under dataset-side `shape_meta`.
- No downstream PTP policy score exists.

## Current Decision

- Direction B remains the lower-risk pretraining probe; downstream policy should remain exact PTP in the first pass.

## Next Step

- Monitor full-vs-future pretraining probes, then use resulting encoder checkpoints for exact-PTP downstream frozen/finetune ablation on Square and ToolHang.
