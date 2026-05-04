# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 28 |
| Recent Progress | Reallocated the GPUs toward higher-value table columns and then packed GPU1 further. GPU0 remains occupied by the `Tool-Hang long-hist DP/PTP` pair, each using about `60 GiB`. GPU1 was taken away from the older `Square` reruns and now carries a `Long Square long-hist DP/PTP` pair plus a newly launched `Transport long-hist DP/PTP` pair. The `Long Square` pair has already allocated about `9.4 GiB` each on GPU1, while the `Transport` pair is still in raw-image preload from `transport/mh/image_abs.hdf5`, so GPU1 should rise further once those two finish loading. Session 28 presence note: `history_log.md` explicitly includes the literal `## Session 28` section plus the final per-GPU assignment. |
