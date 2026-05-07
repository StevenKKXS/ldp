# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 97 |
| Recent Progress | Resumed paused DP jobs on `10.100.0.29:36645` using two H200 GPUs. Added and synced `session97_resume_dp_2gpu_36645.sh`, then launched seven DP resume runs under stamp `1778075154` with `training.resume=true`: Square `a8/a1`, Transport `a8/a1` on GPU0, Tool-Hang `a8/a1` and LongSquare `a1` on GPU1. At `2026-05-07T12:22:30Z`, GPU0 used `16433 MiB` at `100%`, GPU1 used `8854 MiB` at `98%`, GPU2/GPU3 remained idle, and all seven DP logs showed checkpoint resume plus entry into training epoch with no traceback. |
