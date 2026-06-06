# Direction C -> GMP Handoff

日期：2026-06-06

接手对象：后续在 Gated Memory Policy workspace 中继续处理 long-context / translator / memory-condition 方向的 intern。

这份文档的目的不是让接手者照搬当前 LDP 代码，而是把这轮探索的初衷、已经验证的负结果、关键卡点和建议的下一步讲清楚，避免重复跑已经确认不值得继续投入的路径。

## 1. 实验初衷

最初的问题是：

```text
translator 作为最终 policy 可能不够精细，
但它从 observation history 学到的 hidden state，
是否能成为 DP / PTP / memory policy 更好的 behavior-aware condition？
```

我们想验证的最小闭环是：

```text
Stage 1:
  obs history -> BehaviorTranslator -> sketch past/future actions
  目标：让 hidden state 学到 history-to-action alignment

Stage 2:
  freeze translator
  将 translator context 注入下游 DP/PTP
  目标：看 pretrained context 是否优于 random context

Stage 3:
  若 Stage 2 有信号，再考虑 finetune 或更深集成
```

核心 go/no-go 判据：

```text
Downstream policy + pretrained translator context
  >
Downstream policy + same-architecture random translator context
  >=
Downstream policy base
```

目前这个判据没有通过。

## 2. 当前最重要结论

当前 v0 pooled/projection translator context 是负结果。

最新 Square 300-episode rollout stability eval：

| Setting | Episodes | Success Rate |
| --- | ---: | ---: |
| `base_e49` | 300 | `166/300 = 55.33%` |
| `random_add_last_e24` | 300 | `164/300 = 54.67%` |
| `pretrained_add_last_e24` | 300 | `135/300 = 45.00%` |

早期 50-episode corrected Stage2b eval 也同向：

| Setting | Episodes | Success Rate |
| --- | ---: | ---: |
| base e24 EMA | 50 | `22/50 = 44%` |
| random context e24 EMA | 50 | `21/50 = 42%` |
| random context e49 EMA | 50 | `26/50 = 52%` |
| pretrained add_last e24 EMA | 50 | `15/50 = 30%` |
| pretrained add_all e24 EMA | 50 | `18/50 = 36%` |

因此，不建议继续在 GMP 中复刻同一个 pooled vector + additive projection 的设计，除非只是为了 sanity check。

更准确的结论是：

```text
当前失败的是 v0 pooled/projection context injection，
不是所有 history-aware hidden state / memory-token 方案。
```

## 3. 当前代码与环境位置

权威代码分支：

```text
/work-agents/intern_ldp_explorer/ldp
branch: intern_ldp_explorer/task002_flow_matching_square_toolhang
```

Ceph 执行副本：

```text
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/repos/ldp
```

注意：Ceph 执行副本没有 `.git`，只作为运行拷贝。可追溯代码以 GitHub 分支为准。

主实验环境：

```text
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph
Python 3.9.25
torch 2.5.1+cu124
robomimic 0.2.0
robosuite 1.2.0
hydra 1.2.0
diffusers 0.11.1
```

运行前必须检查：

```bash
VENV=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph
"$VENV/bin/python" diffusion_policy/scripts/check_main_runtime_env.py --require-cuda
```

Square 数据：

```text
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/datasets/robomimic/datasets/square/mh/image_abs.hdf5
```

ToolHang 注意事项：

```text
当前 Ceph Direction C tree 中没有确认可用的 ToolHang image_abs.hdf5。
若 GMP 接手要跑 ToolHang，需要先恢复数据路径或明确使用哪个 live dataset。
```

## 4. 关键实现文件

Stage1 translator：

```text
diffusion_policy/model/behavior_translator.py
diffusion_policy/workspace/train_behavior_translator_workspace.py
experiment_configs/square/behavior_translator_square_past.yaml
experiment_configs/square/behavior_translator_square_future.yaml
experiment_configs/square/behavior_translator_square_past_future.yaml
experiment_configs/square/behavior_translator_square_past_actsize_norm.yaml
experiment_configs/square/behavior_translator_square_past_actsize_rawloss.yaml
```

Downstream context injection：

```text
diffusion_policy/policy/translator_conditioned_transformer_hybrid_image_policy.py
experiment_configs/square/transformer_square_action8_causalcond_off_base.yaml
experiment_configs/square/transformer_square_random_context_action8_causalcond_off_add_last.yaml
experiment_configs/square/transformer_square_translator_context_action8_causalcond_off_add_last.yaml
experiment_configs/square/transformer_square_translator_context_action8_causalcond_off_add_all.yaml
```

Rollout eval：

```text
eval_flow_matching_rollout.py
tools/direction_c_launch_square_rollout_stability_nenv8_max8.sh
```

相关报告：

```text
docs/direction_c_behavior_translator/square_rollout_stability_eval_2026_06_06.md
docs/direction_c_behavior_translator/scaleup_shortcut_report_2026_06_02.md
docs/direction_c_behavior_translator/action_generation_dataflow_report_2026_06_02.md
docs/direction_c_behavior_translator/to_be_improved.md
```

## 5. Translator 数据流

当前 translator 的输入是 Robomimic observation history：

```text
image:
  agentview_image
  robot0_eye_in_hand_image

lowdim / proprio:
  robot0_eef_pos
  robot0_eef_quat
  robot0_gripper_qpos
```

Square action8 常用维度：

```text
H = 16 observation history
P = 16 past action horizon
K = 8 future action horizon
Da = 10 action dim
Do = 137 encoded obs dim
```

Stage1 模型：

```text
raw obs history
  -> robomimic obs_encoder per timestep
  -> obs_tokens [B, H, 137]
  -> ObsProjector
  -> causal TransformerEncoder
  -> z_obs [B, H, D]
  -> learned action queries cross-attend to z_obs
  -> h_action [B, P+K, D]
  -> SketchActionHead -> predicted actions [B, P+K, Da]
  -> pooled context projector -> context [B, 512]
```

关键卡点：

```text
Stage1 loss 直接监督 SketchActionHead 的 action prediction。
下游用的是 pooled context / context_projector。
这个 exported context 没有被 Stage1 单独约束成 downstream-useful representation。
```

这很可能是 downstream 失败的一部分原因。

## 6. Proprio Shortcut 经验

最重要的经验教训是：当前 past-action translation objective 很容易走 proprio / lowdim shortcut。

checkpoint perturbation：

| Condition | d256 past L1 | ACT-size past L1 | Readout |
| --- | ---: | ---: | --- |
| baseline | `0.01737` | `0.01598` | normal |
| image zero | `0.03078` | `0.02231` | worsens, but not catastrophic |
| image shuffle | `0.01957` | `0.01659` | close to baseline |
| proprio zero | `0.56714` | `0.52645` | catastrophic |
| proprio shuffle | `0.03096` | `0.01734` | weaker than zeroing; micro-batch caveat |

lowdim-only / image-only retrain, ACT-size normalized past setup, 20 epoch budget：

| Input | Best val total | Best past L1 | Best future L1 | Readout |
| --- | ---: | ---: | ---: | --- |
| full input reference e20 | `0.00638` | `0.01211` | `0.07398` | image + lowdim |
| lowdim-only | `0.00533` | `0.01264` | `0.06974` | close to full |
| image-only | `0.01141` | `0.02054` | `0.07031` | past much worse |

结论：

```text
lowdim-only ~= full input
image-only << full input
```

所以 current Stage1 objective 没有强迫模型学习 image-grounded task state。接手者如果继续做 translator / memory pretraining，必须先解决这个 shortcut，否则换到 GMP 后大概率只是把同一个弱 representation 注入另一个架构。

## 7. Scale-up 与 ACT 经验

我们试过把 translator 放大到 ACT-like size。参数量：

| Model | Core Params | Full Params With Obs Encoder |
| --- | ---: | ---: |
| shared Robomimic obs encoder | - | `22.394M` |
| d256 translator | `5.776M` | `28.170M` |
| ACT-size translator | `56.177M` | `78.571M` |
| deterministic ACT-style baseline | `55.116M` | `77.510M` |
| official-ACT-compatible CVAE adapter | `72.513M` | `94.907M` |

结论：

```text
scale up 可以改善一部分 past L1，
但没有证明 downstream context 有用。
主要瓶颈不是模型太小，而是目标函数与 representation 语义不对。
```

Official-ACT-compatible Square action8 只做到了弱 smoke：

```text
25 epochs, rollout 1/20 = 5%
```

不要把它解释为 official ACT 不行；这只是当前适配和预算下的弱 baseline。

## 8. Offline Loss 与 Rollout SR 不一致

历史上多次看到：

```text
offline validation loss 更好
!=
rollout success rate 更高
```

因此接手者不能只看 reconstruction / diffusion validation loss。下游判断必须用 rollout SR，并且必须包含 random same-architecture control。

建议每组下游实验至少保留：

```text
base policy
same-architecture random context / random memory
pretrained context / pretrained memory
```

如果没有 random control，结论很容易被参数量、正则化、额外噪声或优化路径混淆。

## 9. Long-context 成本要拆成训练与推理/eval

不要把 long-context "慢" 只写成一个问题。训练和推理/eval 的优化方法不同。

训练侧成本：

```text
raw image history 重复编码
长窗口导致显存和 batch size 压力
no-cache 训练非常慢
dataloader / storage / worker 设置对速度影响大
```

训练侧可优化方向：

```text
frozen encoder / cached visual embedding 用于快速 ablation
raw image end-to-end 只用于最终确认
batch size 与 LR 联合 sweep
standard speed table: samples/epoch, steps/epoch, sec/epoch, GPU util, CPU idle/load, num_workers
sparse image history / lowdim full history
```

推理/eval 侧成本：

```text
rollout 主要受 MuJoCo / CPU / vector env 并发影响
在线策略若每步重复编码长 image history，也会浪费计算
```

推理/eval 可优化方向：

```text
vector env 并发按 CPU 动态调整
对在线 image encoding 做 sliding cache
把 long history 压成 recurrent memory state
只对关键帧或新帧编码 image，历史 memory 增量更新
```

已验证 rollout 并发经验：

```text
10.100.2.39:23494 是 192-core / 8xH200 节点。
n_envs=8 x 8 concurrent eval = 64 active envs 可以接受。
n_envs=20 x 8 concurrent eval = 160 active envs 压力过高，不建议。
```

## 10. 给 GMP 接手者的建议路线

用户当前明确：先不把"换代码库"作为问题本身。但如果下一位 intern 在 GMP workspace 中接手，应把 GMP 当作 memory-interface 参考和承载环境，而不是直接重复当前 LDP 的 pooled context 实验。

建议路线：

### Step 1: 先对齐评估协议

在 GMP workspace 中先确认：

```text
Square Robomimic eval 是否能跑通
环境版本是否与 py39 + robomimic 0.2.0 对齐
若不对齐，必须标注为 version-ablation
```

优先复用同一组 seed ranges：

```text
100000
200000
300000
100 episodes each
```

### Step 2: 找 GMP 中最自然的 memory/context interface

不要先做 pooled vector add-to-last-token。

优先找这些接口：

```text
memory tokens
history encoder hidden states
cross-attention keys/values
policy encoder replacement
recurrent memory state update
```

目标是让 translator / history encoder 的 hidden state 成为真正被 policy 使用的 memory，而不是额外加一个投影向量。

### Step 3: 用最小对照矩阵验证

最小下游矩阵：

| ID | Condition | Purpose |
| --- | --- | --- |
| G1 | GMP base | baseline |
| G2 | GMP + random same-arch memory/context | parameter/control |
| G3 | GMP + pretrained translator/history memory | core test |
| G4 | GMP + pretrained memory with lowdim dropout pretraining | shortcut mitigation |

go/no-go：

```text
G3 > G2 and G3 >= G1
```

如果做了 lowdim dropout：

```text
G4 > G3
```

才说明 image-grounded memory supervision 有帮助。

### Step 4: 优先解决 supervision，而不是继续 scale up

当前最值得尝试的是：

```text
lowdim/proprio dropout during pretraining
image-only / lowdim-only controls
future object/contact prediction if labels are available
contrastive future-action or task-phase objective
token-level hidden state supervision
```

不建议先做：

```text
更大 translator
更长训练同一个 past-action objective
同一个 pooled context add_last/add_all 注入
只看 offline loss 的选择策略
```

## 11. 接手时必须保留的安全检查

每次实验启动前：

```text
1. 记录代码 commit / workspace path。
2. 记录 Python / robomimic / robosuite / torch 版本。
3. 区分 rollout SR 和 offline validation loss。
4. 保留 random same-architecture control。
5. 记录是否使用 EMA policy。
6. 记录 eval seed ranges 和 episode count。
7. 记录是否使用 raw image end-to-end 或 cached/frozen features。
8. 记录是否使用 full input / lowdim-only / image-only / modality perturbation。
```

## 12. 当前 artifact 快速索引

Ceph root：

```text
/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator
```

Stage1 translator outputs：

```text
outputs/stage1_square_past_ceph_20260526_032417_safe_workers
outputs/behavior_translator_square_past_actsize_norm_20260530_061543
outputs/behavior_translator_square_past_actsize_rawloss_20260601_1058_50ep
outputs/stage1_square_modality_ablation_20260601
```

Stage2 downstream outputs：

```text
outputs/stage2b_square_causalcond_off_20260526_032417_safe_workers
outputs/stage2b_square_causalcond_off_pretrained_cephpast_20260526_144615
outputs/stage2b_rollout_eval_newnode_20260527
```

300-episode stability eval：

```text
outputs/stage2b_square_rollout_stability_nenv8_max8_20260605
```

Video outputs：

```text
outputs/stage2b_square_rollout_videos_20260605
```

Official-ACT-compatible smoke：

```text
outputs/official_act_square_action8/20260601_1208_official_act_square_action8_fixed_rollout25
```

## 13. 一句话交接结论

当前 Direction C 已经证明：

```text
history-to-action translator 能学到 past-action reconstruction，
但当前目标主要走 proprio shortcut，
pooled/projection context 注入下游 diffusion 不能提升 rollout SR。
```

GMP 接手时不要从"再训练更久/更大 translator"开始。更合理的任务是：

```text
利用 GMP 的 memory interface，
重新设计 image-grounded history representation 的注入方式，
并用 base / random / pretrained 三组 rollout 对照验证。
```
