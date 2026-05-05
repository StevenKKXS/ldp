# intern_ldp_explorer - 状态

<!-- METADATA:STATUS=Working,TASK=task001_reproduce_ldp_ptp_baseline_h200 -->

| 字段 | 值 |
|------|-----|
| Name | intern_ldp_explorer |
| Status | Working |
| Current Task | task001_reproduce_ldp_ptp_baseline_h200 |
| PR | https://github.com/StevenKKXS/ldp/pull/new/intern_ldp_explorer/task001_reproduce_ldp_ptp_baseline_h200 |
| Session | 54 |
| Recent Progress | Checked whether public PTP sources specify batch size and GPU count. Paper/project page describe the training recipe and epoch count but do not explicitly specify batch size or number of GPUs per run. Official GitHub configs and local configs specify `dataloader.batch_size=64`, `val_dataloader.batch_size=64`, `gradient_accumulate_every=1`, and `training.device=cuda:0`; `transformer_history.sh` also launches with `training.device=cuda:0`, and no DDP / torchrun / DataParallel path is present in the training entry. Current reproducible assumption: one process on one GPU per run, effective train batch size `64`, no gradient accumulation. |
