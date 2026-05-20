# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 39 |
| Recent Progress | Checked current GPU utilization. Old formal node `10.100.2.35:25076` has two active Stage 1 jobs: `past` on GPU0 pid `1086376` using about `5.5GB` and `past_future` on GPU2 pid `26885` using about `5.4GB`; GPU1 and GPU3 are idle. A 5-sample check showed intermittent compute, with four samples at `0%` util and the final sample at GPU0 `77%` / GPU2 `85%`, consistent with input-pipeline waiting. New 4xH200 node `10.100.4.35:19382` is fully idle with no train/eval/rollout processes. Stage2a 50-epoch probes and the 8-epoch `past` LR sweep have completed. |
