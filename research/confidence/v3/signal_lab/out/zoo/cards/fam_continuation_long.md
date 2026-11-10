# Impact card: fam_continuation_long

bullish continuation patterns only (long side) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.007 R20 over the next 2 bars (10 min), p=0.62; we would catch an effect of 0.017 R20 or more 80% of the time).
- MES 5-min size: the market moves 4% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.020 R20, CONFIRMED, q=1.56e-17, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.31 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.247 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.011 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.040 R20 or more 80% of the time).
- MES 15-min size: the market moves 4% MORE after the event than after matched bars over the next 4 bars (1 h) (+0.041 R20, CONFIRMED, q=0.0019, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.20 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.134 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.022 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.44).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.19 at recent bar sizes, 90% range up to $4.81); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.008 R20 over the next 1 bar (5 min), p=0.083; we would catch an effect of 0.021 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.036 R20, CONFIRMED, q=2.19e-27, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.19 at recent bar sizes, 90% range up to $0.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.011 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.049 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.035).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.46 at recent bar sizes, 90% range up to $2.19); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.054 R20 over the next 2 bars (2 h), p=0.041; we would catch an effect of 0.080 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.049).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.80 at recent bar sizes, 90% range up to $11.61); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.015 R20 over the next 2 bars (10 min), p=0.15; we would catch an effect of 0.036 R20 or more 80% of the time).
- MYM 5-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.038 R20, CONFIRMED, q=1.91e-11, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.16 at recent bar sizes, 90% range up to $0.54); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.014 R20 over the next 1 bar (15 min), p=0.85; we would catch an effect of 0.068 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.32).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.27 at recent bar sizes, 90% range up to $1.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.009 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.109 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.16).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.35 at recent bar sizes, 90% range up to $5.95); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.004 | -0.010 .. +0.002 | -0.0018 | 0.17 / 0.14 / 0.11 | 0.119 |  |  | 11/16 | +0.002 | -0.010 |  | -1.5 / -1.4 |  |
| MES | 5 | h2 * | -0.007 | -0.015 .. +0.001 | -0.0021 | 0.1 / 0.096 / 0.076 | 0.0755 | 1 | 1 | 11/16 | -0.003 | -0.010 | False | -1.8 / -1.6 |  |
| MES | 5 | h4 | +0.001 | -0.010 .. +0.013 | +0.0002 | 0.86 / 0.86 / 0.87 | 0.864 |  |  | 7/16 | +0.006 | -0.004 |  | +0.2 / +0.2 | 0.017 |
| MES | 5 | h8 | -0.007 | -0.024 .. +0.011 | -0.0010 | 0.47 / 0.47 / 0.38 | 0.375 |  |  | 11/16 | -0.011 | -0.003 |  | -0.9 / -0.7 |  |
| MES | 5 | h16 | -0.015 | -0.045 .. +0.014 | -0.0016 | 0.31 / 0.33 / 0.17 | 0.173 |  |  | 10/16 | -0.017 | -0.013 |  | -1.4 / -1.0 |  |
| MES | 5 | eod | +0.039 | -0.376 .. +0.454 | +0.0008 | 0.85 / 0.86 / 0.51 | 0.509 |  |  | 10/16 | -0.002 | +0.080 |  | +0.7 / +0.2 |  |
| MES | 15 | h1 | -0.005 | -0.015 .. +0.006 | -0.0018 | 0.37 / 0.38 / 0.38 | 0.388 |  |  | 9/16 | -0.006 | -0.004 |  | -0.9 / -0.9 |  |
| MES | 15 | h2 * | -0.011 | -0.026 .. +0.004 | -0.0028 | 0.15 / 0.15 / 0.16 | 0.166 | 1 | 1 | 9/16 | -0.030 | +0.007 | False | -1.4 / -1.4 |  |
| MES | 15 | h4 | -0.005 | -0.029 .. +0.020 | -0.0008 | 0.71 / 0.71 / 0.69 | 0.688 |  |  | 8/16 | -0.036 | +0.026 |  | -0.4 / -0.4 | 0.040 |
| MES | 15 | h8 | -0.006 | -0.045 .. +0.034 | -0.0007 | 0.78 / 0.78 / 0.72 | 0.718 |  |  | 8/16 | -0.053 | +0.041 |  | -0.4 / -0.3 |  |
| MES | 15 | h16 | +0.004 | -0.065 .. +0.072 | +0.0003 | 0.92 / 0.92 / 0.87 | 0.873 |  |  | 8/16 | -0.044 | +0.051 |  | +0.2 / +0.1 |  |
| MES | 15 | eod | +0.055 | -0.169 .. +0.279 | +0.0018 | 0.63 / 0.65 / 0.33 | 0.32 |  |  | 8/16 | -0.024 | +0.133 |  | +1.0 / +0.5 |  |
| MES | 60 | h1 | +0.007 | -0.014 .. +0.028 | +0.0026 | 0.51 / 0.54 / 0.55 | 0.556 |  |  | 9/16 | -0.011 | +0.025 |  | +0.6 / +0.7 |  |
| MES | 60 | h2 * | +0.022 | -0.009 .. +0.053 | +0.0059 | 0.16 / 0.18 / 0.17 | 0.173 | 1 | 1 | 9/16 | +0.012 | +0.033 | False | +1.3 / +1.4 |  |
| MES | 60 | h4 | +0.030 | -0.016 .. +0.076 | +0.0056 | 0.21 / 0.24 / 0.18 | 0.179 |  |  | 11/16 | -0.009 | +0.069 |  | +1.3 / +1.3 | 0.076 |
| MES | 60 | h8 | +0.016 | -0.049 .. +0.080 | +0.0021 | 0.63 / 0.65 / 0.59 | 0.574 |  |  | 9/16 | +0.007 | +0.024 |  | +0.5 / +0.5 |  |
| MES | 60 | h16 | +0.015 | -0.060 .. +0.090 | +0.0016 | 0.7 / 0.71 / 0.64 | 0.638 |  |  | 9/16 | -0.010 | +0.040 |  | +0.5 / +0.4 |  |
| MES | 60 | eod | +0.023 | -0.055 .. +0.101 | +0.0023 | 0.56 / 0.58 / 0.48 | 0.48 |  |  | 9/16 | +0.003 | +0.044 |  | +0.7 / +0.6 |  |
| MNQ | 5 | h1 * | +0.008 | +0.002 .. +0.014 | +0.0028 | 0.014 / 0.014 / 0.014 | 0.0141 | 1 | 0.945 | 12/16 | +0.010 | +0.006 | False | +2.5 / +2.5 |  |
| MNQ | 5 | h2 | +0.002 | -0.007 .. +0.012 | +0.0005 | 0.62 / 0.62 / 0.61 | 0.592 |  |  | 9/16 | -0.002 | +0.007 |  | +0.5 / +0.5 |  |
| MNQ | 5 | h4 | +0.006 | -0.008 .. +0.020 | +0.0009 | 0.39 / 0.42 / 0.42 | 0.416 |  |  | 11/16 | +0.002 | +0.010 |  | +0.9 / +0.9 | 0.021 |
| MNQ | 5 | h8 | +0.006 | -0.016 .. +0.028 | +0.0006 | 0.61 / 0.63 / 0.6 | 0.597 |  |  | 8/16 | -0.013 | +0.024 |  | +0.6 / +0.5 |  |
| MNQ | 5 | h16 | -0.009 | -0.048 .. +0.030 | -0.0006 | 0.64 / 0.66 / 0.6 | 0.614 |  |  | 8/16 | -0.038 | +0.019 |  | -0.7 / -0.5 |  |
| MNQ | 5 | eod | +0.199 | -0.398 .. +0.796 | +0.0029 | 0.51 / 0.53 / 0.024 | 0.0221 |  |  | 13/16 | +0.127 | +0.271 |  | +2.5 / +0.7 |  |
| MNQ | 15 | h1 * | +0.011 | -0.001 .. +0.022 | +0.0032 | 0.065 / 0.087 / 0.13 | 0.129 | 1 | 1 | 12/16 | +0.005 | +0.016 | False | +1.7 / +1.8 |  |
| MNQ | 15 | h2 | +0.015 | -0.003 .. +0.033 | +0.0027 | 0.11 / 0.11 / 0.2 | 0.187 |  |  | 11/16 | -0.003 | +0.032 |  | +1.7 / +1.6 |  |
| MNQ | 15 | h4 | +0.009 | -0.020 .. +0.039 | +0.0010 | 0.55 / 0.56 / 0.64 | 0.62 |  |  | 9/16 | -0.015 | +0.033 |  | +0.7 / +0.6 | 0.049 |
| MNQ | 15 | h8 | +0.009 | -0.039 .. +0.058 | +0.0008 | 0.71 / 0.71 / 0.7 | 0.703 |  |  | 7/16 | -0.022 | +0.040 |  | +0.5 / +0.4 |  |
| MNQ | 15 | h16 | +0.015 | -0.065 .. +0.096 | +0.0010 | 0.71 / 0.71 / 0.63 | 0.618 |  |  | 8/16 | -0.038 | +0.069 |  | +0.6 / +0.4 |  |
| MNQ | 15 | eod | +0.066 | -0.209 .. +0.341 | +0.0015 | 0.64 / 0.65 / 0.42 | 0.414 |  |  | 7/16 | -0.103 | +0.234 |  | +1.0 / +0.5 |  |
| MNQ | 60 | h1 | +0.028 | +0.003 .. +0.053 | +0.0101 | 0.029 / 0.042 / 0.031 | 0.0315 |  |  | 10/16 | +0.026 | +0.030 |  | +2.1 / +2.2 |  |
| MNQ | 60 | h2 * | +0.054 | +0.016 .. +0.093 | +0.0137 | 0.0052 / 0.0069 / 0.0021 | 0.00156 | 0.959 | 0.69 | 11/16 | +0.028 | +0.081 | False | +2.9 / +2.8 |  |
| MNQ | 60 | h4 | +0.071 | +0.017 .. +0.125 | +0.0126 | 0.01 / 0.013 / 0.0025 | 0.00156 |  |  | 10/16 | +0.019 | +0.123 |  | +2.8 / +2.6 | 0.080 |
| MNQ | 60 | h8 | +0.068 | -0.007 .. +0.142 | +0.0088 | 0.075 / 0.084 / 0.022 | 0.0224 |  |  | 10/16 | +0.041 | +0.094 |  | +2.2 / +1.8 |  |
| MNQ | 60 | h16 | +0.059 | -0.030 .. +0.148 | +0.0059 | 0.19 / 0.2 / 0.071 | 0.0669 |  |  | 10/16 | +0.014 | +0.104 |  | +1.7 / +1.3 |  |
| MNQ | 60 | eod | +0.063 | -0.027 .. +0.153 | +0.0060 | 0.17 / 0.18 / 0.061 | 0.062 |  |  | 10/16 | +0.018 | +0.107 |  | +1.8 / +1.4 |  |
| MYM | 5 | h1 | -0.005 | -0.014 .. +0.005 | -0.0014 | 0.34 / 0.31 / 0.54 | 0.543 |  |  | 5/8 | n/a | -0.005 |  | -1.0 / -1.0 |  |
| MYM | 5 | h2 * | -0.015 | -0.028 .. -0.002 | -0.0029 | 0.02 / 0.026 / 0.078 | 0.0801 | 1 | 0.969 | 6/8 | n/a | -0.015 | False | -2.4 / -2.3 |  |
| MYM | 5 | h4 | -0.015 | -0.036 .. +0.005 | -0.0018 | 0.15 / 0.15 / 0.34 | 0.339 |  |  | 6/8 | n/a | -0.015 |  | -1.7 / -1.5 | 0.036 |
| MYM | 5 | h8 | -0.020 | -0.056 .. +0.016 | -0.0017 | 0.28 / 0.26 / 0.32 | 0.331 |  |  | 6/8 | n/a | -0.020 |  | -1.5 / -1.1 |  |
| MYM | 5 | h16 | -0.038 | -0.094 .. +0.018 | -0.0025 | 0.18 / 0.2 / 0.13 | 0.138 |  |  | 6/8 | n/a | -0.038 |  | -2.0 / -1.3 |  |
| MYM | 5 | eod | +0.041 | -0.824 .. +0.906 | +0.0006 | 0.93 / 0.92 / 0.67 | 0.669 |  |  | 4/8 | n/a | +0.041 |  | +0.4 / +0.1 |  |
| MYM | 15 | h1 * | -0.014 | -0.031 .. +0.003 | -0.0042 | 0.11 / 0.1 / 0.18 | 0.177 | 1 | 1 | 5/8 | n/a | -0.014 | False | -1.6 / -1.6 |  |
| MYM | 15 | h2 | -0.014 | -0.041 .. +0.013 | -0.0024 | 0.31 / 0.28 / 0.44 | 0.409 |  |  | 5/8 | n/a | -0.014 |  | -1.1 / -1.0 |  |
| MYM | 15 | h4 | -0.013 | -0.052 .. +0.025 | -0.0014 | 0.5 / 0.5 / 0.63 | 0.612 |  |  | 5/8 | n/a | -0.013 |  | -0.8 / -0.7 | 0.068 |
| MYM | 15 | h8 | -0.018 | -0.085 .. +0.049 | -0.0014 | 0.59 / 0.59 / 0.59 | 0.577 |  |  | 6/8 | n/a | -0.018 |  | -0.7 / -0.5 |  |
| MYM | 15 | h16 | +0.003 | -0.108 .. +0.114 | +0.0002 | 0.96 / 0.96 / 0.95 | 0.951 |  |  | 3/8 | n/a | +0.003 |  | +0.1 / +0.1 |  |
| MYM | 15 | eod | +0.045 | -0.376 .. +0.465 | +0.0010 | 0.84 / 0.83 / 0.7 | 0.693 |  |  | 5/8 | n/a | +0.045 |  | +0.5 / +0.2 |  |
| MYM | 60 | h1 * | +0.009 | -0.025 .. +0.043 | +0.0031 | 0.62 / 0.63 / 0.62 | 0.619 | 1 | 1 | 5/8 | n/a | +0.009 | False | +0.5 / +0.5 |  |
| MYM | 60 | h2 | +0.002 | -0.051 .. +0.055 | +0.0005 | 0.94 / 0.94 / 0.94 | 0.938 |  |  | 5/8 | n/a | +0.002 |  | +0.1 / +0.1 |  |
| MYM | 60 | h4 | +0.014 | -0.062 .. +0.090 | +0.0025 | 0.72 / 0.74 / 0.68 | 0.669 |  |  | 3/8 | n/a | +0.014 |  | +0.4 / +0.4 | 0.109 |
| MYM | 60 | h8 | +0.022 | -0.079 .. +0.124 | +0.0030 | 0.66 / 0.68 / 0.59 | 0.594 |  |  | 5/8 | n/a | +0.022 |  | +0.5 / +0.4 |  |
| MYM | 60 | h16 | +0.008 | -0.111 .. +0.126 | +0.0008 | 0.9 / 0.9 / 0.87 | 0.882 |  |  | 4/8 | n/a | +0.008 |  | +0.2 / +0.1 |  |
| MYM | 60 | eod | +0.007 | -0.114 .. +0.129 | +0.0007 | 0.91 / 0.91 / 0.87 | 0.878 |  |  | 5/8 | n/a | +0.007 |  | +0.2 / +0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.020 | +0.016 .. +0.025 | +4.1% | +0.056 | 2.9e-20 | 1.56e-17 | 15/16 |
| MES | 5 | h2 | +0.022 | +0.016 .. +0.027 | +3.1% | +0.060 | 7.5e-13 |  | 15/16 |
| MES | 5 | h4 | +0.027 | +0.018 .. +0.035 | +2.7% | +0.068 | 1.2e-09 |  | 13/16 |
| MES | 5 | h8 | +0.033 | +0.021 .. +0.046 | +2.3% | +0.077 | 1.6e-07 |  | 12/16 |
| MES | 5 | h16 | +0.049 | +0.029 .. +0.068 | +2.3% | +0.098 | 1e-06 |  | 12/16 |
| MES | 5 | eod | +0.143 | -0.006 .. +0.293 | +1.4% | +0.351 | 0.06 |  | 11/16 |
| MES | 15 | h1 | +0.015 | +0.006 .. +0.024 | +2.9% | +0.053 | 0.021 |  | 11/16 |
| MES | 15 | h2 | +0.029 | +0.017 .. +0.041 | +4.0% | +0.067 | 6.1e-05 |  | 13/16 |
| MES | 15 | h4 * | +0.041 | +0.024 .. +0.059 | +3.9% | +0.080 | 8.2e-06 | 0.0019 | 15/16 |
| MES | 15 | h8 | +0.057 | +0.033 .. +0.082 | +3.7% | +0.093 | 0.0016 |  | 11/16 |
| MES | 15 | h16 | +0.075 | +0.038 .. +0.113 | +3.3% | +0.115 | 0.00049 |  | 12/16 |
| MES | 15 | eod | +0.031 | -0.092 .. +0.153 | +0.6% | +0.132 | 0.62 |  | 9/16 |
| MES | 60 | h1 | +0.015 | -0.003 .. +0.032 | +2.9% | +0.043 | 0.53 |  | 10/16 |
| MES | 60 | h2 * | +0.034 | +0.011 .. +0.057 | +4.6% | +0.056 | 0.073 | 1 | 12/16 |
| MES | 60 | h4 | +0.039 | +0.005 .. +0.073 | +3.7% | +0.055 | 0.098 |  | 9/16 |
| MES | 60 | h8 | +0.022 | -0.018 .. +0.062 | +1.5% | +0.039 | 0.4 |  | 8/16 |
| MES | 60 | h16 | +0.009 | -0.036 .. +0.054 | +0.5% | +0.023 | 0.69 |  | 9/16 |
| MES | 60 | eod | -0.001 | -0.047 .. +0.045 | -0.0% | +0.018 | 0.98 |  | 7/16 |
| MNQ | 5 | h1 * | +0.036 | +0.030 .. +0.043 | +6.8% | +0.080 | 3.1e-30 | 2.19e-27 | 14/16 |
| MNQ | 5 | h2 | +0.048 | +0.038 .. +0.058 | +6.2% | +0.097 | 5.7e-22 |  | 14/16 |
| MNQ | 5 | h4 | +0.070 | +0.054 .. +0.086 | +6.3% | +0.126 | 1.8e-17 |  | 14/16 |
| MNQ | 5 | h8 | +0.089 | +0.061 .. +0.116 | +5.5% | +0.160 | 2.8e-10 |  | 14/16 |
| MNQ | 5 | h16 | +0.133 | +0.084 .. +0.182 | +5.5% | +0.231 | 1.3e-07 |  | 14/16 |
| MNQ | 5 | eod | +0.531 | +0.240 .. +0.822 | +4.2% | +1.190 | 0.00035 |  | 13/16 |
| MNQ | 15 | h1 | +0.023 | +0.012 .. +0.033 | +4.3% | +0.050 | 0.02 |  | 11/16 |
| MNQ | 15 | h2 | +0.031 | +0.013 .. +0.048 | +3.9% | +0.055 | 0.032 |  | 11/16 |
| MNQ | 15 | h4 | +0.043 | +0.012 .. +0.075 | +3.8% | +0.074 | 0.1 |  | 13/16 |
| MNQ | 15 | h8 | +0.068 | +0.018 .. +0.119 | +4.1% | +0.101 | 0.013 |  | 13/16 |
| MNQ | 15 | h16 * | +0.090 | +0.030 .. +0.150 | +3.6% | +0.123 | 0.0059 | 0.844 | 11/16 |
| MNQ | 15 | eod | +0.084 | -0.118 .. +0.286 | +1.3% | +0.214 | 0.42 |  | 9/16 |
| MNQ | 60 | h1 | -0.000 | -0.020 .. +0.019 | -0.1% | +0.009 | 0.97 |  | 7/16 |
| MNQ | 60 | h2 | +0.022 | -0.002 .. +0.045 | +2.8% | +0.030 | 0.3 |  | 10/16 |
| MNQ | 60 | h4 * | +0.048 | +0.016 .. +0.081 | +4.4% | +0.046 | 0.0081 | 1 | 10/16 |
| MNQ | 60 | h8 | +0.037 | -0.003 .. +0.077 | +2.3% | +0.054 | 0.14 |  | 10/16 |
| MNQ | 60 | h16 | +0.050 | +0.002 .. +0.098 | +2.3% | +0.056 | 0.052 |  | 11/16 |
| MNQ | 60 | eod | +0.046 | -0.002 .. +0.093 | +2.0% | +0.051 | 0.076 |  | 11/16 |
| MYM | 5 | h1 * | +0.038 | +0.029 .. +0.046 | +7.1% | +0.090 | 4.8e-14 | 1.91e-11 | 8/8 |
| MYM | 5 | h2 | +0.044 | +0.032 .. +0.056 | +5.8% | +0.099 | 8.5e-13 |  | 7/8 |
| MYM | 5 | h4 | +0.051 | +0.029 .. +0.073 | +4.6% | +0.112 | 5.6e-06 |  | 7/8 |
| MYM | 5 | h8 | +0.068 | +0.029 .. +0.108 | +4.3% | +0.138 | 0.00061 |  | 7/8 |
| MYM | 5 | h16 | +0.079 | +0.024 .. +0.134 | +3.4% | +0.161 | 0.0047 |  | 7/8 |
| MYM | 5 | eod | +0.364 | +0.096 .. +0.633 | +3.1% | +0.724 | 0.0084 |  | 7/8 |
| MYM | 15 | h1 * | +0.027 | +0.014 .. +0.041 | +5.1% | +0.062 | 0.053 | 1 | 6/8 |
| MYM | 15 | h2 | +0.029 | +0.007 .. +0.050 | +3.8% | +0.067 | 0.11 |  | 6/8 |
| MYM | 15 | h4 | +0.025 | -0.011 .. +0.062 | +2.3% | +0.069 | 0.53 |  | 6/8 |
| MYM | 15 | h8 | +0.027 | -0.032 .. +0.086 | +1.7% | +0.072 | 0.97 |  | 5/8 |
| MYM | 15 | h16 | +0.006 | -0.085 .. +0.098 | +0.3% | +0.038 | 0.9 |  | 6/8 |
| MYM | 15 | eod | +0.024 | -0.217 .. +0.266 | +0.4% | +0.175 | 0.87 |  | 5/8 |
| MYM | 60 | h1 * | +0.038 | +0.007 .. +0.069 | +7.3% | +0.077 | 0.026 | 1 | 5/8 |
| MYM | 60 | h2 | +0.046 | +0.003 .. +0.088 | +6.1% | +0.094 | 0.16 |  | 5/8 |
| MYM | 60 | h4 | +0.049 | -0.003 .. +0.101 | +4.6% | +0.088 | 0.1 |  | 5/8 |
| MYM | 60 | h8 | +0.025 | -0.034 .. +0.085 | +1.6% | +0.067 | 0.74 |  | 4/8 |
| MYM | 60 | h16 | +0.039 | -0.027 .. +0.105 | +1.8% | +0.065 | 0.27 |  | 5/8 |
| MYM | 60 | eod | +0.018 | -0.052 .. +0.089 | +0.8% | +0.048 | 0.62 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.07 pts | -0.43 .. +0.29 | 0.7 |
| MES | 15 | -0.25 pts | -0.85 .. +0.36 | 0.45 |
| MES | 60 | +0.53 pts | -0.61 .. +1.67 | 0.37 |
| MNQ | 5 | -0.20 pts | -0.54 .. +0.15 | 0.29 |
| MNQ | 15 | +0.24 pts | -0.38 .. +0.87 | 0.45 |
| MNQ | 60 | +1.42 pts | +0.22 .. +2.61 | 0.02 |
| MYM | 5 | -0.45 pts | -0.96 .. +0.05 | 0.083 |
| MYM | 15 | -0.43 pts | -1.28 .. +0.42 | 0.33 |
| MYM | 60 | +0.66 pts | -0.97 .. +2.29 | 0.45 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 86726 | +0.013 | 0.392 | +0.12 | -3.38 | -3.46 | -3.27 | -3.47 |
| MES | 5 | h2 | event | against signal | 86726 | +0.017 | 0.392 | +0.17 | -3.33 | -3.42 | -3.21 | -3.45 |
| MES | 5 | h4 | event | with signal | 86726 | -0.002 | 0.392 | -0.00 | -3.50 | -3.48 | -3.54 | -3.41 |
| MES | 5 | h8 | event | against signal | 86726 | -0.007 | 0.392 | -0.11 | -3.61 | -3.54 | -3.71 | -3.62 |
| MES | 5 | h16 | event | against signal | 86726 | -0.027 | 0.392 | -0.21 | -3.71 | -3.65 | -3.78 | -3.58 |
| MES | 5 | eod | event | with signal | 86726 | +0.771 | 0.392 | +4.65 | +1.15 | +0.27 | +2.31 | -1.04 |
| MES | 15 | h1 | event | against signal | 25134 | +0.006 | 0.205 | +0.12 | -3.38 | -3.43 | -3.31 | -3.44 |
| MES | 15 | h2 | event | against signal | 25134 | +0.008 | 0.205 | +0.04 | -3.46 | -3.35 | -3.57 | -3.49 |
| MES | 15 | h4 | event | against signal | 25134 | -0.011 | 0.205 | -0.47 | -3.97 | -3.43 | -4.57 | -3.90 |
| MES | 15 | h8 | event | against signal | 25134 | -0.036 | 0.205 | -0.84 | -4.34 | -3.61 | -5.15 | -4.03 |
| MES | 15 | h16 | event | with signal | 25134 | +0.095 | 0.205 | +1.31 | -2.19 | -2.86 | -1.45 | -2.84 |
| MES | 15 | eod | event | with signal | 25134 | +0.390 | 0.205 | +4.63 | +1.13 | -0.06 | +2.44 | -0.39 |
| MES | 60 | h1 | event | with signal | 5720 | +0.019 | 0.097 | +0.68 | -2.82 | -3.38 | -2.27 | -3.12 |
| MES | 60 | h2 | event | with signal | 5720 | +0.048 | 0.097 | +1.60 | -1.90 | -2.62 | -1.19 | -2.52 |
| MES | 60 | h4 | event | with signal | 5720 | +0.075 | 0.097 | +3.07 | -0.43 | -2.50 | +1.62 | -1.52 |
| MES | 60 | h8 | event | with signal | 5720 | +0.087 | 0.097 | +4.02 | +0.52 | -1.06 | +2.07 | -1.03 |
| MES | 60 | h16 | event | with signal | 5720 | +0.110 | 0.097 | +6.12 | +2.62 | -0.44 | +5.64 | +0.79 |
| MES | 60 | eod | event | with signal | 5720 | +0.120 | 0.097 | +6.38 | +2.88 | -0.19 | +5.90 | +1.08 |
| MNQ | 5 | h1 | event | with signal | 83989 | +0.008 | 0.168 | +0.05 | -1.95 | -1.98 | -1.89 | -1.90 |
| MNQ | 5 | h2 | event | with signal | 83989 | +0.006 | 0.168 | +0.05 | -1.95 | -2.00 | -1.88 | -1.90 |
| MNQ | 5 | h4 | event | with signal | 83989 | +0.025 | 0.168 | +0.25 | -1.75 | -1.93 | -1.48 | -1.75 |
| MNQ | 5 | h8 | event | with signal | 83989 | +0.054 | 0.168 | +0.49 | -1.51 | -1.88 | -0.93 | -1.66 |
| MNQ | 5 | h16 | event | against signal | 83989 | -0.083 | 0.168 | -0.48 | -2.48 | -2.25 | -2.84 | -2.12 |
| MNQ | 5 | eod | event | with signal | 83989 | +1.238 | 0.168 | +6.65 | +4.65 | +1.53 | +9.53 | +3.08 |
| MNQ | 15 | h1 | event | with signal | 25091 | +0.015 | 0.085 | +0.39 | -1.61 | -1.86 | -1.30 | -1.63 |
| MNQ | 15 | h2 | event | with signal | 25091 | +0.027 | 0.085 | +0.67 | -1.33 | -1.79 | -0.76 | -1.42 |
| MNQ | 15 | h4 | event | with signal | 25091 | +0.039 | 0.085 | +1.03 | -0.97 | -1.73 | -0.03 | -1.30 |
| MNQ | 15 | h8 | event | with signal | 25091 | +0.076 | 0.085 | +1.83 | -0.17 | -1.57 | +1.58 | -0.99 |
| MNQ | 15 | h16 | event | with signal | 25091 | +0.124 | 0.085 | +2.64 | +0.64 | -1.27 | +3.04 | -0.12 |
| MNQ | 15 | eod | event | with signal | 25091 | +0.506 | 0.085 | +6.82 | +4.82 | +0.75 | +9.90 | +3.42 |
| MNQ | 60 | h1 | event | with signal | 5929 | +0.042 | 0.039 | +1.23 | -0.77 | -1.25 | -0.25 | -1.23 |
| MNQ | 60 | h2 | event | with signal | 5929 | +0.084 | 0.039 | +3.98 | +1.98 | -0.79 | +4.97 | +1.09 |
| MNQ | 60 | h4 | event | with signal | 5929 | +0.124 | 0.039 | +6.54 | +4.54 | -0.39 | +9.86 | +2.95 |
| MNQ | 60 | h8 | event | with signal | 5929 | +0.156 | 0.039 | +7.99 | +5.99 | +0.97 | +11.41 | +3.62 |
| MNQ | 60 | h16 | event | with signal | 5929 | +0.172 | 0.039 | +10.05 | +8.05 | +1.17 | +15.47 | +6.01 |
| MNQ | 60 | eod | event | with signal | 5929 | +0.179 | 0.039 | +10.43 | +8.43 | +1.20 | +16.24 | +6.57 |
| MYM | 5 | h1 | event | against signal | 38402 | +0.013 | 0.186 | +0.10 | -1.90 | +nan | -1.90 | -2.00 |
| MYM | 5 | h2 | event | against signal | 38402 | +0.025 | 0.186 | +0.21 | -1.79 | +nan | -1.79 | -1.90 |
| MYM | 5 | h4 | event | against signal | 38402 | +0.025 | 0.186 | +0.06 | -1.94 | +nan | -1.94 | -2.07 |
| MYM | 5 | h8 | event | against signal | 38402 | +0.024 | 0.186 | -0.03 | -2.03 | +nan | -2.03 | -2.08 |
| MYM | 5 | h16 | event | against signal | 38402 | +0.039 | 0.186 | +0.08 | -1.92 | +nan | -1.92 | -1.90 |
| MYM | 5 | eod | event | with signal | 38402 | +0.327 | 0.186 | +3.83 | +1.83 | +nan | +1.83 | +0.77 |
| MYM | 15 | h1 | event | against signal | 12219 | +0.019 | 0.103 | +0.23 | -1.77 | +nan | -1.77 | -1.88 |
| MYM | 15 | h2 | event | against signal | 12219 | +0.019 | 0.103 | +0.16 | -1.84 | +nan | -1.84 | -1.97 |
| MYM | 15 | h4 | event | against signal | 12219 | +0.008 | 0.103 | -0.25 | -2.25 | +nan | -2.25 | -2.19 |
| MYM | 15 | h8 | event | against signal | 12219 | +0.006 | 0.103 | -0.18 | -2.18 | +nan | -2.18 | -2.07 |
| MYM | 15 | h16 | event | with signal | 12219 | -0.000 | 0.103 | +0.29 | -1.71 | +nan | -1.71 | -1.51 |
| MYM | 15 | eod | event | with signal | 12219 | +0.159 | 0.103 | +3.66 | +1.66 | +nan | +1.66 | +1.43 |
| MYM | 60 | h1 | event | with signal | 2884 | +0.014 | 0.049 | +0.12 | -1.88 | +nan | -1.88 | -2.09 |
| MYM | 60 | h2 | event | with signal | 2884 | +0.009 | 0.049 | +0.39 | -1.61 | +nan | -1.61 | -1.82 |
| MYM | 60 | h4 | event | with signal | 2884 | +0.029 | 0.049 | +1.64 | -0.36 | +nan | -0.36 | -0.89 |
| MYM | 60 | h8 | event | with signal | 2884 | +0.053 | 0.049 | +3.49 | +1.49 | +nan | +1.49 | +0.43 |
| MYM | 60 | h16 | event | with signal | 2884 | +0.058 | 0.049 | +5.48 | +3.48 | +nan | +3.48 | +1.55 |
| MYM | 60 | eod | event | with signal | 2884 | +0.060 | 0.049 | +6.03 | +4.03 | +nan | +4.03 | +1.94 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.839 | -0.944 | -1.019 | -1.059 | -1.091 | +0.000 | -0.068 | -0.075 | -0.066 | -0.072 | -0.079 |
| MES | 15 | -0.982 | -1.080 | -1.176 | -1.228 | -1.264 | +0.000 | -0.027 | -0.034 | -0.027 | -0.026 | -0.014 |
| MES | 60 | -1.060 | -1.162 | -1.249 | -1.339 | -1.390 | +0.000 | +0.006 | +0.023 | +0.028 | -0.070 | +0.002 |
| MNQ | 5 | -1.015 | -1.125 | -1.204 | -1.242 | -1.263 | +0.000 | -0.022 | -0.028 | -0.018 | -0.008 | -0.010 |
| MNQ | 15 | -1.095 | -1.188 | -1.271 | -1.331 | -1.363 | +0.000 | +0.004 | +0.012 | +0.013 | +0.021 | +0.042 |
| MNQ | 60 | -1.113 | -1.252 | -1.322 | -1.412 | -1.453 | +0.000 | +0.029 | +0.055 | +0.073 | -0.014 | +0.014 |
| MYM | 5 | -1.003 | -1.119 | -1.212 | -1.260 | -1.289 | +0.000 | -0.021 | -0.031 | -0.028 | -0.027 | -0.046 |
| MYM | 15 | -1.068 | -1.150 | -1.261 | -1.327 | -1.362 | +0.000 | -0.013 | -0.010 | -0.002 | +0.000 | +0.058 |
| MYM | 60 | -1.131 | -1.252 | -1.340 | -1.429 | -1.478 | +0.000 | +0.010 | +0.005 | +0.018 | -0.023 | -0.027 |

## Calibration

- MES 5-min: 1036271 bars, 86726 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 25134 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 5720 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 83989 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 25091 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 5929 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 38402 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 12219 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 2884 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38706 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
