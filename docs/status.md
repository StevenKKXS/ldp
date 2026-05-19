# 全局实验状态

Last updated: 2026-05-19

## 当前 Active Plan

- Global: `docs/plans/plan_init_2026-05-18.md`
- Direction A: `docs/direction_a_future_action_contrastive/plan_detailed_2026-05-18.md`
- Direction B: `docs/direction_b_action_sequence_predictive/plan_detailed_2026-05-18.md`
- Direction C: `docs/direction_c_behavior_translator/plan_review_2026-05-19.md`

Owner note: `intern_ldp_explorer` is responsible for Direction C. Direction A/B are owned by another intern.

## 总体状态表

| Direction | Status | Current Task | Current Experiment | Latest Result | Next Step |
|---|---|---|---|---|---|
| A: Future-Action Contrastive | Reviewed, owned by another intern | Square / ToolHang | N/A | N/A | Not in intern_ldp_explorer execution queue |
| B: Action-Sequence Predictive | Reviewed, owned by another intern | Square / ToolHang | N/A | N/A | Not in intern_ldp_explorer execution queue |
| C: Behavior Translator Context | Active for intern_ldp_explorer, offline-first plan preferred | Square first | N/A | N/A | Implement BehaviorTranslationDataset, BehaviorTranslator, and one Square T3 config, then run shape smoke |

## 当前实验顺序 for intern_ldp_explorer

1. Direction C: Square dataset/model/config smoke
2. Direction C: Square offline translator Stage 1
3. Direction C: Square frozen-head probe Stage 2a
4. Direction C: ToolHang offline translator Stage 1
5. Direction C: ToolHang frozen-head probe Stage 2a
6. Direction C: DP/PTP integration only if Stage 2a passes the pretrained-vs-random gate

## 最新关键结论

- PTP 数据相关训练、encoder pretraining 对比、rollout 复现必须使用 Python 3.9 + `robomimic==0.2.0`；`gmp-py310` / `robomimic 0.4.0` 结果不可作为可信 PTP-data 复现证据。
- 当前 FM GPU 节点 `10.100.2.35:33805` 尚未发现可用 `/root/ptp_ldp_py39`；继续可信实验前需要从 CPU/公共侧重建或同步并验证 py39 / `robomimic==0.2.0` 环境。
- 尚未开始实验。
- Direction A 已保存详细 plan 并完成初步 review，但没有实验结果；由另一个 intern 负责。
- Direction A review 已根据用户澄清更新: first pass 优先保持 PTP policy 结构不变，只做 encoder pretraining。
- Direction B 已保存详细 plan 并完成初步 review，但没有实验结果；由另一个 intern 负责。
- Direction B review 建议 first pass 保持 PTP policy 结构不变，只做 predictive encoder pretraining。
- Direction C 已保存 review 后计划，但没有实现和实验结果。
- Direction C 的第一版应复用 raw obs -> existing robomimic obs_encoder -> translator token 的路径；不能默认假设 dataloader 已返回 camera embeddings。
- `intern_ldp_explorer` 当前主线是 Direction C，不主动推进 Direction A/B。
- 不允许把任何方向视为已验证有效。
- Direction A 需要先讨论 exact PTP baseline、contrastive action segment、encoder checkpoint format、frozen/finetune protocol、以及 B2 是否与 B1 区分。
- Direction B 需要先讨论 exact PTP baseline、predictive action target、decoder capacity、encoder checkpoint format、frozen/finetune protocol、以及 B2 是否与 B1 区分。
