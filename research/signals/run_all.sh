#!/bin/bash
# Runs every market/timeframe ONE AT A TIME, each in its own process capped at 6 GB of memory.
cd "$(dirname "$0")"
for sym in ES NQ YM; do
  for tf in ${TFS:-120 60 15 5 1}; do
    \
      env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:. python3 run_signal_stats.py $sym $tf \
      || echo "FAILED $sym $tf"
  done
done
