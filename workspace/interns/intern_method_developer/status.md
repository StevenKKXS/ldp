# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task006_eval_official_robomimic_square_bcrnn -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task006_eval_official_robomimic_square_bcrnn |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_method_developer/task006_eval_official_robomimic_square_bcrnn |
| Session | 7 |

## 最近进展
- 已核对 BC-RNN 与 SmolVLA 输入信息：issue157 图像 BC-RNN 和 SmolVLA 都使用两路图像加 `robot0_eef_pos/quat/gripper_qpos`，没有使用 `object`；官方 model-zoo low-dim BC-RNN 使用额外 `object` 低维状态但不使用图像。
