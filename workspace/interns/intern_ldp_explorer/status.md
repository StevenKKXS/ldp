# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 57 |
| Recent Progress | Answered why LongSquare appears to use one HDF5 while other tasks may be discussed as needing multiple files. Rechecked the executable `_emb` configs: each task currently points dataset and env runner at a single configured HDF5 path. LongSquare is special mostly because the longhist release path is already an embedding-capable dataset (`demos_emb.hdf5` / previously validated embedded `demos.hdf5`), while Robomimic tasks may require raw and embedding-bearing variants depending on preprocessing. No training or code changes were made in this session. |
