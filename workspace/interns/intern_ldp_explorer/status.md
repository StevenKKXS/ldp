# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 86 |
| Recent Progress | Traced how `control_delta=false` is set for the robomimic tasks. The main finding is that Square, Tool-Hang, Transport, and LongSquare do not each carry a separate task-specific control-delta rule in the runner; instead, the runners uniformly override `env_meta['env_kwargs']['controller_configs']['control_delta'] = False` whenever `abs_action=true`. The HDF5 files themselves still report `control_delta=true` even for `image_abs.hdf5`, so the absolute-control switch is primarily a runtime override rather than a property stored back into dataset metadata. |
