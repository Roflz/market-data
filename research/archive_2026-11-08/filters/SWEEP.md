# Section 15, W sweep: which wide-stop overnight-break trades to skip (written 2026-11-08, before results)

Research sweep requested by the trader after the single pre-registered W test was set up. Base: the live overnight-break
trades in chosen_models_trades.csv (1,731 trades, $23,214 at 1 MNQ micro after costs). Judge in net $ at a FIXED
1 micro (prop-firm account), plus max drawdown and worst day of the overnight-break model alone and of the 3-model book.
Every decision must use only information known at the trade's entry.

## Width measures (stop distance = 2 x ATR at the signal, exactly as chosen_models.overnight_break / exits_engine)
M1  stop as a share of raw entry price (as in rule W)
M2  stop in points relative to the median stop (points) of the live overnight-break trades in the lookback window
    (same as M1 up to price drift; include it only if it differs materially from M1; otherwise say so and drop it)
M3  dollar risk of 1 micro = stop points x $2 + $2 cost. Fixed dollar thresholds, no lookback.
M4  volatility shock: the signal bar's ATR divided by the median ATR of the same instrument over the previous 60
    sessions at any time of day (from the 5-minute data exits_engine uses), i.e. "today is unusually volatile"

## Variants
For M1 (and M2 if kept) and M4: skip trades above the q-th percentile of the measure among the live trades in the
previous L trading days (strictly before the trade date), q in {50, 67, 80, 90}, L in {125, 250, 500}; no skipping
until L days of history exist. That is 4 x 3 = 12 variants per measure.
For M3: skip if 1-micro dollar risk > X, X in {$75, $100, $150, $200, $250, $300}. (Mostly affects 2020 onward,
because NQ was cheap before; report the share of trades skipped by year.)
The pre-registered rule W (M1, q=67, L=250) is one of the variants; report it separately as the primary.

## For every variant report
trades removed (count, share), removed $ total and per era (2010-13, 2014-17, 2018-20, 2021-23, 2024-26), kept $,
$ per trade kept vs removed with Welch t, max drawdown and worst day (model alone and 3-model book), the same at
2 ticks per fill ($1 less per trade), and a RANDOM-SKIP control: remove the same number of trades at random from the
same eligible trades (1,000 draws, seed 12345) and give the percentile of the variant's removed $ in that
distribution (a good skip rule removes trades that lose MORE than random removals: low percentile).

## Selection honesty
1. Family-wise control: for each of the 1,000 random draws, take the best (most negative) removed-$ across all variants
   when each variant is replaced by a random removal of the same count; report where the actual best variant falls.
2. Walk-forward: from 2013 on, each year use the variant with the best cumulative (kept $ - all $) in all earlier
   years (ties -> no filter), and compare that year-by-year book with no filter.
A variant is worth adopting only if: removed $ < 0 in both 2010-2017 and 2018-2026, random-skip percentile <= 5%,
the family-wise check puts the best variant at or below the 5th percentile, and the walk-forward beats no filter.
