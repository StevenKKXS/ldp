# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task002_flow_matching_square_toolhang -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task002_flow_matching_square_toolhang |
| PR | https://github.com/StevenKKXS/ldp/pull/1 |
| Session | 61 |
| Recent Progress | Answered the user's question about per-epoch sample count and sampling logic. Recomputed the active Square/mh split from the Ceph HDF5: `300` demos, `80,731` frames total; `val_ratio=0.02,seed=42` selects 6 validation demos `[26,129,130,194,229,257]`, leaving `294` train demos. Because current configs use `sequence_length=24,pad_before=16,pad_after=7`, each selected episode of length `L` contributes `L - 24 + 16 + 7 + 1 = L` windows. Therefore each train epoch covers `79,289` train windows and validation covers `1,442` windows. Stage2b batch 32 gives `2,478` train batches and `46` val batches per epoch; Stage1 batch 128 gives `620` train batches and `12` val batches. |
