# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 34 |
| Recent Progress | Generated GPU3 utilization and memory curves for the Direction C Stage 1 Square `past` `batch_size=128,num_workers=64` benchmark. The curve shows bursty GPU use: all-sample average utilization 14.84%, max 99%, nonzero-util samples 32.6%, and average utilization 45.48% only when nonzero. Bottleneck is mainly input pipeline / startup / DataLoader IPC scheduling rather than H200 memory or raw GPU compute. |
