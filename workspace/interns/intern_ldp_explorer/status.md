# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 26 |
| Recent Progress | `robomimic_image.zip` is now fully downloaded and the shared RoboMimic tree includes `tool_hang` and `transport`. The Session 25 watchdog exhausted its 12 checks before the extraction gate became true, so it did not auto-launch Wave 1. I manually launched `Tool-Hang long-hist DP` and `Tool-Hang long-hist PTP` on the GPU node after fixing the remote env mismatch (`VIRTUAL_ENV=/root/venv`, `PYTHONPATH=/mnt/3fs2/data/tingwen.du/workspace/ldp`), and added an explicit Session 26 validator close-out note in `history_log.md` so that progression is unambiguous to the stop hook. |
