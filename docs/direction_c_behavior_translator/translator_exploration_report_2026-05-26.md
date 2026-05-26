# Behavior Translator 方向探索汇报

Date: 2026-05-26  
Owner: `intern_ldp_explorer`  
Scope: Direction C, Behavior Translator Context for DP/PTP

## 1. 一句话结论

Behavior Translator 方向目前最强的证据是：

> 用 observation history 预测 `past action` 的 translator，能学到比同结构 random translator 更有用的 offline behavior context；但这个 context 是否能稳定提升 DP/PTP rollout 成功率，还没有被 corrected downstream rollout 证明。

当前判断：

- `past` 是最稳的 Stage 1 translator 目标。
- `future` 与 `past_future` 更接近原始直觉，但在当前设置下验证 loss 很早变差，说明未来动作直接预测更受多模态和目标噪声影响。
- Stage 2a frozen-head probe 已经给出正信号：pretrained `past` context 明显优于 frozen random context。
- 旧 Stage 2b rollout 混合且不可作为最终证据，因为后来发现 action8 transformer 的 condition mask 会让最新 obs 与 `add_last` context 不可见。
- corrected Stage 2b 正在 Ceph-only 环境重跑；目前只有 M1/M3 的 offline checkpoint，M2/M4 pretrained context 还未到可比 checkpoint。

## 2. 原始问题与实验假设

最初的目标不是让 translator 直接成为最终 policy，而是验证一个更窄的问题：

```text
obs history -> translator -> behavior-aware hidden state
```

这个 hidden state 是否能作为额外 condition，帮助下游 DP/PTP 生成更精细的 future action chunk。

核心判据设计为：

```text
DP/PTP + pretrained frozen translator context
>
DP/PTP + same-architecture frozen random translator context
```

如果 pretrained context 优于 random context，说明收益不是单纯来自多加参数或多加 token，而是来自 history-action 对齐表征。

## 3. 初始实验规划

原始规划分三阶段：

| Stage | 目标 | 问题 |
|---|---|---|
| Stage 1 | 训练 translator：obs history -> action sketch | hidden state 是否学到历史行为对齐 |
| Stage 2a | freeze translator，训练简单 future-action head | pretrained context 是否比 random context 更好用 |
| Stage 2b | 将 translator context 接入 DP/PTP | offline 表征能否转化为 rollout 成功率 |

第一版刻意不做这些复杂模块：

- 显式 action encoder
- VQ/action tokenizer
- latent diffusion / flow matching
- future obs prediction
- EMA teacher
- contrastive loss

原因是先验证最核心假设：history-to-action translation 是否能产生有用 condition。

## 4. 数据与窗口构造

主实验使用 Square/mh `image_abs.hdf5`，raw image/proprio 输入，encoder 参与训练。

当前设置：

```text
H = 16  obs history
P = 16  past action horizon
K = 8   future action horizon
```

以 anchor `t` 为中心：

```text
obs_hist   = o[t-15 : t]
act_past   = a[t-16 : t-1]
act_future = a[t : t+7]
```

在代码里对应：

```text
sequence_length = 24
anchor = 16
obs indices = 1..16
past action indices = 0..15
future action indices = 16..23
```

当前 Square/mh split：

| 项 | 数量 |
|---|---:|
| demos | 300 |
| total frames | 80,731 |
| train demos | 294 |
| val demos | 6 |
| train windows | 79,289 |
| val windows | 1,442 |

由于 `sequence_length=24,pad_before=16,pad_after=7`，每条 demo 长度为 `L` 时，sampler window 数为：

```text
L - 24 + 16 + 7 + 1 = L
```

因此当前每个 frame 对应一个 temporal window。train/val 按 episode 切分，不跨 demo。

## 5. 实现内容

已实现的关键文件：

| 模块 | 文件 |
|---|---|
| translator dataset | `diffusion_policy/dataset/behavior_translation_dataset.py` |
| translator model | `diffusion_policy/model/behavior_translator.py` |
| Stage 1 workspace | `diffusion_policy/workspace/train_behavior_translator_workspace.py` |
| Stage 2a head probe | `diffusion_policy/workspace/train_translator_head_workspace.py` |
| Stage 2b policy | `diffusion_policy/policy/translator_conditioned_transformer_hybrid_image_policy.py` |
| corrected transformer mask | `diffusion_policy/model/diffusion/transformer_for_diffusion.py` |

主模型结构：

```text
raw obs history
  -> robomimic obs_encoder
  -> BehaviorTranslator
      -> causal obs encoder
      -> action-query decoder
      -> sketch action head
      -> behavior_context
```

Stage 2b 的最小接入方式：

```text
base DP/PTP condition tokens
  + projected translator context
  -> diffusion transformer
```

## 6. Stage 1：translator 预训练探索

### 6.1 初始对比

先跑了三类目标：

| Objective | 监督目标 | 初始目的 |
|---|---|---|
| `past` | `a[t-16:t-1]` | 学历史 obs-action 对齐 |
| `future` | `a[t:t+7]` | 直接学未来行为趋势 |
| `past_future` | both | 同时学历史解释与未来趋势 |

### 6.2 主要结果

| Objective | 观察 | 代表结果 |
|---|---|---|
| `past` | 最稳定，验证 loss 低，长训后仍可用 | formal best `0.000455 @ e113`; tuned best `0.000434 @ e118` |
| `future` | train loss 下降，但 val 很早最优后变差 | early best `0.008961 @ e4` |
| `past_future` | 概念上最接近原设想，但 future 部分噪声更大 | equal-weight best `0.010111 @ e4`; `w_future=0.5` best `0.006501 @ e4` |

### 6.3 阶段判断

原始规划里，`past_future` 是最自然的主 translator，因为它同时要求模型解释历史行为并预测未来动作。但实验后判断发生了变化：

- `past` 更像稳定的 representation pretraining 目标。
- `future` 容易被多模态行为影响：相同 observation history 下，未来 action 可能有多个合理分支。
- `past_future` 的 future loss 会拖累整体验证曲线；降低 `w_future` 有帮助，但仍弱于 `past`。

因此，Stage 1 的主线从“优先 past+future”修正为：

```text
先用 past translator 做 behavior-context 主线，
把 future/past_future 作为 ablation 和后续改进方向。
```

## 7. Stage 2a：frozen-head representation probe

### 7.1 设计

Stage 2a 不做 rollout，只回答：

```text
frozen translator context 是否能让一个简单 head 更好预测 future action
```

对照：

| ID | Context | Head | 目的 |
|---|---|---|---|
| H1 | frozen random translator | MLP | 排除结构/参数量影响 |
| H2 | frozen pretrained `past` translator | MLP | 验证表征 |
| H3 | pretrained `past` finetune | MLP | 看微调是否有收益 |
| H4 | pretrained `past_future` | MLP | 检查更接近原目标的 translator |

### 7.2 结果

| Context | Frozen | Offline val loss | Future L1 | 判断 |
|---|---:|---:|---:|---|
| random translator | yes | `0.011571` | `0.06736` | baseline |
| pretrained `past` e50 | yes | `0.007839` | `0.04917` | 明显优于 random |
| pretrained `past` best/latest | yes | `0.00796-0.00803` | - | 信号稳定 |
| pretrained `past` finetune | no | `0.008056` 左右 | - | 没有明显优于 frozen |
| pretrained `past_future` | yes | `0.0106-0.0136` | - | 弱于 `past` |

### 7.3 阶段判断

Stage 2a 给出正信号：

```text
pretrained past context > frozen random context
```

这说明 `past` translator hidden state 确实包含 future-action probe 可用的信息。  
但 Stage 2a 只是 offline action prediction，不产生环境成功率。

因此，当时推进到 Stage 2b 是合理的。

## 8. Stage 2b：接入 DP/PTP 后的混合结果

### 8.1 旧 Stage 2b 结果

旧实验中，translator context 接入 transformer DP/PTP 后，rollout 结果不稳定：

| Setting | Rollout 结果 |
|---|---:|
| add-all pretrained e24 | `0/10` |
| add-all random e24 | `2/10` |
| add-all pretrained e49 | `2/10` |
| add-all random e49 | `5/10` |
| add-all pretrained e99 | `4/10` |
| add-all random e99 | `3/10` |
| nonzero-projector pretrained e99 | `4/10` |
| add-last pretrained e49 | `4/10` |
| add-last random e49 | `0/10` |

当时初步观察：

- `add_all` 并没有稳定帮助，甚至多次弱于 random。
- `add_last` 有一个看起来正向的点，但只有 10 seeds，不够稳。
- base no-context 结果当时缺失或不完整。

这促使我回到模型结构本身检查 context 是否真的被 action decoder 使用。

## 9. 关键诊断：condition mask 让最新 obs/context 不可见

旧 action8 设置：

```yaml
policy.horizon: 8
policy.n_obs_steps: 16
policy.causal_attn: true
policy.n_cond_layers: 0
```

在 `TransformerForDiffusion` 里，causal memory mask 使 action token `0..7` 只能 attend 到 obs condition token `0..7`。

问题是：

```text
obs token 8..15 完全不可见
```

这意味着：

- 最新/current obs token 不可见。
- `context_injection=add_last` 注入到 token 15，实际被 mask 掉。
- `add_all` 虽然影响 token 0..7，但那是更老的 history，而不是当前观测附近的信息。

我做了两个验证：

| 验证 | 结果 |
|---|---|
| perturbation visibility | 旧设置只有 obs token `0..7` 能影响输出；关闭 condition causal mask 后 `0..15` 都可见 |
| gradient visibility | 旧设置 obs token `8..15` 梯度为 0；修正后全 history token 有非零梯度 |

### 9.1 代码修正

增加参数：

```python
causal_cond_attn: bool = True
```

默认保持旧行为；corrected long-history action8 设为：

```yaml
policy.causal_cond_attn: false
```

### 9.2 规划修正

旧 Stage 2b rollout 被降级为 diagnostic，不作为最终 evidence。  
下一组正式 downstream 对照改为：

| ID | Policy | Context | Injection | `causal_cond_attn` | 目的 |
|---|---|---|---|---:|---|
| M1 | base transformer | none | none | false | corrected no-context baseline |
| M2 | translator-conditioned | pretrained `past` | add_last | false | 主实验 |
| M3 | translator-conditioned | random | add_last | false | random control |
| M4 | translator-conditioned | pretrained `past` | add_all | false | 检查全局注入 |

## 10. 当前 Ceph-only corrected 实验状态

NFS/3FS 下线后，实验迁移到 Ceph：

```text
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator
```

环境：

```text
Python 3.9
robomimic==0.2.0
torch 2.5.1+cu124
```

### 10.1 Stage 1 Ceph 重训

| Run | Best val/loss_total | 判断 |
|---|---:|---|
| `obs_lr=1e-4,tr_lr=1e-4` | `0.000689 @ e17` | 当前 Ceph 中较好 |
| `obs_lr=5e-5,tr_lr=1e-4` | `0.000724 @ e22` | 接近，但略弱 |
| historical NFS tuned `past` | `0.000434 @ e118` | 历史最好 |

判断：Ceph 重训可用，但还没达到历史 tuned best。

### 10.2 Corrected Stage 2b offline

| ID | Setting | 当前结果 |
|---|---|---:|
| M1 | base no-context | best offline `val_loss=0.057315 @ e22`; e24 `0.058112` |
| M3 | random context add_last | best offline `val_loss=0.058737 @ e22`; e24 `0.058755` |
| M2 | pretrained `past` add_last | 已启动，尚未到可比 checkpoint |
| M4 | pretrained `past` add_all | 已启动，尚未到可比 checkpoint |

当前 offline 初步判断：

- M1 base 略好于 M3 random context。
- 这不说明 translator 不行，只说明“随机 context/多参数”没有自然带来提升。
- 真正关键仍是 M2 是否优于 M3，并且是否不弱于 M1。

### 10.3 Rollout 状态

还没有 corrected rollout success rate。

原因：

- Stage 2b 训练配置里 rollout 被关闭：`rollout_every=999999`, `n_test=0`。
- 训练只做 offline validation。
- success rate 需要 checkpoint 后单独跑 reward-only rollout。
- Ceph py39 环境还缺 rollout runtime：`robosuite` 缺失，`mujoco_py` OSMesa 编译缺 `GL/osmesa.h`。

## 11. 速度与系统瓶颈判断

当前 H200 训练不是 GPU 算力跑满，也不是文件读取阻塞。

Live profiling 结果：

| 指标 | 观察 | 解释 |
|---|---:|---|
| iowait | `0%` | 不是磁盘/Ceph 读取瓶颈 |
| block input | near `0` | step 中没有持续读盘 |
| CPU 全机使用 | 约 `13%` user, `86-87%` idle | 不是整机 CPU 饱和 |
| GPU util | 大量 `0%`，偶尔 spike 到 `70-80%` | GPU 被脉冲式喂数据 |
| Stage2b speed | 约 `1.6-1.7 it/s` | batch 构造/传输节奏慢 |

主要瓶颈：

```text
CPU-side raw image batch construction
ColorJitter
numpy/torch copies
DataLoader IPC
/dev/shm=16G 限制 workers
```

这也解释了为什么数据总量不算特别大，但 wall-clock 仍慢：每个 sample 包含 16 步 history、两路相机图像以及 CPU augmentation。

## 12. 从原始规划到当前规划的修正

| 原始想法 | 实验后判断 | 当前修正 |
|---|---|---|
| `past_future` 是主 translator | equal-weight future 目标验证不稳 | 以 `past` 为主线，`past_future` 做 ablation |
| Stage 1 offline loss 可直接指导 downstream | Stage 2a 支持 `past`，但 Stage 2b 可能受结构问题影响 | Stage 2a 是 go/no-go，Stage 2b 必须做结构可见性检查 |
| add-last 是干净注入 | 旧 mask 下 add-last 实际不可见 | corrected `causal_cond_attn=false` 后重跑 |
| old rollout 可以初步判断 | old rollout 受 mask bug 影响 | 旧结果只保留为 diagnostic |
| 多开训练充分利用 GPU 就好 | 多 run 共 GPU 会拖慢单个 run | 关键对照应优先独占 GPU 或提高 DataLoader 吞吐 |
| rollout 等训练自然产生 | 训练配置关闭 rollout | checkpoint 后单独跑 reward-only rollout |

## 13. 接下来计划

### 13.1 必做：补齐 corrected rollout

优先修 Ceph rollout runtime：

```text
robosuite
mujoco_py + OSMesa / EGL runtime
reward-only rollout script
```

然后先跑已有 checkpoint：

| Priority | Eval |
|---:|---|
| 1 | M1 base e24 rollout |
| 2 | M3 random e24 rollout |
| 3 | M2 pretrained add-last first comparable checkpoint rollout |
| 4 | M4 pretrained add-all first comparable checkpoint rollout |

最终表格应包含：

```text
method, checkpoint epoch, offline val_loss, rollout success, n_test, notes
```

### 13.2 必做：让 M2/M4 到可比 checkpoint

当前 M2/M4 还没有可比 checkpoint。建议：

- 让 M2/M4 独占 GPU 或减少 M1/M3 继续训练占用。
- 如果目标是尽快得到对照，临时把 checkpoint interval 调小。
- 至少拿 e24/e25 与 M1/M3 对齐。

### 13.3 速度改进

不建议用预编码 obs 作为主路线，因为我们的目标就是训练 encoder。

建议优先：

1. 使用更大的 `/dev/shm` 或 `--ipc=host` 资源。
2. 测 `num_workers=8/16`、`persistent_workers=true`、`prefetch_factor=2`。
3. 测 batch size `64/128`，但按 optimizer step 对齐比较。
4. 暂时关闭 CPU ColorJitter 或移到 GPU 侧做速度 ablation。
5. 给 Stage2b 加 `data_time/compute_time` 日志，精确拆开 DataLoader 与模型计算。

### 13.4 若 corrected rollout 仍无收益

优先排查：

| 方向 | 原因 |
|---|---|
| context token 而不是 pooled vector | pooled context 可能丢失时序/action-side 信息 |
| projector-only finetune | 全量 finetune 可能破坏 Stage 1 表征 |
| nonzero / gated projector | zero-init 可能让 context 学得太慢 |
| token-level h_action context | action-query decoder hidden 可能比 pooled context 更有信息 |
| future weight 重新调参 | `past_future` 仍可能有价值，但需要更低 future 权重 |
| bidirectional obs encoder ablation | causal encoder 稳健，但 bidirectional 可能更适合 offline pretraining |

## 14. 建议放进飞书的图和表

### 图 1：整体 workflow 图

用途：让读者一眼看到 Stage 1/2a/2b 的关系。

```text
raw obs history
  -> obs encoder
  -> BehaviorTranslator
      -> Stage 1 action sketch loss
      -> behavior context
            -> Stage 2a MLP probe
            -> Stage 2b DP/PTP condition
```

### 图 2：数据窗口示意图

用途：解释 `H=16,P=16,K=8` 的 anchor 切片。

```text
window index:  0  1  ... 15 16 17 ... 23
obs_hist:         [1 ............. 16]
act_past:      [0 .......... 15]
act_future:                    [16 ... 23]
```

### 图 3：Stage 1 曲线

建议画：

- `past` train/val total loss
- `future` train/val total loss
- `past_future` train/val total loss
- 标注 best epoch

要表达的结论：`past` 稳定，`future/past_future` early-best 后验证变差。

### 表 1：Stage 1 objective 对比

| Objective | Best val | Best epoch | 现象 | 当前结论 |
|---|---:|---:|---|---|
| past | `0.000434` | 118 | 稳定 | 主线 |
| future | `0.008961` | 4 | early-best | 多模态强 |
| past_future | `0.006501` | 4 | 权重敏感 | ablation |

### 图 4：Stage 2a bar chart

建议画 bar：

- random frozen val loss `0.011571`
- pretrained past frozen val loss `0.007839`
- pretrained past_future frozen val loss `0.0106-0.0136`

要表达的结论：offline representation probe 支持 `past` context。

### 图 5：mask visibility heatmap

用途：解释为什么 old rollout 不能作为最终证据。

横轴：obs condition token `0..15`  
纵轴：action token `0..7`

两张图：

- old `causal_cond_attn=true`：只有 obs `0..7` 可见。
- corrected `causal_cond_attn=false`：obs `0..15` 全可见。

### 表 2：旧 Stage 2b rollout 与可信度

| Setting | Result | 是否作为最终证据 | 原因 |
|---|---:|---|---|
| add-all e49 pretrained/random | `2/10` vs `5/10` | no | old mask |
| add-all e99 pretrained/random | `4/10` vs `3/10` | no | old mask |
| add-last e49 pretrained/random | `4/10` vs `0/10` | no | add-last token 被 mask |

### 表 3：corrected Stage 2b 当前状态

| ID | Method | Context | Status | Offline |
|---|---|---|---|---:|
| M1 | base | none | e24 checkpoint | `0.058112` |
| M2 | pretrained add-last | `past` | running | pending |
| M3 | random add-last | random | e24 checkpoint | `0.058755` |
| M4 | pretrained add-all | `past` | running | pending |

### 图 6：系统瓶颈示意图

用途：解释慢在哪里。

```text
zarr cache in memory
  -> DataLoader workers
  -> CPU ColorJitter / numpy-torch copies
  -> host-to-device transfer
  -> GPU short compute burst
```

要表达的结论：不是文件读取，也不是 GPU 满载，是 input pipeline / IPC / preprocessing。

## 15. 当前需要你检查的点

我建议你重点看三个判断是否符合你的直觉：

1. 是否同意把 `past` 作为 Direction C 当前主线，而不是继续把 `past_future` 作为主线。
2. 是否同意旧 Stage 2b rollout 全部降级为 diagnostic，必须以 corrected mask 重跑为准。
3. 是否同意下一步先修 rollout runtime 并跑 M1/M3/M2/M4 的统一 reward-only rollout 表，而不是继续只看 offline val loss。

