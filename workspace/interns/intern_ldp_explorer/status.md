# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 13 |
| Recent Progress | Clarified what `long hist square` actually means in the paper and in code, and added an explicit Session 13 close-out check after the stop-hook. It is not just the standard RoboMimic `square` task with a larger observation window; in the paper it is a new long-horizon square task where the robot must place and remove the square twice before the final drop, making success genuinely history-dependent. In the repo this is implemented through a separate `longhist` config family with its own dataset path `data/longhistsquare100/demos.hdf5`, task name `square_long_image`, and long-history runner wiring, rather than by a simple flag on the regular `square` task. |
