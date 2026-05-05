# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 49 |
| Recent Progress | Completed smoke train plus online rollout on the 4 currently feasible tasks on `10.100.0.29:30103`: Square, Tool-Hang, Transport, and LongSquare. Each run used `num_epochs=1`, `max_train_steps=1`, `max_val_steps=1`, `rollout_every=1`, `n_envs=1`, `n_test=1`, `max_steps=5`, offline wandb, and wrote `logs.json.txt` plus `checkpoints/latest.ckpt`. Final `test/mean_score` was `0.0` for all four, with no traceback/error matches in logs. Outputs: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/outputs/session49_smoke_{square,toolhang,transport,longsquare}_1777972600`; logs: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session49_smoke_{square,toolhang,transport,longsquare}_1777972600.log`. H200 GPUs were idle after completion. |
