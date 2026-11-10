#!/bin/bash
# RAM-aware scheduler: independent CHAINS run in parallel (jobs inside a chain run in order).
# A chain starts only when fewer than MAXPAR chains are running AND available RAM >= MINFREE_MB; 120 s between starts.
# Status: out/sched_status.log; memory every minute: out/sched_mem.log; each chain's output: out/sched_chain_<n>.log
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.
MAXPAR=${MAXPAR:-3}; MINFREE_MB=${MINFREE_MB:-8000}
SIG='cd ../signals && export PYTHONPATH=../../pylib:../..:. &&'
CHAINS=(
  'python3 stop_options.py NQ && python3 compare_stops.py NQ'
  'python3 ablate_cost.py'
  'for s in stat_shrink_combo stat_screen_nb stat_screen_sa stat_screen_rvm stat_screen_dma stat_screen_dms stat_screen_bma stat_screen_bnn; do python3 compare_approaches.py NQ sc:$s; done'
  'python3 compare_approaches.py NQ sc:ml_creamer_boost; python3 compare_approaches.py NQ sc:ml_creamer_experts; python3 compare_approaches.py NQ "sc:ml_afml_rf|max_rows=150000"'
  'python3 compare_approaches.py NQ prior'
  'python3 run_pipeline.py exit --scopes pooled --models gbm && python3 run_pipeline.py exit --scopes ES,NQ,YM && python3 run_pipeline.py perm --workers 2 && python3 run_pipeline.py prop && python3 run_pipeline.py report'
  "$SIG"' python3 run_signal_stats.py ES 1; for tf in 120 60 15 5 1; do python3 run_signal_stats.py NQ $tf; done; for tf in 120 60 15 5 1; do python3 run_signal_stats.py YM $tf; done; python3 make_report.py; for s in ES NQ YM; do for tf in 120 60 15 5 1; do python3 run_exit_study.py $s $tf; done; done; python3 make_exit_report.py'
)
avail() { free -m | awk '/Mem:/{print $7}'; }
( while true; do echo "$(date +%H:%M) used $(free -m | awk '/Mem:/{print $3}') MB, available $(avail) MB"; sleep 60; done ) >> out/sched_mem.log &
MEMPID=$!
pids=()
for n in "${!CHAINS[@]}"; do
  while true; do
    running=0; for p in "${pids[@]}"; do kill -0 "$p" 2>/dev/null && running=$((running+1)); done
    [ "$running" -lt "$MAXPAR" ] && [ "$(avail)" -ge "$MINFREE_MB" ] && break
    sleep 30
  done
  echo "$(date +%H:%M) START chain $n (available $(avail) MB): ${CHAINS[$n]:0:100}" >> out/sched_status.log
  ( bash -c "${CHAINS[$n]}" > "out/sched_chain_$n.log" 2>&1; echo "$(date +%H:%M) END chain $n (exit $?) available $(avail) MB" >> out/sched_status.log ) &
  pids+=($!)
  sleep 120
done
wait "${pids[@]}"
kill $MEMPID
echo "$(date +%H:%M) ALL CHAINS DONE" >> out/sched_status.log
