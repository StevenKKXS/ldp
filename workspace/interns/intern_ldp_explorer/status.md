# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 60 |
| Recent Progress | Answered the user's two experiment questions. Clarified that current M1 base is already the same-architecture no-translator/no-pretraining image baseline: `DiffusionTransformerHybridImagePolicy` with robomimic image obs encoder, `obs_encoder_dir=null`, `obs_encoder_freeze=false`, and no translator context. It is not yet compared by corrected rollout against a separate canonical DP/PTP baseline. Checked speed and rollout blockers on `10.100.2.19:28106`: M1/M3 have epoch-24 checkpoints and M2/M4 are alive at epoch 0 around step `1057`; training validation runs every epoch, but rollout is disabled in training (`rollout_every=999999`, `n_test=0`) and checkpoints are saved only every 25 epochs. Manual rollout also needs environment repair because the Ceph py39 env has `robomimic==0.2.0` but lacks `robosuite`, and `mujoco_py` OSMesa compilation failed due to missing `GL/osmesa.h`. |
