# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 73 |
| Recent Progress | Rechecked Direction C progress on `2026-05-30`. All known GPU endpoints now refuse SSH, including the previously active `10.100.2.19:28106`, so no e99 rollout can be launched until a GPU node is available. Ceph logs show Stage2b continued until about `2026-05-30 02:55 UTC`: M1 last epoch `213`, M3 `217`, M2 `188`, M4 `189`. Offline best points remain early: M1 `0.03769 @ e57`, M3 `0.04459 @ e52`, M2 `0.03330 @ e64`, M4 `0.03011 @ e62`; latest/e99+ losses are worse, so longer training looks overfit by offline validation. No new rollout JSON exists beyond the previous e24/e49 table. Stage1 Ceph `past` reached last epoch `178`; best remains obs lr `1e-4` at `0.000485 @ e110` and obs lr `5e-5` at `0.000524 @ e129`. User requested final migration from Ceph to 3FS1; target root `/mnt/3fs1/data/tingwen.du/intern_ldp_explorer/direction_c_behavior_translator` was created. |
