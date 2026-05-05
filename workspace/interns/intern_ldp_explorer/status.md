# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 50 |
| Recent Progress | Inspected current training recipe without modifying code. Confirmed node `10.100.0.29:30103` has no active `run_train.py` / `train.py` / `eval.py` processes and all 4 H200s are idle. Current valid recipe is the Figure 9-style cached-embedding path for the 4 smoke-validated tasks: Square, Tool-Hang, Transport, and LongSquare. Core setup: `/root/venv`, `MUJOCO_GL=egl`, wrapper `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/run_train.py`, frozen official observation encoders, `_emb` configs, `num_epochs=3500`, `batch_size=64`, cosine LR with `lr=1e-4`, EMA enabled, online rollout/checkpoint cadence from task config, and DP/PTP controlled by `policy.past_action_pred=false/true`. |
