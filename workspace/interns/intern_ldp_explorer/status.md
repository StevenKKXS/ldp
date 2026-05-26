# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 62 |
| Recent Progress | Answered the user's bottleneck question with live profiling on `10.100.2.19:28106`. `vmstat` showed about `13%` CPU user time, `86-87%` idle, `0%` iowait, and block input near zero, so the active bottleneck is not file reading. `nvidia-smi dmon` showed bursty GPU utilization with many `0%` samples and spikes up to about `79%`, while H200 memory use is only about `10GB` for Stage2b and `17.6GB` for Stage1, so the GPUs are not compute- or memory-saturated. Stage2b train logs show about `1.6-1.7 it/s` per run. The most likely limiting path is CPU-side batch construction and DataLoader IPC: raw image history (`16` obs steps x `2` cameras), CPU ColorJitter, numpy/torch copies, and safe-worker settings (`num_workers=4,val_workers=2`) forced by `/dev/shm=16G`; M1/M2 and M3/M4 also share GPUs, slowing individual jobs. |
