# History Log

<!-- METADATA:SESSION=1 -->

## Session 0
- Created task for no-training evaluation of the official robomimic v0.1 Square(PH) low-dimensional BC-RNN checkpoint.
- Scope includes official checkpoint download, 50-rollout horizon-400 evaluation, video saving, and compatibility reporting.

## Session 1
- Downloaded official model-zoo checkpoint `square_ph_low_dim_epoch_1850_succ_84.pth` into the task directory.
- Current runnable GPU stack is Python 3.12.3, torch 2.5.1+cu124, robomimic 0.3.0, robosuite 1.4.1, mujoco 3.8.0.
- robomimic 0.3 cannot directly load the v0.1 checkpoint because the old config lacks newer fields such as `algo.transformer`; a loader-only patched checkpoint was generated without changing weights.
- Formal current-stack eval with 50 rollouts, horizon 400, seed 0, and saved video produced 33/50 success = 66%.
- Installed robomimic 0.1.0 into the task-local `python_pkgs` target path and confirmed it can load the original checkpoint, but strict old-stack rollout is blocked by `mujoco-py` build requirements (`GL/osmesa.h`) and missing robosuite `offline_study` branch.
- Inspected local Square HDF5 files under `intern_ldp_explorer`; Square PH/MH image datasets have v1.4.1-style env metadata and no explicit `env_version` attribute. The SmolVLA training copy is Square MH `image_abs.hdf5`, 300 demos and 80,731 timesteps.
