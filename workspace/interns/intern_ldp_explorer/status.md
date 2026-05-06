# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 74 |
| Recent Progress | Continued the loss-curve answer with concrete command-line recipes. Provided copy-paste Python JSONL commands to inspect checkpoint-level rows in the 8 `logs.json.txt` files and optional one-run commands for Square PTP. Main conclusion remains: all 8 runs reduce train loss, so the optimizer learned the supervised objective, but success does not track loss. Square PTP peaks at epoch 99 where val loss is best; Transport shows train loss falling while val loss rises and success stays 0; Tool-Hang val loss improves but sparse task success remains 0. This supports expert-action replay and behavior-video diagnostics before spending on longer reruns. |
