# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 69 |
| Recent Progress | Completed six-task dataset embedding consistency checks. Consistent: Square (`rel_l2_mean=0.000438`), Tool-Hang (`0.000125`), and Transport (`0.000171`). Missing/needs adaptation: Push-T zarr has keys `action/img/keypoint/n_contacts/state` and no embedding key. Inconsistent: ALOHA/Cube `aloha_twomodes_single/demos.hdf5` vs `aloha_encoder.ckpt` (`rel_l2_mean=6.7609`, `cosine_mean=0.2785`), with an additional structural mismatch because the encoder config expects `qpos.shape=[14]` while the current HDF5 has `qpos.shape=(T,7)`. Inconsistent: LongSquare `longhistsquare100/demos.hdf5` vs `longhist_encoder.ckpt` (`rel_l2_mean=1.1414`, `cosine_mean=0.4791`). Result JSON: `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/debug/session69_all_embedding_check/all_embedding_consistency_summary.json`. |
