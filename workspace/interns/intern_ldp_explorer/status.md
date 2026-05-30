# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 75 |
| Recent Progress | Set up new H200 node `10.100.0.20:26715` for Direction C with py39 / `robomimic==0.2.0`, repaired node-level Python 3.9 and OSMesa dependencies, verified the Ceph py39 env, and added the norm / ACT-size experiment path. Code changes add Stage1 translator `action_loss_reduction` plus `loss_scale`, optional `translator_context_norm` before downstream context projection, and a deterministic ACT-style action chunking image policy. Added Square configs for ACT-style action8, ACT-size DP/PTP base, ACT-size normalized translator-context, and ACT-size normalized Stage1 past translator. All four configs passed Hydra parse and 1-step train/val smoke. Started four Square runs on GPUs 0-3 under `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/outputs/session75_norm_act_20260530_061542`; Ceph currently contains Square data only, so ToolHang waits for data restoration to Ceph or 3FS1. |
