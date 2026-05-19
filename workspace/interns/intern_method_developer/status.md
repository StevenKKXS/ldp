# intern_method_developer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_method_developer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 15 |
| Recent Progress | High-level progress beyond environment setup: Direction A and Direction B have both been implemented, pretrained, and tested in a first 50-epoch exact-PTP downstream ablation. Direction A frozen is currently the strongest Square loss-only row; Direction B full frozen is also positive. |
| Handoff | Seed-43 repeat is still running on `10.100.2.4:35140` with 8 active jobs. At epoch 35, Square repeat vals are original `0.0756`, `A_future_frozen` `0.0731`, `B_full_frozen` `0.0731`, `B_future_frozen` `0.0735`; ToolHang repeat is around epoch 14 and remains close across rows. |
