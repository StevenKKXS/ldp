# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 85 |
| Recent Progress | Produced task-specific recommendations for getting Tool-Hang and Transport off zero success. The recommendation split is now explicit: Tool-Hang should not be retrained first; it should first get a stable expert-replay path using the absolute-action dataset and environment settings that actually reproduce demos. Transport has the opposite profile: expert replay passes, so the next moves should focus on longer fresh-schedule training, denser checkpointing, saved rollout videos, and EMA/non-EMA or multi-sample diagnostics rather than environment surgery. |
