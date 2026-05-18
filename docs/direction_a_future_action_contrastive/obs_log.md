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
