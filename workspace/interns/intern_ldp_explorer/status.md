# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 54 |
| Recent Progress | Clarified the value and result status of the stale Direction C experiments. Stage 1 and Stage 2a results were already captured and are useful: `past` translator is the strongest offline objective, with formal/tuned best val losses around `0.000455 @ e113` and `0.000434 @ e118`, and frozen-head Stage 2a shows pretrained `past` context beating random context (`0.007839` / future L1 `0.04917` vs `0.011571` / `0.06736`). Old Stage 2b rollout numbers were also captured, but they are diagnostic only because the old action8 condition mask hid obs tokens `8..15`; they should not be used as final downstream evidence. The currently stale processes themselves have no further useful value while blocked in I/O wait. |
