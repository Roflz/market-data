# Impact card: rev_inside_down_eod

inside bar -> drift down to 16:45

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.049 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.029 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.98 at recent bar sizes, 90% range up to $2.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best +0.019 R20 over the next 1 bar (15 min), p=0.83; we would catch an effect of 0.066 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.68 at recent bar sizes, 90% range up to $6.03); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best +0.011 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.037 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.18 at recent bar sizes, 90% range up to $4.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.003 | -0.006 .. +0.011 | +0.0013 | 0.52 / 0.53 / 0.53 | 0.54 |  |  | 4/8 | n/a | +0.003 |  | +0.6 / +0.6 |  |
| MES | 15 | h2 | -0.001 | -0.019 .. +0.017 | -0.0002 | 0.94 / 0.94 / 0.93 | 0.931 |  |  | 3/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MES | 15 | h4 | -0.016 | -0.059 .. +0.028 | -0.0032 | 0.48 / 0.5 / 0.16 | 0.163 |  |  | 4/8 | n/a | -0.016 |  | -1.0 / -0.7 | 0.029 |
| MES | 15 | h8 * | -0.049 | -0.126 .. +0.029 | -0.0072 | 0.22 / 0.22 / 0.0015 | 0.00105 | 1 | 0.995 | 4/8 | n/a | -0.049 | False | -2.3 / -1.2 |  |
| MES | 15 | h16 | -0.091 | -0.260 .. +0.078 | -0.0095 | 0.29 / 0.28 / 0.0001 | 0.000527 |  |  | 4/8 | n/a | -0.091 |  | -3.1 / -1.1 |  |
| MES | 15 | eod | -0.463 | -1.421 .. +0.495 | -0.0180 | 0.34 / 0.34 / 1.8e-10 | 0.000527 |  |  | 3/8 | n/a | -0.463 |  | -5.2 / -0.9 |  |
| MNQ | 15 | h1 * | +0.019 | -0.004 .. +0.042 | +0.0061 | 0.11 / 0.14 / 0.011 | 0.0216 | 1 | 0.916 | 6/8 | n/a | +0.019 | False | +1.4 / +1.6 |  |
| MNQ | 15 | h2 | -0.001 | -0.034 .. +0.032 | -0.0002 | 0.95 / 0.96 / 0.94 | 0.94 |  |  | 4/8 | n/a | -0.001 |  | -0.0 / -0.1 |  |
| MNQ | 15 | h4 | -0.017 | -0.106 .. +0.072 | -0.0018 | 0.71 / 0.74 / 0.43 | 0.434 |  |  | 3/8 | n/a | -0.017 |  | -0.4 / -0.4 | 0.066 |
| MNQ | 15 | h8 | -0.025 | -0.154 .. +0.103 | -0.0021 | 0.7 / 0.73 / 0.34 | 0.332 |  |  | 5/8 | n/a | -0.025 |  | -0.4 / -0.4 |  |
| MNQ | 15 | h16 | -0.141 | -0.444 .. +0.163 | -0.0103 | 0.36 / 0.39 / 8.4e-06 | 0.000527 |  |  | 3/8 | n/a | -0.141 |  | -2.4 / -0.9 |  |
| MNQ | 15 | eod | -0.660 | -2.201 .. +0.880 | -0.0159 | 0.4 / 0.42 / 7.7e-11 | 0.000527 |  |  | 2/8 | n/a | -0.660 |  | -3.4 / -0.8 |  |
| MYM | 15 | h1 * | +0.011 | -0.005 .. +0.027 | +0.0044 | 0.16 / 0.19 / 0.049 | 0.0527 | 1 | 0.95 | 5/8 | n/a | +0.011 | False | +1.3 / +1.4 |  |
| MYM | 15 | h2 | -0.007 | -0.041 .. +0.027 | -0.0015 | 0.69 / 0.71 / 0.48 | 0.473 |  |  | 3/8 | n/a | -0.007 |  | -0.4 / -0.4 |  |
| MYM | 15 | h4 | -0.039 | -0.138 .. +0.059 | -0.0053 | 0.43 / 0.45 / 0.019 | 0.0184 |  |  | 3/8 | n/a | -0.039 |  | -1.1 / -0.8 | 0.037 |
| MYM | 15 | h8 | -0.078 | -0.264 .. +0.108 | -0.0080 | 0.41 / 0.42 / 0.00056 | 0.00158 |  |  | 3/8 | n/a | -0.078 |  | -1.8 / -0.8 |  |
| MYM | 15 | h16 | -0.200 | -0.651 .. +0.250 | -0.0146 | 0.38 / 0.39 / 2e-10 | 0.000527 |  |  | 2/8 | n/a | -0.200 |  | -3.4 / -0.9 |  |
| MYM | 15 | eod | -0.578 | -1.774 .. +0.618 | -0.0175 | 0.34 / 0.35 / 1.4e-12 | 0.000527 |  |  | 3/8 | n/a | -0.578 |  | -4.2 / -0.9 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.007 | -0.014 .. +0.001 | -1.3% | -0.020 | 0.18 | 1 | 5/8 |
| MES | 15 | h2 | +0.003 | -0.018 .. +0.024 | +0.4% | +0.001 | 0.77 |  | 4/8 |
| MES | 15 | h4 | +0.012 | -0.040 .. +0.063 | +1.1% | +0.032 | 0.66 |  | 3/8 |
| MES | 15 | h8 | +0.035 | -0.054 .. +0.124 | +2.2% | +0.126 | 0.44 |  | 3/8 |
| MES | 15 | h16 | +0.070 | -0.092 .. +0.232 | +3.0% | +0.310 | 0.4 |  | 4/8 |
| MES | 15 | eod | +0.497 | -0.384 .. +1.378 | +8.4% | +0.777 | 0.27 |  | 3/8 |
| MNQ | 15 | h1 | +0.007 | -0.014 .. +0.028 | +1.3% | -0.002 | 0.51 |  | 4/8 |
| MNQ | 15 | h2 | +0.032 | -0.051 .. +0.115 | +4.2% | +0.050 | 0.46 |  | 2/8 |
| MNQ | 15 | h4 | +0.088 | -0.121 .. +0.297 | +7.9% | +0.162 | 0.41 |  | 1/8 |
| MNQ | 15 | h8 | +0.140 | -0.212 .. +0.492 | +8.4% | +0.400 | 0.44 |  | 1/8 |
| MNQ | 15 | h16 | +0.147 | -0.255 .. +0.548 | +5.9% | +0.752 | 0.48 |  | 1/8 |
| MNQ | 15 | eod * | +0.844 | -0.966 .. +2.654 | +13.3% | +1.366 | 0.37 | 1 | 3/8 |
| MYM | 15 | h1 | -0.000 | -0.013 .. +0.013 | -0.0% | -0.015 | 1 |  | 4/8 |
| MYM | 15 | h2 | +0.025 | -0.031 .. +0.081 | +3.2% | +0.029 | 0.39 |  | 3/8 |
| MYM | 15 | h4 | +0.060 | -0.077 .. +0.196 | +5.3% | +0.106 | 0.39 |  | 3/8 |
| MYM | 15 | h8 | +0.096 | -0.130 .. +0.322 | +5.8% | +0.258 | 0.41 |  | 3/8 |
| MYM | 15 | h16 | +0.203 | -0.236 .. +0.642 | +8.2% | +0.519 | 0.37 |  | 1/8 |
| MYM | 15 | eod * | +0.615 | -0.525 .. +1.754 | +10.2% | +0.851 | 0.3 | 1 | 3/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.03 pts | -0.57 .. +0.52 | 0.93 |
| MNQ | 15 | +0.24 pts | -0.33 .. +0.80 | 0.67 |
| MYM | 15 | +0.01 pts | -0.57 .. +0.59 | 0.96 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | event | long | 32079 | +0.006 | 0.141 | +0.07 | -3.43 | +nan | -3.43 | -3.47 |
| MES | 15 | h2 | event | short | 32079 | -0.006 | 0.141 | -0.18 | -3.68 | +nan | -3.68 | -3.59 |
| MES | 15 | h4 | event | short | 32079 | +0.000 | 0.141 | -0.24 | -3.74 | +nan | -3.74 | -3.62 |
| MES | 15 | h8 | event | short | 32079 | +0.018 | 0.141 | -0.21 | -3.71 | +nan | -3.71 | -3.49 |
| MES | 15 | h16 | event | short | 32079 | +0.035 | 0.141 | -0.82 | -4.32 | +nan | -4.32 | -3.96 |
| MES | 15 | eod | event | short | 32079 | +0.264 | 0.141 | -3.77 | -7.27 | +nan | -7.27 | -7.03 |
| MNQ | 15 | h1 | event | long | 27601 | +0.022 | 0.047 | +0.33 | -1.67 | +nan | -1.67 | -1.81 |
| MNQ | 15 | h2 | event | short | 27601 | -0.006 | 0.047 | -0.42 | -2.42 | +nan | -2.42 | -2.24 |
| MNQ | 15 | h4 | event | short | 27601 | +0.003 | 0.047 | -0.69 | -2.69 | +nan | -2.69 | -2.43 |
| MNQ | 15 | h8 | event | short | 27601 | -0.005 | 0.047 | -1.29 | -3.29 | +nan | -3.29 | -2.68 |
| MNQ | 15 | h16 | event | short | 27601 | +0.097 | 0.047 | -2.22 | -4.22 | +nan | -4.22 | -3.91 |
| MNQ | 15 | eod | event | short | 27601 | +0.528 | 0.047 | -8.92 | -10.92 | +nan | -10.92 | -12.41 |
| MYM | 15 | h1 | event | long | 28791 | +0.010 | 0.101 | +0.21 | -1.79 | +nan | -1.79 | -1.80 |
| MYM | 15 | h2 | event | short | 28791 | +0.006 | 0.101 | -0.27 | -2.27 | +nan | -2.27 | -2.30 |
| MYM | 15 | h4 | event | short | 28791 | +0.038 | 0.101 | -0.20 | -2.20 | +nan | -2.20 | -2.34 |
| MYM | 15 | h8 | event | short | 28791 | +0.081 | 0.101 | -0.33 | -2.33 | +nan | -2.33 | -2.68 |
| MYM | 15 | h16 | event | short | 28791 | +0.215 | 0.101 | -0.62 | -2.62 | +nan | -2.62 | -3.58 |
| MYM | 15 | eod | event | short | 28791 | +0.490 | 0.101 | -2.75 | -4.75 | +nan | -4.75 | -6.30 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.013 | -0.006 | +0.006 | +0.009 | -0.007 | +0.000 | -0.004 | -0.008 | -0.021 | -0.053 | -0.101 |
| MNQ | 15 | +0.002 | +0.003 | +0.016 | +0.011 | -0.009 | +0.000 | +0.001 | -0.019 | -0.035 | -0.041 | -0.182 |
| MYM | 15 | -0.026 | -0.014 | -0.004 | +0.003 | -0.009 | +0.000 | -0.007 | -0.025 | -0.057 | -0.104 | -0.258 |

## Calibration

- MES 15-min: 171560 bars, 32079 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 171530 bars, 27601 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 28791 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
