# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 72 |
| Recent Progress | Clarified Square reproduction level. Training-time Square PTP rollout scores over `n_test=40` were epoch 99 `0.475` (19/40, best), epoch 199 `0.400`, epoch 299 `0.250`, epoch 399 `0.400`, and epoch 499 `0.425`. The selected best checkpoint `epoch=0099-test_mean_score=0.475.ckpt` scored `0.36` on the separate Session 65 100-episode eval (`36/100`, `n_samples=1`). Square no-PTP/DP rollout scores were `0.000` through epoch 399 and `0.025` at epoch 499, then `0.00` on the 100-episode eval. Compared with paper Square PTP `0.89±0.01`, current best training rollout is about `53%` of paper and current 100-episode eval is about `40%` of paper. |
