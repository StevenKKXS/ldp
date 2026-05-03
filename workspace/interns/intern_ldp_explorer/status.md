# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 8 |
| Recent Progress | Re-sampled all known server endpoints on `2026-05-03` and confirmed the old 72h node entry `10.100.2.47:37893` is no longer reachable, while the 96h node `10.100.2.47:15744` remains live as host `lg-cmc-b7r201-e06u16-h200-000110`. Current GPU snapshot there is `GPU0 0%, 4 MiB` and `GPU1 57%, 27875 MiB`, so the box is not saturated. From current `ps` and `logs.json.txt`, only `node96_no_ptp_square_obs16_1777613676` and `node96_nohist_square_short_1777613676` are still active; the earlier `node96_ptp_*` jobs left output directories and metrics but do not appear active anymore. |
