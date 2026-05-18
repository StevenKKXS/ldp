# Direction A Status

Last updated: 2026-05-18

## Active Plan

- Active plan: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_a_future_action_contrastive/review_2026-05-18.md`

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
- No experiment has been launched.
- No validated conclusion exists.

## Current Decision

- Do not implement until the open design questions in `review_2026-05-18.md` are resolved.

## Next Step

- Discuss and finalize the first-pass implementation: aligned action chunk, feature-dim condition concat, B2 baseline, diagonal-masked soft CE, and offline representation checks.
