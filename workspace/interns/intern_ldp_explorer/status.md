# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 44 |
| Recent Progress | Continued Direction C by turning Stage2b into rollout evidence. Tuned Stage2a probes completed 50 epochs on the new node. Fixed rollout environment on the new node without GPU-node network access by downloading Noble OSMesa/GL packages from the CPU side into `/mnt/nfs/tingwen/intern_ldp_explorer/packages/osmesa_noble_20260521` and using the extracted rootfs through `CPATH`, `LIBRARY_PATH`, and `LD_LIBRARY_PATH`; verified `mujoco_py`, `robosuite 1.2.0`, and `robomimic 0.2.0` imports. Stage2b Square action8 rollout results so far are unfavorable to the core pretrained-context hypothesis: epoch 49 pretrained context `2/10` vs random context `5/10`; epoch 24 pretrained context `0/10` vs random context `2/10`. Filled the new 4xH200 node with additional Stage2b ablations under `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage2b_square_ablation_20260521_2230`: base no-context, pretrained add-last, random add-last, and pretrained nonzero-projector. |
