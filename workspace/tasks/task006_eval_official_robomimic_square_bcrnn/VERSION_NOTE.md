# Version Note

<!-- METADATA:SESSION=1 -->

## Downloaded Checkpoint
- File: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/checkpoints/square_ph_low_dim_epoch_1850_succ_84.pth`
- Source: `http://downloads.cs.stanford.edu/downloads/rt_benchmark/model_zoo/square/bc_rnn/square_ph_low_dim_epoch_1850_succ_84.pth`
- SHA256: `f2143ebfd474e694c7eecbf013ab82308fbc4c6e00abaffd53e5c8eba2613301`
- Version identity: official model-zoo robomimic-v0.1 Square(PH) low-dimensional BC-RNN checkpoint.
- Checkpoint metadata: `env_name=NutAssemblySquare`, `algo_name=bc`, training data path embedded as `/cvgl2/u/amandlek/batch_datasets/final_benchmark_datasets/square/ph/low_dim.hdf5`; no explicit `env_version` field was present.

## Local Data
- Square PH image data: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/ph/image.hdf5`, 200 demos, 30,154 timesteps.
- Square MH image data: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image.hdf5`, 300 demos, 80,731 timesteps.
- SmolVLA training copy: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`, 300 demos, 80,731 timesteps.
- These files store `env_args` for `NutAssemblySquare` with camera names `agentview` and `robot0_eye_in_hand`, but no explicit `env_version`. The metadata shape and file lineage match robomimic v0.3 / robosuite v1.4.1-style datasets, not the old `offline_study` dataset used by model-zoo v0.1 checkpoints.

## Current Evaluation Stack
- GPU stack: Python 3.12.3, torch 2.5.1+cu124, robomimic 0.3.0, robosuite 1.4.1, mujoco 3.8.0.
- Current-stack result with a loader-only patched checkpoint: 33/50 success = 66%, horizon 400, seed 0.
- Saved video: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/videos/official_square_ph_low_dim_bcrnn_seed0_50rollouts_h400.mp4`.

## Strict Old Stack Status
- robomimic 0.1.0 was installed under the task-local `python_pkgs` path and can load the original checkpoint.
- Strict rollout is blocked because robomimic 0.1.0 uses `mujoco_py`; `mujoco_py` compilation currently fails on missing `GL/osmesa.h`, and the robosuite `offline_study` branch is not installed.
