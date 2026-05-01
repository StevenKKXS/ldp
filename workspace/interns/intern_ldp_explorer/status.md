# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 5 |
| Recent Progress | Verified that `num_epochs=3500` is explicitly set in the upstream square and longhist configs, then traced why the `obs16` run looks so slow: each epoch is already about 1141 optimizer steps, validation runs every epoch, rollout uses 28 envs and 40 test episodes, and the current long-context run is still on raw images without embedding caching, so the earlier ~950h estimate reflects a genuinely heavy recipe rather than a single obvious reproduction bug. |
