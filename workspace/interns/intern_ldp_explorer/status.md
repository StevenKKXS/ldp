# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 70 |
| Recent Progress | Recorded that encoder/data inconsistencies remain in history and shifted current priority to Tool-Hang / Transport zero-success diagnosis. Evidence: Square PTP has nonzero rollout scores from epoch 99 onward and final selected-checkpoint eval reaches `0.36`, while Tool-Hang and Transport DP/PTP checkpoints are `0.000` at every saved epoch and their Session 65 100-episode evals are also `0.0`. Tool-Hang and Transport also have `train/mean_score=0.0` across training rollouts, so this is not only a test-seed generalization problem. Config comparison shows the main Fig. 9 settings match (`global_obs=16`, `global_horizon=32`, `global_action=8`, `batch_size=64`, frozen official encoder, cached embeddings consistent); strongest current hypotheses are task difficulty, sparse rewards, insufficient 500-epoch recipe for these harder tasks, and possible task-specific runner/action validation issues. |
