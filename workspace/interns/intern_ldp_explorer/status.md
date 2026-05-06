# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 82 |
| Recent Progress | Reorganized the four Tool-Hang replay experiments into a clearer natural-language explanation. The key framing is: these are replay diagnostics rather than training runs, and they vary only a small set of parameters around the same stored Tool-Hang demos. The main explanatory split is between `image_abs` versus original `image` actions, `use_object_obs` false versus true, and default reset behavior versus `hard_reset=False`, with all cases keeping states-only reset and video-enabled environment construction. |
