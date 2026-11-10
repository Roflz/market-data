# Impact card: fomc_day

scheduled FOMC statement session (data/fomc_dates.csv) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (5 min), p=0.98; we would catch an effect of 0.047 R20 or more 80% of the time).
- MES 5-min size: the market moves 41% MORE after the event than after matched bars over the rest of the session (to 16:45) (+4.046 R20, possible, q=0.169, 12 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.08 at recent bar sizes, 90% range up to $1.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.022 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.088 R20 or more 80% of the time).
- MES 15-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.024 R20, CONFIRMED, q=0.00555, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.51 at recent bar sizes, 90% range up to $3.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.183 R20 or more 80% of the time).
- MES 60-min size: the market moves 11% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.055 R20, CONFIRMED, q=0.0232, 12 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.33 at recent bar sizes, 90% range up to $14.55); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.028 R20 over the next 4 bars (20 min), p=0.76; we would catch an effect of 0.055 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.051).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.71 at recent bar sizes, 90% range up to $2.86); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.137 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.102 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.092).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.48 at recent bar sizes, 90% range up to $7.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.017 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.202 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.038).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.37 at recent bar sizes, 90% range up to $30.13); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -3.409 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.075 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.056).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $37.88 at recent bar sizes, 90% range up to $1.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -1.802 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.138 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.24).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $32.42 at recent bar sizes, 90% range up to $4.34); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.878 R20 over the rest of the session (to 16:45), p=0.62; we would catch an effect of 0.286 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.21).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $33.05 at recent bar sizes, 90% range up to $27.71); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.006 | -0.002 .. +0.013 | +0.0014 | 0.13 / 0.14 / 0.18 | 0.175 | 1 | 1 | 11/16 | +0.006 | +0.005 | False | +1.3 / +1.5 |  |
| MES | 5 | h2 | +0.010 | -0.004 .. +0.025 | +0.0018 | 0.15 / 0.16 / 0.2 | 0.2 |  |  | 11/16 | +0.010 | +0.011 |  | +1.7 / +1.5 |  |
| MES | 5 | h4 | +0.022 | -0.007 .. +0.051 | +0.0026 | 0.13 / 0.14 / 0.19 | 0.193 |  |  | 11/16 | +0.020 | +0.024 |  | +2.6 / +1.5 | 0.047 |
| MES | 5 | h8 | +0.045 | -0.015 .. +0.105 | +0.0038 | 0.14 / 0.15 / 0.19 | 0.191 |  |  | 11/16 | +0.040 | +0.051 |  | +3.7 / +1.5 |  |
| MES | 5 | h16 | +0.093 | -0.038 .. +0.224 | +0.0054 | 0.17 / 0.18 / 0.19 | 0.196 |  |  | 10/16 | +0.085 | +0.100 |  | +5.0 / +1.4 |  |
| MES | 5 | eod | -0.497 | -3.970 .. +2.977 | -0.0057 | 0.78 / 0.79 / 0.67 | 0.67 |  |  | 8/16 | +1.045 | -2.030 |  | -3.8 / -0.3 |  |
| MES | 15 | h1 | +0.003 | -0.011 .. +0.018 | +0.0008 | 0.65 / 0.66 / 0.66 | 0.679 |  |  | 9/16 | +0.005 | +0.002 |  | +0.4 / +0.5 |  |
| MES | 15 | h2 | +0.009 | -0.021 .. +0.038 | +0.0014 | 0.55 / 0.56 / 0.57 | 0.586 |  |  | 9/16 | +0.013 | +0.005 |  | +0.8 / +0.6 |  |
| MES | 15 | h4 * | +0.022 | -0.039 .. +0.083 | +0.0022 | 0.49 / 0.5 / 0.5 | 0.508 | 1 | 1 | 10/16 | +0.031 | +0.012 | False | +1.3 / +0.7 | 0.088 |
| MES | 15 | h8 | +0.041 | -0.089 .. +0.170 | +0.0030 | 0.54 / 0.55 / 0.53 | 0.545 |  |  | 10/16 | +0.069 | +0.012 |  | +1.6 / +0.6 |  |
| MES | 15 | h16 | +0.073 | -0.207 .. +0.353 | +0.0038 | 0.61 / 0.62 / 0.59 | 0.605 |  |  | 10/16 | +0.145 | +0.002 |  | +1.9 / +0.5 |  |
| MES | 15 | eod | -0.252 | -2.127 .. +1.622 | -0.0050 | 0.79 / 0.8 / 0.71 | 0.698 |  |  | 9/16 | +0.637 | -1.138 |  | -2.1 / -0.3 |  |
| MES | 60 | h1 * | +0.007 | -0.033 .. +0.047 | +0.0016 | 0.74 / 0.74 / 0.68 | 0.678 | 1 | 1 | 8/16 | +0.016 | -0.002 | False | +0.3 / +0.3 |  |
| MES | 60 | h2 | +0.008 | -0.074 .. +0.090 | +0.0013 | 0.84 / 0.84 / 0.8 | 0.802 |  |  | 8/16 | +0.027 | -0.011 |  | +0.3 / +0.2 |  |
| MES | 60 | h4 | +0.013 | -0.152 .. +0.178 | +0.0015 | 0.88 / 0.88 / 0.84 | 0.839 |  |  | 8/16 | +0.060 | -0.033 |  | +0.3 / +0.2 | 0.183 |
| MES | 60 | h8 | +0.016 | -0.311 .. +0.343 | +0.0013 | 0.92 / 0.92 / 0.89 | 0.895 |  |  | 8/16 | +0.138 | -0.105 |  | +0.3 / +0.1 |  |
| MES | 60 | h16 | -0.059 | -0.652 .. +0.535 | -0.0037 | 0.85 / 0.85 / 0.79 | 0.792 |  |  | 10/16 | +0.161 | -0.278 |  | -0.7 / -0.2 |  |
| MES | 60 | eod | -0.077 | -0.793 .. +0.639 | -0.0046 | 0.83 / 0.84 / 0.76 | 0.755 |  |  | 8/16 | +0.230 | -0.384 |  | -0.9 / -0.2 |  |
| MNQ | 5 | h1 | +0.006 | -0.003 .. +0.014 | +0.0011 | 0.18 / 0.18 / 0.27 | 0.267 |  |  | 10/16 | +0.003 | +0.008 |  | +1.2 / +1.3 |  |
| MNQ | 5 | h2 | +0.013 | -0.003 .. +0.029 | +0.0016 | 0.12 / 0.12 / 0.24 | 0.22 |  |  | 9/16 | +0.006 | +0.019 |  | +1.9 / +1.5 |  |
| MNQ | 5 | h4 * | +0.028 | -0.005 .. +0.061 | +0.0023 | 0.094 / 0.095 / 0.23 | 0.192 | 1 | 1 | 10/16 | +0.013 | +0.043 | False | +3.0 / +1.7 | 0.055 |
| MNQ | 5 | h8 | +0.057 | -0.010 .. +0.123 | +0.0032 | 0.096 / 0.098 / 0.24 | 0.198 |  |  | 11/16 | +0.024 | +0.089 |  | +4.2 / +1.7 |  |
| MNQ | 5 | h16 | +0.118 | -0.025 .. +0.262 | +0.0047 | 0.11 / 0.11 / 0.22 | 0.203 |  |  | 11/16 | +0.063 | +0.174 |  | +5.9 / +1.6 |  |
| MNQ | 5 | eod | +1.271 | -2.462 .. +5.005 | +0.0106 | 0.5 / 0.51 / 0.4 | 0.404 |  |  | 11/16 | +1.742 | +0.805 |  | +9.0 / +0.7 |  |
| MNQ | 15 | h1 | +0.004 | -0.011 .. +0.019 | +0.0007 | 0.61 / 0.6 / 0.71 | 0.668 |  |  | 8/16 | +0.002 | +0.006 |  | +0.5 / +0.5 |  |
| MNQ | 15 | h2 | +0.011 | -0.019 .. +0.041 | +0.0011 | 0.48 / 0.48 / 0.64 | 0.576 |  |  | 8/16 | +0.004 | +0.018 |  | +0.9 / +0.7 |  |
| MNQ | 15 | h4 | +0.024 | -0.038 .. +0.086 | +0.0015 | 0.45 / 0.45 / 0.63 | 0.55 |  |  | 8/16 | +0.010 | +0.038 |  | +1.4 / +0.8 | 0.102 |
| MNQ | 15 | h8 | +0.048 | -0.082 .. +0.178 | +0.0023 | 0.47 / 0.47 / 0.6 | 0.554 |  |  | 9/16 | +0.033 | +0.063 |  | +1.8 / +0.7 |  |
| MNQ | 15 | h16 * | +0.137 | -0.143 .. +0.416 | +0.0054 | 0.34 / 0.33 / 0.43 | 0.397 | 1 | 1 | 11/16 | +0.122 | +0.151 | False | +3.6 / +1.0 |  |
| MNQ | 15 | eod | +0.501 | -1.429 .. +2.431 | +0.0069 | 0.61 / 0.61 / 0.56 | 0.514 |  |  | 11/16 | +0.684 | +0.319 |  | +4.0 / +0.5 |  |
| MNQ | 60 | h1 * | +0.017 | -0.024 .. +0.057 | +0.0035 | 0.42 / 0.42 / 0.35 | 0.35 | 1 | 1 | 11/16 | +0.011 | +0.022 | False | +0.8 / +0.8 |  |
| MNQ | 60 | h2 | +0.026 | -0.057 .. +0.109 | +0.0038 | 0.54 / 0.54 / 0.47 | 0.474 |  |  | 11/16 | +0.020 | +0.032 |  | +0.8 / +0.6 |  |
| MNQ | 60 | h4 | +0.046 | -0.124 .. +0.215 | +0.0048 | 0.6 / 0.6 / 0.52 | 0.521 |  |  | 11/16 | +0.050 | +0.041 |  | +1.0 / +0.5 | 0.202 |
| MNQ | 60 | h8 | +0.076 | -0.263 .. +0.415 | +0.0058 | 0.66 / 0.66 / 0.58 | 0.584 |  |  | 9/16 | +0.123 | +0.030 |  | +1.2 / +0.4 |  |
| MNQ | 60 | h16 | +0.062 | -0.556 .. +0.681 | +0.0036 | 0.84 / 0.84 / 0.8 | 0.803 |  |  | 10/16 | +0.136 | -0.011 |  | +0.8 / +0.2 |  |
| MNQ | 60 | eod | +0.083 | -0.665 .. +0.832 | +0.0046 | 0.83 / 0.83 / 0.76 | 0.766 |  |  | 9/16 | +0.249 | -0.082 |  | +1.0 / +0.2 |  |
| MYM | 5 | h1 | +0.001 | -0.009 .. +0.012 | +0.0002 | 0.82 / 0.81 / 0.87 | 0.866 |  |  | 5/8 | n/a | +0.001 |  | +0.2 / +0.2 |  |
| MYM | 5 | h2 | +0.006 | -0.016 .. +0.028 | +0.0007 | 0.59 / 0.58 / 0.73 | 0.687 |  |  | 4/8 | n/a | +0.006 |  | +0.6 / +0.5 |  |
| MYM | 5 | h4 | +0.017 | -0.030 .. +0.063 | +0.0012 | 0.48 / 0.47 / 0.67 | 0.601 |  |  | 4/8 | n/a | +0.017 |  | +1.2 / +0.7 | 0.075 |
| MYM | 5 | h8 | +0.037 | -0.061 .. +0.134 | +0.0018 | 0.46 / 0.45 / 0.64 | 0.58 |  |  | 5/8 | n/a | +0.037 |  | +1.8 / +0.7 |  |
| MYM | 5 | h16 | +0.071 | -0.137 .. +0.279 | +0.0027 | 0.5 / 0.49 / 0.62 | 0.573 |  |  | 5/8 | n/a | +0.071 |  | +2.4 / +0.7 |  |
| MYM | 5 | eod * | -3.409 | -9.603 .. +2.785 | -0.0299 | 0.28 / 0.27 / 0.088 | 0.0917 | 1 | 1 | 4/8 | n/a | -3.409 | False | -14.8 / -1.1 |  |
| MYM | 15 | h1 | -0.005 | -0.025 .. +0.016 | -0.0009 | 0.65 / 0.64 / 0.74 | 0.721 |  |  | 4/8 | n/a | -0.005 |  | -0.4 / -0.4 |  |
| MYM | 15 | h2 | -0.001 | -0.044 .. +0.042 | -0.0001 | 0.95 / 0.95 / 0.97 | 0.966 |  |  | 3/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 15 | h4 | -0.000 | -0.090 .. +0.089 | -0.0000 | 1 / 1 / 1 | 1 |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 | 0.138 |
| MYM | 15 | h8 | +0.000 | -0.187 .. +0.188 | +0.0000 | 1 / 1 / 0.99 | 0.988 |  |  | 4/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 15 | h16 | +0.020 | -0.384 .. +0.423 | +0.0007 | 0.92 / 0.92 / 0.94 | 0.929 |  |  | 4/8 | n/a | +0.020 |  | +0.4 / +0.1 |  |
| MYM | 15 | eod * | -1.802 | -4.830 .. +1.225 | -0.0256 | 0.24 / 0.24 / 0.12 | 0.1 | 1 | 1 | 5/8 | n/a | -1.802 | False | -9.2 / -1.2 |  |
| MYM | 60 | h1 | -0.024 | -0.085 .. +0.036 | -0.0051 | 0.43 / 0.42 / 0.33 | 0.33 |  |  | 5/8 | n/a | -0.024 |  | -0.8 / -0.8 |  |
| MYM | 60 | h2 | -0.063 | -0.185 .. +0.060 | -0.0091 | 0.32 / 0.31 / 0.22 | 0.217 |  |  | 5/8 | n/a | -0.063 |  | -1.4 / -1.0 |  |
| MYM | 60 | h4 | -0.145 | -0.391 .. +0.101 | -0.0151 | 0.25 / 0.24 / 0.14 | 0.149 |  |  | 5/8 | n/a | -0.145 |  | -2.2 / -1.2 | 0.286 |
| MYM | 60 | h8 | -0.320 | -0.808 .. +0.168 | -0.0241 | 0.2 / 0.2 / 0.093 | 0.0943 |  |  | 5/8 | n/a | -0.320 |  | -3.6 / -1.3 |  |
| MYM | 60 | h16 | -0.673 | -1.545 .. +0.200 | -0.0387 | 0.13 / 0.13 / 0.05 | 0.0511 |  |  | 6/8 | n/a | -0.673 |  | -5.8 / -1.5 |  |
| MYM | 60 | eod * | -0.878 | -1.932 .. +0.176 | -0.0482 | 0.1 / 0.1 / 0.021 | 0.0258 | 1 | 1 | 6/8 | n/a | -0.878 | False | -7.1 / -1.6 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.007 | +0.002 .. +0.013 | +1.5% | +0.023 | 0.033 |  | 12/16 |
| MES | 5 | h2 | +0.012 | +0.003 .. +0.022 | +1.8% | +0.038 | 0.055 |  | 11/16 |
| MES | 5 | h4 | +0.019 | +0.002 .. +0.037 | +1.9% | +0.066 | 0.097 |  | 11/16 |
| MES | 5 | h8 | +0.034 | -0.002 .. +0.070 | +2.4% | +0.120 | 0.12 |  | 11/16 |
| MES | 5 | h16 | +0.068 | -0.004 .. +0.141 | +3.3% | +0.247 | 0.12 |  | 11/16 |
| MES | 5 | eod * | +4.046 | +1.789 .. +6.302 | +40.6% | +7.267 | 0.00098 | 0.169 | 12/16 |
| MES | 15 | h1 * | +0.024 | +0.014 .. +0.034 | +4.7% | +0.052 | 2.5e-05 | 0.00555 | 15/16 |
| MES | 15 | h2 | +0.030 | +0.011 .. +0.048 | +4.1% | +0.079 | 0.0035 |  | 10/16 |
| MES | 15 | h4 | +0.040 | +0.003 .. +0.076 | +3.8% | +0.118 | 0.052 |  | 10/16 |
| MES | 15 | h8 | +0.059 | -0.015 .. +0.133 | +3.8% | +0.208 | 0.13 |  | 8/16 |
| MES | 15 | h16 | +0.131 | -0.031 .. +0.293 | +5.7% | +0.407 | 0.12 |  | 9/16 |
| MES | 15 | eod | +2.100 | +0.894 .. +3.307 | +38.3% | +3.875 | 0.0011 |  | 11/16 |
| MES | 60 | h1 * | +0.055 | +0.028 .. +0.083 | +10.8% | +0.125 | 0.00011 | 0.0232 | 12/16 |
| MES | 60 | h2 | +0.089 | +0.038 .. +0.139 | +12.0% | +0.223 | 0.0006 |  | 12/16 |
| MES | 60 | h4 | +0.170 | +0.069 .. +0.272 | +16.1% | +0.406 | 0.00097 |  | 11/16 |
| MES | 60 | h8 | +0.343 | +0.142 .. +0.544 | +22.8% | +0.724 | 0.00081 |  | 10/16 |
| MES | 60 | h16 | +0.626 | +0.265 .. +0.986 | +30.4% | +1.249 | 0.00067 |  | 11/16 |
| MES | 60 | eod | +0.792 | +0.349 .. +1.235 | +36.6% | +1.573 | 0.00046 |  | 11/16 |
| MNQ | 5 | h1 | +0.007 | +0.001 .. +0.013 | +1.3% | +0.021 | 0.11 |  | 11/16 |
| MNQ | 5 | h2 | +0.009 | -0.002 .. +0.020 | +1.2% | +0.035 | 0.18 |  | 10/16 |
| MNQ | 5 | h4 | +0.015 | -0.006 .. +0.036 | +1.3% | +0.058 | 0.22 |  | 11/16 |
| MNQ | 5 | h8 | +0.009 | -0.033 .. +0.051 | +0.6% | +0.097 | 0.78 |  | 11/16 |
| MNQ | 5 | h16 | -0.007 | -0.091 .. +0.077 | -0.3% | +0.169 | 0.9 |  | 7/16 |
| MNQ | 5 | eod * | +3.208 | +0.924 .. +5.492 | +25.5% | +6.419 | 0.0085 | 1 | 9/16 |
| MNQ | 15 | h1 | +0.013 | +0.003 .. +0.023 | +2.4% | +0.037 | 0.29 |  | 11/16 |
| MNQ | 15 | h2 | +0.007 | -0.012 .. +0.026 | +0.9% | +0.048 | 0.75 |  | 10/16 |
| MNQ | 15 | h4 | -0.020 | -0.061 .. +0.022 | -1.7% | +0.049 | 0.69 |  | 8/16 |
| MNQ | 15 | h8 | -0.048 | -0.127 .. +0.032 | -2.8% | +0.048 | 0.56 |  | 8/16 |
| MNQ | 15 | h16 | -0.036 | -0.189 .. +0.118 | -1.4% | +0.124 | 0.65 |  | 9/16 |
| MNQ | 15 | eod * | +1.502 | +0.337 .. +2.667 | +23.6% | +2.966 | 0.015 | 1 | 8/16 |
| MNQ | 60 | h1 | +0.035 | +0.008 .. +0.062 | +6.6% | +0.096 | 0.012 |  | 9/16 |
| MNQ | 60 | h2 | +0.057 | +0.004 .. +0.110 | +7.5% | +0.170 | 0.034 |  | 9/16 |
| MNQ | 60 | h4 | +0.110 | +0.004 .. +0.216 | +9.9% | +0.310 | 0.044 |  | 9/16 |
| MNQ | 60 | h8 | +0.247 | +0.039 .. +0.455 | +15.6% | +0.552 | 0.023 |  | 7/16 |
| MNQ | 60 | h16 | +0.461 | +0.085 .. +0.836 | +21.0% | +0.936 | 0.02 |  | 8/16 |
| MNQ | 60 | eod * | +0.669 | +0.202 .. +1.135 | +29.1% | +1.244 | 0.0064 | 0.906 | 9/16 |
| MYM | 5 | h1 | +0.012 | +0.004 .. +0.021 | +2.3% | +0.028 | 0.051 |  | 7/8 |
| MYM | 5 | h2 * | +0.022 | +0.006 .. +0.038 | +2.9% | +0.051 | 0.0094 | 1 | 7/8 |
| MYM | 5 | h4 | +0.038 | +0.007 .. +0.070 | +3.5% | +0.090 | 0.026 |  | 6/8 |
| MYM | 5 | h8 | +0.061 | -0.004 .. +0.126 | +3.8% | +0.154 | 0.079 |  | 6/8 |
| MYM | 5 | h16 | +0.102 | -0.022 .. +0.225 | +4.4% | +0.305 | 0.11 |  | 6/8 |
| MYM | 5 | eod | +4.966 | +0.714 .. +9.218 | +42.4% | +9.248 | 0.023 |  | 6/8 |
| MYM | 15 | h1 | +0.021 | +0.005 .. +0.037 | +3.9% | +0.045 | 0.17 |  | 6/8 |
| MYM | 15 | h2 | +0.024 | -0.008 .. +0.055 | +3.1% | +0.060 | 0.36 |  | 6/8 |
| MYM | 15 | h4 | +0.024 | -0.038 .. +0.085 | +2.1% | +0.071 | 0.6 |  | 4/8 |
| MYM | 15 | h8 | +0.005 | -0.110 .. +0.120 | +0.3% | +0.098 | 0.98 |  | 5/8 |
| MYM | 15 | h16 | +0.005 | -0.241 .. +0.250 | +0.2% | +0.217 | 0.99 |  | 4/8 |
| MYM | 15 | eod * | +2.188 | +0.137 .. +4.238 | +36.3% | +3.992 | 0.039 | 1 | 5/8 |
| MYM | 60 | h1 | +0.046 | +0.003 .. +0.088 | +8.7% | +0.114 | 0.035 |  | 5/8 |
| MYM | 60 | h2 | +0.060 | -0.010 .. +0.129 | +7.9% | +0.196 | 0.1 |  | 5/8 |
| MYM | 60 | h4 | +0.134 | -0.005 .. +0.274 | +12.4% | +0.341 | 0.067 |  | 6/8 |
| MYM | 60 | h8 | +0.250 | -0.037 .. +0.537 | +16.2% | +0.599 | 0.091 |  | 5/8 |
| MYM | 60 | h16 | +0.543 | +0.020 .. +1.067 | +25.6% | +1.032 | 0.045 |  | 6/8 |
| MYM | 60 | eod * | +0.714 | +0.059 .. +1.369 | +32.1% | +1.332 | 0.035 | 1 | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.40 pts | -1.37 .. +0.57 | 0.45 |
| MES | 15 | -0.01 pts | -1.67 .. +1.65 | 0.99 |
| MES | 60 | -0.66 pts | -4.90 .. +3.57 | 0.76 |
| MNQ | 5 | +0.31 pts | -0.61 .. +1.23 | 0.54 |
| MNQ | 15 | +0.66 pts | -1.01 .. +2.32 | 0.48 |
| MNQ | 60 | +0.92 pts | -3.33 .. +5.16 | 0.87 |
| MYM | 5 | +0.22 pts | -1.00 .. +1.43 | 0.73 |
| MYM | 15 | +0.13 pts | -1.84 .. +2.11 | 0.9 |
| MYM | 60 | -1.85 pts | -7.73 .. +4.02 | 0.55 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 31983 | +0.006 | 0.326 | +0.04 | -3.46 | -3.47 | -3.45 | -3.44 |
| MES | 5 | h2 | event | long | 31983 | +0.013 | 0.326 | +0.10 | -3.40 | -3.43 | -3.38 | -3.40 |
| MES | 5 | h4 | event | long | 31983 | +0.029 | 0.326 | +0.20 | -3.30 | -3.35 | -3.25 | -3.30 |
| MES | 5 | h8 | event | long | 31983 | +0.063 | 0.326 | +0.41 | -3.09 | -3.19 | -2.98 | -3.12 |
| MES | 5 | h16 | event | long | 31983 | +0.131 | 0.326 | +0.86 | -2.64 | -2.85 | -2.41 | -2.75 |
| MES | 5 | eod | event | short | 31983 | +0.194 | 0.326 | -0.81 | -4.31 | -10.13 | +1.79 | -6.30 |
| MES | 15 | h1 | event | long | 10457 | +0.009 | 0.208 | +0.15 | -3.35 | -3.40 | -3.30 | -3.40 |
| MES | 15 | h2 | event | long | 10457 | +0.021 | 0.208 | +0.31 | -3.19 | -3.28 | -3.09 | -3.31 |
| MES | 15 | h4 | event | long | 10457 | +0.047 | 0.208 | +0.67 | -2.83 | -3.03 | -2.62 | -3.09 |
| MES | 15 | h8 | event | long | 10457 | +0.090 | 0.208 | +1.31 | -2.19 | -2.57 | -1.79 | -2.63 |
| MES | 15 | h16 | event | long | 10457 | +0.157 | 0.208 | +2.46 | -1.04 | -1.55 | -0.49 | -1.69 |
| MES | 15 | eod | event | short | 10457 | +0.058 | 0.208 | -1.26 | -4.76 | -9.93 | +0.76 | -5.01 |
| MES | 60 | h1 | event | long | 2433 | +0.014 | 0.105 | +0.78 | -2.72 | -3.04 | -2.34 | -2.81 |
| MES | 60 | h2 | event | long | 2433 | +0.024 | 0.105 | +1.61 | -1.89 | -2.66 | -0.97 | -2.10 |
| MES | 60 | h4 | event | long | 2433 | +0.047 | 0.105 | +3.16 | -0.34 | -1.75 | +1.33 | -0.89 |
| MES | 60 | h8 | event | long | 2433 | +0.082 | 0.105 | +5.35 | +1.85 | +0.14 | +3.87 | +0.62 |
| MES | 60 | h16 | event | short | 2433 | -0.041 | 0.105 | -5.60 | -9.10 | -8.18 | -10.18 | -7.38 |
| MES | 60 | eod | event | short | 2433 | -0.024 | 0.105 | -4.70 | -8.20 | -8.97 | -7.28 | -6.57 |
| MNQ | 5 | h1 | event | long | 31796 | +0.011 | 0.130 | +0.18 | -1.82 | -1.97 | -1.66 | -1.86 |
| MNQ | 5 | h2 | event | long | 31796 | +0.022 | 0.130 | +0.36 | -1.64 | -1.93 | -1.33 | -1.69 |
| MNQ | 5 | h4 | event | long | 31796 | +0.047 | 0.130 | +0.73 | -1.27 | -1.86 | -0.66 | -1.38 |
| MNQ | 5 | h8 | event | long | 31796 | +0.096 | 0.130 | +1.44 | -0.56 | -1.71 | +0.66 | -0.83 |
| MNQ | 5 | h16 | event | long | 31796 | +0.199 | 0.130 | +2.86 | +0.86 | -1.40 | +3.24 | +0.16 |
| MNQ | 5 | eod | event | long | 31796 | +1.851 | 0.130 | +20.66 | +18.66 | +3.57 | +34.55 | +22.13 |
| MNQ | 15 | h1 | event | long | 10374 | +0.016 | 0.082 | +0.52 | -1.48 | -1.90 | -1.04 | -1.68 |
| MNQ | 15 | h2 | event | long | 10374 | +0.033 | 0.082 | +1.06 | -0.94 | -1.79 | -0.02 | -1.31 |
| MNQ | 15 | h4 | event | long | 10374 | +0.070 | 0.082 | +2.15 | +0.15 | -1.56 | +2.00 | -0.64 |
| MNQ | 15 | h8 | event | long | 10374 | +0.135 | 0.082 | +4.17 | +2.17 | -1.14 | +5.76 | +0.76 |
| MNQ | 15 | h16 | event | long | 10374 | +0.256 | 0.082 | +7.56 | +5.56 | -0.29 | +11.91 | +4.20 |
| MNQ | 15 | eod | event | long | 10374 | +0.821 | 0.082 | +18.95 | +16.95 | +3.41 | +31.66 | +16.89 |
| MNQ | 60 | h1 | event | long | 2370 | +0.026 | 0.042 | +1.90 | -0.10 | -1.57 | +1.75 | -0.26 |
| MNQ | 60 | h2 | event | long | 2370 | +0.042 | 0.042 | +3.50 | +1.50 | -1.23 | +4.93 | +1.24 |
| MNQ | 60 | h4 | event | long | 2370 | +0.078 | 0.042 | +6.18 | +4.18 | -0.47 | +10.03 | +3.63 |
| MNQ | 60 | h8 | event | long | 2370 | +0.139 | 0.042 | +10.26 | +8.26 | +0.98 | +17.43 | +7.23 |
| MNQ | 60 | h16 | event | long | 2370 | +0.159 | 0.042 | +13.70 | +11.70 | +1.31 | +24.77 | +10.64 |
| MNQ | 60 | eod | event | long | 2370 | +0.188 | 0.042 | +13.59 | +11.59 | +2.70 | +22.79 | +10.52 |
| MYM | 5 | h1 | event | long | 15587 | +0.004 | 0.175 | -0.01 | -2.01 | +nan | -2.01 | -2.05 |
| MYM | 5 | h2 | event | long | 15587 | +0.009 | 0.175 | -0.01 | -2.01 | +nan | -2.01 | -2.08 |
| MYM | 5 | h4 | event | long | 15587 | +0.021 | 0.175 | -0.02 | -2.02 | +nan | -2.02 | -2.15 |
| MYM | 5 | h8 | event | long | 15587 | +0.045 | 0.175 | -0.04 | -2.04 | +nan | -2.04 | -2.30 |
| MYM | 5 | h16 | event | long | 15587 | +0.091 | 0.175 | -0.05 | -2.05 | +nan | -2.05 | -2.54 |
| MYM | 5 | eod | event | short | 15587 | +3.484 | 0.175 | +17.18 | +15.18 | +nan | +15.18 | +11.77 |
| MYM | 15 | h1 | event | short | 5031 | -0.003 | 0.108 | +0.05 | -1.95 | +nan | -1.95 | -1.82 |
| MYM | 15 | h2 | event | short | 5031 | -0.007 | 0.108 | +0.07 | -1.93 | +nan | -1.93 | -1.73 |
| MYM | 15 | h4 | event | short | 5031 | -0.016 | 0.108 | +0.10 | -1.90 | +nan | -1.90 | -1.50 |
| MYM | 15 | h8 | event | long | 5031 | +0.017 | 0.108 | -0.21 | -2.21 | +nan | -2.21 | -2.67 |
| MYM | 15 | h16 | event | long | 5031 | -0.022 | 0.108 | -0.85 | -2.85 | +nan | -2.85 | -2.56 |
| MYM | 15 | eod | event | short | 5031 | +1.850 | 0.108 | +17.98 | +15.98 | +nan | +15.98 | +13.52 |
| MYM | 60 | h1 | event | short | 1092 | +0.020 | 0.052 | +0.07 | -1.93 | +nan | -1.93 | -1.86 |
| MYM | 60 | h2 | event | short | 1092 | +0.055 | 0.052 | +0.22 | -1.78 | +nan | -1.78 | -1.65 |
| MYM | 60 | h4 | event | short | 1092 | +0.134 | 0.052 | +0.97 | -1.03 | +nan | -1.03 | -0.89 |
| MYM | 60 | h8 | event | short | 1092 | +0.302 | 0.052 | +3.62 | +1.62 | +nan | +1.62 | +1.86 |
| MYM | 60 | h16 | event | short | 1092 | +0.639 | 0.052 | +12.31 | +10.31 | +nan | +10.31 | +10.91 |
| MYM | 60 | eod | event | short | 1092 | +0.865 | 0.052 | +19.62 | +17.62 | +nan | +17.62 | +17.34 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.010 | +0.010 | +0.001 | -0.001 | -0.001 | +0.000 | +0.004 | +0.009 | +0.020 | +0.045 | +0.107 |
| MES | 15 | +0.075 | +0.032 | +0.016 | +0.006 | +0.001 | +0.000 | +0.006 | +0.014 | +0.035 | +0.085 | +0.147 |
| MES | 60 | +0.170 | +0.102 | +0.051 | +0.006 | +0.009 | +0.000 | +0.005 | +0.007 | +0.043 | +0.049 | +0.077 |
| MNQ | 5 | +0.006 | +0.004 | -0.003 | -0.004 | -0.003 | +0.000 | +0.008 | +0.016 | +0.033 | +0.067 | +0.153 |
| MNQ | 15 | +0.075 | +0.028 | +0.011 | +0.003 | -0.001 | +0.000 | +0.011 | +0.024 | +0.051 | +0.109 | +0.191 |
| MNQ | 60 | +0.129 | +0.068 | +0.030 | -0.012 | -0.002 | +0.000 | +0.015 | +0.018 | +0.052 | +0.049 | +0.084 |
| MYM | 5 | +0.014 | +0.011 | -0.001 | -0.003 | -0.002 | +0.000 | +0.007 | +0.013 | +0.029 | +0.055 | +0.116 |
| MYM | 15 | +0.012 | -0.001 | +0.008 | +0.004 | +0.000 | +0.000 | +0.008 | +0.014 | +0.028 | +0.075 | +0.199 |
| MYM | 60 | +0.111 | +0.052 | +0.032 | +0.016 | +0.024 | +0.000 | -0.023 | -0.065 | -0.045 | -0.013 | +0.011 |

## Calibration

- MES 5-min: 1036271 bars, 31983 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 10457 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 2433 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 31796 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 10374 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 2370 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 15587 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 5031 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1092 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
