# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 99 |
| Recent Progress | Investigated release-data and simulator-version provenance for the RoboMimic tasks. Local HDF5 metadata for Square, Tool-Hang, Transport, and LongSquare records env names, cameras, controller settings, and `control_delta`, but no robomimic / robosuite / MuJoCo version keys. The LDP and Diffusion Policy environment files pin `robomimic==0.2.0` plus a `cheng-chi/robosuite` commit, while the active training venv is `robomimic 0.3.0`, `robosuite 1.4.1`, `mujoco 3.8.0`. Robomimic docs and issue `ARISE-Initiative/robomimic#178` confirm Tool-Hang image success can be version / data-generation sensitive, especially across `offline_study`, robosuite `v1.4.1`, and generated image datasets. |
