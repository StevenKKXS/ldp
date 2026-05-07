# Task Knowledge

<!-- METADATA:SESSION=1 -->

## Working Rules
- Do not train; only evaluate the official pretrained BC-RNN checkpoint.
- Keep all downloaded checkpoints, rollout logs, videos, and reports under the intern_method_developer task directory.
- Treat robomimic / robosuite version differences as first-order experimental variables.

## Official References
- Model-zoo entry: `https://robomimic.github.io/docs/model_zoo/robomimic_v0.1.html`
- Official eval tutorial: `https://robomimic.github.io/docs/tutorials/using_pretrained_models.html`

## Findings
- Official target: Square(PH), low-dimensional BC-RNN, approximate success rate 84%.
- Official tutorial uses 50 rollouts, horizon 400, seed 0, and can save video with `--video_path`.
- Official checkpoint downloaded for this task: `http://downloads.cs.stanford.edu/downloads/rt_benchmark/model_zoo/square/bc_rnn/square_ph_low_dim_epoch_1850_succ_84.pth`; SHA256 `f2143ebfd474e694c7eecbf013ab82308fbc4c6e00abaffd53e5c8eba2613301`.
- The checkpoint is model-zoo robomimic-v0.1 Square(PH) low-dimensional BC-RNN. It stores `env_name=NutAssemblySquare` and config path `/cvgl2/u/amandlek/batch_datasets/final_benchmark_datasets/square/ph/low_dim.hdf5`, but no explicit environment version field.
- Current successful evaluation stack is robomimic 0.3.0 + robosuite 1.4.1 + mujoco 3.8.0 with a loader-only config patch. This is not the official strict stack.
- Strict older loader attempt: robomimic 0.1.0 can load the original checkpoint, but rollout requires `mujoco_py` and an offline-study-era robosuite install. `mujoco_py` compilation is blocked by missing system header `GL/osmesa.h`.
- Local `intern_ldp_explorer` Square PH image dataset: 200 demos, 30,154 timesteps, path `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/ph/image.hdf5`.
- Local `intern_ldp_explorer` Square MH image dataset: 300 demos, 80,731 timesteps, path `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image.hdf5`.
- The task003 SmolVLA training copy is Square MH `image_abs.hdf5`, 300 demos, 80,731 timesteps, copied from the local `intern_ldp_explorer` dataset and using image observations plus absolute-action conversion.
- Issue #157 is relevant: maintainers point to robosuite branch/version mismatch and say image-observation performance can degrade because textures changed between robosuite v1.2 and v1.4; model-zoo pretrained links were trained on robosuite v1.2 / old stack.
