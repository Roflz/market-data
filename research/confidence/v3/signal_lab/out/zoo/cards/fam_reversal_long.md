# Impact card: fam_reversal_long

bullish reversal patterns only (long side) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.016 R20 over the next 8 bars (40 min), p=0.2; we would catch an effect of 0.014 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.013).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.24 at recent bar sizes, 90% range up to $0.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.007 R20 over the next 1 bar (15 min), p=0.67; we would catch an effect of 0.028 R20 or more 80% of the time).
- MES 15-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.011 R20, possible, q=0.11, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.27 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.130 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.011 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.056 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.029).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.49 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.025 R20 over the next 16 bars (80 min), p=0.98; we would catch an effect of 0.016 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.58).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.62 at recent bar sizes, 90% range up to $0.64); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.186 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.041 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.52).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $8.27 at recent bar sizes, 90% range up to $1.39); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.008 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.061 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.87).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.75 at recent bar sizes, 90% range up to $5.66); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.068 R20 over the next 16 bars (80 min), p=0.033; we would catch an effect of 0.033 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.77).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.80 at recent bar sizes, 90% range up to $0.73); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.084 R20 over the next 16 bars (4 h), p=0.49; we would catch an effect of 0.046 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.97).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.70 at recent bar sizes, 90% range up to $1.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.035 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.084 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.7).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.49 at recent bar sizes, 90% range up to $5.63); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.001 | -0.003 .. +0.005 | +0.0005 | 0.63 / 0.61 / 0.59 | 0.576 |  |  | 10/16 | -0.003 | +0.005 |  | +0.5 / +0.5 |  |
| MES | 5 | h2 | +0.002 | -0.003 .. +0.008 | +0.0009 | 0.41 / 0.4 / 0.36 | 0.365 |  |  | 9/16 | -0.002 | +0.007 |  | +0.8 / +0.8 |  |
| MES | 5 | h4 | +0.003 | -0.005 .. +0.012 | +0.0009 | 0.45 / 0.46 / 0.39 | 0.389 |  |  | 10/16 | -0.002 | +0.008 |  | +0.8 / +0.8 | 0.014 |
| MES | 5 | h8 * | +0.016 | +0.001 .. +0.031 | +0.0029 | 0.031 / 0.034 / 0.0047 | 0.00521 | 1 | 0.996 | 14/16 | +0.016 | +0.016 | False | +2.8 / +2.2 |  |
| MES | 5 | h16 | +0.019 | -0.007 .. +0.045 | +0.0024 | 0.16 / 0.17 / 0.021 | 0.0214 |  |  | 12/16 | +0.013 | +0.025 |  | +2.3 / +1.4 |  |
| MES | 5 | eod | +0.146 | -0.267 .. +0.559 | +0.0037 | 0.49 / 0.51 / 0.0055 | 0.00469 |  |  | 11/16 | +0.027 | +0.264 |  | +3.3 / +0.7 |  |
| MES | 15 | h1 * | -0.007 | -0.015 .. +0.001 | -0.0033 | 0.079 / 0.078 / 0.082 | 0.0789 | 1 | 1 | 11/16 | -0.006 | -0.008 | False | -1.8 / -1.8 |  |
| MES | 15 | h2 | +0.004 | -0.007 .. +0.015 | +0.0013 | 0.47 / 0.47 / 0.48 | 0.473 |  |  | 10/16 | +0.005 | +0.003 |  | +0.7 / +0.7 |  |
| MES | 15 | h4 | +0.011 | -0.008 .. +0.030 | +0.0024 | 0.25 / 0.25 / 0.18 | 0.182 |  |  | 10/16 | +0.010 | +0.012 |  | +1.4 / +1.1 | 0.028 |
| MES | 15 | h8 | +0.020 | -0.013 .. +0.053 | +0.0030 | 0.23 / 0.22 / 0.09 | 0.0878 |  |  | 12/16 | +0.016 | +0.024 |  | +1.7 / +1.2 |  |
| MES | 15 | h16 | +0.022 | -0.036 .. +0.081 | +0.0024 | 0.45 / 0.45 / 0.19 | 0.191 |  |  | 11/16 | +0.039 | +0.006 |  | +1.3 / +0.8 |  |
| MES | 15 | eod | +0.069 | -0.164 .. +0.302 | +0.0028 | 0.56 / 0.58 / 0.13 | 0.136 |  |  | 9/16 | +0.043 | +0.094 |  | +1.6 / +0.6 |  |
| MES | 60 | h1 | -0.001 | -0.017 .. +0.015 | -0.0004 | 0.91 / 0.91 / 0.91 | 0.913 |  |  | 9/16 | -0.001 | -0.000 |  | -0.1 / -0.1 |  |
| MES | 60 | h2 | -0.003 | -0.028 .. +0.021 | -0.0011 | 0.78 / 0.78 / 0.76 | 0.764 |  |  | 8/16 | -0.001 | -0.006 |  | -0.3 / -0.3 |  |
| MES | 60 | h4 * | -0.011 | -0.050 .. +0.028 | -0.0025 | 0.58 / 0.59 / 0.5 | 0.495 | 1 | 1 | 12/16 | -0.026 | +0.004 | False | -0.6 / -0.6 | 0.056 |
| MES | 60 | h8 | -0.007 | -0.072 .. +0.057 | -0.0012 | 0.82 / 0.83 / 0.74 | 0.744 |  |  | 11/16 | -0.023 | +0.008 |  | -0.3 / -0.2 |  |
| MES | 60 | h16 | -0.019 | -0.113 .. +0.074 | -0.0025 | 0.68 / 0.69 / 0.49 | 0.487 |  |  | 9/16 | -0.029 | -0.010 |  | -0.7 / -0.4 |  |
| MES | 60 | eod | -0.016 | -0.116 .. +0.083 | -0.0020 | 0.75 / 0.75 / 0.57 | 0.573 |  |  | 10/16 | -0.039 | +0.006 |  | -0.5 / -0.3 |  |
| MNQ | 5 | h1 | -0.000 | -0.005 .. +0.004 | -0.0002 | 0.85 / 0.85 / 0.82 | 0.83 |  |  | 9/16 | +0.002 | -0.003 |  | -0.2 / -0.2 |  |
| MNQ | 5 | h2 | -0.001 | -0.008 .. +0.006 | -0.0001 | 0.87 / 0.87 / 0.89 | 0.89 |  |  | 8/16 | +0.003 | -0.004 |  | -0.2 / -0.2 |  |
| MNQ | 5 | h4 | +0.002 | -0.008 .. +0.013 | +0.0004 | 0.66 / 0.66 / 0.69 | 0.669 |  |  | 8/16 | +0.009 | -0.005 |  | +0.5 / +0.4 | 0.016 |
| MNQ | 5 | h8 | +0.010 | -0.008 .. +0.028 | +0.0011 | 0.29 / 0.29 / 0.28 | 0.269 |  |  | 9/16 | +0.024 | -0.005 |  | +1.3 / +1.1 |  |
| MNQ | 5 | h16 * | +0.025 | -0.010 .. +0.059 | +0.0020 | 0.16 / 0.16 / 0.058 | 0.0591 | 1 | 1 | 11/16 | +0.040 | +0.010 | False | +2.3 / +1.4 |  |
| MNQ | 5 | eod | +0.194 | -0.311 .. +0.699 | +0.0033 | 0.45 / 0.47 / 0.0035 | 0.00443 |  |  | 10/16 | +0.060 | +0.327 |  | +3.2 / +0.8 |  |
| MNQ | 15 | h1 | -0.002 | -0.011 .. +0.008 | -0.0006 | 0.73 / 0.73 / 0.76 | 0.746 |  |  | 11/16 | -0.007 | +0.004 |  | -0.4 / -0.3 |  |
| MNQ | 15 | h2 | +0.006 | -0.008 .. +0.019 | +0.0012 | 0.42 / 0.42 / 0.5 | 0.476 |  |  | 9/16 | +0.004 | +0.007 |  | +0.9 / +0.8 |  |
| MNQ | 15 | h4 | +0.006 | -0.017 .. +0.028 | +0.0007 | 0.62 / 0.62 / 0.7 | 0.679 |  |  | 9/16 | -0.004 | +0.015 |  | +0.6 / +0.5 | 0.041 |
| MNQ | 15 | h8 | +0.000 | -0.036 .. +0.036 | +0.0000 | 1 / 1 / 1 | 0.995 |  |  | 8/16 | -0.023 | +0.023 |  | +0.0 / +0.0 |  |
| MNQ | 15 | h16 | +0.035 | -0.028 .. +0.098 | +0.0028 | 0.27 / 0.29 / 0.13 | 0.125 |  |  | 12/16 | +0.028 | +0.042 |  | +1.7 / +1.1 |  |
| MNQ | 15 | eod * | +0.186 | -0.075 .. +0.447 | +0.0051 | 0.16 / 0.18 / 0.0046 | 0.00443 | 1 | 1 | 11/16 | +0.197 | +0.175 | False | +3.6 / +1.4 |  |
| MNQ | 60 | h1 | +0.001 | -0.017 .. +0.020 | +0.0006 | 0.87 / 0.87 / 0.87 | 0.869 |  |  | 10/16 | +0.010 | -0.007 |  | +0.2 / +0.2 |  |
| MNQ | 60 | h2 * | +0.008 | -0.019 .. +0.035 | +0.0024 | 0.56 / 0.55 / 0.51 | 0.519 | 1 | 1 | 10/16 | +0.020 | -0.004 | False | +0.6 / +0.6 |  |
| MNQ | 60 | h4 | -0.002 | -0.043 .. +0.039 | -0.0005 | 0.91 / 0.92 / 0.9 | 0.9 |  |  | 10/16 | +0.008 | -0.013 |  | -0.1 / -0.1 | 0.061 |
| MNQ | 60 | h8 | +0.005 | -0.061 .. +0.071 | +0.0007 | 0.89 / 0.89 / 0.85 | 0.85 |  |  | 10/16 | -0.001 | +0.010 |  | +0.2 / +0.1 |  |
| MNQ | 60 | h16 | -0.007 | -0.104 .. +0.090 | -0.0008 | 0.88 / 0.89 / 0.82 | 0.831 |  |  | 9/16 | -0.027 | +0.013 |  | -0.2 / -0.1 |  |
| MNQ | 60 | eod | -0.008 | -0.111 .. +0.094 | -0.0009 | 0.88 / 0.88 / 0.8 | 0.799 |  |  | 9/16 | -0.028 | +0.012 |  | -0.3 / -0.2 |  |
| MYM | 5 | h1 | +0.003 | -0.004 .. +0.010 | +0.0011 | 0.37 / 0.36 / 0.42 | 0.409 |  |  | 5/8 | n/a | +0.003 |  | +0.9 / +0.9 |  |
| MYM | 5 | h2 | +0.006 | -0.004 .. +0.016 | +0.0013 | 0.27 / 0.25 / 0.36 | 0.354 |  |  | 4/8 | n/a | +0.006 |  | +1.2 / +1.1 |  |
| MYM | 5 | h4 | +0.024 | +0.009 .. +0.040 | +0.0034 | 0.0025 / 0.0017 / 0.019 | 0.0163 |  |  | 7/8 | n/a | +0.024 |  | +3.6 / +3.0 | 0.033 |
| MYM | 5 | h8 | +0.038 | +0.010 .. +0.067 | +0.0039 | 0.0075 / 0.0061 / 0.0082 | 0.00948 |  |  | 5/8 | n/a | +0.038 |  | +3.8 / +2.7 |  |
| MYM | 5 | h16 * | +0.068 | +0.020 .. +0.117 | +0.0054 | 0.0054 / 0.0052 / 0.00025 | 0.00105 | 0.782 | 0.467 | 8/8 | n/a | +0.068 | False | +4.6 / +2.8 |  |
| MYM | 5 | eod | +0.356 | -0.373 .. +1.085 | +0.0062 | 0.34 / 0.34 / 1.9e-05 | 0.000527 |  |  | 7/8 | n/a | +0.356 |  | +4.4 / +1.0 |  |
| MYM | 15 | h1 | -0.011 | -0.023 .. +0.002 | -0.0039 | 0.087 / 0.077 / 0.14 | 0.142 |  |  | 6/8 | n/a | -0.011 |  | -1.8 / -1.7 |  |
| MYM | 15 | h2 | -0.008 | -0.026 .. +0.009 | -0.0018 | 0.35 / 0.35 / 0.48 | 0.462 |  |  | 4/8 | n/a | -0.008 |  | -1.0 / -0.9 |  |
| MYM | 15 | h4 | +0.007 | -0.021 .. +0.035 | +0.0008 | 0.64 / 0.65 / 0.75 | 0.749 |  |  | 5/8 | n/a | +0.007 |  | +0.5 / +0.5 | 0.046 |
| MYM | 15 | h8 | +0.040 | -0.010 .. +0.090 | +0.0039 | 0.11 / 0.11 / 0.11 | 0.11 |  |  | 7/8 | n/a | +0.040 |  | +2.2 / +1.6 |  |
| MYM | 15 | h16 * | +0.084 | -0.010 .. +0.177 | +0.0058 | 0.081 / 0.071 / 0.03 | 0.0285 | 1 | 1 | 6/8 | n/a | +0.084 | False | +3.1 / +1.7 |  |
| MYM | 15 | eod | +0.182 | -0.199 .. +0.563 | +0.0052 | 0.35 / 0.34 / 0.047 | 0.0443 |  |  | 5/8 | n/a | +0.182 |  | +2.7 / +0.9 |  |
| MYM | 60 | h1 | +0.005 | -0.019 .. +0.029 | +0.0021 | 0.7 / 0.71 / 0.69 | 0.683 |  |  | 4/8 | n/a | +0.005 |  | +0.4 / +0.4 |  |
| MYM | 60 | h2 | +0.002 | -0.035 .. +0.039 | +0.0005 | 0.93 / 0.93 / 0.92 | 0.925 |  |  | 3/8 | n/a | +0.002 |  | +0.1 / +0.1 |  |
| MYM | 60 | h4 | +0.009 | -0.051 .. +0.070 | +0.0021 | 0.76 / 0.76 / 0.7 | 0.693 |  |  | 5/8 | n/a | +0.009 |  | +0.4 / +0.3 | 0.084 |
| MYM | 60 | h8 | +0.010 | -0.090 .. +0.111 | +0.0017 | 0.84 / 0.84 / 0.76 | 0.756 |  |  | 3/8 | n/a | +0.010 |  | +0.3 / +0.2 |  |
| MYM | 60 | h16 | +0.018 | -0.116 .. +0.151 | +0.0021 | 0.8 / 0.8 / 0.68 | 0.678 |  |  | 3/8 | n/a | +0.018 |  | +0.4 / +0.3 |  |
| MYM | 60 | eod * | +0.035 | -0.103 .. +0.174 | +0.0041 | 0.62 / 0.63 / 0.42 | 0.424 | 1 | 1 | 4/8 | n/a | +0.035 | False | +0.8 / +0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.004 | +0.001 .. +0.007 | +0.9% | +0.006 | 0.0061 |  | 11/16 |
| MES | 5 | h2 * | +0.007 | +0.003 .. +0.011 | +1.0% | +0.011 | 0.0022 | 0.359 | 10/16 |
| MES | 5 | h4 | +0.009 | +0.003 .. +0.016 | +0.9% | +0.018 | 0.0073 |  | 12/16 |
| MES | 5 | h8 | +0.010 | -0.001 .. +0.021 | +0.7% | +0.018 | 0.074 |  | 12/16 |
| MES | 5 | h16 | +0.010 | -0.007 .. +0.027 | +0.5% | +0.008 | 0.24 |  | 11/16 |
| MES | 5 | eod | -0.067 | -0.211 .. +0.077 | -0.7% | -0.065 | 0.79 |  | 8/16 |
| MES | 15 | h1 * | +0.011 | +0.005 .. +0.016 | +2.1% | +0.022 | 0.00061 | 0.11 | 14/16 |
| MES | 15 | h2 | +0.011 | +0.002 .. +0.019 | +1.5% | +0.024 | 0.012 |  | 11/16 |
| MES | 15 | h4 | +0.012 | -0.000 .. +0.025 | +1.2% | +0.025 | 0.064 |  | 10/16 |
| MES | 15 | h8 | +0.020 | +0.001 .. +0.039 | +1.3% | +0.014 | 0.044 |  | 12/16 |
| MES | 15 | h16 | +0.006 | -0.026 .. +0.038 | +0.3% | -0.021 | 0.71 |  | 9/16 |
| MES | 15 | eod | -0.064 | -0.190 .. +0.062 | -1.2% | -0.074 | 0.32 |  | 10/16 |
| MES | 60 | h1 * | +0.017 | +0.006 .. +0.029 | +3.4% | +0.040 | 0.0049 | 0.722 | 12/16 |
| MES | 60 | h2 | +0.026 | +0.008 .. +0.043 | +3.5% | +0.053 | 0.005 |  | 12/16 |
| MES | 60 | h4 | +0.027 | +0.002 .. +0.052 | +2.6% | +0.068 | 0.033 |  | 11/16 |
| MES | 60 | h8 | +0.035 | +0.003 .. +0.067 | +2.3% | +0.078 | 0.067 |  | 13/16 |
| MES | 60 | h16 | +0.009 | -0.033 .. +0.051 | +0.4% | +0.067 | 0.67 |  | 11/16 |
| MES | 60 | eod | +0.009 | -0.036 .. +0.053 | +0.4% | +0.069 | 0.77 |  | 10/16 |
| MNQ | 5 | h1 * | +0.004 | +0.000 .. +0.007 | +0.7% | +0.008 | 0.097 | 1 | 11/16 |
| MNQ | 5 | h2 | +0.005 | -0.001 .. +0.011 | +0.7% | +0.015 | 0.22 |  | 13/16 |
| MNQ | 5 | h4 | +0.007 | -0.004 .. +0.018 | +0.7% | +0.017 | 0.34 |  | 12/16 |
| MNQ | 5 | h8 | -0.003 | -0.024 .. +0.019 | -0.2% | -0.002 | 0.81 |  | 8/16 |
| MNQ | 5 | h16 | -0.009 | -0.048 .. +0.030 | -0.4% | -0.042 | 0.65 |  | 6/16 |
| MNQ | 5 | eod | -0.165 | -0.394 .. +0.063 | -1.3% | -0.295 | 0.16 |  | 10/16 |
| MNQ | 15 | h1 | +0.006 | -0.000 .. +0.013 | +1.2% | +0.015 | 0.53 |  | 12/16 |
| MNQ | 15 | h2 | +0.006 | -0.007 .. +0.018 | +0.7% | +0.014 | 0.59 |  | 10/16 |
| MNQ | 15 | h4 | -0.002 | -0.031 .. +0.026 | -0.2% | -0.001 | 0.98 |  | 8/16 |
| MNQ | 15 | h8 | -0.031 | -0.074 .. +0.013 | -1.8% | -0.064 | 0.17 |  | 12/16 |
| MNQ | 15 | h16 * | -0.044 | -0.095 .. +0.006 | -1.8% | -0.149 | 0.086 | 1 | 12/16 |
| MNQ | 15 | eod | -0.147 | -0.345 .. +0.050 | -2.3% | -0.253 | 0.14 |  | 12/16 |
| MNQ | 60 | h1 | +0.008 | -0.005 .. +0.021 | +1.5% | +0.030 | 0.23 |  | 11/16 |
| MNQ | 60 | h2 | +0.010 | -0.008 .. +0.028 | +1.3% | +0.031 | 0.3 |  | 8/16 |
| MNQ | 60 | h4 | +0.004 | -0.022 .. +0.030 | +0.3% | +0.043 | 0.78 |  | 8/16 |
| MNQ | 60 | h8 * | +0.026 | -0.008 .. +0.060 | +1.6% | +0.054 | 0.15 | 1 | 10/16 |
| MNQ | 60 | h16 | +0.014 | -0.030 .. +0.058 | +0.6% | +0.056 | 0.55 |  | 9/16 |
| MNQ | 60 | eod | +0.012 | -0.033 .. +0.057 | +0.5% | +0.052 | 0.61 |  | 10/16 |
| MYM | 5 | h1 * | +0.004 | -0.001 .. +0.009 | +0.8% | +0.006 | 0.13 | 1 | 5/8 |
| MYM | 5 | h2 | +0.001 | -0.008 .. +0.011 | +0.2% | +0.003 | 0.8 |  | 5/8 |
| MYM | 5 | h4 | -0.004 | -0.024 .. +0.015 | -0.4% | +0.001 | 0.68 |  | 3/8 |
| MYM | 5 | h8 | -0.002 | -0.039 .. +0.035 | -0.1% | -0.008 | 0.94 |  | 3/8 |
| MYM | 5 | h16 | -0.016 | -0.067 .. +0.035 | -0.7% | -0.055 | 0.54 |  | 3/8 |
| MYM | 5 | eod | -0.073 | -0.325 .. +0.178 | -0.6% | -0.131 | 0.57 |  | 4/8 |
| MYM | 15 | h1 | +0.006 | -0.004 .. +0.016 | +1.1% | +0.011 | 0.45 |  | 6/8 |
| MYM | 15 | h2 | -0.001 | -0.017 .. +0.015 | -0.2% | +0.009 | 0.95 |  | 3/8 |
| MYM | 15 | h4 | -0.005 | -0.038 .. +0.028 | -0.4% | -0.009 | 0.94 |  | 3/8 |
| MYM | 15 | h8 | -0.013 | -0.065 .. +0.038 | -0.8% | -0.052 | 0.61 |  | 3/8 |
| MYM | 15 | h16 | -0.049 | -0.141 .. +0.042 | -2.0% | -0.141 | 0.29 |  | 4/8 |
| MYM | 15 | eod * | -0.172 | -0.411 .. +0.066 | -2.9% | -0.222 | 0.16 | 1 | 7/8 |
| MYM | 60 | h1 * | +0.014 | -0.003 .. +0.031 | +2.7% | +0.026 | 0.12 | 1 | 5/8 |
| MYM | 60 | h2 | +0.013 | -0.012 .. +0.038 | +1.7% | +0.040 | 0.32 |  | 6/8 |
| MYM | 60 | h4 | +0.015 | -0.023 .. +0.052 | +1.4% | +0.053 | 0.47 |  | 5/8 |
| MYM | 60 | h8 | +0.038 | -0.018 .. +0.093 | +2.5% | +0.087 | 0.27 |  | 6/8 |
| MYM | 60 | h16 | -0.013 | -0.074 .. +0.048 | -0.6% | +0.074 | 0.68 |  | 6/8 |
| MYM | 60 | eod | -0.022 | -0.083 .. +0.039 | -1.0% | +0.071 | 0.5 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.01 pts | -0.31 .. +0.30 | 0.99 |
| MES | 15 | +0.19 pts | -0.35 .. +0.73 | 0.5 |
| MES | 60 | +0.31 pts | -0.77 .. +1.39 | 0.58 |
| MNQ | 5 | +0.11 pts | -0.21 .. +0.43 | 0.5 |
| MNQ | 15 | +0.40 pts | -0.16 .. +0.97 | 0.17 |
| MNQ | 60 | +0.80 pts | -0.31 .. +1.91 | 0.16 |
| MYM | 5 | +0.31 pts | -0.19 .. +0.81 | 0.22 |
| MYM | 15 | -0.34 pts | -1.16 .. +0.49 | 0.48 |
| MYM | 60 | -0.15 pts | -1.78 .. +1.47 | 0.86 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 130496 | -0.004 | 0.364 | -0.01 | -3.51 | -3.54 | -3.48 | -3.44 |
| MES | 5 | h2 | event | with signal | 130496 | -0.003 | 0.364 | -0.04 | -3.54 | -3.54 | -3.53 | -3.44 |
| MES | 5 | h4 | event | with signal | 130496 | +0.003 | 0.364 | +0.01 | -3.49 | -3.51 | -3.46 | -3.41 |
| MES | 5 | h8 | event | with signal | 130496 | +0.029 | 0.364 | +0.17 | -3.33 | -3.37 | -3.27 | -3.33 |
| MES | 5 | h16 | event | with signal | 130496 | +0.056 | 0.364 | +0.45 | -3.05 | -3.25 | -2.80 | -3.18 |
| MES | 5 | eod | event | with signal | 130496 | +0.695 | 0.364 | +4.70 | +1.20 | -0.48 | +3.29 | +0.09 |
| MES | 15 | h1 | event | against signal | 38280 | +0.007 | 0.196 | +0.08 | -3.42 | -3.45 | -3.39 | -3.47 |
| MES | 15 | h2 | event | with signal | 38280 | +0.008 | 0.196 | +0.06 | -3.44 | -3.43 | -3.44 | -3.41 |
| MES | 15 | h4 | event | with signal | 38280 | +0.026 | 0.196 | +0.26 | -3.24 | -3.28 | -3.19 | -3.30 |
| MES | 15 | h8 | event | with signal | 38280 | +0.053 | 0.196 | +0.50 | -3.00 | -3.09 | -2.92 | -3.18 |
| MES | 15 | h16 | event | with signal | 38280 | +0.086 | 0.196 | +0.99 | -2.51 | -2.52 | -2.51 | -2.78 |
| MES | 15 | eod | event | with signal | 38280 | +0.314 | 0.196 | +3.64 | +0.14 | -0.45 | +0.76 | -0.41 |
| MES | 60 | h1 | event | against signal | 8877 | -0.009 | 0.093 | -0.60 | -4.10 | -4.03 | -4.17 | -3.88 |
| MES | 60 | h2 | event | against signal | 8877 | -0.015 | 0.093 | -0.90 | -4.40 | -4.34 | -4.46 | -3.97 |
| MES | 60 | h4 | event | against signal | 8877 | -0.027 | 0.093 | -1.52 | -5.02 | -4.17 | -5.86 | -4.13 |
| MES | 60 | h8 | event | against signal | 8877 | -0.061 | 0.093 | -2.55 | -6.05 | -4.87 | -7.23 | -4.48 |
| MES | 60 | h16 | event | against signal | 8877 | -0.090 | 0.093 | -3.95 | -7.45 | -6.03 | -8.86 | -4.95 |
| MES | 60 | eod | event | against signal | 8877 | -0.100 | 0.093 | -4.39 | -7.89 | -6.06 | -9.70 | -5.19 |
| MNQ | 5 | h1 | event | against signal | 114994 | +0.000 | 0.137 | +0.06 | -1.94 | -2.00 | -1.88 | -1.99 |
| MNQ | 5 | h2 | event | against signal | 114994 | -0.000 | 0.137 | +0.15 | -1.85 | -1.99 | -1.70 | -1.94 |
| MNQ | 5 | h4 | event | with signal | 114994 | +0.010 | 0.137 | -0.13 | -2.13 | -1.95 | -2.32 | -2.06 |
| MNQ | 5 | h8 | event | with signal | 114994 | +0.036 | 0.137 | -0.03 | -2.03 | -1.83 | -2.25 | -2.10 |
| MNQ | 5 | h16 | event | with signal | 114994 | +0.081 | 0.137 | +0.30 | -1.70 | -1.67 | -1.74 | -1.93 |
| MNQ | 5 | eod | event | with signal | 114994 | +0.877 | 0.137 | +6.08 | +4.08 | +0.88 | +7.55 | +4.70 |
| MNQ | 15 | h1 | event | against signal | 36677 | -0.005 | 0.076 | -0.21 | -2.21 | -2.00 | -2.42 | -2.14 |
| MNQ | 15 | h2 | event | with signal | 36677 | +0.018 | 0.076 | +0.35 | -1.65 | -1.86 | -1.44 | -1.78 |
| MNQ | 15 | h4 | event | with signal | 36677 | +0.032 | 0.076 | +0.62 | -1.38 | -1.80 | -0.95 | -1.71 |
| MNQ | 15 | h8 | event | with signal | 36677 | +0.055 | 0.076 | +1.29 | -0.71 | -1.69 | +0.29 | -1.43 |
| MNQ | 15 | h16 | event | with signal | 36677 | +0.111 | 0.076 | +1.87 | -0.13 | -1.11 | +0.89 | -0.56 |
| MNQ | 15 | eod | event | with signal | 36677 | +0.477 | 0.076 | +6.04 | +4.04 | +1.39 | +6.78 | +4.11 |
| MNQ | 60 | h1 | event | with signal | 8712 | +0.013 | 0.038 | +0.09 | -1.91 | -1.57 | -2.27 | -2.16 |
| MNQ | 60 | h2 | event | with signal | 8712 | +0.029 | 0.038 | +0.75 | -1.25 | -1.00 | -1.52 | -1.75 |
| MNQ | 60 | h4 | event | against signal | 8712 | -0.038 | 0.038 | -1.23 | -3.23 | -3.18 | -3.29 | -2.22 |
| MNQ | 60 | h8 | event | with signal | 8712 | +0.082 | 0.038 | +3.51 | +1.51 | -0.19 | +3.33 | -0.48 |
| MNQ | 60 | h16 | event | against signal | 8712 | -0.119 | 0.038 | -5.78 | -7.78 | -4.57 | -11.21 | -4.69 |
| MNQ | 60 | eod | event | against signal | 8712 | -0.128 | 0.038 | -5.90 | -7.90 | -4.78 | -11.23 | -4.61 |
| MYM | 5 | h1 | event | with signal | 55418 | -0.004 | 0.171 | -0.03 | -2.03 | +nan | -2.03 | -1.95 |
| MYM | 5 | h2 | event | with signal | 55418 | -0.006 | 0.171 | -0.07 | -2.07 | +nan | -2.07 | -1.94 |
| MYM | 5 | h4 | event | with signal | 55418 | +0.003 | 0.171 | +0.06 | -1.94 | +nan | -1.94 | -1.74 |
| MYM | 5 | h8 | event | with signal | 55418 | +0.009 | 0.171 | +0.10 | -1.90 | +nan | -1.90 | -1.65 |
| MYM | 5 | h16 | event | with signal | 55418 | +0.034 | 0.171 | +0.41 | -1.59 | +nan | -1.59 | -1.34 |
| MYM | 5 | eod | event | with signal | 55418 | +0.467 | 0.171 | +4.24 | +2.24 | +nan | +2.24 | +2.40 |
| MYM | 15 | h1 | event | against signal | 18321 | +0.014 | 0.099 | +0.16 | -1.84 | +nan | -1.84 | -1.93 |
| MYM | 15 | h2 | event | against signal | 18321 | +0.015 | 0.099 | +0.32 | -1.68 | +nan | -1.68 | -1.82 |
| MYM | 15 | h4 | event | with signal | 18321 | +0.000 | 0.099 | -0.04 | -2.04 | +nan | -2.04 | -1.90 |
| MYM | 15 | h8 | event | with signal | 18321 | +0.028 | 0.099 | +0.69 | -1.31 | +nan | -1.31 | -1.03 |
| MYM | 15 | h16 | event | with signal | 18321 | +0.041 | 0.099 | +1.24 | -0.76 | +nan | -0.76 | +0.01 |
| MYM | 15 | eod | event | with signal | 18321 | +0.181 | 0.099 | +3.31 | +1.31 | +nan | +1.31 | +2.52 |
| MYM | 60 | h1 | event | with signal | 4364 | +0.008 | 0.048 | +0.52 | -1.48 | +nan | -1.48 | -1.58 |
| MYM | 60 | h2 | event | with signal | 4364 | +0.004 | 0.048 | +0.87 | -1.13 | +nan | -1.13 | -1.17 |
| MYM | 60 | h4 | event | with signal | 4364 | +0.014 | 0.048 | +1.98 | -0.02 | +nan | -0.02 | -0.18 |
| MYM | 60 | h8 | event | with signal | 4364 | +0.022 | 0.048 | +2.44 | +0.44 | +nan | +0.44 | +0.03 |
| MYM | 60 | h16 | event | with signal | 4364 | +0.045 | 0.048 | +3.69 | +1.69 | +nan | +1.69 | +0.54 |
| MYM | 60 | eod | event | with signal | 4364 | +0.067 | 0.048 | +4.53 | +2.53 | +nan | +2.53 | +1.05 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.200 | +0.231 | +0.105 | -0.052 | -0.474 | +0.000 | -0.045 | -0.046 | -0.046 | -0.031 | -0.032 |
| MES | 15 | +0.247 | +0.282 | +0.145 | -0.051 | -0.527 | +0.000 | -0.023 | -0.012 | -0.005 | +0.005 | +0.010 |
| MES | 60 | +0.364 | +0.266 | +0.147 | -0.048 | -0.540 | +0.000 | -0.002 | -0.008 | -0.027 | -0.029 | +0.054 |
| MNQ | 5 | +0.306 | +0.359 | +0.205 | -0.004 | -0.504 | +0.000 | -0.017 | -0.021 | -0.017 | -0.007 | +0.006 |
| MNQ | 15 | +0.302 | +0.341 | +0.199 | -0.020 | -0.530 | +0.000 | -0.005 | +0.004 | +0.006 | +0.004 | +0.037 |
| MNQ | 60 | +0.467 | +0.338 | +0.200 | -0.020 | -0.519 | +0.000 | +0.003 | +0.009 | -0.009 | -0.008 | -0.002 |
| MYM | 5 | +0.292 | +0.338 | +0.194 | -0.021 | -0.529 | +0.000 | -0.007 | -0.007 | +0.008 | +0.019 | +0.049 |
| MYM | 15 | +0.275 | +0.309 | +0.179 | -0.027 | -0.534 | +0.000 | -0.010 | -0.009 | +0.006 | +0.043 | +0.100 |
| MYM | 60 | +0.302 | +0.268 | +0.158 | -0.045 | -0.531 | +0.000 | +0.005 | -0.007 | +0.001 | +0.013 | -0.022 |

## Calibration

- MES 5-min: 1036271 bars, 130496 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 38280 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 8877 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 114994 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 36677 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 8712 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 55418 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 18321 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 4364 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43054 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
