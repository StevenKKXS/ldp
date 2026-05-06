# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 77 |
| Recent Progress | Answered whether the encoder is frozen during training. Confirmed that the current paper-aligned cached-embedding 4x2 diffusion runs use `_emb` configs with `obs_encoder_freeze=true`; the policy code then sets every observation-encoder parameter to `requires_grad=False`. In cached-embedding loss computation, `use_embed_if_present=true` consumes `batch["obs"]["embedding"]` directly, so training does not normally forward raw images through the encoder. Raw-image / non-embedding configs can have `obs_encoder_freeze=false` and are not the current main reproduction line. |
