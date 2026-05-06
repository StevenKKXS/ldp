# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 62 |
| Recent Progress | Collected a fresh run-status snapshot at `2026-05-06 01:27 UTC`. The 8 seed-42 Wave A/B training parent PIDs have exited after reaching `Training epoch 499`; both checked H200 containers are idle with 4 GPUs at about `1 MiB` used and `0%` utilization. `/mnt/3fs2` reports `448T` size, `317T` used, `131T` available, `71%` used. Checkpoint scores from training-time `n_test=40`: Square DP best `0.025` at epoch `499`; Square PTP best `0.475` at epoch `99` and final epoch `499` score `0.425`; Tool-Hang DP/PTP, Transport DP/PTP, and LongSquare DP/PTP all have best checkpoint score `0.000`. Error scan found zero matches for 7 runs; LongSquare PTP has one async checkpoint-save incident near epoch `450` with `No space left on device`, leaving `epoch=0449-test_mean_score=0.000.ckpt` as a 0-byte file. LongSquare PTP `epoch=0499...ckpt` and `latest.ckpt` were verified loadable with `torch.load`. These are not final paper-style evaluation results. |
