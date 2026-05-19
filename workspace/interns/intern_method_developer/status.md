# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 13 |
| Recent Progress | Completed the first 16 exact-PTP downstream ablations. Square shows the clearest train/val loss signal for frozen pretrained encoders; ToolHang is essentially tied across methods. Added rollout eval smoke tooling and repaired current py310 env-runner compatibility enough for a 5-step Square rollout smoke to pass. |
| Handoff | Launched 8 seed-43 downstream repeat jobs on `10.100.2.4:35140` to test whether Square frozen-encoder gains are stable. Logs: `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/downstream_logs/20260519_session13_seed43/pids.tsv`; outputs: `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session13_seed43`. |
