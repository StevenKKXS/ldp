# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 41 |
| Recent Progress | Checked progress on 2026-05-21. Old node `10.100.2.35:25076` still has all 4 H200s occupied by Stage1 runs. Formal `past` reached epoch `141` with best val loss `0.000455 @ e113`; formal `past_future` reached epoch `142` with latest val loss `0.01856`. Tuned `past` reached epoch `169` with best val loss `0.000434 @ e118`; tuned `past_future` with `w_future=0.5` reached epoch `168` with best val loss `0.006501 @ e4` and latest future L1 `0.04472`. The previous Stage2a next batch on `10.100.4.35:19382` completed all four 50-epoch probes: `past_best_frozen` best `0.007966`, `past_latest_frozen` best `0.008028`, `past_best_finetune_tr1e5` best `0.008056`, and `past_future_best_frozen` best `0.010617`, so frozen `past` remains the strongest Stage2a signal. The new node was refilled with tuned-checkpoint Stage2a probes under `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage2a_square_tuned_20260521_0833`. |
