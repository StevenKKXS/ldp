# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 7 |
| Recent Progress | Re-sampled the 96h node and confirmed all four `node96_*` jobs have moved beyond preload into real training: the short-history PTP and no-history runs are already at epochs `20/21`, the `obs16` PTP and no-PTP runs are at epoch `3`, and the latest `nvidia-smi` snapshot at `2026-05-01 06:42 UTC` showed low instantaneous utilization (`GPU0 0%`, `GPU1 17%`) despite roughly `27.9 GiB` resident on each card, which means the jobs are alive but still not saturating the H200s. |
