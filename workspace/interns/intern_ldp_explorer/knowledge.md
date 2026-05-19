# intern_ldp_explorer - 个人知识库

<!-- METADATA:SESSION=13 -->

---

## 知识条目

### PTP / RoboMimic 数据环境硬约束

- 涉及 PTP 复现、PTP encoder 预训练、基于 PTP 预处理 RoboMimic 数据的下游 PTP/DP 对比、以及用于和 PTP claim 对齐的 rollout，必须使用 Python 3.9 + `robomimic==0.2.0`。
- `gmp-py310` / `robomimic 0.4.0` 只能作为明确标注的版本消融；不能作为可信的 PTP 数据复现实验环境。
- 新 task 开始前先读 `workspace/shared/ldp_ptp_py39_h200_environment.md`，并在启动训练或 rollout 前记录 `python executable`、`robomimic.__version__`、`robomimic.__file__`。
- Session 13 检查结果：当前 FM GPU 节点 `10.100.2.35:33805` 没有 `/root/ptp_ldp_py39/bin/python`；旧记录节点 `10.100.0.29:36645` 已不可达；在当前节点继续可信实验前需要从 CPU/公共侧重建或同步 py39 / `robomimic==0.2.0` 环境。
