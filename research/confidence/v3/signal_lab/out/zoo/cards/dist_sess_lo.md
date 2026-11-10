# Impact card: dist_sess_lo

(close - session low so far) in R20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.051 R20 over the next 16 bars (80 min), p=0.64; we would catch an effect of 0.023 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=1).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.37 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.227 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.029 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.043 R20 or more 80% of the time).
- MES 15-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.024 R20, CONFIRMED, q=3.29e-05, 10 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.06 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.127 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.014 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.078 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.27).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.25 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.030 R20 over the next 4 bars (20 min), p=0.15; we would catch an effect of 0.030 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.43).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.38 at recent bar sizes, 90% range up to $0.86); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.504 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.060 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.028 R20, possible, q=0.022, 9 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $11.36 at recent bar sizes, 90% range up to $1.59); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.054 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.082 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.48 at recent bar sizes, 90% range up to $3.84); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.075 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.057).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.99 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.170 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.028 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.084 R20 or more 80% of the time).
- MYM 15-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.040 R20, possible, q=0.0361, 4 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.30 at recent bar sizes, 90% range up to $2.62); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.021 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.116 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.45 at recent bar sizes, 90% range up to $2.84); about 2.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.007 .. +0.001 | -0.0033 | 0.19 / 0.19 / 0.16 | 0.173 |  |  | 10/16 | -0.005 | -0.001 |  | -1.2 / -1.3 |  |
| MES | 5 | h2 | +0.001 | -0.007 .. +0.009 | -0.0006 | 0.78 / 0.78 / 0.81 | 0.816 |  |  | 6/16 | -0.006 | +0.008 |  | +0.3 / +0.3 |  |
| MES | 5 | h4 | +0.011 | -0.005 .. +0.027 | +0.0024 | 0.17 / 0.18 / 0.18 | 0.18 |  |  | 8/16 | -0.001 | +0.023 |  | +2.2 / +1.4 | 0.023 |
| MES | 5 | h8 | +0.022 | -0.009 .. +0.052 | +0.0036 | 0.16 / 0.18 / 0.18 | 0.18 |  |  | 10/16 | -0.000 | +0.043 |  | +2.9 / +1.4 |  |
| MES | 5 | h16 * | +0.051 | -0.008 .. +0.111 | +0.0066 | 0.092 / 0.11 / 0.11 | 0.11 | 1 | 1 | 9/16 | +0.009 | +0.093 | False | +4.9 / +1.7 |  |
| MES | 5 | eod | +0.010 | -0.883 .. +0.903 | +0.0045 | 0.98 / 0.98 / 1 | 1 |  |  | 5/16 | +0.242 | -0.221 |  | +0.2 / +0.0 |  |
| MES | 15 | h1 | -0.003 | -0.012 .. +0.005 | -0.0036 | 0.47 / 0.46 / 0.44 | 0.444 |  |  | 10/16 | -0.006 | -0.000 |  | -0.7 / -0.7 |  |
| MES | 15 | h2 | +0.005 | -0.008 .. +0.018 | +0.0020 | 0.47 / 0.49 / 0.52 | 0.527 |  |  | 7/16 | -0.006 | +0.015 |  | +0.7 / +0.7 |  |
| MES | 15 | h4 | +0.011 | -0.017 .. +0.039 | +0.0048 | 0.44 / 0.46 / 0.46 | 0.459 |  |  | 9/16 | -0.009 | +0.031 |  | +1.0 / +0.8 | 0.043 |
| MES | 15 | h8 * | +0.029 | -0.026 .. +0.085 | +0.0069 | 0.3 / 0.31 / 0.29 | 0.287 | 1 | 1 | 8/16 | -0.018 | +0.077 | False | +2.0 / +1.0 |  |
| MES | 15 | h16 | +0.047 | -0.074 .. +0.168 | +0.0110 | 0.45 / 0.45 / 0.39 | 0.395 |  |  | 6/16 | -0.024 | +0.118 |  | +2.3 / +0.8 |  |
| MES | 15 | eod | +0.145 | -0.483 .. +0.773 | +0.0185 | 0.65 / 0.64 / 0.47 | 0.473 |  |  | 6/16 | +0.039 | +0.250 |  | +2.7 / +0.5 |  |
| MES | 60 | h1 | +0.007 | -0.008 .. +0.021 | +0.0029 | 0.38 / 0.41 / 0.41 | 0.43 |  |  | 10/16 | -0.005 | +0.018 |  | +0.8 / +0.9 |  |
| MES | 60 | h2 * | +0.014 | -0.011 .. +0.040 | +0.0035 | 0.27 / 0.3 / 0.32 | 0.324 | 1 | 1 | 10/16 | -0.007 | +0.036 | False | +1.2 / +1.1 |  |
| MES | 60 | h4 | +0.019 | -0.026 .. +0.064 | +0.0037 | 0.4 / 0.42 / 0.45 | 0.441 |  |  | 11/16 | +0.007 | +0.031 |  | +1.1 / +0.8 | 0.078 |
| MES | 60 | h8 | +0.017 | -0.058 .. +0.092 | +0.0024 | 0.66 / 0.67 / 0.68 | 0.673 |  |  | 7/16 | +0.010 | +0.024 |  | +0.8 / +0.4 |  |
| MES | 60 | h16 | +0.009 | -0.107 .. +0.126 | -0.0012 | 0.88 / 0.88 / 0.87 | 0.872 |  |  | 8/16 | -0.006 | +0.025 |  | +0.3 / +0.2 |  |
| MES | 60 | eod | +0.012 | -0.116 .. +0.139 | -0.0004 | 0.86 / 0.86 / 0.85 | 0.845 |  |  | 8/16 | -0.009 | +0.033 |  | +0.4 / +0.2 |  |
| MNQ | 5 | h1 | +0.004 | -0.001 .. +0.010 | +0.0009 | 0.1 / 0.11 / 0.099 | 0.0969 |  |  | 10/16 | -0.001 | +0.010 |  | +1.4 / +1.6 |  |
| MNQ | 5 | h2 | +0.013 | +0.001 .. +0.026 | +0.0038 | 0.034 / 0.033 / 0.019 | 0.0203 |  |  | 10/16 | -0.002 | +0.029 |  | +2.4 / +2.1 |  |
| MNQ | 5 | h4 * | +0.030 | +0.004 .. +0.056 | +0.0056 | 0.025 / 0.023 / 0.0079 | 0.0086 | 1 | 0.996 | 11/16 | +0.002 | +0.057 | False | +3.4 / +2.2 | 0.030 |
| MNQ | 5 | h8 | +0.032 | -0.009 .. +0.074 | +0.0023 | 0.13 / 0.13 / 0.15 | 0.149 |  |  | 11/16 | -0.005 | +0.069 |  | +2.5 / +1.5 |  |
| MNQ | 5 | h16 | +0.027 | -0.057 .. +0.110 | -0.0021 | 0.53 / 0.54 / 0.53 | 0.535 |  |  | 10/16 | -0.022 | +0.075 |  | +1.5 / +0.6 |  |
| MNQ | 5 | eod | +0.439 | -0.795 .. +1.672 | +0.0181 | 0.49 / 0.48 / 0.33 | 0.324 |  |  | 6/16 | +0.320 | +0.557 |  | +5.8 / +0.7 |  |
| MNQ | 15 | h1 | -0.003 | -0.017 .. +0.012 | -0.0023 | 0.7 / 0.7 / 0.6 | 0.614 |  |  | 6/16 | -0.006 | +0.001 |  | -0.4 / -0.4 |  |
| MNQ | 15 | h2 | +0.005 | -0.015 .. +0.025 | +0.0012 | 0.63 / 0.63 / 0.64 | 0.65 |  |  | 10/16 | -0.007 | +0.017 |  | +0.4 / +0.5 |  |
| MNQ | 15 | h4 | +0.001 | -0.041 .. +0.043 | +0.0003 | 0.98 / 0.98 / 0.98 | 0.975 |  |  | 10/16 | -0.024 | +0.025 |  | +0.0 / +0.0 | 0.060 |
| MNQ | 15 | h8 | -0.008 | -0.082 .. +0.065 | -0.0005 | 0.83 / 0.83 / 0.84 | 0.838 |  |  | 7/16 | -0.044 | +0.028 |  | -0.3 / -0.2 |  |
| MNQ | 15 | h16 | +0.036 | -0.112 .. +0.183 | +0.0089 | 0.64 / 0.64 / 0.6 | 0.591 |  |  | 7/16 | -0.074 | +0.144 |  | +1.2 / +0.5 |  |
| MNQ | 15 | eod * | +0.504 | -0.359 .. +1.367 | +0.0317 | 0.25 / 0.24 / 0.055 | 0.056 | 1 | 1 | 7/16 | +0.233 | +0.773 | False | +5.6 / +1.1 |  |
| MNQ | 60 | h1 | +0.002 | -0.015 .. +0.019 | +0.0033 | 0.82 / 0.82 / 0.82 | 0.804 |  |  | 9/16 | -0.013 | +0.017 |  | +0.2 / +0.2 |  |
| MNQ | 60 | h2 | -0.001 | -0.031 .. +0.029 | +0.0034 | 0.95 / 0.95 / 0.95 | 0.951 |  |  | 8/16 | -0.028 | +0.026 |  | -0.1 / -0.1 |  |
| MNQ | 60 | h4 | -0.002 | -0.053 .. +0.050 | +0.0020 | 0.94 / 0.94 / 0.94 | 0.939 |  |  | 9/16 | -0.023 | +0.020 |  | -0.1 / -0.1 | 0.082 |
| MNQ | 60 | h8 | +0.012 | -0.073 .. +0.098 | +0.0050 | 0.78 / 0.77 / 0.76 | 0.772 |  |  | 7/16 | -0.005 | +0.030 |  | +0.5 / +0.3 |  |
| MNQ | 60 | h16 * | +0.054 | -0.076 .. +0.184 | +0.0091 | 0.41 / 0.41 / 0.35 | 0.34 | 1 | 1 | 8/16 | +0.020 | +0.088 | False | +1.7 / +0.8 |  |
| MNQ | 60 | eod | +0.058 | -0.082 .. +0.198 | +0.0090 | 0.42 / 0.42 / 0.34 | 0.332 |  |  | 9/16 | +0.014 | +0.102 |  | +1.8 / +0.8 |  |
| MYM | 5 | h1 | -0.000 | -0.008 .. +0.008 | +0.0001 | 0.96 / 0.96 / 0.95 | 0.956 |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 5 | h2 | +0.011 | -0.015 .. +0.038 | +0.0074 | 0.4 / 0.4 / 0.19 | 0.181 |  |  | 2/8 | n/a | +0.011 |  | +1.2 / +0.8 |  |
| MYM | 5 | h4 | +0.041 | -0.026 .. +0.108 | +0.0134 | 0.23 / 0.22 / 0.028 | 0.0242 |  |  | 3/8 | n/a | +0.041 |  | +2.6 / +1.2 | 0.048 |
| MYM | 5 | h8 * | +0.075 | -0.038 .. +0.188 | +0.0157 | 0.19 / 0.19 / 0.024 | 0.0211 | 1 | 1 | 3/8 | n/a | +0.075 | False | +3.4 / +1.3 |  |
| MYM | 5 | h16 | +0.119 | -0.061 .. +0.299 | +0.0193 | 0.19 / 0.19 / 0.034 | 0.029 |  |  | 4/8 | n/a | +0.119 |  | +4.5 / +1.3 |  |
| MYM | 5 | eod | -0.056 | -1.648 .. +1.535 | +0.0118 | 0.94 / 0.94 / 0.93 | 0.937 |  |  | 6/8 | n/a | -0.056 |  | -0.6 / -0.1 |  |
| MYM | 15 | h1 | +0.001 | -0.013 .. +0.015 | -0.0003 | 0.87 / 0.88 / 0.87 | 0.872 |  |  | 4/8 | n/a | +0.001 |  | +0.1 / +0.2 |  |
| MYM | 15 | h2 * | +0.028 | -0.012 .. +0.069 | +0.0103 | 0.17 / 0.18 / 0.073 | 0.0732 | 1 | 1 | 5/8 | n/a | +0.028 | False | +1.6 / +1.4 |  |
| MYM | 15 | h4 | +0.056 | -0.029 .. +0.140 | +0.0142 | 0.2 / 0.21 / 0.078 | 0.079 |  |  | 4/8 | n/a | +0.056 |  | +1.8 / +1.3 | 0.084 |
| MYM | 15 | h8 | +0.106 | -0.058 .. +0.270 | +0.0217 | 0.21 / 0.21 / 0.05 | 0.049 |  |  | 4/8 | n/a | +0.106 |  | +2.7 / +1.3 |  |
| MYM | 15 | h16 | +0.252 | -0.149 .. +0.653 | +0.0382 | 0.22 / 0.23 / 0.017 | 0.0153 |  |  | 4/8 | n/a | +0.252 |  | +4.8 / +1.2 |  |
| MYM | 15 | eod | +0.468 | -0.737 .. +1.673 | +0.0356 | 0.45 / 0.45 / 0.18 | 0.182 |  |  | 3/8 | n/a | +0.468 |  | +3.8 / +0.8 |  |
| MYM | 60 | h1 | +0.011 | -0.011 .. +0.034 | +0.0073 | 0.32 / 0.35 / 0.36 | 0.363 |  |  | 5/8 | n/a | +0.011 |  | +0.9 / +1.0 |  |
| MYM | 60 | h2 * | +0.021 | -0.020 .. +0.062 | +0.0101 | 0.32 / 0.33 / 0.32 | 0.323 | 1 | 1 | 5/8 | n/a | +0.021 | False | +1.1 / +1.0 |  |
| MYM | 60 | h4 | +0.008 | -0.066 .. +0.081 | +0.0093 | 0.84 / 0.84 / 0.83 | 0.84 |  |  | 6/8 | n/a | +0.008 |  | +0.3 / +0.2 | 0.116 |
| MYM | 60 | h8 | -0.002 | -0.123 .. +0.119 | +0.0029 | 0.97 / 0.97 / 0.97 | 0.965 |  |  | 3/8 | n/a | -0.002 |  | -0.1 / -0.0 |  |
| MYM | 60 | h16 | -0.059 | -0.231 .. +0.113 | -0.0055 | 0.5 / 0.5 / 0.46 | 0.468 |  |  | 4/8 | n/a | -0.059 |  | -1.4 / -0.7 |  |
| MYM | 60 | eod | -0.053 | -0.235 .. +0.128 | -0.0049 | 0.57 / 0.57 / 0.53 | 0.538 |  |  | 4/8 | n/a | -0.053 |  | -1.2 / -0.6 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.003 | -0.008 .. +0.002 | -0.7% | -0.006 | 0.18 | 1 | 9/16 |
| MES | 5 | h2 | -0.002 | -0.010 .. +0.006 | -0.3% | -0.003 | 0.58 |  | 8/16 |
| MES | 5 | h4 | +0.003 | -0.013 .. +0.019 | +0.3% | +0.005 | 0.71 |  | 10/16 |
| MES | 5 | h8 | +0.012 | -0.019 .. +0.042 | +0.8% | +0.020 | 0.95 |  | 11/16 |
| MES | 5 | h16 | +0.015 | -0.038 .. +0.067 | +0.7% | +0.031 | 0.94 |  | 9/16 |
| MES | 5 | eod | +0.463 | -0.171 .. +1.096 | +4.6% | +0.315 | 0.6 |  | 12/16 |
| MES | 15 | h1 * | -0.024 | -0.034 .. -0.015 | -4.8% | -0.054 | 1.2e-07 | 3.29e-05 | 10/16 |
| MES | 15 | h2 | -0.036 | -0.056 .. -0.016 | -4.9% | -0.074 | 0.00051 |  | 11/16 |
| MES | 15 | h4 | -0.049 | -0.090 .. -0.008 | -4.6% | -0.103 | 0.02 |  | 9/16 |
| MES | 15 | h8 | -0.054 | -0.121 .. +0.013 | -3.5% | -0.147 | 0.12 |  | 8/16 |
| MES | 15 | h16 | -0.053 | -0.164 .. +0.059 | -2.3% | -0.234 | 0.36 |  | 8/16 |
| MES | 15 | eod | -0.086 | -0.599 .. +0.427 | -1.6% | -0.401 | 0.74 |  | 4/16 |
| MES | 60 | h1 * | -0.018 | -0.036 .. -0.000 | -3.5% | -0.043 | 0.046 | 1 | 12/16 |
| MES | 60 | h2 | -0.014 | -0.041 .. +0.012 | -1.9% | -0.051 | 0.29 |  | 10/16 |
| MES | 60 | h4 | -0.015 | -0.056 .. +0.025 | -1.5% | -0.060 | 0.45 |  | 9/16 |
| MES | 60 | h8 | -0.024 | -0.084 .. +0.036 | -1.6% | -0.082 | 0.43 |  | 10/16 |
| MES | 60 | h16 | -0.020 | -0.099 .. +0.058 | -1.0% | -0.075 | 0.61 |  | 8/16 |
| MES | 60 | eod | -0.018 | -0.103 .. +0.067 | -0.8% | -0.077 | 0.68 |  | 9/16 |
| MNQ | 5 | h1 * | -0.007 | -0.014 .. +0.001 | -1.3% | -0.011 | 0.072 | 1 | 8/16 |
| MNQ | 5 | h2 | -0.011 | -0.028 .. +0.007 | -1.4% | -0.014 | 0.23 |  | 8/16 |
| MNQ | 5 | h4 | -0.015 | -0.051 .. +0.020 | -1.4% | -0.020 | 0.39 |  | 7/16 |
| MNQ | 5 | h8 | -0.016 | -0.080 .. +0.047 | -1.0% | -0.030 | 0.61 |  | 6/16 |
| MNQ | 5 | h16 | -0.009 | -0.112 .. +0.093 | -0.4% | -0.054 | 0.86 |  | 6/16 |
| MNQ | 5 | eod | +0.599 | -0.341 .. +1.540 | +4.8% | +0.524 | 0.31 |  | 14/16 |
| MNQ | 15 | h1 * | -0.028 | -0.042 .. -0.014 | -5.2% | -0.057 | 0.00011 | 0.022 | 9/16 |
| MNQ | 15 | h2 | -0.049 | -0.086 .. -0.012 | -6.3% | -0.095 | 0.0088 |  | 8/16 |
| MNQ | 15 | h4 | -0.075 | -0.167 .. +0.017 | -6.6% | -0.156 | 0.11 |  | 8/16 |
| MNQ | 15 | h8 | -0.102 | -0.263 .. +0.058 | -6.1% | -0.274 | 0.21 |  | 8/16 |
| MNQ | 15 | h16 | -0.076 | -0.263 .. +0.112 | -3.0% | -0.447 | 0.43 |  | 6/16 |
| MNQ | 15 | eod | -0.296 | -1.148 .. +0.556 | -4.7% | -0.690 | 0.5 |  | 6/16 |
| MNQ | 60 | h1 * | -0.010 | -0.027 .. +0.007 | -1.9% | -0.028 | 0.24 | 1 | 8/16 |
| MNQ | 60 | h2 | -0.006 | -0.031 .. +0.019 | -0.8% | -0.029 | 0.62 |  | 9/16 |
| MNQ | 60 | h4 | +0.001 | -0.036 .. +0.037 | +0.1% | -0.032 | 0.97 |  | 8/16 |
| MNQ | 60 | h8 | -0.007 | -0.064 .. +0.050 | -0.4% | -0.042 | 0.81 |  | 8/16 |
| MNQ | 60 | h16 | +0.014 | -0.068 .. +0.096 | +0.6% | -0.015 | 0.86 |  | 10/16 |
| MNQ | 60 | eod | +0.018 | -0.068 .. +0.105 | +0.8% | -0.011 | 0.74 |  | 9/16 |
| MYM | 5 | h1 * | -0.015 | -0.026 .. -0.004 | -2.8% | -0.022 | 0.0095 | 1 | 5/8 |
| MYM | 5 | h2 | -0.026 | -0.055 .. +0.003 | -3.4% | -0.039 | 0.082 |  | 4/8 |
| MYM | 5 | h4 | -0.052 | -0.121 .. +0.018 | -4.7% | -0.072 | 0.15 |  | 4/8 |
| MYM | 5 | h8 | -0.080 | -0.201 .. +0.041 | -5.0% | -0.123 | 0.19 |  | 4/8 |
| MYM | 5 | h16 | -0.087 | -0.274 .. +0.099 | -3.7% | -0.210 | 0.36 |  | 4/8 |
| MYM | 5 | eod | +0.203 | -0.946 .. +1.353 | +1.7% | +0.278 | 0.75 |  | 6/8 |
| MYM | 15 | h1 * | -0.040 | -0.060 .. -0.019 | -7.5% | -0.073 | 0.00019 | 0.0361 | 4/8 |
| MYM | 15 | h2 | -0.075 | -0.130 .. -0.020 | -9.8% | -0.134 | 0.0081 |  | 5/8 |
| MYM | 15 | h4 | -0.128 | -0.253 .. -0.004 | -11.5% | -0.243 | 0.044 |  | 4/8 |
| MYM | 15 | h8 | -0.178 | -0.383 .. +0.026 | -10.9% | -0.445 | 0.088 |  | 4/8 |
| MYM | 15 | h16 | -0.296 | -0.676 .. +0.083 | -12.0% | -0.731 | 0.13 |  | 5/8 |
| MYM | 15 | eod | -0.589 | -1.623 .. +0.445 | -9.8% | -1.016 | 0.29 |  | 5/8 |
| MYM | 60 | h1 * | -0.014 | -0.043 .. +0.016 | -2.6% | -0.022 | 0.36 | 1 | 4/8 |
| MYM | 60 | h2 | +0.002 | -0.042 .. +0.045 | +0.2% | -0.021 | 0.95 |  | 4/8 |
| MYM | 60 | h4 | +0.004 | -0.057 .. +0.066 | +0.4% | -0.018 | 0.89 |  | 5/8 |
| MYM | 60 | h8 | +0.011 | -0.076 .. +0.097 | +0.7% | -0.040 | 0.81 |  | 5/8 |
| MYM | 60 | h16 | +0.005 | -0.112 .. +0.122 | +0.2% | -0.044 | 0.94 |  | 5/8 |
| MYM | 60 | eod | +0.014 | -0.113 .. +0.140 | +0.6% | -0.038 | 0.97 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.47 pts | -1.03 .. +0.09 | 0.1 |
| MES | 15 | -0.41 pts | -1.33 .. +0.51 | 0.39 |
| MES | 60 | +0.13 pts | -1.41 .. +1.67 | 0.87 |
| MNQ | 5 | -0.10 pts | -0.66 .. +0.46 | 0.77 |
| MNQ | 15 | -0.83 pts | -1.75 .. +0.10 | 0.083 |
| MNQ | 60 | -0.47 pts | -2.09 .. +1.15 | 0.57 |
| MYM | 5 | -0.48 pts | -1.23 .. +0.28 | 0.23 |
| MYM | 15 | -0.15 pts | -1.46 .. +1.17 | 0.83 |
| MYM | 60 | +0.56 pts | -1.93 .. +3.04 | 0.95 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 207388 | +0.006 | 0.307 | +0.08 | -3.42 | -3.45 | -3.39 | -3.45 |
| MES | 5 | h2 | top fifth | long | 207224 | +0.007 | 0.346 | +0.12 | -3.38 | -3.43 | -3.35 | -3.41 |
| MES | 5 | h4 | top fifth | long | 207224 | +0.019 | 0.346 | +0.28 | -3.22 | -3.33 | -3.13 | -3.30 |
| MES | 5 | h8 | top fifth | long | 207224 | +0.043 | 0.346 | +0.58 | -2.92 | -3.15 | -2.77 | -3.10 |
| MES | 5 | h16 | top fifth | long | 207224 | +0.094 | 0.346 | +1.14 | -2.36 | -2.80 | -2.05 | -2.74 |
| MES | 5 | eod | top fifth | long | 207224 | +0.436 | 0.346 | +3.40 | -0.10 | +1.57 | -1.28 | -2.27 |
| MES | 15 | h1 | bottom fifth | long | 68506 | +0.010 | 0.172 | +0.10 | -3.40 | -3.40 | -3.39 | -3.46 |
| MES | 15 | h2 | top fifth | long | 68421 | +0.018 | 0.196 | +0.34 | -3.16 | -3.30 | -3.04 | -3.30 |
| MES | 15 | h4 | top fifth | long | 68421 | +0.039 | 0.196 | +0.71 | -2.79 | -3.05 | -2.59 | -3.09 |
| MES | 15 | h8 | top fifth | long | 68421 | +0.072 | 0.196 | +1.27 | -2.23 | -2.58 | -1.96 | -2.78 |
| MES | 15 | h16 | top fifth | long | 68421 | +0.126 | 0.196 | +1.90 | -1.60 | -1.73 | -1.49 | -2.68 |
| MES | 15 | eod | top fifth | long | 68421 | +0.194 | 0.196 | +2.43 | -1.07 | +0.85 | -2.56 | -2.53 |
| MES | 60 | h1 | top fifth | long | 16683 | +0.025 | 0.096 | +0.94 | -2.56 | -3.12 | -2.04 | -2.85 |
| MES | 60 | h2 | top fifth | long | 16683 | +0.044 | 0.096 | +1.45 | -2.05 | -2.72 | -1.43 | -2.64 |
| MES | 60 | h4 | top fifth | long | 16683 | +0.076 | 0.096 | +2.37 | -1.13 | -1.79 | -0.52 | -2.22 |
| MES | 60 | h8 | top fifth | long | 16683 | +0.093 | 0.096 | +3.13 | -0.37 | -0.97 | +0.17 | -1.94 |
| MES | 60 | h16 | top fifth | long | 16683 | +0.097 | 0.096 | +3.89 | +0.39 | -0.60 | +1.30 | -1.19 |
| MES | 60 | eod | top fifth | long | 16683 | +0.101 | 0.096 | +4.17 | +0.67 | -0.54 | +1.79 | -0.67 |
| MNQ | 5 | h1 | top fifth | long | 206876 | +0.008 | 0.158 | +0.13 | -1.87 | -1.96 | -1.78 | -1.91 |
| MNQ | 5 | h2 | top fifth | long | 206876 | +0.016 | 0.158 | +0.27 | -1.73 | -1.90 | -1.56 | -1.79 |
| MNQ | 5 | h4 | top fifth | long | 206876 | +0.032 | 0.158 | +0.56 | -1.44 | -1.80 | -1.09 | -1.56 |
| MNQ | 5 | h8 | top fifth | long | 206876 | +0.056 | 0.158 | +1.03 | -0.97 | -1.64 | -0.33 | -1.22 |
| MNQ | 5 | h16 | top fifth | long | 206876 | +0.110 | 0.158 | +1.98 | -0.02 | -1.32 | +1.25 | -0.54 |
| MNQ | 5 | eod | top fifth | long | 206876 | +1.160 | 0.158 | +5.32 | +3.32 | +2.59 | +4.03 | -0.62 |
| MNQ | 15 | h1 | bottom fifth | long | 68437 | +0.011 | 0.068 | -0.02 | -2.02 | -1.93 | -2.13 | -2.14 |
| MNQ | 15 | h2 | top fifth | long | 68413 | +0.019 | 0.082 | +0.59 | -1.41 | -1.77 | -1.08 | -1.60 |
| MNQ | 15 | h4 | top fifth | long | 68413 | +0.033 | 0.082 | +1.10 | -0.90 | -1.57 | -0.28 | -1.28 |
| MNQ | 15 | h8 | bottom fifth | long | 68437 | +0.056 | 0.068 | +0.57 | -1.43 | -1.42 | -1.44 | -1.77 |
| MNQ | 15 | h16 | top fifth | long | 68413 | +0.133 | 0.082 | +3.19 | +1.19 | -0.63 | +2.85 | -0.14 |
| MNQ | 15 | eod | top fifth | long | 68413 | +0.477 | 0.082 | +4.14 | +2.14 | +2.45 | +1.86 | +0.11 |
| MNQ | 60 | h1 | top fifth | long | 16682 | +0.022 | 0.038 | +1.26 | -0.74 | -1.65 | +0.13 | -1.26 |
| MNQ | 60 | h2 | bottom fifth | long | 16683 | +0.027 | 0.037 | +0.45 | -1.55 | -1.32 | -1.82 | -1.89 |
| MNQ | 60 | h4 | bottom fifth | long | 16683 | +0.057 | 0.037 | +1.61 | -0.39 | -0.56 | -0.20 | -1.17 |
| MNQ | 60 | h8 | top fifth | long | 16682 | +0.108 | 0.038 | +4.45 | +2.45 | +0.61 | +4.22 | +0.01 |
| MNQ | 60 | h16 | top fifth | long | 16682 | +0.127 | 0.038 | +5.32 | +3.32 | +1.14 | +5.41 | +1.57 |
| MNQ | 60 | eod | top fifth | long | 16682 | +0.132 | 0.038 | +5.69 | +3.69 | +1.17 | +6.10 | +2.29 |
| MYM | 5 | h1 | bottom fifth | long | 103835 | -0.000 | 0.147 | +0.08 | -1.92 | +nan | -1.92 | -1.92 |
| MYM | 5 | h2 | top fifth | long | 103787 | +0.000 | 0.203 | +0.08 | -1.92 | +nan | -1.92 | -1.89 |
| MYM | 5 | h4 | top fifth | long | 103787 | +0.005 | 0.203 | +0.18 | -1.82 | +nan | -1.82 | -1.77 |
| MYM | 5 | h8 | top fifth | long | 103787 | +0.016 | 0.203 | +0.44 | -1.56 | +nan | -1.56 | -1.53 |
| MYM | 5 | h16 | top fifth | long | 103787 | +0.048 | 0.203 | +0.83 | -1.17 | +nan | -1.17 | -1.31 |
| MYM | 5 | eod | bottom fifth | long | 103835 | -0.145 | 0.147 | +3.45 | +1.45 | +nan | +1.45 | +2.25 |
| MYM | 15 | h1 | top fifth | long | 34284 | +0.005 | 0.104 | +0.17 | -1.83 | +nan | -1.83 | -1.90 |
| MYM | 15 | h2 | top fifth | long | 34284 | +0.013 | 0.104 | +0.38 | -1.62 | +nan | -1.62 | -1.71 |
| MYM | 15 | h4 | top fifth | long | 34284 | +0.019 | 0.104 | +0.54 | -1.46 | +nan | -1.46 | -1.62 |
| MYM | 15 | h8 | top fifth | long | 34284 | +0.026 | 0.104 | +0.85 | -1.15 | +nan | -1.15 | -1.38 |
| MYM | 15 | h16 | top fifth | long | 34284 | +0.053 | 0.104 | +1.57 | -0.43 | +nan | -0.43 | -0.51 |
| MYM | 15 | eod | top fifth | long | 34284 | +0.074 | 0.104 | +3.29 | +1.29 | +nan | +1.29 | +1.29 |
| MYM | 60 | h1 | top fifth | long | 8331 | +0.017 | 0.049 | +0.64 | -1.36 | +nan | -1.36 | -1.60 |
| MYM | 60 | h2 | top fifth | long | 8331 | +0.027 | 0.049 | +0.89 | -1.11 | +nan | -1.11 | -1.53 |
| MYM | 60 | h4 | top fifth | long | 8331 | +0.036 | 0.049 | +0.99 | -1.01 | +nan | -1.01 | -1.84 |
| MYM | 60 | h8 | bottom fifth | long | 8331 | +0.039 | 0.045 | +0.57 | -1.43 | +nan | -1.43 | -2.31 |
| MYM | 60 | h16 | bottom fifth | long | 8331 | +0.088 | 0.045 | +1.56 | -0.44 | +nan | -0.44 | -1.58 |
| MYM | 60 | eod | bottom fifth | long | 8331 | +0.112 | 0.045 | +2.03 | +0.03 | +nan | +0.03 | -2.35 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.003 | -0.900 | -0.717 | -0.486 | -0.290 | +0.000 | -0.012 | -0.011 | -0.002 | +0.006 | +0.030 |
| MES | 15 | -2.486 | -1.875 | -1.316 | -0.855 | -0.517 | +0.000 | -0.007 | -0.002 | -0.000 | +0.013 | +0.017 |
| MES | 60 | -3.810 | -3.021 | -2.192 | -1.455 | -0.887 | +0.000 | +0.002 | +0.004 | -0.005 | -0.083 | -0.389 |
| MNQ | 5 | -1.174 | -1.030 | -0.801 | -0.531 | -0.313 | +0.000 | +0.002 | +0.010 | +0.027 | +0.031 | +0.021 |
| MNQ | 15 | -2.751 | -2.045 | -1.412 | -0.913 | -0.550 | +0.000 | +0.007 | +0.015 | +0.013 | +0.011 | +0.055 |
| MNQ | 60 | -3.936 | -3.094 | -2.233 | -1.496 | -0.918 | +0.000 | +0.002 | -0.007 | -0.014 | -0.057 | +0.181 |
| MYM | 5 | -1.030 | -0.944 | -0.754 | -0.504 | -0.297 | +0.000 | +0.003 | +0.010 | +0.030 | +0.052 | +0.088 |
| MYM | 15 | -2.541 | -1.957 | -1.393 | -0.904 | -0.545 | +0.000 | +0.019 | +0.044 | +0.072 | +0.120 | +0.274 |
| MYM | 60 | -3.903 | -3.069 | -2.266 | -1.522 | -0.930 | +0.000 | +0.013 | +0.019 | -0.004 | -0.038 | -0.702 |

## Calibration

- MES 5-min: 1036271 bars, 207224 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68421 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 206876 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68413 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16682 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103787 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34284 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8331 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
