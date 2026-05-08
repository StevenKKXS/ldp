# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 105 |
| Recent Progress | Checked the robosuite side of the version inference. The upstream LDP / Diffusion Policy environment pins `cheng-chi/robosuite@277ab9588ad7a4f4b55cf75508b44aa67ec171f0`, not a PyPI `robosuite==...` release. That pinned source declares `__version__ = "1.2.0"` and `setup.py` version `1.2.0`; GitHub compare shows the pinned commit is on the `offline_study` lineage and the `offline_study` branch is two commits ahead of it. Therefore the prior robosuite inference is best stated as `cheng-chi/robosuite` offline-study-era commit with source version `1.2.0`, not current `robosuite 1.4.1`. |
