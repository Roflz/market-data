# Signal Lab report: what actually moves price, and how sure we are

*Autonomous run of 2026-11-09 (about 12:45 to 15:30 MST). All data ends before the locked holdout (2025-06-30 18:00 ET); the holdout was never touched.*

**Bottom line in three sentences.**
1. The lab can be trusted to say "yes, this metric changes the next move", and it passed every self-test on ES, NQ and YM at 15 and 60 minutes.
2. None of the 96 metrics we tested, including every tool in your kit (EMA 8/20/50, Momentum(14), VWAP, swing levels, high/low of day, candle patterns, pullbacks), moves the **direction** of price by enough to pay for a micro round trip.
3. Many of them reliably change the **size** of the next move. That is useful for stop width, targets and when to trade, but not, on its own, for picking long or short.

**Words used below**
- **Average bar**: the average high-to-low range of the last 20 bars. The lab measures moves in average bars so that quiet and wild years can be compared.
- **$ per micro**: the result of one trade on one micro contract (MES $5/pt, MNQ $2/pt, MYM $0.50/pt).
- **Cost**: one round trip at $1 plus 1 tick each way: MES $3.50, MNQ $2.00, MYM $2.00.
- **Matched bars**: every effect is measured against ordinary bars at the same time of day and weekday, in the same volatility level, EMA trend state and year, with the same last-bar colour. So "NQ went up for 15 years" does not count as an edge.

---

## 1. How much to trust the lab

The lab was checked on real ES, NQ and YM prices, with known answers planted or removed. All 6 market/timeframe combinations **PASSED** every rule. The rules were fixed before the runs (file `out/calibration/self_test_status.json`).

| Check | MES 15m | MES 60m | MNQ 15m | MNQ 60m | MYM 15m | MYM 60m |
|---|---|---|---|---|---|---|
| **False yes:** random signals CONFIRMED, each judged alone | 1 of 200 | 0 of 200 | 1 of 200 | 2 of 200 | 0 of 200 | 0 of 200 |
| **False yes:** random signals CONFIRMED in a 200-metric batch | 0 | 0 | 0 | 0 | 0 | 0 |
| **Smallest edge found 80% of the time**, signal about once per session, $ per micro per trade (tested alone / as 1 of 100 metrics) | $1.17 / $1.80 | $2.55 / $3.90 | $2.03 / $3.12 | $4.43 / $6.79 | $1.27 / $1.95 | $2.78 / $4.25 |
| Same, top fifth vs bottom fifth of a number-type metric (tested alone) | $0.20 | $0.85 | $0.36 | $1.48 | $0.25 | $0.93 |
| Round-trip cost | $3.50 | $3.50 | $2.00 | $2.00 | $2.00 | $2.00 |
| For a no-edge once-per-session signal, edges above this are ruled out | $2.65 | $4.76 | $4.70 | $8.15 | $3.37 | $5.53 |
| **Positive controls** found: last-bar range, time of day, the 8:30 news bar | 3 of 3 | 3 of 3 | 3 of 3 | 3 of 3 | 3 of 3 | 3 of 3 |
| **Negative controls**: 56 real signals moved to the wrong days, CONFIRMED | 0 | 0 | 0 | 0 | 0 | 0 |
| **Look-ahead leaks** planted, caught in every try | 7 of 7 | 7 of 7 | 7 of 7 | 7 of 7 | 7 of 7 | 7 of 7 |

**In plain words:**
- **False yes rate.** A metric judged on its own is wrongly CONFIRMED about 1 time in 300: 4 of 1,200 random signals across the 6 combinations, all 4 labelled "too small to trade". Inside a batch of many metrics the rate was 0 of 1,200.
- **Smallest effect it can see.** On ES and YM 15-min it reliably finds a once-per-session edge of about $1.20-$1.30 per micro. That is well below the cost, so if a cost-beating edge existed there, the lab would see it. On 60-min bars and on NQ, a rare signal needs a bigger edge before the lab can see it ($2.00-$4.40 per micro).
- **Positive controls (things we know are real).**
  - A big last bar is followed by a bigger next bar: +21% to +25%, same sign in 15-16 of 16 years on ES/NQ and 7-8 of 8 on YM.
  - The busy times of day (the slot's usual range, learned from the first half of the data) have bigger bars: +98% to +143%.
  - The 8:30 bar on jobs-report and CPI days is bigger: +149% to +389% (on ES 15-min, a median of 9.5 points vs 3.0 on other days).
  - An independent reviewer rebuilt two of these controls with separate code and got the same numbers.
- **Negative controls (things that must show nothing)** showed nothing.
- **Look-ahead.** The lab catches metrics that peek at future bars, including rare yes/no candle leaks firing on 0.9-13.5% of bars. A peeking metric gets every verdict replaced by INVALID.

**How reliable the four bottom-line labels are** (100 runs per case, edges planted into real prices at a known $ size):

| Planted truth | Called REAL & TRADABLE | Called CONFIDENTLY NOTHING | Mostly called |
|---|---|---|---|
| No edge (random signals) | 0% | 0% (NQ 60, YM 60) to 60% (ES 15) | INCONCLUSIVE everywhere except ES 15 |
| Edge exactly equal to the cost | 3-12% (a wrong "yes") | 0% | REAL BUT TOO SMALL on ES and YM 15; INCONCLUSIVE on NQ and YM 60 |
| Edge twice the cost | 33% (NQ 60) to 100% (ES 15, YM 15) | 0% | REAL & TRADABLE, except NQ 60 (mostly INCONCLUSIVE) |

> **Warning, found after calibration:** the label REAL & TRADABLE is **not reliable at long holds** (16 bars, or held to 16:45). The zoo run (Section 2) caught it calling doji tradable at +$5 to +$15 per trade; in plain dollars the edge was +$0.28 to +$1.90 and not significant. Until this is fixed in the lab, a "tradable" label at a long hold must pass the plain-$ check (`zoo.py dollarcheck`) before you believe it. The same weighting means a direction CONFIRMED at a long hold may be true only in average-bar units, not in dollars, so the plain-$ check applies to it too.

---

## 2. Impact table: what each metric does to price

**What was tested:**
- 96 metrics on ES, NQ and YM, on 5-, 15- and 60-minute bars: 864 market/timeframe tests.
- Every direction and size result was corrected together for testing this many things.
- To count, an effect had to repeat in both halves of the data (2010-17 vs 2018-25; YM: odd vs even quarters), beat a placebo with shuffled days, and keep the same sign in most years.

All 96 metrics passed the look-ahead check. Full ranking: `out/zoo_ranked.csv`. One card per metric: `out/zoo/cards/`.

### 2a. Confident effects on DIRECTION

Only two metric families have a direction effect that survived both the lab and a plain-dollar check. Both are far too small to trade.

| Metric | Where | Best hold | Effect (average bars) | $ per micro per trade, 2018-25 (± 1 standard error) | Cost | Tradable? | Years with same sign |
|---|---|---|---|---|---|---|---|
| Compression candles (doji, spinning top, inside bar, NR7), long | MYM 15-min | 2 bars (30 min) | +0.033 | +$0.36 ± 0.11 | $2.00 | **No** | 8 of 8 |
| same | MYM 5-min | 4 bars (20 min) | +0.052 | +$0.17 ± 0.07 | $2.00 | **No** | 8 of 8 |
| same | MES 15-min | 2 bars (30 min) | +0.017 | +$0.34 ± 0.15 | $3.50 | **No** | 15 of 16 |
| Breakout candles (inside-bar breakout, NR7 breakout, outside bar), in the textbook direction | MES 5-min | 2 bars (10 min) | -0.011 (they go slightly the wrong way) | -$0.40 ± 0.07 | $3.50 | **No**, either way | 14 of 16 |

**What this means.** After a quiet candle, price leans up by a few cents to 36 cents per micro. Breakout candles slightly fail. Both effects are real but far smaller than the $2.00-$3.50 cost. At most they could serve as a small tie-breaker inside a setup that already pays.

**Flagged by the lab but failed the plain-dollar check (treat as no effect):**

| Metric | Lab's $ edge | Plain-$ result | Why it failed |
|---|---|---|---|
| Doji, MES 15-min, held to 16:45 | +$9.69 | +$1.12 ± 4.02 | the long-hold flaw: quiet bars weighted too heavily |
| Doji, MNQ 15-min, held to 16:45 | +$15.10 | +$1.90 ± 6.57 | same |
| Doji, MYM 15-min, 16 bars | +$5.06 | +$0.28 ± 0.77 | same |
| Doji, MNQ 5 and MYM 5 (short holds) | (too small) | +$0.45 and +$0.16 | not significant, far below cost |
| Overnight bars 18:00-02:00, MNQ 60-min, held to close | +$8.89 | +$7.37 ± 8.40 | not significant |
| Momentum(14) divergence, MNQ 5-min, 1 bar | +$0.15 | -$0.03 ± 0.08 | not significant |

Close far above EMA8 leaned back for 1 bar on ES 5-min only; the sign disagreed in most other markets and timeframes, so it does not count.

**Reverse-engineering (Section 3) found the same thing:** 0 of 21 direction tests confirmed.

### 2b. Metrics that change only the SIZE of the move

These change **how far** price moves next, not which way. 38 metrics did this in at least 6 of the 9 market/timeframe panels.

**How to read the %:**
- **Time blocks and yes/no signals:** the next move compared with matched bars.
- **Number-type metrics:** the top fifth compared with the bottom fifth. For example, "price far above EMA8" against "price far below EMA8".

| Metric | Change in next move's size (median, range across panels) | Panels | How to use it |
|---|---|---|---|
| 08:00-09:30 ET | **+91%** (+23% to +118%) | 9 of 9 | Widest stops/targets; best time to need movement |
| 09:30-10:30 ET | **+85%** (+44% to +125%) | 9 of 9 | same |
| 02:00-08:00 ET (Europe) | +46% (+14% to +56%) | 9 of 9 | moderate |
| 10:30-15:00 ET | -15% (-46% to +54%) | 9 of 9 | mixed by market; smaller on average |
| 15:00-16:45 ET | **-52%** (-81% to -42%) | 9 of 9 | Moves are about half size: tighter targets, or skip if a setup needs room to cover costs |
| 18:00-02:00 ET (overnight) | **-52%** (-68% to -9%) | 9 of 9 | same |
| Big bar (range over 2x its 20-bar average) | **+23%** (+20% to +28%) | 9 of 9 | Do not use a tight stop right after a big bar |
| Bar range / previous 20-bar average | +20% (+18% to +24%) | 9 of 9 | same idea, as a number |
| Volume spike (over 2x the usual for that time) | +18% (+15% to +25%) | 9 of 9 | Widen stops after a spike |
| Tall trend bar | +13% (+10% to +16%) | 9 of 9 | same |
| Volume / usual volume for that time | +13% (+10% to +20%) | 9 of 9 | same |
| Continuation candles (short side: +15%) | +10% (+7% to +15%) | 9 of 9 | same |
| Swing break (first close beyond the last swing high/low) | +9% (+7% to +13%) | 8 of 9 | Breakouts bring bigger moves, not a direction |
| Distance below session high | +8% (+4% to +16%) | 8 of 9 | Far from the high: bigger moves |
| New session high or low | +7% (+3% to +10%) | 8 of 9 | Bigger moves, no direction |
| NR7 (narrowest bar of 7) | -7% (-13% to -4%) | 9 of 9 | A quiet bar is followed by a quiet bar, not a breakout |
| Realized volatility, last 20 bars vs last 200 | -11% (-16% to -9%) | 9 of 9 | measured on top of the lab's volatility control; use with care |
| 5/15/60-min trend agreement (all up vs all down) | -11% (-19% to -5%) | 9 of 9 | Up-trend moves are smaller than down-trend moves: smaller stops/targets for longs in agreed up-trends |
| Distance from EMA8 (far above vs far below) | -11% (-15% to -7%) | 9 of 9 | same pattern: being stretched up means calmer moves than being stretched down |
| Distance from EMA20 | -9% (-14% to -6%) | 9 of 9 | same |
| Distance from VWAP | -9% (-17% to -3%) | 8 of 9 | same |
| EMA8 slope (5-bar change) | -8% (-11% to -7%) | 9 of 9 | same |
| Momentum(14) level | -8% (-10% to -7%) | 9 of 9 | same |
| EMA 8/20/50 stack (up vs down) | -5% (-6% to -5%) | 9 of 9 | same |
| Above VWAP vs below | -4% (-8% to -1%) | 8 of 9 | same |

**Others (smaller or less consistent):**
- Also in 6-8 of 9 panels: EMA20 slope, distance to EMA50, distance to swing high/low, position in the session's range, Momentum slope and divergence, pin bar, NR7 breakout, Mondays, doji (-8%), compression candles (-3%).
- In 1-5 panels only: 40 more metrics, for example FOMC day (+26% median, but only 2 of 9 panels) and most single candle patterns.

**The same size effects, confirmed on 2018-25 data the discovery never saw** (Section 3), in $ per micro:

| Signal | Next 15 min | Next hour |
|---|---|---|
| Big bar (top fifth of bar size vs its 20-bar average) | MES +$3.15, MNQ +$4.90, MYM +$2.40 (about +22%) | MES +$4.80, MNQ +$7.30, MYM +$3.60 (about +16%) |
| Volume surge (top fifth vs the usual for that time) | MES +$2.00, MNQ +$2.95, MYM +$1.45 (about +13-14%) | clearly only on ES |
| Narrowest bar of 7 | MES about -$1.00 (-7%); not confirmed on NQ or YM | not confirmed |

For scale: in 2018-25 the average 15-minute bar is about $27 (MES), $45 (MNQ) and $21 (MYM) per micro.

### 2c. No measurable effect on direction or size

Many of these got a confident "any edge is smaller than the round-trip cost" in at least some panels.

- **Engulfing:** nothing.
- **Shooting star:** nothing confirmed.
- **Dark cloud cover:** nothing.
- **Morning / evening star:** nothing.
- **Three inside up/down:** nothing.
- **Inside-bar breakout:** nothing.
- **Breakout family**, long side and short side tested separately: nothing.
- **Bullish reversal patterns (pooled):** nothing.
- **Pullback setups** (shallow, deep, hidden divergence): nothing.
- **Momentum(14) crossing 100:** nothing.
- **Overnight gap at the 18:00 reopen:** nothing.
- **Turn of the month:** nothing.
- **Jobs-report (NFP) days, as a whole day:** nothing. The 8:30 bar itself is huge; see the positive controls.
- **CPI days, as a whole day:** nothing (same note).
- **The 7 textbook signals** (EMA20 gap, Momentum(14), above VWAP, big-bar follow, last-bar return, 4-bar return, range ratio): none CONFIRMED on direction in the calibration batch. Judged one at a time, ES 15 range ratio and NQ 60 Momentum came out REAL BUT TOO SMALL; the rest were CONFIDENTLY NOTHING or INCONCLUSIVE.

---

## 3. Reverse-engineering big moves: did the "obvious" signals survive?

**Method:**
1. Study only 2010-17 (ES and NQ 15-min).
2. Write down 10 candidate signals and freeze them, with the code fingerprinted (sha256) before the test.
3. Test them once on 2018 to mid-2025 on ES, NQ and YM. The fingerprints were re-checked after the test and were unchanged.

**What the discovery half showed:**
- **Big moves were studied three ways:** the top 5% of next-hour moves for each time of day (about 8,600 per market), the top 5% of moves to 16:45, and about 268 strong trend days per market.
- **Before big up hours, price was already up.** It was above EMA8, up in the last hour and making new highs of the day. Before big down hours it was the mirror image, in all 8 years for ES and NQ.
- **That is a hindsight trap.** Across all bars, the same readings were followed by a mild fade instead, and the fade itself was gone after 2017.
- **Bar size and volume** clearly came before big moves, but without a direction.

**Confirmation on 2018-25** (one run; corrected for the 60 tests; all 10 passed the look-ahead check):

| Candidate | What it claims | MES | MNQ | MYM | Survived? |
|---|---|---|---|---|---|
| Fade the stretch from EMA8 | direction, 1 h | CONFIDENTLY NOTHING | INCONCLUSIVE | CONFIDENTLY NOTHING | No |
| Fade the last hour | direction, 1 h | CONFIDENTLY NOTHING | CONFIDENTLY NOTHING | CONFIDENTLY NOTHING | No |
| Fade a new high/low of day | direction, 1 h | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | No |
| Fade the stretch on a volume surge | direction, 1 h | INCONCLUSIVE | INCONCLUSIVE | CONFIDENTLY NOTHING | No |
| Outside bar, drift up into 16:45 | direction | CONFIDENTLY NOTHING | INCONCLUSIVE | INCONCLUSIVE | No |
| Inside bar, drift down into 16:45 | direction | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | No |
| 09:30 bar-size ratio predicts the trend day | direction | INCONCLUSIVE (wrong sign) | INCONCLUSIVE (wrong sign) | INCONCLUSIVE (not confirmed) | No |
| **Big bar, then a bigger move** | size | **CONFIRMED** +22% | **CONFIRMED** +21% | **CONFIRMED** +22% | **Yes** |
| **Volume surge, then a bigger move** | size | **CONFIRMED** +14% | **CONFIRMED** +13% | **CONFIRMED** +13% | **Yes** |
| Narrowest bar of 7, then a smaller move | size | **CONFIRMED** -7% | not confirmed | not confirmed | ES only |

**Results:**
- **Direction: 0 of 21 tests confirmed.** The 7 "confidently nothing" results mean the 90% range of the edge at 1-8 bar holds stayed within about $0.80-$1.80 per micro, under the $2.00-$3.50 cost.
- **Size: the "big move is coming" warning held up.** The direction did not.

---

## 4. How to test any new idea yourself (one command)

1. **Copy `v3/signal_lab/ideas/example_idea.py`** and change the function.
   - It returns one value per bar, using only that bar and earlier bars.
   - Pick a `kind`:
     - `sided`: +1 long, -1 short, 0 nothing.
     - `event`: 1 yes, 0 no.
     - `continuous`: any number.
     - `state`: a few ordered levels.
   - Put long and short in separate metrics, because pooling the two sides can hide a one-sided edge.
2. **Run it from `research/confidence`:**

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3:v3/signal_lab OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3 nice -n 5 python3 v3/signal_lab/try_idea.py v3/signal_lab/ideas/my_idea.py
```

**What the command does:**
- **Markets and timeframes:** by default it tests ES, NQ and YM on 15- and 60-min bars, the combinations the lab is calibrated for. Add `ES,NQ,YM 5,15,60` to include 5-min bars, which are uncalibrated and must run under the heavy lock.
- **Run time:** in the 2-metric demo below, each market and timeframe took 0.4-4 seconds after loading (plus the look-ahead check).
- **Output:** one impact card per metric in `out/ideas/my_idea/cards/<metric>.md`, plus a summary table.
- **Logging:** every test is added to `out/trials.csv`, so the "how many things have we tried" count stays honest.

**The demo run:** I ran the example file, an EMA20 pullback in an EMA 8/20/50 stack with long and short as separate metrics; its 12 tests are logged.
- **Direction:** INCONCLUSIVE everywhere. MES 15-min: best hold $0.26 per trade, 90% range up to $1.74, against a $3.50 cost.
- **Size:** after a long pullback signal, moves were **8-11% bigger** on MES 15/60 and MYM 15 (CONFIRMED).

**How to read an impact card:**

| Line on the card | Meaning | What to do |
|---|---|---|
| **INVALID (LOOK-AHEAD)** | The metric uses future bars. None of its numbers mean anything. | Fix the code. |
| **REAL & TRADABLE** | Confirmed, and the cautious (lower 80%) 2018-25 edge per trade in $ beats the cost. | At 16-bar or to-16:45 holds, run the plain-$ check first (Section 1 warning). Then build a strategy and confirm it once on the holdout. |
| **REAL BUT TOO SMALL** | The effect is real, but not clearly bigger than the cost. | Use it only as a filter or for sizing. |
| **CONFIDENTLY NOTHING** | Any edge at 1-8 bar holds is smaller than the cost, with 90% confidence. | Drop it as a direction signal. |
| **INCONCLUSIVE** | Not confirmed, but a cost-sized edge cannot be ruled out. The card gives the largest edge still possible and roughly how much more data would settle it. | Treat it as unproven. Do not trade it. |
| **Size: moves X% MORE / LESS** | How much bigger or smaller the next move is than on matched bars, with q-value and years with the same sign. | Use it for stop and target width, and for when to trade. |
| **Self-test: PASSED / UNCALIBRATED** | Whether the lab was proven on this market and timeframe. | Treat UNCALIBRATED (5-min) verdicts as indicative only. |

**The rule that makes a "yes" trustworthy:** decide the idea, its side and its hold before you look, and test it once. If you tweak it after seeing a card, the tweak is a new test and counts against you.

---

## 5. Honest caveats

- **The tradability label has a known flaw at long holds.** Moves are measured in average bars, and over 16 bars or to 16:45 that gives quiet bars too much weight. This made doji look tradable. The fix (make the plain-$ check a required gate, plus a calibration case for a metric that fires on quiet bars) is **not built yet**.
- **5-minute results are not calibrated.** The self-tests covered 15- and 60-min bars only.
- **A confident "no" is rare outside ES 15-min.** For rare signals on 60-min bars and on NQ, expect INCONCLUSIVE with an "edges above $X are ruled out" figure, not a firm no.
- **The long-hold part of "confidently nothing" uses a best estimate, not a confidence range.** An edge exactly at cost that only shows at long holds could still be called "nothing" up to about half the time.
- **Both sides are pooled unless tested separately.** In the zoo, only the candle families were also split long-only and short-only. A one-sided effect of a single pattern could be hidden.
- **Per-trade $ figures count every signal bar as a trade.** Many metrics fire on bars in a row, so these are per-signal averages, not a strategy's P&L.
- **Top and bottom fifths use cut points from the whole sample.** That is fine for measuring an effect, but a live rule must use cut points from past data only.
- **Event-day flags cover the whole day.** NFP, CPI and FOMC were not tested on the release bar alone, which is probably why they show "no effect" despite the huge 8:30 bar.
- **Some rules were set during the run.** The zoo's "confident direction" ranking rule and the plain-$ check were written during the run, not pre-registered. Before today, more than 4,000 configurations had been tried. This run logged at least 1,035 more tests to `trials.csv`: 897 zoo, 120 reverse, 6 calibration and 12 demo.
- **Market differences:** YM has data only from 2018, so its replication splits by alternate quarters, which is weaker than splitting by years. Effects are measured after removing time-of-day, weekday, volatility, trend, last-bar-colour and year effects. A metric that only repeats those gets no credit.
- **The holdout (after 2025-06-30) is untouched.** Nothing here is confirmed on it. Anything that ever looks tradable should be tested on it **once**, as a full strategy with costs.
- **Shared code in the parallel workflow.** The look-ahead check used by the parallel edge-hunt-v3 experiments (`harness.lookahead_check`, 20 random cuts) probably has the same rare-leak weakness this lab had before it was fixed. I did not touch it.

---

### Files

| What | Where |
|---|---|
| The lab | `v3/signal_lab/lab.py` |
| Self-tests and calibration report | `v3/signal_lab/calibrate_lab.py`, `test_lab.py`; `out/calibration/calibration_report.md`, `out/calibration/self_test_status.json` |
| Your one-command tester | `v3/signal_lab/try_idea.py`, example `v3/signal_lab/ideas/example_idea.py`; demo cards in `out/ideas/example_idea/cards/` |
| 96-metric zoo | `v3/signal_lab/zoo.py`; `out/zoo_ranked.csv`, `out/zoo/zoo_batch.csv`, `out/zoo/dollar_check.csv`, `out/zoo/cards/` |
| Reverse-engineering | `reverse_*.py`; `out/reverse_candidates.md`, `out/reverse/discovery_2010_17.csv`, `out/reverse/confirm/confirm_summary.csv`, `out/reverse/confirm/cards/` |
