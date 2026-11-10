# Confidence-weighted entries and exits: build spec (v1)

Goal: learn a CONFIDENCE (probability) for every textbook-direction entry signal and for every "should I exit now" moment
in an open trade, from all our signals plus context, and show the learned weights as a readable scorecard.
Method = meta-labeling (research/signals/CONFIDENCE_RESEARCH.md): the textbook rule proposes, a model scores.
Everything is judged in net $ per 1 micro contract after costs, out of sample, against simple baselines.

Run convention: `cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 x.py`
Reuse `research/signals/signals.py` (bars, context, pivots, patterns, PATTERN_RULES, SPEC) and
`research/signals/exits.py` (session_frame = 16:45 ET cutoff, next_true, fresh, pattern_extreme, SPAN).
scikit-learn 1.9 is available (LogisticRegression, HistGradientBoostingClassifier, CalibratedClassifierCV,
IsotonicRegression). No lightgbm/xgboost/statsmodels.

v1 scope: 15-minute bars; markets ES, NQ, YM (traded as MES $5/pt, MNQ $2/pt, MYM $0.50/pt). Code must take tf and sym
as parameters so 5/60-minute runs work later.

## Costs (every label)
Round trip per micro = $1.00 commission + 1 tick slippage on entry + 1 tick on exit (= signals.SPEC cost) and ONE EXTRA
tick when the exit is a STOP fill (stops slip). Tick $: MES 1.25, MNQ 0.50, MYM 0.50.

## Timing rules (no look-ahead)
* A tf-bar's index = its START time (New York). Its OHLC is known at its close = start + tf.
* A signal/feature for bar t uses only data up to the close of bar t. Entry fills at the OPEN of bar t+1 (same session
  segment `seg` and contract). Nothing is entered on bars that start after 16:45 - tf (exits.session_frame `allowed`).
* Swing pivots (signals.pivots, k bars each side) are known only at the close of bar p+k.
* Higher-timeframe (60-min) values may be used at a 15-min bar t only if the 60-min bar has CLOSED by t's close.
* Other markets' values at bar t: only their bars with the same start time (closed at the same moment) or earlier.

## Module 1: features.py
`build_features(sym, tf, others=("ES","NQ","YM")) -> (b, F)`; b = signals.bars(sym, tf) (+ ctx columns as needed),
F = DataFrame on b.index, float32, every column known at the close of its bar. Columns (SIGNED features use +1 =
bullish / -1 = bearish; the model multiplies them by the trade direction d so that + means "with the trade"):
* `pat_<name>` for each of the 25 directional patterns: signals.patterns value (+1/-1/0). Neutral ones (doji, spinning
  top, inside bar, nr7) as 0/1 `pat_<name>`.
* families (signed, sum of member patterns clipped to [-1, 1]): `fam_reversal` (hammer, inverted_hammer, hanging_man,
  shooting_star, dragonfly_doji, gravestone_doji, engulfing, harami, piercing, dark_cloud, morning_evening_star,
  three_inside, tweezer, pin_bar), `fam_continuation` (three_soldiers_crows, marubozu, tall_trend_bar), `fam_breakout`
  (inside_bar_breakout, nr7_breakout, outside_bar), `fam_closeloc` (clv_extreme, clv5_extreme, bar_80_20),
  `fam_exhaustion` (five_lower_lows_higher_highs).
* scale unit R20 = mean (H-L) of the 20 bars BEFORE t (same contract run); distances are in R20 units ("bars").
* structure, for k in (5, 10): `dist_swhi_k`, `dist_swlo_k` (close to latest CONFIRMED swing high/low, R20 units),
  `brk_k` signed fresh break (+1 = first close above latest swing high, -1 = first close below latest swing low),
  `struct_k` (+1 if the last two confirmed swing highs AND lows are rising, -1 if both falling, else 0),
  `fibpos_k` = where the close sits in the latest confirmed swing leg (0 = leg start, 1 = leg end, signed by the leg's
  direction), `atfib_k` = 1 if within 0.15 R20 of the 0.382/0.5/0.618 level of that leg.
* trend: `ema_stack` (+1/-1/0), `ema20_slope` (EMA20 change over 10 bars, R20 units), `dist_ema8/20/50` (R20),
  `above_ema20_share` (share of last 20 closes above EMA20, mapped to [-1,1]).
* momentum: `mom` = mom14 - 100, `mom_slope3` (change over 3 bars), `mom_x100` signed fresh cross of 100.
* VWAP: `dist_vwap` (R20), signed.
* bar: `rng_rel` (range / R20), `body_frac`, `clv` (close location 0..1 -> mapped to [-1,1]), `vol_rel` (volume / mean
  volume of prior 20 bars), `gap_open` (session's first-bar open minus prior session close, R20, signed).
* day so far: `day_range_rel` (session high-low so far / mean of prior 20 sessions' full ranges), `day_ret` (close -
  session open, R20, signed).
* time: `tod_<bucket>` one-hot (Asia 18-2, Europe 2-8, US pre 8-9:30, Open 9:30-10:30, Midday 10:30-15, Close 15-16:45),
  `dow_<0..4>`.
* higher timeframe (60-min, only fully closed bars): `h1_ema_stack`, `h1_mom`, `h1_struct_5`.
* cross-market (each other market, same-start bar): `x_<SYM>_ret` (bar return in that market's R20 units, signed),
  `x_<SYM>_ema_stack`.
Test (test_features.py): PERTURBATION test - compute F on real data slices; change every bar after bar t (and in the
other markets); recompute; F rows <= t must be identical. Plus hand-made checks for a few columns.

## Module 2: labels.py
`entry_events(b, P) -> DataFrame` one row per (signal bar t, direction d) where at least one directional pattern of
direction d fires (textbook direction); columns t, d, patterns (list), n_patterns, stop reference = most extreme
L (long) / H (short) over the max SPAN of the patterns that fired, minus/plus 1 tick. Also `random_events(b, frac,
seed)`: random bars (allowed ones), random direction, stop = the signal bar's own low/high -/+ 1 tick.
`label_entries(sym, tf, b, events, target_R=(1.0, 1.5, 2.0), max_bars=16) -> DataFrame`:
* entry = open of bar t+1; risk = |entry - stop| (if entry is already past the stop: exit at the entry open,
  label as a loss of the costs); target = entry + d * target_R * risk; time limit = close of bar t+max_bars or the
  16:45 forced-exit bar (exits.session_frame), whichever first.
* the path is walked on 1-MINUTE bars (research_lib.bars_1m) between the entry and the time limit: stop hit if a 1-min
  low <= stop (long), filled at min(open, stop) of that minute then minus 1 extra tick; target hit if a 1-min high
  >= target + 1 tick, filled at target; if one minute touches both -> STOP first.
* outputs per target_R: `pnl_usd_<R>`, `y_<R>` (pnl > 0), `exit_kind_<R>` (stop/target/time), `t_end_<R>` (timestamp
  of the exit, for purging). Primary label: y_1.5. Also `risk_pts`, `risk_usd`.
`exit_rows(sym, tf, b, F, events, max_bars=32, frac=0.25, seed) -> DataFrame`: for a random `frac` of entry events
PLUS random events, manage each trade with the baseline (stop at the stop reference, no target, time limit max_bars or
16:45). For every tf-bar k the trade is open at its close (k >= entry bar), one row: trade id, k, d, F row k, trade
state (`open_R` = (close_k - entry)*d/risk, `mfe_R`, `mae_R` so far, `bars_held`, `dist_stop_R`, `mins_to_1645`),
and the label: `exit_gain_usd` = $ from exiting at the open of bar k+1 minus $ from holding to the baseline end
(same costs both ways; the stop's extra slippage counts if the baseline ends at the stop), `y_exit` =
exit_gain_usd > 0, `t_end` (baseline end timestamp). Rows after the stop/time end are not created.
Test (test_labels.py): hand-made 1-min paths for stop, target, same-minute tie, gap through stop, time exit, 16:45
cutoff, entry past stop, short mirror, exit-row labels.

## Module 3: walkforward.py
* Folds: expanding window by calendar year. Test years 2013 ... 2024 and 2025H1 (2025-01-01 to 2025-06-30). LOCKED
  HOLDOUT 2025-07-01 onward: the code must refuse to evaluate on it unless `final=True` is passed.
* Purge: drop training events whose label end (t_end) is after (test start - 1 day); embargo 1 session after the test
  window for later folds (not needed with expanding windows but keep the function general).
* Sample weights: (a) uniqueness = 1 / number of events (same market) whose [entry, t_end] windows overlap this one,
  averaged over the window (approximate with counts is ok); (b) cross-market: divide by the number of markets with an
  event on the same timestamp and direction. Exit rows: each trade's rows share weight 1.
* Direction handling: multiply every signed feature by d (list of signed columns given by features.py `SIGNED`).
* Models: `vote` = equal-weight family vote (sum of d*fam_* plus d*ema_stack plus d*struct_5 plus d*brk_5 ...) as
  the baseline score; `logit` = StandardScaler + L2 LogisticRegression, C chosen by an inner time-split (last 2
  training years) on log loss, shrunk toward the vote via a prior offset is optional; `gbm` =
  HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter<=300, l2_regularization=1,
  min_samples_leaf=500) + isotonic calibration fitted on the last training year.
* Decision: entries - take when p >= threshold; the threshold is chosen on the TRAINING period's inner out-of-sample
  predictions to maximise mean net $ per trade subject to at least 5% of events kept. Exits - exit when p >= threshold
  (same selection).
* Metrics per fold and pooled: AUC, Brier, log loss, calibration table (10 bins), trades kept, net $ per trade, total
  $, hit rate, $/year. Baselines at the SAME number of trades: all events, vote top-N, random skip (mean and 5-95%
  over 200 draws), pattern-only (single best pattern in training).
* Permutation test: shuffle y within each training year, refit, record OOS $ (20 shuffles).
* Weight table: logit coefficients per fold (standardized and raw), sign stability across folds, and a SCORECARD:
  points = round(coef / (ln 2 / 20)) per unit (credit-scorecard scaling: +20 points doubles the odds), shown in plain
  words with units (R20 -> "average bars").
* Exit evaluation: on test trades, simulate the learned exit (exit at the first bar with p >= thr) vs baseline hold,
  vs "exit on any opposite classic pattern", vs random exit times with the same distribution; net $ per trade.
Test (test_walkforward.py): synthetic data with a planted signal (model must find it, sign right) and a pure-noise
set (no edge OOS); purge correctness; holdout refusal; weights.

## Module 4: run_pipeline.py (integration)
For ES, NQ, YM at 15-min: features -> entry events + labels -> exit rows -> walk-forward (entries and exits) ->
`out/` parquet datasets, `out/entry_results.csv`, `out/exit_results.csv`, `out/weights_*.csv`, `REPORT.md` with: the
scorecard tables, fold-by-fold $ vs baselines, calibration, permutation test, stability, and daily-$ series of the
chosen entry model run through prop_sim.simulate (LucidFlex 25K defaults) with a DAY-BLOCK view (pass odds) next to
the all-events baseline. Never touch the 2025-07+ holdout.
Log every configuration tried to `out/trials.csv` (date, module, parameters, OOS result) for the data-snooping count.
