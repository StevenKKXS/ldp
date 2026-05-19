# ldp - 错题本

> 记录项目相关错误。

---

## PTP 数据复现不可混用 RoboMimic 版本

- 错误模式：在 `gmp-py310` / `robomimic 0.4.0` 环境中训练或 rollout，然后把结果当作 PTP 数据复现结果。
- 影响：PTP 数据和历史可复现结果依赖 `robomimic==0.2.0` 版本族；`robomimic 0.4.0` 会引入环境、wrapper、数据接口、controller/runtime 兼容层差异，结果不可直接和 PTP claim 对齐。
- 规避：所有可信 PTP-data run 使用 Python 3.9 + `robomimic==0.2.0`，启动前打印并归档 `sys.executable`、`robomimic.__version__`、`robomimic.__file__`。
- 当前状态：Session 13 确认 `10.100.2.35:33805` 缺少 `/root/ptp_ldp_py39/bin/python`；必须先从 CPU/公共侧重建或同步正确环境，再启动新的可信训练或 rollout。
