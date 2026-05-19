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

### Log 2026-05-18-03

- Date: 2026-05-18
- Direction: Direction B
- Related experiment: `B_square_predictive_smoke`, `B_toolhang_predictive_smoke`
- Observation: Predictive encoder pretraining runs on raw image Square and ToolHang and writes compatible encoder checkpoints.
- Evidence: Square smoke produced train loss `0.4260`, val loss `0.4002`; ToolHang smoke produced train loss `0.4394`, val loss `0.3929`. Checkpoints were written under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/smoke/`.
- Possible explanation: A lightweight MLP decoder over PTP obs encoder features is enough for implementation-level action-sequence pretraining.
- Decision: Keep Direction B as the lower-risk pretraining branch.
- Next step: Compare full action target against future-only target in longer probes.

### Log 2026-05-18-04

- Date: 2026-05-18
- Direction: Direction B
- Related experiment: `B_square_full_seed42`, `B_square_future_seed42`, `B_tool_hang_full_seed42`, `B_tool_hang_future_seed42`
- Observation: Four Direction B pretraining probes were launched on GPU node `10.100.2.4:35140`.
- Evidence: PID table is `/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/logs/20260518_session8/pids.tsv`; outputs are under `/mnt/3fs2/data/tingwen.du/intern_method_developer/ptp_encoder_probe/runs/20260518_session8`.
- Possible explanation: Full-target vs future-only target is the most direct first ablation for the user question about whether past/current action prediction helps encoder representations.
- Decision: Treat these as pretraining feasibility observations until downstream PTP scores are available.
- Next step: Poll `scripts/poll_encoder_pretrain_probe.sh`, then inspect `logs.jsonl` and checkpoint paths once jobs complete.

### Log 2026-05-18-05

- Date: 2026-05-18
- Direction: Direction B
- Related experiment: `B_square_full_seed42`, `B_square_future_seed42`, `B_tool_hang_full_seed42`, `B_tool_hang_future_seed42`
- Observation: All four Direction B pretraining probes completed 10 epochs and the GPU node is idle.
- Evidence: `scripts/poll_encoder_pretrain_probe.sh` reports all Session 8 PIDs exited. Final losses were Square full/future train `0.0167`/`0.0164`, ToolHang full/future train `0.0243`/`0.0252`; all runs wrote `latest.ckpt`.
- Possible explanation: Predictive action decoding is an easy and stable auxiliary objective, but lower prediction loss does not imply better downstream PTP score.
- Decision: Treat the generated checkpoints as candidates for exact-PTP frozen/finetune ablation.
- Next step: Run downstream PTP ablations and compare against baseline PTP under the same policy architecture.

### Log 2026-05-19-01

- Date: 2026-05-19
- Direction: Direction B
- Related experiment: `B_downstream_session10_main`, `B_downstream_session10_extra`
- Observation: Exact-PTP downstream training runs from Direction B checkpoints are active on Square and ToolHang. Early train/val diffusion losses are close to original encoder baselines.
- Evidence: Main matrix latest poll: Square `B_full_frozen` val `0.0933`, `B_full_finetune` `0.0865`, original `0.0965`; ToolHang `B_full_frozen` `0.1585`, `B_full_finetune` `0.1566`, original `0.1568`. Extra matrix latest poll: Square `B_future_frozen` val `0.1012`, `B_future_finetune` `0.1144`; ToolHang `B_future_frozen` val `0.2668`, `B_future_finetune` `0.2624`.
- Possible explanation: Full-action predictive pretraining is stable and loads into the exact PTP policy. Early Square finetuned rows now show lower val loss than original, while ToolHang remains nearly tied; future-only rows started later and need completed curves before comparison.
- Decision: Continue comparing full-target vs future-only and frozen vs finetuned curves; do not claim method effectiveness from the current small loss differences.
- Next step: Compare completed downstream loss curves and decide whether any row deserves rollout evaluation after environment dependencies are repaired.
