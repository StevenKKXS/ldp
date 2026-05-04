# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 29 |
| Recent Progress | Analyzed why `Tool-Hang long-hist` uses much more GPU memory than `Long Square` and `Transport`. The main reason is task geometry, not an accidental batch-size mismatch: `Tool-Hang` uses two `240x240` cameras with crop `216x216` and `global_action=8`, while `Long Square` uses two `84x84` cameras and `global_action=1`, and `Transport` uses four `84x84` cameras with `global_action=1`. After `Transport` finished preload and entered training, GPU1 rose to about `73.8 GiB`, confirming that the earlier low number was largely a preload artifact rather than proof that the task was intrinsically tiny. Session 29 presence note: `history_log.md` explicitly includes the literal `## Session 29` section plus the memory-gap and batch-size analysis. |
