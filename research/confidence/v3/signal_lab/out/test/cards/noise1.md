# Impact card: noise1

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.071 R20 over the next 8 bars (2 h), p=0.35; we would catch an effect of 0.073 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.40 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.587 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.021 | -0.002 .. +0.045 | +0.0070 | 0.077 / 0.11 / 0.11 | 0.122 |  |  | 2/2 | +0.014 | +0.036 |  | +1.5 / +1.8 |  |
| MES | 15 | h2 | +0.009 | -0.025 .. +0.043 | +0.0030 | 0.61 / 0.64 / 0.65 | 0.674 |  |  | 2/2 | +0.005 | +0.016 |  | +0.4 / +0.5 |  |
| MES | 15 | h4 | +0.042 | -0.006 .. +0.090 | +0.0089 | 0.089 / 0.14 / 0.14 | 0.146 |  |  | 2/2 | +0.040 | +0.046 |  | +1.5 / +1.7 | 0.073 |
| MES | 15 | h8 * | +0.071 | +0.003 .. +0.138 | +0.0091 | 0.041 / 0.059 / 0.081 | 0.0773 | 1 | 0.7 | 2/2 | +0.055 | +0.099 | False | +1.7 / +2.0 |  |
| MES | 15 | h16 | +0.038 | -0.065 .. +0.141 | +0.0039 | 0.47 / 0.49 / 0.52 | 0.53 |  |  | 1/2 | -0.028 | +0.161 |  | +0.7 / +0.7 |  |
| MES | 15 | eod | -0.109 | -0.299 .. +0.081 | -0.0067 | 0.26 / 0.29 / 0.3 | 0.312 |  |  | 1/2 | -0.270 | +0.190 |  | -1.1 / -1.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.006 | -0.009 .. +0.022 | +0.9% | +0.014 | 0.46 |  | 2/2 |
| MES | 15 | h2 * | +0.016 | -0.009 .. +0.042 | +1.7% | +0.008 | 0.21 | 1 | 2/2 |
| MES | 15 | h4 | -0.004 | -0.051 .. +0.042 | -0.3% | +0.005 | 0.86 |  | 1/2 |
| MES | 15 | h8 | -0.007 | -0.048 .. +0.034 | -0.4% | -0.012 | 0.81 |  | 1/2 |
| MES | 15 | h16 | -0.008 | -0.062 .. +0.045 | -0.3% | -0.010 | 0.8 |  | 1/2 |
| MES | 15 | eod | +0.013 | -0.104 .. +0.131 | +0.3% | +0.038 | 0.84 |  | 1/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +1.41 pts | +0.30 .. +2.53 | 0.11 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | short | 7197 | +0.015 | 0.588 | +0.08 | -3.42 | -3.50 | -3.27 | -3.43 |
| MES | 15 | h2 | bottom fifth | short | 7197 | +0.007 | 0.588 | +0.04 | -3.46 | -3.57 | -3.26 | -3.49 |
| MES | 15 | h4 | bottom fifth | short | 7197 | +0.025 | 0.588 | +0.15 | -3.35 | -3.52 | -3.04 | -3.41 |
| MES | 15 | h8 | bottom fifth | short | 7197 | +0.046 | 0.588 | +0.29 | -3.21 | -3.53 | -2.65 | -3.35 |
| MES | 15 | h16 | bottom fifth | short | 7197 | +0.077 | 0.588 | +0.45 | -3.05 | -3.75 | -1.78 | -3.37 |
| MES | 15 | eod | top fifth | short | 7196 | +0.274 | 0.590 | +1.60 | -1.90 | -2.28 | -1.18 | -3.46 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.006 | -0.042 | -0.008 | -0.010 | -0.001 | +0.000 | +0.022 | +0.009 | +0.047 | +0.079 | +0.023 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
