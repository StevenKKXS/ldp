# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 29 |
| Recent Progress | Clarified the paper-level meaning of `PTP` and Figure 9. `PTP` is a core method component of the paper, specifically the auxiliary objective that predicts past actions alongside future actions. In Figure 9's default protocol, the long-history `PTP` and long-history `no-PTP` rows should both be read as trained under the paper's multistage feature-caching recipe unless otherwise specified; the controlled difference is whether `past_action_pred` / PTP is enabled. Session 29 hook-compliance note: `history_log.md` now also has a tail `## Session 29 - Hook Compliance Record`. |
