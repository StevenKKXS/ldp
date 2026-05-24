# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 50 |
| Recent Progress | Continued corrected Direction C setup. Rechecked reachable H200 nodes and attempted to clean stale NFS/page-I/O-wait jobs with `SIGTERM` then `SIGKILL` on parent PIDs `1086376`, `4026333`, `26885`, `4026336`, `4086173`, `2080560`, `2080562`, and `2080564`; the same PIDs remained in `D/Dl` with `wchan=wait_on_page_bit_common`, so existing nodes are still not clean training resources. Added four corrected Square action8 config entry points with `policy.causal_cond_attn=false`: base no-context, pretrained `past` + `add_last`, random + `add_last`, and pretrained `past` + `add_all`. PyYAML validation and py_compile passed. Updated `docs/direction_c_behavior_translator/session49_mask_analysis_report.md` with the prepared matrix and cleanup result. |
