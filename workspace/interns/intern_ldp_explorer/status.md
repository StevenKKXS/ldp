# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 110 |
| Recent Progress | Created `session110_experiment_report.md` summarizing the stopped `session89_4x2x2_2000ep` batch, including settings, data paths, final rollout metrics, aggregate readout, caveats, and stop confirmation. Terminated all matching training processes on `10.100.0.29:30103` and `10.100.0.29:36645`; post-stop `nvidia-smi` showed all 8 visible H200 GPUs at about `1 MiB` memory and `0%` utilization. |
