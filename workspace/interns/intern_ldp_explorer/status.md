# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 57 |
| Recent Progress | Checked the active Ceph-only Direction C jobs on `10.100.2.19:28106` at `2026-05-26 03:41 UTC`. All four parent PIDs `91453`, `91456`, `91460`, and `91463` remain alive in `Sl` state with low `/dev/shm` usage. Stage2b M1/M3 were still in epoch 0 around global step `1779/2478`, so first offline validation loss should arrive in roughly 10-15 minutes from that check. Stage1 `past` retrains were around epoch 1 step `345/620`, so first Stage1 eval and an initial `best.ckpt` should arrive in roughly 15-25 minutes, but a meaningful translator checkpoint for M2/M4 should be judged after several epochs; first rollout-capable Stage2b checkpoints require epoch 25, roughly 10-11 hours at the current safe-worker speed. |
