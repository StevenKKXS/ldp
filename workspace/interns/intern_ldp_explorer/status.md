# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 77 |
| Recent Progress | Completed read-only official ACT repository audit at commit 742c753. Confirmed official ACT uses DETR-style ResNet18 visual backbone, action-query decoder, and CVAE posterior over qpos plus action chunks with latent_dim=32 and KL loss; local `ActionChunkingTransformerHybridImagePolicy` is deterministic ACT-style only, omits CVAE/KL/is_pad/temporal ensembling, and uses the robomimic obs encoder plus long observation history. Prepared minimal Robomimic Square/ToolHang image_abs adaptation plan and risks. |
