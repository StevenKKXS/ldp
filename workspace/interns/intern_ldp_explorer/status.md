# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 81 |
| Recent Progress | Saved Tool-Hang replay videos on the H200 node for four diagnostic cases, two demos each. Video outputs landed under `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/debug/session81_toolhang_replay_videos/` with `manifest.json`. The image-enabled video path exposed an additional sensitivity: `image_abs` replay with offscreen image observations succeeded on `demo_0` and `demo_5`, while the original delta-action cases still failed on both demos, and `abs_hard_reset_false` showed one success and one failure. This means Tool-Hang behavior depends not only on dataset/action path but also on how the environment is instantiated for replay. |
