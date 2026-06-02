# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 79 |
| Recent Progress | Checked official-ACT Square action8 training speed from the completed 25-epoch run. It used `2469` batches per epoch and trained at roughly `15-18 it/s`; later epochs took about `2.5-2.8 min/epoch` for training, validation added about `5s/epoch`, and the final 20-seed rollout took about `3 min`. The full 25-epoch train+val+final-rollout job took about `73 min`; extrapolating naively, 100 epochs is about `4.8-5h`, while 2000 epochs would be about `4 days`. |
