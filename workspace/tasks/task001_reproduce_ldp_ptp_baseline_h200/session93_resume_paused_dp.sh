#!/usr/bin/env bash
set -euo pipefail

STAMP="${1:-1778075154}"
BASE="/mnt/3fs2/data/tingwen.du/intern_ldp_explorer"
REPO="/mnt/3fs2/data/tingwen.du/workspace/ldp"
PYTHON="/root/venv/bin/python"
OUT_ROOT="${BASE}/outputs/session89_4x2x2_2000ep_${STAMP}"
LOG_ROOT="${BASE}/logs/session89_4x2x2_2000ep_${STAMP}"
LONGSQUARE_IMAGE="${BASE}/datasets/longhistsquare100/image.hdf5"

mkdir -p "${OUT_ROOT}" "${LOG_ROOT}"

resume_dp() {
  local gpu="$1"
  local task="$2"
  local action_horizon="$3"
  local config_dir="$4"
  local config_name="$5"
  local encoder="$6"
  local train_data="$7"
  local rollout_data="$8"
  shift 8

  local run_name="session89_${task}_dp_a${action_horizon}_2000ep_s42_${STAMP}"
  local run_dir="${OUT_ROOT}/${run_name}"
  local log_file="${LOG_ROOT}/${run_name}.resume.log"
  local status_file="${LOG_ROOT}/${run_name}.resume.status"

  if pgrep -f "${run_name}" >/dev/null; then
    echo "SKIP_RUNNING ${run_name}"
    return 0
  fi
  if [[ ! -f "${run_dir}/checkpoints/latest.ckpt" ]]; then
    echo "SKIP_NO_LATEST ${run_name}"
    return 0
  fi

  echo "RESUME $(date -u +%Y-%m-%dT%H:%M:%SZ) gpu=${gpu} task=${task} method=dp action=${action_horizon} run=${run_name}" | tee "${status_file}"
  (
    cd "${REPO}"
    export PYTHONPATH="${REPO}:${PYTHONPATH:-}"
    export CUDA_VISIBLE_DEVICES="${gpu}"
    export MUJOCO_GL=egl
    export WANDB_MODE=disabled
    "${PYTHON}" train.py \
      --config-dir="${config_dir}" \
      --config-name="${config_name}" \
      hydra.run.dir="${run_dir}" \
      obs_encoder_dir="${encoder}" \
      global_obs=16 \
      global_horizon=32 \
      global_action="${action_horizon}" \
      policy.use_embed_if_present=true \
      task.dataset.use_cache=false \
      task.dataset.dataset_path="${train_data}" \
      task.dataset_path="${rollout_data}" \
      task.env_runner.dataset_path="${rollout_data}" \
      logging.mode=offline \
      logging.name="${run_name}_resume" \
      training.debug=false \
      training.device=cuda:0 \
      training.resume=true \
      training.seed=42 \
      training.num_epochs=2000 \
      training.gradient_accumulate_every=1 \
      training.rollout_every=100 \
      training.checkpoint_every=100 \
      training.val_every=1 \
      training.sample_every=5 \
      dataloader.batch_size=64 \
      val_dataloader.batch_size=64 \
      dataloader.num_workers=4 \
      val_dataloader.num_workers=4 \
      task.env_runner.n_envs=4 \
      task.env_runner.n_test=100 \
      task.env_runner.n_test_vis=4 \
      task.env_runner.n_train_vis=2 \
      policy.past_action_pred=false \
      policy.past_steps_reg=-1 \
      "$@"
  ) > "${log_file}" 2>&1 &
  echo "$!" > "${LOG_ROOT}/${run_name}.resume.pid"
  echo "DP_RESUME_RUNNING ${run_name} pid=$(cat "${LOG_ROOT}/${run_name}.resume.pid") log=${log_file}"
}

main() {
  local square_encoder="${BASE}/obs_encoders/obs_encoders/square_encoder.ckpt"
  local tool_encoder="${BASE}/obs_encoders/obs_encoders/tool_hang_encoder.ckpt"
  local transport_encoder="${BASE}/obs_encoders/obs_encoders/transport_encoder.ckpt"
  local longhist_encoder="${BASE}/obs_encoders/obs_encoders/longhist_encoder.ckpt"

  resume_dp 0 square 8 experiment_configs/square transformer_square_emb "${square_encoder}" \
    "${BASE}/datasets/robomimic/datasets/square/mh/image_abs_emb.hdf5" \
    "${BASE}/datasets/robomimic/datasets/square/mh/image_abs.hdf5" \
    task.dataset.use_embed_if_present=true \
    ~task.dataset.shape_meta.obs.agentview_image \
    ~task.dataset.shape_meta.obs.robot0_eye_in_hand_image
  resume_dp 0 square 1 experiment_configs/square transformer_square_emb "${square_encoder}" \
    "${BASE}/datasets/robomimic/datasets/square/mh/image_abs_emb.hdf5" \
    "${BASE}/datasets/robomimic/datasets/square/mh/image_abs.hdf5" \
    task.dataset.use_embed_if_present=true \
    ~task.dataset.shape_meta.obs.agentview_image \
    ~task.dataset.shape_meta.obs.robot0_eye_in_hand_image

  resume_dp 1 toolhang 8 experiment_configs/tool transformer_tool_hang_emb "${tool_encoder}" \
    "${BASE}/datasets/robomimic/datasets/tool_hang/ph/image_abs_emb_compact.hdf5" \
    "${BASE}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5" \
    task.dataset.use_embed_if_present=true \
    ~task.dataset.shape_meta.obs.robot0_eye_in_hand_image \
    ~task.dataset.shape_meta.obs.sideview_image
  resume_dp 1 toolhang 1 experiment_configs/tool transformer_tool_hang_emb "${tool_encoder}" \
    "${BASE}/datasets/robomimic/datasets/tool_hang/ph/image_abs_emb_compact.hdf5" \
    "${BASE}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5" \
    task.dataset.use_embed_if_present=true \
    ~task.dataset.shape_meta.obs.robot0_eye_in_hand_image \
    ~task.dataset.shape_meta.obs.sideview_image

  resume_dp 2 transport 8 experiment_configs/transport transformer_transport_emb "${transport_encoder}" \
    "${BASE}/datasets/robomimic/datasets/transport/mh/image_abs_emb_compact.hdf5" \
    "${BASE}/datasets/robomimic/datasets/transport/mh/image_abs.hdf5" \
    +task.dataset.use_embed_if_present=true \
    +task.dataset.shape_meta.obs.embedding.shape=[274] \
    ~task.dataset.shape_meta.obs.robot0_eye_in_hand_image \
    ~task.dataset.shape_meta.obs.robot1_eye_in_hand_image \
    ~task.dataset.shape_meta.obs.shouldercamera0_image \
    ~task.dataset.shape_meta.obs.shouldercamera1_image
  resume_dp 2 transport 1 experiment_configs/transport transformer_transport_emb "${transport_encoder}" \
    "${BASE}/datasets/robomimic/datasets/transport/mh/image_abs_emb_compact.hdf5" \
    "${BASE}/datasets/robomimic/datasets/transport/mh/image_abs.hdf5" \
    +task.dataset.use_embed_if_present=true \
    +task.dataset.shape_meta.obs.embedding.shape=[274] \
    ~task.dataset.shape_meta.obs.robot0_eye_in_hand_image \
    ~task.dataset.shape_meta.obs.robot1_eye_in_hand_image \
    ~task.dataset.shape_meta.obs.shouldercamera0_image \
    ~task.dataset.shape_meta.obs.shouldercamera1_image

  resume_dp 3 longsquare 1 experiment_configs/longhist transformer_longhist_emb "${longhist_encoder}" \
    "${LONGSQUARE_IMAGE}" \
    "${LONGSQUARE_IMAGE}" \
    task.dataset.use_embed_if_present=true \
    ~task.dataset.shape_meta.obs.agentview_image \
    ~task.dataset.shape_meta.obs.robot0_eye_in_hand_image
}

main "$@"
