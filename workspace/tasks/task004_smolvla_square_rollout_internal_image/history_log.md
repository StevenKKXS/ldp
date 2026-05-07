# History Log

<!-- METADATA:SESSION=0 -->

## Session 0
- Created task to configure the internal-image GPU environment and test square rollout success rate using the best SmolVLA-style checkpoint.
- Copied `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/setup_gpu_machine.sh` to the intern-owned task path and patched `INTERN_ROOT` to task004.
- Ran setup successfully through the internal pip mirror; verified `torch`, `mujoco`, `robosuite`, `robomimic`, and `pytorch3d.transforms`.
- Implemented `rollout_smolvla_square.py` to load task003 `epoch_0300.pt` and execute absolute-action Robosuite square rollouts.
- Ran 20 formal rollouts on seeds `10000-10019`; result was `2/20 = 10%` success rate.
- Ran states-only demonstration replay sanity check; first 5 demos succeeded `5/5`.
