# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 53 |
| Recent Progress | Adopted the paper B.3.1 training-length interpretation for PTP transformer experiments. Updated transformer mainline configs so non-ALOHA policies train for `500` epochs by default, and ALOHA transformer configs train for `1500` epochs. This covers Square, Tool-Hang, Transport, LongSquare, Push-T, and ALOHA transformer raw/embedding/reg variants; non-PTP-transformer UNet/BC-RNN legacy configs were left unchanged. The current main `_emb` runnable set now uses `global_obs=16` and `num_epochs=500` for Square/Tool-Hang/Transport/LongSquare. |
