# History Log

<!-- METADATA:SESSION=10 -->

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

## Session 2
- Reproduced the issue #157 final-data fix path by generating Square(PH) `image_v141.hdf5` from official `demo_v141.hdf5` under robomimic 0.3 / robosuite 1.4.1; dataset has 200 demos and 30,154 timesteps.
- Started formal issue #157 BC-RNN image training on `image_v141.hdf5`; early 50-rollout success was 0.42 at epoch 20 and 0.48 at epoch 40, with videos and checkpoints saved under the task run directory.
- Converted official Square(PH) `image_v141.hdf5` to `image_abs_v141.hdf5` for SmolVLA absolute-action training.
- Added scheduled SmolVLA training code that evaluates every 10 epochs through epoch 100 and every 100 epochs after that.
- Launched three detached SmolVLA Square 1000-epoch runs under the task directory: LDP-MH baseline, official PH v141 baseline, and a larger LDP-MH big384 exploratory run.
- First SmolVLA offline eval results: LDP-MH baseline epoch 10 `val_sample_action_mse=0.1463506222`; official PH v141 baseline epoch 10/20/30 `val_sample_action_mse=0.1962940693/0.1815359592/0.1762230098`.

## Session 3
- Checked the remote GPU host on 2026-05-08 02:28 UTC; both H200 GPUs were idle and no SmolVLA or robomimic training processes were running.
- Confirmed all three SmolVLA resource runs reached epoch 1000 and saved `latest.pt` plus scheduled checkpoints.
- SmolVLA final offline action MSEs: LDP-MH baseline `0.1309051514`, official PH v141 baseline `0.1680839658`, LDP-MH big384 exploratory run `0.1530992389`.
- SmolVLA best offline action MSEs: LDP-MH baseline epoch 600 `0.1279252321`, official PH v141 baseline epoch 1000 `0.1680839658`, LDP-MH big384 epoch 1000 `0.1530992389`.
- Confirmed issue #157 BC-RNN image training completed epoch 600 with 30 rollout evals; best 50-rollout success was epoch 540 at `0.80`, final epoch 600 was `0.54`.

## Session 4
- Checked SmolVLA checkpoint frequency in `train_eval_smolvla_square_scheduled.py` and in the actual run directories.
- Named SmolVLA epoch checkpoints are saved only on offline-eval epochs: `10,20,...,100,200,...,1000`.
- `latest.pt` is overwritten on every checkpoint trigger, where the trigger is any offline-eval epoch or any epoch divisible by `checkpoint_every_epochs=25`; non-eval 25-epoch triggers are not retained as named `epoch_XXXX.pt` files.

## Session 5
- Added and pushed `rollout_smolvla_square_all_ckpts.py`, a batch Robosuite rollout runner that discovers all SmolVLA epoch checkpoints and splits work across multiple GPU workers.
- Ran all 57 SmolVLA named checkpoints with 20 rollouts each, seeds `10000-10019`, horizon 400, action horizon 8, and video saving.
- Completed 1140 SmolVLA rollout episodes and saved 1140 mp4 videos under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_all_ckpts_20rollouts_20260508_0255`.
- SmolVLA rollout bests: `ldp_mh_abs10_big384_seed44` epoch 1000 `6/20 = 0.30`; `ldp_mh_abs10_seed42` epoch 200 `5/20 = 0.25`; `official_ph_v141_abs10_seed43` epoch 600 `4/20 = 0.20`.
- Video decode spot checks passed on sample videos from all three SmolVLA runs; the GPU host was idle again after the batch finished.

## Session 6
- Continued with the selected best SmolVLA checkpoints from the all-checkpoint sweep and ran 50-rollout evaluations with video saving for each selected checkpoint.
- Saved 150 additional SmolVLA episode videos under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/rollouts/smolvla_best_ckpts_50rollouts_20260508_0343`.
- 50-rollout results: big384 LDP-MH epoch 1000 `13/50 = 0.26`, small LDP-MH epoch 200 `9/50 = 0.18`, official PH v141 epoch 600 `7/50 = 0.14`.
- Video decode spot checks passed on samples from all three 50-rollout video directories; the GPU host was idle again after completion.

## Session 7
- Compared the observation inputs for the issue #157 image BC-RNN, the official model-zoo low-dimensional BC-RNN, and the SmolVLA-style policies.
- Confirmed issue #157 image BC-RNN uses `agentview_image`, `robot0_eye_in_hand_image`, `robot0_eef_pos`, `robot0_eef_quat`, and `robot0_gripper_qpos`; it does not use `object`, goals, joint states, velocities, depth, or scans.
- Confirmed SmolVLA uses the same two image keys and the same three low-dimensional robot state keys, plus a learned constant language token internal to the model.
- Confirmed the official model-zoo low-dimensional BC-RNN uses `robot0_eef_pos`, `robot0_eef_quat`, `robot0_gripper_qpos`, and `object`, but no images.

## Session 8
- Paused DP no-hist execution after the user requested key parameters first.
- Inspected the LDP Diffusion Policy configs and identified the intended short-history/common DP setting from the project README: `obs=2`, `act=1`, `horizon=16`.
- Proposed the first experiment matrix as two one-GPU runs: Square LDP-MH absolute-action image data and Square official-PH v1.4.1 absolute-action image data, both with scheduled checkpoint/rollout at epochs `10,20,...,100,200,...,1000`.

## Session 9
- Clarified the meaning of DP `horizon=16` in the LDP code path.
- Verified in `DiffusionUnetImagePolicy` that `horizon` controls the length of the action trajectory tensor denoised by the diffusion model, while `n_action_steps` controls how many predicted actions are returned for execution during rollout.
- Verified in `RobomimicReplayImageDataset` that the training batch provides a 16-step action sequence when `horizon=16`, with observations truncated to `n_obs_steps`.

## Session 10
- Confirmed GPU host `10.100.16.46:16139` is reachable on 2026-05-08 09:14 UTC, with two idle NVIDIA H200 GPUs.
- Added task-local scheduled DP workspaces for UNet and DiT-style transformer image policies, avoiding edits to the shared LDP source tree.
- Added a task-local launcher for four Square no-history runs: UNet/DiT crossed with LDP-MH and official-PH v1.4.1 datasets.
- Launched the four runs under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/dp_nohist_unet_dit_20260508_0915`; the processes are alive and currently building or waiting on zarr dataset caches.
