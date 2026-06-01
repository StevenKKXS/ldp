# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 77 |
| Recent Progress | Set up new 8xH200 node `10.100.2.39:23494` with the shared Ceph py39 / `robomimic==0.2.0` runtime. Added Robomimic-compatible official-ACT CVAE policy/configs, a translator modality-ablation eval script, and raw-action-loss support for Stage1 translator. Quick Square leakage sanity check shows image zero/shuffle barely changes past loss, while proprio zero makes past loss explode, supporting a lowdim/proprio shortcut diagnosis. Official-ACT 5-epoch Square rollout is `0/20`; fixed 25-epoch ACT is active. Raw-loss Square translator reached epoch 8 with best val/past loss `0.006775`. ACT-size Stage2b base/random/add_last/add_all are active around epoch 7-8; first rollout is still pending at epoch 25. Added lowdim-only and image-only Square translator ablation runs; lowdim-only is active on GPU0 and image-only is preloading images. |
