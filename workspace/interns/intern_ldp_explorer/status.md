# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 73 |
| Recent Progress | Summarized loss curves for the current 4x2 diffusion subset and provided command-line inspection commands. All 8 runs show train loss decreasing, so raw optimization did happen. Square PTP: train loss `0.0120 -> 0.0066`, val loss worsens `0.0422 -> 0.0584`, best score at epoch 99 `0.475`, suggesting later overfit rather than undertraining. Tool-Hang PTP: train `0.0182 -> 0.0104`, val improves to epoch 349 (`0.0151`) but score remains `0`; loss alone does not explain task success. Transport PTP: train `0.0100 -> 0.0039`, val worsens after epoch 199 (`0.0209 -> 0.0322`), score remains `0`, indicating overfit/task difficulty or runner/action issues more than simple undertraining. LongSquare loss improves strongly but is confounded by known embedding inconsistency. |
