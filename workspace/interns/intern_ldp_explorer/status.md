# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 63 |
| Recent Progress | Ran one `n_test=100`, `n_samples=1`, `n_train=0`, `n_envs=4`, `test_start_seed=100000` evaluation for the selected checkpoint of each of the 8 seed-42 diffusion subset runs. Selection rule: use the highest checkpoint filename score when available, otherwise use epoch `499`. Final evaluation stamp `1778032161`; outputs are under `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/evals/session63_1778032161/<run>/eval_log.json`. Results: Square DP `0.00` from `epoch=0499-test_mean_score=0.025.ckpt`; Square PTP `0.36` from `epoch=0099-test_mean_score=0.475.ckpt`; Tool-Hang DP/PTP `0.00`; Transport DP/PTP `0.00`; LongSquare DP/PTP `0.00`. Final eval logs all have status `DONE` and zero matches for `Traceback`, runtime errors, OOM, and related failure patterns. The independent eval path used a runtime-only `SimpleVectorEnv` wrapper plus no-op `wandb.log` because the project `AsyncVectorEnv` path is incompatible with the current Gym vector API for these observation spaces outside the training workspace. |
