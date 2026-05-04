# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 29 |
| Recent Progress | Rechecked the live remote jobs and classified them against the Figure 9 protocol. The active jobs are raw-image long-history DP/PTP pilots for `Tool-Hang`, `Transport`, and resumed `Long Square`; they match the algorithmic `past_action_pred=false/true` comparison, but they are not Figure 9-aligned multistage cached-embedding runs. `Long Square` had crashed at epoch 9 due a `test_mean_score` checkpoint-monitor mismatch, and was resumed from `latest.ckpt` with `training.checkpoint_every=50` to match `rollout_every=50`. |
