# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 36 |
| Recent Progress | Implemented and launched Direction C Stage 2a Square frozen-head probe. Added `TrainTranslatorHeadWorkspace` and `experiment_configs/square/translator_head_square.yaml`; smoke passed for random frozen and `past_e50`. First formal batch is running on new 4xH200 node `10.100.4.35:19382`: `stage2a_random_frozen`, `stage2a_past_e50`, `stage2a_past_future_e50`, and `stage2a_future_best`, each with `batch=128,num_workers=16,num_epochs=50`. Stage 2a only reports offline validation metrics such as future action loss/L1/MSE and gripper accuracy; environment success rate requires later DP/PTP integration plus rollout. |
