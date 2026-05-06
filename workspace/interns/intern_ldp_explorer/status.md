# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 80 |
| Recent Progress | Reframed the Tool-Hang replay diagnosis into a clearer explanation for the user. The key message is: the sanity controls are healthy (`Square 3/3`, `Transport 5/5`), Tool-Hang replay from stored initial state with stored actions is not healthy (`image_abs 1/8`, original delta `0/8`, `hard_reset=False` still only `1/5`), while Tool-Hang final states are healthy (`8/8` recognized as success). This isolates the problem to rollout fidelity from initial state rather than cached embeddings or the success predicate itself. |
