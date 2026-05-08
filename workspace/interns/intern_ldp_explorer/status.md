# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 106 |
| Recent Progress | Checked why the active setup used `robomimic 0.3.0`, `robosuite 1.4.1`, and `mujoco 3.8.0` instead of the upstream LDP pins. History shows this was an operational H200/Python 3.12/internal-mirror setup choice: the helper script records `robomimic 0.3` as the internal mirror upper bound, `robosuite 1.4.1` as the matching stack for robomimic 0.3, `mujoco 3.8` as the robosuite 1.4 upper bound, and patches away old `mujoco_py` import issues. I did not find a record proving the upstream `robomimic==0.2.0` + pinned `cheng-chi/robosuite@277ab9588...` stack was attempted and failed. |
