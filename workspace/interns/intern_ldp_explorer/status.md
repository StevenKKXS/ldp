# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 61 |
| Recent Progress | Collected a fresh run-status snapshot at `2026-05-05 13:09 UTC`. All 8 seed-42 Wave A/B training parent PIDs are alive and active logs show zero matches for `Error executing job`, `Traceback`, `EOFError`, `RuntimeError`, or OOM. Wave A on `10.100.0.29:30103`: Square DP epoch `213`, best checkpoint score `0.000`; Square PTP epoch `219`, best checkpoint score `0.475`; Tool-Hang DP epoch `149`, best checkpoint score `0.000`; Tool-Hang PTP epoch `155`, best checkpoint score `0.000`. Wave B on `10.100.0.29:36645`: Transport DP epoch `64`, Transport PTP epoch `67`, both before first checkpoint; LongSquare DP epoch `199`, best checkpoint score `0.000`; LongSquare PTP epoch `199`, best checkpoint score `0.000`. These are training-time `n_test=40` checkpoint scores, not final paper-style evaluation results. |
