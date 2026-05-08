#!/usr/bin/env bash
set -euo pipefail

TASK_ROOT=${TASK_ROOT:-/mnt/3fs2/data/tingwen.du/intern_method_developer/task006_eval_official_robomimic_square_bcrnn}
PYTHON=${PYTHON:-/root/venv/bin/python}
STAMP="${1:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${TASK_ROOT}/runs/smolvla_fourway_1000ep_${STAMP}"
LOG_ROOT="${TASK_ROOT}/logs/smolvla_fourway_1000ep_${STAMP}"

TRAIN_SCRIPT="${TRAIN_SCRIPT:-${TASK_ROOT}/scripts/train_eval_smolvla_square_scheduled.py}"
PTP_DATA=${PTP_DATA:-/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/data/square_mh_image_abs.hdf5}
V141_DATA=${V141_DATA:-${TASK_ROOT}/data/square/ph/image_abs_v141.hdf5}

SMOL_NUM_EPOCHS=${SMOL_NUM_EPOCHS:-1000}
SMOL_EVAL_EARLY_EVERY=${SMOL_EVAL_EARLY_EVERY:-10}
SMOL_EVAL_EARLY_UNTIL=${SMOL_EVAL_EARLY_UNTIL:-100}
SMOL_EVAL_LATE_EVERY=${SMOL_EVAL_LATE_EVERY:-100}
SMOL_CHECKPOINT_EVERY=${SMOL_CHECKPOINT_EVERY:-25}
SMOL_BATCH_SIZE=${SMOL_BATCH_SIZE:-128}
SMOL_NUM_WORKERS=${SMOL_NUM_WORKERS:-4}

mkdir -p "${OUT_ROOT}" "${LOG_ROOT}"

if [[ ! -x "${PYTHON}" ]]; then
  echo "Missing python venv: ${PYTHON}" >&2
  exit 1
fi
if [[ ! -f "${TRAIN_SCRIPT}" ]]; then
  echo "Missing train script: ${TRAIN_SCRIPT}" >&2
  exit 1
fi

run_exp() {
  local gpu="$1"
  local dataset_name="$2"
  local dataset_path="$3"
  local size_name="$4"
  local emb_dim="$5"
  local expert_layers="$6"
  local seed="$7"

  local run_name run_dir log_file status_file cmd_file pid
  run_name="smolvla_${size_name}_${dataset_name}_abs10_seed${seed}"
  run_dir="${OUT_ROOT}/${run_name}"
  log_file="${LOG_ROOT}/${run_name}.log"
  status_file="${LOG_ROOT}/${run_name}.status"
  cmd_file="${LOG_ROOT}/${run_name}.cmd.sh"

  if pgrep -f "${run_name}" >/dev/null; then
    echo "SKIP_RUNNING ${run_name}"
    return 0
  fi

  echo "START $(date -u +%Y-%m-%dT%H:%M:%SZ) gpu=${gpu} run=${run_name}" | tee "${status_file}"
  cat > "${cmd_file}" <<EOF
#!/usr/bin/env bash
set -euo pipefail
export CUDA_VISIBLE_DEVICES="${gpu}"
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=4
export MUJOCO_GL=egl
exec "${PYTHON}" "${TRAIN_SCRIPT}" \\
      --dataset "${dataset_path}" \
      --output "${run_dir}" \
      --chunk-size 16 \
      --batch-size "${SMOL_BATCH_SIZE}" \
      --epochs "${SMOL_NUM_EPOCHS}" \
      --lr 1e-4 \
      --weight-decay 1e-4 \
      --emb-dim "${emb_dim}" \
      --expert-layers "${expert_layers}" \
      --heads 8 \
      --dropout 0.1 \
      --num-workers "${SMOL_NUM_WORKERS}" \
      --val-ratio 0.05 \
      --eval-early-every-epochs "${SMOL_EVAL_EARLY_EVERY}" \
      --eval-early-until-epochs "${SMOL_EVAL_EARLY_UNTIL}" \
      --eval-late-every-epochs "${SMOL_EVAL_LATE_EVERY}" \
      --checkpoint-every-epochs "${SMOL_CHECKPOINT_EVERY}" \
      --log-every-steps 100 \
      --max-val-batches 0 \
      --sample-steps 10 \
      --action-repr ldp_abs10 \
      --seed "${seed}" \
      --amp \
      --resume
EOF
  chmod +x "${cmd_file}"

  nohup bash "${cmd_file}" > "${log_file}" 2>&1 < /dev/null &
  pid="$!"
  echo "${pid}" > "${LOG_ROOT}/${run_name}.pid"
  echo "RUNNING ${run_name} gpu=${gpu} pid=${pid} log=${log_file}"
}

# Balance one large run per GPU while still covering both data versions.
run_exp 0 ptp_ldp_mh "${PTP_DATA}" small 256 6 52
run_exp 1 ptp_ldp_mh "${PTP_DATA}" big384 384 8 53
run_exp 0 official_ph_v141 "${V141_DATA}" big384 384 8 54
run_exp 1 official_ph_v141 "${V141_DATA}" small 256 6 55

echo "OUT_ROOT=${OUT_ROOT}"
echo "LOG_ROOT=${LOG_ROOT}"
