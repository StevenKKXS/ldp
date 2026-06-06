# Direction A Status

Last updated: 2026-05-19

## Active Plan

- Active plan: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_a_future_action_contrastive/review_2026-05-18.md`
- Latest review update: `docs/direction_a_future_action_contrastive/review_update_ptp_compat_2026-05-18.md`

## Current Stage

- Downstream exact-PTP first matrix completed; seed-43 repeat running

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
| square_A_future_finetune | Square | exact PTP, `A_square_future_seed42` encoder, finetune | 17 | val loss `0.0866` | Running | Main matrix; below original val `0.0965` at latest poll. |
| square_A_future_frozen | Square | exact PTP, `A_square_future_seed42` encoder, frozen | 8 | val loss `0.1001` | Running | Extra matrix; still earlier in training than main matrix. |
| square_A_future_seed43_finetune | Square | exact PTP, `A_square_future_seed43` encoder, finetune | 7 | val loss `0.1126` | Running | Extra matrix seed-sensitivity probe. |
| tool_hang_A_future_finetune | ToolHang | exact PTP, `A_tool_hang_future_seed42` encoder, finetune | 6 | val loss `0.1572` | Running | Main matrix; close to original val `0.1568`. |
| tool_hang_A_future_frozen | ToolHang | exact PTP, `A_tool_hang_future_seed42` encoder, frozen | 2 | val loss `0.2679` | Running | Extra matrix. |
| tool_hang_A_future_seed43_finetune | ToolHang | exact PTP, `A_tool_hang_future_seed43` encoder, finetune | 1 | val loss `0.3481` | Running | Extra matrix seed-sensitivity probe. |

## Key Observations

- Initial direction document created.
- Detailed Direction A plan saved.
- Review identified required decisions: action-window alignment, condition fusion tensor shape, B2 architecture parity, diagonal masking, action normalization, sigma choice, and frozen/finetune definition.
- User clarified first pass should reproduce PTP structure as much as possible; latest review update now recommends exact-PTP-compatible encoder pretraining rather than policy-side condition concat.
- Raw-image smoke requires removing stale `embedding` from dataset-side `shape_meta`; otherwise dataset conversion attempts to read missing `obs/embedding`.
- Soft contrastive loss must mask diagonal `log_p` before multiplying by `q`; diagonal masked `log_softmax` otherwise creates `0 * -inf = NaN`.
- Square and ToolHang contrastive smokes can write compatible encoder checkpoints.
- Four long-run contrastive pretraining probes completed 10 epochs and wrote `latest.ckpt`.
- Session 10 exact-PTP downstream probes are running from those checkpoints.
- Early Direction A downstream train/val diffusion losses are close to original encoder baselines; no rollout success-rate score exists.
- First completed 50-epoch Square matrix favored `A_future_frozen` in train/val diffusion loss: best val `0.0677` vs original `0.0711`.
- First completed 50-epoch ToolHang matrix did not show a clear Direction A separation; best vals were clustered around `0.0636-0.0646`.
- Seed-43 repeat includes `square_A_future_frozen_s43` and `tool_hang_A_future_frozen_s43`.

## Current Decision

- First-pass Direction A keeps the PTP policy architecture unchanged and uses future-action contrastive learning as encoder pretraining. Square `A_future_frozen` is the current strongest loss-only row, pending seed-43 repeat and rollout evaluation.

## Next Step

- Poll Session 13 seed-43 repeat and evaluate whether `A_future_frozen` remains ahead of original on Square.
