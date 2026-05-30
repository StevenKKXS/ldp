# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 74 |
| Recent Progress | Documented current Direction C code location, branch, and workflow for user inspection. Authoritative git worktree is `/work-agents/intern_ldp_explorer/ldp`, branch `intern_ldp_explorer/task002_flow_matching_square_toolhang`, commit `7cc3e24`; Ceph execution copy is `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/repos/ldp`, which is a synced code copy without `.git`. Key implementation files are `behavior_translation_dataset.py`, `behavior_translator.py`, `train_behavior_translator_workspace.py`, `translator_conditioned_transformer_hybrid_image_policy.py`, and the Square Stage1/Stage2b configs. Main training concern found: Stage1 `target_mode=past` optimizes only past-action SmoothL1, while downstream uses `BehaviorTranslator.get_context()` through a context projector that has no direct Stage1 loss, so context quality may be underconstrained. |
