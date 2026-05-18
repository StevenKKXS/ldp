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
- Direction: Direction B
- Related experiment: N/A
- Observation: Initial plan document created; no experiment has run.
- Evidence: Current files only contain method design and tracking templates.
- Possible explanation: N/A
- Decision: Wait for detailed Direction B plan, then review risks before implementation.
- Next step: Review decoder capacity, prediction horizon, action normalization, PTP integration path, and baseline requirements.

### Log 2026-05-18-02

- Date: 2026-05-18
- Direction: Direction B
- Related experiment: N/A
- Observation: Detailed Direction B plan was saved and reviewed. The direction is technically simpler than Direction A and is a good first implementation smoke candidate, but downstream evaluation should preserve exact PTP policy structure.
- Evidence: `review_2026-05-18.md` records code observations: current PTP has `obs_encoder_dir` / `obs_encoder_freeze`; `past_action_pred=true` keeps the full action trajectory in transformer loss; dataset returns `n_obs_steps` observations and an action sequence of length `horizon`.
- Possible explanation: Predictive pretraining can be implemented as an auxiliary decoder over current obs encoder features, then load only the encoder into PTP.
- Decision: First-pass Direction B should be exact-PTP-compatible encoder pretraining, not policy-side condition concat.
- Next step: Decide target action sequence, decoder capacity, checkpoint compatibility, and frozen/finetune protocol.
