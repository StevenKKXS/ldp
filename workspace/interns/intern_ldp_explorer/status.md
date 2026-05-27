# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 73 |
| Recent Progress | Completed the first corrected Stage2b Square rollout SR table on the fresh Ceph-only 8xH200 node `10.100.0.62:24345`. Reward-only rollout runtime is now working with py39 / `robomimic==0.2.0`. Results under `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_rollout_eval_newnode_20260527`: M1 base e24 EMA `22/50=44%`, M3 random e24 EMA `21/50=42%`, M2 pretrained add_last e24 EMA `15/50=30%`, M4 pretrained add_all e24 EMA `18/50=36%`, M1 base e49 EMA `16/50=32%`, M3 random e49 EMA `26/50=52%`, M1 e49 raw model `2/50=4%`, M4 e24 raw model `4/50=8%`. This is new relative to the latest Feishu report: rollout SR is available, and the current projection-based pretrained translator context does not beat base/random controls in the first matched e24 comparison. |
