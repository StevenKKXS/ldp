# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task006_eval_official_robomimic_square_bcrnn -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task006_eval_official_robomimic_square_bcrnn |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_method_developer/task006_eval_official_robomimic_square_bcrnn |
| Session | 25 |

## 最近进展
- 当前可访问两个 GPU 入口：`10.100.16.46:16139` 和 `10.100.16.46:23989`，两边各自可见 2 张 NVIDIA H200。
- `16139` 正在跑 DP no-hist 四路实验：UNet/DiT × LDP-MH/official-PH v1.4.1，四个主 PID `172304/172310/176077/176083` 均存活。
- `23989` 正在跑 SmolVLA 四路实验：small/big384 × PTP/LDP-MH/official-PH v1.4.1，四个主 PID `27745/27774/27801/27816` 和 post-train monitor `62177` 均存活。
- Session 21 已新增 `current_work_handoff.md`，记录当前全部实验、路径、数据版本、脚本入口，以及迁移到 H200 py39 + robomimic 0.2.0 环境后的复测步骤。
- Session 22 已在 `origin/main` 找到 py39 H200 环境文档：`workspace/shared/ldp_ptp_py39_h200_environment.md`，提交 `968f3ca`。
- Session 23 于 2026-05-08 14:40 UTC 检查：DP 四路仍在跑，official-PH 最好 rollout 为 UNet epoch 90 `0.68`、DiT epoch 70 `0.60`；SmolVLA 四路仍在训练，official-PH 到约 epoch 850/875，PTP/LDP-MH 到约 epoch 330，`epoch_1000.pt` 仍为 `0/4`。
- Session 24 分析 DP 比 SmolVLA 慢的主因：DP 将 50-rollout、50-video、`num_inference_steps=100`、`n_action_steps=1` 的闭环评估嵌入训练，且 batch size 64 导致每 epoch optimizer steps 约为 SmolVLA 的两倍；SmolVLA 当前只做离线 eval。
- Session 25 估算 DP 运行时长与 20-rollout 提速：当前四路已跑约 `5.6h`；20 rollout 主要提升前 100 epoch 的 eval-every-10 阶段，official-PH 约提速 `40-45%`，LDP-MH 约提速 `20-30%`，100 epoch 后因 eval 每 100 epoch 一次整体收益约 `2-6%`。
