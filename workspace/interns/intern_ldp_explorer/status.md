# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 65 |
| Recent Progress | Configured and launched a video-enabled rerun of the same 8 selected-checkpoint eval tasks on the H200 host `10.100.0.29:30103`. Stamp `1778035802`; output root `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/evals/session65_video_1778035802`; logs under `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/logs/session65_video_eval_<run>_1778035802.log`. Settings match the Session 63 scoring pass except visualization is enabled: `n_test=100`, `n_train=0`, `n_envs=4`, `n_samples=1`, `test_start_seed=100000`, `n_test_vis=4`, `n_train_vis=0`. Each run has 4 saved local mp4 files under `<output_root>/<run>/media/` for 32 videos total. The full 100-episode eval processes are still running at the latest check; current progress reached approximately Square `18-19/25`, LongSquare `17/25`, Tool-Hang `12-13/25`, and Transport `7-8/25`, with no failure signature observed. |
