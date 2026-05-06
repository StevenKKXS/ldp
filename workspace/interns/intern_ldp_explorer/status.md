# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 90 |
| Recent Progress | Checked the active 4x2x2 2000-epoch queue. Stamp `1778070500` failed at the first epoch-100 rollout boundary for Square and LongSquare because the custom `AsyncVectorEnv.reset_async()` did not accept Gym 0.25's `seed`, `return_info`, and `options` reset arguments; Tool-Hang and Transport were stopped before reaching the same failure. Patched `diffusion_policy/gym_util/async_vector_env.py`, synced and py-compiled the patch on the H200 node, then relaunched all eight DP-first lanes under stamp `1778073162`. Current sampled state: GPUs 0-3 are active, each task/action-horizon DP run has live processes and no startup traceback, and PTP remains queued after the matching DP lane. |
