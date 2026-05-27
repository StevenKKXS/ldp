# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 73 |
| Recent Progress | Brought up fresh Ceph-only 8xH200 node `10.100.0.62:24345` for Direction C rollout/eval. Repaired the shared py39 environment by installing node-level Python 3.9 and OSMesa headers, then offline-installed `robosuite==1.2.0`, `av==14.2.0`, and `egl-probe==1.0.2` from Ceph package caches. Verified `torch 2.5.1+cu124`, `robomimic 0.2.0`, `robosuite 1.2.0`, and `mujoco_py 2.0.2.13`; completed reward-only Square rollout smoke with M1 e49 checkpoint (`1` episode, score `0.0`). Four corrected Stage2b configs parse on the new node. Launched eight 50-episode Square rollout eval jobs under `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/stage2b_rollout_eval_newnode_20260527`, covering e24/e49 EMA comparisons plus raw-model checks for M1 and M4. |
