# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 40 |
| Recent Progress | Filled the idle GPUs. Old node `10.100.2.35:25076` now uses all 4 H200s: existing formal Stage1 `past` on GPU0 and `past_future` on GPU2, plus new tuned Stage1 jobs on GPU1/GPU3 under `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage1_square_tuned_fill_20260520_1536`. New node `10.100.4.35:19382` now uses all 4 H200s for Stage2a next-stage probes under `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage2a_square_next_20260520_1536`: `past_best_frozen`, `past_latest_frozen`, `past_best_finetune_tr1e5`, and `past_future_best_frozen`. Startup logs show jobs entered training/cache-load without immediate errors. |
