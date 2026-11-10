# Impact card: fam_continuation_short

bearish continuation patterns only (short side) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.011 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.017 R20 or more 80% of the time).
- MES 5-min size: the market moves 8% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.039 R20, CONFIRMED, q=8.08e-42, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.42 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.244 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.030 R20 over the next 2 bars (30 min), p=0.011; we would catch an effect of 0.040 R20 or more 80% of the time).
- MES 15-min size: the market moves 13% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.065 R20, CONFIRMED, q=2.81e-30, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.13 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.133 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.032 R20 over the next 1 bar (1 h), p=0.16; we would catch an effect of 0.077 R20 or more 80% of the time).
- MES 60-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.081 R20, CONFIRMED, q=1.55e-10, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.73 at recent bar sizes, 90% range up to $6.46); about 16.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.023 R20 over the next 4 bars (20 min), p=0.039; we would catch an effect of 0.021 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.065 R20, CONFIRMED, q=4.88e-102, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.57 at recent bar sizes, 90% range up to $1.31); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.026 R20 over the next 2 bars (30 min), p=0.13; we would catch an effect of 0.049 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 15% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.082 R20, CONFIRMED, q=7.29e-43, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.13 at recent bar sizes, 90% range up to $3.98); about 1405.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.037 R20 over the next 1 bar (1 h), p=0.14; we would catch an effect of 0.082 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.082 R20, CONFIRMED, q=7.27e-11, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.31 at recent bar sizes, 90% range up to $10.08); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.009 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.040 R20 or more 80% of the time).
- MYM 5-min size: the market moves 14% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.073 R20, CONFIRMED, q=1.11e-50, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.10 at recent bar sizes, 90% range up to $0.52); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.047 R20 over the next 4 bars (1 h), p=0.46; we would catch an effect of 0.069 R20 or more 80% of the time).
- MYM 15-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.087 R20, CONFIRMED, q=4.23e-18, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.92 at recent bar sizes, 90% range up to $1.72); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.048 R20 over the next 1 bar (1 h), p=0.17; we would catch an effect of 0.112 R20 or more 80% of the time).
- MYM 60-min size: the market moves 21% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.110 R20, CONFIRMED, q=5.28e-10, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.01 at recent bar sizes, 90% range up to $5.58); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.000 | -0.006 .. +0.006 | +0.0002 | 0.9 / 0.89 / 0.86 | 0.861 |  |  | 10/16 | -0.001 | +0.002 |  | +0.1 / +0.1 |  |
| MES | 5 | h2 | +0.004 | -0.005 .. +0.013 | +0.0014 | 0.33 / 0.32 / 0.2 | 0.211 |  |  | 10/16 | +0.000 | +0.009 |  | +1.1 / +1.0 |  |
| MES | 5 | h4 | +0.006 | -0.007 .. +0.018 | +0.0012 | 0.38 / 0.39 / 0.23 | 0.228 |  |  | 10/16 | +0.003 | +0.008 |  | +1.0 / +0.9 | 0.017 |
| MES | 5 | h8 * | +0.011 | -0.009 .. +0.032 | +0.0017 | 0.29 / 0.3 / 0.12 | 0.126 | 1 | 1 | 12/16 | +0.003 | +0.020 | False | +1.5 / +1.1 |  |
| MES | 5 | h16 | +0.014 | -0.022 .. +0.050 | +0.0015 | 0.44 / 0.46 / 0.2 | 0.203 |  |  | 9/16 | +0.003 | +0.025 |  | +1.3 / +0.8 |  |
| MES | 5 | eod | +0.051 | -0.396 .. +0.499 | +0.0010 | 0.82 / 0.83 / 0.45 | 0.467 |  |  | 8/16 | +0.187 | -0.083 |  | +0.9 / +0.2 |  |
| MES | 15 | h1 | +0.015 | +0.003 .. +0.028 | +0.0060 | 0.014 / 0.013 / 0.0045 | 0.00625 |  |  | 9/16 | +0.005 | +0.025 |  | +2.6 / +2.5 |  |
| MES | 15 | h2 * | +0.030 | +0.012 .. +0.048 | +0.0077 | 0.0014 / 0.0018 / 0.00018 | 0.00104 | 0.289 | 0.331 | 13/16 | +0.013 | +0.047 | False | +3.5 / +3.2 |  |
| MES | 15 | h4 | +0.036 | +0.007 .. +0.066 | +0.0063 | 0.015 / 0.02 / 0.0026 | 0.00391 |  |  | 9/16 | -0.000 | +0.073 |  | +3.0 / +2.4 | 0.040 |
| MES | 15 | h8 | +0.041 | -0.007 .. +0.088 | +0.0050 | 0.094 / 0.1 / 0.016 | 0.0177 |  |  | 10/16 | +0.022 | +0.059 |  | +2.4 / +1.7 |  |
| MES | 15 | h16 | +0.027 | -0.049 .. +0.102 | +0.0023 | 0.49 / 0.5 / 0.25 | 0.263 |  |  | 8/16 | -0.006 | +0.059 |  | +1.1 / +0.7 |  |
| MES | 15 | eod | +0.057 | -0.199 .. +0.314 | +0.0019 | 0.66 / 0.67 / 0.34 | 0.357 |  |  | 10/16 | +0.086 | +0.029 |  | +1.0 / +0.4 |  |
| MES | 60 | h1 * | +0.032 | +0.005 .. +0.058 | +0.0120 | 0.019 / 0.027 / 0.0086 | 0.00808 | 1 | 0.976 | 12/16 | +0.010 | +0.054 | False | +2.2 / +2.3 |  |
| MES | 60 | h2 | +0.031 | -0.010 .. +0.071 | +0.0082 | 0.14 / 0.15 / 0.066 | 0.0682 |  |  | 10/16 | +0.011 | +0.051 |  | +1.6 / +1.5 |  |
| MES | 60 | h4 | +0.038 | -0.022 .. +0.098 | +0.0071 | 0.21 / 0.22 / 0.11 | 0.111 |  |  | 10/16 | +0.018 | +0.058 |  | +1.5 / +1.2 | 0.077 |
| MES | 60 | h8 | +0.046 | -0.041 .. +0.133 | +0.0063 | 0.3 / 0.3 / 0.14 | 0.141 |  |  | 11/16 | +0.026 | +0.067 |  | +1.4 / +1.0 |  |
| MES | 60 | h16 | +0.011 | -0.093 .. +0.116 | +0.0012 | 0.83 / 0.83 / 0.76 | 0.762 |  |  | 11/16 | -0.011 | +0.034 |  | +0.3 / +0.2 |  |
| MES | 60 | eod | +0.029 | -0.081 .. +0.139 | +0.0029 | 0.61 / 0.61 / 0.45 | 0.444 |  |  | 9/16 | +0.001 | +0.057 |  | +0.8 / +0.5 |  |
| MNQ | 5 | h1 | +0.007 | +0.000 .. +0.014 | +0.0025 | 0.047 / 0.042 / 0.02 | 0.0219 |  |  | 11/16 | +0.002 | +0.013 |  | +2.1 / +2.0 |  |
| MNQ | 5 | h2 | +0.013 | +0.003 .. +0.024 | +0.0029 | 0.015 / 0.013 / 0.006 | 0.0104 |  |  | 12/16 | +0.005 | +0.021 |  | +2.8 / +2.4 |  |
| MNQ | 5 | h4 * | +0.023 | +0.007 .. +0.039 | +0.0033 | 0.0055 / 0.0065 / 0.002 | 0.0026 | 0.921 | 0.718 | 11/16 | +0.019 | +0.026 | False | +3.4 / +2.8 | 0.021 |
| MNQ | 5 | h8 | +0.030 | +0.003 .. +0.056 | +0.0029 | 0.029 / 0.033 / 0.0086 | 0.0109 |  |  | 11/16 | +0.039 | +0.021 |  | +3.1 / +2.2 |  |
| MNQ | 5 | h16 | +0.029 | -0.018 .. +0.077 | +0.0020 | 0.23 / 0.23 / 0.077 | 0.0828 |  |  | 9/16 | +0.032 | +0.026 |  | +2.1 / +1.2 |  |
| MNQ | 5 | eod | +0.031 | -0.571 .. +0.634 | +0.0004 | 0.92 / 0.92 / 0.78 | 0.779 |  |  | 8/16 | +0.099 | -0.036 |  | +0.4 / +0.1 |  |
| MNQ | 15 | h1 | +0.015 | +0.001 .. +0.029 | +0.0044 | 0.03 / 0.032 / 0.032 | 0.0401 |  |  | 11/16 | +0.005 | +0.025 |  | +2.2 / +2.2 |  |
| MNQ | 15 | h2 * | +0.026 | +0.005 .. +0.047 | +0.0046 | 0.017 / 0.021 / 0.028 | 0.0365 | 1 | 0.969 | 9/16 | +0.018 | +0.033 | False | +2.6 / +2.4 |  |
| MNQ | 15 | h4 | +0.038 | +0.005 .. +0.071 | +0.0040 | 0.024 / 0.036 / 0.061 | 0.069 |  |  | 13/16 | +0.032 | +0.043 |  | +2.7 / +2.3 | 0.049 |
| MNQ | 15 | h8 | +0.044 | -0.009 .. +0.098 | +0.0036 | 0.1 / 0.12 / 0.085 | 0.0873 |  |  | 12/16 | +0.054 | +0.035 |  | +2.2 / +1.6 |  |
| MNQ | 15 | h16 | +0.032 | -0.051 .. +0.116 | +0.0021 | 0.45 / 0.46 / 0.34 | 0.353 |  |  | 8/16 | +0.022 | +0.043 |  | +1.2 / +0.8 |  |
| MNQ | 15 | eod | +0.039 | -0.243 .. +0.321 | +0.0009 | 0.79 / 0.79 / 0.67 | 0.657 |  |  | 10/16 | +0.065 | +0.014 |  | +0.6 / +0.3 |  |
| MNQ | 60 | h1 * | +0.037 | +0.006 .. +0.067 | +0.0129 | 0.019 / 0.023 / 0.0052 | 0.00521 | 1 | 0.957 | 12/16 | +0.036 | +0.038 | False | +2.4 / +2.3 |  |
| MNQ | 60 | h2 | +0.047 | +0.003 .. +0.091 | +0.0116 | 0.035 / 0.039 / 0.0099 | 0.0115 |  |  | 13/16 | +0.045 | +0.049 |  | +2.2 / +2.1 |  |
| MNQ | 60 | h4 | +0.038 | -0.025 .. +0.101 | +0.0066 | 0.23 / 0.22 / 0.13 | 0.125 |  |  | 11/16 | +0.024 | +0.052 |  | +1.4 / +1.2 | 0.082 |
| MNQ | 60 | h8 | +0.040 | -0.045 .. +0.125 | +0.0051 | 0.35 / 0.36 / 0.22 | 0.222 |  |  | 8/16 | +0.035 | +0.045 |  | +1.2 / +0.9 |  |
| MNQ | 60 | h16 | +0.030 | -0.074 .. +0.134 | +0.0029 | 0.57 / 0.57 / 0.42 | 0.422 |  |  | 9/16 | +0.030 | +0.030 |  | +0.8 / +0.6 |  |
| MNQ | 60 | eod | +0.033 | -0.075 .. +0.141 | +0.0031 | 0.55 / 0.55 / 0.39 | 0.395 |  |  | 10/16 | +0.026 | +0.040 |  | +0.9 / +0.6 |  |
| MYM | 5 | h1 | +0.002 | -0.007 .. +0.011 | +0.0007 | 0.65 / 0.67 / 0.69 | 0.683 |  |  | 4/8 | n/a | +0.002 |  | +0.4 / +0.5 |  |
| MYM | 5 | h2 * | +0.009 | -0.005 .. +0.024 | +0.0018 | 0.21 / 0.24 / 0.22 | 0.216 | 1 | 1 | 6/8 | n/a | +0.009 | False | +1.4 / +1.2 |  |
| MYM | 5 | h4 | +0.009 | -0.013 .. +0.031 | +0.0010 | 0.44 / 0.46 / 0.55 | 0.55 |  |  | 5/8 | n/a | +0.009 |  | +0.9 / +0.8 | 0.040 |
| MYM | 5 | h8 | +0.006 | -0.032 .. +0.044 | +0.0005 | 0.76 / 0.77 / 0.73 | 0.725 |  |  | 4/8 | n/a | +0.006 |  | +0.4 / +0.3 |  |
| MYM | 5 | h16 | +0.021 | -0.044 .. +0.086 | +0.0014 | 0.53 / 0.56 / 0.38 | 0.369 |  |  | 5/8 | n/a | +0.021 |  | +1.1 / +0.6 |  |
| MYM | 5 | eod | -0.209 | -1.034 .. +0.616 | -0.0030 | 0.62 / 0.62 / 0.058 | 0.0632 |  |  | 5/8 | n/a | -0.209 |  | -2.0 / -0.5 |  |
| MYM | 15 | h1 | +0.013 | -0.005 .. +0.031 | +0.0039 | 0.17 / 0.17 / 0.21 | 0.2 |  |  | 5/8 | n/a | +0.013 |  | +1.3 / +1.4 |  |
| MYM | 15 | h2 | +0.021 | -0.010 .. +0.051 | +0.0036 | 0.18 / 0.19 / 0.24 | 0.246 |  |  | 6/8 | n/a | +0.021 |  | +1.6 / +1.3 |  |
| MYM | 15 | h4 * | +0.047 | -0.000 .. +0.094 | +0.0049 | 0.05 / 0.054 / 0.093 | 0.098 | 1 | 0.999 | 7/8 | n/a | +0.047 | False | +2.5 / +2.0 | 0.069 |
| MYM | 15 | h8 | +0.022 | -0.055 .. +0.099 | +0.0018 | 0.58 / 0.58 / 0.54 | 0.531 |  |  | 4/8 | n/a | +0.022 |  | +0.9 / +0.6 |  |
| MYM | 15 | h16 | +0.012 | -0.118 .. +0.142 | +0.0007 | 0.86 / 0.86 / 0.83 | 0.83 |  |  | 4/8 | n/a | +0.012 |  | +0.3 / +0.2 |  |
| MYM | 15 | eod | -0.012 | -0.430 .. +0.406 | -0.0003 | 0.96 / 0.96 / 0.92 | 0.924 |  |  | 3/8 | n/a | -0.012 |  | -0.1 / -0.1 |  |
| MYM | 60 | h1 * | +0.048 | +0.007 .. +0.089 | +0.0177 | 0.021 / 0.028 / 0.0055 | 0.00843 | 1 | 0.971 | 7/8 | n/a | +0.048 | False | +2.3 / +2.3 |  |
| MYM | 60 | h2 | +0.050 | -0.009 .. +0.110 | +0.0130 | 0.095 / 0.11 / 0.038 | 0.0432 |  |  | 6/8 | n/a | +0.050 |  | +1.8 / +1.7 |  |
| MYM | 60 | h4 | +0.047 | -0.042 .. +0.136 | +0.0087 | 0.3 / 0.3 / 0.17 | 0.179 |  |  | 5/8 | n/a | +0.047 |  | +1.3 / +1.0 | 0.112 |
| MYM | 60 | h8 | +0.020 | -0.105 .. +0.145 | +0.0027 | 0.76 / 0.75 / 0.66 | 0.64 |  |  | 4/8 | n/a | +0.020 |  | +0.4 / +0.3 |  |
| MYM | 60 | h16 | -0.030 | -0.171 .. +0.110 | -0.0031 | 0.67 / 0.68 / 0.55 | 0.543 |  |  | 4/8 | n/a | -0.030 |  | -0.6 / -0.4 |  |
| MYM | 60 | eod | -0.020 | -0.165 .. +0.125 | -0.0020 | 0.79 / 0.8 / 0.7 | 0.692 |  |  | 4/8 | n/a | -0.020 |  | -0.4 / -0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.039 | +0.034 .. +0.045 | +7.9% | +0.096 | 8.4e-45 | 8.08e-42 | 16/16 |
| MES | 5 | h2 | +0.048 | +0.040 .. +0.056 | +6.8% | +0.111 | 1.8e-32 |  | 14/16 |
| MES | 5 | h4 | +0.057 | +0.047 .. +0.068 | +5.7% | +0.131 | 8.6e-26 |  | 15/16 |
| MES | 5 | h8 | +0.077 | +0.063 .. +0.092 | +5.4% | +0.156 | 1.4e-25 |  | 15/16 |
| MES | 5 | h16 | +0.101 | +0.080 .. +0.123 | +4.8% | +0.197 | 1.2e-20 |  | 14/16 |
| MES | 5 | eod | +0.227 | +0.067 .. +0.387 | +2.3% | +0.527 | 0.0054 |  | 14/16 |
| MES | 15 | h1 * | +0.065 | +0.054 .. +0.075 | +12.7% | +0.153 | 3.5e-33 | 2.81e-30 | 16/16 |
| MES | 15 | h2 | +0.082 | +0.067 .. +0.097 | +11.3% | +0.192 | 1.9e-27 |  | 16/16 |
| MES | 15 | h4 | +0.104 | +0.083 .. +0.125 | +9.9% | +0.229 | 1.6e-21 |  | 16/16 |
| MES | 15 | h8 | +0.129 | +0.100 .. +0.159 | +8.4% | +0.254 | 2.5e-17 |  | 16/16 |
| MES | 15 | h16 | +0.133 | +0.088 .. +0.177 | +5.8% | +0.290 | 4.6e-09 |  | 15/16 |
| MES | 15 | eod | +0.127 | -0.002 .. +0.256 | +2.3% | +0.356 | 0.053 |  | 12/16 |
| MES | 60 | h1 * | +0.081 | +0.059 .. +0.103 | +15.9% | +0.206 | 4.1e-13 | 1.55e-10 | 13/16 |
| MES | 60 | h2 | +0.097 | +0.068 .. +0.126 | +13.1% | +0.243 | 5.3e-11 |  | 15/16 |
| MES | 60 | h4 | +0.125 | +0.087 .. +0.163 | +11.8% | +0.283 | 1.2e-10 |  | 14/16 |
| MES | 60 | h8 | +0.133 | +0.086 .. +0.179 | +8.8% | +0.312 | 4.2e-08 |  | 16/16 |
| MES | 60 | h16 | +0.113 | +0.062 .. +0.165 | +5.5% | +0.285 | 1.6e-05 |  | 14/16 |
| MES | 60 | eod | +0.116 | +0.062 .. +0.170 | +5.4% | +0.289 | 2.9e-05 |  | 14/16 |
| MNQ | 5 | h1 * | +0.065 | +0.059 .. +0.071 | +12.1% | +0.135 | 3.4e-105 | 4.88e-102 | 16/16 |
| MNQ | 5 | h2 | +0.082 | +0.073 .. +0.090 | +10.6% | +0.168 | 3e-78 |  | 16/16 |
| MNQ | 5 | h4 | +0.101 | +0.087 .. +0.115 | +9.1% | +0.212 | 9.7e-45 |  | 16/16 |
| MNQ | 5 | h8 | +0.142 | +0.115 .. +0.169 | +8.8% | +0.278 | 3.9e-25 |  | 15/16 |
| MNQ | 5 | h16 | +0.185 | +0.138 .. +0.232 | +7.7% | +0.356 | 1.9e-14 |  | 15/16 |
| MNQ | 5 | eod | +0.700 | +0.415 .. +0.985 | +5.6% | +1.437 | 1.5e-06 |  | 14/16 |
| MNQ | 15 | h1 * | +0.082 | +0.070 .. +0.093 | +15.3% | +0.174 | 7.4e-46 | 7.29e-43 | 15/16 |
| MNQ | 15 | h2 | +0.106 | +0.087 .. +0.124 | +13.6% | +0.221 | 3.9e-27 |  | 15/16 |
| MNQ | 15 | h4 | +0.126 | +0.093 .. +0.159 | +11.1% | +0.264 | 5.6e-14 |  | 14/16 |
| MNQ | 15 | h8 | +0.154 | +0.102 .. +0.206 | +9.2% | +0.301 | 5.8e-09 |  | 15/16 |
| MNQ | 15 | h16 | +0.176 | +0.113 .. +0.239 | +7.0% | +0.342 | 4e-08 |  | 15/16 |
| MNQ | 15 | eod | +0.174 | -0.030 .. +0.379 | +2.7% | +0.434 | 0.095 |  | 13/16 |
| MNQ | 60 | h1 * | +0.082 | +0.060 .. +0.104 | +15.6% | +0.202 | 1.9e-13 | 7.27e-11 | 14/16 |
| MNQ | 60 | h2 | +0.100 | +0.068 .. +0.131 | +13.0% | +0.236 | 3.8e-10 |  | 15/16 |
| MNQ | 60 | h4 | +0.104 | +0.066 .. +0.141 | +9.4% | +0.260 | 1.2e-07 |  | 14/16 |
| MNQ | 60 | h8 | +0.101 | +0.055 .. +0.147 | +6.4% | +0.282 | 2.1e-05 |  | 16/16 |
| MNQ | 60 | h16 | +0.098 | +0.045 .. +0.150 | +4.5% | +0.290 | 0.00032 |  | 13/16 |
| MNQ | 60 | eod | +0.098 | +0.045 .. +0.150 | +4.2% | +0.290 | 0.00043 |  | 13/16 |
| MYM | 5 | h1 * | +0.073 | +0.064 .. +0.082 | +13.7% | +0.153 | 1e-53 | 1.11e-50 | 8/8 |
| MYM | 5 | h2 | +0.090 | +0.077 .. +0.102 | +11.8% | +0.188 | 1.7e-41 |  | 8/8 |
| MYM | 5 | h4 | +0.106 | +0.083 .. +0.128 | +9.6% | +0.221 | 1.8e-18 |  | 8/8 |
| MYM | 5 | h8 | +0.131 | +0.092 .. +0.171 | +8.3% | +0.267 | 5.2e-11 |  | 7/8 |
| MYM | 5 | h16 | +0.176 | +0.120 .. +0.232 | +7.5% | +0.320 | 6.2e-10 |  | 7/8 |
| MYM | 5 | eod | +0.553 | +0.277 .. +0.829 | +4.7% | +1.039 | 8.6e-05 |  | 7/8 |
| MYM | 15 | h1 * | +0.087 | +0.071 .. +0.103 | +16.4% | +0.178 | 7.6e-21 | 4.23e-18 | 8/8 |
| MYM | 15 | h2 | +0.105 | +0.080 .. +0.131 | +13.8% | +0.214 | 3.7e-08 |  | 8/8 |
| MYM | 15 | h4 | +0.116 | +0.073 .. +0.160 | +10.4% | +0.236 | 0.00017 |  | 6/8 |
| MYM | 15 | h8 | +0.116 | +0.056 .. +0.176 | +7.1% | +0.244 | 0.0014 |  | 7/8 |
| MYM | 15 | h16 | +0.150 | +0.042 .. +0.258 | +6.1% | +0.263 | 0.018 |  | 7/8 |
| MYM | 15 | eod | +0.192 | -0.058 .. +0.443 | +3.2% | +0.426 | 0.19 |  | 6/8 |
| MYM | 60 | h1 * | +0.110 | +0.081 .. +0.139 | +21.0% | +0.225 | 1.4e-12 | 5.28e-10 | 8/8 |
| MYM | 60 | h2 | +0.116 | +0.079 .. +0.153 | +15.4% | +0.263 | 7.1e-09 |  | 7/8 |
| MYM | 60 | h4 | +0.130 | +0.076 .. +0.185 | +12.1% | +0.286 | 3.9e-06 |  | 7/8 |
| MYM | 60 | h8 | +0.161 | +0.098 .. +0.224 | +10.4% | +0.347 | 4.8e-06 |  | 8/8 |
| MYM | 60 | h16 | +0.135 | +0.061 .. +0.210 | +6.4% | +0.313 | 0.00039 |  | 7/8 |
| MYM | 60 | eod | +0.126 | +0.048 .. +0.204 | +5.7% | +0.314 | 0.0017 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.01 pts | -0.34 .. +0.35 | 0.96 |
| MES | 15 | +0.85 pts | +0.22 .. +1.48 | 0.012 |
| MES | 60 | +1.91 pts | +0.69 .. +3.12 | 0.0023 |
| MNQ | 5 | +0.05 pts | -0.33 .. +0.42 | 0.82 |
| MNQ | 15 | +0.79 pts | +0.13 .. +1.45 | 0.019 |
| MNQ | 60 | +1.76 pts | +0.57 .. +2.95 | 0.0044 |
| MYM | 5 | -0.04 pts | -0.52 .. +0.43 | 0.86 |
| MYM | 15 | +0.41 pts | -0.51 .. +1.33 | 0.39 |
| MYM | 60 | +1.53 pts | -0.08 .. +3.14 | 0.066 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 87764 | -0.013 | 0.384 | -0.09 | -3.59 | -3.60 | -3.58 | -3.49 |
| MES | 5 | h2 | event | with signal | 87764 | -0.018 | 0.384 | -0.16 | -3.66 | -3.64 | -3.67 | -3.49 |
| MES | 5 | h4 | event | with signal | 87764 | -0.025 | 0.384 | -0.19 | -3.69 | -3.65 | -3.74 | -3.49 |
| MES | 5 | h8 | event | with signal | 87764 | -0.032 | 0.384 | -0.22 | -3.72 | -3.74 | -3.70 | -3.46 |
| MES | 5 | h16 | event | with signal | 87764 | -0.061 | 0.384 | -0.37 | -3.87 | -3.88 | -3.86 | -3.44 |
| MES | 5 | eod | event | with signal | 87764 | -0.664 | 0.384 | -3.83 | -7.33 | -6.51 | -8.36 | -5.27 |
| MES | 15 | h1 | event | with signal | 25091 | +0.000 | 0.201 | +0.15 | -3.35 | -3.58 | -3.11 | -3.12 |
| MES | 15 | h2 | event | with signal | 25091 | +0.008 | 0.201 | +0.22 | -3.28 | -3.54 | -3.00 | -2.97 |
| MES | 15 | h4 | event | with signal | 25091 | +0.002 | 0.201 | +0.39 | -3.11 | -3.70 | -2.47 | -2.69 |
| MES | 15 | h8 | event | with signal | 25091 | -0.022 | 0.201 | +0.06 | -3.44 | -3.89 | -2.96 | -2.75 |
| MES | 15 | h16 | event | with signal | 25091 | -0.083 | 0.201 | -0.93 | -4.43 | -4.63 | -4.22 | -3.45 |
| MES | 15 | eod | event | with signal | 25091 | -0.240 | 0.201 | -2.27 | -5.77 | -6.14 | -5.39 | -4.86 |
| MES | 60 | h1 | event | with signal | 5730 | +0.020 | 0.094 | +0.84 | -2.66 | -3.38 | -1.96 | -2.32 |
| MES | 60 | h2 | event | with signal | 5730 | +0.003 | 0.094 | +0.38 | -3.12 | -3.55 | -2.71 | -2.31 |
| MES | 60 | h4 | event | with signal | 5730 | -0.014 | 0.094 | -0.83 | -4.33 | -4.29 | -4.35 | -2.87 |
| MES | 60 | h8 | event | with signal | 5730 | -0.035 | 0.094 | -1.49 | -4.99 | -4.57 | -5.38 | -2.91 |
| MES | 60 | h16 | event | with signal | 5730 | -0.073 | 0.094 | -2.96 | -6.46 | -5.63 | -7.25 | -4.80 |
| MES | 60 | eod | event | with signal | 5730 | -0.067 | 0.094 | -2.24 | -5.74 | -5.69 | -5.79 | -3.75 |
| MNQ | 5 | h1 | event | with signal | 83799 | -0.002 | 0.161 | +0.07 | -1.93 | -2.05 | -1.76 | -1.87 |
| MNQ | 5 | h2 | event | with signal | 83799 | -0.006 | 0.161 | +0.04 | -1.96 | -2.08 | -1.79 | -1.84 |
| MNQ | 5 | h4 | event | with signal | 83799 | -0.005 | 0.161 | +0.10 | -1.90 | -2.05 | -1.68 | -1.80 |
| MNQ | 5 | h8 | event | with signal | 83799 | -0.013 | 0.161 | +0.07 | -1.93 | -2.10 | -1.67 | -1.84 |
| MNQ | 5 | h16 | event | with signal | 83799 | -0.050 | 0.161 | -0.05 | -2.05 | -2.27 | -1.74 | -1.83 |
| MNQ | 5 | eod | event | with signal | 83799 | -0.927 | 0.161 | -4.01 | -6.01 | -4.88 | -7.67 | -5.34 |
| MNQ | 15 | h1 | event | with signal | 24785 | +0.004 | 0.083 | +0.32 | -1.68 | -2.05 | -1.25 | -1.46 |
| MNQ | 15 | h2 | event | with signal | 24785 | +0.010 | 0.083 | +0.29 | -1.71 | -1.99 | -1.37 | -1.51 |
| MNQ | 15 | h4 | event | with signal | 24785 | +0.008 | 0.083 | +0.46 | -1.54 | -2.01 | -0.98 | -1.17 |
| MNQ | 15 | h8 | event | with signal | 24785 | -0.013 | 0.083 | -0.06 | -2.06 | -2.18 | -1.92 | -1.41 |
| MNQ | 15 | h16 | event | with signal | 24785 | -0.070 | 0.083 | -0.84 | -2.84 | -2.73 | -2.96 | -2.16 |
| MNQ | 15 | eod | event | with signal | 24785 | -0.344 | 0.083 | -2.09 | -4.09 | -4.63 | -3.45 | -3.93 |
| MNQ | 60 | h1 | event | with signal | 5648 | +0.025 | 0.037 | +1.34 | -0.66 | -1.29 | -0.02 | -0.32 |
| MNQ | 60 | h2 | event | with signal | 5648 | +0.018 | 0.037 | +1.05 | -0.95 | -1.34 | -0.55 | +0.04 |
| MNQ | 60 | h4 | event | with signal | 5648 | -0.016 | 0.037 | -0.47 | -2.47 | -2.46 | -2.49 | -0.63 |
| MNQ | 60 | h8 | event | with signal | 5648 | -0.049 | 0.037 | -1.20 | -3.20 | -2.73 | -3.68 | -0.53 |
| MNQ | 60 | h16 | event | with signal | 5648 | -0.070 | 0.037 | -2.44 | -4.44 | -3.23 | -5.67 | -2.70 |
| MNQ | 60 | eod | event | with signal | 5648 | -0.076 | 0.037 | -1.97 | -3.97 | -3.40 | -4.56 | -2.00 |
| MYM | 5 | h1 | event | with signal | 39108 | -0.004 | 0.185 | -0.03 | -2.03 | +nan | -2.03 | -1.97 |
| MYM | 5 | h2 | event | with signal | 39108 | +0.001 | 0.185 | -0.05 | -2.05 | +nan | -2.05 | -1.97 |
| MYM | 5 | h4 | event | with signal | 39108 | +0.000 | 0.185 | -0.06 | -2.06 | +nan | -2.06 | -2.00 |
| MYM | 5 | h8 | event | with signal | 39108 | -0.007 | 0.185 | -0.26 | -2.26 | +nan | -2.26 | -2.16 |
| MYM | 5 | h16 | event | with signal | 39108 | -0.003 | 0.185 | -0.12 | -2.12 | +nan | -2.12 | -1.86 |
| MYM | 5 | eod | event | against signal | 39108 | +0.520 | 0.185 | +4.48 | +2.48 | +nan | +2.48 | +1.21 |
| MYM | 15 | h1 | event | with signal | 12373 | +0.007 | 0.101 | +0.16 | -1.84 | +nan | -1.84 | -1.75 |
| MYM | 15 | h2 | event | with signal | 12373 | +0.016 | 0.101 | +0.25 | -1.75 | +nan | -1.75 | -1.70 |
| MYM | 15 | h4 | event | with signal | 12373 | +0.038 | 0.101 | +0.76 | -1.24 | +nan | -1.24 | -1.14 |
| MYM | 15 | h8 | event | with signal | 12373 | +0.009 | 0.101 | -0.04 | -2.04 | +nan | -2.04 | -1.91 |
| MYM | 15 | h16 | event | with signal | 12373 | +0.025 | 0.101 | -0.36 | -2.36 | +nan | -2.36 | -2.77 |
| MYM | 15 | eod | event | against signal | 12373 | +0.103 | 0.101 | +2.39 | +0.39 | +nan | +0.39 | +0.52 |
| MYM | 60 | h1 | event | with signal | 2968 | +0.045 | 0.048 | +1.29 | -0.71 | +nan | -0.71 | -0.57 |
| MYM | 60 | h2 | event | with signal | 2968 | +0.036 | 0.048 | +0.66 | -1.34 | +nan | -1.34 | -0.76 |
| MYM | 60 | h4 | event | with signal | 2968 | +0.024 | 0.048 | -0.50 | -2.50 | +nan | -2.50 | -1.52 |
| MYM | 60 | h8 | event | with signal | 2968 | -0.018 | 0.048 | -3.06 | -5.06 | +nan | -5.06 | -3.51 |
| MYM | 60 | h16 | event | against signal | 2968 | +0.051 | 0.048 | +4.99 | +2.99 | +nan | +2.99 | +1.99 |
| MYM | 60 | eod | event | against signal | 2968 | +0.047 | 0.048 | +4.54 | +2.54 | +nan | +2.54 | +1.17 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.062 | -1.135 | -1.141 | -1.124 | -1.119 | +0.000 | -0.063 | -0.064 | -0.065 | -0.061 | -0.067 |
| MES | 15 | -1.276 | -1.386 | -1.399 | -1.348 | -1.322 | +0.000 | -0.011 | +0.002 | +0.005 | -0.001 | -0.037 |
| MES | 60 | -1.620 | -1.622 | -1.654 | -1.599 | -1.525 | +0.000 | +0.030 | +0.022 | +0.026 | -0.066 | -0.051 |
| MNQ | 5 | -1.252 | -1.341 | -1.346 | -1.321 | -1.301 | +0.000 | -0.027 | -0.026 | -0.018 | -0.010 | -0.019 |
| MNQ | 15 | -1.377 | -1.494 | -1.517 | -1.473 | -1.432 | +0.000 | +0.001 | +0.011 | +0.022 | +0.021 | -0.021 |
| MNQ | 60 | -1.665 | -1.692 | -1.711 | -1.695 | -1.625 | +0.000 | +0.037 | +0.041 | +0.030 | -0.098 | +0.077 |
| MYM | 5 | -1.252 | -1.358 | -1.370 | -1.343 | -1.320 | +0.000 | -0.019 | -0.016 | -0.025 | -0.035 | -0.032 |
| MYM | 15 | -1.346 | -1.474 | -1.491 | -1.455 | -1.416 | +0.000 | -0.004 | +0.002 | +0.027 | -0.011 | -0.047 |
| MYM | 60 | -1.547 | -1.617 | -1.664 | -1.655 | -1.575 | +0.000 | +0.051 | +0.056 | +0.058 | -0.047 | -0.043 |

## Calibration

- MES 5-min: 1036271 bars, 87764 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 25091 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 5730 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 83799 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 24785 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 5648 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 39108 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 12373 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 2968 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36786 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
