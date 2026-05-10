# task002_remaining_baselines_push_t_aloha_longsquare_transport - Remaining Baselines

<!-- METADATA:STATUS=Open,ASSIGNEE=intern_ldp_explorer -->

## Background
- Task 001 established the first-stage reproduction evidence and identified that environment versioning matters for Robomimic success rates.
- The next stage should focus on remaining baseline coverage and improving baselines until they are usable comparison points.
- Priority tasks named by the user are Push-T, LH-ALOHA, Long Square, and Transport.

## Goals
- Bring up smoke tests and rollout paths for the remaining baseline tasks.
- Run baseline variants needed for comparison, starting from the recommended PTP-compatible Python 3.9 environment when applicable.
- Improve failing or weak baselines through controlled changes, with exact environment, dataset, config, checkpoint, and rollout records.
- Preserve enough videos and logs for qualitative debugging while avoiding unnecessary large output retention.

## Initial Scope
- Push-T: verify dataset format, config path, training entrypoint, rollout runner, and video saving.
- LH-ALOHA: verify released data / embedding compatibility and long-horizon rollout stability.
- Long Square: continue from the recommended-version evidence and improve baseline performance.
- Transport: continue from the recommended-version evidence and improve baseline performance.

## Acceptance Criteria
- [ ] Each target task has a documented smoke-test result.
- [ ] Each target task has at least one runnable baseline recipe with exact overrides.
- [ ] Rollout evaluation runs with `n_test=100` where task runtime makes this practical.
- [ ] Saved videos exist for representative successful and failed rollouts.
- [ ] Results are summarized in a table with config, checkpoint, score, and known caveats.
- [ ] Remaining blockers are separated into environment, dataset, control/action-space, and training-length categories.
