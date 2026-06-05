# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 100 |
| Recent Progress | Stopped the overly aggressive Square stability rollout batch on `10.100.2.39:23494` and relaunched the 3-settings x 3-seeds x 100-episode evaluation with `n_envs=8` and at most 4 concurrent eval processes, capping active simulator envs at 32 under Ceph output root `stage2b_square_rollout_stability_nenv8_max4_20260605`. |
