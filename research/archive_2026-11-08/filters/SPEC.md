# Section 15: filters for the live breakouts (pre-registered 2026-11-08, before any results)

The trader runs a prop-firm account at a FIXED size. Judge everything in net $ at 1 MNQ micro (usd column of
chosen_models_trades.csv, after costs), plus max drawdown and worst day. A filter only removes trades from the live
model; entries, stops, exits and the existing skip rules are unchanged. Base trades: chosen_models_trades.csv in the
project (overnight_break: 1,731 trades; opening_range: 3,509 trades), built by chosen_models.py.

## W. Skip wide-stop overnight breaks
Stop width = the trade's stop distance in points / the raw entry price (known at entry). Recompute stop distance and
raw entry exactly as chosen_models.overnight_break does (exits_engine.run(..., "hold", k0=2.0) gives R_pts and bar;
raw price = back-adjusted price minus the session's back-adjustment, as chosen_models does for bp). Skip a trade if its
width is above the 67th percentile of the widths of ALL overnight-break trades (of the live model, i.e. after the
cash-day / expiry / R1 filters) dated in the previous 250 trading days, strictly before the trade's date. No trade is
skipped until 250 trading days of history exist (those trades are kept).

## T. Trend-day filters for the opening range (each tested alone; keep the trade only when the filter says keep)
All inputs are known at 9:35 ET on the trade day.
- T1 trend agreement: keep only if the trade direction equals the 20-day trend direction, using exactly the trend
  definition the overnight-break model uses (read setup_rule.py / exits_compare.py to find it; use its value as known
  at the 9:35 decision, i.e. computed from data before 9:35).
- T2 gap agreement: gap = today's 9:30 open minus the previous cash session's 16:00 close (the close of its 15:59 bar,
  or 12:59 on early-close days). Use additively back-adjusted prices (data/daily_sessions_NQ.pkl open_adj/close_adj or
  equivalent) so a contract roll does not create a fake gap. Keep only if sign(gap) equals the trade direction; a zero
  or missing gap counts as disagree (trade removed).
- T3 strong open: first-candle range = max High - min Low of the 9:30-9:34 one-minute bars. Keep only if today's range
  >= the median of the previous 20 cash sessions' first-candle ranges (in points). Fewer than 20 prior sessions: keep.
- T4 quiet night: overnight range = max High - min Low of the one-minute bars from 18:00 ET the prior evening through
  the 9:29 bar. Keep only if today's overnight range <= the median of the previous 20 cash sessions' overnight ranges
  (in points). Fewer than 20 prior sessions: keep.

## Pass rule (each filter separately)
(a) the removed trades lose money in total over the full period AND in 2010-2017 AND in 2018-2026;
(b) kept trades beat removed trades per trade: Welch t on net $ per trade >= 2.0 for W; >= 2.5 for each of T1-T4
    (four tries, Holm-adjusted);
(c) the filtered model's max drawdown (on daily net $, that model alone) and worst day are no worse than the unfiltered
    model's.
Report only: per era (2010-13, 2014-17, 2018-20, 2021-23, 2024-26), 2023-2026, per year, share of trades removed,
the same with 2 ticks per fill (subtract one extra tick per side, i.e. 0.5 NQ point = $1 per trade, from every trade),
and the effect on the combined 3-model book (net $, max drawdown, worst day).
