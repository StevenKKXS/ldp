# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 14 |
| Recent Progress | Clarified what `square` means in this project and added an explicit Session 14 validator note after the stop-hook. In `ldp`, `square` refers to the standard RoboMimic `square` benchmark task and dataset path `data/robomimic/datasets/square/mh/image_abs.hdf5`, not a generic shape label. At the simulator level this task comes from robosuite's `NutAssemblySquare`, i.e. placing a square nut onto its peg. This also sharpens the distinction with the paper's separate `longhist square` / `long-horizon square` task family. |
