# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 39 |
| Recent Progress | Rechecked running results on 2026-05-05 UTC. New node `10.100.2.47:28447` is still running four Square cached jobs around epoch 1329-1335 with low rollout scores so far; old node `:15744` is still running Long Square DP/PTP around epoch 2140-2149 with test score still 0.0. Tool-Hang/Transport jobs stopped at epoch 49 during first rollout due AsyncVectorEnv EOFError plus NVIDIA Xid 31/109, leaving no checkpoint. |
