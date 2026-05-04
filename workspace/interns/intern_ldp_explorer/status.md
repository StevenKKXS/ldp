# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 38 |
| Recent Progress | Configured the new node at `10.100.2.47:28447`; it exposes 2 H200 GPUs despite the 4-card request. Launched Square cached DP/PTP seed42 on GPU0 and Square cached DP/PTP seed43 on GPU1; ALOHA is left blank because its runner requires a MuJoCo/dm-control version change. A 2h old-node monitor is active and will trigger a read-only follow-up check when tracked old jobs go offline. |
