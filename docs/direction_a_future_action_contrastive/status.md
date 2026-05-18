# Direction A Status

Last updated: 2026-05-18

## Active Plan

- Active plan: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_a_future_action_contrastive/review_2026-05-18.md`
- Latest review update: `docs/direction_a_future_action_contrastive/review_update_ptp_compat_2026-05-18.md`

## Current Stage

- Reviewed, discussion needed before implementation

## Completed Experiments

| Exp ID | Task | Setting | Best Score | Best Epoch | Status | Notes |
|---|---|---|---:|---:|---|---|

## Running Experiments

| Exp ID | Task | Setting | Current Epoch | Current Score | Status | Notes |
|---|---|---|---:|---:|---|---|

## Key Observations

- Initial direction document created.
- Detailed Direction A plan saved.
- Review identified required decisions: action-window alignment, condition fusion tensor shape, B2 architecture parity, diagonal masking, action normalization, sigma choice, and frozen/finetune definition.
- User clarified first pass should reproduce PTP structure as much as possible; latest review update now recommends exact-PTP-compatible encoder pretraining rather than policy-side condition concat.
- No experiment has been launched.
- No validated conclusion exists.

## Current Decision

- First-pass Direction A should keep the PTP policy architecture unchanged and use future-action contrastive learning as encoder pretraining.

## Next Step

- Discuss and finalize the PTP-compatible pretraining protocol: exact PTP baseline config, action segment used for behavior similarity, encoder checkpoint format, frozen/finetune settings, and whether B2 is distinct from B1.
