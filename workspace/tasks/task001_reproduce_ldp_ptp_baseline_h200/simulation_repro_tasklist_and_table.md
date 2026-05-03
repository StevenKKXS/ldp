# Simulation Repro Tasklist And Result Table

## Purpose

This file turns the current simulation-side reproduction plan into:

1. a concrete task list ordered by practical feasibility
2. a fill-in result table that preserves the paper-reported numbers and leaves space for our reproduced values

The intent is operational, not archival: use this file as the working checklist for the simulation-only reproduction effort.

## Current Reproduction Boundary

- Already runnable with current staged data:
  - `Square`
- Expected to become runnable after current public-data backfill finishes:
  - `Tool-Hang`
  - `Transport`
  - `Push-T`
  - `ALOHA / Cube`
  - `Long Square`
- Not turnkey from this repo snapshot:
  - `Lift`
  - `Can`
- Not directly reproducible from this repo alone:
  - the source-specific `LDP` row in the quoted table

## Task List

### P0: Validate public data backfill

- Confirm `robomimic_image.zip` finished and that `tool_hang` / `transport` files are present under shared storage.
- Confirm `pusht` extracted to `data/pusht/pusht_cchi_v7_replay.zarr`.
- Confirm `aloha_twomodes_single/demos.hdf5` exists and matches the config path.
- Confirm `longhistsquare100/demos.hdf5` exists and matches the config path.

### P1: Lock down directly supported PTP-vs-baseline tasks

- `Square`
  - Finish / re-run matched `no-history`, `no-PTP`, and `PTP` comparisons.
  - Fill the `DP` and `PTP` rows first.
- `Tool-Hang`
  - Run the standard long-context baseline and PTP config family after data staging.
- `Transport`
  - Run the standard long-context baseline and PTP config family after data staging.
- `Push-T`
  - Verify dataset path and run the available config family.
- `ALOHA / Cube`
  - Run the available ALOHA config family on `aloha_twomodes_single`.
- `Long Square`
  - Run the dedicated `longhist` config family on `longhistsquare100`.

### P2: Record exact reproduction metadata

- For each completed cell, record:
  - config name
  - dataset path
  - checkpoint path
  - seed count
  - metric extraction command
  - whether the result is early / single-seed / converged

### P3: Non-turnkey extensions

- Decide whether to author local `lift` / `can` configs to extend beyond the current public turnkey scope.
- Decide whether to treat the `LDP` row as out-of-scope or to reproduce it via a separate codebase / baseline stack.

## Fill-In Result Table

Legend:

- `Paper` = number reported in the paper / user-provided target table
- `Repro` = our reproduced number to fill in
- `N/A` = not applicable for that method row
- `OOS` = out of current repo turnkey scope

| Method | Setting / Source | Lift Paper | Lift Repro | Can Paper | Can Repro | Square Paper | Square Repro | Tool-Hang Paper | Tool-Hang Repro | Transport Paper | Transport Repro | Push-T Paper | Push-T Repro | ALOHA / Cube Paper | ALOHA / Cube Repro | Long Square Paper | Long Square Repro | Source-specific Avg. Paper | Source-specific Avg. Repro | Notes |
|---|---|---:|---|---:|---|---:|---|---:|---|---:|---|---:|---|---:|---|---:|---|---:|---|---|
| DP | PTP internal baseline: Diffusion (no-hist) | N/A | OOS | N/A | OOS | 0.79 ± 0.06 |  | 0.51 ± 0.14 |  | 0.60 ± 0.08 |  | 0.67 ± 0.03 |  | 0.28 ± 0.04 |  | 0.12 ± 0.05 |  | 0.50 |  | Fill from matched no-history / long-context baseline runs where supported. |
| LDP | LDP + Action-Free + Subopt | 1.00 ± 0.00 | OOS | 0.98 ± 0.00 | OOS | 0.83 ± 0.01 | OOS | N/A | OOS | N/A | OOS | N/A | OOS | 0.97 ± 0.01 | OOS | N/A | OOS | 0.95 | OOS | This row is not directly turnkey from the current public PTP repo snapshot. |
| PTP | Diffusion (PTP) | N/A | OOS | N/A | OOS | 0.89 ± 0.01 |  | 0.75 ± 0.10 |  | 0.67 ± 0.08 |  | 0.62 ± 0.02 |  | 0.98 ± 0.01 |  | 0.93 ± 0.02 |  | 0.81 |  | Main reproduction target row for this repo. |

## Immediate Fill Targets

- `Square`:
  - We already have partial early evidence for matched `obs16` comparison:
    - `no-PTP`: `0.05` at an early checkpoint
    - `PTP`: `0.2` at an early checkpoint
  - These are not paper-equivalent final numbers yet, so they should stay in working notes until a decision is made to surface early results in the table.
- `Tool-Hang`, `Transport`, `Push-T`, `ALOHA / Cube`, `Long Square`:
  - leave blank until the corresponding public datasets are fully staged and runs complete.
- `Lift`, `Can`, `LDP row`:
  - keep marked `OOS` unless we explicitly extend scope.

## Suggested Review Order

1. Check that the task boundary above matches what you want counted as in-scope.
2. Decide whether `Lift` / `Can` should stay `OOS` or whether we should author extra configs.
3. Decide whether to keep the table strictly blank until converged runs finish, or to add a separate "early current value" scratch table below it.
