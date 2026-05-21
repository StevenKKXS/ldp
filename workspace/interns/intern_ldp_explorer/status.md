# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 43 |
| Recent Progress | Continued Direction C execution. Rechecked Stage1 and Stage2a status, confirmed tuned Stage1 `past` and `past_future` completed 200 epochs while formal `past` / `past_future` remain alive on old-node GPU0/GPU2. Tuned Stage2a probes on the new node are still running around epoch 26; latest epoch-25 offline probes still favor `past` context over `past_future` for frozen-head future-action prediction. Filled old-node idle GPU1/GPU3 with Stage2b Square action8 downstream training under `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage2b_square_translator_context_20260521_1252`: pretrained tuned-`past` context pid `4026333` on GPU1 and same-architecture random context pid `4026336` on GPU3. Both Stage2b jobs loaded cache and entered epoch 0 training with nonzero GPU utilization. |
