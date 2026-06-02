# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 78 |
| Recent Progress | Checked official-ACT Square action8 25-epoch run on `10.100.2.39:23494`. The run finished normally, saved `epoch=0024-val_loss=0.046737.ckpt`, and rollout over 20 test seeds produced `test/mean_score=0.05` (`1/20`, only seed `100009` succeeded). This improves over the 5-epoch `0/20` smoke but remains far below the Square DP/PTP baselines; treat current official-ACT-compatible adaptation as a weak baseline, not a solved ACT result. |
