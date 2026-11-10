# Impact card: rev_new_day_extreme

+1 bar made a new high of day, -1 a new low; new high -> next hour down

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.817 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.071 R20 or more 80% of the time).
- MES 15-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.053 R20, CONFIRMED, q=3.38e-07, 7 of 8 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $11.23 at recent bar sizes, 90% range up to $2.06); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best +1.693 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.105 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.034).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $38.99 at recent bar sizes, 90% range up to $5.23); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best +0.030 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.082 R20 or more 80% of the time).
- MYM 15-min size: the market moves 12% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.063 R20, CONFIRMED, q=0.0462, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.32 at recent bar sizes, 90% range up to $3.93); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.001 | -0.022 .. +0.025 | +0.0007 | 0.9 / 0.9 / 0.87 | 0.87 |  |  | 6/8 | n/a | +0.001 |  | +0.1 / +0.1 |  |
| MES | 15 | h2 | +0.010 | -0.021 .. +0.041 | +0.0018 | 0.53 / 0.54 / 0.52 | 0.519 |  |  | 4/8 | n/a | +0.010 |  | +0.5 / +0.6 |  |
| MES | 15 | h4 | +0.021 | -0.041 .. +0.084 | +0.0023 | 0.5 / 0.53 / 0.44 | 0.444 |  |  | 5/8 | n/a | +0.021 |  | +0.7 / +0.7 | 0.071 |
| MES | 15 | h8 | +0.046 | -0.073 .. +0.165 | +0.0036 | 0.45 / 0.47 / 0.32 | 0.325 |  |  | 5/8 | n/a | +0.046 |  | +1.2 / +0.8 |  |
| MES | 15 | h16 | +0.091 | -0.202 .. +0.385 | +0.0052 | 0.54 / 0.55 / 0.24 | 0.247 |  |  | 3/8 | n/a | +0.091 |  | +1.9 / +0.6 |  |
| MES | 15 | eod * | +0.817 | -0.996 .. +2.630 | +0.0187 | 0.38 / 0.38 / 0.0036 | 0.00474 | 1 | 1 | 3/8 | n/a | +0.817 | False | +5.5 / +0.9 |  |
| MNQ | 15 | h1 | -0.006 | -0.055 .. +0.043 | -0.0010 | 0.8 / 0.8 / 0.57 | 0.522 |  |  | 2/8 | n/a | -0.006 |  | -0.3 / -0.3 |  |
| MNQ | 15 | h2 | +0.011 | -0.051 .. +0.074 | +0.0014 | 0.73 / 0.75 / 0.64 | 0.612 |  |  | 6/8 | n/a | +0.011 |  | +0.3 / +0.4 |  |
| MNQ | 15 | h4 | +0.008 | -0.119 .. +0.135 | +0.0004 | 0.9 / 0.91 / 0.85 | 0.832 |  |  | 4/8 | n/a | +0.008 |  | +0.1 / +0.1 | 0.105 |
| MNQ | 15 | h8 | -0.045 | -0.241 .. +0.152 | -0.0027 | 0.66 / 0.69 / 0.51 | 0.485 |  |  | 5/8 | n/a | -0.045 |  | -0.4 / -0.4 |  |
| MNQ | 15 | h16 | +0.132 | -0.282 .. +0.546 | +0.0055 | 0.53 / 0.56 / 0.18 | 0.178 |  |  | 3/8 | n/a | +0.132 |  | +1.4 / +0.6 |  |
| MNQ | 15 | eod * | +1.693 | -1.133 .. +4.519 | +0.0253 | 0.24 / 0.25 / 2.1e-06 | 0.000527 | 1 | 0.99 | 4/8 | n/a | +1.693 | False | +5.2 / +1.2 |  |
| MYM | 15 | h1 | +0.002 | -0.022 .. +0.025 | +0.0002 | 0.89 / 0.89 / 0.88 | 0.874 |  |  | 3/8 | n/a | +0.002 |  | +0.1 / +0.1 |  |
| MYM | 15 | h2 * | +0.030 | -0.040 .. +0.100 | +0.0038 | 0.4 / 0.4 / 0.16 | 0.156 | 1 | 0.999 | 3/8 | n/a | +0.030 | False | +0.9 / +0.8 |  |
| MYM | 15 | h4 | +0.055 | -0.095 .. +0.205 | +0.0041 | 0.47 / 0.49 / 0.13 | 0.133 |  |  | 2/8 | n/a | +0.055 |  | +0.9 / +0.7 | 0.082 |
| MYM | 15 | h8 | +0.123 | -0.171 .. +0.417 | +0.0074 | 0.41 / 0.42 / 0.027 | 0.0285 |  |  | 3/8 | n/a | +0.123 |  | +1.7 / +0.8 |  |
| MYM | 15 | h16 | +0.298 | -0.456 .. +1.052 | +0.0130 | 0.44 / 0.45 / 0.0044 | 0.00527 |  |  | 2/8 | n/a | +0.298 |  | +3.1 / +0.8 |  |
| MYM | 15 | eod | +0.887 | -1.252 .. +3.026 | +0.0166 | 0.42 / 0.42 / 0.0043 | 0.00263 |  |  | 3/8 | n/a | +0.887 |  | +4.0 / +0.8 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.053 | -0.071 .. -0.036 | -10.3% | -0.121 | 3.2e-09 | 3.38e-07 | 7/8 |
| MES | 15 | h2 | -0.087 | -0.140 .. -0.033 | -11.6% | -0.185 | 0.0014 |  | 7/8 |
| MES | 15 | h4 | -0.136 | -0.257 .. -0.015 | -12.6% | -0.294 | 0.028 |  | 7/8 |
| MES | 15 | h8 | -0.197 | -0.389 .. -0.005 | -12.4% | -0.485 | 0.044 |  | 6/8 |
| MES | 15 | h16 | -0.241 | -0.543 .. +0.062 | -10.2% | -0.789 | 0.12 |  | 5/8 |
| MES | 15 | eod | -0.908 | -2.547 .. +0.732 | -15.4% | -1.611 | 0.28 |  | 4/8 |
| MNQ | 15 | h1 * | -0.060 | -0.102 .. -0.017 | -11.4% | -0.142 | 0.0057 | 0.397 | 6/8 |
| MNQ | 15 | h2 | -0.123 | -0.252 .. +0.006 | -16.1% | -0.260 | 0.061 |  | 6/8 |
| MNQ | 15 | h4 | -0.241 | -0.583 .. +0.102 | -21.4% | -0.499 | 0.17 |  | 6/8 |
| MNQ | 15 | h8 | -0.367 | -0.948 .. +0.214 | -22.1% | -0.941 | 0.22 |  | 5/8 |
| MNQ | 15 | h16 | -0.360 | -0.983 .. +0.262 | -14.5% | -1.574 | 0.27 |  | 4/8 |
| MNQ | 15 | eod | -1.793 | -4.907 .. +1.320 | -28.2% | -2.842 | 0.27 |  | 4/8 |
| MYM | 15 | h1 * | -0.063 | -0.099 .. -0.027 | -11.9% | -0.132 | 0.00058 | 0.0462 | 8/8 |
| MYM | 15 | h2 | -0.123 | -0.229 .. -0.017 | -16.1% | -0.233 | 0.022 |  | 7/8 |
| MYM | 15 | h4 | -0.214 | -0.456 .. +0.029 | -19.2% | -0.417 | 0.084 |  | 6/8 |
| MYM | 15 | h8 | -0.309 | -0.703 .. +0.086 | -18.8% | -0.748 | 0.13 |  | 6/8 |
| MYM | 15 | h16 | -0.511 | -1.239 .. +0.216 | -20.8% | -1.210 | 0.17 |  | 5/8 |
| MYM | 15 | eod | -1.105 | -3.080 .. +0.870 | -18.4% | -1.786 | 0.28 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.29 pts | -1.40 .. +0.81 | 0.61 |
| MNQ | 15 | +0.28 pts | -0.86 .. +1.41 | 0.78 |
| MYM | 15 | -0.86 pts | -2.09 .. +0.37 | 0.17 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | top level | long | 23239 | +0.005 | 0.135 | +0.04 | -3.46 | +nan | -3.46 | -3.45 |
| MES | 15 | h2 | top level | long | 23239 | +0.006 | 0.135 | +0.03 | -3.47 | +nan | -3.47 | -3.57 |
| MES | 15 | h4 | bottom level | short | 17973 | +0.028 | 0.119 | -0.09 | -3.59 | +nan | -3.59 | -3.68 |
| MES | 15 | h8 | top level | long | 23239 | +0.028 | 0.135 | +0.04 | -3.46 | +nan | -3.46 | -4.31 |
| MES | 15 | h16 | top level | long | 23239 | +0.066 | 0.135 | +0.90 | -2.60 | +nan | -2.60 | -4.54 |
| MES | 15 | eod | top level | long | 23239 | +0.269 | 0.135 | +6.07 | +2.57 | +nan | +2.57 | -2.53 |
| MNQ | 15 | h1 | bottom level | long | 16524 | +0.017 | 0.041 | +0.12 | -1.88 | +nan | -1.88 | -2.06 |
| MNQ | 15 | h2 | top level | long | 21500 | +0.017 | 0.046 | +0.55 | -1.45 | +nan | -1.45 | -1.83 |
| MNQ | 15 | h4 | top level | long | 21500 | +0.024 | 0.046 | +0.83 | -1.17 | +nan | -1.17 | -2.23 |
| MNQ | 15 | h8 | bottom level | long | 16524 | +0.017 | 0.041 | +1.02 | -0.98 | +nan | -0.98 | -0.88 |
| MNQ | 15 | h16 | top level | long | 21500 | +0.070 | 0.046 | +2.90 | +0.90 | +nan | +0.90 | -3.10 |
| MNQ | 15 | eod | top level | long | 21500 | +0.418 | 0.046 | +12.91 | +10.91 | +nan | +10.91 | +2.35 |
| MYM | 15 | h1 | bottom level | short | 17461 | +0.006 | 0.090 | +0.12 | -1.88 | +nan | -1.88 | -1.87 |
| MYM | 15 | h2 | bottom level | short | 17461 | +0.048 | 0.090 | +0.27 | -1.73 | +nan | -1.73 | -1.80 |
| MYM | 15 | h4 | bottom level | short | 17461 | +0.089 | 0.090 | +0.39 | -1.61 | +nan | -1.61 | -1.71 |
| MYM | 15 | h8 | bottom level | short | 17461 | +0.171 | 0.090 | +0.26 | -1.74 | +nan | -1.74 | -2.06 |
| MYM | 15 | h16 | top level | long | 20992 | -0.056 | 0.099 | -0.57 | -2.57 | +nan | -2.57 | -2.81 |
| MYM | 15 | eod | top level | long | 20992 | +0.104 | 0.099 | +3.04 | +1.04 | +nan | +1.04 | -0.42 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -3.339 | -3.105 | -2.491 | -1.693 | -0.824 | +0.000 | +0.017 | +0.023 | +0.038 | +0.060 | +0.121 |
| MNQ | 15 | -3.523 | -3.304 | -2.688 | -1.860 | -0.943 | +0.000 | +0.035 | +0.059 | +0.071 | +0.017 | +0.226 |
| MYM | 15 | -3.504 | -3.276 | -2.643 | -1.831 | -0.922 | +0.000 | +0.033 | +0.064 | +0.102 | +0.176 | +0.410 |

## Calibration

- MES 15-min: 171560 bars, 23239 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 171530 bars, 21500 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 20992 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
