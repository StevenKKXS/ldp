# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 16 |
| Recent Progress | Analyzed PTP dataloader windowing: SequenceSampler returns fixed contiguous windows; RobomimicReplayImageDataset keeps first obs history tokens and returns action tokens spanning history through future, so fixed historical obs plus historical-to-future action ranges are mostly config-level changes. |
