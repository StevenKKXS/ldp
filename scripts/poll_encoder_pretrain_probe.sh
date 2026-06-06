#!/usr/bin/env bash
set -euo pipefail

LOG_BASE="${LOG_BASE:-/mnt/nfs/tingwen/intern_method_developer/tasks/ptp_encoder_probe/logs/20260518_session8}"
PID_FILE="${PID_FILE:-${LOG_BASE}/pids.tsv}"

if [[ ! -f "${PID_FILE}" ]]; then
  echo "Missing PID file: ${PID_FILE}" >&2
  exit 1
fi

printf "exp_id\tpid\tstate\tlast_log_line\n"
tail -n +2 "${PID_FILE}" | while IFS=$'\t' read -r exp_id pid gpu log_path output_dir; do
  if kill -0 "${pid}" 2>/dev/null; then
    state="running"
  else
    state="exited"
  fi
  if [[ -f "${log_path}" ]]; then
    last_line="$(
      tail -c 4000 "${log_path}" \
        | tr '\r' '\n' \
        | grep -v '^$' \
        | tail -n 1 \
        | tr '\t' ' ' \
        | cut -c 1-180
    )"
  else
    last_line="log_missing"
  fi
  printf "%s\t%s\t%s\t%s\n" "${exp_id}" "${pid}" "${state}" "${last_line}"
done
