# Direction A Status

Last updated: 2026-05-18

## Active Plan

- Active plan: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_a_future_action_contrastive/review_2026-05-18.md`
- Latest review update: `docs/direction_a_future_action_contrastive/review_update_ptp_compat_2026-05-18.md`

## Current Stage

- Encoder pretraining probes running on Square and ToolHang

## Completed Experiments

| Exp ID | Task | Setting | Best Score | Best Epoch | Status | Notes |
|---|---|---|---:|---:|---|---|
| A_square_contrastive_smoke | Square | raw image, `n_obs_steps=16`, future action soft contrastive, batch 4, 1 train step | N/A | N/A | Completed | First run exposed NaN from diagonal `0 * -inf`; fixed in commit `7dcc632`. Rerun train loss `1.2313`, val loss `1.2405`. |
| A_toolhang_contrastive_smoke | ToolHang | raw image, `n_obs_steps=16`, future action soft contrastive, batch 4, 1 train step | N/A | N/A | Completed | Smoke passed after NaN fix. Train loss `1.3928`, val loss `1.1212`. |

## Running Experiments

| Exp ID | Task | Setting | Current Epoch | Current Score | Status | Notes |
|---|---|---|---:|---:|---|---|
| A_square_future_seed42 | Square | contrastive pretraining, future action target, seed 42 | 0+ | N/A | Running | GPU 2 on `10.100.2.4`; output under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_square_future_seed42`. |
| A_square_future_seed43 | Square | contrastive pretraining, future action target, seed 43 | 0+ | N/A | Running | GPU 3 on `10.100.2.4`; output under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8/A_square_future_seed43`. |
| A_tool_hang_future_seed42 | ToolHang | contrastive pretraining, future action target, seed 42 | startup/training | N/A | Running | GPU 6 on `10.100.2.4`; raw image initialization is several minutes before GPU utilization rises. |
| A_tool_hang_future_seed43 | ToolHang | contrastive pretraining, future action target, seed 43 | startup/training | N/A | Running | GPU 7 on `10.100.2.4`; logs tracked in Session 8 PID table. |

## Key Observations

- Initial direction document created.
- Detailed Direction A plan saved.
- Review identified required decisions: action-window alignment, condition fusion tensor shape, B2 architecture parity, diagonal masking, action normalization, sigma choice, and frozen/finetune definition.
- User clarified first pass should reproduce PTP structure as much as possible; latest review update now recommends exact-PTP-compatible encoder pretraining rather than policy-side condition concat.
- Raw-image smoke requires removing stale `embedding` from dataset-side `shape_meta`; otherwise dataset conversion attempts to read missing `obs/embedding`.
- Soft contrastive loss must mask diagonal `log_p` before multiplying by `q`; diagonal masked `log_softmax` otherwise creates `0 * -inf = NaN`.
- Square and ToolHang contrastive smokes can write compatible encoder checkpoints.
- No downstream PTP policy score exists.

## Current Decision

- First-pass Direction A keeps the PTP policy architecture unchanged and uses future-action contrastive learning as encoder pretraining.

## Next Step

- Monitor running probes, then use resulting encoder checkpoints for exact-PTP downstream frozen/finetune ablation on Square and ToolHang.
