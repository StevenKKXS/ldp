# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 68 |
| Recent Progress | Answered the compact-HDF5 empty-image question: Tool-Hang and Transport do not need retraining merely because their compact embedding HDF5 omits or empties raw image arrays, because cached training consumes `obs/embedding` and eval/rollout should use environment-rendered raw images plus the frozen encoder. Their Session 67 embedding checks match online raw-image encoding, so zero success is more likely due checkpoint quality, training length, sparse reward, or eval/task settings than empty compact-image arrays. Recorded the next execution target: check embedding consistency for all six tasks (`Push-T`, `Square`, `Tool-Hang`, `Transport`, `ALOHA/Cube`, `LongSquare`), identify datasets requiring regeneration, create regenerated HDF5 files with new names in the same directories without overwriting originals, and update configs to point at the validated files. |
