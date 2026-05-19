# History Log

<!-- METADATA:SESSION=25 -->

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

## Session 9

- Checked GPU node `10.100.2.35:33805` at `2026-05-18T22:40:48+00:00`.
- All four formal training jobs were still alive:
  - `square_h10`: GPU 0, pid `115485`, 2284 MiB, instantaneous GPU util 49%, latest metric epoch 299, train_loss `0.0178`.
  - `square_action8`: GPU 1, pid `115492`, 2276 MiB, instantaneous GPU util 58%, latest metric epoch 298, train_loss `0.0219`.
  - `tool_hang_h10`: GPU 2, pid `115500`, 8746 MiB, instantaneous GPU util 53%, latest metric epoch 40, train_loss `0.0406`.
  - `tool_hang_action8`: GPU 3, pid `115506`, 8742 MiB, instantaneous GPU util 0%, latest metric epoch 40, train_loss `0.0790`; log showed it was in validation epoch 40 during the snapshot.
- Confirmed ToolHang cache construction had completed because both ToolHang jobs had entered training/validation.

## Session 10

- Checked GPU node `10.100.2.35:33805` at `2026-05-19T02:58:12+00:00`.
- All four formal training jobs were still alive after about 12h25m runtime:
  - `square_h10`: GPU 0, pid `115485`, 2284 MiB, instantaneous GPU util 23%, latest metric epoch 459, train_loss `0.0137`.
  - `square_action8`: GPU 1, pid `115492`, 2276 MiB, instantaneous GPU util 0%, latest metric epoch 457, train_loss `0.0157`.
  - `tool_hang_h10`: GPU 2, pid `115500`, 8746 MiB, instantaneous GPU util 0%, latest metric epoch 64, train_loss `0.0397`.
  - `tool_hang_action8`: GPU 3, pid `115506`, 8742 MiB, instantaneous GPU util 0%, latest metric epoch 64, train_loss `0.0942`.
- Confirmed `latest.ckpt` existed for all four runs:
  - `square_h10`: `2026-05-19 01:22`, 681963039 bytes.
  - `square_action8`: `2026-05-19 01:25`, 681954591 bytes.
  - `tool_hang_h10`: `2026-05-19 02:09`, 681965791 bytes.
  - `tool_hang_action8`: `2026-05-19 02:10`, 681957343 bytes.
- No traceback, killed process, or exception marker was found in the latest progress grep.

## Session 11

- User asked whether current Square checkpoints already show rollout effect without waiting for 3500 epochs.
- Prepared Square rollout on GPU node `10.100.2.35:33805` using current saved `latest.ckpt` files:
  - `square_h10`: `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/formal_train_20260518_143331/square_h10/checkpoints/latest.ckpt`
  - `square_action8`: `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/formal_train_20260518_143331/square_action8/checkpoints/latest.ckpt`
- Added missing rollout runtime dependencies to the shared NFS `gmp-py310` env from the CPU/common side, not through GPU-node network:
  - installed `gym==0.23.1`;
  - installed `opencv-python-headless==4.11.0.86`;
  - downloaded/extracted Ubuntu Noble GLVND packages under `/mnt/nfs/tingwen/ldp/small_files/intern_ldp_explorer/system_libs/noble_extract`;
  - linked `libEGL.so`, `libGL.so`, `libGLX.so.0`, and `libGLdispatch.so.0` into the NFS env lib directory.
- Used evaluation-time compatibility shims for the GMP robosuite 1.5 / gym 0.23 environment:
  - converted legacy robomimic `OSC_POSE` controller metadata to robosuite 1.5 `BASIC` composite controller metadata;
  - disabled `AsyncVectorEnv` shared memory for Gym Dict observations;
  - adapted `AsyncVectorEnv.reset`, `step`, and `concatenate` calls to gym 0.23 signatures.
- Ran 10 test-seed Square rollouts:
  - `square_h10_n10`: `test/mean_score = 0.0`, all 10 seeds reward 0.0.
  - `square_action8_n10_reward_only`: `test/mean_score = 0.0`, all 10 seeds reward 0.0.
- Rollout artifacts:
  - `square_h10`: `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/rollout_square_eval_20260519_0309/square_h10_n10/eval_log.json`
  - `square_action8`: `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/rollout_square_eval_20260519_0309/square_action8_n10_reward_only/eval_log.json`
- The standard runner's extra action-HSIC logging path is not robust for `square_action8` ragged action chunks, so the score was collected with a reward-only rollout loop using the same env, policy, checkpoint, and seeds.

## Session 12

- Checked the active Python environments for `robomimic` version.
- Local default Python in `/work-agents/intern_ldp_explorer` does not have `robomimic` installed.
- The NFS/GPU environment used for training and rollout is `/mnt/nfs/tingwen/ldp/envs/gmp_released_ckpt/miniforge3/envs/gmp-py310/bin/python`.
- That active environment imports `robomimic 0.4.0` from `/mnt/nfs/tingwen/ldp/small_files/intern_ldp_explorer/vendor/gmp/gated-memory-policy/mujoco-env/third_party/robomimic/robomimic/__init__.py`.

## Session 13

- User required switching future PTP-data work back to the native PTP-style Python 3.9 environment with `robomimic==0.2.0`, because the PTP datasets were prepared for that version family.
- Checked current FM GPU node `10.100.2.35:33805`: `/root/ptp_ldp_py39/bin/python` is missing.
- Checked old py39 note host `10.100.0.29:36645`: SSH connection was refused, so the old ready-env record is stale.
- Searched NFS/3FS paths for a ready py39 / `robomimic==0.2.0` environment; found prior py39 logs/scripts and outputs, but no ready reusable env under `/mnt/nfs/tingwen/ldp/envs`.
- Recorded the environment rule in `workspace/interns/intern_ldp_explorer/knowledge.md`, `workspace/ERROR_BOOK.md`, `workspace/shared/ldp_ptp_py39_h200_environment.md`, task knowledge, and encoder experiment docs.
- Marked the current `gmp-py310` / `robomimic 0.4.0` FM runs as version-confounded for PTP-data reproduction; before launching any new trusted training or rollout, rebuild or sync a verified Python 3.9 + `robomimic==0.2.0` environment from CPU/common storage.
- Stopped the remaining `formal_train_20260518_143331` `gmp-py310` training processes on `10.100.2.35:33805`; after termination, `nvidia-smi` showed GPUs 0-3 at 1 MiB used and 0% utilization.

## Session 14

- Built a reusable NFS conda env at `/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020` from the CPU/common side and verified it on GPU node `10.100.2.35:33805`.
- Verified core versions on the GPU node: Python `3.9.23`, `robomimic 0.2.0`, `robosuite 1.2.0`, `mujoco-py 2.1.2.14`, `gym 0.21.0`, `torch 2.5.1`, CUDA available on H200.
- Used MuJoCo runtime `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runtimes/mujoco210` with `MUJOCO_GL=egl` and `PYOPENGL_PLATFORM=egl`.
- Installed GPU-node system render/build deps from the internal apt mirror so `mujoco_py` could compile under py39.
- Patched `diffusion_policy/policy/diffusion_transformer_hybrid_image_policy.py` so `CropRandomizer` lookup works with both robomimic 0.2.0 (`base_nets`) and robomimic 0.4.0 (`obs_core`).
- Added `eval_flow_matching_rollout.py`, a reward-only rollout evaluator that loads the current workspace checkpoint and avoids the standard runner's action-HSIC / wandb logging path.
- Smoke checks passed:
  - imported FM policy, RobomimicImageRunner, and RobomimicReplayImageDataset under py39 / robomimic 0.2.0;
  - `square_h10` 1-seed smoke completed in NutAssemblySquare;
  - `tool_hang_h10` 1-seed smoke completed in ToolHang.
- Ran current `formal_train_20260518_143331/latest.ckpt` rollouts with `ema_model`, reward-only, no videos:
  - Square h10: `7/10`, mean score `0.7`, output `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/rollout_square_eval_py39_rm020_20260519_122543/square_h10_n10/eval_log.json`.
  - Square action8: `4/10`, mean score `0.4`, output `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/rollout_square_eval_py39_rm020_20260519_122543/square_action8_n10/eval_log.json`.
  - ToolHang h10: `0/10`, mean score `0.0`, output `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/rollout_toolhang_eval_py39_rm020_20260519_122543/tool_hang_h10_n10/eval_log.json`.
  - ToolHang action8: `0/10`, mean score `0.0`, output `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/outputs/rollout_toolhang_eval_py39_rm020_20260519_122543/tool_hang_action8_n10/eval_log.json`.
- After rollout completion, `nvidia-smi` showed GPUs 0-3 at 1 MiB used and 0% utilization; no eval process remained.

## Session 15

- User asked whether original PTP normalizes action and proprio.
- Checked `diffusion_policy/dataset/robomimic_replay_image_dataset.py`, `diffusion_policy/common/normalize_util.py`, `diffusion_policy/policy/diffusion_transformer_hybrid_image_policy.py`, and original transformer configs for Square, Transport, and ALOHA.
- Confirmed the original PTP image policy fits a dataset normalizer in the workspace, loads it into both model and EMA model, normalizes observations/actions during training, normalizes observations during rollout, and unnormalizes predicted actions before environment stepping.
- Confirmed robomimic `abs_action: true` configs normalize only absolute action position dimensions to `[-1,1]`; non-position action dimensions are identity. Dual-arm transport applies the same rule per arm.
- Confirmed robomimic proprio is field-wise: `robot*_eef_pos` and `robot*_gripper_qpos` are range-normalized to `[-1,1]`, while `robot*_eef_quat` is identity because it is already bounded.
- Confirmed `abs_action: false` configs use identity action normalization because actions are treated as already normalized.

## Session 16

- User asked whether PTP dataloader can fetch current-to-history observations and history-to-future actions.
- Checked `SequenceSampler` and `RobomimicReplayImageDataset.__getitem__`.
- Confirmed `SequenceSampler` creates a fixed contiguous sequence window with episode-boundary repetition padding controlled by `pad_before` and `pad_after`.
- Confirmed robomimic image dataset loads only the first `n_obs_steps * subsample_frames` tokens for obs keys via `key_first_k`, then returns `obs[key]` as the selected historical obs tokens.
- Confirmed action returns a composed sequence: subsampled historical action tokens from the obs window plus all future action tokens, producing `batch['action']` length `horizon`.
- With `subsample_frames=1`, setting `n_obs_steps=K+1` and `horizon=K+1+F` gives obs offsets `[-K, ..., 0]` and action offsets `[-K, ..., F]` relative to the current frame at index `n_obs_steps-1`.
- For fixed windows this is easy and mostly config-level; arbitrary nonuniform frame sets or separate named obs/action ranges require a small dataset/sampler extension.

## Session 17

- User asked whether dataloader observations are encoder outputs or raw images.
- Checked `RobomimicReplayImageDataset.__init__`, `RobomimicReplayImageDataset.__getitem__`, `LinearNormalizer`, and `DiffusionTransformerHybridImagePolicy`.
- Confirmed normal image configs return raw image tensors in `obs['agentview_image']`, `obs['robot0_eye_in_hand_image']`, plus low-dim proprio tensors; images are converted from HWC uint8 to CHW float in `[0,1]`.
- Confirmed policy-side code then normalizes obs and calls `self.obs_encoder(this_nobs)` during training and rollout.
- Confirmed embedding-cache mode is separate: if `use_embed_if_present=True` and the replay buffer contains `embedding`, the sampler loads only `embedding` and `action`, and `__getitem__` returns `obs['embedding']` instead of raw image/proprio keys.
- Confirmed the normalizer intentionally skips `embedding`, and policy uses `batch['obs']['embedding']` directly as condition when embedding mode is active.

## Session 18

- User asked current Flow Matching progress and whether it can be stopped.
- Checked GPU node `10.100.2.35:33805`: all four H200 GPUs were idle at 1 MiB used and 0% utilization, with no `flow_matching`, `train.py`, `eval_flow_matching`, `diffusion_policy`, or Python training/eval process found.
- Checked `formal_train_20260518_143331` logs:
  - `square_h10` latest log line at epoch `788`, global step `973291`, train loss `0.0223`;
  - `square_action8` latest log line at epoch `786`, global step `970838`, train loss `0.0100`;
  - `tool_hang_h10` latest log line at epoch `115`, global step `168850`, train loss `0.0324`;
  - `tool_hang_action8` latest log line at epoch `115`, global step `168391`, train loss `0.0319`.
- Confirmed latest checkpoints exist for all four formal runs under `formal_train_20260518_143331/*/checkpoints/latest.ckpt`.
- Reconfirmed py39 / `robomimic 0.2.0` reward-only rollout results from current checkpoints: Square h10 `7/10`, Square action8 `4/10`, ToolHang h10 `0/10`, ToolHang action8 `0/10`.
- Conclusion recorded for handoff: the current FM GPU work can stay stopped and the GPU can be released; if continuing FM seriously, restart clean training in the py39 / `robomimic 0.2.0` environment rather than extending the old gmp-py310 / `robomimic 0.4.0` run.

## Session 19

- User handed off a new Behavior Translator experiment idea and asked for feasibility review plus an updated experiment plan before implementation.
- Created Direction C documentation under `docs/direction_c_behavior_translator/`.
- Main feasibility correction: current PTP dataloader normally returns raw image/proprio tensors, not camera embeddings, so the v0 plan should use `raw obs history -> existing robomimic obs_encoder -> obs feature tokens -> BehaviorTranslator`.
- Main scope correction: do not connect DP/PTP in the first implementation; first deliver Stage 1 offline translation and Stage 2a frozen-head probe.
- Main go/no-go criterion: frozen pretrained translator context must outperform frozen random translator context before DP/PTP integration.
- Updated `docs/main.md` and `docs/status.md` to include Direction C.
- Planned first implementation step: build `BehaviorTranslationDataset`, `BehaviorTranslator`, and one Square history->past+future config, then run shape and forward/backward smoke checks in the py39 / `robomimic 0.2.0` environment.

## Session 20

- User clarified ownership: `intern_ldp_explorer` should mainly own Direction C; Direction A/B are handled by another intern.
- Updated `docs/main.md`, `docs/status.md`, `docs/direction_c_behavior_translator/status.md`, and `docs/direction_c_behavior_translator/obs_log.md` to reflect that Direction C is the active execution queue for this agent.
- Preserved Direction A/B docs as references, but marked them outside this agent's execution queue.
- Current Direction C next implementation unit remains: `BehaviorTranslationDataset`, `BehaviorTranslator`, and one Square history->past+future config, followed by shape and forward/backward smoke checks in py39 / `robomimic 0.2.0`.

## Session 21

- User asked whether Stage 1 translator training can be completed first and requested the intended training plan.
- Added `docs/direction_c_behavior_translator/stage1_training_plan_2026-05-19.md`.
- Selected the first Stage 1 run as Square `C1-T3-square-history-past-future`.
- Planned horizons: obs history `H=16`, past action `P=16`, future action `K=8`.
- Corrected the dataset slicing plan: for `H=P=16`, use sequence offsets `0...23`, obs offsets `1...16`, past action offsets `0...15`, and future action offsets `16...23`, so current action is not included in the past target.
- Planned to train the robomimic obs encoder together with the BehaviorTranslator for Stage 1, because the default dataloader returns raw images/proprio and freezing a random obs encoder would not test the intended representation.
- Planned optimization: smoke with batch `8` and max `20` train steps, then first Square run with batch `32`, AdamW lr `1e-4`, weight decay `1e-4`, grad clip `1.0`, `20` epochs, best checkpoint by `val/future_l1`.

## Session 22

- User requested three Stage 1 translator objectives for comparison: obs history -> past actions, obs history -> future actions, and obs history -> past+future actions.
- Implemented `diffusion_policy/dataset/behavior_translation_dataset.py` with explicit anchor slicing and edge-padding-compatible sampling over the existing robomimic replay dataset.
- Implemented `diffusion_policy/model/behavior_translator.py` with obs projection, causal Transformer obs encoder, action-query Transformer decoder, sketch action head, and context projector.
- Implemented `diffusion_policy/workspace/train_behavior_translator_workspace.py` to train the robomimic obs encoder jointly with the BehaviorTranslator, normalize actions with the PTP dataset normalizer, log eval metrics, save `latest`/`best`, and save periodic checkpoints.
- Added three Square configs:
  - `experiment_configs/square/behavior_translator_square_past.yaml`
  - `experiment_configs/square/behavior_translator_square_future.yaml`
  - `experiment_configs/square/behavior_translator_square_past_future.yaml`
- Set all three configs to `1000` epochs, batch `32`, AdamW lr `1e-4`, checkpoint every `50` epochs, and monitor `val/loss_total`.
- Patched `RobomimicReplayImageDataset` so the optional `expert_actions_corr` MLP diagnostic is skipped unless explicitly requested and CUDA is available; this makes CPU-side dataset smoke possible.
- Verification passed:
  - `py_compile` for new dataset/model/workspace and patched robomimic dataset;
  - Hydra `--cfg job` parse for all three configs;
  - dataset shape smoke for Square: obs history length `16`, `act_past` `[16,10]`, `act_future` `[8,10]`;
  - CPU one-step forward/backward smoke for `past_future`, which wrote `latest.ckpt`, `best.ckpt`, `logs.json.txt`, `metrics.csv`, and `env.json`.

## Session 23

- User provided new GPU endpoint `10.100.2.35:25076` for Direction C Stage 1 translator training.
- Verified the node is reachable as `lg-cmc-b7r201-e02u16-h200-000098`, with 4 H200 GPUs idle, `/mnt/nfs` and `/mnt/3fs2` mounted, and `/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020/bin/python` importing torch `2.5.1+cu124` and `robomimic 0.2.0`.
- Synced local branch commit `cf95686` to `/mnt/nfs/tingwen/intern_ldp_explorer/repos/ldp_behavior_translator` without using GPU-node network access.
- Ran a GPU smoke for `behavior_translator_square_past_future` on GPU0 with 1 epoch, 2 train steps, 1 val batch, batch size 2; it completed and wrote `best.ckpt`, `latest.ckpt`, `metrics.csv`, `logs.json.txt`, and `env.json` under `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/smoke/gpu_smoke_20260519_142812`.
- Launched the formal Square Stage 1 comparison set under `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage1_square_20260519_143020`:
  - `past`: GPU0, pid `26881`, config `behavior_translator_square_past`.
  - `future`: GPU1, pid `26883`, config `behavior_translator_square_future`.
  - `past_future`: GPU2, pid `26885`, config `behavior_translator_square_past_future`.
- Confirmed all three jobs entered epoch 1. Snapshot after launch showed GPUs 0/1/2 each using about 5.3GB; GPU1/GPU2 instantaneous utilization was about 83%/86%, and GPU0 had an alive training process while the utilization sample was 0%.
- First two launch attempts did not enter training: one used shell variable `ENV`, which conflicted with the node's shell initialization, and one used nested local SSH quotes that stripped remote variables. The working launch used `ssh ... 'bash -s' <<'REMOTE'` and a non-conflicting `PY39` variable.

## Session 24

- User asked how long the three Direction C Stage 1 Square translator jobs will take.
- Checked `10.100.2.35:25076` at `2026-05-19T14:35:48+00:00`: pids `26881`, `26883`, and `26885` were all alive in epoch 1.
- GPU snapshot: GPU0 `5312 MiB`, GPU1 `5308 MiB`, GPU2 `5312 MiB`, GPU3 idle.
- Live tqdm progress showed roughly 2.6-2.7 train batches/sec over `2478` train batches per epoch, so one train epoch is about 15-16 minutes before small validation/checkpoint overhead.
- Estimated wall time with the current 1000-epoch configs: about 10.5-12 days if uninterrupted. A 96h allocation should cover about 340-380 epochs, not the full 1000.
- Estimated time to first useful periodic checkpoint: epoch 50 in about 13-14 hours from launch; epoch 100 in about 26-28 hours.

## Session 25

- User asked what speed-up methods are available, including more GPUs and `num_workers`.
- Checked the active config values: all three formal translator configs already use `batch_size: 32`, `num_workers: 8`, `pin_memory: true`, `persistent_workers: false`, `num_epochs: 1000`, and `checkpoint_every: 50`.
- Checked the node at `2026-05-19T14:37:09+00:00`: pids `26881`, `26883`, and `26885` were alive, each using about `5.3GB` H200 memory; each run had 8 child dataloader workers, for 24 workers total.
- Recorded speed-up assessment:
  - Increasing `num_workers` beyond 8 might help only if dataloader stalls dominate; because there are already 24 workers and node load was about 25, it should be benchmarked before changing the formal runs.
  - More GPUs do not automatically speed up a single run because the current workspace is single-process/single-GPU. True per-run GPU scaling requires DDP changes: distributed sampler, DDP wrapping, rank-aware logging/checkpointing, and metric reduction.
  - The lowest-risk throughput change is to benchmark larger batches such as 64 or 128 on idle GPU3; H200 memory use is low enough that batch size, not memory, is likely the next easy lever.
  - AMP/bf16 could plausibly improve raw-image obs-encoder plus transformer throughput, but needs a smoke test before formal use.
  - The most reliable wall-clock reduction for this exploratory stage is to compare eval-loss trends at epoch 50 or 100 rather than waiting for all 1000 epochs.
