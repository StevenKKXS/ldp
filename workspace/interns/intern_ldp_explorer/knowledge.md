# intern_ldp_explorer - 个人知识库

<!-- METADATA:SESSION=86 -->

---

## 知识条目

### PTP / RoboMimic 数据环境硬约束

- 涉及 PTP 复现、PTP encoder 预训练、基于 PTP 预处理 RoboMimic 数据的下游 PTP/DP 对比、以及用于和 PTP claim 对齐的 rollout，必须使用 Python 3.9 + `robomimic==0.2.0`。
- `gmp-py310` / `robomimic 0.4.0` 只能作为明确标注的版本消融；不能作为可信的 PTP 数据复现实验环境。
- 新 task 开始前先读 `workspace/shared/ldp_ptp_py39_h200_environment.md`，并在启动训练或 rollout 前记录 `python executable`、`robomimic.__version__`、`robomimic.__file__`。
- Session 13 检查结果：当前 FM GPU 节点 `10.100.2.35:33805` 没有 `/root/ptp_ldp_py39/bin/python`；旧记录节点 `10.100.0.29:36645` 已不可达；在当前节点继续可信实验前需要从 CPU/公共侧重建或同步 py39 / `robomimic==0.2.0` 环境。
- Session 14 已创建当前可用 NFS 环境 `/mnt/nfs/tingwen/ldp/envs/ptp_ldp_py39_rm020`，在 `10.100.2.35:33805` 验证为 Python `3.9.23` + `robomimic 0.2.0`；MuJoCo runtime 使用 `/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/runtimes/mujoco210`。

### 当前主实验环境：Direction C / PTP py39

- 当前 Direction C / PTP-data 主环境是 GPU 节点上的 Ceph venv：
  `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph`
- 已在 `10.100.2.39:23494` 验证：Python `3.9.25`、`robomimic==0.2.0`、`torch==2.5.1+cu124`、CUDA 可用。
- 运行任何训练、rollout、eval、参数统计、smoke 之前，先执行 preflight：

```bash
VENV=/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator/envs/ptp_ldp_py39_ceph
"$VENV/bin/python" diffusion_policy/scripts/check_main_runtime_env.py --require-cuda
```

- 如果 preflight 失败，不能把结果当成可信 PTP / RoboMimic 0.2.0 复现实验；先修环境或显式标注为版本消融。
