# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 36 |
| Recent Progress | Tested the new exclusive 4xH200 node `10.100.4.35:19382` for Direction C Stage 1 translator speed. Fastest stable raw-image setting was `batch=128,num_workers=64,prefetch=2,persistent=false` at about `149.21` samples/sec and projected `8.86` minutes/epoch; larger `batch=256/512`, high prefetch persistent workers, and naive DataParallel either failed on `/dev/shm=16G` DataLoader worker bus errors or were slower. Rechecked formal Square runs: `past` and `past_future` are alive, `future` hit a DataLoader bus error after resume. Current model signal favors `past` as the stable representation pretraining target, with `past_future` worth re-running under better loss/LR settings and `future` best treated as an early-checkpoint probe rather than a long unchanged run. |
