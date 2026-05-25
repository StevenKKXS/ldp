# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 55 |
| Recent Progress | Tried to stop the current GPU contents on `10.100.2.35:25076` by sending `SIGTERM` then `SIGKILL` to the four historical Direction C parent PIDs and their dataloader children. The parent PIDs `1086376`, `4026333`, `26885`, and `4026336` remained in `D/Dl` with `wchan=wait_on_page_bit_common` and continued holding about `5.2-5.5GB` on each H200, so ordinary process stop cannot reclaim the node. Light checks showed `/mnt/nfs` repo/env paths time out while `/mnt/3fs2` dataset stat works; the GPU node local Python has CUDA torch but no `robomimic`, so corrected Stage 2b cannot safely launch on this node. Added `launch_direction_c_stage2b_causalcond_off.sh` to launch the four corrected `causal_cond_attn=false` jobs on a clean py39 / robomimic 0.2.0 node. |
