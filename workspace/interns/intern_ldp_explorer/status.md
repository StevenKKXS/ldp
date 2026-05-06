# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 87 |
| Recent Progress | Clarified the current meaning of “default replay” for Tool-Hang. The default `RobomimicImageRunner` path uses `image_abs.hdf5`, forces `control_delta=false` when `abs_action=true`, disables object observations, sets `hard_reset=false`, enables image observations / offscreen rendering, and resets from stored `states[0]` only. Under replay diagnostics, Tool-Hang is not a clean `0` on expert replay: the broader states-only sweep gave `1/8`, while the image-enabled runner-like video case succeeded on `2/2` selected demos. The all-zero numbers belong to policy rollout success, not to a single stable expert-replay baseline. |
