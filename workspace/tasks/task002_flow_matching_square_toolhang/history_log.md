# History Log

<!-- METADATA:SESSION=12 -->

## Session 0

- Created task for flow-matching DP baseline experiments on square and tool_hang.
- Planned two variants: full-trajectory `horizon=10` and direct 8-step action-only flow matching.
- Resource assigned: `tingwen_ptp_4gpu_node_96h_49722d42` at `10.100.2.35:33805`.

## Session 1

- Added `FlowMatchingTransformerHybridImagePolicy` with action-space FM training target `noise - action` and fixed-step Euler sampling from noise to action.
- Added four experiment configs: square/tool_hang crossed with full `horizon=10` and direct action-only 8-step policy horizon.
- Fixed transformer workspace sampled-action MSE alignment for `pred_action_steps_only=true`.
- Local syntax check passed for the new policy and touched workspace file; full Hydra check requires the remote training env because local Python lacks hydra.
- Pushed branch `intern_method_developer/task002_flow_matching_square_toolhang` at commit `3914a6b`.
- Synced the pushed worktree from CPU side to GPU node path `/mnt/nfs/tingwen/intern_method_developer/repos/ldp_flow_matching` using `tar | ssh`; avoided GPU-node external network access.
- Linked remote `data` to `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets`.
- Remote `gmp-py310` py_compile passed and all four Hydra configs parsed with `--cfg job`.
- Stopped before smoke/training launch per user handoff request; no GPU training process was started by this session.

## Session 2

- User instructed not to touch the previously assigned GPU node and to switch away from this flow-matching task.
- Performed no GPU, SSH, training, smoke, or remote file operation in this session.
- Recorded handoff status locally for task continuity.

## Session 3

- User provided rules for the next PTP encoder method-development task and confirmed the previous GPU must not be touched.
- Created local documentation structure under `docs/` for global plan tracking and two candidate encoder directions.
- Added `docs/main.md`, `docs/agents.md`, `docs/status.md`, global plan, and per-direction plan/status/experiments/obs_log files.
- Marked both directions as waiting for detailed Direction A / Direction B plans before formal review.
- Performed no GPU, SSH, training, smoke, or remote file operation in this session.

## Session 4

- Answered storage-location question for the new PTP encoder docs.
- Verified `docs/` is located at `/work-agents/intern_method_developer/ldp/docs` on filesystem `overlay` mounted at `/`.
- Noted this is not `/mnt/nfs/tingwen` and not `/mnt/cephfs/home/tinwen.du`; the docs are also committed and pushed to the task branch.
- Performed no GPU, SSH, training, smoke, or remote file operation in this session.

## Session 5

- Saved the user-provided Direction A detailed plan as `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`.
- Added review notes at `docs/direction_a_future_action_contrastive/review_2026-05-18.md`.
- Updated `docs/main.md`, `docs/status.md`, Direction A `status.md`, and Direction A `obs_log.md` to mark Direction A as reviewed but not implemented.
- Main review concerns: exact action-window alignment, condition fusion tensor shape, B2 architecture parity, diagonal masking in soft contrastive loss, action normalization, sigma choice, and frozen/finetune semantics.
- Performed no GPU, SSH, training, smoke, or remote file operation in this session.

## Session 6

- Clarified that "action window" in Direction A means the action segment used as contrastive similarity supervision, not a change to PTP prediction horizon or rollout logic.
- User clarified first Direction A experiments should preserve the proven PTP structure in the robomimic 0.2.0-compatible setup as much as possible.
- Added `docs/direction_a_future_action_contrastive/review_update_ptp_compat_2026-05-18.md`.
- Updated Direction A status, obs log, global docs status, and main docs entry to favor exact-PTP-compatible encoder pretraining rather than policy-side condition concat.
- Performed no GPU, SSH, training, smoke, or remote file operation in this session.

## Session 7

- Saved the user-provided Direction B detailed plan as `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`.
- Added review notes at `docs/direction_b_action_sequence_predictive/review_2026-05-18.md`.
- Updated `docs/main.md`, `docs/status.md`, Direction B `status.md`, and Direction B `obs_log.md` to mark Direction B as reviewed but not implemented.
- Main review recommendation: first-pass Direction B should preserve exact PTP policy structure and use action-sequence prediction only as encoder pretraining.
- Code observations recorded: existing PTP has `obs_encoder_dir` / `obs_encoder_freeze`, `past_action_pred=true` keeps full action trajectory loss, and the dataset returns `n_obs_steps` observations plus an action sequence of length `horizon`.
- Performed no GPU, SSH, training, smoke, or remote file operation in this session.

## Session 8

- Took over PR #1 on branch `intern_method_developer/task002_flow_matching_square_toolhang` from `intern_method_developer`.
- Confirmed assigned GPU node `10.100.2.35:33805` is reachable and has 4 idle H200 GPUs.
- Fixed runtime compatibility issues found by smoke:
  - Added robomimic 0.4 fallback for `CropRandomizer`, which moved from `robomimic.models.base_nets` to `robomimic.models.obs_core`.
  - Removed stale `embedding` entries from the two square raw-image FM dataset configs.
  - Changed transformer workspace to instantiate `env_runner` only when the current training run will actually perform rollout and has rollout init states.
  - Installed missing `threadpoolctl==3.6.0` into the NFS `gmp-py310` env from the CPU/common side.
  - Linked the existing pure-Python `pytorch3d` transforms stub into the NFS `gmp-py310` env.
- Smoke command pattern used 1 epoch, 1 train step, 1 val step, sample MSE enabled, rollout disabled, batch size 2, and raw-image mode.
- Smoke passed for all four configs:
  - `square_h10`: train_loss `1.3324`, val_loss `0.9522`, train_action_mse_error `0.8067`.
  - `square_action8`: train_loss `1.3735`, val_loss `1.3963`, train_action_mse_error `0.7950`.
  - `tool_hang_h10`: train_loss `1.3295`, val_loss `0.9937`, train_action_mse_error `1.0175`.
  - `tool_hang_action8`: train_loss `1.3992`, val_loss `1.3916`, train_action_mse_error `0.7914`.
- Smoke artifacts:
  - outputs: `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/handoff_smoke_20260518_141621`
  - logs: `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/logs/handoff_smoke_20260518_141621`
- Launched four formal training jobs on the 4-GPU node:
  - `square_h10`, GPU 0, launcher pid `115480`.
  - `square_action8`, GPU 1, launcher pid `115487`.
  - `tool_hang_h10`, GPU 2, launcher pid `115494`.
  - `tool_hang_action8`, GPU 3, launcher pid `115501`.
- Formal training artifacts:
  - outputs: `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/formal_train_20260518_143331`
  - logs: `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/logs/formal_train_20260518_143331`
- Formal launch settings: default 3500 epochs and batch size 64 from the configs, `training.rollout_every=999999` to avoid online rollout until env-runner dependencies are repaired, and `checkpoint.topk.k=0` to keep only rolling `latest.ckpt` instead of accumulating top-k checkpoint files.
- Switched to the new user-assigned encoder-method GPU node `10.100.2.4:35140`; verified 8x H200 were idle before launch.
- Checked available envs on that node: `gmp-py310` is usable but has RoboMimic `0.4.0`; the documented py39/RoboMimic `0.2.0` env was not present on this node, so current runs are feasibility probes rather than final release-like evidence.
- Added PTP-compatible encoder pretraining workspace `diffusion_policy/workspace/train_encoder_pretrain_workspace.py`.
- Added encoder pretraining configs for Direction A/B on Square/ToolHang under `experiment_configs/encoder_pretrain/`.
- Fixed raw-image encoder configs by removing stale dataset-side `embedding` keys that caused the dataset converter to read missing `obs/embedding`.
- Fixed Direction A contrastive loss NaN by zeroing diagonal `log_p` after masked `log_softmax`.
- Added `scripts/launch_encoder_pretrain_probe.sh` and `scripts/poll_encoder_pretrain_probe.sh`.
- Passed local `py_compile`, bash syntax checks, and `git diff --check` for code/scripts before committing code commit `7dcc632`.
- Passed remote encoder pretraining smokes on `10.100.2.4`:
  - `B_square_predictive_smoke`: train loss `0.4260`, val loss `0.4002`.
  - `A_square_contrastive_smoke`: train loss `1.2313`, val loss `1.2405` after NaN fix.
  - `B_toolhang_predictive_smoke`: train loss `0.4394`, val loss `0.3929`.
  - `A_toolhang_contrastive_smoke`: train loss `1.3928`, val loss `1.1212`.
- Launched 8 long-running encoder pretraining probes on the 8-H200 node:
  - Direction B: `B_square_full_seed42`, `B_square_future_seed42`, `B_tool_hang_full_seed42`, `B_tool_hang_future_seed42`.
  - Direction A: `A_square_future_seed42`, `A_square_future_seed43`, `A_tool_hang_future_seed42`, `A_tool_hang_future_seed43`.
- Encoder probe logs are tracked at `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/logs/20260518_session8/pids.tsv`.
- Encoder probe outputs and checkpoints are under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8`.

## Session 9

- Checked current GPU usage on the user-assigned encoder node `10.100.2.4:35140`.
- `nvidia-smi` reports all 8 H200 GPUs idle: each has 1 MiB memory used and 0% utilization.
- `scripts/poll_encoder_pretrain_probe.sh` reports all 8 Session 8 probe PIDs exited.
- Verified each run wrote 10 `logs.jsonl` entries and `latest.ckpt` under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8`.
- Direction A final long-run losses:
  - `A_square_future_seed42`: train `3.3737`, val `3.3962`.
  - `A_square_future_seed43`: train `3.3742`, val `3.3965`.
  - `A_tool_hang_future_seed42`: train `2.6360`, val `2.6933`.
  - `A_tool_hang_future_seed43`: train `2.6395`, val `2.6921`.
- Direction B final long-run losses:
  - `B_square_full_seed42`: train `0.0167`, val `0.0373`.
  - `B_square_future_seed42`: train `0.0164`, val `0.0426`.
  - `B_tool_hang_full_seed42`: train `0.0243`, val `0.0494`.
  - `B_tool_hang_future_seed42`: train `0.0252`, val `0.0420`.
- Updated global docs and per-direction status/experiments/obs logs to mark encoder pretraining probes completed, while preserving that there is still no downstream PTP policy score.

## Session 10

- Continued on the user-assigned encoder node `10.100.2.4:35140`; verified all 8 H200 GPUs were initially idle before launch.
- Added downstream launch/poll scripts:
  - `scripts/launch_encoder_downstream_probe.sh`
  - `scripts/launch_encoder_downstream_extra_probe.sh`
  - `scripts/poll_encoder_downstream_probe.sh`
- Validated the exact-PTP downstream entrypoint with a 1-step Square smoke using `B_square_full_seed42` frozen encoder:
  - output: `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_smoke/B_square_full_frozen_smoke_20260519_01`
  - train loss `1.0785`, val loss `1.2045`, train action MSE `0.7062`
- Launched the first downstream matrix under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10` with logs at `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/downstream_logs/20260519_session10`:
  - Square: original finetune, `B_full` frozen, `B_full` finetune, `A_future` finetune
  - ToolHang: original finetune, `B_full` frozen, `B_full` finetune, `A_future` finetune
- Added a second matrix under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session10_extra` with logs at `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/downstream_logs/20260519_session10_extra`:
  - Square: `A_future` frozen, `B_future` frozen, `B_future` finetune, `A_future_seed43` finetune
  - ToolHang: `A_future` frozen, `B_future` frozen, `B_future` finetune, `A_future_seed43` finetune
- Early downstream observations from the latest poll:
  - Main Square at epoch 17-18: original val `0.0965`, `B_full_frozen` `0.0933`, `B_full_finetune` `0.0865`, `A_future_finetune` `0.0866`.
  - Main ToolHang at epoch 6: original val `0.1568`, `B_full_frozen` `0.1585`, `B_full_finetune` `0.1566`, `A_future_finetune` `0.1572`.
  - Extra Square at epoch 7-8: `A_future_frozen` val `0.1001`, `B_future_frozen` `0.1012`, `B_future_finetune` `0.1144`, `A_future_seed43_finetune` `0.1126`.
  - Extra ToolHang at epoch 1-2: `A_future_frozen` val `0.2679`, `B_future_frozen` `0.2668`, `B_future_finetune` `0.2624`, `A_future_seed43_finetune` `0.3481`.
- Interpretation recorded: early downstream train/val diffusion losses are close across encoder choices; the current evidence supports implementation feasibility and running comparisons, but it is not a validated success-rate improvement.
- GPU utilization note: 16 downstream processes are running across the 8-H200 node; raw-image PTP training remains CPU/data-pipeline limited, but all GPUs are occupied by active training processes.

## Session 11

- Polled current downstream status on `10.100.2.4:35140`.
- All 16 Session 10 downstream PTP jobs are still running across the 8-H200 node; `nvidia-smi` reports 16 compute apps.
- Main matrix progress:
  - Square rows are around epoch 38-39.
  - ToolHang rows are around epoch 15-16.
- Extra matrix progress:
  - Square rows are around epoch 28-29.
  - ToolHang rows are around epoch 11-12.
- Latest main Square train/val diffusion losses:
  - original finetune val `0.0735`
  - `B_full_frozen` val `0.0702`
  - `B_full_finetune` val `0.0739`
  - `A_future_finetune` val `0.0758`
- Latest main ToolHang train/val diffusion losses:
  - original finetune val `0.1001`
  - `B_full_frozen` val `0.0943`
  - `B_full_finetune` val `0.1002`
  - `A_future_finetune` val `0.1004`
- Latest extra Square train/val diffusion losses:
  - `A_future_frozen` val `0.0820`
  - `A_future_seed43_finetune` val `0.0768`
  - `B_future_frozen` val `0.0839`
  - `B_future_finetune` val `0.0861`
- Latest extra ToolHang train/val diffusion losses:
  - `A_future_frozen` val `0.1178`
  - `A_future_seed43_finetune` val `0.1206`
  - `B_future_frozen` val `0.1226`
  - `B_future_finetune` val `0.1211`
- Interpretation: early downstream loss has a small favorable signal for `B_full_frozen` on both Square and ToolHang, but this remains train/val diffusion loss only and cannot be treated as rollout success-rate evidence.

## Session 12

- Clarified high-level task progress for the user.
- Both planned encoder directions are being advanced:
  - Direction A: Future-action / behavior contrastive encoder pretraining.
  - Direction B: Action-sequence predictive encoder pretraining.
- Completed high-level work:
  - Saved and reviewed both plans.
  - Implemented exact-PTP-compatible encoder pretraining instead of changing the downstream PTP policy structure.
  - Ran pretraining probes for both directions on Square and ToolHang.
  - Produced compatible encoder checkpoints for Direction A and Direction B.
  - Launched downstream PTP ablations that load those encoders as frozen or finetuned encoders.
- Current experimental focus:
  - Compare Direction B full-action predictive encoder against original PTP encoder.
  - Compare Direction A contrastive encoder as a parallel candidate.
  - Keep PTP policy/head/horizon structure unchanged so the first comparison isolates encoder pretraining as much as possible.
- Latest poll confirmed all 16 downstream jobs are still active on `10.100.2.4:35140`.
- Latest high-level signal:
  - Direction B full-action predictive pretraining has the most interesting early loss signal so far on the main matrix.
  - Direction A remains viable but has not shown a clearly stronger signal than Direction B in the current train/val diffusion-loss view.
  - These are optimization signals only; rollout success-rate evaluation has not been run.
