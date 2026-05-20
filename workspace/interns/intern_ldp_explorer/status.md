# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 32 |
| Recent Progress | Benchmarked the Direction C Stage 1 Square `past` translator on GPU3 with aggressive CPU DataLoader settings. The node has 192 logical CPUs; formal jobs use 24 workers total and leave global CPU mostly idle, but individual workers saturate and H200 utilization remains data-pipeline limited. Best valid same-batch setting was batch 32 with 64 workers at 80.59 samples/s; fastest valid raw setting was batch 64 with 96 workers at 104.43 samples/s. Higher worker/batch settings hit DataLoader shared-memory/IPC failures with `/dev/shm` only 16G. Patched translator checkpoint resume to move optimizer state to CUDA and restored `past`/`future` formal runs from latest checkpoints. |
