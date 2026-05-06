# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 67 |
| Recent Progress | Completed cached-embedding versus frozen-online-encoder consistency checks on the current selected PTP checkpoints. Square, Tool-Hang, and Transport match tightly (`rel_l2_mean` about `1e-4` to `4e-4`, cosine about `1.0`). LongSquare is a clear mismatch (`rel_l2_mean=1.1414`, `l2_mean=3.0731`, `cosine_mean=0.4791`) even though the training checkpoint encoder weights exactly match `longhist_encoder.ckpt` and the normalizer tensors match. Result JSON: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/debug/session67_embedding_check/embedding_consistency_summary.json`. Implication: regenerate LongSquare cached embeddings before using or extending that run; Tool-Hang and Transport zero scores need other diagnostics such as checkpoint sweeps or longer training. |
