# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 12 |
| Recent Progress | Reframed the work in terms of distance to the paper's actual result. The strongest completed evidence in hand is still the older matched `obs16` square comparison where `PTP` reached `test/mean_score=0.2` and `no-PTP` reached `0.05`, which supports the paper's direction but is still far from a faithful full-paper reproduction. The main remaining gaps are now explicit: we still do not have `longhistsquare100`, we have not yet run the complete multistage cached-embedding recipe on the intended long-history task, and we have not exercised the paper's test-time verification stage. |
