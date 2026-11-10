# Impact card: pat_pin_bar

candle pattern pin_bar in its textbook direction: range >= avgR10 and one shadow >= 2/3 of range: long lower shadow bullish, long upper bearish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.017 R20 over the next 4 bars (20 min), p=0.12; we would catch an effect of 0.019 R20 or more 80% of the time).
- MES 5-min size: the market moves 6% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.031 R20, CONFIRMED, q=2.29e-27, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.35 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.281 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.022 R20 over the next 1 bar (15 min), p=0.03; we would catch an effect of 0.043 R20 or more 80% of the time).
- MES 15-min size: the market moves 8% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.042 R20, CONFIRMED, q=5.45e-10, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.28 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.148 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.068 R20 over the next 4 bars (4 h), p=0.25; we would catch an effect of 0.088 R20 or more 80% of the time).
- MES 60-min size: the market moves 15% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.076 R20, CONFIRMED, q=6.85e-07, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.56 at recent bar sizes, 90% range up to $6.66); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.009 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.025 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.038 R20, CONFIRMED, q=2.54e-21, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.71 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.091 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.007 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.062 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 9% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.046 R20, CONFIRMED, q=0.0246, 13 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.27 at recent bar sizes, 90% range up to $2.73); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.058 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.100 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 10% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.054 R20, CONFIRMED, q=0.0247, 12 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.99 at recent bar sizes, 90% range up to $12.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.121 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.044 R20 or more 80% of the time).
- MYM 5-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.038 R20, CONFIRMED, q=4.47e-05, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.75 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.203 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.038 R20 over the next 1 bar (15 min), p=0.33; we would catch an effect of 0.078 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.074).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.70 at recent bar sizes, 90% range up to $2.52); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.039 R20 over the next 1 bar (1 h), p=0.88; we would catch an effect of 0.132 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.32).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.52 at recent bar sizes, 90% range up to $7.23); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.005 | -0.013 .. +0.002 | -0.0017 | 0.13 / 0.13 / 0.12 | 0.111 |  |  | 10/16 | -0.019 | +0.008 |  | -1.5 / -1.5 |  |
| MES | 5 | h2 | -0.012 | -0.022 .. -0.001 | -0.0024 | 0.025 / 0.02 / 0.021 | 0.0227 |  |  | 12/16 | -0.025 | +0.002 |  | -2.3 / -2.2 |  |
| MES | 5 | h4 * | -0.017 | -0.031 .. -0.003 | -0.0024 | 0.02 / 0.016 / 0.02 | 0.0188 | 1 | 0.978 | 11/16 | -0.031 | -0.002 | False | -2.4 / -2.3 | 0.019 |
| MES | 5 | h8 | -0.011 | -0.031 .. +0.009 | -0.0011 | 0.28 / 0.27 / 0.3 | 0.289 |  |  | 11/16 | -0.028 | +0.006 |  | -1.1 / -1.1 |  |
| MES | 5 | h16 | +0.011 | -0.018 .. +0.040 | +0.0008 | 0.46 / 0.46 / 0.47 | 0.466 |  |  | 9/16 | -0.010 | +0.032 |  | +0.7 / +0.7 |  |
| MES | 5 | eod | -0.067 | -0.229 .. +0.095 | -0.0009 | 0.42 / 0.43 / 0.42 | 0.422 |  |  | 10/16 | -0.186 | +0.050 |  | -0.9 / -0.8 |  |
| MES | 15 | h1 * | -0.022 | -0.037 .. -0.007 | -0.0058 | 0.005 / 0.0045 / 0.004 | 0.00495 | 0.728 | 0.722 | 13/16 | -0.007 | -0.036 | False | -2.8 / -2.8 |  |
| MES | 15 | h2 | -0.003 | -0.024 .. +0.019 | -0.0005 | 0.79 / 0.79 / 0.79 | 0.797 |  |  | 8/16 | +0.011 | -0.017 |  | -0.3 / -0.3 |  |
| MES | 15 | h4 | -0.002 | -0.034 .. +0.030 | -0.0002 | 0.91 / 0.91 / 0.91 | 0.912 |  |  | 8/16 | +0.015 | -0.019 |  | -0.1 / -0.1 | 0.043 |
| MES | 15 | h8 | -0.014 | -0.062 .. +0.033 | -0.0012 | 0.55 / 0.53 / 0.54 | 0.529 |  |  | 9/16 | -0.000 | -0.028 |  | -0.6 / -0.6 |  |
| MES | 15 | h16 | -0.036 | -0.101 .. +0.028 | -0.0022 | 0.27 / 0.28 / 0.25 | 0.25 |  |  | 9/16 | -0.014 | -0.059 |  | -1.1 / -1.1 |  |
| MES | 15 | eod | +0.023 | -0.127 .. +0.173 | +0.0004 | 0.76 / 0.77 / 0.79 | 0.79 |  |  | 8/16 | -0.009 | +0.055 |  | +0.3 / +0.3 |  |
| MES | 60 | h1 | -0.021 | -0.057 .. +0.015 | -0.0055 | 0.26 / 0.26 / 0.18 | 0.187 |  |  | 9/16 | -0.035 | -0.007 |  | -1.1 / -1.1 |  |
| MES | 60 | h2 | -0.048 | -0.098 .. +0.002 | -0.0088 | 0.062 / 0.056 / 0.027 | 0.0237 |  |  | 9/16 | -0.095 | -0.001 |  | -1.9 / -1.9 |  |
| MES | 60 | h4 * | -0.068 | -0.134 .. -0.003 | -0.0090 | 0.042 / 0.041 / 0.024 | 0.0255 | 1 | 0.998 | 11/16 | -0.145 | +0.008 | False | -2.0 / -2.0 | 0.088 |
| MES | 60 | h8 | -0.050 | -0.143 .. +0.042 | -0.0048 | 0.29 / 0.27 / 0.23 | 0.221 |  |  | 11/16 | -0.166 | +0.065 |  | -1.1 / -1.1 |  |
| MES | 60 | h16 | -0.082 | -0.185 .. +0.021 | -0.0059 | 0.12 / 0.11 / 0.077 | 0.0821 |  |  | 12/16 | -0.196 | +0.031 |  | -1.7 / -1.6 |  |
| MES | 60 | eod | -0.081 | -0.183 .. +0.022 | -0.0056 | 0.12 / 0.11 / 0.083 | 0.0844 |  |  | 12/16 | -0.198 | +0.037 |  | -1.6 / -1.5 |  |
| MNQ | 5 | h1 | -0.001 | -0.011 .. +0.008 | -0.0003 | 0.78 / 0.77 / 0.73 | 0.717 |  |  | 10/16 | -0.009 | +0.007 |  | -0.3 / -0.3 |  |
| MNQ | 5 | h2 * | -0.009 | -0.022 .. +0.005 | -0.0012 | 0.2 / 0.19 / 0.22 | 0.201 | 1 | 1 | 11/16 | -0.014 | -0.004 | False | -1.3 / -1.3 |  |
| MNQ | 5 | h4 | +0.003 | -0.016 .. +0.022 | +0.0002 | 0.78 / 0.78 / 0.82 | 0.805 |  |  | 11/16 | +0.009 | -0.004 |  | +0.3 / +0.3 | 0.025 |
| MNQ | 5 | h8 | +0.010 | -0.017 .. +0.037 | +0.0006 | 0.46 / 0.47 / 0.55 | 0.543 |  |  | 11/16 | +0.015 | +0.005 |  | +0.7 / +0.7 |  |
| MNQ | 5 | h16 | +0.018 | -0.019 .. +0.056 | +0.0008 | 0.34 / 0.35 / 0.44 | 0.435 |  |  | 11/16 | +0.020 | +0.017 |  | +0.9 / +1.0 |  |
| MNQ | 5 | eod | +0.035 | -0.185 .. +0.254 | +0.0003 | 0.76 / 0.77 / 0.78 | 0.774 |  |  | 8/16 | -0.077 | +0.145 |  | +0.3 / +0.3 |  |
| MNQ | 15 | h1 * | -0.007 | -0.026 .. +0.013 | -0.0013 | 0.5 / 0.48 / 0.52 | 0.471 | 1 | 1 | 10/16 | -0.010 | -0.003 | False | -0.7 / -0.7 |  |
| MNQ | 15 | h2 | +0.018 | -0.010 .. +0.046 | +0.0021 | 0.21 / 0.2 / 0.32 | 0.277 |  |  | 11/16 | +0.028 | +0.008 |  | +1.3 / +1.2 |  |
| MNQ | 15 | h4 | +0.018 | -0.025 .. +0.061 | +0.0012 | 0.42 / 0.4 / 0.55 | 0.498 |  |  | 9/16 | +0.020 | +0.016 |  | +0.9 / +0.8 | 0.062 |
| MNQ | 15 | h8 | +0.021 | -0.036 .. +0.078 | +0.0011 | 0.47 / 0.46 / 0.56 | 0.556 |  |  | 10/16 | +0.007 | +0.035 |  | +0.8 / +0.7 |  |
| MNQ | 15 | h16 | +0.002 | -0.078 .. +0.081 | +0.0001 | 0.96 / 0.96 / 0.97 | 0.97 |  |  | 10/16 | -0.002 | +0.006 |  | +0.0 / +0.0 |  |
| MNQ | 15 | eod | +0.062 | -0.149 .. +0.273 | +0.0008 | 0.56 / 0.55 / 0.62 | 0.623 |  |  | 10/16 | +0.078 | +0.047 |  | +0.6 / +0.6 |  |
| MNQ | 60 | h1 | -0.021 | -0.061 .. +0.019 | -0.0053 | 0.29 / 0.28 / 0.23 | 0.226 |  |  | 9/16 | -0.032 | -0.010 |  | -1.1 / -1.0 |  |
| MNQ | 60 | h2 | -0.033 | -0.088 .. +0.022 | -0.0057 | 0.24 / 0.22 / 0.19 | 0.192 |  |  | 10/16 | -0.071 | +0.005 |  | -1.3 / -1.2 |  |
| MNQ | 60 | h4 * | -0.058 | -0.135 .. +0.020 | -0.0070 | 0.14 / 0.13 / 0.1 | 0.101 | 1 | 1 | 10/16 | -0.114 | -0.002 | False | -1.5 / -1.5 | 0.100 |
| MNQ | 60 | h8 | -0.060 | -0.164 .. +0.045 | -0.0054 | 0.26 / 0.24 / 0.2 | 0.194 |  |  | 10/16 | -0.156 | +0.037 |  | -1.2 / -1.1 |  |
| MNQ | 60 | h16 | -0.058 | -0.173 .. +0.056 | -0.0040 | 0.32 / 0.3 / 0.26 | 0.254 |  |  | 9/16 | -0.129 | +0.013 |  | -1.1 / -1.0 |  |
| MNQ | 60 | eod | -0.057 | -0.172 .. +0.059 | -0.0037 | 0.33 / 0.32 / 0.27 | 0.268 |  |  | 9/16 | -0.138 | +0.025 |  | -1.0 / -1.0 |  |
| MYM | 5 | h1 | +0.000 | -0.013 .. +0.013 | +0.0001 | 0.95 / 0.95 / 0.97 | 0.962 |  |  | 5/8 | n/a | +0.000 |  | +0.1 / +0.1 |  |
| MYM | 5 | h2 | -0.002 | -0.020 .. +0.017 | -0.0002 | 0.86 / 0.86 / 0.9 | 0.886 |  |  | 4/8 | n/a | -0.002 |  | -0.2 / -0.2 |  |
| MYM | 5 | h4 | -0.003 | -0.029 .. +0.022 | -0.0003 | 0.79 / 0.79 / 0.86 | 0.83 |  |  | 5/8 | n/a | -0.003 |  | -0.2 / -0.3 | 0.044 |
| MYM | 5 | h8 | -0.017 | -0.053 .. +0.019 | -0.0009 | 0.36 / 0.39 / 0.53 | 0.503 |  |  | 6/8 | n/a | -0.017 |  | -0.9 / -0.9 |  |
| MYM | 5 | h16 | +0.022 | -0.032 .. +0.075 | +0.0008 | 0.43 / 0.45 / 0.52 | 0.514 |  |  | 5/8 | n/a | +0.022 |  | +0.8 / +0.8 |  |
| MYM | 5 | eod * | -0.121 | -0.446 .. +0.203 | -0.0011 | 0.46 / 0.47 / 0.47 | 0.478 | 1 | 1 | 4/8 | n/a | -0.121 | False | -0.8 / -0.7 |  |
| MYM | 15 | h1 * | -0.038 | -0.066 .. -0.010 | -0.0074 | 0.0078 / 0.004 / 0.017 | 0.0295 | 1 | 0.785 | 7/8 | n/a | -0.038 | False | -3.0 / -2.7 |  |
| MYM | 15 | h2 | -0.040 | -0.078 .. -0.002 | -0.0045 | 0.038 / 0.033 / 0.13 | 0.131 |  |  | 5/8 | n/a | -0.040 |  | -2.2 / -2.1 |  |
| MYM | 15 | h4 | -0.036 | -0.088 .. +0.015 | -0.0024 | 0.17 / 0.16 / 0.38 | 0.295 |  |  | 5/8 | n/a | -0.036 |  | -1.4 / -1.4 | 0.078 |
| MYM | 15 | h8 | -0.053 | -0.129 .. +0.023 | -0.0027 | 0.17 / 0.16 / 0.25 | 0.224 |  |  | 5/8 | n/a | -0.053 |  | -1.4 / -1.4 |  |
| MYM | 15 | h16 | -0.048 | -0.148 .. +0.051 | -0.0018 | 0.34 / 0.34 / 0.55 | 0.53 |  |  | 6/8 | n/a | -0.048 |  | -0.9 / -1.0 |  |
| MYM | 15 | eod | +0.164 | -0.116 .. +0.444 | +0.0024 | 0.25 / 0.27 / 0.38 | 0.376 |  |  | 6/8 | n/a | +0.164 |  | +1.2 / +1.1 |  |
| MYM | 60 | h1 * | +0.039 | -0.012 .. +0.090 | +0.0097 | 0.14 / 0.15 / 0.099 | 0.101 | 1 | 1 | 6/8 | n/a | +0.039 | False | +1.5 / +1.5 |  |
| MYM | 60 | h2 | +0.044 | -0.021 .. +0.110 | +0.0079 | 0.19 / 0.19 / 0.18 | 0.173 |  |  | 5/8 | n/a | +0.044 |  | +1.3 / +1.3 |  |
| MYM | 60 | h4 | +0.032 | -0.052 .. +0.116 | +0.0042 | 0.45 / 0.47 / 0.49 | 0.502 |  |  | 6/8 | n/a | +0.032 |  | +0.7 / +0.8 | 0.132 |
| MYM | 60 | h8 | +0.056 | -0.070 .. +0.182 | +0.0052 | 0.39 / 0.39 / 0.39 | 0.396 |  |  | 4/8 | n/a | +0.056 |  | +0.8 / +0.9 |  |
| MYM | 60 | h16 | +0.044 | -0.093 .. +0.181 | +0.0032 | 0.53 / 0.52 / 0.53 | 0.536 |  |  | 4/8 | n/a | +0.044 |  | +0.6 / +0.6 |  |
| MYM | 60 | eod | +0.053 | -0.085 .. +0.191 | +0.0036 | 0.45 / 0.44 / 0.46 | 0.468 |  |  | 4/8 | n/a | +0.053 |  | +0.7 / +0.8 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.031 | +0.026 .. +0.036 | +6.2% | +0.070 | 3.2e-30 | 2.29e-27 | 16/16 |
| MES | 5 | h2 | +0.037 | +0.031 .. +0.044 | +5.3% | +0.087 | 1.9e-25 |  | 16/16 |
| MES | 5 | h4 | +0.048 | +0.038 .. +0.058 | +4.8% | +0.110 | 7.6e-20 |  | 16/16 |
| MES | 5 | h8 | +0.060 | +0.045 .. +0.076 | +4.2% | +0.131 | 1.1e-13 |  | 16/16 |
| MES | 5 | h16 | +0.057 | +0.034 .. +0.080 | +2.7% | +0.137 | 1e-06 |  | 14/16 |
| MES | 5 | eod | +0.013 | -0.160 .. +0.187 | +0.1% | +0.199 | 0.94 |  | 8/16 |
| MES | 15 | h1 * | +0.042 | +0.031 .. +0.054 | +8.3% | +0.088 | 1.5e-12 | 5.45e-10 | 15/16 |
| MES | 15 | h2 | +0.051 | +0.034 .. +0.068 | +7.0% | +0.107 | 2e-08 |  | 14/16 |
| MES | 15 | h4 | +0.062 | +0.036 .. +0.087 | +5.9% | +0.117 | 2.2e-06 |  | 11/16 |
| MES | 15 | h8 | +0.074 | +0.037 .. +0.111 | +4.8% | +0.103 | 8.9e-05 |  | 11/16 |
| MES | 15 | h16 | +0.084 | +0.032 .. +0.136 | +3.7% | +0.068 | 0.0015 |  | 11/16 |
| MES | 15 | eod | -0.094 | -0.252 .. +0.064 | -1.7% | +0.017 | 0.24 |  | 8/16 |
| MES | 60 | h1 * | +0.076 | +0.051 .. +0.100 | +14.7% | +0.107 | 2.3e-09 | 6.85e-07 | 14/16 |
| MES | 60 | h2 | +0.094 | +0.060 .. +0.127 | +12.7% | +0.137 | 3.5e-08 |  | 14/16 |
| MES | 60 | h4 | +0.076 | +0.029 .. +0.123 | +7.2% | +0.142 | 0.0016 |  | 13/16 |
| MES | 60 | h8 | +0.091 | +0.029 .. +0.154 | +6.1% | +0.147 | 0.0042 |  | 13/16 |
| MES | 60 | h16 | +0.074 | +0.008 .. +0.141 | +3.6% | +0.132 | 0.029 |  | 13/16 |
| MES | 60 | eod | +0.063 | -0.003 .. +0.128 | +2.9% | +0.123 | 0.063 |  | 13/16 |
| MNQ | 5 | h1 * | +0.038 | +0.031 .. +0.046 | +7.2% | +0.082 | 4.1e-24 | 2.54e-21 | 16/16 |
| MNQ | 5 | h2 | +0.042 | +0.032 .. +0.053 | +5.5% | +0.104 | 1.9e-15 |  | 16/16 |
| MNQ | 5 | h4 | +0.044 | +0.030 .. +0.057 | +3.9% | +0.119 | 0.0019 |  | 15/16 |
| MNQ | 5 | h8 | +0.050 | +0.028 .. +0.072 | +3.1% | +0.120 | 0.0042 |  | 14/16 |
| MNQ | 5 | h16 | +0.027 | -0.010 .. +0.065 | +1.1% | +0.077 | 0.35 |  | 10/16 |
| MNQ | 5 | eod | +0.114 | -0.172 .. +0.400 | +0.9% | +0.441 | 0.69 |  | 9/16 |
| MNQ | 15 | h1 * | +0.046 | +0.033 .. +0.059 | +8.6% | +0.089 | 0.00012 | 0.0246 | 13/16 |
| MNQ | 15 | h2 | +0.047 | +0.026 .. +0.068 | +6.1% | +0.097 | 0.0051 |  | 11/16 |
| MNQ | 15 | h4 | +0.023 | -0.014 .. +0.060 | +2.0% | +0.080 | 0.29 |  | 10/16 |
| MNQ | 15 | h8 | -0.003 | -0.059 .. +0.052 | -0.2% | -0.000 | 0.91 |  | 9/16 |
| MNQ | 15 | h16 | +0.014 | -0.058 .. +0.085 | +0.5% | -0.101 | 0.81 |  | 8/16 |
| MNQ | 15 | eod | -0.048 | -0.276 .. +0.181 | -0.8% | -0.135 | 0.73 |  | 8/16 |
| MNQ | 60 | h1 * | +0.054 | +0.027 .. +0.082 | +10.3% | +0.089 | 0.00012 | 0.0247 | 12/16 |
| MNQ | 60 | h2 | +0.046 | +0.015 .. +0.078 | +6.1% | +0.095 | 0.022 |  | 12/16 |
| MNQ | 60 | h4 | +0.086 | +0.036 .. +0.136 | +7.8% | +0.134 | 0.0036 |  | 15/16 |
| MNQ | 60 | h8 | +0.092 | +0.028 .. +0.156 | +5.8% | +0.130 | 0.035 |  | 12/16 |
| MNQ | 60 | h16 | +0.081 | +0.016 .. +0.146 | +3.7% | +0.140 | 0.052 |  | 10/16 |
| MNQ | 60 | eod | +0.082 | +0.018 .. +0.147 | +3.6% | +0.135 | 0.037 |  | 11/16 |
| MYM | 5 | h1 * | +0.038 | +0.028 .. +0.048 | +7.2% | +0.073 | 1.7e-07 | 4.47e-05 | 8/8 |
| MYM | 5 | h2 | +0.038 | +0.025 .. +0.051 | +5.0% | +0.082 | 0.00017 |  | 8/8 |
| MYM | 5 | h4 | +0.044 | +0.021 .. +0.068 | +4.0% | +0.097 | 0.026 |  | 7/8 |
| MYM | 5 | h8 | +0.058 | +0.019 .. +0.097 | +3.6% | +0.100 | 0.0046 |  | 7/8 |
| MYM | 5 | h16 | +0.027 | -0.033 .. +0.086 | +1.1% | +0.036 | 0.38 |  | 6/8 |
| MYM | 5 | eod | -0.062 | -0.383 .. +0.259 | -0.5% | +0.197 | 0.71 |  | 4/8 |
| MYM | 15 | h1 | +0.037 | +0.017 .. +0.057 | +7.0% | +0.080 | 0.067 |  | 6/8 |
| MYM | 15 | h2 | +0.041 | +0.010 .. +0.072 | +5.4% | +0.083 | 0.074 |  | 6/8 |
| MYM | 15 | h4 | +0.031 | -0.019 .. +0.082 | +2.8% | +0.055 | 0.4 |  | 4/8 |
| MYM | 15 | h8 | +0.014 | -0.060 .. +0.087 | +0.8% | -0.036 | 1 |  | 4/8 |
| MYM | 15 | h16 | -0.091 | -0.194 .. +0.012 | -3.7% | -0.232 | 0.083 |  | 6/8 |
| MYM | 15 | eod * | -0.370 | -0.655 .. -0.085 | -6.1% | -0.318 | 0.012 | 1 | 6/8 |
| MYM | 60 | h1 | +0.030 | -0.003 .. +0.064 | +5.8% | +0.057 | 0.21 |  | 6/8 |
| MYM | 60 | h2 * | +0.052 | +0.005 .. +0.100 | +6.9% | +0.094 | 0.053 | 1 | 6/8 |
| MYM | 60 | h4 | +0.060 | -0.017 .. +0.137 | +5.6% | +0.112 | 0.19 |  | 5/8 |
| MYM | 60 | h8 | +0.066 | -0.039 .. +0.170 | +4.2% | +0.150 | 0.39 |  | 5/8 |
| MYM | 60 | h16 | +0.034 | -0.068 .. +0.136 | +1.6% | +0.098 | 0.74 |  | 5/8 |
| MYM | 60 | eod | +0.031 | -0.069 .. +0.132 | +1.4% | +0.093 | 0.74 |  | 3/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.62 pts | -1.05 .. -0.19 | 0.0047 |
| MES | 15 | -0.87 pts | -1.63 .. -0.11 | 0.036 |
| MES | 60 | -0.14 pts | -1.65 .. +1.37 | 0.86 |
| MNQ | 5 | -0.08 pts | -0.55 .. +0.38 | 0.76 |
| MNQ | 15 | +0.32 pts | -0.53 .. +1.17 | 0.47 |
| MNQ | 60 | -0.01 pts | -1.64 .. +1.62 | 0.99 |
| MYM | 5 | +0.24 pts | -0.47 .. +0.96 | 0.51 |
| MYM | 15 | -1.19 pts | -2.50 .. +0.11 | 0.08 |
| MYM | 60 | +2.19 pts | +0.16 .. +4.21 | 0.12 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 49286 | +0.005 | 0.444 | -0.06 | -3.56 | -3.44 | -3.73 | -3.56 |
| MES | 5 | h2 | event | against signal | 49286 | +0.011 | 0.444 | -0.00 | -3.50 | -3.42 | -3.61 | -3.49 |
| MES | 5 | h4 | event | against signal | 49286 | +0.015 | 0.444 | +0.07 | -3.43 | -3.39 | -3.50 | -3.42 |
| MES | 5 | h8 | event | against signal | 49286 | +0.010 | 0.444 | +0.02 | -3.48 | -3.42 | -3.55 | -3.46 |
| MES | 5 | h16 | event | with signal | 49286 | +0.014 | 0.444 | +0.25 | -3.25 | -3.50 | -2.89 | -3.27 |
| MES | 5 | eod | event | against signal | 49286 | +0.055 | 0.444 | +0.41 | -3.09 | -3.14 | -3.02 | -3.05 |
| MES | 15 | h1 | event | against signal | 14636 | +0.021 | 0.236 | +0.45 | -3.05 | -3.45 | -2.54 | -3.04 |
| MES | 15 | h2 | event | against signal | 14636 | +0.001 | 0.236 | +0.08 | -3.42 | -3.60 | -3.18 | -3.40 |
| MES | 15 | h4 | event | against signal | 14636 | -0.000 | 0.236 | +0.27 | -3.23 | -3.57 | -2.80 | -3.21 |
| MES | 15 | h8 | event | against signal | 14636 | +0.011 | 0.236 | +0.39 | -3.11 | -3.37 | -2.78 | -3.06 |
| MES | 15 | h16 | event | against signal | 14636 | +0.030 | 0.236 | +0.68 | -2.82 | -3.40 | -2.08 | -2.74 |
| MES | 15 | eod | event | with signal | 14636 | +0.030 | 0.236 | +0.02 | -3.48 | -3.69 | -3.22 | -3.61 |
| MES | 60 | h1 | event | against signal | 3493 | +0.018 | 0.101 | -0.02 | -3.52 | -2.96 | -4.09 | -3.47 |
| MES | 60 | h2 | event | against signal | 3493 | +0.042 | 0.101 | +0.49 | -3.01 | -2.20 | -3.83 | -2.89 |
| MES | 60 | h4 | event | against signal | 3493 | +0.059 | 0.101 | -0.31 | -3.81 | -1.37 | -6.31 | -3.61 |
| MES | 60 | h8 | event | against signal | 3493 | +0.037 | 0.101 | -0.89 | -4.39 | -0.99 | -7.86 | -4.14 |
| MES | 60 | h16 | event | against signal | 3493 | +0.068 | 0.101 | -0.40 | -3.90 | -0.12 | -7.78 | -3.69 |
| MES | 60 | eod | event | against signal | 3493 | +0.066 | 0.101 | -0.41 | -3.91 | -0.11 | -7.80 | -3.71 |
| MNQ | 5 | h1 | event | against signal | 41598 | +0.001 | 0.185 | -0.12 | -2.12 | -1.98 | -2.33 | -2.12 |
| MNQ | 5 | h2 | event | against signal | 41598 | +0.008 | 0.185 | -0.06 | -2.06 | -1.99 | -2.17 | -2.06 |
| MNQ | 5 | h4 | event | with signal | 41598 | +0.003 | 0.185 | +0.03 | -1.97 | -1.98 | -1.94 | -1.97 |
| MNQ | 5 | h8 | event | with signal | 41598 | +0.010 | 0.185 | +0.05 | -1.95 | -1.93 | -1.97 | -1.94 |
| MNQ | 5 | h16 | event | with signal | 41598 | +0.019 | 0.185 | +0.35 | -1.65 | -1.91 | -1.24 | -1.66 |
| MNQ | 5 | eod | event | with signal | 41598 | +0.044 | 0.185 | -0.14 | -2.14 | -1.98 | -2.39 | -2.18 |
| MNQ | 15 | h1 | event | against signal | 12817 | +0.006 | 0.094 | +0.06 | -1.94 | -1.99 | -1.87 | -1.91 |
| MNQ | 15 | h2 | event | with signal | 12817 | +0.020 | 0.094 | +0.34 | -1.66 | -1.82 | -1.44 | -1.69 |
| MNQ | 15 | h4 | event | with signal | 12817 | +0.022 | 0.094 | +0.23 | -1.77 | -1.84 | -1.67 | -1.85 |
| MNQ | 15 | h8 | event | with signal | 12817 | +0.028 | 0.094 | +0.66 | -1.34 | -1.64 | -0.95 | -1.48 |
| MNQ | 15 | h16 | event | with signal | 12817 | +0.011 | 0.094 | +0.16 | -1.84 | -1.62 | -2.13 | -1.98 |
| MNQ | 15 | eod | event | with signal | 12817 | +0.089 | 0.094 | -0.52 | -2.52 | -1.86 | -3.36 | -2.69 |
| MNQ | 60 | h1 | event | against signal | 3349 | +0.019 | 0.041 | +0.57 | -1.43 | -1.41 | -1.45 | -1.37 |
| MNQ | 60 | h2 | event | against signal | 3349 | +0.027 | 0.041 | +0.15 | -1.85 | -1.13 | -2.66 | -1.60 |
| MNQ | 60 | h4 | event | against signal | 3349 | +0.046 | 0.041 | -0.71 | -2.71 | -0.84 | -4.82 | -2.30 |
| MNQ | 60 | h8 | event | against signal | 3349 | +0.040 | 0.041 | -1.64 | -3.64 | -0.48 | -7.19 | -2.95 |
| MNQ | 60 | h16 | event | against signal | 3349 | +0.035 | 0.041 | -3.16 | -5.16 | -0.84 | -10.03 | -4.48 |
| MNQ | 60 | eod | event | against signal | 3349 | +0.033 | 0.041 | -3.53 | -5.53 | -0.82 | -10.83 | -4.89 |
| MYM | 5 | h1 | event | with signal | 18481 | +0.001 | 0.203 | +0.02 | -1.98 | +nan | -1.98 | -1.98 |
| MYM | 5 | h2 | event | against signal | 18481 | +0.002 | 0.203 | +0.06 | -1.94 | +nan | -1.94 | -1.93 |
| MYM | 5 | h4 | event | against signal | 18481 | +0.003 | 0.203 | +0.17 | -1.83 | +nan | -1.83 | -1.82 |
| MYM | 5 | h8 | event | against signal | 18481 | +0.017 | 0.203 | +0.40 | -1.60 | +nan | -1.60 | -1.60 |
| MYM | 5 | h16 | event | with signal | 18481 | +0.022 | 0.203 | -0.22 | -2.22 | +nan | -2.22 | -2.22 |
| MYM | 5 | eod | event | against signal | 18481 | +0.128 | 0.203 | +1.71 | -0.29 | +nan | -0.29 | -0.40 |
| MYM | 15 | h1 | event | against signal | 6111 | +0.039 | 0.108 | +0.65 | -1.35 | +nan | -1.35 | -1.35 |
| MYM | 15 | h2 | event | against signal | 6111 | +0.040 | 0.108 | +0.71 | -1.29 | +nan | -1.29 | -1.27 |
| MYM | 15 | h4 | event | against signal | 6111 | +0.040 | 0.108 | +1.07 | -0.93 | +nan | -0.93 | -0.95 |
| MYM | 15 | h8 | event | against signal | 6111 | +0.057 | 0.108 | +1.23 | -0.77 | +nan | -0.77 | -0.82 |
| MYM | 15 | h16 | event | against signal | 6111 | +0.058 | 0.108 | +1.28 | -0.72 | +nan | -0.72 | -0.85 |
| MYM | 15 | eod | event | with signal | 6111 | +0.135 | 0.108 | -0.50 | -2.50 | +nan | -2.50 | -1.99 |
| MYM | 60 | h1 | event | with signal | 1717 | +0.037 | 0.051 | +1.16 | -0.84 | +nan | -0.84 | -0.73 |
| MYM | 60 | h2 | event | with signal | 1717 | +0.043 | 0.051 | +1.27 | -0.73 | +nan | -0.73 | -0.64 |
| MYM | 60 | h4 | event | with signal | 1717 | +0.030 | 0.051 | +1.76 | -0.24 | +nan | -0.24 | -0.08 |
| MYM | 60 | h8 | event | with signal | 1717 | +0.051 | 0.051 | +2.68 | +0.68 | +nan | +0.68 | +0.98 |
| MYM | 60 | h16 | event | with signal | 1717 | +0.033 | 0.051 | +1.85 | -0.15 | +nan | -0.15 | +0.42 |
| MYM | 60 | eod | event | with signal | 1717 | +0.040 | 0.051 | +2.18 | +0.18 | +nan | +0.18 | +0.78 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.118 | +0.130 | +0.085 | +0.038 | -0.019 | +0.000 | -0.055 | -0.061 | -0.066 | -0.060 | -0.036 |
| MES | 15 | +0.130 | +0.157 | +0.136 | +0.065 | +0.006 | +0.000 | -0.045 | -0.026 | -0.029 | -0.039 | -0.057 |
| MES | 60 | +0.250 | +0.154 | +0.122 | +0.122 | +0.027 | +0.000 | -0.026 | -0.059 | -0.083 | -0.082 | -0.370 |
| MNQ | 5 | +0.223 | +0.217 | +0.180 | +0.115 | +0.021 | +0.000 | -0.031 | -0.039 | -0.028 | -0.020 | -0.014 |
| MNQ | 15 | +0.190 | +0.218 | +0.211 | +0.120 | +0.025 | +0.000 | -0.018 | +0.007 | +0.010 | +0.026 | +0.006 |
| MNQ | 60 | +0.233 | +0.185 | +0.155 | +0.119 | +0.016 | +0.000 | -0.023 | -0.038 | -0.074 | -0.040 | +0.472 |
| MYM | 5 | +0.219 | +0.223 | +0.176 | +0.108 | +0.024 | +0.000 | -0.009 | -0.011 | -0.012 | -0.025 | +0.023 |
| MYM | 15 | +0.199 | +0.211 | +0.186 | +0.111 | +0.021 | +0.000 | -0.042 | -0.045 | -0.047 | -0.064 | -0.070 |
| MYM | 60 | -0.043 | +0.123 | +0.114 | +0.103 | +0.017 | +0.000 | +0.037 | +0.043 | +0.024 | +0.202 | +0.355 |

## Calibration

- MES 5-min: 1036271 bars, 49286 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 14636 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 3493 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 41598 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 12817 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 3349 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 18481 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 6111 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1717 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37045 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
