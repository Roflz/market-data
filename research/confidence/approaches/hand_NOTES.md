# Hand-set weights (family `hand`): notes

Module: `approach_hand.py`. Tests: `test_approach_hand.py`. Data files: `bulkowski_weights.csv` (generated from
the table in the module) and `user_weights.csv` (a blank template for your own weights).

The weights are fixed and come from published practitioner sources. `fit()` learns only a Platt calibration,
P(y=1) = sigmoid(a·score + b), and it uses only the training rows it is given. The calibration is stored only as the
floats `platt_a_` and `platt_b_` (no closure), so a `copy.deepcopy` of a fitted scorer is unaffected when the original
is refit on another fold, and fitted scorers can be pickled (joblib, saved models).

The slope `a` is kept at or above 0. If the training years contradict the published direction, the scorer goes
flat at the training base rate (`platt_clipped_ = True`) instead of quietly reversing the source's weights. To allow
a negative slope, pass `allow_negative_slope=True`.

Every scorer runs with `task="entry"` and with `task="exit"`. On an exit row, a high score means evidence against
the open trade.

Run:
```
cd research/confidence/approaches
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../../pylib:../../..:../../signals:..:. python3 test_approach_hand.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../../pylib:../../..:../../signals:..:. python3 approach_hand.py --write-csv   # regenerate bulkowski_weights.csv
```

| scorer | score | source |
|---|---|---|
| `hand_bulkowski` | sum of log-odds of patterns firing with the trade, minus those firing against it (exit: the negative) | Bulkowski, thepatternsite.com candle pages (*Encyclopedia of Candlestick Charts*) |
| `hand_morris_woe` | Weight of the Evidence 0-100 = sum of the weights of the components that are "on" (exit: 100 - WoE); `bands(X)` | Greg Morris, StockCharts 2018 series |
| `hand_ndr_composite` | % of indicators agreeing with the trade (exit: 100 - %); `zones(X)` | Ned Davis Research, U.S. Stock Market Model cut-offs (70 / 55) |
| `hand_user` | sum of weight × feature from `user_weights.csv` | you |

All sources were read on 2026-11-08.

---

## 1. `hand_bulkowski`

**What Bulkowski publishes.** Each candle page has an "Important Results" table with four lines:
- Theoretical performance.
- Tested performance, for example "Bullish reversal 63% of the time". BullEngulfing.html defines this as "price closes above the top of the candlestick pattern 63% of the time".
- Frequency rank.
- Overall performance rank. Ranks are out of 103, and 1 is best. [glossary](https://www.thepatternsite.com/glossary.html): "a ranked sum of the percentage price changes from 1, 3, 5 and 10 trading days after the breakout".

Reversal and continuation are measured against the trend that led into the pattern, not against the candle's colour.

The data is daily US stocks with no costs. The pages say "hundreds of perfect trades" and give no sample period.

**Weight.** p = his measured share of breakouts in our textbook direction, and w = ln(p / (1 - p)).
- If his pattern requires a prior trend and he found it reverses, p is his tested rate (basis `published`).
- If he found it continues instead, p = 1 - his rate (basis `complement`). For example, the hanging man shows "Bullish continuation 59%", so it moves in its textbook bearish direction 41% of the time, and its weight is negative.
- If his pattern has no trend requirement ("Price trend leading to the pattern: None required"), his reversal or continuation rate says nothing about direction. Only an explicit breakout-direction share is used (basis `derived`). Otherwise the weight is 0 (basis `not_published`). This applies to the dragonfly and the gravestone doji alike.
- For the inside-bar and NR7 breakouts, p is the pooled win rate of his chart-pattern trade test (basis `published_trade`, see below).
- Patterns with no Bulkowski number that maps to our rule get weight 0 (basis `no_equivalent`).

| our pattern | side | Bulkowski page | his line | p (textbook dir.) | basis | w (log-odds) | overall rank /103 |
|---|---|---|---|---|---|---|---|
| dragonfly_doji | bull | [Dragonfly](https://www.thepatternsite.com/Dragonfly.html) | Reversal 50% (no trend req.; only "upward breakouts predominate") | - | not_published | 0 | 98 |
| gravestone_doji | bear | [Gravestone](https://www.thepatternsite.com/Gravestone.html) | Bearish reversal 51% (trend "None required"; only "should breakout downward most often, which it does") | - | not_published | 0 | 77 |
| hammer | bull | [Hammer](https://www.thepatternsite.com/Hammer.html) | Bullish reversal 60% | 0.60 | published | +0.405 | 65 |
| hanging_man | bear | [HangingMan](https://www.thepatternsite.com/HangingMan.html) | Bullish continuation 59% | 0.41 | complement | -0.364 | 87 |
| inverted_hammer | bull | [HammerInv](https://www.thepatternsite.com/HammerInv.html) | Bearish continuation 65% | 0.35 | complement | -0.619 | 6 |
| shooting_star | bear | [ShootingStar](https://www.thepatternsite.com/ShootingStar.html) (1 line) | Bearish reversal 59% | 0.59 | published | +0.364 | 55 |
| marubozu | bull | [WhiteMarubozu](https://www.thepatternsite.com/WhiteMarubozu.html) | Continuation 56% (vs trend; no direction share) | - | not_published | 0 | 71 |
| marubozu | bear | [BlackMarubozu](https://www.thepatternsite.com/BlackMarubozu.html) | "upward breakouts occur 34% of the time in the 19,993 black marubozu candles" | 0.66 | derived | +0.663 | 57 |
| engulfing | bull | [BullEngulfing](https://www.thepatternsite.com/BullEngulfing.html) | Bullish reversal 63% | 0.63 | published | +0.532 | 84 (intro says 22) |
| engulfing | bear | [BearEngulfing](https://www.thepatternsite.com/BearEngulfing.html) | Bearish reversal 79% | 0.79 | published | +1.325 | 91 |
| harami | bull | [HaramiBull](https://www.thepatternsite.com/HaramiBull.html) | Bullish reversal 53% | 0.53 | published | +0.120 | 38 |
| harami | bear | [HaramiBear](https://www.thepatternsite.com/HaramiBear.html) | Bullish continuation 53% | 0.47 | complement | -0.120 | 72 |
| piercing | bull | [Piercing](https://www.thepatternsite.com/Piercing.html) | Bullish reversal 64% | 0.64 | published | +0.575 | 13 (intro says 21) |
| dark_cloud | bear | [DarkCloudCover](https://www.thepatternsite.com/DarkCloudCover.html) | Bearish reversal 60% | 0.60 | published | +0.405 | 22 |
| morning_evening_star | bull | [MorningStar](https://www.thepatternsite.com/MorningStar.html) | Bullish reversal 78% | 0.78 | published | +1.266 | 12 |
| morning_evening_star | bear | [EveningStar](https://www.thepatternsite.com/EveningStar.html) | Bearish reversal 72% | 0.72 | published | +0.944 | 4 |
| three_soldiers_crows | bull | [ThreeWhiteSoldiers](https://www.thepatternsite.com/ThreeWhiteSoldiers.html) | Bullish reversal 82% | 0.82 | published | +1.516 | 32 |
| three_soldiers_crows | bear | [ThreeBlackCrows](https://www.thepatternsite.com/ThreeBlackCrows.html) | Bearish reversal 78% | 0.78 | published | +1.266 | 3 |
| three_inside | bull | [ThreeInsideUp](https://www.thepatternsite.com/ThreeInsideUp.html) | Bullish reversal 65% | 0.65 | published | +0.619 | 20 |
| three_inside | bear | [ThreeInsideDown](https://www.thepatternsite.com/ThreeInsideDown.html) | Bearish reversal 60% | 0.60 | published | +0.405 | 56 |
| pin_bar | bull | Hammer + HangingMan | 60% up (downtrend), 59% up (uptrend) | 0.595 | derived (mean) | +0.385 | - |
| pin_bar | bear | ShootingStar + HammerInv | 59% down (uptrend), 65% down (downtrend) | 0.62 | derived (mean) | +0.490 | - |
| tweezer | bull | [TweezersBottom](https://www.thepatternsite.com/TweezersBottom.html) | Bearish continuation 52% | 0.48 | complement | -0.080 | 44 |
| tweezer | bear | [TweezersTop](https://www.thepatternsite.com/TweezersTop.html) | Bullish continuation 56% | 0.44 | complement | -0.241 | 81 |
| tall_trend_bar | bull / bear | [LongWhiteDay](https://www.thepatternsite.com/LongWhiteDay.html), [LongBlack](https://www.thepatternsite.com/LongBlack.html) | Continuation 58% / 53% (vs trend; no direction share) | - | not_published | 0 | 53 / 19 |
| inside_bar_breakout | bull | [InsideDays](https://www.thepatternsite.com/InsideDays.html) Table 7 | up breakouts: bull mkt 57% (7,082 W / 5,375 L), bear mkt 46% (1,315 / 1,514) | 0.549 | published_trade | +0.198 | - |
| inside_bar_breakout | bear | InsideDays Table 7 | down breakouts: bull mkt 43% (4,837 / 6,349), bear mkt 54% (1,665 / 1,445) | 0.455 | published_trade | -0.181 | - |
| nr7_breakout | bull | [nr7](https://www.thepatternsite.com/nr7.html) Table 3 | up breakouts: bull mkt 57% (7,600 / 5,791), bear mkt 45% (920 / 1,112) | 0.552 | published_trade | +0.210 | - |
| nr7_breakout | bear | nr7 Table 3 | down breakouts: bull mkt 45% (4,990 / 6,218), bear mkt 47% (166 / 186) | 0.446 | published_trade | -0.217 | - |
| outside_bar | both | [OutsideDays](https://www.thepatternsite.com/OutsideDays.html) Tables 7/8 | trade tests exist (7%/7%: 58/43/45/53%; pattern stop: 47/36/44/52%) but enter after a later close beyond the range | - | no_equivalent | 0 | - |
| clv_extreme, bar_80_20, clv5_extreme, five_lower_lows_higher_highs | both | none | - | - | no_equivalent | 0 | - |

**Inside-bar and NR7 breakouts (basis `published_trade`).** Both pages publish a breakout trade test that uses our
entry convention: wait for a close beyond the pattern, then buy or short at the next open, with a 7% target and a 7%
stop. nr7.html: "Wait for price to close above the top or below the bottom of the pattern." / "Buy/short at the open
the next day." InsideDays.html: "If price closes above the pattern's high, buy at the open the next day", where the
pattern's high or low is "the first day's high or low", i.e. the mother bar, as in our rule. Our breakouts must
happen within 3 bars of the pattern (`signals.py`); his setups state no window. Wins are pooled by trade count over
bull and bear markets for each breakout side; the counts are in `BULKOWSKI_TRADE_TESTS` in the module.
Caveats:
- These numbers measure "+7% before -7%" on daily stocks, not a candle breakout share. The sample is mostly bull market, which is why shorts (down breakouts) win less than half the time.
- By default the 7%/7% tables are used, not the "with Pattern Stop" tables (inside day pooled 47.2% up / 41.5% down; outside day 46.5% / 39.9%), even though our labels also stop at the pattern extreme. With a symmetric target and stop, 50% means no edge, the same zero point as the candle direction rates. With a tight pattern stop and a 7% target, a coin flip already wins less than half the time (Bulkowski's own inside-day bull/up row wins 47% yet nets +$55.28 a trade), so those win rates are not direction rates. Concretely, both inside-day sides would get negative log-odds (-0.111 and -0.342), and the default symmetric weight would be -0.227: an inside-bar breakout *against* the trade would score higher than one *with* it, a sign that comes from the payoff, not from direction. The variant is available as `hand_bulkowski(breakout_table="pattern_stop")` (NR7 has no pattern-stop table and keeps Table 3), and the pattern-stop counts are kept in `BULKOWSKI_TRADE_TESTS`.
- nr7.html: the setup's first bullet reads "Find a NR7 downtrend" without explanation, and the table header cites 29,021 trades while its win and loss counts sum to 26,983. Both are recorded as published.
- Outside day: the same tables exist, but that trade enters only after a later close beyond the outside day's range, in either direction. Our `outside_bar` fires on the outside bar itself, with its direction taken from its own close vs open, and the page reports nothing by close position or colour. No number maps to our rule, so the weight stays 0.

The default (`directional=False`) gives each two-sided pattern the mean log-odds of its two sides, and a side with
no published rate counts as 0 (no evidence). For example, engulfing gets (0.532 + 1.325) / 2 = 0.929, and the
harami's two sides cancel to exactly 0. The marubozu gets (0 + 0.663) / 2 = 0.332: the black marubozu's derived 66%
is not mirrored onto the white marubozu. The inside-bar and NR7 breakouts nearly cancel (+0.008 and -0.003), so in
the default mode they carry almost no weight; `directional=True` keeps the long/short asymmetry.

The reason is that `score(X)` only sees oriented X and cannot tell a bullish engulfing on a long from a bearish one on
a short. `directional=True` uses the weight for each side: `fit()` reads `meta["d"]`, and `score` and
`predict_proba` then need `d=...`.

The overall rank is recorded in the CSV, but it is not used. The task defines the weight from the rate, and the rank
measures move size after a breakout in either direction. That is why the inverted hammer ranks 6 even though it goes
the wrong way 65% of the time.

**Exit version.** score_exit = -score_entry. A pattern firing against the open trade raises the exit score by its
log-odds, and one firing with the trade lowers it.

The Brooks idea that structure breaks outweigh single candles is available as `structure_weight=<float>`, which adds
that much per fresh swing break against the trade (`brk_5`, `brk_10` = -1). It is off by default because no number is
published. The Brooks page cited in CONFIDENCE_RESEARCH.md
([forum thread](https://www.brookstradingcourse.com/support-forum/09-pullbacks-and-bar-counting/confused-about-consecutive-bottom-attempts-in-a-bear-trend/))
contains only member posts and does not state the rule. The "Ask Al" page ([?p=57617](https://www.brookstradingcourse.com/?p=57617))
gives the 60% / 40% rules of thumb but says nothing about exits.

## 2. `hand_morris_woe`

**What Morris published** (Greg Morris, StockCharts "Dancing with the Trend"):

| article | what it gives |
|---|---|
| [part 4](https://articles.stockcharts.com/article/articles-dancing-2018-02-building-a-rules-based-trend-following-model---4/) 2018-02-03 | 9 indicators; "Each indicator carries a different weight based upon its individual performance"; all on = 100; "price-based indicators should dominate the array" |
| [part 6](https://articles.stockcharts.com/article/articles-dancing-2018-03-building-a-rules-based-trend-following-model---6/) 2018-03-12 | Price Short (10-21 days), hedged: "Many times, a short-term measure is not actually used in the weight of the evidence calculation but serves a weight of the evidence model well with a warning of things to come"; Price Medium 2-4 weeks; Price Long 4-8 weeks; MACD from "the 19 and 39-day" EMAs; binary on above the line |
| [part 8](https://articles.stockcharts.com/article/articles-dancing-2018-04-building-a-rules-based-trend-following-model---8/) 2018-04-13 | Adaptive Trend, "Another price-based measure I use in my weight of the evidence": EMAs of the midpoint and of the true range, ± half the range EMA, ± X standard deviations; on when the close is above the line. ATR period, smoothing and X are **not published** |
| [part 9](https://articles.stockcharts.com/article/articles-dancing-2018-05-building-a-rules-based-trend-following-model---9/) 2018-05-10 | breadth Combo (advances, declines, up/down volume, MACD-like 19/39, on above zero) |
| [part 12](https://articles.stockcharts.com/article/articles-dancing-2018-07-building-a-rules-based-trend-following-model---12) 2018-07-16 | component list (includes Price Short and Adaptive Trend); bands 0-30 Red, 31-50 Orange, 51-80 Yellow, 81-100 Green; "the middle two considered as transition ranges", which absorb volatility |
| [part 13](https://articles.stockcharts.com/article/articles-dancing-2018-07-building-a-rules-based-trend-following-model---13) 2018-07-23 | buys allowed in every band, with a per-instrument hurdle that depends on the band ("Red: Trend > 60, Orange: Trend > 55, Yellow/Green: Trend > 50"); trading up "fairly active" in Green, "limited considerably" in Yellow; sells are stops; **no band-based sell rule** |
| ["Weight of the Evidence"](https://articles.stockcharts.com/article/articles-dancing-2018-08-weight-of-the-evidence) 2018-08-07 | "I cannot divulge the exact details of my Weight of the Evidence" → **the weights are not public** |

**What was used.** Morris states no horizon grouping, and part 4 says each indicator's weight depends on "its
individual performance as a trend measure". Neither the weights nor that performance measure are published, so the
weighting below is **our fallback**, not his structure:
- Price Short is off by default. This is our reading of the hedged part 6 sentence; part 12 lists Price Short among his components, so `include_short=True` (adding it back as a 4th block) is just as defensible.
- The remaining horizons get equal weight: medium, long and breadth are 33.3 each.
- Within a horizon, the weight is split equally across its components.
- Price is 66.7 against 33.3 for breadth, which is in line with part 4's "price-based indicators should dominate the array".
- **Adaptive Trend is omitted.** Its parameters are not published and it is a stateful line with no SPEC feature, so any analog would need invented numbers. `weights_table()` lists it as a 0-weight `(adaptive_trend)` row.
- Weighting each component by its own training-row trend performance (his stated principle) is not offered: it would make this family learned, and his performance metric is not published.

Each component is "on" when its value, oriented with the trade, is above 0.

| horizon | our component | Morris counterpart | weight |
|---|---|---|---|
| short (off) | mom > 0, close > EMA8 | Price Short | 0 |
| medium | EMA8 > EMA20 (`dist_ema20 - dist_ema8`), `ema_stack`, `struct_5` | Price Medium, Trend Capturing with Price | 11.1 each |
| long | EMA20 > EMA50 (`dist_ema50 - dist_ema20`, his 19/39 MACD), close > EMA50, `h1_ema_stack`, `h1_struct_5` | Price Long | 8.33 each |
| breadth | `x_<SYM>_ret`, `x_<SYM>_ema_stack` of the other markets | A/D, new highs/lows, up/down volume, Combo | 8.33 each (2 markets) |

The horizons are kept as bar counts. His 2-4 weeks is about 10-20 daily bars, which here becomes EMA8/EMA20 on 15-min
bars. His breadth comes from Nasdaq internals, which we don't have, so it becomes agreement from the other index
futures.

A component that is NaN is dropped, and the rest of its horizon is re-normalised. A horizon with nothing available
drops out. A row with no information at all scores 50.

**Bands and exits.** `bands(X)` returns these columns:
- `woe`
- `band_red`, `band_orange`, `band_yellow`, `band_green`, `band` (Morris part 12)
- `buy_hurdle`: Morris's part 13 per-instrument hurdle for that band (60 Red, 55 Orange, 50 Yellow/Green). We have no separate per-instrument Trend score, so `score()` does not apply it; the harness can require a higher candidate score (for example a 0-100 `hand_ndr_composite` level) or a higher calibrated p in weaker bands.
- `entry_zone` (WoE > 50) and `exit_zone` (WoE ≤ 30): **our adaptations, not Morris rules.** Morris allows buying in every band and publishes no band-based sell rule (part 13 sells are stops).

The exit score is 100 - WoE. `score()` is stateless (one row at a time), so the transition-zone hysteresis exists
only as the informational zone columns. A harness that exits at the first bar whose p clears its threshold exits on
the first downward crossing of that threshold, which is not tied to 30.

`score_mode="band"` makes the score the band index (0-3) instead of the level.

## 3. `hand_ndr_composite`

**Source, verified.** Ned Davis Research Group, "Volatility Returns - What's Next?" (Amy Lubas, CFA, webinar deck,
2018-05-10), printed p. 11 (PDF p. 14), chart S75A ([PDF](https://cdn2.hubspot.net/hubfs/1818132/EVP_ADVP201805101.pdf)).
The model is the "U.S. Stock Market Model Composite (Monthly, 50% Internal, 50% External)". Its full-history table,
1979-11-30 to 2018-04-30:

| composite | S&P 500 gain per year | % of time |
|---|---|---|
| Above 70.0 | +18.61% | 42.66% |
| 55.0-70.0 | +10.09% | 39.60% |
| Below 55.0 | -14.20% | 17.75% |

Buy and hold over the same period gained 8.73% per year.

Only the 70 / 55 cut-offs are NDR's. The deck does not name the zones: the word BULLISH on that page stands beside
the 2008-2018 Chart View table and matches the current reading (80.00 on 2018-04-30), so it is not a zone label. The
names "bullish / neutral / bearish" in `zones(X)` are ours. The deck does not say how many indicators the model uses.
Its readings (66.7 composite, 58.3 internal, in the table on printed p. 6) look like shares of a small number of
indicators per half, but that is our inference.

**Correction to CONFIDENCE_RESEARCH.md.** It says Morris's 2018-08 "Weight of the Evidence" article cites these
thresholds. It does not: there is no mention of Ned Davis there, in parts 2-3, or in parts 12-13. The numbers above
come from NDR's own deck.

**Our composite.** It is 100 × agreeing / voting.
- **State indicators always vote**, and agree when > 0: `dist_ema8/20/50`, `ema_stack`, `ema20_slope`, `above_ema20_share`, `mom`, `mom_slope3`, `dist_vwap`, `day_ret`, `struct_5/10`, `h1_ema_stack`, `h1_mom`, `h1_struct_5`, and the other markets' `x_*_ret` and `x_*_ema_stack`.
- **Event indicators vote only when they fire**: the `fam_*` families, `brk_5/10` and `mom_x100`. Families are used instead of the 24 single patterns so that overlapping candles are not counted many times. `include_events=False` drops them.

`zones(X)` returns `zone_bullish` (> 70), `zone_neutral` (55-70), `zone_bearish` (< 55), `entry_zone` (> 70) and
`exit_zone` (< 55); the cut-offs are NDR's, the names ours. The exit score is 100 - composite.

## 4. `hand_user`: how to fill `user_weights.csv`

The template lists every feature the harness can pass, plus the six exit trade-state columns (`open_R`, `mfe_R`,
`mae_R`, `bars_held`, `dist_stop_R`, `mins_to_1645`). The columns are `signal`, `entry_weight`, `exit_weight` and
`note`. To fill it in:

1. Put a number in `entry_weight` for each signal you want to count in entries, and in `exit_weight` for exits. Leave the rest blank; blank means 0.
2. Features are oriented: **+ means with the trade**.
   - A pattern value is +1 when it fires with the trade and -1 when it fires against it.
   - A positive entry weight on `pat_engulfing` therefore rewards engulfing with the trade and penalises engulfing against it.
   - For exits, high means exit, so a positive exit weight on `brk_5` would make a with-trade break push toward exiting. You probably want negative exit weights on with-trade evidence and positive ones on state such as `mae_R`.
3. Units are log-odds per unit of the feature, so 0.69 doubles the odds; scorecard points are weight / 0.0347. Only the signs and relative sizes matter, because Platt rescales on training rows. Continuous features (distances in average bars, `mom`) need smaller weights than 0/±1 flags.
4. Keep the file name and columns. A file with all weights blank makes `fit()` raise `HandWeightsMissing`, a subclass of sklearn's `NotFittedError` with `.skip = True`, so the harness can skip it. A non-numeric entry raises `ValueError`. Regenerating the template never overwrites a filled file unless you pass `--write-templates --force`.
5. Signal names are checked in `fit()`, so a typo never drops a weight silently. A weighted name that is neither a column of X nor a SPEC column raises `ValueError`. A SPEC column that is absent from this X (for example an exit-state column given an entry weight) gives a warning and is ignored. If none of the weighted signals is in X, `fit()` raises `HandWeightsMissing`.

## Deviations from the sources, and why

1. **Daily stocks to 15-min futures**, for every source. The published numbers are taken as priors on direction. Platt on the training years sets the scale and the base rate for our y (net $ > 0 after costs with stop and target), which none of these sources measured.
2. **Bulkowski, bull and bear weights averaged** by default, because `score(X)` gets no direction. A side with no published rate counts as 0 in that mean, so no published number is mirrored onto the other side (marubozu 0.332, not 0.663). Use `directional=True` for side-specific weights.
3. **Bulkowski, missing direction shares get weight 0.** This covers the white marubozu, the long days, and the dragonfly and gravestone doji (neither requires a prior trend). We do not mirror the other side and do not use the continuation or reversal rate as a proxy.
4. **Bulkowski, pin bar weight is derived**: the unweighted mean of the two trend contexts of the same shape. It is labelled `derived` in the CSV.
5. **Bulkowski, trend filters differ.** Our three soldiers/crows and marubozu rules have no prior-trend filter, while his do (or his stats are measured in a trend).
6. **Bulkowski, inside-bar and NR7 breakouts use chart-pattern trade tests** (basis `published_trade`): pooled win rates of his 7% target / 7% stop tests on daily stocks, a "+7% before -7%" rate rather than a candle breakout share. The pattern-stop tables are not the default because their asymmetric payoff makes the win rate not a direction rate (it would flip the sign of the default symmetric weight); `breakout_table="pattern_stop"` uses the inside-day one on request. Our breakouts must happen within 3 bars of the pattern; his setup states no window.
7. **Bulkowski, outside bar stays 0.** His outside-day trade test enters after a later close beyond the range; our signal fires on the outside bar itself with direction from its own close.
8. **Morris, weights are secret, and our weighting is a fallback.** Equal weight per horizon, an equal split inside a horizon, and Price Short off by default are our choices, not his structure. Adaptive Trend is omitted because its parameters are unpublished. Component indicators are replaced by our nearest features, and breadth is replaced by the other index futures.
9. **Morris, entry and exit zones are ours.** `entry_zone` (> 50) and `exit_zone` (≤ 30) are our adaptations. His published band rule is a stricter per-instrument buy hurdle in weaker bands (`buy_hurdle`, exposed but not applied in `score()`), and he publishes stops only for sells. The score is stateless, so hysteresis is not enforced.
10. **NDR, composite differs.** NDR's composite is monthly and proprietary (internal and external halves; the deck gives no indicator count). Ours is a percent-agree vote over our own indicators, with events voting only when they fire. Only the 70 / 55 cut-offs are NDR's; the zone names are ours.
11. **Platt slope is clipped at ≥ 0.** This keeps the family hand-set; see the top of this note.
12. **Exit trade-state columns are not used** by scorers 1-3, because no source publishes a hand weight for them. `hand_user` can weight them.

## Review fixes (2026-11-08)

- Calibration is no longer a closure (deepcopy and pickle safe; regression test `test_calibration_survives_deepcopy_refit_and_pickle`).
- Inside-bar and NR7 breakouts now carry Bulkowski's published trade-test rates (`test_breakout_trade_tests_used`). The review preferred the inside day's pattern-stop table; the default keeps the 7%/7% table for the reason given in section 1, and the pattern-stop table is an option (`breakout_table="pattern_stop"`). All counts were re-checked against InsideDays.html, nr7.html and OutsideDays.html.
- The symmetric marubozu weight no longer inherits the black side's 66% (`test_marubozu_symmetric_not_mirrored`).
- The gravestone doji follows the same rule as the dragonfly (weight 0).
- NDR citation corrected to printed p. 11 (PDF p. 14); "labelled BULLISH" and "100+ indicators" removed.
- Morris: full part 6 quote, Price Short exclusion and equal per-horizon weights labelled as our fallback, Adaptive Trend listed as omitted, part 13 hurdle exposed as `buy_hurdle`, entry/exit zones labelled as adaptations.
- `hand_user` checks signal names (`test_user_signal_names_checked`).

## Test output (2026-11-08)

```
PASS test_bulkowski_table_and_csv
PASS test_planted_signal_ranked_higher  {('hand_bulkowski', 'entry'): 0.729, ('hand_bulkowski', 'exit'): 0.717, ('hand_morris_woe', 'entry'): 0.669, ('hand_morris_woe', 'exit'): 0.682, ('hand_ndr_composite', 'entry'): 0.642, ('hand_ndr_composite', 'exit'): 0.634, ('hand_user', 'entry'): 0.736, ('hand_user', 'exit'): 0.736}
PASS test_noise_stays_near_half  {('hand_bulkowski', 'entry'): 0.497, ('hand_bulkowski', 'exit'): 0.5, ('hand_morris_woe', 'entry'): 0.5, ('hand_morris_woe', 'exit'): 0.507, ('hand_ndr_composite', 'entry'): 0.496, ('hand_ndr_composite', 'exit'): 0.5, ('hand_user', 'entry'): 0.5, ('hand_user', 'exit'): 0.5}
PASS test_weights_tables
PASS test_bulkowski_directional_and_exit_sign
PASS test_morris_levels_and_bands
PASS test_ndr_composite_and_zones
PASS test_user_template_and_blank_skip
PASS test_calibration_survives_deepcopy_refit_and_pickle
PASS test_breakout_trade_tests_used
PASS test_marubozu_symmetric_not_mirrored
PASS test_gravestone_same_rule_as_dragonfly
PASS test_user_signal_names_checked
PASS test_morris_published_hurdle_and_labels
PASS test_rowwise_no_lookahead
PASS test_calibration_never_reverses_published_sign
PASS test_unfitted_raises_and_speed  {'hand_bulkowski': 0.295, 'hand_morris_woe': 0.499, 'hand_ndr_composite': 0.573}
ALL PASSED in 5.7s
```

The AUCs are out of sample: fit on the first half of 20,000 synthetic rows, scored on the second half. The speed
test is fit plus predict on 200,000 rows × 80 columns. All three scorers are vectorised with no subsampling, so 1M
rows takes a few seconds.

## Smoke run on real data

This run used real ES 15-min features from 2019 onward (385k bars in the full frame) and scored every bar as if it
were a long or a short. It is not an evaluation. All scorers ran without NaN in 7.6 s, including building the
features.

- **Morris, bar shares by band (long orientation):** red 39%, orange 15%, yellow 26%, green 20%.
- **NDR, bar shares by zone (long orientation):** bullish 26%, neutral 19%, bearish 55%.

The NDR zones put most bars in "bearish" for our composite. Ternary indicators at 0 (for example `ema_stack`,
`struct_k`) count as not agreeing, and intraday futures have no stock-market upward drift. NDR's own composite was
above 70 for 43% of 1979-2018. The thresholds are therefore kept as published, and only Platt maps the level to a
probability.
