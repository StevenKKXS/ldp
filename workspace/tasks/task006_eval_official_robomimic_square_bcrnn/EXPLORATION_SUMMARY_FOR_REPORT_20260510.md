# Square Baseline 探索总结

日期：2026-05-10 UTC

这份文档用于汇总当前 Square 任务探索结果，优先按随笔中的思路组织：

1. 先尝试较新的 baseline SmolVLA，观察是否能直接解决 Square。
2. 再用 BC-RNN specialist 作为参考，检查不同数据集和版本下成功率差异。
3. 最后用 DP 和 SmolVLA 做双数据、双环境交叉验证，判断问题更像是模型、数据，还是版本对齐。

## 总览

目前最强结果仍然是 specialist 的 image BC-RNN 复现：在对齐的 official-PH v1.4.1 图像数据上，epoch 540 达到 `40/50 = 0.80`。这个结果接近 robomimic 官方 model zoo 对 Square(PH) BC-RNN 报告的约 84%。

官方下载的 low-dim BC-RNN checkpoint 在我们当前 py312 / robomimic 0.3 / robosuite 1.4.1 环境中只达到 `33/50 = 0.66`。这说明官方 84% 结果在当前环境下不能直接严格复现，版本对齐风险是真实存在的。

SmolVLA 能正常训练和 rollout，也保存了视频，但当前实现和参数下成功率偏低。所有已完成 SmolVLA 中最好的是 py39 / robomimic 0.2 / robosuite 1.2 环境下 big384 + PTP/LDP-MH 数据，`16/50 = 0.32`。当前 py312 环境下最好是早期三路实验的 big384 + PTP/LDP-MH，`13/50 = 0.26`；四路正式对比中最好是 big384 + official-PH，`12/50 = 0.24`。

DP no-hist 明显强于当前 SmolVLA。当前 py312 环境下，official-PH v1.4.1 数据上 DP UNet 达到 `34/50 = 0.68`，DP DiT 达到 `30/50 = 0.60`。但 DP 同样对数据和环境组合很敏感：PTP/LDP-MH 在当前 py312 环境很低，而在 py39 / robomimic 0.2 / robosuite 1.2 环境中 UNet 目前达到 `23/50 = 0.46`。

当前结论：Square 成功率主要受数据版本、运行环境版本、以及 specialist/generalist 架构差异共同影响。现有证据不能证明 SmolVLA 一定不适合 Square，但能说明我们测试的 SmolVLA recipe 还没有竞争力，明显落后于对齐后的 BC-RNN specialist 和 DP。

## 实验动机

| 实验线 | 为什么做 | 想验证什么 |
| --- | --- | --- |
| SmolVLA 新 baseline | 想确认较新的 VLA / chunk action 模型是否能直接替代 robomimic specialist。 | 当前 SmolVLA 架构、`ldp_abs10` action 表示和本地数据是否足够解决 Square。 |
| 官方 BC-RNN checkpoint 测试 | 官方 model zoo 报告 Square(PH) low-dim BC-RNN 约 84%，需要一个基准参考。 | 官方 checkpoint 在我们当前环境中能否复现官方成功率。 |
| Issue #157 image BC-RNN 复现 | issue #157 提到 robosuite 版本和纹理变化可能导致 image policy 成功率下降。 | 如果使用当前环境对齐的 v1.4.1 图像数据，specialist BC-RNN 是否能恢复高成功率。 |
| SmolVLA 双数据对比 | 同时跑 PTP/LDP-MH 数据和 official-PH v1.4.1 数据。 | SmolVLA 差是否主要来自数据版本或数据分布。 |
| SmolVLA small vs big384 | 在相同数据下增加模型容量。 | 是否只是模型容量不够。 |
| DP no-hist UNet / DiT | 引入常用 DP baseline，并参考 PTP 的 no-hist 参数。 | 判断弱结果是否是 SmolVLA 特有，还是现代生成式策略普遍在该配置下困难。 |
| py39 / robomimic 0.2 / robosuite 1.2 对比环境 | 根据 issue #157 和 PTP 环境线索，构造更旧的运行栈。 | 数据和运行环境是否必须成套对齐，版本错配是否解释成功率差异。 |

## 数据表

| 数据版本 | 路径 | 数据量 | env 信息 | 用途 |
| --- | --- | ---: | --- | --- |
| 官方 model-zoo Square(PH) low-dim checkpoint lineage | checkpoint 内嵌路径为 `/cvgl2/u/amandlek/batch_datasets/final_benchmark_datasets/square/ph/low_dim.hdf5` | 本地没有直接拿到原始 HDF5 数据量 | checkpoint metadata 中无显式 `env_version` | 官方 low-dim BC-RNN checkpoint 测试 |
| 本地 `intern_ldp_explorer` Square PH image | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/ph/image.hdf5` | 200 demos / 30,154 steps | 未看到显式 `env_version` | 本地数据检查 |
| 本地 `intern_ldp_explorer` Square MH image | `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets/robomimic/datasets/square/mh/image.hdf5` | 300 demos / 80,731 steps | 未看到显式 `env_version` | PTP/LDP-MH absolute-action 数据来源 |
| PTP/LDP-MH `image_abs` copy | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5` | 300 demos / 80,731 steps | 未看到显式 `env_version` | SmolVLA 和 DP 的 PTP/LDP-MH 数据 |
| Official-PH image v1.4.1 | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_v141.hdf5` | 200 demos / 30,154 steps | `env_version=1.4.1` | issue #157 image BC-RNN 复现 |
| Official-PH `image_abs` v1.4.1 | `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_abs_v141.hdf5` | 200 demos / 30,154 steps | `env_version=1.4.1` | SmolVLA 和 DP 的 official-PH 数据 |

## 运行环境

| 环境 | 版本 | 实验目的 |
| --- | --- | --- |
| 当前/老环境 py312 | Python 3.12.3, torch 2.5.1+cu124, robomimic 0.3.0, robosuite 1.4.1, mujoco 3.8.0 | 当前 LDP 风格环境，更接近 official-PH v1.4.1 数据的视觉栈。 |
| 新对比环境 py39 | Python 3.9.25, torch 2.5.1+cu124, robomimic 0.2.0, robosuite source version 1.2.0, mujoco-py 2.1.2.14 | 更接近 issue #157 / PTP 提到的旧环境，用来验证版本对齐影响。 |

## 实验设置

| 模型 | 设定 | 输入信息 | 动作和时序 | checkpoint / eval |
| --- | --- | --- | --- | --- |
| 官方 low-dim BC-RNN | 下载 robomimic model-zoo Square(PH) epoch 1850 checkpoint | `robot0_eef_pos`, `robot0_eef_quat`, `robot0_gripper_qpos`, `object`；无图像 | 官方 BC-RNN specialist | 50 rollouts，horizon 400，保存视频 |
| issue #157 image BC-RNN | 在 official-PH v1.4.1 image 数据上训练 image BC-RNN | `agentview_image`, `robot0_eye_in_hand_image`, `robot0_eef_pos`, `robot0_eef_quat`, `robot0_gripper_qpos`；无 `object` | LSTM recurrence，训练 `seq_length=10` / RNN horizon 10 | 训练 600 epochs，rollout eval，保留 best checkpoint |
| SmolVLA small | task-local 独立训练脚本，不污染原 LDP | 与 image BC-RNN 相同的图像 + proprio keys；无 `object` | `chunk_size=16`, `action_repr=ldp_abs10`, sample steps 10, emb_dim 256, expert layers 6 | 1000 epochs；10,20,...,100,200,...,1000 保存命名 checkpoint；全 checkpoint 20-rollout sweep；best checkpoint 50-rollout 保存视频 |
| SmolVLA big384 | 同 SmolVLA small | 同上 | emb_dim 384, expert layers 8 | 同上 |
| DP no-hist UNet | 参考 PTP 常用 no-hist DP 参数 | 图像 + proprio；无 `object` | `horizon=16`, `n_obs_steps=2`, `dataset_obs_steps=2`, `n_action_steps=1`, no past-action prediction | 1000 epochs；scheduled 50-rollout eval；py312 前 100 每 10 epoch eval，py39 前 100 每 20 epoch eval，之后每 100 epoch eval |
| DP no-hist DiT | 按 DP 原生 transformer 路径实现 task-local DiT 版本 | 图像 + proprio；无 `object` | 同 UNet no-hist 设置 | 同上 |

## 结果表

说明：`最终 50` 表示已从 checkpoint sweep 中选出 best checkpoint，并重新做 50 次 closed-loop rollout 且保存视频。`训练中 scheduled 50` 表示训练过程中已经出现的最好 50-rollout eval。DP 的 PTP/LDP-MH 行截至 2026-05-10 03:41 UTC 仍在训练，因此是 best-so-far。

| 状态 | 环境 | 模型/设定 | 数据 | 最好 checkpoint | 成功率 |
| --- | --- | --- | --- | --- | ---: |
| 最终 50 | 当前 py312 | 官方 low-dim BC-RNN model-zoo checkpoint | 官方 Square(PH) low-dim v0.1 lineage | epoch 1850 | 33/50 = 0.66 |
| 最终 50 | 当前 py312 | issue #157 image BC-RNN 复现 | Official-PH image v1.4.1 | epoch 540 | 40/50 = 0.80 |
| 最终 50 | 当前 py312 | SmolVLA small | PTP/LDP-MH image_abs | epoch 200 | 9/50 = 0.18 |
| 最终 50 | 当前 py312 | SmolVLA big384 | PTP/LDP-MH image_abs | epoch 1000 | 13/50 = 0.26 |
| 最终 50 | 当前 py312 | SmolVLA small | Official-PH image_abs v1.4.1 | epoch 600 | 7/50 = 0.14 |
| 最终 50 | 当前 py312 四路正式对比 | SmolVLA small | PTP/LDP-MH image_abs | epoch 700 | 5/50 = 0.10 |
| 最终 50 | 当前 py312 四路正式对比 | SmolVLA big384 | PTP/LDP-MH image_abs | epoch 700 | 9/50 = 0.18 |
| 最终 50 | 当前 py312 四路正式对比 | SmolVLA small | Official-PH image_abs v1.4.1 | epoch 600 | 7/50 = 0.14 |
| 最终 50 | 当前 py312 四路正式对比 | SmolVLA big384 | Official-PH image_abs v1.4.1 | epoch 600 | 12/50 = 0.24 |
| 最终 50 | py39 对比环境 | SmolVLA small | PTP/LDP-MH image_abs | epoch 700 | 12/50 = 0.24 |
| 最终 50 | py39 对比环境 | SmolVLA big384 | PTP/LDP-MH image_abs | epoch 400 | 16/50 = 0.32 |
| 最终 50 | py39 对比环境 | SmolVLA small | Official-PH image_abs v1.4.1 | epoch 90 | 2/50 = 0.04 |
| 最终 50 | py39 对比环境 | SmolVLA big384 | Official-PH image_abs v1.4.1 | epoch 800 | 5/50 = 0.10 |
| scheduled 50，已到 epoch 1000 | 当前 py312 | DP no-hist UNet | Official-PH image_abs v1.4.1 | epoch 90 | 34/50 = 0.68 |
| scheduled 50，已到 epoch 1000 | 当前 py312 | DP no-hist DiT | Official-PH image_abs v1.4.1 | epoch 70 | 30/50 = 0.60 |
| scheduled 50，训练中 | 当前 py312 | DP no-hist UNet | PTP/LDP-MH image_abs | epoch 500 | 5/50 = 0.10 |
| scheduled 50，训练中 | 当前 py312 | DP no-hist DiT | PTP/LDP-MH image_abs | epoch 20 | 2/50 = 0.04 |
| scheduled 50，已到 epoch 1000 | py39 对比环境 | DP no-hist UNet | Official-PH image_abs v1.4.1 | epoch 400 | 10/50 = 0.20 |
| scheduled 50，已到 epoch 1000 | py39 对比环境 | DP no-hist DiT | Official-PH image_abs v1.4.1 | epoch 60 | 24/50 = 0.48 |
| scheduled 50，训练中 | py39 对比环境 | DP no-hist UNet | PTP/LDP-MH image_abs | epoch 200 | 23/50 = 0.46 |
| scheduled 50，训练中 | py39 对比环境 | DP no-hist DiT | PTP/LDP-MH image_abs | epoch 200 | 9/50 = 0.18 |

## DP 曲线重点

当前 py312 环境下，official-PH v1.4.1 的 DP 早期学习很快，但后面会波动下降。因此不能只看 final epoch。

| Eval epoch | UNet success rate | DiT success rate |
| ---: | ---: | ---: |
| 10 | 0.28 | 0.00 |
| 30 | 0.58 | 0.14 |
| 50 | 0.62 | 0.50 |
| 70 | 0.66 | 0.60 |
| 90 | 0.68 | 0.54 |
| 100 | 0.62 | 0.58 |
| 200 | 0.50 | 0.56 |
| 500 | 0.52 | 0.50 |
| 1000 | 0.46 | 0.44 |

## 结论

1. 版本和数据对齐是第一优先问题。

同一个模型家族在不同数据/环境组合下差异很大。当前 py312 环境中，DP 在 official-PH v1.4.1 上达到 `0.68 / 0.60`，但 PTP/LDP-MH 很低。py39 环境中，PTP/LDP-MH 的 DP UNet 反而升到 `0.46`，而 official-PH 的 DP UNet 降到 `0.20`。SmolVLA 也类似：py39 环境让 PTP/LDP-MH 的 SmolVLA 提升到 `0.32`，但 official-PH 降到 `0.10`。这支持“数据生成版本、视觉栈、robosuite 运行环境、action conversion 必须成套对齐”的判断。

2. Specialist BC-RNN 仍是目前最强参考。

Issue #157 image BC-RNN 和 SmolVLA 使用同类 image + proprio 输入，而且不使用 `object`，但 image BC-RNN 达到 `0.80`。官方 low-dim BC-RNN 虽然使用额外 `object` 状态，但在当前环境只有 `0.66`，低于官方 84%。因此，本地最可信的 image-based Square reference 是 issue #157 风格的 aligned image BC-RNN。

3. 当前 SmolVLA 结果偏差，但原因还没有完全拆开。

SmolVLA 最好只有 `0.32`，明显低于 image BC-RNN 的 `0.80` 和当前环境 DP official-PH 的 `0.68`。可能原因包括架构 inductive bias、action chunking、action representation、rollout replanning、超参没有充分调优、或数据转换细节。现有实验说明“只把模型从 small 加大到 big384”不能解决差距。

4. DP 是比当前 SmolVLA 更强的现代 baseline。

DP no-hist 在 official-PH v1.4.1 当前环境中已经能达到 `0.68 / 0.60`，说明 image + proprio 输入本身并非无法完成 Square。DP 仍低于 aligned image BC-RNN，但比 SmolVLA 更接近可用。

5. 必须用 rollout 选 checkpoint。

DP official-PH UNet 最好在 epoch 90，成功率 `0.68`，但 epoch 1000 只有 `0.46`。SmolVLA 的 offline action MSE 也不能可靠预测 closed-loop success。因此 Square 上目前应以 closed-loop rollout 作为 checkpoint selection 标准。

## 当前完成和未完成

| 项目 | 状态 |
| --- | --- |
| SmolVLA 早期三路实验 | 已完成：全 checkpoint 20-rollout sweep、best checkpoint 50-rollout、视频保存。 |
| SmolVLA 当前 py312 四路正式对比 | 已完成：全 checkpoint 20-rollout sweep、best checkpoint 50-rollout、视频保存。 |
| SmolVLA py39 四路对比 | 已完成：全 checkpoint 20-rollout sweep、best checkpoint 50-rollout、视频保存。 |
| DP 当前 py312 official-PH | 已到 epoch 1000，best checkpoint 已明确。 |
| DP py39 official-PH | 已到 epoch 1000，best checkpoint 已明确。 |
| DP 当前 py312 PTP/LDP-MH | 截至最后记录仍在训练，约 epoch 821 / 842。 |
| DP py39 PTP/LDP-MH | 截至最后记录仍在训练，约 epoch 548 / 561。 |

## 需要在汇报中标注“不确定”的点

| 问题 | 当前判断 |
| --- | --- |
| SmolVLA 是否天然不适合 Square？ | 不能这么下结论。只能说当前 tested recipe 在这些数据/环境组合下较弱。 |
| 是否主要是 specialist vs generalist 问题？ | 有证据支持，但没有完全 isolate。BC-RNN 有 recurrence 和 robomimic specialist 实现；SmolVLA 是 chunked flow-style prediction。 |
| 官方 84% 是否能本地严格复现？ | 目前不能。当前环境测到 66%；严格 old-stack 被 mujoco-py / offline-study-era 依赖阻塞。 |
| PTP/LDP-MH 的“正确版本”是什么？ | 本地 PTP/LDP-MH 文件是 300 demos / 80,731 steps，且无显式 `env_version`。它在 py39 / robosuite 1.2 上部分模型更好，但这只是实验证据，不是 provenance 证明。 |
| DP LDP-MH 最终成绩是否固定？ | 还没固定。LDP-MH DP 训练仍在跑，表中是当前 best-so-far scheduled eval。 |

## 可直接放入汇报的一段话

我们在 Square 上测试了三类 baseline：官方/专用 BC-RNN、SmolVLA 和 no-history Diffusion Policy。当前最重要发现是数据和运行环境版本对齐会显著影响成功率。对齐后的 official-PH v1.4.1 image BC-RNN 可以达到 `40/50 = 80%`，接近 robomimic 官方报告；但较新的 SmolVLA 在相同任务上当前最好只有 `16/50 = 32%`。DP 是比当前 SmolVLA 更强的现代 baseline，在 current stack + official-PH v1.4.1 上达到 `34/50 = 68%`，但也明显受数据/环境组合影响。现有证据支持两个判断：第一，Square 实验必须严格控制数据版本和 runtime 版本；第二，在当前参数下，Square 仍更偏向 specialist recurrent policy 或经过调好的 DP-style policy，而不是我们测试的 SmolVLA recipe。
