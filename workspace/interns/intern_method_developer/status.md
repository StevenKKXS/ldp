# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 10 |
| Recent Progress | Started exact-PTP downstream encoder ablations on `10.100.2.4:35140`. A 1-step B-square frozen smoke passed, then 16 Square/ToolHang downstream jobs were launched across 8 H200 GPUs using Session 8 encoder checkpoints. |
| Handoff | Downstream logs are under `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/downstream_logs/{20260519_session10,20260519_session10_extra}` and outputs under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/{20260519_session10,20260519_session10_extra}`. Early loss suggests Square/ToolHang settings are very close so far; these are train/val diffusion losses, not rollout scores. |
