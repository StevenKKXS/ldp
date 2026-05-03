# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 17 |
| Recent Progress | Started the CPU-side dataset backfill on host `dev4infer`. A new helper script now downloads and extracts the missing public simulation datasets in parallel, stages archives under `/work-agents/intern_ldp_explorer/outputs/session17_dataset_downloads`, writes a 10-minute ETA log, and expands data into `/mnt/3fs2/.../datasets`. `aloha_twomodes_single` and `pusht` completed immediately, `longhistsquare100` reached the final extraction stage, and the dominant remaining job is `robomimic_image.zip` with an initial ETA around 2h1m. |
