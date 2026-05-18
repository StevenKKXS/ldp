# Direction A Status

Last updated: 2026-05-18

## Active Plan

- Active plan: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_a_future_action_contrastive/review_2026-05-18.md`
- Latest review update: `docs/direction_a_future_action_contrastive/review_update_ptp_compat_2026-05-18.md`

## Current Stage

- Encoder pretraining probes completed on Square and ToolHang

## Completed Experiments

| Exp ID | Task | Setting | Best Score | Best Epoch | Status | Notes |
|---|---|---|---:|---:|---|---|
| A_square_contrastive_smoke | Square | raw image, `n_obs_steps=16`, future action soft contrastive, batch 4, 1 train step | N/A | N/A | Completed | First run exposed NaN from diagonal `0 * -inf`; fixed in commit `7dcc632`. Rerun train loss `1.2313`, val loss `1.2405`. |
| A_toolhang_contrastive_smoke | ToolHang | raw image, `n_obs_steps=16`, future action soft contrastive, batch 4, 1 train step | N/A | N/A | Completed | Smoke passed after NaN fix. Train loss `1.3928`, val loss `1.1212`. |
| A_square_future_seed42 | Square | contrastive pretraining, future action target, seed 42 | N/A | N/A | Completed | 10 epochs, final train loss `3.3737`, final val loss `3.3962`; checkpoint written. |
| A_square_future_seed43 | Square | contrastive pretraining, future action target, seed 43 | N/A | N/A | Completed | 10 epochs, final train loss `3.3742`, final val loss `3.3965`; checkpoint written. |
| A_tool_hang_future_seed42 | ToolHang | contrastive pretraining, future action target, seed 42 | N/A | N/A | Completed | 10 epochs, final train loss `2.6360`, final val loss `2.6933`; checkpoint written. |
| A_tool_hang_future_seed43 | ToolHang | contrastive pretraining, future action target, seed 43 | N/A | N/A | Completed | 10 epochs, final train loss `2.6395`, final val loss `2.6921`; checkpoint written. |

## Running Experiments

| Exp ID | Task | Setting | Current Epoch | Current Score | Status | Notes |
|---|---|---|---:|---:|---|---|

## Key Observations

- Initial direction document created.
- Detailed Direction A plan saved.
- Review identified required decisions: action-window alignment, condition fusion tensor shape, B2 architecture parity, diagonal masking, action normalization, sigma choice, and frozen/finetune definition.
- User clarified first pass should reproduce PTP structure as much as possible; latest review update now recommends exact-PTP-compatible encoder pretraining rather than policy-side condition concat.
- Raw-image smoke requires removing stale `embedding` from dataset-side `shape_meta`; otherwise dataset conversion attempts to read missing `obs/embedding`.
- Soft contrastive loss must mask diagonal `log_p` before multiplying by `q`; diagonal masked `log_softmax` otherwise creates `0 * -inf = NaN`.
- Square and ToolHang contrastive smokes can write compatible encoder checkpoints.
- Four long-run contrastive pretraining probes completed 10 epochs and wrote `latest.ckpt`.
- No downstream PTP policy score exists.

## Current Decision

- First-pass Direction A keeps the PTP policy architecture unchanged and uses future-action contrastive learning as encoder pretraining.

## Next Step

- Use resulting encoder checkpoints for exact-PTP downstream frozen/finetune ablation on Square and ToolHang.
