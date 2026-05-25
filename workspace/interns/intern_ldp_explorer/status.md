# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 52 |
| Recent Progress | Checked current GPU resource reachability. Local host has no `nvidia-smi`. Only `10.100.2.35:25076` is still SSH-reachable and shows 4x NVIDIA H200, all at `0%` GPU utilization, but each GPU is occupied by an old Python process holding about `5.2-5.5GB` VRAM. Parent PIDs `1086376`, `4026333`, `26885`, and `4026336` remain in `D/Dl` with `wchan=wait_on_page_bit_common`, so this node is not a clean training resource. Historical endpoints `10.100.4.35:19382`, `10.100.2.35:33805`, `10.100.2.35:24644`, `10.100.10.31:24050`, `10.100.12.73:25637`, `10.100.12.73:15135`, and `10.100.0.29:36645` refused SSH. |
