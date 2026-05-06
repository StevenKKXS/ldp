# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 79 |
| Recent Progress | Ran quick expert-action replay diagnostics on the H200 node. Square sanity replay passed 3/3 and Transport passed 5/5 under states-only runner-like reset plus abs-action rotation roundtrip. Tool-Hang failed the same check: `image_abs.hdf5` replay passed only 1/8, original delta `image.hdf5` replay passed 0/8, and `hard_reset=False` still passed only 1/5. Final-state reset checks showed Tool-Hang terminal states are recognized as successful 8/8, so the issue is action rollout / reset fidelity rather than reward predicate alone. Dataset `model_file` exists but reset with model XML fails under current robosuite with missing `robot0_g0_vis`, and the current env runner only uses `states[0]` anyway. |
