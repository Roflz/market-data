#!/bin/bash
# Everything for the detection data, ONE job at a time, each capped at 12 GB.
cd "$(dirname "$0")"
cap() { env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:. python3 "$@"; }
for sym in ES NQ YM; do for tf in 120 60 15 5 1; do cap run_signal_stats.py $sym $tf || echo "FAILED stats $sym $tf"; done; done
for sym in ES NQ YM; do for tf in 120 60 15 5; do cap swing_study.py $sym $tf || echo "FAILED swings $sym $tf"; done; done
for sym in ES NQ YM; do for tf in 60 15 5; do cap chart_swings.py $sym $tf || echo "FAILED chart $sym $tf"; done; done
cap make_report.py
