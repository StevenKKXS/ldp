# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 77 |
| Recent Progress | Read-only reviewed Direction C BehaviorTranslationDataset, TrainBehaviorTranslatorWorkspace, normalizer, and Square configs for leakage/proprio-shortcut diagnostics. Found that lowdim-only/image-only retrain ablations can be done by pruning top-level shape_meta via Hydra or small child configs, while checkpoint-compatible image/proprio mask and shuffle require a small normalizer-aware perturbation hook after obs normalization in the translator workspace; existing shuffle_obs_history is only temporal shuffle, not modality shuffle. |
