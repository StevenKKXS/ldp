# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 92 |
| Recent Progress | Checked effective stamp `1778075154` on `2026-05-07T07:44Z`. The vector-env fixes are now sufficient for rollout/checkpoint: active runs have crossed epoch 100 and are writing ckpts and MP4s. LongSquare DP `a8` completed epoch `1999` cleanly and its PTP `a8` lane is running at epoch `384`. Other active DP lanes: Square `a8` epoch `1599`, Square `a1` epoch `682`, Tool-Hang `a8` epoch `1293`, Tool-Hang `a1` epoch `426`, Transport `a8` epoch `511`, Transport `a1` epoch `252`, LongSquare `a1` epoch `799`; no current traceback markers. Latest rollout scores are mostly `0.0`, with Square DP `a8` latest score `0.02`; these are intermediate training rollouts, not final evaluation. |
