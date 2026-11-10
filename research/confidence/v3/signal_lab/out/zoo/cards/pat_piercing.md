# Impact card: pat_piercing

candle pattern piercing in its textbook direction: bar1 down with body > avgB10, bar2 opens <= close1 and closes above the middle of body1 but below open1 -> bullish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.046 R20 over the next 8 bars (40 min), p=0.083; we would catch an effect of 0.037 R20 or more 80% of the time).
- MES 5-min size: the market moves 4% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.021 R20, CONFIRMED, q=0.00295, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.80 at recent bar sizes, 90% range up to $1.33); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.020 R20 over the next 1 bar (15 min), p=0.4; we would catch an effect of 0.064 R20 or more 80% of the time).
- MES 15-min size: the market moves 5% MORE after the event than after matched bars over the next 2 bars (30 min) (+0.036 R20, possible, q=0.0657, 12 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.56 at recent bar sizes, 90% range up to $1.76); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.063 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.134 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.43 at recent bar sizes, 90% range up to $8.94); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.012 R20 over the next 1 bar (5 min), p=0.94; we would catch an effect of 0.038 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.16).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.31 at recent bar sizes, 90% range up to $1.10); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.067 R20 over the next 4 bars (1 h), p=0.2; we would catch an effect of 0.070 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.92).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.86 at recent bar sizes, 90% range up to $4.47); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.131 R20 over the next 16 bars (16 h), p=0.65; we would catch an effect of 0.149 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $11.52 at recent bar sizes, 90% range up to $16.09); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.207 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.053 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.29).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.48 at recent bar sizes, 90% range up to $0.95); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.016 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.093 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.034).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.33 at recent bar sizes, 90% range up to $2.39); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.227 R20 over the next 16 bars (16 h), p=0.22; we would catch an effect of 0.207 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $9.06 at recent bar sizes, 90% range up to $13.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.000 | -0.014 .. +0.014 | -0.0000 | 0.99 / 0.99 / 0.99 | 0.995 |  |  | 8/16 | -0.015 | +0.015 |  | -0.0 / -0.0 |  |
| MES | 5 | h2 | +0.011 | -0.008 .. +0.030 | +0.0012 | 0.25 / 0.22 / 0.23 | 0.236 |  |  | 9/16 | -0.005 | +0.027 |  | +1.2 / +1.2 |  |
| MES | 5 | h4 | +0.020 | -0.004 .. +0.044 | +0.0015 | 0.097 / 0.096 / 0.14 | 0.131 |  |  | 7/16 | -0.009 | +0.049 |  | +1.6 / +1.7 | 0.037 |
| MES | 5 | h8 * | +0.046 | +0.010 .. +0.082 | +0.0024 | 0.013 / 0.0096 / 0.017 | 0.018 | 1 | 0.944 | 12/16 | +0.018 | +0.074 | False | +2.5 / +2.5 |  |
| MES | 5 | h16 | +0.022 | -0.038 .. +0.082 | +0.0008 | 0.47 / 0.47 / 0.42 | 0.41 |  |  | 10/16 | -0.004 | +0.048 |  | +0.8 / +0.7 |  |
| MES | 5 | eod | +0.258 | -0.152 .. +0.669 | +0.0019 | 0.22 / 0.24 / 0.047 | 0.0438 |  |  | 10/16 | +0.039 | +0.477 |  | +2.2 / +1.2 |  |
| MES | 15 | h1 * | -0.020 | -0.040 .. -0.000 | -0.0034 | 0.048 / 0.053 / 0.07 | 0.0695 | 1 | 1 | 11/16 | -0.013 | -0.028 | False | -1.9 / -2.0 |  |
| MES | 15 | h2 | -0.009 | -0.038 .. +0.019 | -0.0011 | 0.52 / 0.53 / 0.57 | 0.556 |  |  | 9/16 | -0.007 | -0.012 |  | -0.6 / -0.6 |  |
| MES | 15 | h4 | +0.014 | -0.029 .. +0.057 | +0.0011 | 0.53 / 0.51 / 0.56 | 0.549 |  |  | 9/16 | -0.003 | +0.031 |  | +0.7 / +0.6 | 0.064 |
| MES | 15 | h8 | +0.010 | -0.054 .. +0.073 | +0.0005 | 0.77 / 0.76 / 0.78 | 0.771 |  |  | 9/16 | -0.013 | +0.032 |  | +0.3 / +0.3 |  |
| MES | 15 | h16 | -0.038 | -0.138 .. +0.063 | -0.0014 | 0.46 / 0.46 / 0.42 | 0.417 |  |  | 10/16 | +0.005 | -0.080 |  | -0.8 / -0.7 |  |
| MES | 15 | eod | +0.057 | -0.207 .. +0.321 | +0.0008 | 0.67 / 0.69 / 0.62 | 0.614 |  |  | 8/16 | +0.035 | +0.078 |  | +0.6 / +0.4 |  |
| MES | 60 | h1 | +0.002 | -0.041 .. +0.045 | +0.0004 | 0.92 / 0.92 / 0.93 | 0.92 |  |  | 8/16 | +0.005 | -0.000 |  | +0.1 / +0.1 |  |
| MES | 60 | h2 | +0.004 | -0.058 .. +0.066 | +0.0004 | 0.91 / 0.91 / 0.91 | 0.915 |  |  | 7/16 | +0.020 | -0.012 |  | +0.1 / +0.1 |  |
| MES | 60 | h4 | -0.027 | -0.118 .. +0.063 | -0.0024 | 0.55 / 0.54 / 0.54 | 0.541 |  |  | 10/16 | -0.042 | -0.013 |  | -0.6 / -0.6 | 0.134 |
| MES | 60 | h8 * | -0.063 | -0.183 .. +0.057 | -0.0039 | 0.3 / 0.3 / 0.28 | 0.278 | 1 | 1 | 10/16 | -0.100 | -0.026 | False | -1.0 / -1.0 |  |
| MES | 60 | h16 | -0.059 | -0.202 .. +0.084 | -0.0028 | 0.42 / 0.4 / 0.38 | 0.378 |  |  | 8/16 | -0.081 | -0.037 |  | -0.9 / -0.8 |  |
| MES | 60 | eod | -0.058 | -0.200 .. +0.085 | -0.0026 | 0.43 / 0.42 / 0.4 | 0.399 |  |  | 8/16 | -0.073 | -0.043 |  | -0.8 / -0.8 |  |
| MNQ | 5 | h1 * | -0.012 | -0.026 .. +0.001 | -0.0017 | 0.067 / 0.067 / 0.091 | 0.0852 | 1 | 1 | 12/16 | -0.014 | -0.011 | False | -1.9 / -1.8 |  |
| MNQ | 5 | h2 | -0.001 | -0.020 .. +0.018 | -0.0001 | 0.91 / 0.91 / 0.95 | 0.945 |  |  | 8/16 | -0.006 | +0.004 |  | -0.1 / -0.1 |  |
| MNQ | 5 | h4 | +0.008 | -0.018 .. +0.034 | +0.0005 | 0.55 / 0.57 / 0.66 | 0.619 |  |  | 7/16 | -0.012 | +0.028 |  | +0.6 / +0.6 | 0.038 |
| MNQ | 5 | h8 | -0.000 | -0.040 .. +0.040 | -0.0000 | 0.99 / 0.99 / 0.99 | 0.99 |  |  | 8/16 | -0.017 | +0.016 |  | -0.0 / -0.0 |  |
| MNQ | 5 | h16 | -0.003 | -0.065 .. +0.059 | -0.0001 | 0.93 / 0.93 / 0.96 | 0.958 |  |  | 8/16 | +0.013 | -0.018 |  | -0.1 / -0.1 |  |
| MNQ | 5 | eod | +0.062 | -0.424 .. +0.547 | +0.0003 | 0.8 / 0.81 / 0.73 | 0.729 |  |  | 10/16 | -0.146 | +0.268 |  | +0.4 / +0.2 |  |
| MNQ | 15 | h1 | +0.009 | -0.012 .. +0.031 | +0.0012 | 0.4 / 0.41 / 0.52 | 0.422 |  |  | 10/16 | +0.005 | +0.014 |  | +0.8 / +0.8 |  |
| MNQ | 15 | h2 | +0.028 | -0.003 .. +0.060 | +0.0022 | 0.074 / 0.074 / 0.25 | 0.164 |  |  | 11/16 | +0.023 | +0.034 |  | +1.7 / +1.8 |  |
| MNQ | 15 | h4 * | +0.067 | +0.022 .. +0.112 | +0.0031 | 0.0038 / 0.0037 / 0.09 | 0.0891 | 1 | 0.613 | 12/16 | +0.055 | +0.078 | False | +2.9 / +2.9 | 0.070 |
| MNQ | 15 | h8 | +0.040 | -0.029 .. +0.110 | +0.0014 | 0.26 / 0.25 / 0.42 | 0.358 |  |  | 9/16 | -0.015 | +0.095 |  | +1.2 / +1.1 |  |
| MNQ | 15 | h16 | +0.055 | -0.048 .. +0.157 | +0.0016 | 0.3 / 0.29 / 0.37 | 0.35 |  |  | 8/16 | +0.028 | +0.081 |  | +1.1 / +1.0 |  |
| MNQ | 15 | eod | +0.173 | -0.117 .. +0.463 | +0.0018 | 0.24 / 0.27 / 0.3 | 0.28 |  |  | 11/16 | +0.203 | +0.143 |  | +1.5 / +1.2 |  |
| MNQ | 60 | h1 | -0.005 | -0.049 .. +0.039 | -0.0008 | 0.81 / 0.82 / 0.84 | 0.838 |  |  | 8/16 | -0.007 | -0.004 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h2 | -0.016 | -0.085 .. +0.054 | -0.0017 | 0.66 / 0.67 / 0.66 | 0.656 |  |  | 10/16 | +0.000 | -0.032 |  | -0.4 / -0.4 |  |
| MNQ | 60 | h4 | -0.028 | -0.125 .. +0.068 | -0.0022 | 0.56 / 0.58 / 0.58 | 0.59 |  |  | 9/16 | +0.006 | -0.063 |  | -0.6 / -0.6 | 0.149 |
| MNQ | 60 | h8 | -0.067 | -0.203 .. +0.069 | -0.0038 | 0.33 / 0.34 / 0.33 | 0.327 |  |  | 8/16 | -0.058 | -0.077 |  | -1.0 / -1.0 |  |
| MNQ | 60 | h16 * | -0.131 | -0.289 .. +0.026 | -0.0056 | 0.1 / 0.11 / 0.084 | 0.0831 | 1 | 1 | 10/16 | -0.131 | -0.132 | False | -1.7 / -1.6 |  |
| MNQ | 60 | eod | -0.126 | -0.285 .. +0.032 | -0.0052 | 0.12 / 0.12 / 0.1 | 0.0979 |  |  | 9/16 | -0.117 | -0.135 |  | -1.6 / -1.6 |  |
| MYM | 5 | h1 | +0.002 | -0.013 .. +0.018 | +0.0003 | 0.76 / 0.76 / 0.8 | 0.763 |  |  | 6/8 | n/a | +0.002 |  | +0.3 / +0.3 |  |
| MYM | 5 | h2 | +0.000 | -0.023 .. +0.024 | +0.0000 | 0.98 / 0.98 / 0.98 | 0.976 |  |  | 3/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 5 | h4 | +0.002 | -0.031 .. +0.035 | +0.0001 | 0.91 / 0.91 / 0.93 | 0.924 |  |  | 3/8 | n/a | +0.002 |  | +0.1 / +0.1 | 0.053 |
| MYM | 5 | h8 | -0.007 | -0.059 .. +0.045 | -0.0002 | 0.8 / 0.8 / 0.91 | 0.901 |  |  | 5/8 | n/a | -0.007 |  | -0.3 / -0.2 |  |
| MYM | 5 | h16 | +0.016 | -0.067 .. +0.099 | +0.0005 | 0.71 / 0.72 / 0.72 | 0.711 |  |  | 5/8 | n/a | +0.016 |  | +0.4 / +0.4 |  |
| MYM | 5 | eod * | +0.207 | -0.509 .. +0.922 | +0.0013 | 0.57 / 0.58 / 0.31 | 0.335 | 1 | 1 | 4/8 | n/a | +0.207 | False | +1.1 / +0.6 |  |
| MYM | 15 | h1 * | -0.016 | -0.046 .. +0.013 | -0.0022 | 0.28 / 0.27 / 0.39 | 0.318 | 1 | 1 | 4/8 | n/a | -0.016 | False | -1.0 / -1.1 |  |
| MYM | 15 | h2 | -0.007 | -0.049 .. +0.034 | -0.0006 | 0.73 / 0.73 / 0.83 | 0.772 |  |  | 5/8 | n/a | -0.007 |  | -0.3 / -0.3 |  |
| MYM | 15 | h4 | +0.009 | -0.055 .. +0.072 | +0.0004 | 0.79 / 0.79 / 0.87 | 0.823 |  |  | 5/8 | n/a | +0.009 |  | +0.3 / +0.3 | 0.093 |
| MYM | 15 | h8 | +0.022 | -0.074 .. +0.118 | +0.0008 | 0.65 / 0.65 / 0.74 | 0.704 |  |  | 5/8 | n/a | +0.022 |  | +0.5 / +0.4 |  |
| MYM | 15 | h16 | -0.056 | -0.213 .. +0.100 | -0.0014 | 0.48 / 0.47 / 0.57 | 0.561 |  |  | 5/8 | n/a | -0.056 |  | -0.8 / -0.7 |  |
| MYM | 15 | eod | -0.090 | -0.541 .. +0.361 | -0.0010 | 0.7 / 0.7 / 0.7 | 0.701 |  |  | 5/8 | n/a | -0.090 |  | -0.6 / -0.4 |  |
| MYM | 60 | h1 | +0.023 | -0.043 .. +0.090 | +0.0037 | 0.49 / 0.47 / 0.52 | 0.509 |  |  | 4/8 | n/a | +0.023 |  | +0.7 / +0.7 |  |
| MYM | 60 | h2 | +0.006 | -0.097 .. +0.109 | +0.0006 | 0.91 / 0.91 / 0.92 | 0.909 |  |  | 4/8 | n/a | +0.006 |  | +0.1 / +0.1 |  |
| MYM | 60 | h4 | +0.061 | -0.071 .. +0.193 | +0.0048 | 0.36 / 0.37 / 0.39 | 0.392 |  |  | 5/8 | n/a | +0.061 |  | +0.9 / +0.9 | 0.207 |
| MYM | 60 | h8 | +0.188 | +0.004 .. +0.372 | +0.0107 | 0.046 / 0.048 / 0.043 | 0.0464 |  |  | 8/8 | n/a | +0.188 |  | +2.0 / +2.0 |  |
| MYM | 60 | h16 * | +0.227 | +0.014 .. +0.439 | +0.0098 | 0.037 / 0.036 / 0.032 | 0.0332 | 1 | 0.994 | 7/8 | n/a | +0.227 | False | +2.1 / +2.1 |  |
| MYM | 60 | eod | +0.232 | +0.015 .. +0.449 | +0.0096 | 0.036 / 0.038 / 0.032 | 0.0348 |  |  | 7/8 | n/a | +0.232 |  | +2.1 / +2.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.021 | +0.012 .. +0.029 | +4.2% | +0.022 | 1.3e-05 | 0.00295 | 14/16 |
| MES | 5 | h2 | +0.024 | +0.011 .. +0.036 | +3.4% | +0.035 | 0.012 |  | 14/16 |
| MES | 5 | h4 | +0.015 | -0.002 .. +0.032 | +1.5% | +0.045 | 0.47 |  | 10/16 |
| MES | 5 | h8 | +0.016 | -0.009 .. +0.040 | +1.1% | +0.051 | 0.59 |  | 9/16 |
| MES | 5 | h16 | +0.039 | +0.003 .. +0.075 | +1.9% | +0.058 | 0.24 |  | 10/16 |
| MES | 5 | eod | -0.026 | -0.232 .. +0.179 | -0.3% | -0.164 | 0.81 |  | 5/16 |
| MES | 15 | h1 | +0.024 | +0.010 .. +0.038 | +4.7% | +0.034 | 0.00086 |  | 13/16 |
| MES | 15 | h2 * | +0.036 | +0.016 .. +0.056 | +4.9% | +0.049 | 0.00036 | 0.0657 | 12/16 |
| MES | 15 | h4 | +0.032 | +0.005 .. +0.059 | +3.0% | +0.049 | 0.023 |  | 11/16 |
| MES | 15 | h8 | +0.025 | -0.020 .. +0.069 | +1.6% | +0.033 | 0.28 |  | 10/16 |
| MES | 15 | h16 | +0.006 | -0.059 .. +0.070 | +0.2% | +0.023 | 0.87 |  | 7/16 |
| MES | 15 | eod | -0.037 | -0.205 .. +0.131 | -0.7% | +0.024 | 0.67 |  | 6/16 |
| MES | 60 | h1 | +0.007 | -0.020 .. +0.033 | +1.3% | +0.039 | 0.97 |  | 8/16 |
| MES | 60 | h2 * | +0.027 | -0.012 .. +0.066 | +3.6% | +0.045 | 0.36 | 1 | 10/16 |
| MES | 60 | h4 | +0.030 | -0.027 .. +0.087 | +2.8% | +0.085 | 0.57 |  | 11/16 |
| MES | 60 | h8 | +0.021 | -0.050 .. +0.091 | +1.4% | +0.086 | 0.83 |  | 10/16 |
| MES | 60 | h16 | +0.019 | -0.064 .. +0.101 | +0.9% | +0.052 | 0.91 |  | 9/16 |
| MES | 60 | eod | +0.006 | -0.077 .. +0.089 | +0.3% | +0.043 | 0.95 |  | 9/16 |
| MNQ | 5 | h1 * | +0.012 | +0.004 .. +0.021 | +2.3% | +0.017 | 0.026 | 1 | 12/16 |
| MNQ | 5 | h2 | +0.023 | +0.010 .. +0.036 | +3.0% | +0.030 | 0.076 |  | 13/16 |
| MNQ | 5 | h4 | +0.032 | +0.013 .. +0.051 | +2.9% | +0.052 | 0.046 |  | 13/16 |
| MNQ | 5 | h8 | +0.035 | +0.002 .. +0.068 | +2.1% | +0.063 | 0.11 |  | 15/16 |
| MNQ | 5 | h16 | +0.050 | -0.001 .. +0.101 | +2.1% | +0.066 | 0.3 |  | 12/16 |
| MNQ | 5 | eod | -0.103 | -0.413 .. +0.207 | -0.8% | -0.284 | 0.58 |  | 8/16 |
| MNQ | 15 | h1 | +0.009 | -0.006 .. +0.025 | +1.7% | +0.024 | 0.33 |  | 11/16 |
| MNQ | 15 | h2 * | +0.017 | -0.006 .. +0.040 | +2.2% | +0.031 | 0.15 | 1 | 10/16 |
| MNQ | 15 | h4 | +0.005 | -0.033 .. +0.042 | +0.4% | +0.019 | 0.81 |  | 9/16 |
| MNQ | 15 | h8 | -0.010 | -0.066 .. +0.046 | -0.6% | +0.008 | 0.79 |  | 8/16 |
| MNQ | 15 | h16 | -0.030 | -0.101 .. +0.042 | -1.2% | -0.038 | 0.66 |  | 8/16 |
| MNQ | 15 | eod | -0.060 | -0.292 .. +0.173 | -0.9% | -0.049 | 0.67 |  | 9/16 |
| MNQ | 60 | h1 | +0.002 | -0.029 .. +0.033 | +0.4% | +0.021 | 0.89 |  | 7/16 |
| MNQ | 60 | h2 * | +0.029 | -0.021 .. +0.078 | +3.7% | +0.028 | 0.27 | 1 | 9/16 |
| MNQ | 60 | h4 | -0.001 | -0.075 .. +0.072 | -0.1% | +0.077 | 0.97 |  | 9/16 |
| MNQ | 60 | h8 | +0.006 | -0.091 .. +0.103 | +0.4% | +0.111 | 0.9 |  | 9/16 |
| MNQ | 60 | h16 | -0.018 | -0.129 .. +0.093 | -0.8% | +0.104 | 0.76 |  | 9/16 |
| MNQ | 60 | eod | -0.021 | -0.129 .. +0.086 | -0.9% | +0.106 | 0.7 |  | 9/16 |
| MYM | 5 | h1 * | +0.016 | +0.004 .. +0.028 | +3.0% | +0.013 | 0.048 | 1 | 8/8 |
| MYM | 5 | h2 | +0.009 | -0.010 .. +0.029 | +1.2% | +0.021 | 0.35 |  | 4/8 |
| MYM | 5 | h4 | +0.012 | -0.018 .. +0.042 | +1.1% | +0.031 | 0.76 |  | 5/8 |
| MYM | 5 | h8 | +0.015 | -0.030 .. +0.060 | +0.9% | +0.036 | 0.87 |  | 6/8 |
| MYM | 5 | h16 | +0.007 | -0.057 .. +0.071 | +0.3% | +0.033 | 0.84 |  | 6/8 |
| MYM | 5 | eod | -0.064 | -0.401 .. +0.273 | -0.5% | +0.031 | 0.71 |  | 3/8 |
| MYM | 15 | h1 | +0.025 | +0.002 .. +0.047 | +4.6% | +0.037 | 0.099 |  | 7/8 |
| MYM | 15 | h2 | +0.047 | +0.014 .. +0.080 | +6.1% | +0.068 | 0.0067 |  | 7/8 |
| MYM | 15 | h4 * | +0.070 | +0.020 .. +0.119 | +6.2% | +0.072 | 0.0057 | 0.816 | 7/8 |
| MYM | 15 | h8 | +0.062 | -0.013 .. +0.138 | +3.8% | +0.085 | 0.21 |  | 6/8 |
| MYM | 15 | h16 | +0.034 | -0.085 .. +0.153 | +1.4% | +0.041 | 0.84 |  | 6/8 |
| MYM | 15 | eod | -0.040 | -0.325 .. +0.245 | -0.7% | +0.066 | 0.91 |  | 4/8 |
| MYM | 60 | h1 * | +0.011 | -0.031 .. +0.054 | +2.1% | +0.029 | 0.63 | 1 | 4/8 |
| MYM | 60 | h2 | +0.017 | -0.060 .. +0.095 | +2.3% | +0.039 | 0.66 |  | 3/8 |
| MYM | 60 | h4 | +0.015 | -0.079 .. +0.110 | +1.4% | +0.077 | 0.83 |  | 6/8 |
| MYM | 60 | h8 | +0.009 | -0.115 .. +0.133 | +0.6% | +0.090 | 0.95 |  | 5/8 |
| MYM | 60 | h16 | +0.002 | -0.131 .. +0.134 | +0.1% | +0.107 | 0.98 |  | 2/8 |
| MYM | 60 | eod | -0.011 | -0.145 .. +0.124 | -0.5% | +0.111 | 0.88 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.61 pts | -0.24 .. +1.46 | 0.16 |
| MES | 15 | +0.13 pts | -1.19 .. +1.44 | 0.92 |
| MES | 60 | +0.44 pts | -2.00 .. +2.87 | 0.72 |
| MNQ | 5 | +0.13 pts | -0.66 .. +0.93 | 0.74 |
| MNQ | 15 | +1.41 pts | +0.18 .. +2.63 | 0.028 |
| MNQ | 60 | -0.26 pts | -2.60 .. +2.07 | 1 |
| MYM | 5 | -0.02 pts | -1.11 .. +1.07 | 0.97 |
| MYM | 15 | +0.46 pts | -1.18 .. +2.09 | 0.59 |
| MYM | 60 | +1.26 pts | -2.23 .. +4.75 | 0.48 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 13287 | +0.010 | 0.254 | +0.08 | -3.42 | -3.31 | -3.48 | -3.57 |
| MES | 5 | h2 | event | with signal | 13287 | -0.002 | 0.254 | -0.07 | -3.57 | -3.69 | -3.49 | -3.35 |
| MES | 5 | h4 | event | with signal | 13287 | +0.012 | 0.254 | +0.07 | -3.43 | -3.69 | -3.27 | -3.24 |
| MES | 5 | h8 | event | with signal | 13287 | +0.050 | 0.254 | +0.45 | -3.05 | -3.21 | -2.96 | -2.98 |
| MES | 5 | h16 | event | with signal | 13287 | +0.047 | 0.254 | +0.27 | -3.23 | -2.99 | -3.38 | -3.32 |
| MES | 5 | eod | event | with signal | 13287 | +0.613 | 0.254 | +6.73 | +3.23 | +0.06 | +5.10 | +3.08 |
| MES | 15 | h1 | event | against signal | 5703 | +0.024 | 0.170 | +0.36 | -3.14 | -3.44 | -2.92 | -3.25 |
| MES | 15 | h2 | event | against signal | 5703 | +0.010 | 0.170 | +0.10 | -3.40 | -3.68 | -3.19 | -3.47 |
| MES | 15 | h4 | event | with signal | 5703 | +0.023 | 0.170 | +0.64 | -2.86 | -3.05 | -2.71 | -2.88 |
| MES | 15 | h8 | event | with signal | 5703 | +0.038 | 0.170 | +0.73 | -2.77 | -3.15 | -2.50 | -2.97 |
| MES | 15 | h16 | event | against signal | 5703 | -0.023 | 0.170 | -0.75 | -4.25 | -4.47 | -4.09 | -3.87 |
| MES | 15 | eod | event | with signal | 5703 | +0.291 | 0.170 | +4.32 | +0.82 | +0.84 | +0.81 | +0.14 |
| MES | 60 | h1 | event | with signal | 1447 | +0.013 | 0.091 | +0.65 | -2.85 | -2.96 | -2.77 | -3.14 |
| MES | 60 | h2 | event | with signal | 1447 | +0.024 | 0.091 | +0.64 | -2.86 | -2.48 | -3.18 | -3.39 |
| MES | 60 | h4 | event | against signal | 1447 | -0.012 | 0.091 | -1.44 | -4.94 | -3.09 | -6.47 | -3.94 |
| MES | 60 | h8 | event | against signal | 1447 | -0.006 | 0.091 | -3.83 | -7.33 | -2.17 | -11.60 | -5.57 |
| MES | 60 | h16 | event | against signal | 1447 | -0.044 | 0.091 | -6.15 | -9.65 | -4.03 | -14.30 | -7.13 |
| MES | 60 | eod | event | against signal | 1447 | -0.048 | 0.091 | -5.55 | -9.05 | -4.28 | -13.00 | -6.56 |
| MNQ | 5 | h1 | event | against signal | 15496 | +0.014 | 0.123 | +0.19 | -1.81 | -1.94 | -1.70 | -1.88 |
| MNQ | 5 | h2 | event | against signal | 15496 | +0.002 | 0.123 | +0.04 | -1.96 | -1.90 | -2.00 | -2.08 |
| MNQ | 5 | h4 | event | with signal | 15496 | +0.017 | 0.123 | +0.18 | -1.82 | -2.05 | -1.63 | -1.76 |
| MNQ | 5 | h8 | event | against signal | 15496 | -0.032 | 0.123 | -0.56 | -2.56 | -2.11 | -2.93 | -2.41 |
| MNQ | 5 | h16 | event | against signal | 15496 | -0.064 | 0.123 | -0.57 | -2.57 | -2.54 | -2.61 | -2.19 |
| MNQ | 5 | eod | event | with signal | 15496 | +0.711 | 0.123 | +7.57 | +5.57 | +0.69 | +9.66 | +5.38 |
| MNQ | 15 | h1 | event | with signal | 5790 | +0.013 | 0.077 | +0.58 | -1.42 | -1.74 | -1.09 | -1.45 |
| MNQ | 15 | h2 | event | with signal | 5790 | +0.040 | 0.077 | +0.94 | -1.06 | -1.33 | -0.77 | -1.19 |
| MNQ | 15 | h4 | event | with signal | 5790 | +0.094 | 0.077 | +1.82 | -0.18 | -0.91 | +0.57 | -0.56 |
| MNQ | 15 | h8 | event | with signal | 5790 | +0.099 | 0.077 | +2.15 | +0.15 | -1.19 | +1.53 | -0.71 |
| MNQ | 15 | h16 | event | with signal | 5790 | +0.151 | 0.077 | +3.94 | +1.94 | +0.06 | +3.89 | +1.12 |
| MNQ | 15 | eod | event | with signal | 5790 | +0.538 | 0.077 | +7.47 | +5.47 | +3.53 | +7.48 | +4.50 |
| MNQ | 60 | h1 | event | against signal | 1340 | -0.008 | 0.039 | -0.92 | -2.92 | -2.37 | -3.53 | -2.53 |
| MNQ | 60 | h2 | event | against signal | 1340 | -0.007 | 0.039 | -0.44 | -2.44 | -2.84 | -2.02 | -1.74 |
| MNQ | 60 | h4 | event | against signal | 1340 | -0.014 | 0.039 | +0.18 | -1.82 | -3.42 | -0.09 | -0.60 |
| MNQ | 60 | h8 | event | against signal | 1340 | -0.013 | 0.039 | -1.00 | -3.00 | -2.84 | -3.18 | -0.68 |
| MNQ | 60 | h16 | event | against signal | 1340 | +0.009 | 0.039 | -1.98 | -3.98 | -2.57 | -5.49 | -0.77 |
| MNQ | 60 | eod | event | against signal | 1340 | +0.003 | 0.039 | -1.60 | -3.60 | -2.86 | -4.39 | -0.70 |
| MYM | 5 | h1 | event | with signal | 8221 | -0.005 | 0.166 | -0.14 | -2.14 | +nan | -2.14 | -2.04 |
| MYM | 5 | h2 | event | with signal | 8221 | -0.009 | 0.166 | -0.15 | -2.15 | +nan | -2.15 | -2.03 |
| MYM | 5 | h4 | event | with signal | 8221 | -0.007 | 0.166 | -0.25 | -2.25 | +nan | -2.25 | -2.12 |
| MYM | 5 | h8 | event | against signal | 8221 | +0.012 | 0.166 | +0.44 | -1.56 | +nan | -1.56 | -1.65 |
| MYM | 5 | h16 | event | with signal | 8221 | +0.014 | 0.166 | -0.53 | -2.53 | +nan | -2.53 | -2.49 |
| MYM | 5 | eod | event | with signal | 8221 | +0.440 | 0.166 | +3.68 | +1.68 | +nan | +1.68 | +1.05 |
| MYM | 15 | h1 | event | against signal | 2973 | +0.020 | 0.098 | +0.18 | -1.82 | +nan | -1.82 | -1.93 |
| MYM | 15 | h2 | event | against signal | 2973 | +0.009 | 0.098 | +0.31 | -1.69 | +nan | -1.69 | -1.77 |
| MYM | 15 | h4 | event | with signal | 2973 | +0.013 | 0.098 | -0.03 | -2.03 | +nan | -2.03 | -2.03 |
| MYM | 15 | h8 | event | with signal | 2973 | +0.033 | 0.098 | +0.86 | -1.14 | +nan | -1.14 | -1.19 |
| MYM | 15 | h16 | event | against signal | 2973 | +0.047 | 0.098 | -0.71 | -2.71 | +nan | -2.71 | -2.88 |
| MYM | 15 | eod | event | against signal | 2973 | -0.032 | 0.098 | -4.25 | -6.25 | +nan | -6.25 | -6.21 |
| MYM | 60 | h1 | event | with signal | 644 | +0.030 | 0.050 | +0.92 | -1.08 | +nan | -1.08 | -1.23 |
| MYM | 60 | h2 | event | with signal | 644 | +0.011 | 0.050 | +0.13 | -1.87 | +nan | -1.87 | -1.92 |
| MYM | 60 | h4 | event | with signal | 644 | +0.073 | 0.050 | +3.26 | +1.26 | +nan | +1.26 | +1.04 |
| MYM | 60 | h8 | event | with signal | 644 | +0.215 | 0.050 | +6.71 | +4.71 | +nan | +4.71 | +4.03 |
| MYM | 60 | h16 | event | with signal | 644 | +0.283 | 0.050 | +9.71 | +7.71 | +nan | +7.71 | +5.97 |
| MYM | 60 | eod | event | with signal | 644 | +0.288 | 0.050 | +9.19 | +7.19 | +nan | +7.19 | +5.36 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.181 | +0.288 | +0.293 | +0.259 | -0.661 | +0.000 | -0.027 | -0.021 | -0.013 | +0.018 | -0.019 |
| MES | 15 | +0.220 | +0.295 | +0.286 | +0.253 | -0.656 | +0.000 | -0.034 | -0.024 | -0.001 | -0.012 | -0.066 |
| MES | 60 | +0.352 | +0.268 | +0.336 | +0.275 | -0.694 | +0.000 | +0.003 | +0.003 | -0.041 | -0.059 | -0.021 |
| MNQ | 5 | +0.234 | +0.304 | +0.300 | +0.262 | -0.651 | +0.000 | -0.026 | -0.017 | -0.003 | +0.001 | +0.004 |
| MNQ | 15 | +0.218 | +0.308 | +0.311 | +0.268 | -0.659 | +0.000 | +0.005 | +0.029 | +0.066 | +0.040 | +0.054 |
| MNQ | 60 | +0.265 | +0.282 | +0.356 | +0.300 | -0.680 | +0.000 | -0.004 | -0.012 | -0.042 | -0.066 | -0.268 |
| MYM | 5 | +0.160 | +0.265 | +0.280 | +0.247 | -0.649 | +0.000 | -0.007 | -0.009 | -0.001 | +0.000 | +0.025 |
| MYM | 15 | +0.159 | +0.281 | +0.276 | +0.250 | -0.642 | +0.000 | -0.017 | -0.005 | +0.018 | +0.055 | +0.008 |
| MYM | 60 | +0.200 | +0.124 | +0.276 | +0.258 | -0.710 | +0.000 | +0.026 | +0.002 | +0.082 | +0.374 | -0.135 |

## Calibration

- MES 5-min: 1036271 bars, 13287 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 5703 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 1447 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 15496 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 5790 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 1340 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 8221 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 2973 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 644 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36179 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
