# ACT-size Translator 与 Proprio Shortcut 汇报稿

日期：2026-06-03

这份稿子只保留汇报主线：

```text
把原始 BehaviorTranslator 放大到 ACT-size
    -> 观察是否解决表示能力不足
    -> 发现 past-action loss 变好，但主要来自 proprio shortcut
```

不展开 raw-action-loss、official ACT、deterministic ACT-style baseline 等支线。

## 1. 一句话结论

我们把原始 translator 放大到 ACT-like 参数规模后，past action reconstruction 的 offline L1 确实更好；但进一步诊断发现，这个改进主要可能来自 lowdim/proprio 对 past action 的强预测能力，而不是模型学到了 image-grounded behavior representation。

因此这条结果的汇报口径应该是：

```text
scale-up 说明 capacity 不是唯一瓶颈；
proprio shortcut 说明当前 Stage 1 目标没有迫使模型利用图像；
所以 v0 translator 不能直接作为有效的下游 DP/PTP context。
```

## 2. 原始 Translator 做什么

Stage 1 translator 的目标是：

```text
obs history -> sketch action prediction
```

在 Square 上的输入包括两类观测：

```text
image:
  agentview_image
  robot0_eye_in_hand_image

lowdim / proprio:
  robot0_eef_pos        # 末端位置, 3维
  robot0_eef_quat       # 末端姿态四元数, 4维
  robot0_gripper_qpos   # 夹爪状态, 2维
```

数据流：

```text
raw RGB + lowdim obs window
        |
        v
trainable robomimic obs encoder
        |
        v
obs tokens [B, H=16, Do=137]
        |
        v
BehaviorTranslator
  ObsProjector
  CausalObsEncoder
  ActionQueryDecoder
  SketchActionHead
        |
        v
predicted action tokens [B, P+K, Da=10]
```

当前主实验使用 `target_mode=past`，即主要优化：

```text
obs history o_{t-H+1:t}
    -> past actions a_{t-P:t-1}
```

其中常用：

```text
H = 16
P = 16
K = 8
Da = 10
```

## 3. 为什么要放大到 ACT-size

原始 d256 translator 没有带来 downstream 提升后，有一个自然怀疑：

```text
是不是 translator 太小，学不出足够强的 history representation？
```

所以我们做了一个最直接的 scale-up：

```text
保持任务、数据、输入、目标不变；
只把 BehaviorTranslator 的 transformer 几何放大到 ACT-like size。
```

结构对比：

| 模块 | 原始 d256 translator | ACT-size translator |
|---|---:|---:|
| `d_model` | 256 | 512 |
| obs encoder layers | 4 | 4 |
| action decoder layers | 2 | 7 |
| attention heads | 4 | 8 |
| FFN hidden dim | 1024 | 3200 |
| context dim | 512 | 512 |

参数量对比：

| 模型 | core params | full params, including Robomimic obs encoder |
|---|---:|---:|
| d256 translator | 5.776M | 28.170M |
| ACT-size translator | 56.177M | 78.571M |

这基本把 translator core 从约 `5.8M` 扩到约 `56.2M`，接近 ACT-style transformer 的参数规模。

## 4. ACT-size Translator 结果

Stage 1 offline validation 结果：

| Run | Epochs | Best epoch | Best val total | Best val past L1 | Best val future L1 |
|---|---:|---:|---:|---:|---:|
| d256 translator, obs lr 1e-4 | 178 | 110 | 0.000485 | 0.01172 | 0.06096 |
| d256 translator, obs lr 5e-5 | 178 | 129 | 0.000524 | 0.01261 | 0.06708 |
| ACT-size translator | 507 | 430 | 0.002727 | 0.00917 | 0.08539 |

注意：

- ACT-size run 的 `loss_total` 和 d256 不直接可比，因为 loss reduction / loss scale 改过。
- 更可靠的横向比较是 L1。
- ACT-size 把 past L1 从约 `0.01172` 降到 `0.00917`，说明更大模型确实更会拟合 past-action reconstruction。
- 但 future L1 没有同步变好，说明它不一定学到了对未来行为更有用的状态。

阶段性解释：

```text
放大模型能够降低 past-action prediction error；
但这不等价于学到了更好的 image-grounded behavior context。
```

这引出了 shortcut 诊断。

## 5. 什么是 Proprio Shortcut

这里的 proprio / lowdim 指：

```text
robot0_eef_pos
robot0_eef_quat
robot0_gripper_qpos
```

它不是非法信息，因为这些量在训练和 eval 时都能拿到。问题在于，对当前 Stage 1 的 past-action reconstruction 来说，它可能太强。

原因是：

```text
past action a_{t-P:t-1}
    已经影响了后续 robot state

obs history o_{t-H+1:t}
    包含这些 action 执行后的 eef/gripper 状态变化
```

因此模型可以学到近似关系：

```text
eef position / orientation / gripper state 的时间变化
    -> 近期 robot motion / gripper trend
    -> past action
```

这条路径不需要理解图像里的 object pose、contact state、task phase。

换句话说，当前目标可能变成了：

```text
从 robot state trajectory 反推过去动作
```

而不是我们希望的：

```text
从 image + proprio history 中学习 task-aware behavior state
```

这就是 proprio shortcut。

## 6. Shortcut 实验 1：checkpoint perturbation

实验设计：

```text
固定训练好的 translator checkpoint
在 eval 时分别扰动 image 或 proprio
观察 action prediction loss 怎么变
```

扰动类型：

```text
baseline:       正常输入
image zero:     把 image feature 置零/替换为均值
image shuffle:  打乱 image 对应关系
proprio zero:   把 proprio feature 置零/替换为均值
proprio shuffle:打乱 proprio 对应关系
```

d256 translator quick check：

| Condition | val total | past L1 | 解读 |
|---|---:|---:|---|
| baseline | 0.000800 | 0.01737 | 正常 |
| image zero | 0.002051 | 0.03078 | 变差，但不灾难 |
| image shuffle | 0.002043 | 0.01957 | 接近 baseline |
| proprio zero | 0.233882 | 0.56714 | 灾难性变差 |
| proprio shuffle | 0.006923 | 0.03096 | 明显变差 |

ACT-size translator micro check：

| Condition | val total | past L1 | 解读 |
|---|---:|---:|---|
| baseline | 0.002205 | 0.01598 | 正常 |
| image zero | 0.006270 | 0.02231 | 小到中等变差 |
| image shuffle | 0.002401 | 0.01659 | 几乎不变 |
| proprio zero | 2.446047 | 0.52645 | 灾难性变差 |
| proprio shuffle | 0.002468 | 0.01734 | micro batch 下几乎不变 |

解释：

```text
去掉 proprio 后 loss 爆炸；
扰动 image 后 loss 远没有同量级恶化。
```

这个实验说明 translator 的预测强依赖 proprio。但 shuffle 结果要谨慎，因为 micro batch 内 shuffle 不一定构造了足够强的跨 episode 扰动。

## 7. Shortcut 实验 2：lowdim-only vs image-only retrain

为了避免只看 checkpoint perturbation 的不稳定性，我们又做了从头训练的输入消融。

实验设计：

```text
使用同样的 ACT-size translator 训练设置
分别训练：
  full input:    image + lowdim
  lowdim-only:  只保留 proprio / lowdim
  image-only:   只保留两路 image

比较 20 epoch 左右的 validation past L1。
```

结果：

| Input | Best epoch | Best val total | Best past L1 | Best future L1 | 解读 |
|---|---:|---:|---:|---:|---|
| full input, ACT-size e20 reference | 20 | 0.00638 | 0.01211 | 0.07398 | image + lowdim |
| lowdim-only | 20 | 0.00533 | 0.01264 | 0.06974 | 接近 full |
| image-only | 18 | 0.01141 | 0.02054 | 0.07031 | past prediction 明显更差 |

这是更干净的证据：

```text
lowdim-only ~= full input
image-only 明显差于 full input
```

说明当前 past-action objective 下，模型几乎可以靠 lowdim/proprio 拟合到接近 full input 的水平。

## 8. 应该如何汇报这个现象

建议这样讲：

```text
我们最初怀疑 translator 不 work 是因为模型容量不足，
所以将其放大到 ACT-size。

结果发现：
  放大后 past action prediction 确实更好，
  但这种更好主要体现在 past reconstruction，
  没有自然转化为更好的 future/context 表示。

进一步诊断发现：
  lowdim/proprio alone 几乎能达到 full input 的 past L1，
  而 image-only 明显更差；
  eval-time 去掉 proprio 会导致 loss 灾难性上升，
  去掉或打乱 image 的影响小得多。

因此当前 v0 translator 的主要失败模式不是单纯模型太小，
而是 Stage 1 目标存在 proprio shortcut。
```

## 9. 结论与下一步

当前结论：

```text
ACT-size scale-up 排除了“模型太小”作为唯一解释；
proprio shortcut 解释了为什么 Stage 1 loss 能下降但 downstream context 不一定有用。
```

如果继续这个方向，下一步不应只是继续 scale up，而应改变训练目标或输入约束：

```text
1. Stage 1 加 proprio dropout，让模型被迫使用 image。
2. 避免 pure past-action reconstruction 作为唯一主目标。
3. 加入更 image-grounded 的目标，例如 object/contact/task phase 相关预测。
4. downstream 前先验证 pretrained representation 是否比 random representation 更依赖 image。
```

这条汇报主线的最终落点是：

```text
我们发现了 v0 translator objective 的关键问题：
它太容易通过 proprio shortcut 完成 past-action prediction；
后续若要让 translator 真正帮助 DP/PTP，必须先让 Stage 1 表示学习具备 image-grounded 约束。
```
