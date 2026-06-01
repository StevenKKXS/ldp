# History Log

<!-- METADATA:SESSION=21 -->

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

## Session 13

- Continued after the first downstream matrices completed.
- All 16 Session 10 downstream jobs reached 50 epochs and exited cleanly; GPU node was idle before the next launch.
- First completed downstream train/val diffusion-loss summary:
  - Square original best val `0.0711`, last val `0.0739`.
  - Square `A_future_frozen` best val `0.0677`, last val `0.0679`.
  - Square `B_full_frozen` best val `0.0691`, last val `0.0697`.
  - Square `B_future_frozen` best val `0.0700`, last val `0.0702`.
  - Square finetuned rows were close to or worse than original in this loss-only view.
  - ToolHang rows all clustered near best val `0.0636-0.0646`; no meaningful separation appeared in train/val loss.
- Interpretation: Square has a small but consistent-looking loss signal for frozen pretrained encoders, strongest for Direction A frozen and then Direction B frozen. ToolHang has no clear loss signal.
- Added `scripts/run_checkpoint_rollout_eval.py`, a non-interactive checkpoint rollout evaluator that avoids the blocking `IPython.embed()` in `eval.py`.
- Repaired current py310 rollout compatibility enough for a Square 5-step smoke:
  - converted old robosuite part-controller configs such as `OSC_POSE` into robosuite 1.5 composite controller configs in `RobomimicImageRunner`;
  - disabled shared memory in `AsyncVectorEnv` for custom observation spaces;
  - updated `AsyncVectorEnv` reset/concatenate compatibility for gym 0.23.
- Rollout smoke command on Square original latest checkpoint completed and wrote `test/mean_score: 0.0` for a 5-step single-test rollout. This validates env-runner execution only; it is not a method score.
- Launched seed-43 downstream repeat matrix to test robustness while rollout evaluation is being prepared:
  - Square: original finetune, `A_future_frozen`, `B_full_frozen`, `B_future_frozen`.
  - ToolHang: original finetune, `A_future_frozen`, `B_full_frozen`, `B_full_finetune`.
  - Logs: `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/downstream_logs/20260519_session13_seed43/pids.tsv`.
  - Outputs: `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/downstream_runs/20260519_session13_seed43`.
- Latest seed-43 poll: all 8 repeat jobs are running across the 8-H200 node; Square rows are around epoch 5-6 and ToolHang rows around epoch 1.

## Session 14

- Checked and clarified RoboMimic / environment versions for the user.
- Current active GPU node `10.100.2.4:35140` uses env `/mnt/nfs/tingwen/ldp/envs/gmp_released_ckpt/miniforge3/envs/gmp-py310`.
- Confirmed current env versions:
  - RoboMimic `0.4.0`
  - RoboSuite `1.5.1`
  - Gym `0.23.1`
  - Torch `2.8.0+cu128`
  - Diffusers `0.33.1`
- Important interpretation: current downstream and rollout-smoke results are not from the target release-like RoboMimic `0.2.0` stack.
- The documented closer release-like py39 environment is in `workspace/shared/ldp_ptp_py39_h200_environment.md`; it records Python 3.9, RoboMimic `0.2.0`, and RoboSuite source version `1.2.0`.
- Current plan implication: keep using `10.100.2.4` results for feasibility, loss ablations, and code path debugging; use the py39/RoboMimic `0.2.0` stack for final rollout-level evidence when available.

## Session 15

- Clarified high-level progress beyond environment setup.
- Direction A has progressed through:
  - plan review;
  - exact-PTP-compatible future-action contrastive encoder pretraining;
  - Square and ToolHang pretraining probes;
  - downstream exact-PTP frozen/finetune ablation.
- Direction B has progressed through:
  - plan review;
  - exact-PTP-compatible action-sequence predictive encoder pretraining;
  - full-action and future-only pretraining probes;
  - downstream exact-PTP frozen/finetune ablation.
- First completed 50-epoch downstream matrix result:
  - Square original best val `0.0711`.
  - Square `A_future_frozen` best val `0.0677`, currently the strongest loss-only row.
  - Square `B_full_frozen` best val `0.0691`, also positive versus original.
  - Square `B_future_frozen` best val `0.0700`, mildly positive versus original.
  - ToolHang rows clustered around best val `0.0636-0.0646`, so no meaningful method separation appeared.
- Rollout path status:
  - Added non-interactive rollout eval script.
  - Repaired py310 env-runner compatibility enough for a 5-step Square rollout smoke to complete.
  - No formal rollout success-rate comparison has been run.
- Current active work:
  - Seed-43 repeat matrix is running with 8 active jobs on `10.100.2.4:35140`.
  - Current Square repeat around epoch 35: original val `0.0756`, `A_future_frozen` `0.0731`, `B_full_frozen` `0.0731`, `B_future_frozen` `0.0735`.
  - Current ToolHang repeat around epoch 14: original val `0.1024`, `A_future_frozen` `0.1038`, `B_full_frozen` `0.1012`, `B_full_finetune` `0.1021`; rows remain close.
- Interpretation: the main experimental signal so far is Square frozen encoder pretraining, with Direction A and Direction B both viable in loss-only metrics. ToolHang has not shown a clear benefit.

## Session 16

- Provided a concise user-facing explanation of the two encoder plans and connected them to current results.
- Plan A meaning:
  - Future-action / behavior contrastive encoder pretraining.
  - It trains the encoder so histories with similar future expert action chunks have nearby embeddings, and histories with different future behavior are separated.
  - Downstream PTP policy structure is unchanged; only the encoder checkpoint is loaded and either frozen or finetuned.
- Plan B meaning:
  - Action-sequence predictive encoder pretraining.
  - It trains the encoder with a lightweight decoder to predict expert action sequences, then discards the decoder and loads only the encoder into PTP.
  - Tested variants include full-action target and future-only target.
- Current result summary:
  - First seed Square: original best val `0.0711`, Plan A `A_future_frozen` `0.0677`, Plan B `B_full_frozen` `0.0691`, Plan B `B_future_frozen` `0.0700`.
  - Seed-43 Square repeat completed: original best val `0.0692`, Plan A `A_future_frozen` `0.0640`, Plan B `B_full_frozen` `0.0659`, Plan B `B_future_frozen` `0.0662`.
  - ToolHang first seed was essentially tied around best val `0.0636-0.0646`.
  - ToolHang seed-43 repeat is still running and remains close across rows so far.
- Current interpretation:
  - Plan A frozen is currently the strongest loss-only candidate on Square.
  - Plan B full frozen is also consistently better than original on Square, but weaker than Plan A frozen in the two Square seeds.
  - ToolHang has no clear method signal yet.
  - No formal rollout success-rate comparison has been completed.

## Session 17

- Checked the current GPU resource state for the active encoder-method allocation.
- Active managed node:
  - SSH: `10.100.2.4:35140`
  - Hostname: `lg-cmc-b7r201-c08u06-h200-000067`
  - GPUs: 8x NVIDIA H200
  - Per-GPU memory: `143771 MiB`
  - Current usage: each GPU reports `1 MiB / 143771 MiB` and `0%` utilization.
  - Compute apps: none reported by `nvidia-smi`.
- All 8 seed-43 downstream repeat jobs under `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/downstream_logs/20260519_session13_seed43` have exited cleanly.
- Final seed-43 last validation losses from the poll:
  - `square_original_finetune_s43`: epoch 49, val `0.07197584211826324`.
  - `square_A_future_frozen_s43`: epoch 49, val `0.0668635219335556`.
  - `square_B_full_frozen_s43`: epoch 49, val `0.06879491358995438`.
  - `square_B_future_frozen_s43`: epoch 49, val `0.06895673274993896`.
  - `tool_hang_original_finetune_s43`: epoch 49, val `0.07313244789838791`.
  - `tool_hang_A_future_frozen_s43`: epoch 49, val `0.07459280639886856`.
  - `tool_hang_B_full_frozen_s43`: epoch 49, val `0.07380388677120209`.
  - `tool_hang_B_full_finetune_s43`: epoch 49, val `0.07351262867450714`.
- Resource boundary:
  - Historical flow-matching node `10.100.2.35:33805` was not touched because the user instructed not to use the earlier GPU.
  - Documented py39/RoboMimic `0.2.0` host `10.100.0.29:36645` remains a recorded release-like environment reference, not an active allocation verified in this session.

## Session 18

- Checked current task progress for the user.
- Progress summary:
  - Direction A, future-action contrastive encoder pretraining, has been implemented, pretrained on Square/ToolHang, and evaluated through exact-PTP downstream loss ablations.
  - Direction B, action-sequence predictive encoder pretraining, has been implemented, pretrained with full-action and future-only variants, and evaluated through exact-PTP downstream loss ablations.
  - Square shows a repeatable loss-only benefit for frozen pretrained encoders across two seeds; Plan A frozen is the strongest current row.
  - ToolHang remains close across methods and does not yet show a clear method signal.
  - Formal rollout success-rate comparison has not been completed; only a short Square rollout smoke was completed earlier to validate the evaluator path.
- Checked current GPU reachability:
  - SSH probe: `ssh -o BatchMode=yes -o ConnectTimeout=10 -p 35140 10.100.2.4 ...`
  - Result: `Connection refused`.
  - Raw TCP probe via `/dev/tcp/10.100.2.4/35140` also returned `Connection refused`.
- Current resource interpretation:
  - The previously active encoder-method GPU endpoint `10.100.2.4:35140` is not reachable now.
  - No current GPU process state can be confirmed from that endpoint.
  - Historical node `10.100.2.35:33805` was not touched, following the user's prior instruction.

## Session 19

- Tested the new user-provided GPU endpoint:
  - SSH: `root@10.100.2.50 -p 26953`
  - Hostname: `lg-cmc-b7r201-e07u16-h200-000113`
  - GPU: 1x NVIDIA H200, idle before and after benchmark.
  - `/dev/shm`: 256G, with only 12K used before benchmark.
  - CPU count: 192.
  - System memory: about 2.0TiB.
  - `ulimit -n`: 1024.
- Environment note:
  - Existing ceph repo path found at `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/repos/ldp`.
  - Existing ceph py39 env path found at `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph`.
  - That env is incomplete on this node because `bin/python` points to missing `/usr/bin/python3.9`.
  - System Python has PyTorch `2.7.0a0+ecf3bae40a.nv25.02` and torchvision `0.22.0a0`, but does not have `h5py`.
  - Therefore the worker test used system PyTorch synthetic robomimic-like batches instead of the real HDF5 dataset.
- Synthetic shared-memory/collate hard-limit test:
  - Batch shape approximated raw-image PTP batches: batch size 64, two RGB camera views, two observation frames, low-dim state, and action horizon 32.
  - `num_workers=224` opened and iterated successfully, with PyTorch warning that the suggested max worker count is 192.
  - `num_workers=256` failed with `OSError(24, Too many open files)`.
  - Interpretation: `/dev/shm=256G` is not the active limit; the current file descriptor limit is.
- ColorJitter-like benchmark:
  - Tested raw-image-like samples with torchvision `ColorJitter`, batch size 64, `pin_memory=True`, `persistent_workers=False`, `prefetch_factor=2`.
  - 8 workers: about `12.447` total batches/s for 8 batches; after first batch about `24.705` batches/s.
  - 12 workers: about `12.411` total batches/s; after first batch about `36.662` batches/s.
  - 16 workers: about `11.297` total batches/s; after first batch about `28.878` batches/s.
  - 24 workers: about `7.332` total batches/s.
  - 32 workers: about `8.037` total batches/s.
  - 48 workers: about `3.688` total batches/s.
  - 64 workers: about `2.667` total batches/s.
  - 96 workers: about `1.506` total batches/s.
  - 128, 160, 192, and 224 workers also opened with the transform benchmark but were slow due to startup and process overhead.
- Practical conclusion:
  - Start real raw-image training with `num_workers=8` or `12`.
  - Use `16` as a conservative high setting if GPU utilization still starves.
  - Do not use `64+` for this PTP-style pipeline unless a different profiling run proves it helps.
  - `224` is the observed process-open ceiling; it is not a useful throughput setting.

## Session 20

- Recorded code path, branch, and workflow for user inspection.
- Current review source:
  - Local repo: `/work-agents/intern_method_developer/ldp`
  - Branch: `intern_method_developer/task002_flow_matching_square_toolhang`
  - Remote: `git@github.com:StevenKKXS/ldp.git`
  - Latest commit before this documentation update: `7911914 Record dataloader worker benchmark`
  - PR: `https://github.com/StevenKKXS/ldp/pull/1`
- Historical GPU-side code paths used by earlier runs:
  - Encoder probes: `/mnt/nfs/tingwen/intern_method_developer/repos/ldp_encoder_probe`
  - Flow-matching probes: `/mnt/nfs/tingwen/intern_method_developer/repos/ldp_flow_matching`
  - New node `10.100.2.50:26953` did not have a verified synced copy of this active branch; only a separate ceph repo was found under `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/repos/ldp`, and that directory was not a git checkout on the node.
- Encoder pretraining workflow:
  - Entry: `train.py`
  - Workspace: `diffusion_policy/workspace/train_encoder_pretrain_workspace.py`
  - Configs: `experiment_configs/encoder_pretrain/{predictive_square,contrastive_square,predictive_tool_hang,contrastive_tool_hang}.yaml`
  - Launcher: `scripts/launch_encoder_pretrain_probe.sh`
  - Dataset: `RobomimicReplayImageDataset` reads `image_abs.hdf5`, builds an in-memory replay buffer, samples sequences, returns `batch["obs"]` and `batch["action"]`.
  - Model: instantiate PTP `DiffusionTransformerHybridImagePolicy`, keep only `policy.obs_encoder`, wrap it with `EncoderPretrainModel`.
  - Direction B predictive loss: normalize obs/action, encode obs, pool features, MLP predicts selected normalized action sequence, optimize Smooth L1.
  - Direction A contrastive loss: normalize obs/action, encode obs, project embedding, compute pairwise normalized future-action distance, match embedding similarity distribution using soft contrastive CE.
  - Checkpoint: `save_encoder_checkpoint()` writes only obs encoder weights under `state_dicts.model` with `obs_encoder.*` keys plus pretrain metadata.
- Downstream exact-PTP workflow:
  - Entry: `train.py`
  - Workspace: `diffusion_policy/workspace/train_diffusion_transformer_hybrid_workspace.py`
  - Policy: `diffusion_policy/policy/diffusion_transformer_hybrid_image_policy.py`
  - Configs: `experiment_configs/square/transformer_square.yaml` and `experiment_configs/tool/transformer_tool_hang.yaml`
  - Launchers: `scripts/launch_encoder_downstream_probe.sh`, `scripts/launch_encoder_downstream_extra_probe.sh`, `scripts/launch_encoder_downstream_seed43_probe.sh`
  - Encoder loading: `obs_encoder_dir=<checkpoint>` causes `DiffusionTransformerHybridImagePolicy` to load `obs_encoder.*` weights; `obs_encoder_freeze=true/false` controls frozen versus finetuned ablation.
  - Training signal: downstream PTP still uses DDPM policy loss with `past_action_pred=true`; rollout was disabled in the loss ablations with `training.rollout_every=999999`.
- Flow-matching workflow on this branch:
  - Policy: `diffusion_policy/policy/flow_matching_transformer_hybrid_image_policy.py`
  - Configs: `experiment_configs/square/flow_transformer_square_{h10,action8}.yaml` and `experiment_configs/tool/flow_transformer_tool_hang_{h10,action8}.yaml`
  - Data flow: same robomimic image dataset and obs encoder condition path as transformer DP; normalized action trajectory is noised by `x_t=t*noise+(1-t)*action`; transformer predicts velocity `noise-action`; inference integrates from noise to action with Euler steps.
- Important training-review point:
  - Encoder pretraining configs currently use `global_obs=16,horizon=32,n_action_steps=8`.
  - Downstream exact PTP configs use Square `global_obs=2,horizon=32,n_action_steps=1` and ToolHang `global_obs=2,horizon=16,n_action_steps=8`.
  - This means downstream policy structure was kept exact, but the pretraining input horizon is not identical to downstream PTP observation length. This is the first thing to inspect if strict PTP-structure matching is required.

## Session 21

- Answered the user's question about Superpowers skill scoping.
- Observed local skill-related paths:
  - Codex native installed skills are under `/root/.codex/skills`; current available system skills are in `/root/.codex/skills/.system`.
  - The Superpowers plugin payload exists under `/root/.codex/.tmp/plugins/plugins/superpowers`, with skill directories under `/root/.codex/.tmp/plugins/plugins/superpowers/skills`.
  - This intern agent has an agent-local helper skill directory at `/work-agents/intern_method_developer/.agents/skills`, currently containing Feishu skill symlinks.
  - Other intern agents have separate `.agents/skills` directories under `/work-agents/<agent>/.agents/skills`.
  - `/work-agents/intern_method_developer/.codex/config.toml` is a symlink to shared `/work-agents/.github/codex_settings.toml`.
- Scope explanation recorded:
  - Native Codex skills are scoped by the `CODEX_HOME` used when the Codex process starts; with default home, installing into `/root/.codex/skills` affects all sessions sharing that home after restart.
  - Agent-local scope can be achieved by using `/work-agents/<agent>/.agents/skills` for harness/helper skills, or by launching that specific agent with a private `CODEX_HOME` and installing Codex skills there.
  - Workspace-only scope requires a workspace-local skill directory and explicit loader/start-hook support. Creating repo-local skill files alone is not sufficient if the session loader never imports that path.
- No Superpowers skills were installed or symlinked in this session.
