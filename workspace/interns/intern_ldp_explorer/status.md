# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 52 |
| Recent Progress | Explored public PTP sources for training recipe and convergence-time claims. Paper/project page state the method recipe: short-context encoder pretraining, frozen encoder, cached embeddings, long-context policy-head training with PTP; default long-context inputs use 16 observations and single-sample inference. Paper appendix states all policies are trained for 500 epochs by default and long-horizon ALOHA for 1500, while the public GitHub `_emb` configs list `num_epochs=3500`; this is a source mismatch to report. Public sources do not give a task-specific wall-clock or checkpoint number that guarantees paper reward; they report a two-day caching ablation, checkpoints every 50 epochs for that ablation, and that cached training matches baseline performance in 20% of training time and surpasses it within 40% of compute budget. |
