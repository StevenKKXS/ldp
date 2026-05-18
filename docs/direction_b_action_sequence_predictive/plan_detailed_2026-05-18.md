# Direction B: Action-Sequence Predictive Encoder Pretraining

## 0. 文档目的

本文档用于指导 agent 并行推进第二个可能用于超越 PTP 的 encoder 改进方向: Action-Sequence Predictive Encoder Pretraining。

该方向来自“把 encoder 看作从图像/历史到动作坐标序列的翻译任务”的初始想法，但为了降低风险，本方向不直接把它做成最终 policy，而是把它作为 encoder representation pretraining。

训练完成后，丢掉 action prediction decoder，仅保留 encoder，并将 encoder embedding 接入 PTP / diffusion policy。

本方向允许保存和维护历史实验信息。每次实验、讨论或 debug 后，agent 需要把关键 observation 记录到 `obs_log.md` 中，形成持续更新的文档库。

## 1. 核心想法

PTP 通过 Past-Token Prediction 让 diffusion policy 同时预测过去动作和未来动作，从而改善长历史建模。但我们希望进一步验证:

```text
如果在进入 diffusion policy 之前，先让 history encoder 学会从观测历史中预测过去和未来专家动作序列，是否可以得到更好的 action-predictive belief representation？
```

训练形式:

```text
历史观测 / 当前观测 + 历史动作
        ↓
encoder
        ↓
z_t
        ↓
lightweight action decoder
        ↓
predict past + current + future action sequence
```

预训练完成后:

```text
保留 encoder，丢弃 action decoder，将 z_t 接入 PTP / diffusion policy。
```

## 2. 和完整翻译任务的区别

初始发散想法是:

```text
image/history tokens -> coordinate sequence
```

这像一个从图像到动作坐标序列的翻译任务。

但完整翻译任务有风险:

1. 容易退化成普通 behavior cloning。
2. 对多模态动作可能产生平均化问题。
3. 如果 decoder 太强，encoder 不一定学到可迁移的 belief representation。
4. 会和 diffusion policy 的作用重叠。

因此，本方向采用弱化版本:

```text
不是用 action decoder 作为最终 policy，
而是用 action-sequence prediction 作为 encoder pretraining objective。
```

最终 policy 仍然是 PTP / diffusion policy。

## 3. 主要假设

### Hypothesis B1: 动作序列预测可以训练出 action-predictive history representation

如果 encoder 能从历史观测中预测过去、当前和未来动作，那么它应该编码了与控制相关的历史状态信息。

### Hypothesis B2: past + future prediction 比 future-only prediction 更适合长历史任务

PTP 的核心思想说明 past-token prediction 有助于建模历史连续性。我们希望把这个思想前移到 encoder pretraining 中。

需要比较:

```text
future-only prediction
vs
past + future prediction
```

如果 past + future 更好，说明 encoder 端也受益于过去动作重建。

### Hypothesis B3: encoder pretraining 可以缓解 diffusion loss 对上游 encoder 监督不直接的问题

如果预训练 encoder 接入 PTP 后提升性能，说明单纯 end-to-end diffusion training 可能没有充分训练出控制相关 history representation。

## 4. 输入与模型形式

### 4.1 推荐输入

优先使用:

```text
x_t = {o_{t-H:t}, a_{t-H:t-1}}
```

即多帧观测 + 历史动作。

如果实现难度较高，可以先降级为:

```text
x_t = {o_t, a_{t-H:t-1}}
```

或者:

```text
x_t = {o_{t-H:t}}
```

必须在实验记录中明确输入形式。

### 4.2 Encoder

```text
z_t = Enc(x_t)
```

建议第一版使用和 Direction A 相同或类似的 encoder 架构，方便后续比较。

### 4.3 Lightweight Action Decoder

```text
A_hat = Dec(z_t)
```

Decoder 只用于预训练阶段。接入 PTP 时丢弃 decoder。

Decoder 不宜过强，否则可能 decoder 自己记住轨迹模式，削弱 encoder 的学习压力。

第一版优先:

```text
MLP decoder
```

可选:

```text
small transformer decoder with learned action queries
```

## 5. 预测目标

### 5.1 Future-only prediction

```text
A_t+ = a_{t:t+K}
```

训练:

```text
Dec(Enc(x_t)) -> A_t+
```

### 5.2 Past + future prediction

```text
A_t = a_{t-P:t+K}
```

训练:

```text
Dec(Enc(x_t)) -> A_t
```

其中包含:

```text
过去动作 a_{t-P:t-1}
当前动作 a_t
未来动作 a_{t+1:t+K}
```

推荐第一轮重点测试这个版本。

### 5.3 Masked action prediction

Masked action prediction 可作为第二阶段。

形式:

```text
Dec(z_t, masked_action_queries) -> masked action tokens
```

这个版本更接近 representation pretraining，而不是简单回归完整动作序列，但实现成本更高，不作为第一版必做。

## 6. Loss 设计

### 6.1 基础预测 loss

推荐:

```text
L_pred = Huber(A_hat, A_target)
```

也可以测试:

```text
MSE
L1
```

第一版建议 Huber，因为对异常动作值更稳。

### 6.2 Action normalization

必须确认动作是否 normalize。

建议:

```text
对 action chunk 使用 dataset mean/std normalize；
loss 在 normalized action space 上计算。
```

记录:

```text
action normalization method
mean/std 是否使用 train set 统计
是否包含 gripper/action mode 维度
```

### 6.3 Delta action prediction

如果直接预测绝对动作不稳定，可以改成:

```text
Delta A_t = a_t - a_{t-1}
```

或者:

```text
predict action residual / velocity-like signal
```

第一版不强制。

## 7. 接入 PTP / Diffusion Policy

原 plan 推荐 concat:

```text
condition = concat(original_PTP_condition, z_t)
```

但结合 Direction A 的 review 更新和用户要求，第一版应优先保持 PTP policy 结构不变。也就是说，predictive decoder 只作为 encoder pretraining head，最终 policy 仍通过现有 PTP encoder checkpoint loading 路径使用预训练 encoder。

Frozen / finetune 必须测试:

```text
frozen pretrained encoder
finetuned pretrained encoder
```

## 8. 实验任务顺序

### Phase 1: 优先任务

先测试:

```text
Square
ToolHang
```

### Phase 2: 扩展任务

如果 Phase 1 中至少一个任务有明显提升，继续测试:

```text
Push-T
Transport
```

## 9. 第一轮实验矩阵

### 9.1 Baselines

```text
B1. PTP baseline
B2. PTP + same encoder architecture, no predictive pretraining
```

B2 用于控制参数量和架构变化。

### 9.2 Ours

```text
O1. PTP + future-only predictive encoder, frozen
O2. PTP + past+future predictive encoder, frozen
O3. PTP + past+future predictive encoder, finetuned
```

如果时间有限，优先做:

```text
B1, B2, O2, O3
```

因为 past+future 是本方向最贴近 PTP 的核心版本。

### 9.3 第二轮可选实验

如果 O2/O3 有提升，再做:

```text
O4. PTP + masked action predictive encoder, frozen
O5. PTP + masked action predictive encoder, finetuned
O6. PTP + delta-action predictive encoder
```

## 10. 关键判断标准

### 10.1 predictive pretraining 是否有效

```text
O2 > B2
```

说明 action-sequence predictive pretraining 有用。

### 10.2 past+future 是否优于 future-only

```text
O2 > O1
```

说明过去动作预测确实帮助 encoder 保留历史连续性。

```text
O1 >= O2
```

说明 future behavior 可能已经足够，过去动作重建可能引入冗余或噪声。

### 10.3 frozen vs finetune

```text
O2 > O3
```

说明 frozen action-predictive representation 更稳定，diffusion finetune 可能破坏 encoder。

```text
O3 > O2
```

说明 predictive pretraining 是有效初始化，后续 end-to-end diffusion finetune 仍有收益。

### 10.4 是否只是参数量增加

```text
B2 ~= B1 或 B2 < O2
```

则更能说明提升来自 pretraining，而非架构增大。

## 11. 和 Direction A 的关系

Direction A:

```text
用未来动作相似性组织 embedding 空间。
```

Direction B:

```text
让 embedding 可解码出 past/future action sequence。
```

两者可以并行推进，但第一轮不要混合，否则难以判断单独贡献。

后续如果两者都有效，可以测试组合版本:

```text
L = L_pred + lambda * L_contrast
```

组合版本暂时不作为第一轮任务。

## 12. 需要记录的实验信息

每次实验必须记录:

```text
任务名
数据集版本
代码 commit / branch
PTP baseline checkpoint
encoder 输入形式
history length H
past prediction length P
future prediction length K
decoder 类型
loss 类型
是否 action normalize
是否预测 delta action
是否 masked prediction
是否 frozen encoder
是否 finetune encoder
best score
best epoch
current epoch
训练是否稳定
预测 loss 曲线
downstream score
失败现象
初步判断
```

## 13. 需要特别观察的现象

重点记录:

1. action prediction loss 是否稳定下降。
2. pretraining loss 低是否真的对应 downstream score 高。
3. future-only 和 past+future 哪个更好。
4. frozen 和 finetune 哪个更好。
5. 是否出现预测 loss 很低但 policy score 不涨。
6. 是否在 ToolHang 上比 Square 更有效。
7. 是否对 Push-T 这种简单任务无收益。
8. 是否预测 past action 带来明显帮助。
9. 是否 decoder 太强导致 encoder 表征迁移差。
10. 是否需要 masked prediction 或 delta action prediction。

## 14. Observation Log

Observation 记录在 `docs/direction_b_action_sequence_predictive/obs_log.md`。

## 15. Current Status

```text
Status: Candidate direction, not yet validated.
Priority: Medium-high.
First tasks: Square, ToolHang.
Expansion tasks: Push-T, Transport.
Main risk: Method may collapse into ordinary BC-style pretraining and not improve diffusion policy.
Main expected value: Simple, direct, low-engineering-cost encoder pretraining signal.
```
