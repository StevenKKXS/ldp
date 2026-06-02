# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 81 |
| Recent Progress | Recomputed parameter counts on the Ceph py39 / `robomimic==0.2.0` runtime. Default d256 translator is `5.776M` core / `28.170M` with robomimic obs encoder. ACT-size translator is `56.177M` core / `78.571M` with obs encoder, almost the same size as the deterministic ACT-style baseline (`55.116M` core / `77.510M` full). The official-ACT-compatible CVAE adapter is larger: `72.513M` core / `94.907M` full. |
