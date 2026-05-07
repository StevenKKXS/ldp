## Task: SmolVLA Square Rollout with Internal GPU Image

<!-- METADATA:STATUS=InProgress,ASSIGNEE=intern_method_developer -->

### Background
- The previous formal SmolVLA-style square run completed offline evaluation but could not run Robosuite rollout because the available GPU environment lacked simulator dependencies.
- The supervisor pointed to `/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/setup_gpu_machine.sh` on the GPU machine as the reference setup for mounting the internal image.
- Work must copy the setup script into the intern-owned path before use and avoid writing into other interns' storage.

### Goals
- Copy the reference GPU setup script into the intern-owned task directory.
- Configure or enter the required internal-image GPU environment using intern-owned writable paths.
- Use the best checkpoint from task003, `epoch_0300.pt`, to run square rollout evaluation if the simulator stack can be made usable.
- Report success rate or the exact blocker if the rollout stack still cannot execute.

### Acceptance Criteria
- Setup artifacts and logs are saved under `/mnt/3fs2/data/tingwen.du/intern_method_developer/task004_smolvla_square_rollout_internal_image`.
- A report records setup steps, environment status, rollout command, checkpoint used, and success-rate result or blocker.
- The LDP repo task status and knowledge are updated.
