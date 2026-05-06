# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 91 |
| Recent Progress | Checked stamp `1778073162`: Square/Tool-Hang/Transport were still training, but LongSquare DP `a8` and `a1` again stopped at epoch `99` before ckpt/mp4. The new traceback showed Gym 0.25 `concatenate` API incompatibility in the custom vector env, not a task/data/loss issue. Patched `diffusion_policy/gym_util/async_vector_env.py` and `diffusion_policy/gym_util/sync_vector_env.py` to use Gym 0.25 argument order, synced and py-compiled on the H200 node, stopped the doomed `1778073162` processes, and relaunched the full 4x2x2 queue under effective stamp `1778075154`. Sampled state after relaunch: GPUs 0-3 active, all eight DP lanes in epoch 0/1, no startup errors; PTP remains queued after matching DP completion. |
