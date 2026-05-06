# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 76 |
| Recent Progress | Consolidated the parameter-design history into two layers so later analysis does not mix exploratory runs with the main paper-aligned reproduction line. Recorded that the final 4x2 diffusion subset switched to `global_obs=16`, `global_horizon=32`, `global_action=8`, `num_epochs=500`, `batch_size=64`, explicit `past_steps_reg=-1`, DP/PTP split via `past_action_pred`, and cached-embedding training with a frozen official short-context encoder, while older exploratory runs included short-context `global_obs=2`, `global_action=1`, `num_epochs=3500`, raw-image pilots, and different checkpoint / rollout cadences. |
