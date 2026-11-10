#!/bin/bash
# Sequential job queue: ONE heavy job at a time (the machine crashed twice running several at once).
# Memory is logged every minute to out/queue_mem.log; each job's output goes to out/queue_<n>.log.
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.
SIG="cd ../signals && PYTHONPATH=../../pylib:../..:. "
( while true; do echo "$(date +%H:%M) $(free -m | awk '/Mem:/{print "used "$3" MB, available "$7" MB"}')"; sleep 60; done ) >> out/queue_mem.log &
MEMPID=$!
JOBS=(
  "python3 stop_options.py NQ"
  "python3 compare_stops.py NQ"
  "python3 ablate_cost.py"
  "python3 compare_approaches.py NQ sc:stat_shrink_combo"
  "python3 compare_approaches.py NQ sc:stat_screen_nb"
  "python3 compare_approaches.py NQ sc:stat_screen_sa"
  "python3 compare_approaches.py NQ sc:stat_screen_rvm"
  "python3 compare_approaches.py NQ sc:stat_screen_dma"
  "python3 compare_approaches.py NQ sc:stat_screen_dms"
  "python3 compare_approaches.py NQ sc:stat_screen_bma"
  "python3 compare_approaches.py NQ sc:stat_screen_bnn"
  "python3 compare_approaches.py NQ sc:ml_creamer_boost"
  "python3 compare_approaches.py NQ sc:ml_creamer_experts"
  "python3 compare_approaches.py NQ sc:ml_afml_rf|max_rows=150000"
  "python3 compare_approaches.py NQ prior"
  "python3 run_pipeline.py exit --scopes pooled --models gbm"
  "python3 run_pipeline.py exit --scopes ES,NQ,YM"
  "python3 run_pipeline.py perm --workers 2"
  "python3 run_pipeline.py prop"
  "python3 run_pipeline.py report"
  "$SIG TFS=1 bash -c 'for s in ES; do python3 run_signal_stats.py \$s 1; done'"
  "$SIG bash -c 'for tf in 120 60 15 5 1; do python3 run_signal_stats.py NQ \$tf; done'"
  "$SIG bash -c 'for tf in 120 60 15 5 1; do python3 run_signal_stats.py YM \$tf; done'"
  "$SIG python3 make_report.py"
  "$SIG bash -c 'for s in ES NQ YM; do for tf in 120 60 15 5 1; do python3 run_exit_study.py \$s \$tf; done; done'"
  "$SIG python3 make_exit_report.py"
)
n=0
for j in "${JOBS[@]}"; do
  n=$((n+1))
  echo "$(date +%H:%M) START $n: $j" >> out/queue_status.log
  bash -c "$j" > out/queue_$n.log 2>&1
  echo "$(date +%H:%M) END $n (exit $?)  $(free -m | awk '/Mem:/{print "available "$7" MB"}')" >> out/queue_status.log
done
kill $MEMPID
echo "$(date +%H:%M) QUEUE DONE" >> out/queue_status.log
