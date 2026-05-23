# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 47 |
| Recent Progress | Checked currently reachable GPU resources using only `ssh` and `nvidia-smi`, without touching NFS/3FS paths. Local host has no `nvidia-smi`. Reachable GPU nodes are `10.100.2.35:25076` (`lg-cmc-b7r201-e02u16-h200-000098`) and `10.100.4.35:19382` (`lg-cmc-b7r201-g07u26-h200-000162`), each with 4x NVIDIA H200. All 8 GPUs report about `5.2-5.5GB` used and `0%` utilization. The old Direction C training parents are still present, several in `Dl` state, so these nodes are SSH-accessible but not cleanly available for fresh experiments. Historical endpoints `10.100.2.35:33805`, `10.100.10.31:24050`, `10.100.12.73:25637`, `10.100.12.73:15135`, and `10.100.2.35:24644` refused SSH connections. |
