# Simulation Repro Tasklist And Result Table

## Purpose

This is the working artifact for the simulation-side reproduction effort.

This version uses a task-column layout:

- columns are tasks
- rows are paper baselines / paper method / repro rows

This makes it easier to compare one method across all tasks at a glance.

## Why This Layout

The user requested a horizontal table with task-only columns and extra blank repro rows.

This is a good change.

It is also useful to separate three concepts clearly:

- `short-hist DP` = the no-history / default short-context diffusion baseline
- `long-hist DP` = the long-context baseline without PTP (`no-PTP`)
- `long-hist PTP` = the paper's main method

The current paper-number excerpt we are using already gives a short-hist DP row and a PTP row.
The paper / project description also clearly discusses a long-context baseline, so this artifact now reserves a row for it even when the exact paper-number cells are not all copied into the current excerpt.

## In-Scope Simulation Targets

- `Square`
- `Tool-Hang`
- `Transport`
- `Push-T`
- `ALOHA / Cube`
- `Long Square`

Removed from this working artifact:

- `Lift`
- `Can`
- `LDP` row

Reason:

- `Lift` / `Can` are not turnkey in this repo snapshot
- `LDP` is a different project line and should not stay mixed into this PTP tracking sheet

## Execution Task List

### P0: Data Completion

- Confirm `robomimic_image.zip` completed and exposed:
  - `tool_hang`
  - `transport`
- Confirm `pusht` extracted to `data/pusht/pusht_cchi_v7_replay.zarr`
- Confirm `aloha_twomodes_single/demos.hdf5`
- Confirm `longhistsquare100/demos.hdf5`

### P1: Main Reproduction Rows

- `short-hist DP`
  - run / record aligned no-history baselines
- `long-hist DP`
  - run / record aligned no-PTP baselines
- `long-hist PTP`
  - run / record aligned PTP rows

### P2: Fill Supporting Ablations

- `no-history` vs `no-PTP` vs `PTP`
- `obs=2` vs `obs=16`
- raw-image vs cached-embedding
- early checkpoint vs later checkpoint trend
- pilot seed vs repeated-seed confirmation

### P3: Metadata Capture

For every filled repro row, record:

- config name
- dataset path
- checkpoint path
- seed count
- metric source
- whether the result is pilot / early / converged

## Main Result Table

Legend:

- `Paper` rows preserve the paper-side target numbers we currently have
- `Repro` rows are for our reproduced values
- `—` means the current paper-number excerpt does not provide that cell
- blank cells are intentionally left for filling

| Row | Square | Tool-Hang | Transport | Push-T | ALOHA / Cube | Long Square | Avg. | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Paper short-hist DP (`no-history`) | 0.79 ± 0.06 | 0.51 ± 0.14 | 0.60 ± 0.08 | 0.67 ± 0.03 | 0.28 ± 0.04 | 0.12 ± 0.05 | 0.50 | This is the default short-context diffusion baseline row from the current excerpt. |
| Repro short-hist DP |  |  |  |  |  |  |  | Fill with our matched no-history results. |
| Repro short-hist DP (repeat / aggregate) |  |  |  |  |  |  |  | Use for second seed or aggregate value. |
| Paper long-hist DP (`no-PTP`) |  |  |  |  |  |  |  | Reserve this row because the paper uses a long-context baseline, even though the current excerpt does not provide the full row values. |
| Repro long-hist DP |  |  |  |  |  |  |  | Fill with our matched long-context no-PTP results. |
| Repro long-hist DP (repeat / aggregate) |  |  |  |  |  |  |  | Use for second seed or aggregate value. |
| Paper long-hist PTP | 0.89 ± 0.01 | 0.75 ± 0.10 | 0.67 ± 0.08 | 0.62 ± 0.02 | 0.98 ± 0.01 | 0.93 ± 0.02 | 0.81 | Main paper method row from the current excerpt. |
| Repro long-hist PTP |  |  |  |  |  |  |  | Fill with our aligned PTP results. |
| Repro long-hist PTP (repeat / aggregate) |  |  |  |  |  |  |  | Use for second seed or aggregate value. |

## Ablation Table

| Task | Comparison | Expected Direction | Current Repro | Status | Notes |
|---|---|---|---|---|---|
| Square | short-hist DP vs long-hist DP vs long-hist PTP | `PTP` should beat matched long-hist DP; long-hist DP should be compared against short-hist DP | `no-PTP=0.05`, `PTP=0.2` at early checkpoint | pilot | Early only, not final |
| Square | `obs=2` vs `obs=16` | longer context should help if the policy actually uses it |  | open | Fill after matched reruns |
| Square | raw vs cached embeddings | cached should preserve performance and improve speed |  | open | Fill after cached training run |
| Tool-Hang | short-hist DP vs long-hist DP vs long-hist PTP | `PTP` should improve long-context performance |  | blocked on data / run |  |
| Transport | short-hist DP vs long-hist DP vs long-hist PTP | `PTP` should improve long-context performance |  | blocked on data / run |  |
| Push-T | short-hist DP vs long-hist DP vs long-hist PTP | useful supporting ablation, exact gain unclear |  | blocked on data / run |  |
| ALOHA / Cube | short-hist DP vs long-hist DP vs long-hist PTP | large gain expected from paper row |  | blocked on data / run |  |
| Long Square | short-hist DP vs long-hist DP vs long-hist PTP | strong gain expected from paper row |  | blocked on data / run |  |

## Immediate Fill Targets

- Fill `Repro short-hist DP` for `Square` from the already-run short-context baseline lineage.
- Fill `Repro long-hist DP` and `Repro long-hist PTP` for `Square` once the aligned comparison row is finalized.
- Fill `Tool-Hang` and `Transport` next after RoboMimic backfill finishes.
- Fill `Long Square` and `ALOHA / Cube` after their dedicated datasets are confirmed ready.

## Interpretation Notes

- Yes, the core paper comparison is fundamentally `long-hist DP` vs `long-hist PTP`.
- But keeping `short-hist DP` in the table is still reasonable and useful, because it anchors what "default DP ability" looks like before long context is introduced.
- So the best working layout is not two rows but three:
  - `short-hist DP`
  - `long-hist DP`
  - `long-hist PTP`
