# Impact card: tod_europe_02_08

bar closes in the europe_02_08 block (ET) vs all other bars [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.225 R20 over the rest of the session (to 16:45), p=0.12; we would catch an effect of 0.016 R20 or more 80% of the time).
- MES 5-min size: the market moves 46% MORE after the event than after matched bars over the rest of the session (to 16:45) (+4.549 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.03 at recent bar sizes, 90% range up to $0.24); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.094 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.032 R20 or more 80% of the time).
- MES 15-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.081 R20, CONFIRMED, q=2.37e-113, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.97 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.178 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.006 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.052 R20 or more 80% of the time).
- MES 60-min size: the market moves 28% MORE after the event than after matched bars over the next 16 bars (16 h) (+0.574 R20, CONFIRMED, q=5.44e-205, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.23 at recent bar sizes, 90% range up to $3.78); about 1.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.279 R20 over the rest of the session (to 16:45), p=0.084; we would catch an effect of 0.020 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 49% MORE after the event than after matched bars over the rest of the session (to 16:45) (+6.104 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.01 at recent bar sizes, 90% range up to $0.88); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.029 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.062 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 14% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.075 R20, CONFIRMED, q=2.31e-57, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.67 at recent bar sizes, 90% range up to $3.00); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.010 R20 over the next 1 bar (1 h), p=0.43; we would catch an effect of 0.053 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 56% MORE after the event than after matched bars over the next 8 bars (8 h) (+0.884 R20, CONFIRMED, q=1.75e-234, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.64 at recent bar sizes, 90% range up to $7.60); about 101.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.118 R20 over the next 16 bars (80 min), p=0.31; we would catch an effect of 0.033 R20 or more 80% of the time).
- MYM 5-min size: the market moves 48% MORE after the event than after matched bars over the rest of the session (to 16:45) (+5.648 R20, CONFIRMED, q=8.01e-277, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.80 at recent bar sizes, 90% range up to $0.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.025 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.065 R20 or more 80% of the time).
- MYM 15-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.084 R20, CONFIRMED, q=2.77e-29, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.27 at recent bar sizes, 90% range up to $2.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.004 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MYM 60-min size: the market moves 52% MORE after the event than after matched bars over the next 8 bars (8 h) (+0.799 R20, CONFIRMED, q=3.11e-116, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.12 at recent bar sizes, 90% range up to $4.90); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.003 | +0.000 .. +0.006 | +0.0022 | 0.027 / 0.025 / 0.74 | nan |  |  | 12/16 | +0.005 | +0.002 |  | +2.0 / +2.2 |  |
| MES | 5 | h2 | +0.004 | -0.002 .. +0.009 | +0.0018 | 0.17 / 0.17 / 0.86 | nan |  |  | 10/16 | +0.005 | +0.002 |  | +1.7 / +1.4 |  |
| MES | 5 | h4 | +0.004 | -0.007 .. +0.015 | +0.0014 | 0.44 / 0.44 / 0.93 | nan |  |  | 10/16 | +0.005 | +0.003 |  | +1.3 / +0.8 | 0.016 |
| MES | 5 | h8 | +0.002 | -0.019 .. +0.024 | +0.0005 | 0.83 / 0.82 / 0.98 | nan |  |  | 9/16 | +0.003 | +0.002 |  | +0.5 / +0.2 |  |
| MES | 5 | h16 | -0.016 | -0.063 .. +0.030 | -0.0025 | 0.5 / 0.48 / 0.9 | nan |  |  | 9/16 | -0.013 | -0.019 |  | -2.2 / -0.7 |  |
| MES | 5 | eod * | +0.225 | +0.035 .. +0.415 | +0.0068 | 0.02 / 0.018 / 0.79 | nan | 1 | 0.978 | 15/16 | +0.262 | +0.188 | False | +6.3 / +2.3 |  |
| MES | 15 | h1 | -0.001 | -0.006 .. +0.005 | -0.0003 | 0.85 / 0.85 / 0.84 | nan |  |  | 7/16 | +0.001 | -0.002 |  | -0.2 / -0.2 |  |
| MES | 15 | h2 | -0.002 | -0.013 .. +0.009 | -0.0008 | 0.72 / 0.71 / 0.9 | nan |  |  | 6/16 | -0.000 | -0.004 |  | -0.4 / -0.4 |  |
| MES | 15 | h4 | -0.008 | -0.030 .. +0.015 | -0.0022 | 0.5 / 0.48 / 0.95 | nan |  |  | 9/16 | -0.010 | -0.006 |  | -1.2 / -0.7 | 0.032 |
| MES | 15 | h8 | -0.018 | -0.062 .. +0.025 | -0.0036 | 0.41 / 0.39 / 0.99 | nan |  |  | 9/16 | -0.024 | -0.013 |  | -1.8 / -0.8 |  |
| MES | 15 | h16 | -0.034 | -0.118 .. +0.051 | -0.0046 | 0.43 / 0.43 / 0.96 | nan |  |  | 8/16 | -0.040 | -0.027 |  | -2.1 / -0.8 |  |
| MES | 15 | eod * | -0.094 | -0.307 .. +0.120 | -0.0049 | 0.39 / 0.38 / 0.97 | nan | 1 | 1 | 9/16 | +0.002 | -0.189 | False | -2.3 / -0.9 |  |
| MES | 60 | h1 * | -0.006 | -0.016 .. +0.005 | -0.0033 | 0.29 / 0.29 / 0.99 | nan | 1 | 1 | 9/16 | -0.008 | -0.003 | False | -1.0 / -1.1 |  |
| MES | 60 | h2 | -0.007 | -0.026 .. +0.012 | -0.0028 | 0.47 / 0.47 / 1 | nan |  |  | 7/16 | -0.016 | +0.002 |  | -0.8 / -0.7 |  |
| MES | 60 | h4 | -0.018 | -0.053 .. +0.018 | -0.0050 | 0.34 / 0.33 / 0.98 | nan |  |  | 9/16 | -0.033 | -0.002 |  | -1.4 / -1.0 | 0.052 |
| MES | 60 | h8 | -0.005 | -0.070 .. +0.060 | -0.0010 | 0.88 / 0.88 / 0.97 | nan |  |  | 8/16 | -0.016 | +0.006 |  | -0.3 / -0.2 |  |
| MES | 60 | h16 | +0.018 | -0.024 .. +0.060 | +0.0029 | 0.39 / 0.41 / 0.9 | nan |  |  | 9/16 | +0.012 | +0.025 |  | +0.8 / +0.9 |  |
| MES | 60 | eod | -0.005 | -0.041 .. +0.031 | -0.0007 | 0.79 / 0.79 / 0.84 | nan |  |  | 8/16 | -0.017 | +0.007 |  | -0.2 / -0.3 |  |
| MNQ | 5 | h1 | +0.003 | -0.000 .. +0.006 | +0.0016 | 0.073 / 0.073 / 0.78 | nan |  |  | 11/16 | +0.004 | +0.002 |  | +1.6 / +1.8 |  |
| MNQ | 5 | h2 | +0.005 | -0.002 .. +0.012 | +0.0016 | 0.16 / 0.16 / 0.79 | nan |  |  | 9/16 | +0.004 | +0.006 |  | +1.7 / +1.4 |  |
| MNQ | 5 | h4 | -0.000 | -0.014 .. +0.014 | -0.0000 | 0.98 / 0.98 / 0.88 | nan |  |  | 8/16 | +0.002 | -0.002 |  | -0.0 / -0.0 | 0.020 |
| MNQ | 5 | h8 | -0.016 | -0.055 .. +0.024 | -0.0023 | 0.45 / 0.44 / 0.99 | nan |  |  | 9/16 | -0.004 | -0.027 |  | -1.9 / -0.8 |  |
| MNQ | 5 | h16 | -0.048 | -0.135 .. +0.039 | -0.0050 | 0.28 / 0.27 / 0.97 | nan |  |  | 9/16 | -0.018 | -0.077 |  | -3.9 / -1.1 |  |
| MNQ | 5 | eod * | +0.279 | +0.060 .. +0.499 | +0.0062 | 0.013 / 0.014 / 0.81 | nan | 1 | 0.939 | 13/16 | +0.242 | +0.316 | False | +5.7 / +2.5 |  |
| MNQ | 15 | h1 | -0.003 | -0.010 .. +0.004 | -0.0014 | 0.39 / 0.38 / 0.77 | nan |  |  | 9/16 | -0.003 | -0.004 |  | -0.8 / -0.9 |  |
| MNQ | 15 | h2 | -0.005 | -0.018 .. +0.007 | -0.0015 | 0.41 / 0.41 / 0.85 | nan |  |  | 9/16 | -0.004 | -0.006 |  | -0.9 / -0.8 |  |
| MNQ | 15 | h4 * | -0.029 | -0.072 .. +0.014 | -0.0050 | 0.18 / 0.17 / 0.98 | nan | 1 | 1 | 12/16 | -0.014 | -0.045 | False | -2.5 / -1.3 | 0.062 |
| MNQ | 15 | h8 | -0.049 | -0.133 .. +0.035 | -0.0064 | 0.25 / 0.25 / 0.99 | nan |  |  | 8/16 | -0.008 | -0.089 |  | -2.7 / -1.1 |  |
| MNQ | 15 | h16 | -0.057 | -0.179 .. +0.064 | -0.0061 | 0.36 / 0.36 / 0.98 | nan |  |  | 8/16 | +0.008 | -0.121 |  | -2.5 / -0.9 |  |
| MNQ | 15 | eod | -0.107 | -0.406 .. +0.193 | -0.0040 | 0.48 / 0.48 / 0.98 | nan |  |  | 9/16 | +0.053 | -0.265 |  | -1.7 / -0.7 |  |
| MNQ | 60 | h1 * | -0.010 | -0.020 .. +0.001 | -0.0053 | 0.069 / 0.072 / 0.99 | nan | 1 | 1 | 12/16 | -0.009 | -0.010 | False | -1.7 / -1.8 |  |
| MNQ | 60 | h2 | -0.012 | -0.031 .. +0.007 | -0.0046 | 0.2 / 0.21 / 0.98 | nan |  |  | 11/16 | -0.012 | -0.012 |  | -1.4 / -1.3 |  |
| MNQ | 60 | h4 | -0.026 | -0.063 .. +0.010 | -0.0070 | 0.16 / 0.16 / 1 | nan |  |  | 11/16 | -0.027 | -0.025 |  | -1.9 / -1.4 | 0.053 |
| MNQ | 60 | h8 | -0.019 | -0.087 .. +0.049 | -0.0037 | 0.58 / 0.59 / 0.98 | nan |  |  | 9/16 | -0.023 | -0.015 |  | -0.9 / -0.5 |  |
| MNQ | 60 | h16 | +0.013 | -0.031 .. +0.057 | +0.0019 | 0.56 / 0.57 / 0.9 | nan |  |  | 9/16 | +0.017 | +0.010 |  | +0.5 / +0.6 |  |
| MNQ | 60 | eod | -0.017 | -0.054 .. +0.021 | -0.0024 | 0.38 / 0.39 / 0.84 | nan |  |  | 10/16 | -0.020 | -0.013 |  | -0.6 / -0.9 |  |
| MYM | 5 | h1 | +0.001 | -0.004 .. +0.006 | +0.0004 | 0.74 / 0.75 / 0.87 | nan |  |  | 4/8 | n/a | +0.001 |  | +0.3 / +0.3 |  |
| MYM | 5 | h2 | +0.000 | -0.011 .. +0.012 | +0.0000 | 0.98 / 0.98 / 0.84 | nan |  |  | 3/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 5 | h4 | -0.005 | -0.028 .. +0.019 | -0.0009 | 0.7 / 0.71 / 0.87 | nan |  |  | 5/8 | n/a | -0.005 |  | -0.7 / -0.4 | 0.033 |
| MYM | 5 | h8 | -0.041 | -0.084 .. +0.001 | -0.0055 | 0.058 / 0.053 / 1 | nan |  |  | 7/8 | n/a | -0.041 |  | -3.3 / -1.9 |  |
| MYM | 5 | h16 * | -0.118 | -0.237 .. +0.001 | -0.0124 | 0.052 / 0.041 / 0.92 | nan | 1 | 1 | 7/8 | n/a | -0.118 | False | -6.4 / -1.9 |  |
| MYM | 5 | eod | -0.098 | -0.377 .. +0.181 | -0.0023 | 0.49 / 0.5 / 0.9 | nan |  |  | 5/8 | n/a | -0.098 |  | -1.5 / -0.7 |  |
| MYM | 15 | h1 | +0.000 | -0.009 .. +0.009 | +0.0000 | 1 / 1 / 0.68 | nan |  |  | 4/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 15 | h2 | -0.001 | -0.018 .. +0.017 | -0.0002 | 0.95 / 0.95 / 0.72 | nan |  |  | 5/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 15 | h4 * | -0.025 | -0.069 .. +0.020 | -0.0042 | 0.28 / 0.25 / 0.78 | nan | 1 | 1 | 7/8 | n/a | -0.025 | False | -1.4 / -1.1 | 0.065 |
| MYM | 15 | h8 | -0.061 | -0.184 .. +0.062 | -0.0079 | 0.33 / 0.32 / 0.82 | nan |  |  | 6/8 | n/a | -0.061 |  | -2.2 / -1.0 |  |
| MYM | 15 | h16 | -0.109 | -0.344 .. +0.127 | -0.0100 | 0.37 / 0.37 / 0.86 | nan |  |  | 5/8 | n/a | -0.109 |  | -2.8 / -0.9 |  |
| MYM | 15 | eod | -0.194 | -0.671 .. +0.282 | -0.0074 | 0.42 / 0.43 / 0.98 | nan |  |  | 4/8 | n/a | -0.194 |  | -2.2 / -0.8 |  |
| MYM | 60 | h1 * | -0.004 | -0.019 .. +0.010 | -0.0022 | 0.58 / 0.6 / 1 | nan | 1 | 1 | 6/8 | n/a | -0.004 | False | -0.5 / -0.6 |  |
| MYM | 60 | h2 | +0.000 | -0.026 .. +0.026 | +0.0000 | 1 / 1 / 0.97 | nan |  |  | 5/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 60 | h4 | -0.013 | -0.065 .. +0.039 | -0.0036 | 0.62 / 0.63 / 0.98 | nan |  |  | 4/8 | n/a | -0.013 |  | -0.7 / -0.5 | 0.076 |
| MYM | 60 | h8 | -0.024 | -0.121 .. +0.073 | -0.0048 | 0.63 / 0.63 / 1 | nan |  |  | 5/8 | n/a | -0.024 |  | -0.8 / -0.5 |  |
| MYM | 60 | h16 | +0.015 | -0.048 .. +0.077 | +0.0023 | 0.64 / 0.64 / 1 | nan |  |  | 4/8 | n/a | +0.015 |  | +0.4 / +0.5 |  |
| MYM | 60 | eod | -0.001 | -0.055 .. +0.052 | -0.0002 | 0.96 / 0.96 / 0.98 | nan |  |  | 4/8 | n/a | -0.001 |  | -0.0 / -0.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.024 | +0.020 .. +0.028 | +4.8% | +0.037 | 3.2e-37 |  | 14/16 |
| MES | 5 | h2 | +0.034 | +0.027 .. +0.040 | +4.8% | +0.058 | 2e-26 |  | 14/16 |
| MES | 5 | h4 | +0.046 | +0.035 .. +0.057 | +4.6% | +0.087 | 2.9e-16 |  | 14/16 |
| MES | 5 | h8 | +0.080 | +0.060 .. +0.100 | +5.5% | +0.177 | 7.1e-15 |  | 14/16 |
| MES | 5 | h16 | +0.183 | +0.146 .. +0.220 | +8.7% | +0.412 | 2.4e-22 |  | 14/16 |
| MES | 5 | eod * | +4.549 | +4.358 .. +4.740 | +45.6% | +8.926 | 0 | 0 | 16/16 |
| MES | 15 | h1 * | +0.081 | +0.074 .. +0.088 | +15.9% | +0.164 | 1.5e-116 | 2.37e-113 | 16/16 |
| MES | 15 | h2 | +0.102 | +0.089 .. +0.114 | +13.9% | +0.218 | 4e-60 |  | 15/16 |
| MES | 15 | h4 | +0.163 | +0.140 .. +0.187 | +15.5% | +0.355 | 4.2e-43 |  | 15/16 |
| MES | 15 | h8 | +0.235 | +0.200 .. +0.271 | +15.3% | +0.518 | 7.2e-38 |  | 16/16 |
| MES | 15 | h16 | +0.692 | +0.625 .. +0.759 | +30.3% | +1.437 | 1.9e-90 |  | 16/16 |
| MES | 15 | eod | +0.457 | +0.278 .. +0.635 | +8.3% | +0.873 | 5.2e-07 |  | 13/16 |
| MES | 60 | h1 | -0.059 | -0.069 .. -0.048 | -11.4% | -0.114 | 1.3e-28 |  | 15/16 |
| MES | 60 | h2 | -0.025 | -0.041 .. -0.009 | -3.4% | -0.029 | 0.0021 |  | 11/16 |
| MES | 60 | h4 | +0.208 | +0.181 .. +0.235 | +19.6% | +0.436 | 8.3e-51 |  | 16/16 |
| MES | 60 | h8 | +0.718 | +0.672 .. +0.764 | +47.6% | +1.461 | 2.4e-205 |  | 16/16 |
| MES | 60 | h16 * | +0.574 | +0.537 .. +0.610 | +27.9% | +1.108 | 2.2e-208 | 5.44e-205 | 16/16 |
| MES | 60 | eod | +0.428 | +0.397 .. +0.459 | +19.8% | +0.846 | 1e-162 |  | 16/16 |
| MNQ | 5 | h1 | +0.026 | +0.020 .. +0.032 | +4.9% | +0.029 | 2.5e-18 |  | 13/16 |
| MNQ | 5 | h2 | +0.035 | +0.024 .. +0.045 | +4.5% | +0.054 | 5.1e-11 |  | 13/16 |
| MNQ | 5 | h4 | +0.050 | +0.035 .. +0.065 | +4.5% | +0.087 | 2e-11 |  | 11/16 |
| MNQ | 5 | h8 | +0.091 | +0.060 .. +0.122 | +5.6% | +0.185 | 1e-08 |  | 13/16 |
| MNQ | 5 | h16 | +0.198 | +0.108 .. +0.288 | +8.3% | +0.425 | 1.9e-05 |  | 13/16 |
| MNQ | 5 | eod * | +6.104 | +5.818 .. +6.389 | +48.6% | +12.089 | 0 | 0 | 16/16 |
| MNQ | 15 | h1 * | +0.075 | +0.066 .. +0.084 | +14.1% | +0.155 | 1.9e-60 | 2.31e-57 | 15/16 |
| MNQ | 15 | h2 | +0.088 | +0.072 .. +0.103 | +11.3% | +0.191 | 2.3e-27 |  | 15/16 |
| MNQ | 15 | h4 | +0.137 | +0.113 .. +0.162 | +12.1% | +0.299 | 4.6e-28 |  | 16/16 |
| MNQ | 15 | h8 | +0.225 | +0.151 .. +0.300 | +13.4% | +0.501 | 3.3e-09 |  | 16/16 |
| MNQ | 15 | h16 | +0.849 | +0.726 .. +0.971 | +33.6% | +1.797 | 5.7e-42 |  | 16/16 |
| MNQ | 15 | eod | +0.530 | +0.206 .. +0.853 | +8.3% | +1.020 | 0.0013 |  | 14/16 |
| MNQ | 60 | h1 | -0.107 | -0.117 .. -0.096 | -20.2% | -0.212 | 7.3e-93 |  | 16/16 |
| MNQ | 60 | h2 | -0.049 | -0.065 .. -0.034 | -6.4% | -0.083 | 4.8e-10 |  | 15/16 |
| MNQ | 60 | h4 | +0.258 | +0.230 .. +0.287 | +23.4% | +0.525 | 4.5e-71 |  | 16/16 |
| MNQ | 60 | h8 * | +0.884 | +0.832 .. +0.937 | +55.8% | +1.766 | 6.5e-238 | 1.75e-234 | 16/16 |
| MNQ | 60 | h16 | +0.649 | +0.610 .. +0.688 | +29.6% | +1.248 | 6.9e-238 |  | 16/16 |
| MNQ | 60 | eod | +0.504 | +0.471 .. +0.538 | +21.9% | +0.987 | 3.6e-192 |  | 16/16 |
| MYM | 5 | h1 | +0.027 | +0.019 .. +0.035 | +5.1% | +0.032 | 9.4e-11 |  | 7/8 |
| MYM | 5 | h2 | +0.036 | +0.021 .. +0.052 | +4.8% | +0.055 | 6.7e-06 |  | 6/8 |
| MYM | 5 | h4 | +0.049 | +0.020 .. +0.077 | +4.5% | +0.086 | 0.00079 |  | 6/8 |
| MYM | 5 | h8 | +0.110 | +0.071 .. +0.149 | +6.9% | +0.217 | 3.6e-08 |  | 6/8 |
| MYM | 5 | h16 | +0.272 | +0.164 .. +0.379 | +11.6% | +0.570 | 6.8e-07 |  | 7/8 |
| MYM | 5 | eod * | +5.648 | +5.338 .. +5.957 | +48.2% | +11.192 | 2.3e-280 | 8.01e-277 | 8/8 |
| MYM | 15 | h1 * | +0.084 | +0.070 .. +0.098 | +15.8% | +0.165 | 3.6e-32 | 2.77e-29 | 8/8 |
| MYM | 15 | h2 | +0.099 | +0.072 .. +0.126 | +12.9% | +0.201 | 3.1e-13 |  | 7/8 |
| MYM | 15 | h4 | +0.177 | +0.145 .. +0.209 | +15.9% | +0.339 | 1.6e-27 |  | 8/8 |
| MYM | 15 | h8 | +0.328 | +0.223 .. +0.433 | +20.0% | +0.641 | 4.1e-09 |  | 8/8 |
| MYM | 15 | h16 | +0.949 | +0.741 .. +1.156 | +38.5% | +1.870 | 4.5e-18 |  | 8/8 |
| MYM | 15 | eod | +0.583 | +0.165 .. +1.002 | +9.7% | +1.028 | 0.0078 |  | 8/8 |
| MYM | 60 | h1 | -0.083 | -0.097 .. -0.069 | -15.9% | -0.164 | 8.7e-32 |  | 8/8 |
| MYM | 60 | h2 | -0.011 | -0.033 .. +0.011 | -1.4% | -0.022 | 0.34 |  | 4/8 |
| MYM | 60 | h4 | +0.268 | +0.226 .. +0.311 | +24.8% | +0.530 | 5.7e-35 |  | 8/8 |
| MYM | 60 | h8 * | +0.799 | +0.731 .. +0.866 | +51.6% | +1.633 | 1.9e-119 | 3.11e-116 | 8/8 |
| MYM | 60 | h16 | +0.605 | +0.555 .. +0.656 | +28.5% | +1.163 | 7.7e-119 |  | 8/8 |
| MYM | 60 | eod | +0.461 | +0.417 .. +0.504 | +20.7% | +0.909 | 1.3e-95 |  | 8/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.23 pts | -0.62 .. +0.16 | 0.26 |
| MES | 15 | -0.53 pts | -1.16 .. +0.10 | 0.1 |
| MES | 60 | -0.42 pts | -1.43 .. +0.58 | 0.41 |
| MNQ | 5 | -0.13 pts | -0.52 .. +0.25 | 0.5 |
| MNQ | 15 | -0.83 pts | -1.44 .. -0.23 | 0.0095 |
| MNQ | 60 | -0.27 pts | -1.26 .. +0.72 | 0.6 |
| MYM | 5 | +0.00 pts | -0.57 .. +0.58 | 0.99 |
| MYM | 15 | +0.51 pts | -0.42 .. +1.45 | 0.28 |
| MYM | 60 | -0.02 pts | -1.41 .. +1.38 | 0.98 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 278762 | +0.004 | 0.406 | +0.03 | -3.47 | -3.47 | -3.47 | -3.47 |
| MES | 5 | h2 | event | long | 278762 | +0.008 | 0.406 | +0.06 | -3.44 | -3.45 | -3.44 | -3.47 |
| MES | 5 | h4 | event | long | 278762 | +0.014 | 0.406 | +0.10 | -3.40 | -3.41 | -3.39 | -3.45 |
| MES | 5 | h8 | event | long | 278762 | +0.024 | 0.406 | +0.18 | -3.32 | -3.33 | -3.30 | -3.42 |
| MES | 5 | h16 | event | short | 278762 | -0.033 | 0.406 | -0.29 | -3.79 | -3.76 | -3.83 | -3.58 |
| MES | 5 | eod | event | long | 278762 | +0.502 | 0.406 | +4.12 | +0.62 | -0.35 | +1.60 | +0.25 |
| MES | 15 | h1 | event | short | 92931 | -0.006 | 0.257 | -0.07 | -3.57 | -3.57 | -3.57 | -3.51 |
| MES | 15 | h2 | event | short | 92931 | -0.011 | 0.257 | -0.13 | -3.63 | -3.63 | -3.62 | -3.52 |
| MES | 15 | h4 | event | short | 92931 | -0.019 | 0.257 | -0.23 | -3.73 | -3.72 | -3.75 | -3.53 |
| MES | 15 | h8 | event | short | 92931 | -0.035 | 0.257 | -0.44 | -3.94 | -3.83 | -4.05 | -3.55 |
| MES | 15 | h16 | event | short | 92931 | -0.069 | 0.257 | -0.88 | -4.38 | -4.16 | -4.60 | -3.71 |
| MES | 15 | eod | event | short | 92931 | -0.281 | 0.257 | -4.03 | -7.53 | -6.62 | -8.44 | -5.40 |
| MES | 60 | h1 | event | short | 22861 | -0.005 | 0.095 | -0.21 | -3.71 | -3.62 | -3.80 | -3.53 |
| MES | 60 | h2 | event | short | 22861 | -0.013 | 0.095 | -0.50 | -4.00 | -3.75 | -4.25 | -3.60 |
| MES | 60 | h4 | event | short | 22861 | -0.024 | 0.095 | -0.93 | -4.43 | -4.07 | -4.79 | -3.57 |
| MES | 60 | h8 | event | short | 22861 | -0.067 | 0.095 | -2.58 | -6.08 | -5.25 | -6.90 | -4.40 |
| MES | 60 | h16 | event | long | 22861 | +0.126 | 0.095 | +4.21 | +0.71 | -0.59 | +2.01 | -1.93 |
| MES | 60 | eod | event | short | 22861 | -0.126 | 0.095 | -4.21 | -7.71 | -6.41 | -9.01 | -4.53 |
| MNQ | 5 | h1 | event | long | 278631 | +0.005 | 0.171 | +0.04 | -1.96 | -1.97 | -1.94 | -1.97 |
| MNQ | 5 | h2 | event | long | 278631 | +0.009 | 0.171 | +0.07 | -1.93 | -1.95 | -1.91 | -1.94 |
| MNQ | 5 | h4 | event | short | 278631 | -0.011 | 0.171 | -0.12 | -2.12 | -2.08 | -2.16 | -2.11 |
| MNQ | 5 | h8 | event | short | 278631 | -0.012 | 0.171 | -0.21 | -2.21 | -2.16 | -2.26 | -2.18 |
| MNQ | 5 | h16 | event | short | 278631 | -0.014 | 0.171 | -0.34 | -2.34 | -2.30 | -2.38 | -2.23 |
| MNQ | 5 | eod | event | long | 278631 | +0.687 | 0.171 | +5.22 | +3.22 | +1.14 | +5.30 | +3.86 |
| MNQ | 15 | h1 | event | short | 92919 | -0.006 | 0.107 | -0.09 | -2.09 | -2.06 | -2.12 | -1.99 |
| MNQ | 15 | h2 | event | short | 92919 | -0.011 | 0.107 | -0.16 | -2.16 | -2.12 | -2.20 | -2.03 |
| MNQ | 15 | h4 | event | short | 92919 | -0.006 | 0.107 | -0.26 | -2.26 | -2.22 | -2.29 | -2.03 |
| MNQ | 15 | h8 | event | short | 92919 | -0.018 | 0.107 | -0.39 | -2.39 | -2.42 | -2.37 | -1.93 |
| MNQ | 15 | h16 | event | short | 92919 | -0.052 | 0.107 | -0.62 | -2.62 | -2.84 | -2.39 | -2.11 |
| MNQ | 15 | eod | event | short | 92919 | -0.338 | 0.107 | -5.13 | -7.13 | -5.11 | -9.14 | -4.64 |
| MNQ | 60 | h1 | event | short | 22861 | -0.004 | 0.037 | -0.19 | -2.19 | -2.18 | -2.21 | -1.90 |
| MNQ | 60 | h2 | event | short | 22861 | -0.013 | 0.037 | -0.44 | -2.44 | -2.36 | -2.51 | -1.84 |
| MNQ | 60 | h4 | event | short | 22861 | -0.025 | 0.037 | -0.56 | -2.56 | -2.74 | -2.37 | -1.34 |
| MNQ | 60 | h8 | event | short | 22861 | -0.067 | 0.037 | -2.17 | -4.17 | -3.53 | -4.81 | -1.91 |
| MNQ | 60 | h16 | event | long | 22861 | +0.142 | 0.037 | +4.59 | +2.59 | +0.83 | +4.34 | -0.91 |
| MNQ | 60 | eod | event | short | 22861 | -0.142 | 0.037 | -4.59 | -6.59 | -4.83 | -8.34 | -2.26 |
| MYM | 5 | h1 | event | long | 139269 | +0.002 | 0.215 | +0.02 | -1.98 | +nan | -1.98 | -1.98 |
| MYM | 5 | h2 | event | long | 139269 | +0.003 | 0.215 | +0.03 | -1.97 | +nan | -1.97 | -1.97 |
| MYM | 5 | h4 | event | short | 139269 | -0.002 | 0.215 | -0.04 | -2.04 | +nan | -2.04 | -2.05 |
| MYM | 5 | h8 | event | short | 139269 | +0.018 | 0.215 | -0.04 | -2.04 | +nan | -2.04 | -2.04 |
| MYM | 5 | h16 | event | short | 139269 | +0.062 | 0.215 | -0.05 | -2.05 | +nan | -2.05 | -2.01 |
| MYM | 5 | eod | event | short | 139269 | -0.116 | 0.215 | -3.65 | -5.65 | +nan | -5.65 | -5.55 |
| MYM | 15 | h1 | event | long | 46446 | +0.003 | 0.134 | +0.03 | -1.97 | +nan | -1.97 | -2.00 |
| MYM | 15 | h2 | event | short | 46446 | -0.001 | 0.134 | -0.03 | -2.03 | +nan | -2.03 | -2.02 |
| MYM | 15 | h4 | event | short | 46446 | +0.016 | 0.134 | -0.05 | -2.05 | +nan | -2.05 | -2.05 |
| MYM | 15 | h8 | event | short | 46446 | +0.045 | 0.134 | -0.16 | -2.16 | +nan | -2.16 | -2.25 |
| MYM | 15 | h16 | event | short | 46446 | +0.105 | 0.134 | -0.36 | -2.36 | +nan | -2.36 | -2.89 |
| MYM | 15 | eod | event | short | 46446 | +0.069 | 0.134 | -3.45 | -5.45 | +nan | -5.45 | -5.91 |
| MYM | 60 | h1 | event | short | 11429 | -0.001 | 0.048 | -0.16 | -2.16 | +nan | -2.16 | -2.07 |
| MYM | 60 | h2 | event | long | 11429 | +0.007 | 0.048 | +0.43 | -1.57 | +nan | -1.57 | -1.77 |
| MYM | 60 | h4 | event | short | 11429 | -0.003 | 0.048 | -0.62 | -2.62 | +nan | -2.62 | -2.18 |
| MYM | 60 | h8 | event | short | 11429 | -0.007 | 0.048 | -1.65 | -3.65 | +nan | -3.65 | -2.80 |
| MYM | 60 | h16 | event | long | 11429 | +0.050 | 0.048 | +3.53 | +1.53 | +nan | +1.53 | +0.05 |
| MYM | 60 | eod | event | short | 11429 | -0.050 | 0.048 | -3.53 | -5.53 | +nan | -5.53 | -3.46 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.001 | -0.002 | -0.002 | -0.002 | -0.001 | +0.000 | -0.000 | -0.001 | +0.001 | +0.002 | +0.003 |
| MES | 15 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 |
| MES | 60 | +nan | +0.000 | -0.000 | +0.000 | +0.000 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +nan |
| MNQ | 5 | -0.003 | -0.005 | -0.004 | -0.003 | -0.002 | +0.000 | +0.001 | +0.001 | +0.005 | +0.005 | +0.002 |
| MNQ | 15 | +0.000 | +0.000 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | +0.000 |
| MNQ | 60 | +nan | -0.000 | -0.000 | +0.000 | -0.000 | +0.000 | -0.000 | +0.000 | -0.000 | -0.000 | +nan |
| MYM | 5 | +0.001 | +0.001 | +0.001 | +0.001 | +0.001 | +0.000 | +0.001 | +0.001 | +0.001 | +0.001 | +0.001 |
| MYM | 15 | -0.000 | -0.000 | -0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 |
| MYM | 60 | +nan | +0.000 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +nan |

## Calibration

- MES 5-min: 1036271 bars, 278762 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 92931 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 22861 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 278631 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 92919 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 22861 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 139269 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 46446 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 11429 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
