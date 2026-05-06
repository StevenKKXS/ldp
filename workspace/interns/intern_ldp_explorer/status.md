# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 66 |
| Recent Progress | Analyzed why most selected-checkpoint evals are at 0 success. Evidence points primarily to underperforming learned policies or a task-specific train/eval representation mismatch, not a globally broken evaluator: Square PTP reaches `0.36` under the same Session 63/65 eval path, while Tool-Hang, Transport, and LongSquare had zero training-rollout checkpoint scores across saved epochs. Session 65 has completed JSON for Square, LongSquare, and Tool-Hang; Transport was still running at `20/25` chunks at `2026-05-06 03:27 UTC`. Recommended adjustment order: first verify cached embedding vs online encoder equivalence per task, then run small all-checkpoint eval sweeps on zero-score tasks, then extend only the strongest PTP candidates before spending on full reruns. |
