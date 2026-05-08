# History Log

<!-- METADATA:SESSION=17 -->

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

## Session 11
- Checked DP no-hist progress on 2026-05-08 12:08 UTC. All four main processes are alive: UNet LDP-MH PID `172304`, UNet official-PH PID `172310`, DiT LDP-MH PID `176077`, DiT official-PH PID `176083`.
- GPU state: both H200s have active processes, with about 26.9GB used on GPU0 and 27.1GB used on GPU1.
- Current epoch progress: DiT LDP-MH epoch 38, UNet LDP-MH epoch 35, DiT official-PH epoch 83, UNet official-PH epoch 71.
- Current 50-rollout best scores: DiT LDP-MH epoch 20 `0.04`, UNet LDP-MH epoch 10 `0.04`, DiT official-PH epoch 70 `0.60`, UNet official-PH epoch 70 `0.66`.
- Video saving is working; current mp4 counts are 168, 168, 448, and 392 respectively across the four runs.

## Session 12
- Clarified the data used by the earlier SmolVLA runs.
- `ldp_mh_abs10_seed42` and `ldp_mh_abs10_big384_seed44` used `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5`, a 300-demo, 80,731-step LDP-MH copy from `intern_ldp_explorer`.
- `official_ph_v141_abs10_seed43` used `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_abs_v141.hdf5`, a 200-demo, 30,154-step official-PH v1.4.1 dataset generated in this task.
- Metadata check: the official-PH file has `env_version=1.4.1`; the LDP-MH / intern_ldp_explorer files do not include an explicit `env_version` field in `env_args`.

## Session 13
- Checked accessible GPU resources on 2026-05-08 12:35 UTC.
- Host `10.100.16.46:16139` is reachable and exposes two NVIDIA H200 GPUs with 143,771 MiB each.
- Current usage: GPU0 uses 26,924 MiB and GPU1 uses 27,060 MiB. Four DP no-hist main processes are alive: `172304`, `172310`, `176077`, and `176083`.
- Current experiment progress: UNet LDP-MH epoch 40, DiT LDP-MH epoch 43, UNet official-PH epoch 83, DiT official-PH epoch 99.

## Session 14
- Assessed whether two GPUs are enough to retrain SmolVLA on original/LDP-MH data and official-PH v1.4.1 data for a controlled comparison.
- Historical evidence: on 2026-05-07/08, two H200 GPUs completed three SmolVLA 1000-epoch runs (`ldp_mh_abs10_seed42`, `official_ph_v141_abs10_seed43`, and `ldp_mh_abs10_big384_seed44`), with named checkpoints at `10,20,...,100,200,...,1000`.
- Conclusion: two H200 GPUs are sufficient for the two-run comparison if assigned one SmolVLA run per GPU. They are also sufficient for rollout evaluation, but full 50-rollout evaluation over all 38 named checkpoints would be the longer part and would generate many videos.
- Current caveat: the same two GPUs are actively occupied by four DP no-hist processes, so launching SmolVLA immediately on top of them would share compute even though there is substantial memory headroom.

## Session 15
- Configured the new GPU entry `10.100.16.46:23989` from the existing intern setup path. The new container has `/mnt/3fs2` mounted and `/root/venv` now validates torch 2.5.1+cu124, robosuite 1.4.1, robomimic 0.3.0, mujoco 3.8.0, and 2 visible H200 GPUs.
- Added task-local launcher `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/launch_smolvla_fourway_square.sh` and synced it to the shared task script directory.
- Ran a short SmolVLA smoke train on official-PH v1.4.1 data; it completed 1 epoch, offline eval, and checkpoint writing under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/smolvla_smoke_23989_20260508_125954`.
- Launched four detached SmolVLA 1000-epoch runs under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runs/smolvla_fourway_1000ep_20260508_130111`, with logs under the matching `logs/smolvla_fourway_1000ep_20260508_130111` directory.
- Four launched runs: `smolvla_small_ptp_ldp_mh_abs10_seed52` PID `27745` on GPU0, `smolvla_big384_ptp_ldp_mh_abs10_seed53` PID `27774` on GPU1, `smolvla_big384_official_ph_v141_abs10_seed54` PID `27801` on GPU0, and `smolvla_small_official_ph_v141_abs10_seed55` PID `27816` on GPU1.
- Shared training schedule for the four runs: 1000 epochs, chunk size 16, batch size 128, `ldp_abs10` action representation, AMP, eval/named checkpoint epochs `10,20,...,100,200,...,1000`, and `latest.pt` refresh at eval epochs plus every 25 epochs.

## Session 16
- Checked the four active SmolVLA runs on `10.100.16.46:23989` and confirmed the requested two-task-per-GPU layout is active.
- GPU0 hosts PID `27745` (`smolvla_small_ptp_ldp_mh_abs10_seed52`) and PID `27801` (`smolvla_big384_official_ph_v141_abs10_seed54`); GPU1 hosts PID `27774` (`smolvla_big384_ptp_ldp_mh_abs10_seed53`) and PID `27816` (`smolvla_small_official_ph_v141_abs10_seed55`).
- `nvidia-smi dmon` sampled both H200s at high SM utilization: GPU0 ranged roughly `89%-95%`, GPU1 ranged roughly `94%-99%`, with four compute-app PIDs visible.
- Training is progressing normally: official-PH v1.4.1 runs have crossed epoch 100 and continue training; PTP/LDP-MH runs are around epoch 57 because that dataset has about 599 steps per epoch versus about 223 for official-PH v1.4.1.
- No additional third-per-GPU process was launched because the target was exactly two tasks per card and current SM utilization is already high.

## Session 17
- Rechecked the four SmolVLA training runs on `10.100.16.46:23989` at 2026-05-08 13:24 UTC. All four main PIDs were still alive: `27745`, `27774`, `27801`, and `27816`.
- Latest observed training progress: PTP/LDP-MH small and big384 had reached about epoch 80; official-PH v1.4.1 small and big384 had reached about epoch 200. No run had finished epoch 1000 yet.
- Added `workspace/tasks/task006_eval_official_robomimic_square_bcrnn/scripts/monitor_smolvla_fourway_rollout_best50.sh`, a post-training monitor that waits for all four `epoch_1000.pt` files and no matching training processes before launching rollout.
- Started the post-training monitor on the new GPU host as PID `62177`, with log root `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/logs/smolvla_fourway_rollout_after_train_20260508_132807`.
- The scheduled rollout plan is: all named checkpoints from the four-way run get 20 rollouts each with videos, then the best checkpoint per run is selected by rollout success rate and evaluated with 50 rollouts each. The final report path is `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/reports/smolvla_fourway_rollout_after_train_20260508_132807.md`.
