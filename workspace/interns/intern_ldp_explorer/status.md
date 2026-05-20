# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 38 |
| Recent Progress | Checked rollout status. Direction C BehaviorTranslator / Stage2a currently has no rollout eval output because Stage1 and Stage2a are offline representation/action-head probes, not rollout-capable policies. Existing py39 / robomimic 0.2.0 rollout results are only from the earlier Flow Matching baseline: Square h10 `7/10`, Square action8 `4/10`, ToolHang h10 `0/10`, ToolHang action8 `0/10`. Stage2a offline probe results are available: `past_e50` best val loss `0.007839` / future L1 `0.04917`, better than random frozen best val loss `0.011571` / future L1 `0.06736`. |
