## Task: Reproduce LDP Baseline and PTP on H200

<!-- METADATA:STATUS=InProgress,ASSIGNEE=intern_ldp_explorer -->

### Background
- Reproduce the official `long-context-dp/ldp` results as closely as practical on available H200 infrastructure.
- Cover both baseline and PTP (`Past-Token Prediction`) variants.
- Prefer official released assets when available. As of task creation, the upstream GitHub repo has no GitHub Releases, but the README provides official dataset and encoder download links.
- Reuse and judge any currently running training on the debug server when it matches the intended experiment matrix.

### Goals
- Identify the official experiment matrix relevant to `robomimic square` and other practical benchmarks we can run with current assets.
- Verify whether the currently running training belongs to baseline or PTP and incorporate it if valid.
- Reproduce at least one baseline run and one PTP run with clear configs, logs, checkpoints, and evaluation outputs.
- Prefer official encoder checkpoints and official datasets where applicable.
- Utilize H200 capacity efficiently by running multiple jobs in parallel when GPU utilization leaves headroom.

### Acceptance Criteria
- A written report summarizes:
- official upstream assets used and missing assets not publicly released
- exact configs / overrides used for baseline and PTP
- current server run classification and whether it was reused
- quantitative results obtained vs paper / website claims, with caveats
- environment or compatibility patches required on H200
- Repro artifacts are saved under a stable directory on shared storage.
