#!/bin/bash
# one heavy job at a time: window tests (pid $1, already running) -> bigger charts (MES/MYM 60/120 min + cost_bar)
# -> when the v1 queue (pid $2) is done too: fixed H1/H2 rerun
cd "$(dirname "$0")"
log() { echo "$(date +%H:%M) $*" >> out/resumer.log; }
room() { [ "$(free -m | awk '/Mem:/{print $7}')" -ge 8000 ] && [ "$(awk '{print int($1)}' /proc/loadavg)" -lt "$1" ]; }
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3
while kill -0 "$1" 2>/dev/null; do sleep 60; done
log "END window-tests"
until room 11; do sleep 60; done
log "START bigger-charts (threads 3, cores 6-8, available $(free -m | awk '/Mem:/{print $7}') MB)"
taskset -c 6-8 python3 -u run_bigger_charts.py > out/bigger_charts.log 2>&1
log "END bigger-charts (exit $?)"
while kill -0 "$2" 2>/dev/null; do sleep 60; done
until room 10; do sleep 60; done
log "START h1h2-rerun (threads 3, cores 0-2, available $(free -m | awk '/Mem:/{print $7}') MB)"
taskset -c 0-2 python3 -u run_h1h2.py NQ > out/h1h2_NQ.log 2>&1
log "END h1h2-rerun (exit $?)"
