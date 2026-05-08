# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task006_eval_official_robomimic_square_bcrnn -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task006_eval_official_robomimic_square_bcrnn |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_method_developer/task006_eval_official_robomimic_square_bcrnn |
| Session | 21 |

## 最近进展
- 当前可访问两个 GPU 入口：`10.100.16.46:16139` 和 `10.100.16.46:23989`，两边各自可见 2 张 NVIDIA H200。
- `16139` 正在跑 DP no-hist 四路实验：UNet/DiT × LDP-MH/official-PH v1.4.1，四个主 PID `172304/172310/176077/176083` 均存活。
- `23989` 正在跑 SmolVLA 四路实验：small/big384 × PTP/LDP-MH/official-PH v1.4.1，四个主 PID `27745/27774/27801/27816` 和 post-train monitor `62177` 均存活。
- Session 21 已新增 `current_work_handoff.md`，记录当前全部实验、路径、数据版本、脚本入口，以及迁移到 H200 py39 + robomimic 0.2.0 环境后的复测步骤。
