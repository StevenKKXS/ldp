# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 73 |
| Recent Progress | Estimated current corrected Stage2b Square ETA to the 100-epoch checkpoint (`epoch=0099`, because checkpoint names are zero-indexed). Current logs are actively updating. Observed safe-worker speed is about `26` minutes per epoch including validation/checkpoint overhead. M1 base is around e67 and M3 random around e68, so their e99 checkpoints should land in about `14` hours, around `2026-05-27 23:05-23:15 UTC`. M2 pretrained add-last is around e40 and M4 pretrained add-all around e41, so their e99 checkpoints should land in about `25.5-26` hours, around `2026-05-28 10:50 UTC`. From scratch, e100 for one current Stage2b run is roughly `43-44` hours before rollout evaluation. |
