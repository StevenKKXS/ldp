# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 103 |
| Recent Progress | Checked main experiment progress under stamp `1778075154` at `2026-05-08T12:10:06Z`. PTP queue on `30103` remains healthy: Square `a8` and LongSquare `a8` are complete at epoch `1999`; Square `a1`, Tool-Hang `a8/a1`, Transport `a8/a1`, and LongSquare `a1` are still running with no traceback. Best nonzero training-rollout scores remain Square PTP `a8=0.45`, Square PTP `a1=0.28`, Transport PTP `a8=0.01`. DP queue on `36645` is also running without traceback, but Square DP `a8` reached epoch `2699` and Tool-Hang DP `a8` reached epoch `2499`, both clearly beyond the intended 2000-epoch target. |
