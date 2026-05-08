# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 107 |
| Recent Progress | Configured a new isolated PTP-version venv on `10.100.0.29:36645` at `/root/ptp_ldp_py39`. It uses Python `3.9.25`, `robomimic 0.2.0`, pinned `cheng-chi/robosuite@277ab9588ad7a4f4b55cf75508b44aa67ec171f0` with source version `1.2.0`, MuJoCo `2.1.0` binary for `mujoco-py 2.1.2.14`, `mujoco 2.3.7`, and H200-compatible `torch 2.5.1` / CUDA 12.4. Smoke checks passed for LDP imports, Square / Tool-Hang / Transport env reset, `reset_to({'states': ...})`, `reset_to({'model': ..., 'states': ...})`, and a tiny mp4 write/read test. |
