# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 29 |
| Recent Progress | Analyzed why `Tool-Hang long-hist` uses much more GPU memory than `Long Square` and `Transport`, then checked the paper's motivation for multistage training. The main reason for the current memory gap is task geometry, not an accidental batch-size mismatch; and in the paper, the two-step recipe is described more as a compute-efficiency method that avoids repeatedly processing visual inputs and keeps long-context training practical, not as a pure VRAM workaround. Session 29 presence note: `history_log.md` explicitly includes the literal `## Session 29` section plus the memory-gap, batch-size, paper-grounded multistage-training interpretation, and the `/model gpt-5.5` control note. |
