# Task Knowledge

<!-- METADATA:SESSION=7 -->

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
