# Direction B Status

Last updated: 2026-05-18

## Active Plan

- Active plan: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`
- Review: `docs/direction_b_action_sequence_predictive/review_2026-05-18.md`

## Current Stage

- Reviewed, PTP-compatible encoder-pretraining first pass preferred

## Completed Experiments

| Exp ID | Task | Setting | Best Score | Best Epoch | Status | Notes |
|---|---|---|---:|---:|---|---|

## Running Experiments

| Exp ID | Task | Setting | Current Epoch | Current Score | Status | Notes |
|---|---|---|---:|---:|---|---|

## Key Observations

- Initial direction document created.
- Detailed Direction B plan saved.
- Review recommends exact-PTP-compatible encoder pretraining first: auxiliary action decoder is discarded, and the existing PTP policy loads the pretrained encoder.
- No experiment has been launched.
- No validated conclusion exists.

## Current Decision

- Direction B is a good low-cost implementation smoke candidate, but downstream policy should remain exact PTP in the first pass.

## Next Step

- Decide exact PTP baseline, target action sequence, decoder capacity, encoder checkpoint format, and frozen/finetune protocol.
