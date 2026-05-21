# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 42 |
| Recent Progress | Continued Direction C by implementing the Stage2b translator-conditioned transformer path. Added `TranslatorConditionedTransformerHybridImagePolicy`, which loads a frozen BehaviorTranslator checkpoint, extracts 16-step behavior context, projects it into obs-feature space, and injects it into existing transformer condition tokens without changing the default PTP policy path. Added Square action8 config `experiment_configs/square/transformer_square_translator_context_action8.yaml`, using `n_obs_steps=16`, dataset horizon `24`, action chunk `8`, and tuned `past` best checkpoint by default. Fixed a `pred_action_steps_only=true` NaN loss bug in the base diffusion transformer by skipping the old `n_obs_steps-1` slice after the action-only target has already been sliced. Verified py_compile, Hydra config parse, and CPU single-sample `compute_loss` smoke with finite losses; synced the new files to the NFS GPU worktree. Current GPUs remain occupied: old node has 4 Stage1 jobs, new node has 4 tuned Stage2a probes. |
