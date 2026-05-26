# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 59 |
| Recent Progress | Checked Ceph-only Direction C experiment progress on `10.100.2.19:28106`. Corrected Stage2b M1/M3 have crossed epoch 24 and written first checkpoints: M1 base best offline `val_loss=0.057315 @ e22`, epoch-24 checkpoint `val_loss=0.058112`; M3 random-context best offline `val_loss=0.058737 @ e22`, epoch-24 checkpoint `val_loss=0.058755`. Stage1 `past` retrain is working: `obs_lr=1e-4,tr_lr=1e-4` is better than `obs_lr=5e-5,tr_lr=1e-4`, with best `val/loss_total=0.000689 @ e17` versus `0.000828 @ e14`; this is stable but still worse than the historical NFS best `0.000434`. Used the better Ceph `past` best checkpoint to launch M2 pretrained add_last PID `1368459` and M4 pretrained add_all PID `1368462`; both loaded cache/checkpoint and entered training. Follow-up live poll at `2026-05-26 14:51 UTC`: M2/M4 are alive in epoch 0 around steps `545/542`, with no validation or checkpoint yet. No new rollout success rate yet. |
