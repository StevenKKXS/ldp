# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 49 |
| Recent Progress | Analyzed why Direction C Stage2a looked useful but Stage2b rollout was mixed. Found a concrete action8 masking bug: with `horizon=8`, `n_obs_steps=16`, `causal_attn=true`, and `n_cond_layers=0`, the transformer causal memory mask lets action tokens attend only obs tokens `0..7`; obs tokens `8..15`, including the newest/current observation and `add_last` context injection, are invisible. Added backward-compatible `causal_cond_attn` option to `TransformerForDiffusion` and the image policy, defaulting to old behavior, so corrected experiments can run with `policy.causal_cond_attn=false`. Ran synthetic perturbation and gradient visibility experiments: old behavior had nonzero sensitivity/gradient only for obs tokens `0..7` and exact zero for `add_last`; disabling causal condition attention made all 16 obs tokens visible. Wrote report `docs/direction_c_behavior_translator/session49_mask_analysis_report.md`. Formal Robomimic training/rollout was not launched because current H200 nodes are still occupied by stale `Dl` NFS/page-I/O-wait processes and large NFS/3FS artifacts remain unreliable. |
