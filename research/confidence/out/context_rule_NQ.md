# Stronger "after a decline / after a rise" context, MNQ 15-min (context_rule.py)

**Rule.** A bullish reversal pattern has *strong context* when all three hold. A bearish pattern uses the mirror image.
1. The close of the reference bar is at least X average bars (X * R20) below the highest high of the 10 bars that end at that bar. X is 1.5 or 3.
2. EMA 10 at the reference bar is lower than it was 3 bars earlier.
3. The pattern's lowest low is within 0.5 average bars of the lowest low of the last 10 bars, the pattern bar included.

The reference bar is the bar the existing EMA-10 rule already checks. For one-bar patterns it is the bar before. For two-bar patterns (engulfing, harami, piercing, dark cloud, tweezer) it is their first bar. For morning/evening star and three inside it is also the first bar, two bars back. Every window must stay within one contract and uses only bars up to the signal bar's close.

Patterns covered: hammer, hanging man, inverted hammer, shooting star, dragonfly doji, gravestone doji, engulfing, harami, piercing, dark cloud, tweezer, morning/evening star and three inside. An event counts as strong if any of its reversal patterns in the event's direction has strong context.

All figures are net $ per trade on 1 micro after costs, using the 1.5R target and the v1 stop. Years are 2013 to June 2025 (the out-of-sample period).

## Every event taken (no model)
| group | trades | $/trade | hit rate |
|---|---:|---:|---:|
| all events | 273,954 | -2.22 | 33.8% |
| non-reversal events | 213,686 | -2.36 | 32.2% |
| reversal events (current loose rule) | 60,268 | -1.71 | 39.3% |
| reversal, strong X=1.5 | 32,166 | -1.51 | 40.1% |
| reversal, loose only X=1.5 | 28,102 | -1.94 | 38.5% |
| reversal, strong X=3 | 14,517 | -1.63 | 40.3% |
| reversal, loose only X=3 | 45,751 | -1.73 | 39.0% |

Strong X=1.5 beats loose-only in 9 of 13 years. It loses in 2015, 2021, 2022 and 2024. Both groups lose money in every year except 2020 and 2022. Per pattern, the strong context helps the hammer (X=3: +2.82 vs -2.62 loose only) and the morning star (X=3: +4.39 vs -0.53). It hurts the shooting star, piercing and gravestone doji. These per-pattern groups are small (200 to 1,400 trades), so treat them as leads only.

## v1 logit walk-forward (out of sample, 2013 to 2025H1)
| run | AUC | kept | $/trade kept | all events $/tr | random skip $/tr (5-95%) |
|---|---:|---:|---:|---:|---:|
| v1 logit (reference) | 0.619 | 26,399 | -0.69 | -2.22 | -1.93 (-2.37 .. -1.56) |
| all events + strong_ctx X=1.5 | 0.619 | 26,430 | -0.90 | -2.22 | -2.04 (-2.44 .. -1.66) |
| all events + strong_ctx X=3 | 0.619 | 23,667 | -0.80 | -2.22 | -2.00 (-2.48 .. -1.58) |
| strong-context events only X=1.5 | 0.532 | 2,925 | +0.29 | -1.51 | -1.32 (-2.90 .. +0.42) |
| strong-context events only X=3 | 0.517 | 3,470 | -1.01 | -1.63 | -1.74 (-2.96 .. -0.50) |
| control: all reversal events (loose) | 0.542 | 11,970 | -1.03 | -1.71 | -1.65 (-2.41 .. -0.91) |

The strong_ctx weight is about +0.03 per unit (median over folds), which is close to zero. Year by year, the strong-only X=1.5 model wins in 6 of 13 years and loses in 7. It loses -5.9 $/trade in 2025H1. Its +0.29 sits inside the random-skip range, and X=3 does not repeat it. Per-year detail is in context_rule_NQ.csv (sections wf_by_year and unfiltered_by_year).

## Conclusion
Requiring a real decline (or rise) before a reversal candle helps a little when every trade is taken. With the milder version (1.5 average bars), these trades lose about 0.43 $/trade less than reversals without a real move, and win about 1.6 points more often. The stricter version (3 average bars) adds nothing. Even so, they still lose money in almost every year. Adding the context to the model does not improve it: it stays at about -0.8 to -0.9 $/trade, against -0.69 for the v1 model. Trading only strong-context reversals with the model gives +0.29 $/trade, but only in some years, within the range of random skipping, and not with the stricter version, so it is most likely luck. Keep the stronger context as a possible per-pattern filter (hammer, morning star) to test on ES and YM. It is not an edge on its own.
