#!/bin/bash
# exit study for every market and timeframe; one process per market, timeframes in sequence
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:.
for S in ES NQ YM; do
  ( for T in 120 60 15 5; do python3 run_exit_study.py $S $T 2>&1 | grep -v "done (" ; done ) > out/exits_log_$S.txt &
done
wait
echo ALL DONE
