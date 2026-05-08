#!/usr/bin/env bash
set -euo pipefail

TASK_ROOT=/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn
REPO_ROOT=/mnt/3fs2/data/tingwen.du/workspace/ldp
PYTHON=/root/venv/bin/python
STAMP="${1:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${TASK_ROOT}/runs/dp_nohist_unet_dit_${STAMP}"
LOG_ROOT="${TASK_ROOT}/logs/dp_nohist_unet_dit_${STAMP}"

LDP_MH_DATA=/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5
OFFICIAL_PH_DATA=/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn/data/square/ph/image_abs_v141.hdf5

mkdir -p "${OUT_ROOT}" "${LOG_ROOT}"

run_exp() {
  local gpu="$1"
  local model="$2"
  local dataset_name="$3"
  local dataset_type="$4"
  local dataset_path="$5"
  local seed="$6"

  local config_name target extra_overrides run_name run_dir log_file status_file
  run_name="dp_nohist_${model}_${dataset_name}_seed${seed}"
  run_dir="${OUT_ROOT}/${run_name}"
  log_file="${LOG_ROOT}/${run_name}.log"
  status_file="${LOG_ROOT}/${run_name}.status"

  if [[ "${model}" == "unet" ]]; then
    config_name="train_diffusion_unet_image_workspace"
    target="dp_nohist_scheduled_workspaces.ScheduledDiffusionUnetImageWorkspace"
    extra_overrides=(
      "obs_as_global_cond=true"
    )
  elif [[ "${model}" == "dit" ]]; then
    config_name="train_diffusion_transformer_hybrid_workspace"
    target="dp_nohist_scheduled_workspaces.ScheduledDiffusionTransformerHybridWorkspace"
    extra_overrides=(
      "obs_as_cond=true"
      "+policy.past_action_pred=false"
      "+policy.use_embed_if_present=false"
    )
  else
    echo "Unknown model: ${model}" >&2
    exit 2
  fi

  if pgrep -f "${run_name}" >/dev/null; then
    echo "SKIP_RUNNING ${run_name}"
    return 0
  fi

  echo "START $(date -u +%Y-%m-%dT%H:%M:%SZ) gpu=${gpu} model=${model} dataset=${dataset_name} run=${run_name}" | tee "${status_file}"
  (
    cd "${REPO_ROOT}"
    export PYTHONPATH="${TASK_ROOT}/scripts:${REPO_ROOT}:${PYTHONPATH:-}"
    export CUDA_VISIBLE_DEVICES="${gpu}"
    export MUJOCO_GL=egl
    export WANDB_MODE=offline
    "${PYTHON}" train.py \
      --config-name="${config_name}" \
      "_target_=${target}" \
      "task=square_image_abs" \
      "hydra.run.dir=${run_dir}" \
      "hydra.sweep.dir=${run_dir}" \
      "name=${run_name}" \
      "exp_name=dp_nohist_square" \
      "horizon=16" \
      "n_obs_steps=2" \
      "dataset_obs_steps=2" \
      "n_action_steps=1" \
      "n_latency_steps=0" \
      "past_action_visible=false" \
      "task.dataset_type=${dataset_type}" \
      "task.dataset.dataset_path=${dataset_path}" \
      "task.env_runner.dataset_path=${dataset_path}" \
      "task.dataset.use_cache=true" \
      "task.dataset.val_ratio=0.02" \
      "task.dataset.seed=${seed}" \
      "task.env_runner.n_train=0" \
      "task.env_runner.n_train_vis=0" \
      "task.env_runner.n_test=50" \
      "task.env_runner.n_test_vis=50" \
      "task.env_runner.n_envs=28" \
      "task.env_runner.test_start_seed=100000" \
      "training.device=cuda:0" \
      "training.seed=${seed}" \
      "training.debug=false" \
      "training.resume=true" \
      "training.num_epochs=1000" \
      "training.val_every=10" \
      "training.sample_every=10" \
      "+training.schedule_early_until=100" \
      "+training.schedule_early_every=10" \
      "+training.schedule_late_every=100" \
      "+training.rollout_final=true" \
      "+training.checkpoint_final=true" \
      "dataloader.batch_size=64" \
      "val_dataloader.batch_size=64" \
      "dataloader.num_workers=4" \
      "val_dataloader.num_workers=4" \
      "checkpoint.topk.k=50" \
      "+checkpoint.save_epoch_ckpt=true" \
      "logging.mode=offline" \
      "logging.project=dp_nohist_square" \
      "logging.name=${run_name}" \
      "${extra_overrides[@]}"
  ) > "${log_file}" 2>&1 &

  echo "$!" > "${LOG_ROOT}/${run_name}.pid"
  echo "RUNNING ${run_name} gpu=${gpu} pid=$(cat "${LOG_ROOT}/${run_name}.pid") log=${log_file}"
}

run_exp 0 unet ldp_mh mh "${LDP_MH_DATA}" 42
run_exp 1 unet official_ph ph "${OFFICIAL_PH_DATA}" 43
run_exp 0 dit ldp_mh mh "${LDP_MH_DATA}" 44
run_exp 1 dit official_ph ph "${OFFICIAL_PH_DATA}" 45

echo "OUT_ROOT=${OUT_ROOT}"
echo "LOG_ROOT=${LOG_ROOT}"
