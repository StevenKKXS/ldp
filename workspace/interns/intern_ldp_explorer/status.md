# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 47 |
| Recent Progress | Read-only review of `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/setup_gpu_machine.sh` and Fig. 9 task env needs. Current setup builds a Python 3.12 `/root/venv` for the RoboMimic/robosuite stack with Torch 2.5.1, MuJoCo 3.8.0, robosuite 1.4.1, robomimic 0.3.0, zarr/gym/Hydra/media packages plus site-package patches. It should cover RoboMimic benchmark tasks and Long Square after existing wrappers/overrides, but it does not explicitly cover ALOHA (`dm-control` missing and known incompatible with MuJoCo 3.8.0) or Push-T (`pygame`/`pymunk`/`shapely`/`scikit-image` not explicit). No environment or script modifications were made. |
