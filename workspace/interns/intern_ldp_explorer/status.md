# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 70 |
| Recent Progress | Clarified the current Direction C input contract: current Square translator/downstream image configs use two rollout-observable RGB streams (`agentview_image`, `robot0_eye_in_hand_image`) and proprio lowdim keys (`robot0_eef_pos`, `robot0_eef_quat`, `robot0_gripper_qpos`), not privileged `past_act` or object state. Added `docs/direction_c_behavior_translator/experiments.md` Session 70 sections documenting the input contract, fast modality checks, and the revised Stage2b plan: B0 default DP with `cond[0..1]`, B1 proven PTP with `cond[0..15]` and past+future action objective, plus both current projection-based translator injection and encoder-replacement transfer experiments. |
