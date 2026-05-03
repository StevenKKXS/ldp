# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 9 |
| Recent Progress | Reframed the reproduction work against the paper's actual method stack and baselines. The current live node remains `10.100.2.47:15744`, and the latest sample shows `GPU0 0%, 4 MiB` and `GPU1 99%, 27875 MiB`, with only `node96_no_ptp_square_obs16_1777613676` and `node96_nohist_square_short_1777613676` still active. The cleanest completed result in hand remains the older matched `obs16` comparison where long-context `PTP` reached `test/mean_score=0.2` while long-context `no-PTP` reached `0.05`, which is the main evidence currently supporting the paper's claim in our square reproduction. |
