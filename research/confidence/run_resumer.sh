#!/bin/bash
# Load-aware resumer: resumes paused jobs / starts new ones ONE AT A TIME, only when the 1-minute load average is
# below MAXLOAD (about one runnable thread per core on this 12-core machine) and available RAM >= MINFREE_MB.
# New jobs get capped thread pools so they share cores instead of oversubscribing them.
# Log: out/resumer.log
cd "$(dirname "$0")"
MAXLOAD=${MAXLOAD:-13}; MINFREE_MB=${MINFREE_MB:-8000}
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.
log() { echo "$(date +%H:%M) $*" >> out/resumer.log; }
ready() {
  local l a
  l=$(awk '{print int($1)}' /proc/loadavg); a=$(free -m | awk '/Mem:/{print $7}')
  [ "$l" -lt "$MAXLOAD" ] && [ "$a" -ge "$MINFREE_MB" ]
}
wait_ready() { until ready; do sleep 30; done; }
alive() { kill -0 "$1" 2>/dev/null; }
start() {   # $1 = threads, $2 = name, $3 = command
  log "START $2 (threads $1, load $(cut -d' ' -f1 /proc/loadavg), available $(free -m | awk '/Mem:/{print $7}') MB)"
  ( export OMP_NUM_THREADS=$1 OPENBLAS_NUM_THREADS=$1 MKL_NUM_THREADS=$1
    bash -c "$3" > "out/resumer_$2.log" 2>&1; log "END $2 (exit $?)" ) &
}
# the old scheduler loop and its memory logger: stop them (their running chains are separate processes)
kill -CONT 126988 2>/dev/null; kill 126991 126988 2>/dev/null
for pid_name in "130042 prior-approaches" "129460 stat-approaches" "129843 rf-approach"; do
  set -- $pid_name
  if alive "$1"; then wait_ready; log "RESUME $2 (pid $1, load $(cut -d' ' -f1 /proc/loadavg))"; kill -CONT "$1"; sleep 120; fi
done
wait_ready; start 3 sane-check "python3 check_sane_by_year.py"; sleep 120
wait_ready; start 4 v1-rest "python3 run_pipeline.py exit --scopes pooled --models gbm && python3 run_pipeline.py exit --scopes ES,NQ,YM && python3 run_pipeline.py perm --workers 2 && python3 run_pipeline.py prop && python3 run_pipeline.py report"; sleep 120
wait_ready; start 2 stats-rerun "cd ../signals && export PYTHONPATH=../../pylib:../..:. && python3 run_signal_stats.py ES 1; for tf in 120 60 15 5 1; do python3 run_signal_stats.py NQ \$tf; done; for tf in 120 60 15 5 1; do python3 run_signal_stats.py YM \$tf; done; python3 make_report.py; for s in ES NQ YM; do for tf in 120 60 15 5 1; do python3 run_exit_study.py \$s \$tf; done; done; python3 make_exit_report.py"
wait
log "ALL STARTED JOBS DONE"
