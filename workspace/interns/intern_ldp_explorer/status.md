# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 89 |
| Recent Progress | Preprocessed LongSquare by copying `demos.hdf5` to `image.hdf5` and rewriting cached embeddings with the released `longhist_encoder.ckpt`. Fixed the Robomimic image runners to instantiate `AsyncVectorEnv(..., shared_memory=False)`, because `n_test=100` video rollouts hit Gym's custom-space shared-memory limitation. Relaunched the 4x2x2 2000-epoch queue with action horizons `8` and `1`; all eight first-stage DP runs are active and writing `logs.json.txt`, with PTP queued after each corresponding DP lane finishes. |
