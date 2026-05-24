# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 48 |
| Recent Progress | Rechecked current GPU usage on `2026-05-24T10:52-10:53Z` using only `ssh`, `nvidia-smi`, `pmon`, compute-app queries, and `/proc` process state. Local host has no `nvidia-smi`. Reachable GPU nodes remain `10.100.2.35:25076` and `10.100.4.35:19382`, each with 4x NVIDIA H200. All 8 GPUs show `0%` GPU and memory utilization, but each has one old Python compute process holding about `5.2-5.5GB` VRAM. Exact parent PIDs are `1086376`, `4026333`, `26885`, `4026336` on `10.100.2.35:25076`, and `4086173`, `2080560`, `2080562`, `2080564` on `10.100.4.35:19382`. All eight parent processes are in `Dl` with `wchan=wait_on_page_bit_common`, so there is no active GPU compute; the cards are blocked by stale NFS/page-I/O-wait training processes and are not cleanly reusable until those processes are handled. |
