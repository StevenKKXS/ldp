## Task: Flow-Matching DP Baselines on Square and Tool Hang

<!-- METADATA:STATUS=Open,ASSIGNEE= -->

### Background

- Test whether replacing DDPM denoising with flow matching can learn the current LDP/DP image-policy tasks.
- Keep the observation setup close to traditional DP: two observation frames.
- Compare two action-generation formulations:
  - full-trajectory flow matching with `horizon=10`, `n_obs_steps=2`, `n_action_steps=8`
  - action-steps-only flow matching with direct 8-step action chunks
- Scope is limited to `square` and `tool_hang`; do not test other tasks yet.

### Resource

- Assigned node: `tingwen_ptp_4gpu_node_96h_49722d42`
- SSH: `10.100.2.35:33805`
- Expected capacity: 4 GPUs

### Goals

- Implement a reusable `FlowMatchingTransformerHybridImagePolicy`.
- Add configs for square and tool hang covering both flow variants.
- Run smoke tests before launching long runs.
- Launch four comparable training jobs if smoke passes:
  - square, full trajectory
  - square, action-steps-only
  - tool_hang, full trajectory
  - tool_hang, action-steps-only
- Save small files, configs, launch scripts, logs, and reports under the NFS/CephFS small-file archive rules.

### Acceptance Criteria

- Code path trains without shape or dtype errors on at least one small smoke batch.
- For each launched experiment, record exact config, command, output path, GPU assignment, and process id.
- Record early offline metrics: train loss, validation loss if available, sampled action MSE if available.
- If sufficient time/resources allow, run rollout evaluation and report success rate.
- Report whether flow matching shows evidence of learning compared with DDPM baselines.

