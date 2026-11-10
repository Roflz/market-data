# Impact card: pat_outside_bar

candle pattern outside_bar in its textbook direction: high > previous high AND low < previous low; direction of the close vs open [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.008 R20 over the next 1 bar (5 min), p=0.15; we would catch an effect of 0.020 R20 or more 80% of the time).
- MES 5-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.024 R20, CONFIRMED, q=2.98e-11, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.54 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.195 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.022 R20 over the next 4 bars (1 h), p=0.52; we would catch an effect of 0.039 R20 or more 80% of the time).
- MES 15-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.024 R20, CONFIRMED, q=0.00144, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.57 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.122 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.060 R20 over the next 8 bars (8 h), p=0.18; we would catch an effect of 0.052 R20 or more 80% of the time).
- MES 60-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.025 R20, possible, q=0.22, 12 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.30 at recent bar sizes, 90% range up to $5.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.017 R20 over the next 4 bars (20 min), p=0.31; we would catch an effect of 0.024 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.015 R20, possible, q=0.057, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.00 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.076 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.019 R20 over the next 1 bar (15 min), p=0.029; we would catch an effect of 0.040 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 4% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.023 R20, CONFIRMED, q=0.0081, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.85 at recent bar sizes, 90% range up to $3.29); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.064 R20 over the next 16 bars (16 h), p=0.3; we would catch an effect of 0.054 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.056).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.77 at recent bar sizes, 90% range up to $6.72); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.167 R20 over the rest of the session (to 16:45), p=0.43; we would catch an effect of 0.037 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.15).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.07 at recent bar sizes, 90% range up to $0.44); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.068 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.055 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.67).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.92 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.097 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.018 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.070 R20 or more 80% of the time).
- MYM 60-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.038 R20, possible, q=0.132, 6 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.74 at recent bar sizes, 90% range up to $3.25); about 4.3x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.008 | -0.016 .. -0.001 | -0.0026 | 0.025 / 0.025 / 0.02 | 0.0175 | 1 | 0.992 | 11/16 | -0.007 | -0.009 | False | -2.1 / -2.2 |  |
| MES | 5 | h2 | -0.010 | -0.019 .. -0.000 | -0.0021 | 0.048 / 0.046 / 0.058 | 0.0583 |  |  | 12/16 | -0.015 | -0.004 |  | -1.8 / -2.0 |  |
| MES | 5 | h4 | -0.014 | -0.028 .. -0.000 | -0.0020 | 0.045 / 0.041 / 0.052 | 0.0518 |  |  | 9/16 | -0.018 | -0.009 |  | -1.9 / -2.0 | 0.020 |
| MES | 5 | h8 | -0.014 | -0.034 .. +0.005 | -0.0014 | 0.15 / 0.16 / 0.17 | 0.164 |  |  | 12/16 | -0.016 | -0.013 |  | -1.4 / -1.4 |  |
| MES | 5 | h16 | -0.003 | -0.031 .. +0.024 | -0.0002 | 0.81 / 0.81 / 0.82 | 0.818 |  |  | 8/16 | -0.013 | +0.006 |  | -0.2 / -0.2 |  |
| MES | 5 | eod | +0.038 | -0.087 .. +0.162 | +0.0005 | 0.55 / 0.56 / 0.57 | 0.564 |  |  | 7/16 | -0.034 | +0.109 |  | +0.6 / +0.6 |  |
| MES | 15 | h1 | -0.010 | -0.022 .. +0.003 | -0.0033 | 0.12 / 0.12 / 0.13 | 0.134 |  |  | 12/16 | -0.011 | -0.009 |  | -1.6 / -1.5 |  |
| MES | 15 | h2 | -0.015 | -0.032 .. +0.002 | -0.0034 | 0.093 / 0.084 / 0.12 | 0.114 |  |  | 10/16 | -0.034 | +0.004 |  | -1.7 / -1.7 |  |
| MES | 15 | h4 * | -0.022 | -0.047 .. +0.003 | -0.0033 | 0.084 / 0.067 / 0.11 | 0.103 | 1 | 1 | 11/16 | -0.051 | +0.007 | False | -1.8 / -1.7 | 0.039 |
| MES | 15 | h8 | -0.023 | -0.061 .. +0.015 | -0.0025 | 0.23 / 0.2 / 0.22 | 0.221 |  |  | 11/16 | -0.073 | +0.026 |  | -1.3 / -1.2 |  |
| MES | 15 | h16 | -0.039 | -0.091 .. +0.014 | -0.0029 | 0.15 / 0.12 / 0.11 | 0.107 |  |  | 12/16 | -0.085 | +0.008 |  | -1.6 / -1.4 |  |
| MES | 15 | eod | +0.026 | -0.073 .. +0.125 | +0.0008 | 0.6 / 0.6 / 0.64 | 0.639 |  |  | 9/16 | +0.034 | +0.019 |  | +0.5 / +0.5 |  |
| MES | 60 | h1 | -0.006 | -0.027 .. +0.014 | -0.0026 | 0.53 / 0.53 / 0.54 | 0.553 |  |  | 10/16 | -0.005 | -0.008 |  | -0.6 / -0.6 |  |
| MES | 60 | h2 | -0.007 | -0.034 .. +0.021 | -0.0019 | 0.63 / 0.63 / 0.64 | 0.645 |  |  | 10/16 | +0.001 | -0.014 |  | -0.5 / -0.5 |  |
| MES | 60 | h4 | -0.025 | -0.061 .. +0.011 | -0.0051 | 0.17 / 0.17 / 0.17 | 0.169 |  |  | 10/16 | -0.012 | -0.039 |  | -1.3 / -1.4 | 0.052 |
| MES | 60 | h8 * | -0.060 | -0.109 .. -0.011 | -0.0088 | 0.017 / 0.018 / 0.02 | 0.0188 | 1 | 0.96 | 11/16 | -0.027 | -0.093 | False | -2.2 / -2.4 |  |
| MES | 60 | h16 | -0.070 | -0.129 .. -0.012 | -0.0079 | 0.019 / 0.019 / 0.026 | 0.0253 |  |  | 10/16 | -0.020 | -0.120 |  | -2.2 / -2.4 |  |
| MES | 60 | eod | -0.064 | -0.125 .. -0.004 | -0.0069 | 0.037 / 0.036 / 0.047 | 0.0448 |  |  | 10/16 | -0.006 | -0.123 |  | -1.9 / -2.1 |  |
| MNQ | 5 | h1 | -0.004 | -0.011 .. +0.002 | -0.0014 | 0.19 / 0.18 / 0.27 | 0.267 |  |  | 9/16 | +0.003 | -0.011 |  | -1.3 / -1.3 |  |
| MNQ | 5 | h2 | -0.009 | -0.019 .. +0.000 | -0.0018 | 0.051 / 0.049 / 0.11 | 0.11 |  |  | 11/16 | -0.004 | -0.014 |  | -2.1 / -1.9 |  |
| MNQ | 5 | h4 * | -0.017 | -0.030 .. -0.003 | -0.0021 | 0.013 / 0.012 / 0.05 | 0.0529 | 1 | 0.871 | 12/16 | -0.014 | -0.019 | False | -2.6 / -2.5 | 0.024 |
| MNQ | 5 | h8 | -0.023 | -0.041 .. -0.006 | -0.0020 | 0.0091 / 0.011 / 0.06 | 0.0617 |  |  | 12/16 | -0.025 | -0.022 |  | -2.5 / -2.6 |  |
| MNQ | 5 | h16 | -0.018 | -0.043 .. +0.008 | -0.0011 | 0.18 / 0.17 / 0.32 | 0.317 |  |  | 8/16 | -0.004 | -0.031 |  | -1.3 / -1.3 |  |
| MNQ | 5 | eod | +0.021 | -0.115 .. +0.157 | +0.0003 | 0.76 / 0.76 / 0.79 | 0.782 |  |  | 8/16 | +0.035 | +0.007 |  | +0.3 / +0.3 |  |
| MNQ | 15 | h1 * | -0.019 | -0.029 .. -0.009 | -0.0057 | 0.0003 / 0.00034 / 0.0041 | 0.00964 | 0.703 | 0.11 | 12/16 | -0.020 | -0.018 | False | -3.3 / -3.6 |  |
| MNQ | 15 | h2 | -0.023 | -0.038 .. -0.009 | -0.0042 | 0.0015 / 0.0018 / 0.031 | 0.0419 |  |  | 12/16 | -0.037 | -0.010 |  | -2.9 / -3.2 |  |
| MNQ | 15 | h4 | -0.039 | -0.061 .. -0.018 | -0.0042 | 0.00041 / 0.00042 / 0.042 | 0.0451 |  |  | 12/16 | -0.047 | -0.031 |  | -3.5 / -3.5 | 0.040 |
| MNQ | 15 | h8 | -0.048 | -0.078 .. -0.019 | -0.0040 | 0.0012 / 0.0016 / 0.051 | 0.0518 |  |  | 14/16 | -0.051 | -0.046 |  | -3.0 / -3.2 |  |
| MNQ | 15 | h16 | -0.034 | -0.078 .. +0.009 | -0.0023 | 0.12 / 0.12 / 0.23 | 0.226 |  |  | 12/16 | -0.047 | -0.022 |  | -1.5 / -1.6 |  |
| MNQ | 15 | eod | +0.024 | -0.084 .. +0.133 | +0.0006 | 0.66 / 0.66 / 0.75 | 0.743 |  |  | 9/16 | +0.032 | +0.017 |  | +0.4 / +0.4 |  |
| MNQ | 60 | h1 | -0.011 | -0.033 .. +0.011 | -0.0045 | 0.33 / 0.33 / 0.32 | 0.332 |  |  | 8/16 | -0.005 | -0.017 |  | -1.0 / -1.0 |  |
| MNQ | 60 | h2 | -0.016 | -0.046 .. +0.014 | -0.0046 | 0.29 / 0.3 / 0.28 | 0.281 |  |  | 9/16 | -0.007 | -0.025 |  | -1.0 / -1.1 |  |
| MNQ | 60 | h4 | -0.011 | -0.048 .. +0.026 | -0.0023 | 0.55 / 0.56 / 0.56 | 0.573 |  |  | 8/16 | +0.005 | -0.027 |  | -0.6 / -0.6 | 0.054 |
| MNQ | 60 | h8 | -0.032 | -0.082 .. +0.018 | -0.0047 | 0.22 / 0.23 / 0.23 | 0.234 |  |  | 9/16 | -0.013 | -0.051 |  | -1.2 / -1.2 |  |
| MNQ | 60 | h16 * | -0.064 | -0.126 .. -0.003 | -0.0073 | 0.04 / 0.04 / 0.047 | 0.0503 | 1 | 0.996 | 10/16 | -0.044 | -0.085 | False | -1.9 / -2.1 |  |
| MNQ | 60 | eod | -0.064 | -0.125 .. -0.003 | -0.0070 | 0.04 / 0.041 / 0.052 | 0.0521 |  |  | 10/16 | -0.037 | -0.091 |  | -1.9 / -2.1 |  |
| MYM | 5 | h1 | -0.004 | -0.012 .. +0.004 | -0.0013 | 0.3 / 0.32 / 0.57 | 0.572 |  |  | 6/8 | n/a | -0.004 |  | -0.9 / -1.0 |  |
| MYM | 5 | h2 | -0.001 | -0.013 .. +0.010 | -0.0002 | 0.83 / 0.83 / 0.92 | 0.899 |  |  | 5/8 | n/a | -0.001 |  | -0.2 / -0.2 |  |
| MYM | 5 | h4 | -0.003 | -0.019 .. +0.014 | -0.0003 | 0.74 / 0.74 / 0.87 | 0.872 |  |  | 6/8 | n/a | -0.003 |  | -0.3 / -0.3 | 0.037 |
| MYM | 5 | h8 | -0.008 | -0.031 .. +0.016 | -0.0006 | 0.52 / 0.51 / 0.68 | 0.662 |  |  | 6/8 | n/a | -0.008 |  | -0.6 / -0.6 |  |
| MYM | 5 | h16 | +0.017 | -0.017 .. +0.050 | +0.0010 | 0.33 / 0.34 / 0.46 | 0.459 |  |  | 5/8 | n/a | +0.017 |  | +0.9 / +1.0 |  |
| MYM | 5 | eod * | +0.167 | -0.009 .. +0.343 | +0.0024 | 0.063 / 0.057 / 0.096 | 0.0975 | 1 | 1 | 7/8 | n/a | +0.167 | False | +1.9 / +1.9 |  |
| MYM | 15 | h1 | -0.003 | -0.018 .. +0.012 | -0.0009 | 0.71 / 0.72 / 0.78 | 0.768 |  |  | 4/8 | n/a | -0.003 |  | -0.4 / -0.4 |  |
| MYM | 15 | h2 | +0.002 | -0.018 .. +0.023 | +0.0005 | 0.81 / 0.82 / 0.88 | 0.879 |  |  | 5/8 | n/a | +0.002 |  | +0.2 / +0.2 |  |
| MYM | 15 | h4 | +0.003 | -0.024 .. +0.031 | +0.0003 | 0.82 / 0.84 / 0.91 | 0.889 |  |  | 4/8 | n/a | +0.003 |  | +0.2 / +0.2 | 0.055 |
| MYM | 15 | h8 | -0.010 | -0.050 .. +0.030 | -0.0009 | 0.62 / 0.63 / 0.75 | 0.748 |  |  | 5/8 | n/a | -0.010 |  | -0.5 / -0.5 |  |
| MYM | 15 | h16 | +0.026 | -0.034 .. +0.086 | +0.0016 | 0.4 / 0.4 / 0.57 | 0.572 |  |  | 5/8 | n/a | +0.026 |  | +0.8 / +0.8 |  |
| MYM | 15 | eod * | +0.068 | -0.064 .. +0.200 | +0.0017 | 0.31 / 0.29 / 0.51 | 0.514 | 1 | 1 | 5/8 | n/a | +0.068 | False | +0.9 / +1.0 |  |
| MYM | 60 | h1 * | +0.018 | -0.008 .. +0.043 | +0.0076 | 0.17 / 0.19 / 0.21 | 0.219 | 1 | 1 | 6/8 | n/a | +0.018 | False | +1.2 / +1.4 |  |
| MYM | 60 | h2 | +0.017 | -0.018 .. +0.053 | +0.0052 | 0.34 / 0.35 / 0.37 | 0.384 |  |  | 6/8 | n/a | +0.017 |  | +0.9 / +1.0 |  |
| MYM | 60 | h4 | +0.018 | -0.026 .. +0.063 | +0.0039 | 0.42 / 0.46 / 0.47 | 0.482 |  |  | 5/8 | n/a | +0.018 |  | +0.7 / +0.8 | 0.070 |
| MYM | 60 | h8 | +0.020 | -0.042 .. +0.083 | +0.0032 | 0.53 / 0.56 / 0.56 | 0.56 |  |  | 5/8 | n/a | +0.020 |  | +0.5 / +0.6 |  |
| MYM | 60 | h16 | -0.017 | -0.101 .. +0.068 | -0.0020 | 0.7 / 0.72 / 0.7 | 0.693 |  |  | 4/8 | n/a | -0.017 |  | -0.4 / -0.4 |  |
| MYM | 60 | eod | -0.017 | -0.103 .. +0.069 | -0.0019 | 0.7 / 0.72 / 0.71 | 0.709 |  |  | 4/8 | n/a | -0.017 |  | -0.4 / -0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.024 | +0.018 .. +0.030 | +4.8% | +0.045 | 7.5e-14 | 2.98e-11 | 15/16 |
| MES | 5 | h2 | +0.028 | +0.020 .. +0.035 | +3.9% | +0.044 | 4.2e-11 |  | 16/16 |
| MES | 5 | h4 | +0.038 | +0.027 .. +0.049 | +3.8% | +0.059 | 1e-11 |  | 16/16 |
| MES | 5 | h8 | +0.039 | +0.024 .. +0.054 | +2.7% | +0.060 | 1.6e-05 |  | 15/16 |
| MES | 5 | h16 | +0.031 | +0.009 .. +0.054 | +1.5% | +0.042 | 0.12 |  | 12/16 |
| MES | 5 | eod | -0.048 | -0.224 .. +0.128 | -0.5% | -0.151 | 0.59 |  | 7/16 |
| MES | 15 | h1 * | +0.024 | +0.015 .. +0.034 | +4.8% | +0.047 | 6.1e-06 | 0.00144 | 14/16 |
| MES | 15 | h2 | +0.029 | +0.017 .. +0.041 | +4.0% | +0.050 | 0.00083 |  | 12/16 |
| MES | 15 | h4 | +0.026 | +0.008 .. +0.044 | +2.5% | +0.051 | 0.048 |  | 14/16 |
| MES | 15 | h8 | +0.039 | +0.013 .. +0.065 | +2.5% | +0.052 | 0.025 |  | 13/16 |
| MES | 15 | h16 | +0.028 | -0.012 .. +0.068 | +1.2% | +0.027 | 0.23 |  | 12/16 |
| MES | 15 | eod | +0.029 | -0.098 .. +0.156 | +0.5% | -0.024 | 0.65 |  | 13/16 |
| MES | 60 | h1 * | +0.025 | +0.010 .. +0.040 | +4.9% | +0.044 | 0.0013 | 0.22 | 12/16 |
| MES | 60 | h2 | +0.009 | -0.012 .. +0.029 | +1.2% | +0.036 | 0.4 |  | 10/16 |
| MES | 60 | h4 | +0.012 | -0.014 .. +0.038 | +1.1% | +0.023 | 0.45 |  | 9/16 |
| MES | 60 | h8 | -0.000 | -0.038 .. +0.037 | -0.0% | +0.032 | 0.99 |  | 9/16 |
| MES | 60 | h16 | -0.030 | -0.070 .. +0.009 | -1.5% | +0.006 | 0.27 |  | 10/16 |
| MES | 60 | eod | -0.039 | -0.080 .. +0.001 | -1.8% | -0.003 | 0.11 |  | 10/16 |
| MNQ | 5 | h1 * | +0.015 | +0.010 .. +0.020 | +2.9% | +0.035 | 0.0003 | 0.057 | 14/16 |
| MNQ | 5 | h2 | +0.018 | +0.010 .. +0.026 | +2.3% | +0.031 | 0.0017 |  | 14/16 |
| MNQ | 5 | h4 | +0.024 | +0.011 .. +0.038 | +2.2% | +0.036 | 0.016 |  | 13/16 |
| MNQ | 5 | h8 | +0.014 | -0.011 .. +0.038 | +0.8% | +0.028 | 0.48 |  | 13/16 |
| MNQ | 5 | h16 | +0.002 | -0.040 .. +0.045 | +0.1% | +0.002 | 0.91 |  | 12/16 |
| MNQ | 5 | eod | -0.053 | -0.300 .. +0.194 | -0.4% | -0.235 | 0.67 |  | 6/16 |
| MNQ | 15 | h1 * | +0.023 | +0.014 .. +0.031 | +4.3% | +0.034 | 3.7e-05 | 0.0081 | 14/16 |
| MNQ | 15 | h2 | +0.030 | +0.016 .. +0.044 | +3.9% | +0.039 | 0.014 |  | 15/16 |
| MNQ | 15 | h4 | +0.017 | -0.012 .. +0.046 | +1.5% | +0.029 | 0.67 |  | 12/16 |
| MNQ | 15 | h8 | +0.004 | -0.039 .. +0.048 | +0.3% | +0.005 | 0.86 |  | 13/16 |
| MNQ | 15 | h16 | +0.010 | -0.043 .. +0.062 | +0.4% | -0.022 | 0.72 |  | 11/16 |
| MNQ | 15 | eod | -0.020 | -0.213 .. +0.173 | -0.3% | -0.052 | 0.88 |  | 5/16 |
| MNQ | 60 | h1 | +0.017 | +0.000 .. +0.033 | +3.2% | +0.038 | 0.047 |  | 12/16 |
| MNQ | 60 | h2 * | +0.029 | +0.007 .. +0.051 | +3.8% | +0.053 | 0.0093 | 1 | 13/16 |
| MNQ | 60 | h4 | +0.024 | -0.004 .. +0.051 | +2.1% | +0.047 | 0.11 |  | 10/16 |
| MNQ | 60 | h8 | +0.013 | -0.020 .. +0.047 | +0.8% | +0.037 | 0.53 |  | 8/16 |
| MNQ | 60 | h16 | -0.003 | -0.043 .. +0.037 | -0.1% | +0.021 | 0.89 |  | 7/16 |
| MNQ | 60 | eod | -0.009 | -0.050 .. +0.032 | -0.4% | +0.018 | 0.71 |  | 10/16 |
| MYM | 5 | h1 * | +0.020 | +0.013 .. +0.027 | +3.8% | +0.037 | 0.026 | 1 | 7/8 |
| MYM | 5 | h2 | +0.020 | +0.008 .. +0.031 | +2.6% | +0.034 | 0.037 |  | 7/8 |
| MYM | 5 | h4 | +0.025 | +0.003 .. +0.047 | +2.3% | +0.043 | 0.16 |  | 7/8 |
| MYM | 5 | h8 | +0.028 | -0.010 .. +0.066 | +1.8% | +0.043 | 0.21 |  | 7/8 |
| MYM | 5 | h16 | +0.030 | -0.025 .. +0.084 | +1.3% | +0.042 | 0.32 |  | 7/8 |
| MYM | 5 | eod | +0.026 | -0.220 .. +0.271 | +0.2% | -0.040 | 0.84 |  | 5/8 |
| MYM | 15 | h1 * | +0.017 | +0.004 .. +0.029 | +3.1% | +0.028 | 0.11 | 1 | 7/8 |
| MYM | 15 | h2 | +0.020 | -0.001 .. +0.040 | +2.6% | +0.034 | 0.14 |  | 7/8 |
| MYM | 15 | h4 | +0.020 | -0.017 .. +0.056 | +1.8% | +0.029 | 0.57 |  | 7/8 |
| MYM | 15 | h8 | +0.022 | -0.032 .. +0.075 | +1.3% | +0.031 | 0.64 |  | 7/8 |
| MYM | 15 | h16 | +0.009 | -0.085 .. +0.103 | +0.4% | -0.003 | 1 |  | 6/8 |
| MYM | 15 | eod | +0.067 | -0.167 .. +0.301 | +1.1% | +0.043 | 0.58 |  | 7/8 |
| MYM | 60 | h1 * | +0.038 | +0.016 .. +0.059 | +7.2% | +0.056 | 0.00075 | 0.132 | 6/8 |
| MYM | 60 | h2 | +0.025 | -0.001 .. +0.052 | +3.4% | +0.047 | 0.15 |  | 6/8 |
| MYM | 60 | h4 | +0.035 | -0.005 .. +0.076 | +3.3% | +0.052 | 0.088 |  | 5/8 |
| MYM | 60 | h8 | +0.060 | +0.009 .. +0.112 | +3.9% | +0.081 | 0.022 |  | 6/8 |
| MYM | 60 | h16 | +0.034 | -0.028 .. +0.095 | +1.6% | +0.057 | 0.29 |  | 5/8 |
| MYM | 60 | eod | +0.029 | -0.033 .. +0.090 | +1.3% | +0.046 | 0.42 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.35 pts | -0.75 .. +0.06 | 0.11 |
| MES | 15 | -0.65 pts | -1.28 .. -0.01 | 0.049 |
| MES | 60 | -0.41 pts | -1.47 .. +0.65 | 0.45 |
| MNQ | 5 | -0.38 pts | -0.76 .. +0.00 | 0.052 |
| MNQ | 15 | -0.78 pts | -1.32 .. -0.24 | 0.0096 |
| MNQ | 60 | +0.05 pts | -0.99 .. +1.08 | 0.98 |
| MYM | 5 | -0.18 pts | -0.63 .. +0.28 | 0.53 |
| MYM | 15 | -0.34 pts | -1.02 .. +0.34 | 0.53 |
| MYM | 60 | +0.45 pts | -0.87 .. +1.77 | 0.59 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 48492 | +0.020 | 0.245 | +0.19 | -3.31 | -3.35 | -3.29 | -3.47 |
| MES | 5 | h2 | event | against signal | 48492 | +0.026 | 0.245 | +0.24 | -3.26 | -3.24 | -3.27 | -3.49 |
| MES | 5 | h4 | event | against signal | 48492 | +0.031 | 0.245 | +0.31 | -3.19 | -3.20 | -3.19 | -3.43 |
| MES | 5 | h8 | event | against signal | 48492 | +0.029 | 0.245 | +0.23 | -3.27 | -3.24 | -3.28 | -3.48 |
| MES | 5 | h16 | event | against signal | 48492 | +0.020 | 0.245 | -0.10 | -3.60 | -3.21 | -3.80 | -3.83 |
| MES | 5 | eod | event | with signal | 48492 | +0.018 | 0.245 | +0.49 | -3.01 | -4.09 | -2.45 | -2.67 |
| MES | 15 | h1 | event | against signal | 22049 | +0.018 | 0.162 | +0.37 | -3.13 | -3.30 | -3.02 | -3.31 |
| MES | 15 | h2 | event | against signal | 22049 | +0.025 | 0.162 | +0.52 | -2.98 | -2.99 | -2.97 | -3.19 |
| MES | 15 | h4 | event | against signal | 22049 | +0.031 | 0.162 | +0.14 | -3.36 | -2.92 | -3.64 | -3.57 |
| MES | 15 | h8 | event | against signal | 22049 | +0.034 | 0.162 | -0.13 | -3.63 | -2.77 | -4.18 | -3.86 |
| MES | 15 | h16 | event | against signal | 22049 | +0.051 | 0.162 | -0.22 | -3.72 | -2.95 | -4.21 | -3.99 |
| MES | 15 | eod | event | with signal | 22049 | +0.031 | 0.162 | +1.47 | -2.03 | -3.06 | -1.38 | -2.02 |
| MES | 60 | h1 | event | against signal | 7580 | +0.007 | 0.089 | +0.54 | -2.96 | -3.47 | -2.54 | -2.97 |
| MES | 60 | h2 | event | against signal | 7580 | +0.010 | 0.089 | +0.87 | -2.63 | -3.62 | -1.83 | -2.73 |
| MES | 60 | h4 | event | against signal | 7580 | +0.030 | 0.089 | +1.77 | -1.73 | -3.49 | -0.30 | -1.92 |
| MES | 60 | h8 | event | against signal | 7580 | +0.067 | 0.089 | +2.45 | -1.05 | -2.97 | +0.50 | -1.35 |
| MES | 60 | h16 | event | against signal | 7580 | +0.067 | 0.089 | +1.97 | -1.53 | -3.58 | +0.13 | -1.43 |
| MES | 60 | eod | event | against signal | 7580 | +0.066 | 0.089 | +1.89 | -1.61 | -3.85 | +0.21 | -1.68 |
| MNQ | 5 | h1 | event | against signal | 74690 | +0.009 | 0.109 | +0.19 | -1.81 | -1.98 | -1.70 | -1.90 |
| MNQ | 5 | h2 | event | against signal | 74690 | +0.018 | 0.109 | +0.36 | -1.64 | -1.93 | -1.46 | -1.79 |
| MNQ | 5 | h4 | event | against signal | 74690 | +0.022 | 0.109 | +0.47 | -1.53 | -1.85 | -1.33 | -1.64 |
| MNQ | 5 | h8 | event | against signal | 74690 | +0.022 | 0.109 | +0.46 | -1.54 | -1.81 | -1.37 | -1.53 |
| MNQ | 5 | h16 | event | against signal | 74690 | +0.015 | 0.109 | +0.29 | -1.71 | -1.90 | -1.59 | -1.66 |
| MNQ | 5 | eod | event | with signal | 74690 | +0.016 | 0.109 | +0.01 | -1.99 | -1.98 | -2.00 | -1.75 |
| MNQ | 15 | h1 | event | against signal | 28845 | +0.022 | 0.069 | +0.53 | -1.47 | -1.83 | -1.19 | -1.57 |
| MNQ | 15 | h2 | event | against signal | 28845 | +0.025 | 0.069 | +0.41 | -1.59 | -1.65 | -1.55 | -1.65 |
| MNQ | 15 | h4 | event | against signal | 28845 | +0.038 | 0.069 | +0.35 | -1.65 | -1.65 | -1.65 | -1.64 |
| MNQ | 15 | h8 | event | against signal | 28845 | +0.044 | 0.069 | +0.29 | -1.71 | -1.62 | -1.78 | -1.58 |
| MNQ | 15 | h16 | event | against signal | 28845 | +0.035 | 0.069 | +0.25 | -1.75 | -1.60 | -1.87 | -1.81 |
| MNQ | 15 | eod | event | with signal | 28845 | +0.034 | 0.069 | +0.73 | -1.27 | -2.05 | -0.68 | -1.37 |
| MNQ | 60 | h1 | event | against signal | 8760 | +0.010 | 0.037 | +0.69 | -1.31 | -2.19 | -0.47 | -1.28 |
| MNQ | 60 | h2 | event | against signal | 8760 | +0.018 | 0.037 | +1.33 | -0.67 | -2.20 | +0.81 | -0.79 |
| MNQ | 60 | h4 | event | against signal | 8760 | +0.015 | 0.037 | +1.65 | -0.35 | -2.56 | +1.78 | -0.60 |
| MNQ | 60 | h8 | event | against signal | 8760 | +0.037 | 0.037 | +1.66 | -0.34 | -1.83 | +1.09 | -0.66 |
| MNQ | 60 | h16 | event | against signal | 8760 | +0.064 | 0.037 | +4.03 | +2.03 | -1.85 | +5.78 | +2.00 |
| MNQ | 60 | eod | event | against signal | 8760 | +0.068 | 0.037 | +4.41 | +2.41 | -1.96 | +6.62 | +2.15 |
| MYM | 5 | h1 | event | against signal | 40577 | +0.012 | 0.161 | +0.07 | -1.93 | +nan | -1.93 | -2.02 |
| MYM | 5 | h2 | event | against signal | 40577 | +0.011 | 0.161 | +0.03 | -1.97 | +nan | -1.97 | -2.09 |
| MYM | 5 | h4 | event | against signal | 40577 | +0.014 | 0.161 | +0.01 | -1.99 | +nan | -1.99 | -2.13 |
| MYM | 5 | h8 | event | against signal | 40577 | +0.019 | 0.161 | -0.03 | -2.03 | +nan | -2.03 | -2.18 |
| MYM | 5 | h16 | event | with signal | 40577 | -0.001 | 0.161 | +0.23 | -1.77 | +nan | -1.77 | -1.56 |
| MYM | 5 | eod | event | with signal | 40577 | +0.136 | 0.161 | +0.84 | -1.16 | +nan | -1.16 | -0.78 |
| MYM | 15 | h1 | event | against signal | 15539 | +0.008 | 0.097 | +0.11 | -1.89 | +nan | -1.89 | -2.00 |
| MYM | 15 | h2 | event | with signal | 15539 | -0.003 | 0.097 | -0.25 | -2.25 | +nan | -2.25 | -2.14 |
| MYM | 15 | h4 | event | with signal | 15539 | +0.001 | 0.097 | +0.02 | -1.98 | +nan | -1.98 | -1.92 |
| MYM | 15 | h8 | event | against signal | 15539 | +0.013 | 0.097 | +0.14 | -1.86 | +nan | -1.86 | -1.93 |
| MYM | 15 | h16 | event | with signal | 15539 | +0.027 | 0.097 | +0.51 | -1.49 | +nan | -1.49 | -1.48 |
| MYM | 15 | eod | event | with signal | 15539 | +0.068 | 0.097 | +1.23 | -0.77 | +nan | -0.77 | -0.65 |
| MYM | 60 | h1 | event | with signal | 4536 | +0.019 | 0.048 | +0.60 | -1.40 | +nan | -1.40 | -1.45 |
| MYM | 60 | h2 | event | with signal | 4536 | +0.013 | 0.048 | +0.09 | -1.91 | +nan | -1.91 | -1.70 |
| MYM | 60 | h4 | event | with signal | 4536 | +0.012 | 0.048 | -0.23 | -2.23 | +nan | -2.23 | -1.94 |
| MYM | 60 | h8 | event | with signal | 4536 | +0.012 | 0.048 | +0.36 | -1.64 | +nan | -1.64 | -1.24 |
| MYM | 60 | h16 | event | against signal | 4536 | +0.009 | 0.048 | -0.28 | -2.28 | +nan | -2.28 | -2.04 |
| MYM | 60 | eod | event | against signal | 4536 | +0.010 | 0.048 | -0.39 | -2.39 | +nan | -2.39 | -2.21 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.425 | -0.468 | -0.516 | -0.517 | -0.703 | +0.000 | -0.029 | -0.035 | -0.040 | -0.039 | -0.028 |
| MES | 15 | -0.511 | -0.535 | -0.559 | -0.541 | -0.721 | +0.000 | -0.020 | -0.027 | -0.037 | -0.042 | -0.082 |
| MES | 60 | -0.680 | -0.588 | -0.561 | -0.512 | -0.690 | +0.000 | -0.007 | -0.012 | -0.042 | -0.084 | -0.073 |
| MNQ | 5 | -0.412 | -0.453 | -0.490 | -0.494 | -0.679 | +0.000 | -0.018 | -0.026 | -0.031 | -0.031 | -0.019 |
| MNQ | 15 | -0.502 | -0.532 | -0.546 | -0.525 | -0.706 | +0.000 | -0.026 | -0.029 | -0.045 | -0.051 | -0.048 |
| MNQ | 60 | -0.738 | -0.625 | -0.566 | -0.516 | -0.684 | +0.000 | -0.010 | -0.022 | -0.031 | -0.076 | +0.007 |
| MYM | 5 | -0.411 | -0.445 | -0.482 | -0.479 | -0.673 | +0.000 | -0.016 | -0.015 | -0.019 | -0.024 | -0.003 |
| MYM | 15 | -0.492 | -0.488 | -0.504 | -0.498 | -0.686 | +0.000 | -0.009 | -0.004 | -0.000 | -0.013 | +0.040 |
| MYM | 60 | -0.648 | -0.585 | -0.543 | -0.509 | -0.681 | +0.000 | +0.019 | +0.018 | +0.003 | -0.035 | -0.045 |

## Calibration

- MES 5-min: 1036271 bars, 48492 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 22049 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 7580 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 74690 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 28845 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 8760 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 40577 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 15539 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 4536 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36521 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
