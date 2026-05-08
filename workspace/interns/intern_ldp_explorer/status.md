# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 98 |
| Recent Progress | Checked DP and PTP queues under stamp `1778075154` on `2026-05-08T02:35:39Z`. PTP remains on `10.100.0.29:30103`: 7 runs active, LongSquare PTP `a8` completed at epoch `1999`, all sampled logs have no traceback; Square PTP `a8` best checkpoint score is `0.45`, Square PTP `a1` best is `0.28`, all Tool-Hang/Transport/LongSquare PTP sampled checkpoint scores remain `0.0`. DP resume remains on `10.100.0.29:36645`: 7 runs active, LongSquare DP `a8` completed at epoch `1999`, all sampled logs have no traceback; Square DP `a8` has exceeded the intended 2000-epoch target and is still running around epoch `2259`, so it should be handled as an over-target resume anomaly. |
