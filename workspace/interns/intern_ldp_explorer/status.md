# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 69 |
| Recent Progress | Analyzed the current Direction C questions. Verified from code that the translator input path includes raw images plus proprio through the trainable robomimic obs encoder, but current logs cannot prove the learned context uses images rather than mostly proprio; proposed fast modality ablations and eval-time image/proprio masking to test this. Rechecked Stage2b corrected Square runs on Ceph: M1 base and M3 random have epoch-49 checkpoints, M2/M4 pretrained runs are around epoch 23 and near their first checkpoint, and rollout SR is currently blocked because the Ceph py39 env has `robomimic==0.2.0` but lacks `robosuite` and `mujoco_py` fails OSMesa compilation due missing `GL/osmesa.h`. Summarized the four Stage2b injection settings and the recommended fast SR path. |
