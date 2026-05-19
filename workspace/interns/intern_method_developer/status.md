# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 11 |
| Recent Progress | Polled exact-PTP downstream encoder ablations on `10.100.2.4:35140`: all 16 jobs are still running across 8 H200 GPUs. Main Square is around epoch 38-39 and main ToolHang around epoch 15-16. |
| Handoff | Latest train/val diffusion losses remain non-rollout signals. Main Square latest vals: original `0.0735`, `B_full_frozen` `0.0702`, `B_full_finetune` `0.0739`, `A_future_finetune` `0.0758`. Main ToolHang latest vals: original `0.1001`, `B_full_frozen` `0.0943`, `B_full_finetune` `0.1002`, `A_future_finetune` `0.1004`. |
