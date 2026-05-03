#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-start}"

TASK_ROOT="/work-agents/intern_ldp_explorer/ldp/workspace/tasks/task001_reproduce_ldp_ptp_baseline_h200"
OUT_DIR="/work-agents/intern_ldp_explorer/outputs/session25_monitor_schedule"
STATE_DIR="${OUT_DIR}/state"
PID_DIR="${OUT_DIR}/pids"
LOG_FILE="${OUT_DIR}/session25_monitor_schedule.log"

DOWNLOAD_STAGING="/work-agents/intern_ldp_explorer/outputs/session17_dataset_downloads"
DOWNLOAD_MANIFEST="${DOWNLOAD_STAGING}/manifest.tsv"

REMOTE_HOST="root@10.100.2.47"
REMOTE_PORT="15744"
REMOTE_ROOT="/mnt/3fs2/data/tingwen.du/intern_ldp_explorer"
REMOTE_LOG_DIR="${REMOTE_ROOT}/logs"
REMOTE_OUT_DIR="${REMOTE_ROOT}/outputs"

MAX_CHECKS=12
SLEEP_SECONDS=600

mkdir -p "${OUT_DIR}" "${STATE_DIR}" "${PID_DIR}"

log() {
    printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*" | tee -a "${LOG_FILE}"
}

remote_sh() {
    ssh -o StrictHostKeyChecking=no -p "${REMOTE_PORT}" "${REMOTE_HOST}" "$@"
}

archive_size() {
    local path="$1"
    if [[ -f "${path}" ]]; then
        stat -c '%s' "${path}"
    else
        echo 0
    fi
}

check_download_status() {
    local done_count=0
    local total_count=0
    while IFS=$'\t' read -r name _url expected_bytes archive_path done_marker; do
        [[ "${name}" == "name" ]] && continue
        total_count=$((total_count + 1))
        local status="running"
        local size
        size="$(archive_size "${archive_path}")"
        if [[ -f "${done_marker}" ]]; then
            status="done"
            done_count=$((done_count + 1))
        fi
        log "download:${name}:status=${status}:size_bytes=${size}:expected_bytes=${expected_bytes}"
    done < "${DOWNLOAD_MANIFEST}"
    log "download:summary:${done_count}/${total_count}_complete"
}

robomimic_ready() {
    remote_sh "test -f '${REMOTE_ROOT}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5' && test -f '${REMOTE_ROOT}/datasets/robomimic/datasets/transport/mh/image_abs.hdf5'"
}

all_datasets_ready() {
    [[ -f "${DOWNLOAD_STAGING}/robomimic_image.done" ]] || return 1
    [[ -f "${DOWNLOAD_STAGING}/pusht.done" ]] || return 1
    [[ -f "${DOWNLOAD_STAGING}/aloha_twomodes_single.done" ]] || return 1
    [[ -f "${DOWNLOAD_STAGING}/longhistsquare100.done" ]] || return 1
    robomimic_ready
}

sync_wave1_configs() {
    remote_sh "mkdir -p '${REMOTE_ROOT}/my_configs/tool'"
    scp -P "${REMOTE_PORT}" \
        /work-agents/intern_ldp_explorer/ldp/experiment_configs/tool/transformer_tool_hang.yaml \
        "${REMOTE_HOST}:${REMOTE_ROOT}/my_configs/tool/transformer_tool_hang.yaml" >/dev/null
}

launch_wave1() {
    if [[ -f "${STATE_DIR}/wave1_launched" ]]; then
        log "wave1:already_launched"
        return 0
    fi

    sync_wave1_configs

    local stamp
    stamp="$(date +%s)"

    local dp_run="session25_toolhang_longhist_dp_${stamp}"
    local ptp_run="session25_toolhang_longhist_ptp_${stamp}"

    local base_cmd="source ~/.bashrc 2>/dev/null; cd '${REMOTE_ROOT}'; export WANDB_MODE=offline; export HF_HOME='${REMOTE_ROOT}/hf_cache';"

    local dp_cmd="${base_cmd} CUDA_VISIBLE_DEVICES=0 nohup python '${REMOTE_ROOT}/run_train.py' \
--config-dir='${REMOTE_ROOT}/my_configs/tool' \
--config-name=transformer_tool_hang \
global_obs=16 \
dataloader.num_workers=4 \
dataloader.batch_size=64 \
dataloader.persistent_workers=true \
val_dataloader.num_workers=4 \
val_dataloader.batch_size=64 \
val_dataloader.persistent_workers=true \
logging.mode=offline \
policy.past_action_pred=false \
task.dataset.use_cache=false \
task.dataset.dataset_path='${REMOTE_ROOT}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5' \
task.dataset_path='${REMOTE_ROOT}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5' \
task.env_runner.dataset_path='${REMOTE_ROOT}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5' \
hydra.run.dir='${REMOTE_OUT_DIR}/${dp_run}' \
> '${REMOTE_LOG_DIR}/${dp_run}.log' 2>&1 & echo \$! > '${REMOTE_LOG_DIR}/${dp_run}.pid'"

    local ptp_cmd="${base_cmd} CUDA_VISIBLE_DEVICES=0 nohup python '${REMOTE_ROOT}/run_train.py' \
--config-dir='${REMOTE_ROOT}/my_configs/tool' \
--config-name=transformer_tool_hang \
global_obs=16 \
dataloader.num_workers=4 \
dataloader.batch_size=64 \
dataloader.persistent_workers=true \
val_dataloader.num_workers=4 \
val_dataloader.batch_size=64 \
val_dataloader.persistent_workers=true \
logging.mode=offline \
policy.past_action_pred=true \
task.dataset.use_cache=false \
task.dataset.dataset_path='${REMOTE_ROOT}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5' \
task.dataset_path='${REMOTE_ROOT}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5' \
task.env_runner.dataset_path='${REMOTE_ROOT}/datasets/robomimic/datasets/tool_hang/ph/image_abs.hdf5' \
hydra.run.dir='${REMOTE_OUT_DIR}/${ptp_run}' \
> '${REMOTE_LOG_DIR}/${ptp_run}.log' 2>&1 & echo \$! > '${REMOTE_LOG_DIR}/${ptp_run}.pid'"

    remote_sh "mkdir -p '${REMOTE_LOG_DIR}' '${REMOTE_OUT_DIR}'"
    remote_sh "${dp_cmd}"
    remote_sh "${ptp_cmd}"

    {
        echo "stamp=${stamp}"
        echo "dp_run=${dp_run}"
        echo "ptp_run=${ptp_run}"
        echo "gpu=0"
    } > "${STATE_DIR}/wave1_launched"

    log "wave1:launched:${dp_run}:${ptp_run}"
}

run_check() {
    local idx="$1"
    log "check:${idx}:begin"
    check_download_status
    if all_datasets_ready; then
        log "check:${idx}:all_datasets_ready"
        launch_wave1
        return 0
    fi
    log "check:${idx}:datasets_not_ready"
    return 1
}

monitor_loop() {
    local idx
    for idx in $(seq 1 "${MAX_CHECKS}"); do
        if run_check "${idx}"; then
            log "monitor:success:stopping_after_check=${idx}"
            return 0
        fi
        if [[ "${idx}" -lt "${MAX_CHECKS}" ]]; then
            log "monitor:sleep_seconds=${SLEEP_SECONDS}"
            sleep "${SLEEP_SECONDS}"
        fi
    done
    log "monitor:exhausted_checks_without_full_completion"
}

case "${MODE}" in
    start)
        setsid "${BASH_SOURCE[0]}" monitor > "${OUT_DIR}/monitor.nohup.log" 2>&1 < /dev/null &
        echo "$!" > "${PID_DIR}/monitor.pid"
        log "start:monitor_pid=$(cat "${PID_DIR}/monitor.pid")"
        ;;
    monitor)
        monitor_loop
        ;;
    once)
        run_check 0 || true
        ;;
    *)
        echo "unknown mode: ${MODE}" >&2
        exit 1
        ;;
esac
