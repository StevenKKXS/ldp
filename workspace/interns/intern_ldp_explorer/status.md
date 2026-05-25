# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 53 |
| Recent Progress | Confirmed the four stale GPU processes on `10.100.2.35:25076` are historical `intern_ldp_explorer` Direction C jobs, not unknown external workloads. PIDs `1086376` and `26885` match Stage 1 Square translator `past` and `past_future` runs under `stage1_square_20260519_143020`; PIDs `4026333` and `4026336` match Stage 2b Square action8 pretrained-context and random-context runs under `stage2b_square_translator_context_20260521_1252`. Remote `/proc` confirms their cwd/PYTHONPATH point to `/mnt/nfs/tingwen/intern_ldp_explorer/repos/ldp_behavior_translator`, they use py39 / `robomimic==0.2.0`, they now have `PPID=1`, and all remain blocked in `wait_on_page_bit_common`. |
