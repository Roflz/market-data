# Impact card: noise2

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.008 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.075 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.27).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.23 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.587 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.008 | -0.033 .. +0.018 | -0.0016 | 0.57 / 0.59 / 0.55 | 0.564 | 1 | 1 | 1/2 | -0.013 | +0.003 | False | -0.5 / -0.6 |  |
| MES | 15 | h2 | -0.007 | -0.047 .. +0.032 | -0.0005 | 0.72 / 0.72 / 0.71 | 0.738 |  |  | 2/2 | -0.005 | -0.011 |  | -0.4 / -0.4 |  |
| MES | 15 | h4 | -0.017 | -0.081 .. +0.046 | -0.0027 | 0.6 / 0.57 / 0.54 | 0.564 |  |  | 1/2 | +0.017 | -0.080 |  | -0.6 / -0.5 | 0.075 |
| MES | 15 | h8 | +0.003 | -0.087 .. +0.093 | +0.0022 | 0.94 / 0.94 / 0.94 | 0.945 |  |  | 1/2 | +0.041 | -0.067 |  | +0.1 / +0.1 |  |
| MES | 15 | h16 | +0.011 | -0.105 .. +0.127 | +0.0025 | 0.85 / 0.83 / 0.83 | 0.854 |  |  | 1/2 | +0.093 | -0.141 |  | +0.2 / +0.2 |  |
| MES | 15 | eod | +0.003 | -0.171 .. +0.178 | +0.0029 | 0.97 / 0.97 / 0.98 | 0.978 |  |  | 1/2 | +0.044 | -0.072 |  | +0.0 / +0.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.008 | -0.024 .. +0.009 | -1.1% | -0.007 | 0.42 |  | 2/2 |
| MES | 15 | h2 | +0.003 | -0.020 .. +0.026 | +0.3% | +0.005 | 0.79 |  | 2/2 |
| MES | 15 | h4 | +0.016 | -0.014 .. +0.046 | +1.2% | +0.008 | 0.32 |  | 2/2 |
| MES | 15 | h8 | +0.044 | -0.005 .. +0.093 | +2.3% | +0.036 | 0.081 |  | 2/2 |
| MES | 15 | h16 | +0.031 | -0.023 .. +0.085 | +1.2% | +0.021 | 0.44 |  | 2/2 |
| MES | 15 | eod * | +0.117 | +0.013 .. +0.222 | +2.6% | +0.089 | 0.045 | 1 | 2/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.61 pts | -2.29 .. +1.08 | 0.48 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | long | 7197 | +0.003 | 0.589 | +0.02 | -3.48 | -3.44 | -3.55 | -3.47 |
| MES | 15 | h2 | bottom fifth | long | 7197 | +0.007 | 0.589 | +0.05 | -3.45 | -3.44 | -3.48 | -3.43 |
| MES | 15 | h4 | top fifth | short | 7196 | +0.016 | 0.588 | +0.09 | -3.41 | -3.54 | -3.17 | -3.46 |
| MES | 15 | h8 | bottom fifth | short | 7197 | +0.027 | 0.589 | +0.15 | -3.35 | -3.35 | -3.35 | -3.47 |
| MES | 15 | h16 | bottom fifth | short | 7197 | +0.048 | 0.589 | +0.30 | -3.20 | -3.45 | -2.72 | -3.48 |
| MES | 15 | eod | bottom fifth | short | 7197 | +0.247 | 0.589 | +1.45 | -2.05 | -3.04 | -0.12 | -3.60 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.121 | -0.055 | -0.029 | -0.048 | -0.040 | +0.000 | -0.009 | -0.009 | -0.020 | -0.006 | -0.006 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
