# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 56 |
| Recent Progress | Moved Direction C execution to Ceph-only storage after the user clarified that NFS and 3FS are offline. New node `10.100.2.19:28106` has 4xH200 and Ceph mounted at `/mnt/cephfs/home/tinwen.du`. Created Ceph root `/mnt/cephfs/home/tinwen.du/intern_ldp_explorer/direction_c_behavior_translator`, synced repo to `repos/ldp`, copied Square `image_abs.hdf5` to `datasets/robomimic/datasets/square/mh/`, and built py39 / `robomimic==0.2.0` env at `envs/ptp_ldp_py39_ceph`. Fixed plain transformer policy so inherited `translator_*` config keys do not leak into `scheduler.step()`, added a local `pytorch3d` transforms stub, and updated the corrected Stage 2b launcher for Ceph paths and compact GPU assignment. One-step smoke passed. Since the pretrained translator ckpt is unavailable on Ceph, launched safe-worker jobs on the new node: Stage2b M1 base and M3 random-context, plus two Stage1 `past` retrains to regenerate a Ceph checkpoint. |
