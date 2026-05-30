# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 20 |
| Recent Progress | Documented the active code path, branch, launch scripts, and training data flow for user review. Current branch is `intern_method_developer/task002_flow_matching_square_toolhang` at commit `7911914`; local review path is `/work-agents/intern_method_developer/ldp`. |
| Handoff | Encoder method workflow uses `train.py` with `TrainEncoderPretrainWorkspace` for Direction A/B pretraining, then exact PTP downstream via `TrainDiffusionTransformerHybridWorkspace` and `DiffusionTransformerHybridImagePolicy` loading `obs_encoder_dir`. Important review point: encoder pretrain configs currently use `global_obs=16,horizon=32`, while downstream exact PTP uses Square `global_obs=2,horizon=32,n_action_steps=1` and ToolHang `global_obs=2,horizon=16,n_action_steps=8`; if strict PTP-structure matching is required, pretrain observation length should be reviewed. Flow-matching code is also on the branch via `FlowMatchingTransformerHybridImagePolicy`, but current encoder results came from the encoder-pretrain/downstream path, not FM rollout. |
