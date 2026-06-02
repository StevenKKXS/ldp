# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 86 |
| Recent Progress | Marked the GPU-node py39 venv as the main Direction C / PTP-data runtime and added a preflight script. Main env: `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph`, verified as Python `3.9.25`, `robomimic==0.2.0`, `torch==2.5.1+cu124`, CUDA available. Run `diffusion_policy/scripts/check_main_runtime_env.py --require-cuda` with that venv before training, rollout, eval, parameter counting, or smoke tests. |
