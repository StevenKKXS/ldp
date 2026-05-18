# Observation Log

## Log Template

### Log YYYY-MM-DD-XX

- Date:
- Direction:
- Related experiment:
- Observation:
- Evidence:
- Possible explanation:
- Decision:
- Next step:

## Initial Log

### Log 2026-05-18-01

- Date: 2026-05-18
- Direction: Direction A
- Related experiment: N/A
- Observation: Initial plan document created; no experiment has run.
- Evidence: Current files only contain method design and tracking templates.
- Possible explanation: N/A
- Decision: Wait for detailed Direction A plan, then review risks before implementation.
- Next step: Review action similarity definition, hard negatives, PTP integration path, and baseline requirements.

### Log 2026-05-18-02

- Date: 2026-05-18
- Direction: Direction A
- Related experiment: N/A
- Observation: Detailed Direction A plan was saved and reviewed. The direction is promising but not implementation-ready until several tensor and experimental-control details are fixed.
- Evidence: Review file `docs/direction_a_future_action_contrastive/review_2026-05-18.md` records concrete concerns from current code: action chunk slicing uses `start = n_obs_steps - 1`; current transformer condition is `B x To x Do` with `T_cond = 1 + n_obs_steps`; naive extra condition tokens require model changes.
- Possible explanation: The method idea is high-level and valid, but current PTP implementation has fixed assumptions about condition token count and action slicing.
- Decision: Keep Direction A as a high-priority candidate, but discuss and finalize action-window alignment, condition fusion, B2 baseline parity, diagonal masking, action normalization, and frozen/finetune semantics before implementation.
- Next step: Review Direction B plan when provided, then jointly choose first-pass validation order and resource request.

### Log 2026-05-18-03

- Date: 2026-05-18
- Direction: Direction A
- Related experiment: N/A
- Observation: User clarified that first-pass experiments should reproduce the proven PTP structure as much as possible. The review was updated to recommend encoder pretraining through the existing PTP encoder-loading path instead of adding a new policy condition module.
- Evidence: `review_update_ptp_compat_2026-05-18.md` explains that "action window" means the contrastive label segment, not a change to PTP prediction horizon. It recommends preserving PTP policy architecture and loading a contrastive-pretrained encoder via `obs_encoder_dir`.
- Possible explanation: Since PTP already works in the target robomimic 0.2.0-compatible setup, the cleanest first test is whether a better encoder initialization helps unchanged PTP.
- Decision: First-pass Direction A should be exact-PTP-compatible encoder pretraining. Policy-side `concat(original_condition, z_t)` is deferred.
- Next step: Decide exact PTP baseline config/checkpoint, action segment for contrastive similarity, encoder checkpoint compatibility, and frozen/finetune protocol.

### Log 2026-05-18-04

- Date: 2026-05-18
- Direction: Direction A
- Related experiment: `A_square_contrastive_smoke`, `A_toolhang_contrastive_smoke`
- Observation: Soft future-action contrastive pretraining now runs on raw image Square and ToolHang and writes compatible encoder checkpoints.
- Evidence: Square rerun after fix produced train loss `1.2313`, val loss `1.2405`; ToolHang produced train loss `1.3928`, val loss `1.1212`. Checkpoints were written under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/smoke/`.
- Possible explanation: The initial NaN was an implementation bug from diagonal masked `log_softmax`, not a method-level failure.
- Decision: Keep Direction A in the probe matrix and monitor longer pretraining jobs.
- Next step: Use completed pretraining checkpoints for exact-PTP frozen/finetune downstream tests.

### Log 2026-05-18-05

- Date: 2026-05-18
- Direction: Direction A
- Related experiment: `A_square_future_seed42`, `A_square_future_seed43`, `A_tool_hang_future_seed42`, `A_tool_hang_future_seed43`
- Observation: Four Direction A pretraining probes were launched on GPU node `10.100.2.4:35140`.
- Evidence: PID table is `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/logs/20260518_session8/pids.tsv`; outputs are under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8`.
- Possible explanation: Running two Square seeds plus two ToolHang seeds gives a quick stability check before downstream PTP ablations.
- Decision: Treat these as implementation/pretraining probes only.
- Next step: Poll `scripts/poll_encoder_pretrain_probe.sh`, then inspect `logs.jsonl` and checkpoint paths once jobs complete.
