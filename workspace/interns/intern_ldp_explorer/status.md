# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 73 |
| Recent Progress | Rechecked Direction C progress on `2026-05-29`. The active GPU node is now `10.100.2.19:28106`; `10.100.0.62:24345` refuses SSH. Six training jobs are still alive on the 4xH200 node: Stage2b M1/M2 share GPU0, M3/M4 share GPU1, and two Stage1 `past` translator runs use GPUs2/3. All four corrected Stage2b Square runs have passed e99 and saved e99 checkpoints, but no e99 rollout eval has been run yet; only the previous e24/e49 rollout table exists. Offline validation now suggests overfitting after roughly e50-e65: M1 best `0.03769 @ e57`, M3 best `0.04459 @ e52`, M2 best `0.03330 @ e64`, M4 best `0.03011 @ e62`; e99 losses are worse than those best values. Stage1 Ceph `past` also improved: obs lr `1e-4` best `0.000485 @ e110`, obs lr `5e-5` best `0.000524 @ e129`. |
