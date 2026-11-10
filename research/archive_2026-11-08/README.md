# Research archive, 2026-11-08

Scripts, pre-registered rule files and results from the review-doc work on this day, copied out of the session
scratchpad so they can be re-run or checked later. Large caches (*.pkl, *.npz, files over 20 MB) were left out; the
scripts rebuild them. Paths inside the scripts still point at the old scratchpad folder: change S/T at the top of a
script to this folder before re-running. New tests should use research_lib.py (the shared toolkit) instead.

| Folder / file | What it is | Review doc |
|---|---|---|
| tests/specs/ | rule files for sections 11-13 + CONVENTIONS.md (data, costs, rules of the game) | 11-13 |
| tests/s11_*, s12_*, s13_* | two independent builds (X, Y) and the reconcile for each section | 11-13 |
| l1b/ | jobs-report fade exits (L1b), price paths after entry, jobs-day filter (L1c) | 13 |
| filters/ | SPEC.md (W, T1-T4) and SWEEP.md (42 wide-stop versions), builds and reconciles | 15 |
| stopcap/ | stop caps as a share of price, sweep, per-period $ and which trades a cap changes | 6.2 |
| next/paper | paper-log test backfills | 14 |
| next/sizing*, next/rebal* | position sizing study; rebalancing rule A (pre-registration + hash + check) | 14 |
| sessions/ | time-of-day volatility map and event continuation tests | 13 |
| caltests/, caltests2/ | calendar tests 1-14 | 9 |
| skiprules/ | R1/R2 skip-rule robustness | 10 |
| orb_grid.py, stop_grid.py | opening-range 720-combination grid; overnight-break stop/management grid | 6.2, 1.9 |
| expiry_fade.py, p2_regime.py, vol_vs_trades.py | expiry fade, P2 by regime, volatility vs results | 8.3-8.4, 3.3 |
