# Impact card: planted

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: moves price up 0.241 average bars (top-minus-bottom spread ~$1.44; ~$0.72 per trade when trading both ends, at 2018-25 bar sizes) over the next 4 bars (1 h) (top fifth vs bottom fifth of the metric), same sign in 2 of 2 years, q=6.25e-12; best leg (bottom fifth, short) grosses $+0.76 and nets $-2.74 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 15-min size: no measurable effect on how much price moves (best p=0.041).
- MES 15-min BOTTOM LINE (direction): REAL BUT TOO SMALL (look-ahead UNCHECKED) - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.62, pessimistic $+0.45) does not clearly beat the $3.50 round trip: use it as a filter or for sizing only. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.065 | +0.041 .. +0.089 | +0.0253 | 7.8e-08 / 7.4e-07 / 1.1e-05 | 0.00276 |  |  | 2/2 | +0.060 | +0.074 |  | +4.6 / +5.4 |  |
| MES | 15 | h2 | +0.135 | +0.098 .. +0.171 | +0.0408 | 4.1e-13 / 8.6e-13 / 8.5e-11 | 0.00276 |  |  | 2/2 | +0.144 | +0.117 |  | +6.7 / +7.3 |  |
| MES | 15 | h4 * | +0.241 | +0.193 .. +0.289 | +0.0518 | 8.4e-23 / 8.9e-20 / 5.5e-17 | 0.00276 | 6.25e-12 | 0 | 2/2 | +0.260 | +0.207 | True | +8.4 / +9.8 | 0.076 |
| MES | 15 | h8 | +0.269 | +0.193 .. +0.345 | +0.0378 | 3.3e-12 / 2.3e-11 / 1.9e-11 | 0.00276 |  |  | 2/2 | +0.302 | +0.208 |  | +6.6 / +7.0 |  |
| MES | 15 | h16 | +0.314 | +0.212 .. +0.416 | +0.0322 | 1.7e-09 / 1.1e-08 / 1.2e-08 | 0.00276 |  |  | 2/2 | +0.317 | +0.307 |  | +5.6 / +6.0 |  |
| MES | 15 | eod | +0.283 | +0.133 .. +0.432 | +0.0163 | 0.00021 / 0.0011 / 0.0026 | 0.00276 |  |  | 2/2 | +0.316 | +0.220 |  | +2.8 / +3.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.005 | -0.022 .. +0.012 | -0.7% | -0.005 | 0.99 |  | 1/2 |
| MES | 15 | h2 | -0.011 | -0.032 .. +0.011 | -1.1% | -0.005 | 0.71 |  | 2/2 |
| MES | 15 | h4 | -0.024 | -0.063 .. +0.015 | -1.8% | -0.012 | 0.26 |  | 1/2 |
| MES | 15 | h8 | -0.041 | -0.093 .. +0.010 | -2.2% | -0.040 | 0.19 |  | 2/2 |
| MES | 15 | h16 * | -0.109 | -0.187 .. -0.030 | -4.1% | -0.048 | 0.0069 | 1 | 2/2 |
| MES | 15 | eod | -0.026 | -0.154 .. +0.102 | -0.6% | -0.037 | 0.83 |  | 1/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +4.80 pts | +3.43 .. +6.18 | 7.7e-09 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | short | 7197 | +0.043 | 0.589 | +0.25 | -3.25 | -3.26 | -3.23 | -3.26 |
| MES | 15 | h2 | bottom fifth | short | 7197 | +0.075 | 0.589 | +0.44 | -3.06 | -3.08 | -3.02 | -3.09 |
| MES | 15 | h4 | bottom fifth | short | 7197 | +0.130 | 0.589 | +0.76 | -2.74 | -2.83 | -2.59 | -2.79 |
| MES | 15 | h8 | bottom fifth | short | 7197 | +0.156 | 0.589 | +0.92 | -2.58 | -2.68 | -2.40 | -2.71 |
| MES | 15 | h16 | bottom fifth | short | 7197 | +0.216 | 0.589 | +1.27 | -2.23 | -2.54 | -1.65 | -2.53 |
| MES | 15 | eod | bottom fifth | short | 7197 | +0.434 | 0.589 | +2.59 | -0.91 | -1.47 | +0.13 | -2.54 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.053 | -0.004 | -0.021 | -0.013 | -0.012 | +0.000 | +0.065 | +0.131 | +0.237 | +0.267 | +0.310 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
