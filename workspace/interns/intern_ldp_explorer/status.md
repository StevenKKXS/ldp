# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 56 |
| Recent Progress | Applied user review corrections to the pre-launch plan. Updated the four executable main `_emb` configs so `global_action=8` for Square, Tool-Hang, Transport, and LongSquare. Confirmed each already has `past_steps_reg=-1`; launch commands will still explicitly set `policy.past_steps_reg=-1` for both DP and PTP. The experiment will be labeled `Fig9 diffusion-only subset` rather than full Fig. 9. Training rollout stays `n_test=40` for checkpoint selection; final paper-style eval must use `n_test=100`, `n_samples=1`, seeds `[42,43,44]`, and avoid the `eval.py` perturb path that forces `n_test=150`. |
