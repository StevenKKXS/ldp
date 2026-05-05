# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 55 |
| Recent Progress | Prepared a pre-launch parameter checklist for user review; no training was started. Planned first formal runnable batch is the 4 smoke-validated tasks only: Square, Tool-Hang, Transport, and LongSquare, each with DP (`policy.past_action_pred=false`) and PTP (`true`). Common recipe: single process on one H200 per run, `batch_size=64`, `gradient_accumulate_every=1`, `global_obs=16`, `global_horizon=32`, `global_action=1`, `num_epochs=500`, frozen official encoder, cached embedding HDF5 train file, raw HDF5 rollout path, `lr=1e-4`, cosine scheduler, warmup `1000`, EMA enabled, seed `42` for the first pass. Training rollout remains config-driven (`n_test=40`) for checkpoint selection; final paper-style evaluation should use `100` episodes x `3` seeds. |
