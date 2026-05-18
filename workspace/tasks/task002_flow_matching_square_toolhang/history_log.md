# History Log

<!-- METADATA:SESSION=1 -->

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
