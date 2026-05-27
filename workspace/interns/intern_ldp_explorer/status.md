# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 73 |
| Recent Progress | Compared current corrected Stage2b Square training budget against the LDP Square reference configs and reaffirmed the calculation for the hook-compliance pass. Original Square LDP configs (`transformer_square*.yaml`) use `3500` epochs with batch size `64`; current Direction C Stage2b configs use batch size `32`, `2478` train batches/epoch, and have rollout checkpoints at e24/e49 for M1/M3 and e24 for M2/M4. By data-pass epoch count, e24/e49 are only `0.69%/1.40%` of the 3500-epoch reference. By optimizer-step count, because current batch is half as large, e24/e49 are about `1.37%/2.80%` of the full 3500-epoch LDP budget. Compared to the earlier Square FM checkpoint around e786 that already produced Square rollout signal, current e24/e49 are about `3.1%/6.2%` by epoch or `6.1%/12.5%` by optimizer steps. |
