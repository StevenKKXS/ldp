# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 17 |
| Recent Progress | Confirmed PTP dataloader observation format: normal image configs return raw image/proprio tensors, and the policy obs_encoder encodes them during forward; only embedding-cache configs with use_embed_if_present=true and an embedding key return precomputed embeddings. |
