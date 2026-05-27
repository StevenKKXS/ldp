#!/usr/bin/env python3
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


OUT = Path(__file__).resolve().parent / "feishu_translator_report_2026-05-27"
OUT.mkdir(parents=True, exist_ok=True)


def savefig(name):
    path = OUT / name
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()
    return path


def add_box(ax, xy, wh, text, fc="#f7f7f7", ec="#222", fontsize=10):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.2, edgecolor=ec, facecolor=fc)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, wrap=True)
    return patch


def add_arrow(ax, p1, p2):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle="->", mutation_scale=14,
        linewidth=1.3, color="#333"))


def fig_story():
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    boxes = [
        (0.25, "Idea\nhistory-to-action\ntranslator hidden state"),
        (2.55, "Stage 1\nobs history ->\npast/future actions"),
        (4.85, "Stage 2a\noffline frozen\nhead probe"),
        (7.15, "Stage 2b\nDP/PTP rollout\nintegration"),
        (9.45, "Revision\ninput contract,\nbaselines,\ninjection paths"),
    ]
    colors = ["#e8f1ff", "#f7f7f7", "#e9f7ef", "#fff2df", "#f1e9ff"]
    for (x, txt), c in zip(boxes, colors):
        add_box(ax, (x, 1.55), (1.9, 1.1), txt, fc=c)
    for x in [2.15, 4.45, 6.75, 9.05]:
        add_arrow(ax, (x, 2.1), (x + 0.35, 2.1))
    ax.text(0.25, 0.55,
            "Main claim under test: pretrained behavior context should beat same-architecture random context.",
            fontsize=11, color="#333")
    ax.text(0.25, 0.20,
            "Current boundary: offline probe is positive; corrected rollout SR is not available until runtime is repaired.",
            fontsize=11, color="#9a3412")
    ax.set_title("Direction C Behavior Translator: story and evidence boundary", fontsize=15)
    return savefig("fig1_storyline.png")


def fig_input_contract():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    add_box(ax, (0.4, 3.8), (2.1, 1.0), "Image 1\nagentview_image\n[3,84,84]", "#e8f1ff")
    add_box(ax, (0.4, 2.5), (2.1, 1.0), "Image 2\neye_in_hand\n[3,84,84]", "#e8f1ff")
    add_box(ax, (0.4, 1.2), (2.1, 1.0), "Proprio\nEEF pos/quat\ngripper qpos", "#e9f7ef")
    add_box(ax, (3.4, 2.45), (2.2, 1.15), "Trainable\nrobomimic\nobs encoder", "#f7f7f7")
    add_box(ax, (6.4, 2.45), (2.2, 1.15), "Behavior\nTranslator\ncontext", "#f1e9ff")
    for y in [4.3, 3.0, 1.7]:
        add_arrow(ax, (2.55, y), (3.35, 3.05))
    add_arrow(ax, (5.65, 3.05), (6.35, 3.05))
    ax.text(0.4, 0.45,
            "Out-of-contract unless explicitly marked: past_act, object state, simulator state, reward, privileged labels.",
            fontsize=11, color="#9a3412")
    ax.text(6.25, 0.45,
            "Fast checks: mask/shuffle images vs proprio; retrain lowdim-only and image-only.",
            fontsize=11, color="#333")
    ax.set_title("Input contract: train/eval observable signals only", fontsize=15)
    return savefig("fig2_input_contract.png")


def fig_stage1():
    labels = [
        "past\nformal",
        "past\ntuned",
        "future\nearly",
        "past+future\nequal",
        "past+future\nw_future=.5",
        "Ceph past\nobs1e-4",
        "Ceph past\nobs5e-5",
    ]
    vals = [0.000455, 0.000434, 0.008961, 0.010111, 0.006501, 0.000593, 0.000598]
    colors = ["#2f6db3", "#2f6db3", "#b45309", "#b45309", "#b45309", "#5b8f3a", "#5b8f3a"]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(range(len(vals)), vals, color=colors)
    ax.set_yscale("log")
    ax.set_ylabel("best validation loss (log scale)")
    ax.set_xticks(range(len(vals)), labels)
    ax.set_title("Stage 1 translator objectives: past is the stable representation target")
    ax.grid(axis="y", alpha=0.25)
    for i, v in enumerate(vals):
        ax.text(i, v * 1.12, f"{v:.6f}", ha="center", fontsize=9)
    return savefig("fig3_stage1_objectives_updated.png")


def fig_stage2a():
    labels = ["random\nfrozen", "past e50\nfrozen", "past tuned\nfrozen", "past tuned\nfinetune", "past+future\nfrozen"]
    vals = [0.011571, 0.007839, 0.007959, 0.008056, 0.010617]
    colors = ["#9ca3af", "#2f6db3", "#2f6db3", "#5b8f3a", "#b45309"]
    fig, ax = plt.subplots(figsize=(10.5, 5))
    ax.bar(range(len(vals)), vals, color=colors)
    ax.set_ylabel("offline probe val loss")
    ax.set_xticks(range(len(vals)), labels)
    ax.set_title("Stage 2a frozen-head probe: pretrained past context beats random")
    ax.grid(axis="y", alpha=0.25)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.00025, f"{v:.4f}", ha="center", fontsize=9)
    return savefig("fig4_stage2a_probe_updated.png")


def fig_stage2b():
    labels = [
        "M1 base\ne24", "M3 random\ne24", "M2 pre add_last\ne24", "M4 pre add_all\ne24",
        "M1 base\nbest e52", "M3 random\nbest e52", "M4 pre\nbest e22", "M2 pre\nbest e24",
    ]
    vals = [0.058112, 0.058755, 0.050084, 0.048616, 0.040411, 0.044589, 0.046840, 0.050084]
    colors = ["#2f6db3", "#9ca3af", "#7c3aed", "#7c3aed", "#2f6db3", "#9ca3af", "#7c3aed", "#7c3aed"]
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.bar(range(len(vals)), vals, color=colors)
    ax.set_ylabel("offline validation loss")
    ax.set_xticks(range(len(vals)), labels)
    ax.set_title("Corrected Stage 2b offline status: four-way checkpoint now exists, SR still blocked")
    ax.grid(axis="y", alpha=0.25)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.0012, f"{v:.4f}", ha="center", fontsize=9)
    ax.text(0.05, -0.24,
            "Matched e24 comparison favors pretrained context; longer M1/M3 runs improve further. Need matched training budget + rollout SR.",
            transform=ax.transAxes, fontsize=10, color="#9a3412")
    return savefig("fig5_stage2b_corrected_status.png")


def fig_next_matrix():
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    add_box(ax, (0.35, 4.15), (2.2, 0.9), "B0\nDefault DP\ncond[0..1]", "#e8f1ff")
    add_box(ax, (0.35, 2.75), (2.2, 0.9), "B1\nPTP base\ncond[0..15]\npast+future loss", "#e8f1ff", fontsize=9)
    add_box(ax, (3.4, 3.45), (2.4, 0.9), "Projection path\nP0/P1/P2\ncontext -> projector", "#fff2df")
    add_box(ax, (6.65, 3.45), (2.4, 0.9), "Replacement path\nR0/R1/R2/R3\ntransfer encoder", "#f1e9ff")
    add_box(ax, (9.85, 3.45), (1.75, 0.9), "SR table\nsame rollout\nprotocol", "#e9f7ef")
    add_arrow(ax, (2.6, 3.2), (3.35, 3.9))
    add_arrow(ax, (2.6, 3.2), (6.6, 3.9))
    add_arrow(ax, (5.85, 3.9), (6.6, 3.9))
    add_arrow(ax, (9.1, 3.9), (9.8, 3.9))
    rows = [
        ("Expectation A", "P1/P2 > P0 and >= B1", "translator context helps downstream policy"),
        ("Expectation B", "R1/R2 > R0", "pretrained encoder is useful even without pooled context"),
        ("If lowdim-only ~ full", "context is likely proprio-dominated", "revise objective to force visual grounding"),
        ("If offline improves but SR does not", "loss is not rollout-aligned", "run SR-first selection, token context, or action-side tokens"),
    ]
    y = 1.95
    for title, cond, action in rows:
        add_box(ax, (0.45, y), (2.0, 0.55), title, "#f7f7f7", fontsize=9)
        add_box(ax, (2.85, y), (3.35, 0.55), cond, "#ffffff", fontsize=9)
        add_box(ax, (6.6, y), (4.7, 0.55), action, "#ffffff", fontsize=9)
        y -= 0.7
    ax.set_title("Next experiment matrix: expectations and revision rules", fontsize=15)
    return savefig("fig6_next_experiment_matrix.png")


def write_report(figs):
    report = f"""# Direction C Behavior Translator 更新汇报

Owner: intern_ldp_explorer｜Project: ldp｜Date: 2026-05-27｜Scope: Translator / Stage 2b revision

## 一句话结论

Direction C 的核心想法仍然成立为一个待验证假设：translator 通过 observation history 学到 behavior-aware hidden state，这个 hidden state 可能帮助下游 DP/PTP。但现在最严谨的边界是：Stage 2a offline probe 已经给出正信号；corrected Stage 2b 已有四组 offline checkpoint，成功率 SR 还没有跑出，因为 Ceph py39 rollout runtime 缺 `robosuite` 且 `mujoco_py` 缺 OSMesa header。

图 1 展示当前故事线：从 idea 到 Stage 1/2a/2b，再到本轮根据结果修正实验矩阵。

![figure](fig1_storyline.png)

## 1. Idea 出发点

最初目标不是让 translator 直接当 policy，而是验证：

> obs history -> action translation 这个预训练任务是否能学到一种 behavior-aware context，让下游 DP/PTP 更容易生成未来动作 chunk。

核心判据原本是：

```text
PTP/DP + pretrained frozen translator context
    >
PTP/DP + same-architecture frozen random context
```

这个判据用于排除“只是多了模块或多了参数”的解释。

## 2. 输入契约：训练和 rollout eval 必须一致

我们刚重新明确了输入约束：rollout-facing policy 和 translator 只允许使用 eval 时也能拿到的 observation。

| 类别 | key | 含义 |
|---|---|---|
| image1 | `agentview_image` | 第三方/front RGB camera |
| image2 | `robot0_eye_in_hand_image` | wrist / eye-in-hand RGB camera |
| proprio | `robot0_eef_pos` | end-effector position |
| proprio | `robot0_eef_quat` | end-effector quaternion |
| proprio | `robot0_gripper_qpos` | gripper joint positions |

当前 Direction C translator configs 使用的是 `image_abs.hdf5`，不包含 `past_act`。past/future action 只作为训练监督 label，不作为输入。

图 2 说明当前输入路径和要补的 modality 验证。

![figure](fig2_input_contract.png)

### 2.1 为什么要补 modality 验证

虽然代码路径确实包含 image1/image2/proprio，但当前 loss 不能证明 translator 真正用了 image。`past` objective 表现最好，有可能主要学到 proprio 到近期 action 的映射。这个问题不影响当前代码正确性，但会影响我们如何解释方法贡献。

计划补四个检查：

| 检查 | 操作 | 预期 |
|---|---|---|
| image-masked eval | 固定 ckpt，eval 时置零或 shuffle 两路 image | 若 loss 不变，image 贡献小 |
| proprio-masked eval | 固定 ckpt，eval 时置零或 shuffle proprio | 若 loss 大幅变差，proprio 主导 |
| lowdim-only retrain | 只保留 proprio 训练 | 若接近 full，说明 image 不是必要条件 |
| image-only retrain | 只保留两路 image 训练 | 若明显更差，说明当前 objective 缺少视觉 grounding 压力 |

## 3. Stage 1：translator 预训练结果

实验从三个目标开始：`past`、`future`、`past_future`。原始直觉上 `past_future` 最接近“理解历史并预测未来”，但结果推动了我们修正判断。

| 目标 | best validation | 判断 |
|---|---:|---|
| historical `past` formal | `0.000455 @ e113` | 稳定 |
| historical `past` tuned | `0.000434 @ e118` | 当前历史最好 |
| historical `future` | `0.008961 @ e4` | early-best 后验证变差 |
| historical `past_future` equal weight | `0.010111 @ e4` | future 部分拖累 |
| historical `past_future`, `w_future=0.5` | `0.006501 @ e4` | 有改善但仍弱于 past |
| current Ceph `past`, obs lr `1e-4` | `0.000593 @ e31` | 可用但弱于历史 best |
| current Ceph `past`, obs lr `5e-5` | `0.000598 @ e31` | 与 `1e-4` 接近 |

图 3 给出 Stage 1 目标对比。

![figure](fig3_stage1_objectives_updated.png)

阶段判断：`past` 不是最“语义漂亮”的目标，但它是目前最稳定的 behavior-history representation pretraining。`future/past_future` 仍保留为 ablation，不作为当前主线。

## 4. Stage 2a：offline frozen-head probe

Stage 2a 不产生 SR，只回答一个更便宜的问题：

> freeze translator 后，context 是否比 same-architecture random context 更容易预测 future action？

结果是正向的。

| Context | val loss | future L1 | 解释 |
|---|---:|---:|---|
| frozen random translator | `0.011571` | `0.06736` | 控制组 |
| pretrained `past` e50 frozen | `0.007839` | `0.04917` | 明显更好 |
| tuned `past` frozen | `0.007959` | - | 与 e50 接近 |
| tuned `past` finetune | `0.008056` | - | 未明显优于 frozen |
| pretrained `past_future` frozen | `~0.0106-0.0136` | - | 当前弱于 `past` |

图 4 展示 offline probe 的主要证据。

![figure](fig4_stage2a_probe_updated.png)

分析：Stage 2a 支持“translator hidden state 不是 random”的说法，但它还不能证明环境成功率会提升。

## 5. 旧 Stage 2b rollout 为什么降级为诊断

旧 Stage 2b 曾有混合 rollout：

| Setting | Result |
|---|---|
| add_all e24 | pretrained `0/10`, random `2/10` |
| add_all e49 | pretrained `2/10`, random `5/10` |
| add_all e99 | pretrained `4/10`, random `3/10` |
| add_last e49 | pretrained `4/10`, random `0/10` |

这些结果不能作为最终 evidence。后来定位到 action8 设置下 `horizon=8, n_obs_steps=16, causal_attn=true, n_cond_layers=0` 会让 action token 看不到 condition token 8..15。也就是说最新 obs 和 `add_last` context 在旧设置里可能不可见。

修正：corrected runs 使用 `policy.causal_cond_attn=false`。

## 6. Corrected Stage 2b 当前状态

当前 Ceph-only corrected Stage 2b 四组都已经有 checkpoint。仍需强调：下面是 offline validation，不是 SR。

| ID | Setting | e24/e25 附近 | 当前 best | 状态 |
|---|---|---:|---:|---|
| M1 | base no-context | e24 `0.058112` | `0.040411 @ e52` | running |
| M3 | random add_last | e24 `0.058755` | `0.044589 @ e52` | running |
| M2 | pretrained `past` add_last | e24 `0.050084` | `0.050084 @ e24` | running |
| M4 | pretrained `past` add_all | e24 `0.048616` | `0.046840 @ e22` | running |

图 5 展示 corrected offline 状态。

![figure](fig5_stage2b_corrected_status.png)

当前分析：

- 在 matched e24 位置，M2/M4 pretrained context 的 offline loss 明显低于 M1/M3，这是一个积极信号。
- M1/M3 继续训练到 e52 后又显著下降，说明不能只拿不同训练长度比较。
- M4 `add_all` 在早期 offline loss 上强于 M2 `add_last`，说明 broadcast context 可能更容易被 transformer 利用；但它也更可能覆盖时序 obs token，需要 SR 验证。
- SR 仍缺失。原因是 Ceph py39 环境目前 `robomimic==0.2.0` 可用，但 `robosuite` 缺失，`mujoco_py` OSMesa 编译缺 `GL/osmesa.h`。

## 7. 我对当前结果的修正判断

| 原假设 | 现阶段观察 | 修正 |
|---|---|---|
| `past_future` 应该是主目标 | future 部分验证不稳 | 以 `past` 为主线，`past_future` 做加权 ablation |
| Stage 2a 正信号可以直接转成 SR | Stage 2b 受 mask 和注入方式影响 | SR 必须用 corrected matrix 单独验证 |
| pooled context 足够 | projection path 可能压缩过强 | 同时测试 encoder replacement 和 token-level context |
| translator 可能学视觉历史 | `past` 可能被 proprio shortcut 解释 | 补 modality mask / lowdim-only / image-only 验证 |

## 8. 结合新建议后的下一步实验设计

我们把 downstream 重新组织成两个 baseline、两条 translator transfer 路径。

### 8.1 Baseline

| ID | Setting | 目的 | 预期 |
|---|---|---|---|
| B0 | default DP, obs=2, `cond[0..1]` | 标准短历史 DP baseline | 给出最基础 SR 标尺 |
| B1 | proven PTP, obs=16, `cond[0..15]`, past+future objective | 强 long-context baseline | 应优于或接近 B0；若不优，先修 PTP baseline |

### 8.2 Projection path

| ID | Setting | 目的 | 预期 |
|---|---|---|---|
| P0 | B1 + random translator context projection | 架构控制 | 不应稳定优于 B1 |
| P1 | B1 + pretrained context `add_last` | 低风险 context 注入 | 若 hypothesis 成立，应优于 P0 |
| P2 | B1 + pretrained context `add_all` | 强 broadcast 注入 | 若 context 需要全局影响，可能优于 P1 |

### 8.3 Encoder replacement path

| ID | Setting | 目的 | 预期 |
|---|---|---|---|
| R0 | B1 + random same-architecture encoder | replacement control | 不应稳定优于 B1 |
| R1 | B1 + frozen translator obs encoder | 测 frozen encoder transfer | 若 encoder 表征有用，应优于 R0 |
| R2 | B1 + finetuned translator obs encoder | 测端到端适配 | 可能优于 R1，但有破坏预训练表征的风险 |
| R3 | B0 + finetuned translator obs encoder | 测是否帮助 default DP | 若只帮 PTP 不帮 DP，说明收益依赖 long-context objective |

图 6 展示矩阵和修正规则。

![figure](fig6_next_experiment_matrix.png)

## 9. 结果不符合预期时的修正规则

| 现象 | 解释 | 修正 |
|---|---|---|
| P1/P2 不优于 P0 | pretrained context 没被用上，或 context 无效 | 做 modality check；改成 token context；检查 projector 训练 |
| P2 优于 P1 | broadcast context 更有效 | 保留 `add_all`，同时检查是否伤害 rollout stability |
| P1 优于 P2 | context 更适合作为最新 belief | 主线用 `add_last` 或额外 context token |
| R1/R2 优于 projection path | 主要收益来自 obs encoder pretraining | 主线转向 encoder replacement |
| lowdim-only 接近 full | 方法可能主要是 proprio shortcut | 加 image-only / proprio-drop training，或改目标为视觉 grounding 更强的任务 |
| offline val 好但 SR 差 | loss 与 rollout 不一致 | 用 SR-first checkpoint selection，补更多 seeds，检查 action slicing / normalizer |

## 10. Todo

1. 修 Ceph rollout runtime：安装/迁移 `robosuite`，补 `mujoco_py` OSMesa header/runtime。
2. 对 M1/M2/M3/M4 的 e24 checkpoint 先跑统一 reward-only SR smoke。
3. 在新卡上启动 B0/B1 baseline，作为后续所有 transfer 实验的 SR 标尺。
4. 实现 projection path 的 P0/P1/P2 完整矩阵。
5. 实现 encoder replacement path 的 R0/R1/R2/R3。
6. 补 modality 诊断：image-masked eval、proprio-masked eval、lowdim-only retrain、image-only retrain。

## 11. 路径

本地报告目录：`{OUT}`

Ceph active root：`/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator`

当前代码分支：`intern_ldp_explorer/task002_flow_matching_square_toolhang`
"""
    (OUT / "source_report.md").write_text(report, encoding="utf-8")


def main():
    figs = [
        fig_story(),
        fig_input_contract(),
        fig_stage1(),
        fig_stage2a(),
        fig_stage2b(),
        fig_next_matrix(),
    ]
    write_report(figs)
    for p in figs:
        print(p)
    print(OUT / "source_report.md")


if __name__ == "__main__":
    main()
