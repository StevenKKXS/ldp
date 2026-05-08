# Task Knowledge

<!-- METADATA:SESSION=10 -->

## Working Rules
- The task expanded from no-training BC-RNN evaluation to include issue #157 retraining checks and SmolVLA resource-utilization training runs.
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
- Issue #157 final fix path is to train/evaluate with image observations generated for the active robosuite 1.4.x visual stack. For this task, official `demo_v141.hdf5` was converted to `image_v141.hdf5` and then to `image_abs_v141.hdf5` for SmolVLA-style absolute-action training.
- SmolVLA resource run base: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/smolvla_resource_1000ep_early10_20260507_122849`.
- Required SmolVLA runs: `ldp_mh_abs10_seed42` on the LDP-MH own copy `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`, and `official_ph_v141_abs10_seed43` on `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_abs_v141.hdf5`.
- Exploratory SmolVLA run: `ldp_mh_abs10_big384_seed44`, using emb_dim 384 and 8 expert layers on the same LDP-MH dataset.
- Completed SmolVLA checkpoints: each run has `latest.pt` plus named eval checkpoints `epoch_0010.pt`, `epoch_0020.pt`, ..., `epoch_0100.pt`, then `epoch_0200.pt`, ..., `epoch_1000.pt` under the run base. Offline metrics are from action reconstruction / flow validation, not robosuite rollout success.
- SmolVLA checkpoint logic: `latest.pt` is overwritten whenever `should_eval` is true or `epoch % checkpoint_every_epochs == 0`; with the run args this means eval epochs plus every 25 epochs. Named `epoch_XXXX.pt` files are written only when `should_eval` is true, so the retained named checkpoints follow the eval schedule.
- SmolVLA all-checkpoint rollout output root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_all_ckpts_20rollouts_20260508_0255`; completed 57 checkpoints, 20 rollouts each, and 1140 saved episode videos.
- SmolVLA rollout bests under the 20-rollout protocol: big384 LDP-MH epoch 1000 `0.30`, small LDP-MH epoch 200 `0.25`, official PH v141 epoch 600 `0.20`. This shows offline action MSE is not a reliable ranker for closed-loop success.
- SmolVLA selected best-checkpoint 50-rollout output root: `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_best_ckpts_50rollouts_20260508_0343`; completed 150 rollouts and 150 saved videos.
- SmolVLA selected best-checkpoint 50-rollout results: big384 LDP-MH epoch 1000 `13/50 = 0.26`, small LDP-MH epoch 200 `9/50 = 0.18`, official PH v141 epoch 600 `7/50 = 0.14`.
- Input comparison: issue #157 image BC-RNN and SmolVLA both use `agentview_image`, `robot0_eye_in_hand_image`, `robot0_eef_pos`, `robot0_eef_quat`, and `robot0_gripper_qpos`; neither uses the dataset's `object`, joint state, velocity, depth, scan, or goal observations.
- Input comparison caveat: official model-zoo low-dimensional BC-RNN is different from the issue #157 image BC-RNN. It uses low-dimensional `object` in addition to `robot0_eef_pos`, `robot0_eef_quat`, and `robot0_gripper_qpos`, and uses no image observations.
- Temporal comparison: issue #157 image BC-RNN has LSTM recurrence with training `seq_length=10` and RNN horizon 10, while the SmolVLA-style policy conditions on the current two images and current 9D robot state, then predicts a 16-step action chunk. This is temporal memory/architecture difference, not an extra privileged observation key.
- Completed issue #157 BC-RNN checkpoint/video highlight: best checkpoint `model_epoch_540_NutAssemblySquare_success_0.8.pth` and video `NutAssemblySquare_epoch_540.mp4` under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/issue157_v141/issue157_square_ph_image_v141_bc_rnn_600ep_s1/20260507120353`.
- DP no-hist candidate for discussion: use `train_diffusion_unet_image_workspace.yaml` with `task=square_image_abs`, `n_obs_steps=2`, `dataset_obs_steps=2`, `n_action_steps=1`, `horizon=16`, no past-action prediction, and no object observation. This matches the README's short-history DP note (`obs=2, act=1, horizon=16`) more closely than the Square `unet_hybrid_square.yaml` default (`obs=16`, `horizon=32`, past action prediction enabled).
- DP no-hist candidate datasets: LDP-MH absolute-action image data at `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5` and official-PH v1.4.1 absolute-action image data at `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_abs_v141.hdf5`.
- DP `horizon=16` means the UNet diffusion policy denoises a 16-step action trajectory per sample. It is not the environment rollout horizon; the rollout limit remains PH 400 or MH 500 by task config. In inference, `DiffusionUnetImagePolicy.predict_action` samples `action_pred` with length `horizon`, then returns only the slice from `n_obs_steps - 1` through `n_obs_steps - 1 + n_action_steps`; therefore `n_action_steps=1` executes one action then replans, while `n_action_steps=8` executes an 8-action chunk from the same 16-step prediction.
- DP no-hist implementation: task-local wrappers in `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/dp_nohist_scheduled_workspaces.py` add scheduled checkpoint/rollout epochs while preserving native UNet and transformer policy behavior. The DiT-style run uses `DiffusionTransformerHybridImagePolicy` / `TransformerForDiffusion` with `past_action_pred=false` and `use_embed_if_present=false`.
- DP no-hist launch script: `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/launch_dp_nohist_unet_dit_square.sh` starts four runs with `horizon=16`, `n_obs_steps=2`, `n_action_steps=1`, 1000 epochs, and 50-video test rollout evals on scheduled epochs.
