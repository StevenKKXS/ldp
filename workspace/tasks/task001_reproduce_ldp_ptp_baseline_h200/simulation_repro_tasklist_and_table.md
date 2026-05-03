# Simulation Repro Tasklist And Result Table

## Purpose

This file is the working artifact for the simulation-side reproduction effort.

It keeps two things in one place:

1. the execution task list
2. the result tables to fill as runs complete

This version is intentionally trimmed to keep only tasks and comparisons that are meaningfully alignable with the current public PTP repo workflow.

## In-Scope Simulation Targets

Main aligned targets:

- `Square`
- `Tool-Hang`
- `Transport`
- `Push-T`
- `ALOHA / Cube`
- `Long Square`

Explicitly removed from the working table:

- `Lift`
- `Can`
- `LDP` row

Reason:

- `Lift` / `Can` do not have turnkey config families in this repo snapshot
- `LDP` is a different lab project line, not the same method family we are reproducing here

## Task List

### P0: Data Staging

- Confirm `robomimic_image.zip` fully finishes and exposes:
  - `tool_hang`
  - `transport`
  - any other needed RoboMimic subfolders
- Confirm `pusht` extracted to `data/pusht/pusht_cchi_v7_replay.zarr`
- Confirm `aloha_twomodes_single/demos.hdf5`
- Confirm `longhistsquare100/demos.hdf5`

### P1: Main Result Rows

- `Square`
  - matched `DP`-style baseline
  - matched `PTP`
- `Tool-Hang`
  - matched `DP`-style baseline
  - matched `PTP`
- `Transport`
  - matched `DP`-style baseline
  - matched `PTP`
- `Push-T`
  - matched baseline
  - matched `PTP` if config / adaptation is valid
- `ALOHA / Cube`
  - matched baseline
  - matched `PTP`
- `Long Square`
  - matched baseline
  - matched `PTP`

### P2: Ablation Fill-Ins

Use ablations to fill the story even when some headline cells are slow to converge.

Priority ablations:

- `no-history` vs `no-PTP` vs `PTP`
- `obs=2` vs `obs=16`
- raw-image vs cached-embedding
- short-context encoder frozen vs not frozen if relevant
- early checkpoint trend vs later checkpoint trend
- single-seed pilot vs repeated-seed confirmation

### P3: Metadata Capture

For every filled cell, record:

- config name
- dataset path
- checkpoint path
- seed count
- metric source
- whether the result is early / pilot / converged

## Main Result Table

Legend:

- `Paper` = number from the target paper / user-provided table
- `Repro` = our value to fill in
- blank `Repro` means not yet filled

| Method | Setting / Source | Square Paper | Square Repro | Tool-Hang Paper | Tool-Hang Repro | Transport Paper | Transport Repro | Push-T Paper | Push-T Repro | ALOHA / Cube Paper | ALOHA / Cube Repro | Long Square Paper | Long Square Repro | Source-specific Avg. Paper | Source-specific Avg. Repro | Notes |
|---|---|---:|---|---:|---|---:|---|---:|---|---:|---|---:|---|---:|---|---|
| DP | PTP internal baseline: Diffusion (no-hist) | 0.79 ± 0.06 |  | 0.51 ± 0.14 |  | 0.60 ± 0.08 |  | 0.67 ± 0.03 |  | 0.28 ± 0.04 |  | 0.12 ± 0.05 |  | 0.50 |  | Main baseline row to align first. |
| PTP | Diffusion (PTP) | 0.89 ± 0.01 |  | 0.75 ± 0.10 |  | 0.67 ± 0.08 |  | 0.62 ± 0.02 |  | 0.98 ± 0.01 |  | 0.93 ± 0.02 |  | 0.81 |  | Main method row to align first. |

## Ablation Table

Use this table even if the main result table is still incomplete.

| Task | Comparison | Paper Expectation | Current Repro | Status | Notes |
|---|---|---|---|---|---|
| Square | `no-history` vs `no-PTP` vs `PTP` | `PTP` should beat matched baseline | `no-PTP=0.05`, `PTP=0.2` at early checkpoint | pilot | Early only, not final |
| Square | `obs=2` vs `obs=16` | long history should matter more with PTP |  | open | Fill after matched reruns |
| Square | raw vs cached embeddings | cached should speed training materially |  | open | Fill once cache path is exercised in training |
| Tool-Hang | baseline vs `PTP` | `PTP` should improve long-context performance |  | blocked on data / run |  |
| Transport | baseline vs `PTP` | `PTP` should improve long-context performance |  | blocked on data / run |  |
| Push-T | baseline vs `PTP` | unclear strength, useful supporting ablation |  | blocked on data / run |  |
| ALOHA / Cube | baseline vs `PTP` | large gain expected from paper table |  | blocked on data / run |  |
| Long Square | baseline vs `PTP` | strong gain expected from paper table |  | blocked on data / run |  |

## Immediate Fill Targets

- Fill `Square` first because it already has partial pilot evidence.
- Fill `Tool-Hang` and `Transport` next once `robomimic_image` backfill completes.
- Fill `Long Square` and `ALOHA / Cube` next because they are directly tied to paper-specific long-history datasets.
- Use the ablation table aggressively even before all headline cells converge.

## Review Notes

This file is intentionally biased toward:

- aligned comparisons
- public-data-supported tasks
- ablations that let us say something useful before every headline number is finished
