# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 93 |
| Recent Progress | Confirmed resume is supported via `training.resume=true` from each run's `checkpoints/latest.ckpt`, and verified unfinished DP latest checkpoints were stable before pausing. Stopped the unfinished DP lanes, kept completed LongSquare DP `a8` and already-running LongSquare PTP `a8`, then launched the remaining PTP jobs first using `session93_ptp_priority.sh`. Health check at `2026-05-07T08:04:25Z`: all eight PTP jobs are running across GPUs 0-3 with no startup errors; unfinished DP processes are all stopped at resumable checkpoints. Added `session93_resume_paused_dp.sh` to resume the paused DP jobs after PTP priority runs have progressed or completed. |
