# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 37 |
| Recent Progress | Explained Direction C Stage 1 `past` data flow and loss. The dataset builds a 24-step sample with obs history indices `1..16`, past action targets `0..15`, and future action diagnostics `16..23`; the model receives only raw obs/proprio history, encodes it through the trainable robomimic obs encoder and BehaviorTranslator, predicts 16 past plus 8 future action tokens, and in `target_mode=past` backpropagates only SmoothL1 over the first 16 normalized action predictions. Future metrics are logged for diagnostics but do not contribute to the `past` loss. |
