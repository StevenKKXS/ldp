# Task Knowledge

<!-- METADATA:SESSION=1 -->

## Working Rules

- Use observation length 2 for the initial flow-matching experiments.
- Compare both `horizon=10, n_action_steps=8` and direct 8-step action-only prediction.
- Limit first experiment matrix to `square` and `tool_hang`.
- Store small files and launch metadata under `/mnt/nfs/tingwen/intern_method_developer/tasks/task002_flow_matching_square_toolhang/`, then archive to CephFS when stable.
- Do not persist checkpoints, large rollout outputs, datasets, or videos unless explicitly requested.
- GPU nodes must not perform external network operations; fetch/clone/pip/network prep should happen on CPU/common environment and then be copied to the GPU node.

## Findings

- Current DDPM policy diffuses normalized action tensors directly; obs embeddings condition the model but are not the noised variable.
- The FM implementation keeps the same normalized action-space convention: training uses `x_t = t * noise + (1 - t) * action`, target velocity `noise - action`, and inference integrates from `t=1` to `t=0`.
- Full-trajectory configs use dataset/policy `horizon=10`, `n_obs_steps=2`, `n_action_steps=8`; predicted actions are sliced from indices 1 through 8.
- Action-only configs keep dataset `horizon=10` but set policy `horizon=8` and `pred_action_steps_only=true`, training directly on `action[:, 1:9]`.
- Remote node has usable conda env `/mnt/nfs/tingwen/ldp/envs/gmp_released_ckpt/miniforge3/envs/gmp-py310` with torch, hydra, diffusers, robomimic, wandb, and zarr installed.
- Remote code handoff path is `/mnt/nfs/tingwen/intern_method_developer/repos/ldp_flow_matching`, branch `intern_method_developer/task002_flow_matching_square_toolhang`, commit `3914a6b`, with `data` symlinked to `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets`.
- Dataset files observed on the remote node include square `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image_abs.hdf5` and tool_hang `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5`.
- Four configs parsed on the remote env: `experiment_configs/square/flow_transformer_square_h10.yaml`, `experiment_configs/square/flow_transformer_square_action8.yaml`, `experiment_configs/tool/flow_transformer_tool_hang_h10.yaml`, and `experiment_configs/tool/flow_transformer_tool_hang_action8.yaml`.
