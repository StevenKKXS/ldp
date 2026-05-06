# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 88 |
| Recent Progress | Verified the actual data and action semantics used by the current 4x2 repro runs. Square, Tool-Hang, and Transport train on derived `image_abs_*emb*.hdf5` files and roll out against raw `image_abs.hdf5`; LongSquare currently trains and rolls out from `demos.hdf5` with `abs_action=true`. In other words, the active robomimic/longhist reproduction line is on the absolute-action path for both training semantics and rollout semantics, while the earlier delta replay cases were only diagnostics. |
