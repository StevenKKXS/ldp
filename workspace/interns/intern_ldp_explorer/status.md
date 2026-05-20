# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 36 |
| Recent Progress | Shifted priority to Direction C Stage 1 `past` LR tuning while preserving old Stage 1 checkpoints. On new 4xH200 node `10.100.4.35:19382`, kept the minimal Stage 2a gate jobs `stage2a_random_frozen` and `stage2a_past_e50`, stopped the lower-priority Stage 2a `past_future_e50` and `future_best` jobs to free GPUs, and launched two 8-epoch `past` sweeps using the fast `batch=128` setup: `stage1_past_bs128_lr1e4` and `stage1_past_bs128_obs5e5_tr1e4`. A watchdog monitors both runs after epoch 5 and terminates them if validation loss becomes abnormal. |
