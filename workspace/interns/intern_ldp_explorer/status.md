# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 83 |
| Recent Progress | Clarified the control-semantics question for Tool-Hang experiment 1 vs experiment 2. Experiment 1 replays `image_abs.hdf5` by explicitly setting `control_delta=false` and sending absolute 7D actions back into the env after the same rotation6d roundtrip used by the policy path. Experiment 2 replays original `image.hdf5` by keeping delta-control semantics and sending the raw relative 7D actions directly. This means the replay script did not mix absolute actions with a relative controller or vice versa; that specific semantic mismatch was avoided on purpose. |
