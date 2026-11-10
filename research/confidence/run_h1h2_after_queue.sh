#!/bin/bash
# Waits for the load-aware queue (run_resumer.sh, pid given as $1) to finish, then reruns the H1/H2 study with the
# 2026-11-09 fixes (entry slips 1 tick; gbm/min_inner sized for ~4k trades). Old outputs: out/h1h2_before_fix/.
cd "$(dirname "$0")"
QPID=$1
log() { echo "$(date +%H:%M) $*" >> out/resumer.log; }
while kill -0 "$QPID" 2>/dev/null; do sleep 60; done
until [ "$(free -m | awk '/Mem:/{print $7}')" -ge 8000 ] && [ "$(awk '{print int($1)}' /proc/loadavg)" -lt 10 ]; do sleep 60; done
log "START h1h2-rerun (threads 3, cores 0-2, available $(free -m | awk '/Mem:/{print $7}') MB)"
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3
taskset -c 0-2 python3 -u run_h1h2.py NQ > out/h1h2_NQ.log 2>&1
log "END h1h2-rerun (exit $?)"
