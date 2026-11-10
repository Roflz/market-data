"""
HAND-SET confidence weights from published practitioner sources (family "hand").

The weights are FIXED from the sources below; fit() only calibrates score -> probability with Platt scaling
(sigmoid(a * score + b), the same fit as scorer_api.platt) on the TRAINING rows it is given. Nothing else is learned.
The Platt slope a is kept >= 0 (allow_negative_slope=True lifts this): calibration may shrink the hand weights to
nothing (flat = training base rate, platt_clipped_ = True) but never reverses the published direction, so the "hand"
family stays hand-set rather than half-learned. Every scorer works for task="entry" and
task="exit". X arrives oriented by trade direction (+ = with the trade). For exits, a high score = evidence AGAINST the
open trade, so each exit score is the entry evidence turned around (see each class).

Registered scorers
------------------
hand_bulkowski      per-pattern log-odds from Thomas Bulkowski's measured candle behaviour (thepatternsite.com candle
                    pages, which summarise his Encyclopedia of Candlestick Charts, Wiley 2008), plus his inside-day and
                    NR7 breakout TRADE tests for inside_bar_breakout / nr7_breakout (basis published_trade).
                    weight_p = ln(p / (1 - p)), p = his measured rate of price moving in OUR textbook direction (his
                    "tested performance" line, or its complement when he found the opposite behaviour).
                    score = sum of weights of patterns firing with the trade - sum of those firing against it.
                    Every number, URL and the mapping per pattern is in BULKOWSKI (below) and bulkowski_weights.csv.
hand_morris_woe     Greg Morris's "Weight of the Evidence" (StockCharts "Dancing with the Trend", 2018 series
                    "Building a Rules-Based Trend Following Model" parts 4-13 and "Weight of the Evidence" 1-3):
                    binary trend components, fixed weights summing to 100, score 0-100 read in bands 0-30 red,
                    31-50 orange, 51-80 yellow, 81-100 green (middle two = transition zones).
hand_ndr_composite  Ned Davis Research style composite: percent of indicators that agree with the trade, read with the
                    cut-offs of NDR's U.S. Stock Market Model: above 70, 55-70, below 55 (zone names are ours).
hand_user           the user's own weights from user_weights.csv (columns signal, entry_weight, exit_weight, note).
                    Blank weights -> fit() raises HandWeightsMissing (a sklearn NotFittedError) so a harness can skip.
                    A weighted signal that is not a SPEC column (typo) -> ValueError; a SPEC column absent from this X
                    -> warning; no weighted signal present in X at all -> HandWeightsMissing.

Sources and exactly what was taken from each (all pages read 2026-11-08)
-----------------------------------------------------------------------
Bulkowski, thepatternsite.com. Each candle page has an "Important Results" table with "Theoretical performance",
  "Tested performance" (e.g. BullEngulfing.html: "Bullish reversal 63% of the time", defined on that page as "price
  closes above the top of the candlestick pattern 63% of the time"), "Frequency rank" and "Overall performance rank"
  ("All ranks are out of 103 candlestick patterns with the top performer ranking 1"). Glossary
  (thepatternsite.com/glossary.html): overall performance rank = "a ranked sum of the percentage price changes from
  1, 3, 5 and 10 trading days after the breakout" over bull/bear markets and up/down breakouts; reversal / continuation
  = price leaves the pattern opposite to / in the same direction as it entered (i.e. RELATIVE TO THE PRIOR TREND, not
  to the candle colour). Data: daily US stocks, no trading costs ("based on hundreds of perfect trades"); the pages do
  not state the sample period.
  Consequence used below: when his pattern REQUIRES a prior trend (hammer: down; shooting star: up; ...), "reversal"
  = breakout in the textbook direction, so p = the reversal rate, and when he found "continuation" instead
  (hanging man "Bullish continuation 59%") p = 1 - that rate (41% in the textbook bearish direction). When his
  pattern has NO trend requirement ("Price trend leading to the pattern: None required": marubozu, long day,
  dragonfly doji, gravestone doji) the reversal/continuation rate says nothing about direction; only an explicit
  breakout-direction share is usable (black marubozu: "upward breakouts occur 34% of the time in the 19,993 black
  marubozu candles" -> 66% downward). Where no direction share is published the weight is 0 and the row is labelled
  not_published. (Gravestone: "Bearish reversal 51%", but no trend is required and the page gives no breakout share,
  only that price "should breakout downward most often, which it does" -> weight 0, the same rule as the dragonfly.)
Bulkowski chart-pattern TRADE tests (basis published_trade). nr7.html "Table 3: Testing the NR7" ("Wait for price to
  close above the top or below the bottom of the pattern." / "Buy/short at the open the next day.") and InsideDays.html
  "Table 7" ("If price closes above the pattern's high, buy at the open the next day." / "If price closes below the
  pattern's low, short at the open the next day."; the pattern's high/low = "the first day's high or low", i.e. the
  mother bar, as in our rule) use OUR entry convention, with a symmetric 7% target / 7% stop. Wins per (bull/bear
  market, up/down breakout) are pooled by trade count per breakout side (counts in BULKOWSKI_TRADE_TESTS): NR7 up
  8,520 W / 6,903 L = 55.2%, down 5,156 / 6,404 = 44.6%; inside day up 8,397 / 6,889 = 54.9%, down 6,502 / 7,794 =
  45.5%. These measure "+7% before -7%" on daily stocks (sample mostly bull market), not a candle breakout share.
  Why the 7%/7% tables by default and not the inside day's "with Pattern Stop" Table 8 (stop "a penny below the bottom
  of the inside day pattern"; pooled up 47.2%, down 41.5%), although our labels also stop at the pattern extreme: with
  a symmetric target/stop 50% = no edge, the same zero point as the candle direction rates; with a tight pattern stop
  and a 7% target a coin flip already wins < 50% (his bull-market/up row wins 47% yet nets +$55.28 per trade), so both
  sides get NEGATIVE log-odds and the default symmetric weight becomes (-0.111 - 0.342) / 2 = -0.227: a breakout
  AGAINST the trade would then score higher than one WITH it, a sign produced by the payoff, not by direction.
  breakout_table="pattern_stop" builds that variant on request (NR7 has no pattern-stop table and keeps Table 3).
  OutsideDays.html has the same tables, but its trade enters only after a later close beyond the outside day's range
  (breakout price "the second day's high or low"), while our outside_bar fires on the outside bar itself with
  direction from its own close vs open, and the page reports nothing by close position or colour -> outside_bar keeps
  weight 0.
Morris, StockCharts articles (Greg Morris, "Dancing with the Trend"):
  part 4 (2018-02-03): 9 indicators; "Each indicator carries a different weight based upon its individual performance
    as a trend measure"; "when they are all 'on,' the total is 100"; "price-based indicators should dominate the array".
  part 6 (2018-03-12): Price Short = "the price relationship in the 10 to 21-day range"; Price Medium = 2-4 weeks;
    Price Long = 4-8 weeks; "The two exponential averages used to calculate MACD are the 19 and 39-day"; each
    component is a binary that is on above its zero/signal line. On Price Short the article is hedged: "Many times, a
    short-term measure is not actually used in the weight of the evidence calculation but serves a weight of the
    evidence model well with a warning of things to come." (and part 12 lists Price Short among his components).
  part 8 (2018-04-13): Adaptive Trend, "Another price-based measure I use in my weight of the evidence": exponential
    averages of the midpoint and of the true range, +/- half the range average and X standard deviations, on when the
    close is above the line. ATR period, smoothing and X are NOT published. part 9 (2018-05-10): breadth "Combo" from
    Nasdaq advances/declines/up and down volume, MACD-like 19/39, on above zero.
  part 12 (2018-07-16): components = Trend Capturing with Price, Price Short/Medium/Long, Adaptive Trend,
    Advance/Decline, New Highs/New Lows, Up/Down Volume, Breadth Combination, Trend Capturing with Breadth (relative
    strength abandoned); bands 0-30 Red, 31-50 Orange, 51-80 Yellow, 81-100 Green, "the middle two considered as
    transition ranges", which "allows the model to absorb some market volatility without penalizing the process".
  part 13 (2018-07-23): buys are allowed in EVERY band, with a per-instrument hurdle that depends on the band
    ("Red: Trend > 60, Orange: Trend > 55, Yellow/Green: Trend > 50"); trading up "fairly active" in Green, "limited
    considerably" in Yellow. No band-based sell rule is published (sells are stops).
  "Weight of the Evidence" (2018-08-07): "I cannot divulge the exact details of my Weight of the Evidence, as it is
    still used to manage millions of dollars." -> the individual weights are NOT public (part 4: they differ by
    "individual performance as a trend measure"; no grouping by horizon is stated).
NDR: Ned Davis Research Group webinar deck "Volatility Returns - What's Next?" (Amy Lubas, CFA), 2018-05-10, printed
  p. 11 (PDF p. 14), chart S75A, https://cdn2.hubspot.net/hubfs/1818132/EVP_ADVP201805101.pdf : "U.S. Stock Market
  Model Composite (Monthly, 50% Internal, 50% External)"; full-history table 1979-11-30 to 2018-04-30: "Above 70.0"
  (S&P 500 +18.61%/annum, 42.66% of the time), "55.0 - 70.0" (+10.09%, 39.60%), "Below 55.0" (-14.20%, 17.75%);
  buy/hold 8.73%. Only the 70 / 55 cut-offs are NDR's: the deck names no zones (the word BULLISH on that page stands
  beside the 2008-2018 Chart View table, matching the current reading of 80.00, not a zone label), so "bullish /
  neutral / bearish" below are OUR names. The deck gives no indicator count; its readings (66.7 / 58.3 etc., table on
  printed p. 6) are consistent with a small number of indicators per half (inference, not stated).
  NOTE: CONFIDENCE_RESEARCH.md says Morris's 2018-08 "Weight of the Evidence" article cites these thresholds; it does
  not (checked: no mention of Ned Davis there or in parts 2-3 / 12-13). The numbers above come from NDR's own deck.
Brooks (exit idea "structure breaks weigh more than single candles"): the forum page cited in CONFIDENCE_RESEARCH.md
  (brookstradingcourse.com/support-forum/09-pullbacks-and-bar-counting/confused-about-consecutive-bottom-attempts-in-
  a-bear-trend/) contains only member posts and does NOT state that rule; no number is published. So it is NOT used by
  default; hand_bulkowski(task="exit", structure_weight=<float>) adds it only when the user supplies the weight.

Adaptations (daily stock/index methods -> 15-minute futures signals), and why
-----------------------------------------------------------------------------
* Bulkowski's rates are for daily stocks and measure only the breakout DIRECTION, not $ after our stop/target/costs.
  We use them as a prior on direction and let Platt (on training rows) set the scale and the base rate.
* Bulkowski differs for the bullish and bearish version of a pattern (engulfing 63% vs 79%). score(X) only sees the
  oriented X, so by default each two-sided pattern gets the MEAN log-odds of its two sides, an unpublished side
  counting as 0 (no evidence; directional=False). So the black marubozu's derived 66% is NOT given to the white
  marubozu: the symmetric marubozu weight is (0.663 + 0) / 2. directional=True uses the side-specific weight and then
  needs the trade direction: fit() takes it from meta["d"], score()/predict_proba() need d=... .
* Morris: daily Nasdaq Composite -> each of our markets on 15-min bars; horizons kept as BAR COUNTS (his medium 2-4
  weeks = 10-20 daily bars -> EMA8 vs EMA20 and 5-bar swing structure; his long 4-8 weeks with a 19/39 MACD ->
  EMA20 vs EMA50 plus the 60-minute trend). His breadth (Nasdaq advances/declines/volume) -> agreement of the OTHER
  index futures (x_<SYM>_*), the only cross-section we have. His weights are secret and he states no horizon grouping,
  so the weighting here is OUR FALLBACK, not his structure: equal weight per horizon (medium, long, breadth: 33.3 each,
  so price gets 66.7, in line with part 4's "price-based indicators should dominate the array"), equal split inside a
  horizon, and Price Short left out by default (our reading of part 6's hedged "Many times ..." sentence; part 12
  lists Price Short, so include_short=True adds it back as a 4th equal block). Adaptive Trend (part 8) is OMITTED: its
  ATR period, smoothing and standard-deviation multiple are not published and it is a stateful line with no SPEC
  feature; any analog would need invented numbers. Morris's own principle (weight by each indicator's trend
  performance) is not used either, because it would make this family learned and his performance metric is not given.
* Morris entries/exits: he allows buys in every band and only raises the per-instrument hurdle in weaker bands
  (part 13: "Red: Trend > 60, Orange: Trend > 55, Yellow/Green: Trend > 50"); that hurdle is exposed as
  bands()["buy_hurdle"] for the harness (we have no separate per-instrument Trend score, so score() does not apply it).
  bands()["entry_zone"] (WoE > 50) and ["exit_zone"] (WoE <= 30) are OUR adaptations, not Morris rules; he publishes
  no band-based sell rule. Exit score = 100 - WoE. score() is stateless (one row at a time), so the transition-zone
  hysteresis exists only as these informational columns; a harness that exits at the first bar whose p clears its
  threshold exits on the first downward crossing of THAT threshold, which is not tied to 30.
* NDR: their composite is monthly U.S. stocks over proprietary indicators (count not given in the deck). Ours =
  percent of our trend/momentum/breadth state indicators (always voting) plus event families that vote only when they
  fire. Exit score = 100 - composite; exit zone = composite < 55 (NDR's negative-return zone), entry zone > 70.
* Missing values (warm-up, no bar in another market): a NaN pattern counts as not firing; a NaN Morris/NDR component
  is dropped and the rest re-normalised (a row with nothing available scores 50 = no evidence).
* Trade-state columns of exit rows (open_R, mfe_R, ...) have no published hand weight in these sources and are not
  used by hand_bulkowski / hand_morris_woe / hand_ndr_composite (hand_user can weight them).
"""
from __future__ import annotations

import math
import os
import sys
import warnings

import numpy as np
import pandas as pd
from sklearn.exceptions import NotFittedError

from scorer_api import Scorer, platt, register

HERE = os.path.dirname(os.path.abspath(__file__))
BULKOWSKI_CSV = os.path.join(HERE, "bulkowski_weights.csv")
USER_CSV = os.path.join(HERE, "user_weights.csv")
LOGODDS_PER_POINT = math.log(2) / 20                       # credit-scorecard scaling: +20 points doubles the odds
EXIT_STATE = ["open_R", "mfe_R", "mae_R", "bars_held", "dist_stop_R", "mins_to_1645"]
MARKETS = ("ES", "NQ", "YM")


class HandWeightsMissing(NotFittedError):
    """Raised by fit() when a hand scorer has no weights to use (e.g. user_weights.csv still blank). Subclass of
    sklearn's NotFittedError (itself ValueError + AttributeError), so a harness can catch any of them and skip."""
    skip = True


def logit(p):
    return math.log(p / (1.0 - p))


# ============================================================================================================ Bulkowski
# One row per (our pattern, side). side = the RAW direction our rule gives the pattern (bull = +1, bear = -1).
# rate = Bulkowski's measured share of breakouts in OUR textbook direction for that side (None = not published).
# basis: published (his tested rate is the textbook direction), complement (he found the opposite: 1 - his rate),
# derived (computed from published numbers, see note), published_trade (pooled win rate of his 7%-target/7%-stop
# breakout TRADE test, see BULKOWSKI_TRADE_TESTS), not_published (no direction share on the page -> weight 0),
# no_equivalent (no Bulkowski number maps to our rule -> weight 0).
_B = "https://www.thepatternsite.com/"

# Bulkowski chart-pattern trade tests, (wins, losses) for (bull market, bear market) per breakout side, as printed.
# Setup on all of them: close above the top / below the bottom of the pattern, buy/short at the next day's open.
# "used" = the table that feeds BULKOWSKI (symmetric 7% target / 7% stop); the others are kept for reference only.
BULKOWSKI_TRADE_TESTS = {
    ("nr7_breakout", "used"): dict(
        page="nr7.html", table="Table 3: Testing the NR7 (7% target, 7% stop)",
        up=((7600, 5791), (920, 1112)), down=((4990, 6218), (166, 186)),
        caveat="setup's first bullet reads 'Find a NR7 downtrend' (not explained); table header cites 29,021 trades "
               "but its win+loss counts sum to 26,983; 1,201 stocks, 1990-01 to 2013-03 per the statistics section"),
    ("inside_bar_breakout", "used"): dict(
        page="InsideDays.html", table="Table 7: Testing the Inside Day (7% target, 7% stop)",
        up=((7082, 5375), (1315, 1514)), down=((4837, 6349), (1665, 1445)),
        caveat="entry 'If price closes above the pattern's high, buy at the open the next day' (pattern high/low = "
               "'the first day's high or low', the mother bar, as our rule); no trend required; 29,582 trades "
               "(reconciles with the counts); 1,260 stocks, 1989-12 to 2013-01"),
    ("inside_bar_breakout", "pattern_stop"): dict(
        page="InsideDays.html",
        table="Table 8: Testing the Inside Day with Pattern Stop (used only with breakout_table='pattern_stop')",
        up=((5915, 6580), (1322, 1507)), down=((4266, 6942), (1680, 1429)),
        caveat="stop a penny beyond the pattern instead of 7% (target not restated; average winner ~$705 as in Table "
               "7): asymmetric payoff, so the win rate is not a direction rate (bull/up wins 47% yet nets +$55.28 "
               "per trade)"),
    ("outside_bar", "reference"): dict(
        page="OutsideDays.html", table="Table 7: Testing the Outside Day (7% target, 7% stop; not used)",
        up=((7142, 5273), (1401, 1688)), down=((4729, 6227), (1721, 1497)),
        caveat="enters after a LATER close beyond the outside day's range; our outside_bar fires on the bar itself with "
               "direction from its own close vs open"),
    ("outside_bar", "pattern_stop"): dict(
        page="OutsideDays.html", table="Table 8: Testing the Outside Day with Pattern Stop (not used)",
        up=((5863, 6609), (1373, 1717)), down=((4001, 6990), (1666, 1554)), caveat="as Table 7, pattern stop"),
}


def trade_rate(pattern, side, which="used"):
    """Pooled win rate (wins / trades over bull + bear markets) of a Bulkowski trade test for one breakout side."""
    t = BULKOWSKI_TRADE_TESTS[(pattern, which)][side]
    w, n = sum(a for a, _ in t), sum(a + b for a, b in t)
    return w / n


def _trade_line(pattern, side, which="used"):
    t = BULKOWSKI_TRADE_TESTS[(pattern, which)]
    (bw, bl), (rw, rl) = t[side]
    return (f"{t['table']}: {side} breakouts wins bull mkt {bw / (bw + bl):.0%} ({bw:,} W / {bl:,} L), bear mkt "
            f"{rw / (rw + rl):.0%} ({rw:,} W / {rl:,} L) -> pooled {trade_rate(pattern, side, which):.1%}")


BULKOWSKI = [
    # pattern, side, Bulkowski name, page, theoretical, tested performance (verbatim), rate, basis, overall rank, freq rank, note
    ("dragonfly_doji", "bull", "Doji, dragonfly", "Dragonfly.html", "Bullish reversal during a decline, otherwise indecision",
     "Reversal 50% of the time", None, "not_published", 98, 44,
     "No trend required, so the 50% reversal rate is not a direction rate; page only says 'upward breakouts "
     "predominate' (no number). Weight 0."),
    ("gravestone_doji", "bear", "Doji, gravestone", "Gravestone.html", "Indecision to bearish reversal (during up trends)",
     "Bearish reversal 51% of the time", None, "not_published", 77, 42,
     "Price trend leading to the pattern: 'None required' (as the dragonfly), so the 51% reversal rate is not a "
     "direction rate; page only says price 'should breakout downward most often, which it does' (no number). "
     "Weight 0 (same rule as the dragonfly; was +0.040 if the 51% were read as a direction share)."),
    ("hammer", "bull", "Hammer", "Hammer.html", "Bullish reversal", "Bullish reversal 60% of the time", 0.60,
     "published", 65, 36, "Downtrend required; our rule needs prior close < EMA10."),
    ("hanging_man", "bear", "Hanging man", "HangingMan.html", "Bearish reversal",
     "Bullish continuation 59% of the time", 0.41, "complement", 87, 16,
     "Upward breakouts 59% -> textbook bearish direction 41%: negative weight."),
    ("inverted_hammer", "bull", "Hammer, inverted", "HammerInv.html", "Bullish reversal",
     "Bearish continuation 65% of the time", 0.35, "complement", 6, 61,
     "Downward breakouts 65% -> textbook bullish direction 35%: negative weight (yet overall rank 6)."),
    ("shooting_star", "bear", "Shooting star (one line)", "ShootingStar.html", "Bearish reversal",
     "Bearish reversal 59% of the time", 0.59, "published", 55, 37, "Uptrend required; our rule needs prior close > EMA10."),
    ("marubozu", "bull", "Marubozu, white", "WhiteMarubozu.html", "Continuation", "Continuation 56% of the time",
     None, "not_published", 71, 27,
     "Continuation is vs the prior trend, no trend required; no upward-breakout share published. Weight 0."),
    ("marubozu", "bear", "Marubozu, black", "BlackMarubozu.html", "Continuation", "Continuation 53% of the time",
     0.66, "derived", 57, 30,
     "Page: 'upward breakouts occur 34% of the time in the 19,993 black marubozu candles' -> 66% downward."),
    ("engulfing", "bull", "Engulfing, bullish", "BullEngulfing.html", "Bullish reversal",
     "Bullish reversal 63% of the time", 0.63, "published", 84, 12,
     "Page intro also says rank 22; the results table says 84 (used)."),
    ("engulfing", "bear", "Engulfing, bearish", "BearEngulfing.html", "Bearish reversal",
     "Bearish reversal 79% of the time", 0.79, "published", 91, 11, "About 20,000 samples per the page."),
    ("harami", "bull", "Harami, bullish", "HaramiBull.html", "Bullish reversal", "Bullish reversal 53% of the time",
     0.53, "published", 38, 25, ""),
    ("harami", "bear", "Harami, bearish", "HaramiBear.html", "Bearish reversal", "Bullish continuation 53% of the time",
     0.47, "complement", 72, 26, "Upward breakouts 53% -> textbook bearish 47%."),
    ("piercing", "bull", "Piercing pattern", "Piercing.html", "Bullish reversal", "Bullish reversal 64% of the time",
     0.64, "published", 13, 40, "Page intro says rank 21; results table and discussion say 13 (used)."),
    ("dark_cloud", "bear", "Dark cloud cover", "DarkCloudCover.html", "Bearish reversal",
     "Bearish reversal 60% of the time", 0.60, "published", 22, 46, ""),
    ("morning_evening_star", "bull", "Morning star", "MorningStar.html", "Bullish reversal",
     "Bullish reversal 78% of the time", 0.78, "published", 12, 66, ""),
    ("morning_evening_star", "bear", "Evening star", "EveningStar.html", "Bearish reversal",
     "Bearish reversal 72% of the time", 0.72, "published", 4, 71, ""),
    ("three_soldiers_crows", "bull", "Three white soldiers", "ThreeWhiteSoldiers.html", "Bullish reversal",
     "Bullish reversal 82% of the time", 0.82, "published", 32, 67,
     "His rule needs a downtrend, ours does not. 'Just 593 out of 3,333 samples showed downward breakouts.' Intro "
     "'ranking 3' is the reversal rank; overall rank 32."),
    ("three_soldiers_crows", "bear", "Three black crows", "ThreeBlackCrows.html", "Bearish reversal",
     "Bearish reversal 78% of the time", 0.78, "published", 3, 60, "His rule needs an uptrend, ours does not."),
    ("three_inside", "bull", "Three inside up", "ThreeInsideUp.html", "Bullish reversal",
     "Bullish reversal 65% of the time", 0.65, "published", 20, 31, ""),
    ("three_inside", "bear", "Three inside down", "ThreeInsideDown.html", "Bearish reversal",
     "Bearish reversal 60% of the time", 0.60, "published", 56, 33, ""),
    ("outside_bar", "bull", "(none; Outside day is a chart pattern)", "OutsideDays.html", "",
     _trade_line("outside_bar", "up", "reference"), None, "no_equivalent", None, None,
     "Trade tests exist (Table 7 7%/7%: up 58%/45%, down 43%/53% bull/bear mkt; Table 8 pattern stop 47/36/44/52%) but "
     "they enter after a LATER close beyond the outside day's range, in either direction; our outside_bar fires on the "
     "outside bar itself with its direction from its own close vs open, and the page reports nothing by close position "
     "or colour. No number maps to our rule. Weight 0."),
    ("outside_bar", "bear", "(none; Outside day is a chart pattern)", "OutsideDays.html", "",
     _trade_line("outside_bar", "down", "reference"), None, "no_equivalent", None, None,
     "As bull side. Weight 0."),
    ("pin_bar", "bull", "Hammer + Hanging man (same shape, both trend contexts)", "Hammer.html HangingMan.html", "",
     "60% up (hammer, downtrend); 59% up (hanging man, uptrend)", 0.595, "derived", None, None,
     "Our pin bar has no trend filter, so it is the union of his hammer (60% up) and hanging-man (59% up) contexts: "
     "unweighted mean 59.5%."),
    ("pin_bar", "bear", "Shooting star + Inverted hammer (same shape, both trend contexts)",
     "ShootingStar.html HammerInv.html", "", "59% down (shooting star, uptrend); 65% down (inverted hammer, downtrend)",
     0.62, "derived", None, None, "Union of shooting star (59% down) and inverted hammer (65% down): mean 62%."),
    ("tweezer", "bull", "Tweezers bottom", "TweezersBottom.html", "Bullish reversal",
     "Bearish continuation 52% of the time", 0.48, "complement", 44, 39, "Downward breakouts 52% -> textbook bullish 48%."),
    ("tweezer", "bear", "Tweezers top", "TweezersTop.html", "Bearish reversal", "Bullish continuation 56% of the time",
     0.44, "complement", 81, 35, "'an upward breakout ... happens 56% of the time' -> textbook bearish 44%."),
    ("inside_bar_breakout", "bull", "Inside day (chart pattern), upward breakout", "InsideDays.html", "",
     _trade_line("inside_bar_breakout", "up"), trade_rate("inside_bar_breakout", "up"), "published_trade", None, None,
     "Trade test with our entry convention (close above the first day's high, buy next open); 7% target / 7% stop, "
     "daily stocks: '+7% before -7%', not a candle breakout share. Pattern-stop Table 8 (47% / 47%, pooled 47.2%) "
     "not used by default (asymmetric payoff; breakout_table='pattern_stop' uses it). "
     + BULKOWSKI_TRADE_TESTS[("inside_bar_breakout", "used")]["caveat"]),
    ("inside_bar_breakout", "bear", "Inside day (chart pattern), downward breakout", "InsideDays.html", "",
     _trade_line("inside_bar_breakout", "down"), trade_rate("inside_bar_breakout", "down"), "published_trade",
     None, None, "As bull side (short at the next open after a close below the first day's low). Pattern-stop Table 8 "
     "pooled 41.5% not used by default. Below 50%: in his mostly bull-market stock sample shorts lose."),
    ("nr7_breakout", "bull", "NR7 (chart pattern), upward breakout", "nr7.html", "",
     _trade_line("nr7_breakout", "up"), trade_rate("nr7_breakout", "up"), "published_trade", None, None,
     "Trade test with our entry convention (close above the NR7 bar, buy next open); 7% target / 7% stop, daily "
     "stocks. " + BULKOWSKI_TRADE_TESTS[("nr7_breakout", "used")]["caveat"]),
    ("nr7_breakout", "bear", "NR7 (chart pattern), downward breakout", "nr7.html", "",
     _trade_line("nr7_breakout", "down"), trade_rate("nr7_breakout", "down"), "published_trade", None, None,
     "As bull side (short at the next open after a close below the NR7 bar). Below 50%: shorts lose in his sample."),
    ("clv_extreme", "bull", "(none)", "", "", "", None, "no_equivalent", None, None, "Close-location fade. Weight 0."),
    ("clv_extreme", "bear", "(none)", "", "", "", None, "no_equivalent", None, None, "Weight 0."),
    ("bar_80_20", "bull", "(none)", "", "", "", None, "no_equivalent", None, None,
     "80-20 bar is not a Bulkowski candle. Weight 0."),
    ("bar_80_20", "bear", "(none)", "", "", "", None, "no_equivalent", None, None, "Weight 0."),
    ("tall_trend_bar", "bull", "Long white day", "LongWhiteDay.html", "Continuation", "Continuation 58% of the time",
     None, "not_published", 53, 10,
     "Continuation is vs the prior trend (no trend required); no upward-breakout share published. Weight 0. (Our "
     "1.46 x avgR22 tall-bar threshold follows his tall-candle rule.)"),
    ("tall_trend_bar", "bear", "Long black day", "LongBlack.html", "Continuation", "Continuation 53% of the time",
     None, "not_published", 19, 9, "As long white day. Weight 0."),
    ("five_lower_lows_higher_highs", "bull", "(none)", "", "", "", None, "no_equivalent", None, None, "Weight 0."),
    ("five_lower_lows_higher_highs", "bear", "(none)", "", "", "", None, "no_equivalent", None, None, "Weight 0."),
    ("clv5_extreme", "bull", "(none)", "", "", "", None, "no_equivalent", None, None, "Weight 0."),
    ("clv5_extreme", "bear", "(none)", "", "", "", None, "no_equivalent", None, None, "Weight 0."),
]
_BCOLS = ["pattern", "side", "bulkowski_name", "page", "theoretical", "tested_performance", "rate_textbook", "basis",
          "overall_rank_of_103", "frequency_rank", "note"]
USABLE_BASIS = ("published", "complement", "derived", "published_trade")
ALL_BASIS = USABLE_BASIS + ("not_published", "no_equivalent")


BREAKOUT_TABLES = ("7pct", "pattern_stop")


def bulkowski_table(breakout_table: str = "7pct") -> pd.DataFrame:
    """The Bulkowski mapping as a DataFrame with the log-odds weight per side and the symmetric (mean) weight.
    weight_symmetric = mean of weight_logodds over ALL rows of the pattern, an unpublished side counting as 0 (no
    evidence): one side's published number is never mirrored onto the other (black marubozu 0.663 -> 0.332).
    breakout_table: "7pct" (default; InsideDays Table 7 / nr7 Table 3, 7% target and 7% stop) or "pattern_stop"
    (inside day from InsideDays Table 8, stop a penny beyond the pattern; NR7 has no such table and keeps Table 3)."""
    if breakout_table not in BREAKOUT_TABLES:
        raise ValueError(f"breakout_table must be one of {BREAKOUT_TABLES}")
    t = pd.DataFrame(BULKOWSKI, columns=_BCOLS)
    if breakout_table == "pattern_stop":
        for side, sd in (("bull", "up"), ("bear", "down")):
            i = (t.pattern == "inside_bar_breakout") & (t.side == side)
            t.loc[i, "rate_textbook"] = trade_rate("inside_bar_breakout", sd, "pattern_stop")
            t.loc[i, "tested_performance"] = _trade_line("inside_bar_breakout", sd, "pattern_stop")
            t.loc[i, "note"] = ("breakout_table='pattern_stop': InsideDays Table 8, our entry convention, stop a penny "
                                "beyond the pattern. Both sides < 50% because the payoff is asymmetric (bull/up wins "
                                "47% yet nets +$55.28), so the symmetric weight is negative: read with care.")
    t["url"] = [" ".join(_B + p for p in pg.split()) if pg else "" for pg in t.page]
    t["weight_logodds"] = [logit(r) if (b in USABLE_BASIS and r is not None and not pd.isna(r)) else 0.0
                           for r, b in zip(t.rate_textbook, t.basis)]
    sym = t.groupby("pattern").weight_logodds.mean().round(12)              # harami: +0.12 and -0.12 -> exactly 0
    t["weight_symmetric"] = t.pattern.map(sym).fillna(0.0)
    t["points"] = t.weight_logodds / LOGODDS_PER_POINT
    return t[["pattern", "side", "bulkowski_name", "url", "theoretical", "tested_performance", "rate_textbook",
              "basis", "weight_logodds", "weight_symmetric", "points", "overall_rank_of_103", "frequency_rank", "note"]]


def write_bulkowski_csv(path=BULKOWSKI_CSV):
    bulkowski_table().to_csv(path, index=False, float_format="%.4f")
    return path


# ============================================================================================================ helpers
def _num(X: pd.DataFrame, c: str) -> np.ndarray:
    """Column as float array (NaN if the column is missing)."""
    if c not in X.columns:
        return np.full(len(X), np.nan)
    return pd.to_numeric(X[c], errors="coerce").to_numpy(dtype=float)


def _d_array(d, n):
    if d is None:
        return None
    d = np.asarray(d, dtype=float).reshape(-1)
    if d.size == 1:
        d = np.full(n, d[0])
    if d.size != n or not np.isin(d, (-1.0, 1.0)).all():
        raise ValueError("d must be +1/-1 per row (or a scalar)")
    return d


class _Calibrated(Scorer):
    """Shared Platt calibration: fit() computes the fixed hand score on the training rows and maps it to P(y=1)."""
    family = "hand"
    needs_d = False

    def _prepare(self, X, y, w, meta):          # hook (hand_user loads its weights here)
        pass

    def _d_from_meta(self, meta, n):
        if not self.needs_d:
            return None
        if meta is None or "d" not in meta:
            raise ValueError(f"{self.name}: directional=True needs meta['d'] in fit()")
        return _d_array(meta["d"].to_numpy(), n)

    def fit(self, X, y, w=None, meta=None):
        """Platt on the TRAINING rows only (same fit as scorer_api.platt, kept as (a, b) so the table can show the
        calibrated log-odds). The slope is kept >= 0 unless allow_negative_slope=True: a hand-set scorer must not let
        the calibration silently reverse the published direction; if the training rows contradict it, the scorer
        becomes flat at the training base rate (platt_clipped_ = True), which says 'no information' honestly."""
        self._prepare(X, y, w, meta)
        self.columns_ = list(X.columns)
        y = np.asarray(y).astype(int).reshape(-1)
        s = self.score(X, d=self._d_from_meta(meta, len(X)))
        self.n_train_ = len(y)
        self.base_rate_ = float(np.average(y, weights=w)) if len(y) else 0.5
        flat = (0.0, logit(min(max(self.base_rate_, 1e-6), 1 - 1e-6)))
        self.platt_clipped_ = False
        if len(np.unique(y)) < 2 or np.nanstd(s) == 0:
            self.platt_a_, self.platt_b_ = flat         # nothing to calibrate against: constant = base rate
        else:
            from sklearn.linear_model import LogisticRegression
            m = LogisticRegression(C=1e6, max_iter=1000).fit(s.reshape(-1, 1), y, sample_weight=w)
            self.platt_a_, self.platt_b_ = float(m.coef_[0, 0]), float(m.intercept_[0])
            if self.platt_a_ < 0 and not self.params.get("allow_negative_slope", False):
                self.platt_a_, self.platt_b_ = flat
                self.platt_clipped_ = True
        # No closure is stored: the calibration lives only in the plain floats platt_a_ / platt_b_, so a deepcopy of a
        # fitted scorer is independent of later refits of the original (no fold-to-fold leakage) and pickling works.
        return self

    def predict_proba(self, X, d=None):
        if not hasattr(self, "platt_a_"):
            raise NotFittedError(f"{self.name}: call fit() first")
        z = self.platt_a_ * np.asarray(self.score(X, d=d), float) + self.platt_b_
        return np.clip(1.0 / (1.0 + np.exp(-z)), 0.0, 1.0)

    def _table_columns(self, X_columns=None):
        """Columns to describe: those given, else those seen in fit(), else every market's x_ columns."""
        if X_columns is not None:
            return list(X_columns)
        return getattr(self, "columns_", None) or [f"x_{m}_{s}" for m in MARKETS for s in ("ret", "ema_stack")]

    def _table(self, rows):
        t = pd.DataFrame(rows, columns=["signal", "weight", "points", "meaning", "source"])
        if hasattr(self, "platt_a_"):
            t["calibrated_logodds"] = self.platt_a_ * t.weight      # log-odds of y per unit after Platt
        return t


# ============================================================================================================ 1 Bulkowski
@register
class HandBulkowski(_Calibrated):
    """score = sum over patterns firing WITH the trade of w_p - sum over patterns firing AGAINST it of w_p
    (w_p = ln(p/(1-p)), p = Bulkowski's rate in the textbook direction; X is oriented so pat_x = +1 with, -1 against).
    Exit task: score_exit = -score_entry (+ optional structure term), i.e. evidence against the open trade.
    params: directional (False) - side-specific weights (needs d); structure_weight (None) - exit only: log-odds added
    per structure break against the trade (brk_5, brk_10 == -1); no published number exists, so it is off unless set;
    breakout_table ("7pct") - which Bulkowski inside-day trade table feeds inside_bar_breakout ("pattern_stop" = his
    Table 8; see the module docstring for why it is not the default)."""
    name = "hand_bulkowski"
    source = ("Bulkowski, thepatternsite.com candle pages (Encyclopedia of Candlestick Charts, Wiley 2008): tested "
              "reversal/continuation rates -> log-odds; inside-day/NR7 breakout trade tests; see bulkowski_weights.csv")

    def __init__(self, task="entry", directional=False, structure_weight=None, breakout_table="7pct", **params):
        super().__init__(task=task, directional=directional, structure_weight=structure_weight,
                         breakout_table=breakout_table, **params)
        self.directional = bool(directional)
        self.needs_d = self.directional
        self.structure_weight = structure_weight
        self.breakout_table = breakout_table
        self.table = bulkowski_table(breakout_table)
        t = self.table
        self.patterns = list(dict.fromkeys(t.pattern))
        self.w_sym = t.groupby("pattern").weight_symmetric.first().to_dict()
        self.w_side = {(p, s): w for p, s, w in zip(t.pattern, t.side, t.weight_logodds)}

    def score(self, X, d=None):
        n = len(X)
        s = np.zeros(n)
        d = _d_array(d, n)
        if self.directional and d is None:
            raise ValueError("hand_bulkowski(directional=True) needs d (trade direction) in score/predict_proba")
        for p in self.patterns:
            v = np.nan_to_num(_num(X, f"pat_{p}"))
            v = np.sign(v)
            if not v.any():
                continue
            if self.directional:
                raw = v * d                                           # +1 = the bullish version fired
                w = np.where(raw > 0, self.w_side.get((p, "bull"), 0.0), self.w_side.get((p, "bear"), 0.0))
            else:
                w = self.w_sym.get(p, 0.0)
            s += v * w
        if self.task == "exit":
            s = -s
            if self.structure_weight:
                for c in ("brk_5", "brk_10"):
                    s += float(self.structure_weight) * (np.nan_to_num(_num(X, c)) < 0)
        return s

    def weights_table(self):
        sign = -1.0 if self.task == "exit" else 1.0
        rows = []
        t = self.table
        for p in self.patterns:
            sub = t[t.pattern == p]
            src = "; ".join(f"{r.bulkowski_name}: {r.tested_performance or 'n/a'} [{r.basis}] {r.url}".strip()
                            for r in sub.itertuples())
            sides = [(r.side, r.weight_logodds, r.rate_textbook) for r in sub.itertuples()]
            if self.directional:
                for (side, wl, rate), basis in zip(sides, sub.basis):
                    w = sign * wl
                    rows.append((f"pat_{p}:{side}", w, w / LOGODDS_PER_POINT,
                                 self._meaning(p, side, rate, w, basis), src))
            else:
                w = sign * self.w_sym.get(p, 0.0)
                desc = ", ".join(f"{s} {r:.1%}" for s, _, r in sides if r is not None and not pd.isna(r)) or "no rate"
                rows.append((f"pat_{p}", w, w / LOGODDS_PER_POINT,
                             f"{p} firing with the trade ({desc}; mean log-odds over its sides, an unpublished side "
                             "counting 0)"
                             + (" -> counts AGAINST the open trade when it fires with it; exit evidence when it "
                                "fires against" if self.task == "exit" else ""), src))
        if self.task == "exit" and self.structure_weight:
            for c in ("brk_5", "brk_10"):
                rows.append((f"{c}<0", float(self.structure_weight), float(self.structure_weight) / LOGODDS_PER_POINT,
                             "fresh swing break against the open trade (user-set; no published number)",
                             "user parameter structure_weight (Brooks idea, unquantified)"))
        return self._table(rows)

    def _meaning(self, p, side, rate, w, basis=""):
        if rate is None or pd.isna(rate):
            r = "no published direction rate"
        elif basis == "published_trade":
            kind = ("7% target / pattern stop" if (self.breakout_table == "pattern_stop" and p == "inside_bar_breakout")
                    else "7% target / 7% stop")
            r = f"Bulkowski breakout trade test ({kind}): {rate:.1%} wins in the textbook direction"
        else:
            r = f"Bulkowski {rate:.1%} in textbook direction"
        if self.task == "exit":
            return f"{side} {p}: {r}; exit weight per +1 (fired with the trade) = {w:+.3f}"
        return f"{side} {p} firing with the trade: {r}"


# ============================================================================================================ 2 Morris
# component: (name, horizon, how it is computed from oriented X (on if > 0), Morris counterpart)
MORRIS_COMPONENTS = [
    ("mom>0", "short", "mom", "Price Short (10-21 day price relationship) -> 14-bar momentum"),
    ("close>ema8", "short", "dist_ema8", "Price Short -> close vs EMA8"),
    ("ema8>ema20", "medium", "dist_ema20-dist_ema8", "Price Medium (2-4 weeks, MACD-like) -> EMA8 vs EMA20"),
    ("ema_stack>0", "medium", "ema_stack", "Price Medium -> EMA8/20/50 stacked with the trade"),
    ("struct_5>0", "medium", "struct_5", "Trend Capturing with Price -> rising/falling 5-bar swings"),
    ("ema20>ema50", "long", "dist_ema50-dist_ema20", "Price Long (4-8 weeks, MACD 19/39 approx.) -> EMA20 vs EMA50"),
    ("close>ema50", "long", "dist_ema50", "Price Long -> close vs EMA50"),
    ("h1_ema_stack>0", "long", "h1_ema_stack", "Price Long -> 60-min EMA stack"),
    ("h1_struct_5>0", "long", "h1_struct_5", "Price Long -> 60-min swing structure"),
    # breadth components are added per x_<SYM>_ column present in X
]
MORRIS_BANDS = [(0, 30, "red"), (30, 50, "orange"), (50, 80, "yellow"), (80, 100, "green")]   # (lo, hi] by level
MORRIS_BUY_HURDLE = {"red": 60.0, "orange": 55.0, "yellow": 50.0, "green": 50.0}   # part 13: per-instrument "Trend >"
MORRIS_SRC = ("Morris, StockCharts 'Building a Rules-Based Trend Following Model' parts 4, 6, 8, 9, 12, 13 (2018) and "
              "'Weight of the Evidence' (2018-08-07): binary components, weights sum to 100, bands "
              "0-30/31-50/51-80/81-100. His weights are not public: equal weight per horizon with Price Short off by "
              "default is OUR fallback; Adaptive Trend omitted (parameters unpublished)")
MORRIS_SHORT_QUOTE = ("part 6: 'Many times, a short-term measure is not actually used in the weight of the evidence "
                      "calculation but serves a weight of the evidence model well with a warning of things to come'; "
                      "part 12 lists Price Short among his components")


def _expr(X, e):
    if "-" in e:
        a, b = e.split("-")
        return _num(X, a) - _num(X, b)
    return _num(X, e)


@register
class HandMorrisWoE(_Calibrated):
    """Weight of the Evidence level 0-100 = sum of the weights of the components that are 'on' (with the trade).
    Entry score = level; exit score = 100 - level (evidence against the open trade). bands(X) gives the band
    membership (red/orange/yellow/green, Morris part 12), his part 13 per-instrument buy hurdle for that band
    (buy_hurdle: 60/55/50/50), and OUR adapted entry_zone (> 50) / exit_zone (<= 30) columns (not Morris rules).
    params: include_short (False: our fallback reading of part 6; part 12 lists Price Short, so True is defensible),
    score_mode ('level' | 'band': score = band index 0-3)."""
    name = "hand_morris_woe"
    source = MORRIS_SRC

    def __init__(self, task="entry", include_short=False, score_mode="level", **params):
        super().__init__(task=task, include_short=include_short, score_mode=score_mode, **params)
        self.include_short = bool(include_short)
        if score_mode not in ("level", "band"):
            raise ValueError("score_mode must be 'level' or 'band'")
        self.score_mode = score_mode
        self.horizons = (["short"] if self.include_short else []) + ["medium", "long", "breadth"]

    def _components(self, X):
        comps = [(n, h, e, m) for n, h, e, m in MORRIS_COMPONENTS if h in self.horizons]
        for c in X.columns:
            if c.startswith("x_") and (c.endswith("_ret") or c.endswith("_ema_stack")):
                comps.append((f"{c}>0", "breadth", c, "Breadth (Nasdaq A/D, new highs/lows, up/down volume) -> "
                              "other index futures agree: " + c))
        return comps

    def level(self, X):
        comps = self._components(X)
        n = len(X)
        num = np.zeros(n)
        den = np.zeros(n)
        for h in self.horizons:
            hc = [c for c in comps if c[1] == h]
            if not hc:
                continue
            vals = np.column_stack([_expr(X, e) for _, _, e, _ in hc])
            avail = np.isfinite(vals)
            k = avail.sum(axis=1)
            on = np.where(avail, vals > 0, False).sum(axis=1)
            frac = np.divide(on, k, out=np.zeros(n), where=k > 0)   # share of this horizon's available components on
            num += np.where(k > 0, frac, 0.0)
            den += (k > 0)
        return np.where(den > 0, 100.0 * num / np.maximum(den, 1), 50.0)

    def bands(self, X):
        lv = self.level(X)
        out = pd.DataFrame({"woe": lv}, index=X.index)
        for lo, hi, nm in MORRIS_BANDS:
            out[f"band_{nm}"] = ((lv > lo) | (lo == 0)) & (lv <= hi)
        out["band"] = np.select([out[f"band_{nm}"] for _, _, nm in MORRIS_BANDS], [nm for *_, nm in MORRIS_BANDS], "")
        # Morris part 13: buys are allowed in every band, the instrument's own Trend must clear a band-dependent hurdle.
        # Exposed for the harness (e.g. against a 0-100 candidate score); score() does not apply it.
        out["buy_hurdle"] = out["band"].map(MORRIS_BUY_HURDLE).astype(float)
        out["entry_zone"] = lv > 50                    # OUR adaptation (yellow/green), not a Morris rule
        out["exit_zone"] = lv <= 30                    # OUR adaptation (red); Morris publishes no band-based sell rule
        return out

    def score(self, X, d=None):
        lv = self.level(X)
        if self.score_mode == "band":
            lv = np.select([lv <= 30, lv <= 50, lv <= 80], [0.0, 1.0, 2.0], 3.0)
            return 3.0 - lv if self.task == "exit" else lv
        return 100.0 - lv if self.task == "exit" else lv

    def weights_table(self, X_columns=None):
        comps = self._components(pd.DataFrame(columns=self._table_columns(X_columns)))
        hw = 100.0 / len(self.horizons)
        sign = -1.0 if self.task == "exit" else 1.0
        rows = []
        for h in self.horizons:
            hc = [c for c in comps if c[1] == h]
            for nm, _, e, m in hc:
                w = sign * hw / len(hc)
                rows.append((nm, w, w, f"[{h}] {m}" + ("; on = evidence to STAY (exit score = 100 - WoE)"
                                                        if self.task == "exit" else ""), MORRIS_SRC))
        if not self.include_short:
            for nm, h, e, m in MORRIS_COMPONENTS:
                if h == "short":
                    rows.append((nm, 0.0, 0.0, f"[short] {m}: off by default (our fallback; {MORRIS_SHORT_QUOTE}; "
                                 "include_short=True adds it)", MORRIS_SRC))
        rows.append(("(adaptive_trend)", 0.0, 0.0, "[omitted] Morris part 8 Adaptive Trend (EMA of midpoint +/- half the "
                     "true-range EMA +/- X std devs; close above = on): ATR period, smoothing and X not published, "
                     "stateful line with no SPEC feature -> not built", MORRIS_SRC))
        t = self._table(rows)
        t["horizon"] = [r[3].split("]")[0].strip("[") for r in rows]
        return t


# ============================================================================================================ 3 NDR
NDR_STATE = ["dist_ema8", "dist_ema20", "dist_ema50", "ema_stack", "ema20_slope", "above_ema20_share", "mom",
             "mom_slope3", "dist_vwap", "day_ret", "struct_5", "struct_10", "h1_ema_stack", "h1_mom", "h1_struct_5"]
NDR_EVENTS = ["fam_reversal", "fam_continuation", "fam_breakout", "fam_closeloc", "fam_exhaustion", "brk_5", "brk_10",
              "mom_x100"]
NDR_ZONES = {"bullish": 70.0, "bearish_below": 55.0}      # cut-offs are NDR's; the zone NAMES are ours
NDR_SRC = ("Ned Davis Research, 'Volatility Returns - What's Next?' webinar deck 2018-05-10, printed p.11 (PDF p.14), "
           "chart S75A (https://cdn2.hubspot.net/hubfs/1818132/EVP_ADVP201805101.pdf): U.S. Stock Market Model "
           "Composite cut-offs Above 70.0 / 55.0-70.0 / Below 55.0 (zone names ours)")


@register
class HandNDRComposite(_Calibrated):
    """Composite = 100 x (indicators agreeing with the trade) / (indicators voting). State indicators (trend, momentum,
    VWAP, 60-min, other markets) always vote (agree if > 0); event indicators (pattern families, swing breaks, momentum
    cross) vote only when they fire (include_events=True). Entry score = composite; exit score = 100 - composite.
    zones(X): our names on NDR's U.S. Stock Market Model cut-offs: bullish > 70, neutral 55-70, bearish < 55; exit
    zone = composite < 55."""
    name = "hand_ndr_composite"
    source = NDR_SRC

    def __init__(self, task="entry", include_events=True, **params):
        super().__init__(task=task, include_events=include_events, **params)
        self.include_events = bool(include_events)

    def _indicators(self, X):
        state = [c for c in NDR_STATE] + [c for c in X.columns if c.startswith("x_") and
                                          (c.endswith("_ret") or c.endswith("_ema_stack"))]
        events = list(NDR_EVENTS) if self.include_events else []
        return state, events

    def composite(self, X):
        state, events = self._indicators(X)
        n = len(X)
        agree = np.zeros(n)
        votes = np.zeros(n)
        for c in state:
            v = _num(X, c)
            ok = np.isfinite(v)
            votes += ok
            agree += ok & (v > 0)
        for c in events:
            v = _num(X, c)
            ok = np.isfinite(v) & (v != 0)
            votes += ok
            agree += ok & (v > 0)
        return np.where(votes > 0, 100.0 * agree / np.maximum(votes, 1), 50.0)

    def zones(self, X):
        c = self.composite(X)
        return pd.DataFrame({"composite": c, "zone_bullish": c > 70, "zone_neutral": (c >= 55) & (c <= 70),
                             "zone_bearish": c < 55, "entry_zone": c > 70, "exit_zone": c < 55}, index=X.index)

    def score(self, X, d=None):
        c = self.composite(X)
        return 100.0 - c if self.task == "exit" else c

    def weights_table(self, X_columns=None):
        state, events = self._indicators(pd.DataFrame(columns=self._table_columns(X_columns)))
        n = len(state) + len(events)
        sign = -1.0 if self.task == "exit" else 1.0
        rows = []
        for c in state:
            w = sign * 100.0 / n
            rows.append((c, w, w, f"{c} > 0 (with the trade) is one agreeing vote; always votes; points shown for a "
                         "row where every indicator votes", NDR_SRC))
        for c in events:
            w = sign * 100.0 / n
            rows.append((c, w, w, f"{c}: votes only when it fires (+1 agree / -1 disagree)", NDR_SRC))
        return self._table(rows)


# ============================================================================================================ 4 user
def spec_columns(markets=MARKETS):
    """Every feature column name (SPEC) the harness can pass: features._BASE_COLS + all x_ columns + exit trade state."""
    try:
        import features as F                                      # noqa: E402 (sibling module in ..)
        base = list(F._BASE_COLS)
        markets = tuple(getattr(F, "MARKETS", markets))
    except Exception:                                              # fallback: rebuild the SPEC list
        sys.path.insert(0, os.path.join(HERE, "..", "..", "signals"))
        pats = ["dragonfly_doji", "gravestone_doji", "hammer", "hanging_man", "inverted_hammer", "shooting_star",
                "marubozu", "engulfing", "harami", "piercing", "dark_cloud", "morning_evening_star",
                "three_soldiers_crows", "three_inside", "outside_bar", "pin_bar", "tweezer", "inside_bar_breakout",
                "nr7_breakout", "clv_extreme", "bar_80_20", "tall_trend_bar", "five_lower_lows_higher_highs",
                "clv5_extreme", "doji", "spinning_top", "inside_bar", "nr7"]
        base = ([f"pat_{p}" for p in pats] + [f"fam_{f}" for f in ("reversal", "continuation", "breakout", "closeloc",
                                                                     "exhaustion")]
                + [f"{c}_{k}" for k in (5, 10) for c in ("dist_swhi", "dist_swlo", "brk", "struct", "fibpos", "atfib")]
                + ["ema_stack", "ema20_slope", "dist_ema8", "dist_ema20", "dist_ema50", "above_ema20_share", "mom",
                   "mom_slope3", "mom_x100", "dist_vwap", "rng_rel", "body_frac", "clv", "vol_rel", "gap_open",
                   "day_range_rel", "day_ret"]
                + [f"tod_{t}" for t in ("asia", "europe", "uspre", "open", "midday", "close")]
                + [f"dow_{i}" for i in range(5)] + ["h1_ema_stack", "h1_mom", "h1_struct_5"])
    return base + [f"x_{m}_{s}" for m in markets for s in ("ret", "ema_stack")] + EXIT_STATE


def _column_note(c):
    if c in EXIT_STATE:
        return {"open_R": "exit rows only: open profit in R (risk units)", "mfe_R": "exit rows only: best open profit so far (R)",
                "mae_R": "exit rows only: worst open loss so far (R)", "bars_held": "exit rows only: bars in the trade",
                "dist_stop_R": "exit rows only: distance to the stop in R", "mins_to_1645": "exit rows only: minutes left to 16:45 ET"}[c]
    if c in ("pat_doji", "pat_spinning_top", "pat_inside_bar", "pat_nr7"):
        return "neutral pattern, 1 = present (no direction)"
    if c.startswith("pat_"):
        return "pattern: +1 fired WITH the trade, -1 fired AGAINST it, 0 none"
    if c.startswith("fam_"):
        return "pattern family: +1 with the trade, -1 against, 0 none"
    if c.startswith("tod_") or c.startswith("dow_"):
        return "time one-hot (1 = this bucket)"
    if c.startswith("atfib_"):
        return "1 if the close is within 0.15 bars of a 38/50/62% level of the latest swing leg"
    if c.startswith("x_"):
        return "other market's same bar: + = moving / trending with the trade"
    unsigned = {"rng_rel": "bar range / average bar", "body_frac": "body / range (0-1)", "vol_rel": "volume / average",
                "day_range_rel": "day range so far / average day range"}
    if c in unsigned:
        return unsigned[c] + " (no direction)"
    return "signed context (+ = with the trade), unit as in SPEC.md (distances in average bars)"


def write_user_template(path=USER_CSV, overwrite=False):
    """TEMPLATE with every signal/feature and blank weights. Never overwrites a filled file unless overwrite=True."""
    if os.path.exists(path) and not overwrite:
        return path
    pd.DataFrame({"signal": spec_columns(), "entry_weight": "", "exit_weight": "",
                  "note": [_column_note(c) for c in spec_columns()]}).to_csv(path, index=False)
    return path


@register
class HandUser(_Calibrated):
    """score = sum(weight_c * X[c]) with the user's weights (entry_weight or exit_weight column of user_weights.csv;
    NaN feature values count as 0). Weights are read in log-odds per unit of the oriented feature (points = weight /
    (ln2/20)); only their RELATIVE size and sign matter because Platt rescales. Blank -> HandWeightsMissing."""
    name = "hand_user"
    source = "user_weights.csv (the trader's own hand-set weights)"

    def __init__(self, task="entry", path=None, **params):
        super().__init__(task=task, path=path, **params)
        self.path = path or USER_CSV

    def load(self):
        col = "exit_weight" if self.task == "exit" else "entry_weight"
        if not os.path.exists(self.path):
            raise HandWeightsMissing(f"hand_user: {self.path} not found (run approach_hand.py --write-templates)")
        t = pd.read_csv(self.path, dtype=str, keep_default_na=False)
        for c in ("signal", col):
            if c not in t.columns:
                raise ValueError(f"hand_user: {self.path} needs columns signal, entry_weight, exit_weight, note")
        raw = t[col].str.strip()
        val = pd.to_numeric(raw.replace("", np.nan), errors="coerce")
        bad = raw.ne("") & val.isna()
        if bad.any():
            raise ValueError(f"hand_user: non-numeric {col} for {list(t.signal[bad])[:5]}")
        t["w"] = val
        t = t[t.w.notna() & (t.w != 0)]
        if t.empty:
            raise HandWeightsMissing(f"hand_user: no {col} filled in {self.path}; fill some weights or skip this scorer")
        if t.signal.duplicated().any():
            raise ValueError(f"hand_user: duplicated signals {list(t.signal[t.signal.duplicated()])}")
        self.weights_ = dict(zip(t.signal, t.w.astype(float)))
        self.notes_ = dict(zip(t.signal, t.get("note", pd.Series([""] * len(t)))))
        return self.weights_

    def _prepare(self, X, y, w, meta):
        """Check the weighted signals against X and SPEC before fitting, so a typo never drops a weight silently:
        unknown name (neither in X nor a SPEC column) -> ValueError; SPEC column absent from this X (e.g. an exit-state
        column on entry rows, or a market not passed) -> warning; no weighted signal in X at all -> HandWeightsMissing."""
        self.load()
        cols = set(X.columns)
        self.missing_ = [c for c in self.weights_ if c not in cols]
        if not self.missing_:
            return
        spec = set(spec_columns())
        unknown = [c for c in self.missing_ if c not in spec]
        if unknown:
            raise ValueError(f"hand_user: {self.task} weights in {self.path} name signals that are neither columns of X "
                             f"nor SPEC columns (typo?): {unknown}")
        if len(self.missing_) == len(self.weights_):
            raise HandWeightsMissing(f"hand_user: none of the {self.task} weighted signals {self.missing_} is a column "
                                     "of this X; nothing to score")
        warnings.warn(f"hand_user: {self.task} weights on {self.missing_} ignored: SPEC columns absent from this X",
                      stacklevel=3)

    def score(self, X, d=None):
        if not hasattr(self, "weights_"):
            self.load()
        s = np.zeros(len(X))
        for c, w in self.weights_.items():
            if c in X.columns:
                s += w * np.nan_to_num(_num(X, c))
        return s

    def weights_table(self):
        if not hasattr(self, "weights_"):
            try:
                self.load()
            except HandWeightsMissing:
                return None
        rows = [(c, w, w / LOGODDS_PER_POINT, self.notes_.get(c, "") or _column_note(c), f"user ({self.path})")
                for c, w in self.weights_.items()]
        return self._table(rows)


if __name__ == "__main__":
    if "--write-csv" in sys.argv or "--write-templates" in sys.argv:
        print("wrote", write_bulkowski_csv())
        print("wrote" if not os.path.exists(USER_CSV) or "--force" in sys.argv else "kept existing",
              write_user_template(overwrite="--force" in sys.argv))
    pd.set_option("display.width", 200, "display.max_colwidth", 60)
    print(bulkowski_table()[["pattern", "side", "rate_textbook", "basis", "weight_logodds", "weight_symmetric",
                             "overall_rank_of_103"]].to_string())
