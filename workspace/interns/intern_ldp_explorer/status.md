# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 45 |
| Recent Progress | Continued Direction C Stage2b rollout and training. Old-node add-all downstream jobs are still alive on `10.100.2.35:25076`: pretrained context reached about epoch `284`, random context about epoch `281`, with checkpoints through e199/e149 respectively. New-node ablations on `10.100.4.35:19382` remain active for pretrained add-last, random add-last, and pretrained nonzero-projector; the original base no-context process exited before its first checkpoint, so a clean base rerun was started on GPU0 at `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage2b_square_ablation_20260523_0110_base_rerun/stage2b_base_no_context_action8_rerun`, pid `4086173`. Added rollout evidence: add-all e99 gives pretrained `4/10` vs random `3/10`; nonzero-projector pretrained e99 gives `4/10`; add-last e49 gives pretrained `4/10` vs random `0/10`. Current evidence is mixed: add-last is favorable to translator context, while add-all still needs base/no-context and repeated seeds before claiming a reliable gain. |
