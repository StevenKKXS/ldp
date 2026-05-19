# Direction C Observation Log

## 2026-05-19 Plan Review

- The user-proposed Behavior Translator direction is feasible as a representation pretraining pipeline.
- The first implementation should not assume camera embeddings are available from the dataloader; current PTP image dataloader normally returns raw image/proprio tensors.
- V0 should reuse the existing robomimic obs encoder to convert raw obs history into feature tokens before the translator.
- Stage 1 and Stage 2a are the right first milestones; DP/PTP integration should wait until frozen pretrained context beats frozen random context.

## 2026-05-19 Ownership Clarification

- User clarified that `intern_ldp_explorer` is mainly responsible for Direction C.
- Direction A/B are owned by another intern and should not be placed in this agent's execution queue.

## 2026-05-19 Stage 1 Training Plan

- The first Stage 1 run should be Square `C1-T3`: history observations to past+future actions.
- Use `H=16`, `P=16`, `K=8`.
- The BehaviorTranslationDataset needs explicit anchor slicing: for `H=P=16`, use sequence offsets `0...23`, obs offsets `1...16`, past action offsets `0...15`, and future action offsets `16...23`.
- Train the robomimic obs encoder together with the translator in Stage 1; freezing a randomly initialized obs encoder would not test the intended visual-history representation.
