# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 111 |
| Recent Progress | Checked the user's proposed PTP-version rerun requirement without launching training. The request is valid as an environment-version ablation of the stopped 4x2x2 batch. `36645` has `/root/ptp_ldp_py39` with Python `3.9.25`, RoboMimic `0.2.0`, pinned RoboSuite source version `1.2.0`, `mujoco-py 2.1.2.14`, and idle 4 x H200; `30103` is idle but does not have that venv. Wrote `session111_ptp_env_4x2x2_requirement_check.md` with the proposed matrix, assumptions, risks, and confirmation items. |
