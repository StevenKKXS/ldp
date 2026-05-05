# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 58 |
| Recent Progress | Started Wave A of the user-approved Fig9 diffusion-only subset on the new GPU host `10.100.0.29:30103` (`lg-cmc-b7r201-b04u06-h200-000040`). Confirmed 4 x H200 GPUs, copied current Square/Tool `_emb` configs to `my_configs/session58`, and launched four seed-42 single-GPU runs: Square DP PID `299641` GPU0, Square PTP PID `299643` GPU1, Tool-Hang DP PID `299645` GPU2, Tool-Hang PTP PID `299647` GPU3. All use `global_obs=16`, `global_horizon=32`, `global_action=8`, `num_epochs=500`, `batch_size=64`, `gradient_accumulate_every=1`, cached embeddings, explicit `policy.past_steps_reg=-1`, and training rollout `n_test=40`. Training-time env runner concurrency is set to `n_envs=4` to reduce the prior async rollout `EOFError` risk. Initial health check at `2026-05-05 11:13 UTC` showed all four parent PIDs alive and in training epoch 2 with GPU utilization around 40%. |
