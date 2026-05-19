# Task Knowledge

<!-- METADATA:SESSION=24 -->

## Working Rules

- Use observation length 2 for the initial flow-matching experiments.
- Compare both `horizon=10, n_action_steps=8` and direct 8-step action-only prediction.
- Limit first experiment matrix to `square` and `tool_hang`.
- Store small files and launch metadata under `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/`, then archive to CephFS when stable.
- Do not persist checkpoints, large rollout outputs, datasets, or videos unless explicitly requested.
- GPU nodes must not perform external network operations; fetch/clone/pip/network prep should happen on CPU/common environment and then be copied to the GPU node.
- Do not touch the previous GPU node for this task; ownership has moved to another agent.
- New PTP encoder method-development docs live under `docs/`; start from `docs/main.md` and `docs/status.md` before answering progress questions.
- For the new encoder task, no experiment is valid until Direction A / Direction B detailed plans are reviewed and experiment logs are recorded.
- Current local `docs/` path is `/work-agents/intern_method_developer/ldp/docs`, on container `overlay` mounted at `/`; it is not currently placed under `/mnt/nfs/tingwen` or `/mnt/cephfs/home/tinwen.du`.
- Direction A review file: `docs/direction_a_future_action_contrastive/review_2026-05-18.md`.
- Direction A latest review update: `docs/direction_a_future_action_contrastive/review_update_ptp_compat_2026-05-18.md`.
- Direction A "action window" means the action segment used as contrastive similarity supervision, not a change to PTP prediction horizon or rollout logic.
- Direction A first implementation should preserve the proven PTP policy structure and use future-action contrastive learning as encoder pretraining loaded through existing PTP encoder checkpoint hooks.
- Policy-side condition concat is deferred; exact-PTP-compatible encoder pretraining is preferred for the first pass.
- Direction A B2 is mandatory only if a new policy-side architecture is added; if policy structure is unchanged, compare exact PTP baseline against contrastive-pretrained encoder frozen/finetuned and record whether B2 is distinct from B1.
- Direction B plan file: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`.
- Direction B review file: `docs/direction_b_action_sequence_predictive/review_2026-05-18.md`.
- Direction B first implementation should preserve the proven PTP policy structure and use action-sequence prediction only as encoder pretraining; discard the decoder before downstream PTP training.
- Direction B is likely the simpler smoke path: `dataset batch -> obs_encoder -> small MLP decoder -> Huber(normalized action sequence) -> compatible encoder checkpoint`.
- If no new retained policy module is added, Direction B B2 may not be distinct from B1; record this rather than inventing a misleading control.

## Findings

- Current DDPM policy diffuses normalized action tensors directly; obs embeddings condition the model but are not the noised variable.
- The FM implementation keeps the same normalized action-space convention: training uses `x_t = t * noise + (1 - t) * action`, target velocity `noise - action`, and inference integrates from `t=1` to `t=0`.
- Full-trajectory configs use dataset/policy `horizon=10`, `n_obs_steps=2`, `n_action_steps=8`; predicted actions are sliced from indices 1 through 8.
- Action-only configs keep dataset `horizon=10` but set policy `horizon=8` and `pred_action_steps_only=true`, training directly on `action[:, 1:9]`.
- Remote node has usable conda env `/mnt/nfs/tingwen/ldp/envs/gmp_released_ckpt/miniforge3/envs/gmp-py310` with torch, hydra, diffusers, robomimic, wandb, and zarr installed.
- Remote code handoff path is `/mnt/nfs/tingwen/intern_method_developer/repos/ldp_flow_matching`, branch `intern_method_developer/task002_flow_matching_square_toolhang`, commit `3914a6b`, with `data` symlinked to `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets`.
- Dataset files observed on the remote node include square `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image_abs.hdf5` and tool_hang `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`.
- Four configs parsed on the remote env: `experiment_configs/square/flow_transformer_square_h10.yaml`, `experiment_configs/square/flow_transformer_square_action8.yaml`, `experiment_configs/tool/flow_transformer_tool_hang_h10.yaml`, and `experiment_configs/tool/flow_transformer_tool_hang_action8.yaml`.
- `gmp-py310` initially lacked `threadpoolctl`; dataset import fails without it. It was installed into the NFS env from CPU/common side, not from the GPU node.
- `gmp-py310` also lacked `pytorch3d`; a pure-Python transforms stub already existed at `/mnt/nfs/tingwen/ldp/small_files/intern_ldp_explorer/pytorch3d_src` and was symlinked into the NFS env as `site-packages/pytorch3d`.
- The GMP robomimic 0.4 checkout has `CropRandomizer` in `robomimic.models.obs_core`, not `robomimic.models.base_nets`.
- The square FM configs must not include `task.dataset.shape_meta.obs.embedding` when using raw `image_abs.hdf5`; the dataset conversion tries to load every key in dataset `shape_meta`.
- The current `gmp-py310` env is sufficient for training when rollout is disabled.
- The transformer workspace now skips env-runner instantiation when the local training run will not hit a rollout epoch or when `n_train+n_test == 0`.
- Formal runs started with online rollout disabled via `training.rollout_every=999999`; rollout evaluation should be launched as a separate phase after env-runner dependencies are repaired.
- As of `2026-05-18T22:40:48+00:00`, all four formal FM jobs were alive; ToolHang cache construction had completed and both ToolHang jobs had entered training/validation.
- As of `2026-05-19T02:58:12+00:00`, all four formal FM jobs were still alive, all had written `latest.ckpt`, Square was around epoch 457-459, and ToolHang was at epoch 64.
- Square rollout env now needs these runtime shims in the GMP py310 environment: `LD_LIBRARY_PATH` must include the NFS env lib directory with linked GLVND libs; `PYOPENGL_PLATFORM=egl` and `MUJOCO_GL=egl`; legacy robomimic `OSC_POSE` controller metadata must be converted to robosuite 1.5 `BASIC` composite controller metadata; Gym 0.23 requires AsyncVectorEnv reset/step/concatenate compatibility shims.
- Current saved Square FM `latest.ckpt` rollout result at `2026-05-19T03:21:00+00:00`: `square_h10` 10 test seeds `0/10`, `square_action8` 10 test seeds `0/10`.
- Standard RobomimicImageRunner reward aggregation works for `square_h10`, but its extra online action-HSIC path can fail on `square_action8` ragged chunks; use reward-only rollout for score-only checks or patch the runner before relying on action-HSIC logs.
- Active NFS/GPU `gmp-py310` imports `robomimic 0.4.0` from the GMP vendor checkout, not robomimic 0.2.0.
- User requires all future PTP-data training, encoder-pretraining comparisons, and rollout intended for PTP claim reproduction to use Python 3.9 + `robomimic==0.2.0`.
- Treat the current FM `gmp-py310` / `robomimic 0.4.0` training and rollout results as version-confounded; do not use them as trusted PTP-data evidence.
- Session 13 environment check: current GPU node `10.100.2.35:33805` lacks `/root/ptp_ldp_py39/bin/python`; old py39 note host `10.100.0.29:36645` is no longer reachable; rebuild or sync a py39 / `robomimic==0.2.0` env from CPU/common storage before the next trusted run.
- Session 13 stopped the `formal_train_20260518_143331` `gmp-py310` FM jobs on `10.100.2.35:33805`; existing checkpoints/logs remain on NFS, but the run should be treated as noncompliant with the py39 / robomimic 0.2.0 requirement.
- Session 14 created and verified NFS env `/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020` for current GPU node `10.100.2.35:33805`; verified Python `3.9.23`, `robomimic 0.2.0`, `robosuite 1.2.0`, `mujoco-py 2.1.2.14`, `gym 0.21.0`, `torch 2.5.1`.
- Required py39 rollout environment exports: `MUJOCO_PY_MUJOCO_PATH=/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runtimes/mujoco210`, `LD_LIBRARY_PATH=$MUJOCO_PY_MUJOCO_PATH/bin:/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020/lib:$LD_LIBRARY_PATH`, `MUJOCO_GL=egl`, `PYOPENGL_PLATFORM=egl`, and `PYTHONPATH=/mnt/nfs/tingwen/intern_method_developer/repos/ldp_flow_matching:$PYTHONPATH`.
- `eval_flow_matching_rollout.py` is the reward-only evaluator used for py39 tests; it loads the workspace checkpoint, selects `ema_model` by default, overrides rollout counts, and writes `eval_log.json`.
- Robomimic 0.2.0 compatibility fix: `diffusion_transformer_hybrid_image_policy.py` must not unconditionally import `robomimic.models.obs_core`; use `base_nets.CropRandomizer` first and fall back to `obs_core.CropRandomizer` only when available.
- Current py39 / robomimic 0.2.0 FM rollout results from `formal_train_20260518_143331/latest.ckpt`: Square h10 `7/10`, Square action8 `4/10`, ToolHang h10 `0/10`, ToolHang action8 `0/10`.
- Original PTP normalization answer: the workspace calls `dataset.get_normalizer()` and installs it into model/EMA; policy training normalizes `batch['obs']` and `batch['action']`, rollout normalizes obs and unnormalizes predicted actions.
- For robomimic `abs_action: true`, action normalization is partial: first 3 EEF position dimensions are range-normalized to `[-1,1]`; remaining rotation/gripper dimensions are identity. For dual-arm actions, the first 3 position dimensions of each arm are range-normalized and the remaining dimensions are identity.
- For proprio in original robomimic PTP configs, `robot*_eef_pos` and `robot*_gripper_qpos` are range-normalized to `[-1,1]`; `robot*_eef_quat` is identity. This is not a uniform z-score normalizer.
- PTP dataloader window rule: `SequenceSampler` emits one contiguous sequence; `RobomimicReplayImageDataset.__getitem__` returns obs from the first `n_obs_steps * subsample_frames` samples, then returns actions as subsampled historical actions plus future actions. With `subsample_frames=1`, `n_obs_steps=K+1` and `horizon=K+1+F` represent obs offsets `[-K, ..., 0]` and action offsets `[-K, ..., F]` around the current frame.
- Current policy assumes chronological order. Reversing obs order to current-to-history instead of history-to-current is mechanically easy but changes positional semantics and should be treated as an architecture/training change.
- PTP dataloader obs format: default image configs return raw image/proprio tensors, not encoder outputs. `DiffusionTransformerHybridImagePolicy` runs `self.obs_encoder(...)` inside training and rollout.
- Embedding-cache exception: when `use_embed_if_present=True` and replay data has an `embedding` key, `RobomimicReplayImageDataset` returns `obs['embedding']` plus action only; the normalizer skips `embedding`, and the policy uses the embedding directly as condition.
- Session 18 FM stop decision: no FM process is currently running on `10.100.2.35:33805`; current checkpoints already have py39 rollout measurements. It is reasonable to release the GPU. Further FM improvement should restart clean py39 / `robomimic 0.2.0` training instead of resuming the old gmp-py310 run.
- Direction C Behavior Translator plan lives at `docs/direction_c_behavior_translator/plan_review_2026-05-19.md`; its first implementation should be offline-first and use existing robomimic obs_encoder features rather than assuming dataloader camera embeddings.
- Direction C DP/PTP integration is gated on the frozen-head probe: pretrained frozen translator context must beat a same-architecture frozen random translator context.
- Ownership clarification: `intern_ldp_explorer` mainly owns Direction C Behavior Translator. Direction A/B are owned by another intern and should not be placed in this agent's execution queue.
- Direction C Stage 1 first run should be Square `C1-T3` with `H=16`, `P=16`, `K=8`, explicit anchor slicing, trainable robomimic obs encoder plus BehaviorTranslator, SmoothL1 past/future loss, and best checkpoint by `val/future_l1`.
- Direction C Stage 1 now has three implemented Square configs: `behavior_translator_square_past.yaml`, `behavior_translator_square_future.yaml`, and `behavior_translator_square_past_future.yaml`. Each trains for `1000` epochs, checkpoints every `50`, and uses `val/loss_total` as the eval-loss monitor.
- `RobomimicReplayImageDataset` no longer computes the action-correlation diagnostic unless `compute_action_corr=True` and CUDA is available; this diagnostic is not required for translator training.
- Direction C GPU node `10.100.2.35:25076` is verified for py39 / `robomimic 0.2.0` work with 4xH200, `/mnt/nfs`, and `/mnt/3fs2`.
- Direction C synced GPU worktree path: `/mnt/nfs/tingwen/intern_ldp_explorer/repos/ldp_behavior_translator`, currently from branch `intern_ldp_explorer/task002_flow_matching_square_toolhang` commit `cf95686`.
- Direction C Stage 1 active run root: `/mnt/nfs/tingwen/intern_ldp_explorer/tasks/direction_c_behavior_translator/outputs/stage1_square_20260519_143020`; manifest maps `past` to GPU0 pid `26881`, `future` to GPU1 pid `26883`, and `past_future` to GPU2 pid `26885`.
- On this GPU node, avoid using shell variable name `ENV` for Python env paths because shell initialization can set it to `/etc/shinit_v2`. Use a name like `PY39`.
- For remote background launches containing many quoted paths, send the script with `ssh ... 'bash -s' <<'REMOTE'` so local shell quoting does not erase remote variables.
- Direction C Stage 1 Square translator speed on `10.100.2.35:25076`: current batch throughput is about 2.6-2.7 train batches/sec for `2478` train batches per epoch, so one epoch is about 15-16 minutes plus validation/checkpoint overhead. The 1000-epoch plan is about 10.5-12 days; a 96h allocation reaches roughly 340-380 epochs.
