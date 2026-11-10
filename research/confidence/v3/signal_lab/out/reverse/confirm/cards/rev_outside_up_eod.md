# Impact card: rev_outside_up_eod

outside bar (higher high and lower low than the last bar) -> drift up to 16:45

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.026 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.051 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.02).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.96 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.122 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best +0.058 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.084 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.46).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.33 at recent bar sizes, 90% range up to $2.58); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best +0.062 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.063 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.99).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.16 at recent bar sizes, 90% range up to $1.19); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.006 | -0.022 .. +0.009 | -0.0022 | 0.42 / 0.44 / 0.44 | 0.457 |  |  | 5/8 | n/a | -0.006 |  | -0.8 / -0.8 |  |
| MES | 15 | h2 | -0.005 | -0.026 .. +0.015 | -0.0012 | 0.6 / 0.6 / 0.66 | 0.679 |  |  | 6/8 | n/a | -0.005 |  | -0.5 / -0.5 |  |
| MES | 15 | h4 | -0.010 | -0.039 .. +0.020 | -0.0014 | 0.52 / 0.51 / 0.6 | 0.604 |  |  | 5/8 | n/a | -0.010 |  | -0.6 / -0.6 | 0.051 |
| MES | 15 | h8 * | -0.026 | -0.063 .. +0.011 | -0.0027 | 0.17 / 0.21 / 0.28 | 0.282 | 1 | 0.987 | 6/8 | n/a | -0.026 | False | -1.1 / -1.4 |  |
| MES | 15 | h16 | -0.010 | -0.074 .. +0.053 | -0.0008 | 0.75 / 0.76 / 0.75 | 0.759 |  |  | 4/8 | n/a | -0.010 |  | -0.3 / -0.3 |  |
| MES | 15 | eod | -0.057 | -0.295 .. +0.182 | -0.0016 | 0.64 / 0.65 / 0.53 | 0.524 |  |  | 5/8 | n/a | -0.057 |  | -0.7 / -0.5 |  |
| MNQ | 15 | h1 | +0.003 | -0.011 .. +0.017 | +0.0007 | 0.71 / 0.72 / 0.78 | 0.743 |  |  | 5/8 | n/a | +0.003 |  | +0.3 / +0.4 |  |
| MNQ | 15 | h2 | +0.008 | -0.012 .. +0.027 | +0.0011 | 0.44 / 0.45 / 0.64 | 0.583 |  |  | 4/8 | n/a | +0.008 |  | +0.7 / +0.8 |  |
| MNQ | 15 | h4 | +0.001 | -0.029 .. +0.031 | +0.0001 | 0.94 / 0.94 / 0.97 | 0.973 |  |  | 5/8 | n/a | +0.001 |  | +0.1 / +0.1 | 0.084 |
| MNQ | 15 | h8 | +0.005 | -0.038 .. +0.048 | +0.0003 | 0.82 / 0.83 / 0.89 | 0.877 |  |  | 5/8 | n/a | +0.005 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h16 * | +0.058 | -0.018 .. +0.133 | +0.0035 | 0.13 / 0.15 / 0.15 | 0.151 | 1 | 0.947 | 5/8 | n/a | +0.058 | False | +1.8 / +1.5 |  |
| MNQ | 15 | eod | +0.143 | -0.166 .. +0.451 | +0.0028 | 0.37 / 0.38 / 0.23 | 0.224 |  |  | 4/8 | n/a | +0.143 |  | +1.7 / +0.9 |  |
| MYM | 15 | h1 | +0.011 | -0.003 .. +0.025 | +0.0033 | 0.13 / 0.15 / 0.25 | 0.252 |  |  | 7/8 | n/a | +0.011 |  | +1.4 / +1.5 |  |
| MYM | 15 | h2 | +0.017 | -0.003 .. +0.038 | +0.0030 | 0.099 / 0.099 / 0.28 | 0.27 |  |  | 5/8 | n/a | +0.017 |  | +1.5 / +1.6 |  |
| MYM | 15 | h4 | +0.024 | -0.008 .. +0.055 | +0.0025 | 0.14 / 0.15 / 0.36 | 0.363 |  |  | 5/8 | n/a | +0.024 |  | +1.5 / +1.5 | 0.063 |
| MYM | 15 | h8 | +0.003 | -0.044 .. +0.050 | +0.0003 | 0.89 / 0.89 / 0.9 | 0.91 |  |  | 4/8 | n/a | +0.003 |  | +0.1 / +0.1 |  |
| MYM | 15 | h16 * | +0.062 | -0.040 .. +0.163 | +0.0035 | 0.24 / 0.24 / 0.15 | 0.149 | 1 | 0.873 | 4/8 | n/a | +0.062 | False | +1.9 / +1.2 |  |
| MYM | 15 | eod | +0.088 | -0.170 .. +0.345 | +0.0021 | 0.5 / 0.51 / 0.39 | 0.388 |  |  | 5/8 | n/a | +0.088 |  | +1.1 / +0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.024 | +0.011 .. +0.037 | +4.6% | +0.040 | 0.0033 | 0.244 | 6/8 |
| MES | 15 | h2 | +0.029 | +0.013 .. +0.045 | +3.8% | +0.043 | 0.0073 |  | 7/8 |
| MES | 15 | h4 | +0.006 | -0.018 .. +0.031 | +0.6% | +0.026 | 0.84 |  | 5/8 |
| MES | 15 | h8 | +0.020 | -0.016 .. +0.056 | +1.2% | +0.018 | 0.52 |  | 7/8 |
| MES | 15 | h16 | +0.017 | -0.039 .. +0.072 | +0.7% | -0.007 | 0.6 |  | 7/8 |
| MES | 15 | eod | -0.025 | -0.224 .. +0.175 | -0.4% | -0.084 | 0.81 |  | 3/8 |
| MNQ | 15 | h1 * | +0.016 | +0.005 .. +0.027 | +3.1% | +0.014 | 0.076 | 1 | 8/8 |
| MNQ | 15 | h2 | +0.023 | +0.002 .. +0.045 | +3.1% | +0.015 | 0.21 |  | 7/8 |
| MNQ | 15 | h4 | -0.005 | -0.054 .. +0.044 | -0.5% | -0.015 | 0.83 |  | 3/8 |
| MNQ | 15 | h8 | -0.028 | -0.104 .. +0.047 | -1.7% | -0.075 | 0.46 |  | 2/8 |
| MNQ | 15 | h16 | -0.019 | -0.105 .. +0.068 | -0.8% | -0.125 | 0.67 |  | 4/8 |
| MNQ | 15 | eod | -0.158 | -0.496 .. +0.180 | -2.5% | -0.238 | 0.37 |  | 3/8 |
| MYM | 15 | h1 * | +0.014 | +0.002 .. +0.027 | +2.7% | +0.025 | 0.16 | 1 | 5/8 |
| MYM | 15 | h2 | +0.016 | -0.003 .. +0.036 | +2.1% | +0.028 | 0.2 |  | 6/8 |
| MYM | 15 | h4 | +0.012 | -0.024 .. +0.047 | +1.0% | +0.012 | 0.79 |  | 7/8 |
| MYM | 15 | h8 | +0.008 | -0.045 .. +0.060 | +0.5% | -0.006 | 0.98 |  | 6/8 |
| MYM | 15 | h16 | -0.012 | -0.104 .. +0.080 | -0.5% | -0.062 | 0.8 |  | 2/8 |
| MYM | 15 | eod | +0.014 | -0.220 .. +0.247 | +0.2% | -0.039 | 0.97 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +0.20 pts | -0.63 .. +1.03 | 0.71 |
| MNQ | 15 | +0.07 pts | -0.66 .. +0.80 | 0.97 |
| MYM | 15 | +0.53 pts | -0.25 .. +1.30 | 0.18 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | event | short | 14182 | -0.005 | 0.122 | -0.05 | -3.55 | +nan | -3.55 | -3.31 |
| MES | 15 | h2 | event | short | 14182 | -0.004 | 0.122 | -0.11 | -3.61 | +nan | -3.61 | -3.45 |
| MES | 15 | h4 | event | short | 14182 | -0.012 | 0.122 | -0.28 | -3.78 | +nan | -3.78 | -3.40 |
| MES | 15 | h8 | event | short | 14182 | -0.012 | 0.122 | -0.64 | -4.14 | +nan | -4.14 | -3.53 |
| MES | 15 | h16 | event | short | 14182 | -0.043 | 0.122 | -1.42 | -4.92 | +nan | -4.92 | -4.27 |
| MES | 15 | eod | event | short | 14182 | -0.105 | 0.122 | -3.28 | -6.78 | +nan | -6.78 | -6.04 |
| MNQ | 15 | h1 | event | long | 16942 | +0.013 | 0.045 | +0.45 | -1.55 | +nan | -1.55 | -1.88 |
| MNQ | 15 | h2 | event | long | 16942 | +0.015 | 0.045 | +0.50 | -1.50 | +nan | -1.50 | -1.71 |
| MNQ | 15 | h4 | event | long | 16942 | +0.028 | 0.045 | +1.06 | -0.94 | +nan | -0.94 | -1.86 |
| MNQ | 15 | h8 | event | long | 16942 | +0.054 | 0.045 | +2.20 | +0.20 | +nan | +0.20 | -1.35 |
| MNQ | 15 | h16 | event | long | 16942 | +0.107 | 0.045 | +3.24 | +1.24 | +nan | +1.24 | -0.24 |
| MNQ | 15 | eod | event | long | 16942 | +0.315 | 0.045 | +9.18 | +7.18 | +nan | +7.18 | +4.13 |
| MYM | 15 | h1 | event | long | 16223 | +0.013 | 0.096 | +0.25 | -1.75 | +nan | -1.75 | -1.79 |
| MYM | 15 | h2 | event | long | 16223 | +0.012 | 0.096 | +0.23 | -1.77 | +nan | -1.77 | -1.68 |
| MYM | 15 | h4 | event | long | 16223 | +0.026 | 0.096 | +0.70 | -1.30 | +nan | -1.30 | -1.37 |
| MYM | 15 | h8 | event | long | 16223 | +0.013 | 0.096 | +0.47 | -1.53 | +nan | -1.53 | -1.66 |
| MYM | 15 | h16 | event | long | 16223 | +0.046 | 0.096 | +1.17 | -0.83 | +nan | -0.83 | -0.64 |
| MYM | 15 | eod | event | long | 16223 | +0.157 | 0.096 | +2.69 | +0.69 | +nan | +0.69 | +0.56 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.010 | -0.020 | -0.015 | -0.004 | -0.004 | +0.000 | +0.001 | +0.002 | -0.004 | -0.022 | +0.004 |
| MNQ | 15 | -0.024 | -0.024 | -0.018 | -0.001 | +0.002 | +0.000 | +0.016 | +0.023 | +0.020 | +0.019 | +0.084 |
| MYM | 15 | -0.002 | -0.009 | -0.004 | +0.001 | -0.004 | +0.000 | +0.021 | +0.030 | +0.038 | +0.022 | +0.112 |

## Calibration

- MES 15-min: 171560 bars, 14182 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 171530 bars, 16942 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 16223 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
