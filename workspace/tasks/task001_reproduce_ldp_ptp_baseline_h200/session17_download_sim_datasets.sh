#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-start}"

TASK_ROOT="/work-agents/intern_ldp_explorer/ldp/workspace/tasks/task001_reproduce_ldp_ptp_baseline_h200"
STAGING_DIR="/work-agents/intern_ldp_explorer/outputs/session17_dataset_downloads"
LOG_DIR="${STAGING_DIR}/logs"
MANIFEST="${STAGING_DIR}/manifest.tsv"
PROGRESS_LOG="${STAGING_DIR}/progress.log"
TARGET_ROOT="/mnt/3fs2/data/tingwen.du/intern_ldp_explorer/datasets"
PID_DIR="${STAGING_DIR}/pids"

mkdir -p "${STAGING_DIR}" "${LOG_DIR}" "${PID_DIR}" "${TARGET_ROOT}"

gdrive_final_url() {
    local file_id="$1"
    local tmp_html
    tmp_html="$(mktemp)"
    wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate \
        "https://drive.google.com/uc?export=download&id=${file_id}" -O "${tmp_html}"
    local uuid confirm
    uuid="$(grep -oP 'name="uuid" value="\K[^"]+' "${tmp_html}" | head -n 1)"
    confirm="$(grep -oP 'name="confirm" value="\K[^"]+' "${tmp_html}" | head -n 1)"
    rm -f "${tmp_html}"
    echo "https://drive.usercontent.google.com/download?id=${file_id}&export=download&confirm=${confirm}&uuid=${uuid}"
}

http_size() {
    local url="$1"
    curl -fsSLI "${url}" | awk 'tolower($1)=="content-length:" {print $2}' | tr -d '\r' | tail -n 1
}

human_bytes() {
    local bytes="${1:-0}"
    if [[ -z "${bytes}" || "${bytes}" == "unknown" ]]; then
        printf "unknown"
        return
    fi
    awk -v b="${bytes}" 'BEGIN{
        split("B KiB MiB GiB TiB PiB",u," ");
        i=1;
        while (b>=1024 && i<6) {b/=1024; i++}
        printf "%.2f %s", b, u[i]
    }'
}

human_duration() {
    local secs="${1:-0}"
    if [[ -z "${secs}" || "${secs}" == "unknown" ]]; then
        printf "unknown"
        return
    fi
    awk -v s="${secs}" 'BEGIN{
        h=int(s/3600); m=int((s%3600)/60); sec=int(s%60);
        if (h>0) printf "%dh%02dm%02ds", h, m, sec;
        else if (m>0) printf "%dm%02ds", m, sec;
        else printf "%ds", sec;
    }'
}

write_manifest() {
    local aloha_url longhist_url
    aloha_url="$(gdrive_final_url "1gwzIRBmn0a4Orj2okMNQ9qiPPpxmqdKA")"
    longhist_url="$(gdrive_final_url "1-ZDi8-aVx1I8aZCan-vXJQIpLyCCNwym")"

    {
        printf "name\turl\texpected_bytes\tarchive_path\tdone_marker\n"
        printf "robomimic_image\thttps://diffusion-policy.cs.columbia.edu/data/training/robomimic_image.zip\t%s\t%s\t%s\n" \
            "$(http_size "https://diffusion-policy.cs.columbia.edu/data/training/robomimic_image.zip" || echo unknown)" \
            "${STAGING_DIR}/robomimic_image.zip" \
            "${STAGING_DIR}/robomimic_image.done"
        printf "pusht\thttps://diffusion-policy.cs.columbia.edu/data/training/pusht.zip\t%s\t%s\t%s\n" \
            "$(http_size "https://diffusion-policy.cs.columbia.edu/data/training/pusht.zip" || echo unknown)" \
            "${STAGING_DIR}/pusht.zip" \
            "${STAGING_DIR}/pusht.done"
        printf "aloha_twomodes_single\t%s\t%s\t%s\t%s\n" \
            "${aloha_url}" \
            "$(http_size "${aloha_url}" || echo unknown)" \
            "${STAGING_DIR}/aloha_twomodes_single.zip" \
            "${STAGING_DIR}/aloha_twomodes_single.done"
        printf "longhistsquare100\t%s\t%s\t%s\t%s\n" \
            "${longhist_url}" \
            "$(http_size "${longhist_url}" || echo unknown)" \
            "${STAGING_DIR}/longhistsquare100.zip" \
            "${STAGING_DIR}/longhistsquare100.done"
    } > "${MANIFEST}"
}

download_one() {
    local name="$1" url="$2" archive="$3" done_marker="$4"
    local log_file="${LOG_DIR}/${name}.log"
    if [[ -f "${done_marker}" ]]; then
        echo "[$(date -u +%FT%TZ)] ${name}: already complete" >> "${log_file}"
        return 0
    fi

    echo "[$(date -u +%FT%TZ)] ${name}: download start" >> "${log_file}"
    wget -c -O "${archive}" "${url}" >> "${log_file}" 2>&1
    echo "[$(date -u +%FT%TZ)] ${name}: download finished, extracting" >> "${log_file}"
    unzip -n "${archive}" -d "${TARGET_ROOT}" >> "${log_file}" 2>&1
    touch "${done_marker}"
    echo "[$(date -u +%FT%TZ)] ${name}: complete" >> "${log_file}"
}

start_downloads() {
    tail -n +2 "${MANIFEST}" | while IFS=$'\t' read -r name url expected archive done_marker; do
        nohup bash -lc "$(printf '%q ' "${BASH_SOURCE[0]}" worker "${name}" "${url}" "${archive}" "${done_marker}")" \
            > "${LOG_DIR}/${name}.nohup.log" 2>&1 &
        echo "$!" > "${PID_DIR}/${name}.pid"
    done
}

monitor_loop() {
    local last_ts
    last_ts="$(date +%s)"
    while true; do
        local now
        now="$(date +%s)"
        {
            echo "===== $(date -u +%FT%TZ) ====="
        } >> "${PROGRESS_LOG}"

        local all_done=1
        local max_eta=0
        while IFS=$'\t' read -r name url expected archive done_marker; do
            [[ "${name}" == "name" ]] && continue
            local size=0 elapsed=0 rate=0 eta="unknown" status="running"
            if [[ -f "${done_marker}" ]]; then
                status="done"
            else
                all_done=0
            fi
            if [[ -f "${archive}" ]]; then
                size="$(stat -c '%s' "${archive}")"
                elapsed=$(( now - $(stat -c '%Y' "${archive}") + 1 ))
                if (( elapsed > 0 )); then
                    rate=$(( size / elapsed ))
                fi
            fi
            if [[ "${expected}" != "unknown" && "${rate}" -gt 0 && "${size}" -lt "${expected}" ]]; then
                eta=$(( (expected - size) / rate ))
                if (( eta > max_eta )); then
                    max_eta="${eta}"
                fi
            elif [[ -f "${done_marker}" ]]; then
                eta=0
            fi
            printf "%s\tstatus=%s\tsize=%s\tavg_rate=%s/s\teta=%s\n" \
                "${name}" \
                "${status}" \
                "$(human_bytes "${size}")" \
                "$(human_bytes "${rate}")" \
                "$(human_duration "${eta}")" >> "${PROGRESS_LOG}"
        done < "${MANIFEST}"

        if (( all_done == 1 )); then
            echo "ALL_DOWNLOADS_COMPLETE" >> "${PROGRESS_LOG}"
            break
        fi

        if (( max_eta > 0 )); then
            echo "aggregate_download_eta=$(human_duration "${max_eta}")" >> "${PROGRESS_LOG}"
        else
            echo "aggregate_download_eta=unknown" >> "${PROGRESS_LOG}"
        fi
        echo >> "${PROGRESS_LOG}"
        sleep 600
        last_ts="${now}"
    done
}

case "${MODE}" in
    start)
        write_manifest
        start_downloads
        nohup bash -lc "$(printf '%q ' "${BASH_SOURCE[0]}" monitor)" > "${LOG_DIR}/monitor.nohup.log" 2>&1 &
        echo $! > "${PID_DIR}/monitor.pid"
        ;;
    worker)
        download_one "$2" "$3" "$4" "$5"
        ;;
    monitor)
        monitor_loop
        ;;
    *)
        echo "unknown mode: ${MODE}" >&2
        exit 1
        ;;
esac
