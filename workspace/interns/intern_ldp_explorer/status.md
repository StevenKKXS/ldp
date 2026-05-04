# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 26 |
| Recent Progress | `robomimic_image.zip` is now fully downloaded and the shared RoboMimic tree includes `tool_hang` and `transport`. The Session 25 watchdog exhausted its 12 checks before the extraction gate became true, so it did not auto-launch Wave 1. I manually launched `Tool-Hang long-hist DP` and `Tool-Hang long-hist PTP` on the GPU node after fixing the remote env mismatch: the key missing pieces were `VIRTUAL_ENV=/root/venv` and `PYTHONPATH=/mnt/3fs2/data/tingwen.du/workspace/ldp`. Both jobs are now alive as `PID 3361630` and `PID 3361637`. |
