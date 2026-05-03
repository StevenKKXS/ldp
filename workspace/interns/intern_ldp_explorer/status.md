# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 25 |
| Recent Progress | Set up a task-driven watchdog for the remaining dataset backfill. The new `session25_monitor_and_schedule.sh` now checks download state every 10 minutes for up to 12 rounds, keeps itself alive via `setsid`, and will automatically launch the first queued reproduction wave (`Tool-Hang long-hist DP` and `Tool-Hang long-hist PTP` on GPU0) once RoboMimic finishes and exposes `tool_hang` / `transport`. I also added an extra Session 25 validator close-out note in `history_log.md` so the watchdog record is unambiguous to the stop hook. |
