# Raw-data pattern search: ES / NQ / YM (micro futures)

## Findings in brief

**Direction: no.** Raw market statistics do not predict which way price goes next in a way you can trade. This holds at 5 minutes, 15 minutes, 60 minutes and to 16:45 ET, on MES, MNQ and MYM. It applies to states, motifs, their combinations, a linear model and a nearest-neighbour analog model. After costs, every direction test loses money per micro, or its confidence interval includes zero.

**Size: yes, strongly.** The same statistics predict how big the coming move will be (its forward high-low range). Out of sample they explain about 66-70% of the variation (correlation about 0.82), compared with 47-51% from time of day alone. This is useful for position size and for stop and target distances. It does not tell you which side to take.

| Question | Answer | $ per micro after costs (out of sample, 2022 to 2025-06) |
|---|---|---|
| Does any state or motif shift the average forward move? | No. 0 of 1,552 tests significant after correction (smallest BY q = 0.60) | n/a |
| Does any state or motif shift the chance the next bar closes up? | Yes, but only by 1.3-3.4 percentage points, almost all at 5 minutes (18 cells) | ES -$3.3 to -$3.6, NQ -$1.4 to -$1.9, YM -$1.6 to -$2.0. All 18 have a 95% CI entirely below 0 |
| Best global model, top and bottom 10% of predictions, 5-60 min | Correlation 0.00-0.02, R^2 about 0 | ES -2.1 to -3.2, NQ -2.6 to +0.6 (CI includes 0), YM -1.3 to -2.2 |
| Same model, hold to 16:45 | Positive point estimates; every CI includes 0 | ES ridge +$10.3 [-7.9, 28.9]; time-of-day-only reference ES +$6.3, NQ +$14.7. This is the market's upward drift, not skill |
| Can the size of the next 15-60 min range be predicted? | Yes | Correlation 0.81-0.83, R^2 0.66-0.70 (time of day alone 0.47-0.51) |

## How the study was run

- **Data:** 1-minute bars for the ES, NQ and YM front contracts. One sample every 5 minutes from 18:05 to 16:40 ET, in each Globex session from 2018 to 2025-06-27. ES and NQ have 525,326 samples each; YM has 523,859.
- **Discovery** (2018-2021): the states and motifs were found without looking at any forward return. The fitted models were then frozen and their sha256 hashes recorded.
- **Confirmation** (2022-01-01 to 2025-06-27): the frozen models were tested once and never refitted. This period has now been used.
- **Holdout** (from 2025-06-30 18:00 onward): never loaded. Asserts in the code enforce this.
- **Inference:**
  - Each result is compared with a matched baseline: the same market, the same 15-minute clock slot and the same year.
  - Uncertainty comes from a stationary block bootstrap over whole sessions (mean block 5 sessions, B = 2000).
  - Multiple tests are corrected with Benjamini-Yekutieli.
  - A surviving cell must also have the same sign in at least 2 of the 3 markets and in both 2022-23 and 2024-25H1.
- **Costs per round trip:** MES $3.50, MNQ $2.00, MYM $2.00. No stops were used, so no extra stop tick applies.

## The raw statistics used

All are computed only from data available at the sample time; a truncation test confirmed this, 30 of 30 rows per market and 20 more on a re-check. No custom indicators or composite scores are used. Each statistic is scaled by recent per-minute volatility where relevant.

- **Returns:** over the last 1, 5, 15, 30, 60, 120 and 240 minutes; since the session open; since 09:30; the previous session's return.
- **Volatility and range:** realised volatility and high-low range over 15, 60 and 240 minutes, and where price sits inside each range.
- **Session location:** distance to the session high and low, position within the session range, distance from VWAP.
- **Volume:** volume relative to the same clock time over the last 20 sessions, at 5, 15 and 60 minutes; signed-volume imbalance over 15 and 60 minutes; share of up minutes in the last 30.
- **Microstructure:** lag-1 autocorrelation of 1-minute returns over 60 minutes. It averages -0.067 on ES, so minutes mildly mean-revert.
- **Path shape:** the shape of the last 60 minutes as 12 points, normalised.
- **Cross-market:** the other two indices' 15- and 60-minute returns. ES and NQ 15-minute returns correlate at 0.91.

## What was found in 2018-2021 (descriptive)

States come from 31 statistics, reduced by PCA to 13 components and grouped with a Gaussian mixture into 12 states. Motifs are k-means clusters of the 60-minute path shape, 10 in all. Cluster stability was only moderate (best min-ARI 0.46 for states and 0.52 for motifs). The market behaves like a continuum, so these are useful bins rather than distinct regimes.

### States

| State | Freq ES/NQ/YM | Typical stay | Share in RTH | Peak hours ET | Plain description |
|---|---|---|---|---|---|
| S0 | 12/12/13% | 15 min | 32% | 13, 06, 07 | average on everything |
| S1 | 11/14/12% | 17 min | 4% | 00, 23, 01 | quiet overnight, low volume, choppy minutes |
| S2 | 13/12/12% | 12 min | 9% | 02, 01, 20 | quiet grind up near session high |
| S3 | 12/12/12% | 13 min | 20% | 07, 06, 08 | quiet, near high, session up, above VWAP |
| S4 | 11/11/11% | 15 min | 7% | 20, 02, 21 | quiet drift down near session low, below VWAP |
| S5 | 7/7/7% | 13 min | 62% | 12, 13, 11 | volatile up session near its high |
| S6 | 7/6/6% | 11 min | 31% | 03, 20, 04 | near high, top of hour's range, volume on up minutes |
| S7 | 6/6/6% | 14 min | 31% | 03, 04, 09 | near session low, falling, high volume |
| S8 | 6/5/6% | 10 min | 62% | 15, 16, 10 | sharp 15-min drop, volume on down minutes |
| S9 | 5/6/5% | 20 min | 81% | 11, 10, 12 | high-vol, high-volume down session, trending minutes |
| S10 | 5/5/5% | 13 min | 68% | 10, 09, 16 | sharp rise to top of hour's range |
| S11 | 4/4/4% | 16 min | 73% | 10, 09, 11 | volatile selloff near session low |

Notes on the states:
- Frequencies are nearly identical across the three markets.
- States are strongly tied to time of day, which is why every test uses a clock-matched baseline.
- In 2022-25, S1 grew from 11-14% to 18-21% of samples. This suggests the distribution of the statistics shifted after 2021.

### Motifs (shape of the last 60 minutes)

| Motif | Freq | Shape |
|---|---|---|
| M0 | 16% | S-curve up |
| M1 | 14% | S-curve down |
| M2 | 12% | flat, then late breakdown |
| M3 | 12% | sharp early rise, then flat at the high |
| M4 | 10% | flat, then late breakout |
| M5 | 8% | sharp early fall, then flat at the low |
| M6 | 7% | V, low about 20 minutes in |
| M7 | 7% | late V that rebounds above the start |
| M8 | 7% | late inverted V ending below the start |
| M9 | 6% | early inverted V, gives back about half |

Motif shares are nearly identical across markets and times of day (28-31% fall in regular trading hours).

## Confirmation results (2022 to 2025-06-27, tested once)

**Checks:** all frozen hashes matched. Re-labelling the discovery rows reproduced the saved labels 100%. Each market has 244,618 confirmation samples over 901 sessions.

**Average forward move:**
- 58 of 1,552 tests had p < 0.05. Chance alone would give about 78.
- 0 tests survive correction.
- The pre-registered momentum-or-reversal questions were:
  - sharp-move states S8, S10 and S11;
  - late-break motifs M2, M4 and M7.

  Their smallest q is 1.0, so they show nothing.

**Chance the next bar closes up:** 18 cells survive correction and the consistency rules. Almost all are at 5 minutes.
- More often up: S4 (quiet drift near the low) on ES, NQ and YM; S7 on ES and YM; M2 on ES, NQ and YM; S8 on YM.
- Less often up: S2 (quiet grind near the high) on ES, NQ and YM; S6 on YM.
- The base rate is 0.47-0.50, because many 5-minute returns are exactly zero, and how often that happens differs by state (ES: 13.3% in S1 against 2.6% in S9). These are tick-level bounce effects worth cents.

**$ per micro per trade for the 18 cells** (non-overlapping trades):

| Market | Gross | Net after cost |
|---|---|---|
| MES | -$0.06 to +$0.16 | -$3.3 to -$3.6 |
| MNQ | +$0.07 to +$0.64 | -$1.4 to -$1.9 (best: S4 with M5, long, -$1.37, CI [-1.89, -0.85]) |
| MYM | +$0.02 to +$0.43 | -$1.6 to -$2.0 |

**Size of the coming range, compared with the matched baseline (log units):**
- **Wider:** S9 and S11 +0.30 to +0.36 (about 35-43% wider); S10 +0.12 to +0.17; S7 +0.13 to +0.15; S8 +0.08 to +0.11.
- **Narrower:** S1 -0.16 to -0.20 (about 18% narrower, and understated, see below); S2 about -0.10; S6 -0.07 to -0.10.
- **Motifs:** all within +/-0.08. The widest is M2, the late breakdown.
- 562 of 774 size tests survive. The effects hold in all 3 markets and in both sub-periods.

## Benchmarks: linear (ridge) and analog (nearest-neighbour)

Both models were trained on 2018-21 and scored on 2022 to 2025-06. The tables show out-of-sample correlation between prediction and outcome, with 95% bootstrap CIs.

| Direction | 5 min | 15 min | 60 min | to 16:45 |
|---|---|---|---|---|
| ES ridge | 0.011 [0.005, 0.017] | 0.013 [0.006, 0.019] | 0.017 [0.004, 0.030] | 0.012 [-0.035, 0.063] |
| ES analog | 0.019 [0.007, 0.030] | 0.006 n.s. | about 0 | 0.013 n.s. |
| NQ ridge | 0.008 [0.002, 0.014] | 0.008 n.s. | 0.010 n.s. | 0.009 n.s. |
| NQ analog | 0.012 [0.003, 0.021] | about 0 | 0.005 n.s. | 0.012 n.s. |
| YM ridge | 0.004 n.s. | 0.006 n.s. | 0.010 n.s. | 0.025 n.s. |
| YM analog | about 0 | about 0 | about 0 | about 0 |

R^2 for direction is between -0.017 and +0.0003 everywhere, so the models explain essentially none of the variation. A few correlations at 5-15 minutes are statistically different from zero on ES and NQ, but they are far too small to cover $2-3.50 a trade.

Trading the top and bottom 10% of predictions gives the following net $ per micro per trade.

| Horizon | MES | MNQ | MYM |
|---|---|---|---|
| 5 min | -2.8 to -3.2 | -1.1 to -1.5 | about -2.0 |
| 15 min | -2.9 to -3.1 | -1.2 to -2.6 | -1.9 to -2.2 |
| 60 min | -2.1 to -2.7 | +0.60 (ridge, CI [-1.6, 2.7]) | -1.3 to -1.7 |
| to 16:45 | +3.3 to +10.3 (CIs include 0) | +0.2 to +6.1 | +1.5 to +4.7 |

The 16:45 results come from only about 880 trades per market, and a time-of-day-only reference does as well or better (ES +$6.3, NQ +$14.7). They reflect the 2022-25 upward drift, not skill.

| Size (log forward range) | Corr, 15 min | Corr, 60 min | R^2 |
|---|---|---|---|
| Ridge | 0.82-0.83 | 0.81-0.82 | 0.66-0.70 |
| Analog | 0.77-0.79 | 0.79-0.80 | 0.59-0.62 |
| Time of day only | 0.70-0.74 | 0.71-0.74 | 0.47-0.51 |

## Skeptic's review (independent re-check)

**No blocking issues.** Every headline number was recomputed from the output files and from raw 1-minute bars, and all matched:
- Features: 20 of 20 matched on a new truncation test. With the control tightened to rows whose forward return is not zero, the truncated data reproduced the forward return in 0 of 20 rows.
- 15 rows were recomputed by hand from 1-minute bars, and all matched.
- Hashes, the 2018-2021-only fitting, the cost deductions and the counts of significant tests all matched.

Four caveats affect how the results should be read:
1. **Side used in the economics test.** The $ test traded each cell in the direction of its mean-return effect. For 5 of the 18 cells that is the opposite of the hit-rate effect: ES M2, NQ S2, NQ S4, NQ M2, and YM M2 at 15 minutes. Their gross is only $0.01-$0.33, so trading them the other way still loses after costs. The side was also chosen using the confirmation data, which flatters the result, and the cells lose anyway.
2. **S1's narrowing is understated by about 40%.** S1 makes up about 42% of its own clock-slot baseline, which pulls its effect toward zero.
3. **Hit rate partly measures how often returns are exactly zero,** which differs by state.
4. **Benchmark correlation CIs** are not corrected for multiple testing. The effect sizes are negligible either way.

## What this means for next steps

1. **Stop looking for direction in raw statistics at intraday horizons on these three markets.** States, path motifs, linear models and analogs all agree. Across the 5-minute to end-of-day horizons the best out-of-sample correlation is about 0.02. A trade needs much more than that to clear $2.00-$3.50.
2. **Use the volatility forecast for sizing and distances, not for side.** The coming 15-60 minute range is about 70% explainable. Options:
   - scale contracts so that dollar risk stays constant;
   - set stop and target distances from the forecast range;
   - skip trades when the forecast range is too small to pay the costs (S1 overnight is about 18% or more narrower).

   Any of these would need its own pre-registered test on fresh data. The confirmation period is now spent, and the holdout from 2025-06-30 is still untouched for one final test.
3. **Treat the end-of-day long result as beta.** Holding long to 16:45 made money in 2022-25 whatever the signal said. This is market drift and should not be counted as an edge.
4. **If you search for direction again, it needs different information:** order book, events, longer horizons, or other assets. The 1-minute bar statistics tested here have been tested thoroughly.

Files are in `research/confidence/v4/` (features.py, discover.py, confirm.py) and `research/confidence/v4/out/`:
- confirm_tests.csv
- confirm_survivors.csv
- confirm_econ.csv
- confirm_bench.csv
- frozen/FROZEN.md
