#!/bin/bash
# 1) when the signal-stats rerun (queue chain pid $1) is done and the machine has room: rolling-window / decay tests
# 2) when the whole queue (pid $2) is done too: the fixed H1/H2 rerun (old outputs in out/h1h2_before_fix/)
cd "$(dirname "$0")"
log() { echo "$(date +%H:%M) $*" >> out/resumer.log; }
room() { [ "$(free -m | awk '/Mem:/{print $7}')" -ge 8000 ] && [ "$(awk '{print int($1)}' /proc/loadavg)" -lt "$1" ]; }
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3
while kill -0 "$1" 2>/dev/null; do sleep 60; done
until room 11; do sleep 60; done
log "START window-tests (threads 3, cores 6-8, available $(free -m | awk '/Mem:/{print $7}') MB)"
taskset -c 6-8 python3 -u run_window_tests.py NQ ES YM > out/window_tests.log 2>&1
log "END window-tests (exit $?)"
while kill -0 "$2" 2>/dev/null; do sleep 60; done
until room 10; do sleep 60; done
log "START h1h2-rerun (threads 3, cores 0-2, available $(free -m | awk '/Mem:/{print $7}') MB)"
taskset -c 0-2 python3 -u run_h1h2.py NQ > out/h1h2_NQ.log 2>&1
log "END h1h2-rerun (exit $?)"
