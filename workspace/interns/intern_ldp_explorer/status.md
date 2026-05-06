# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 78 |
| Recent Progress | Summarized the likely causes for lower-than-paper success rates and zero-success Tool-Hang / Transport. Current diagnosis: embedding mismatch is not the main explanation for Square, Tool-Hang, or Transport; the strongest remaining risks are evaluation / reporting mismatch, sparse-reward checkpoint selection, 500-epoch schedule versus released longer YAMLs, runner / action-conversion validity, task difficulty, and known dataset issues for LongSquare / ALOHA / Push-T. Recommended priority is expert-action replay first, then rollout video and action dumps, then controlled longer reruns with a fresh LR schedule after runner validity is established. |
