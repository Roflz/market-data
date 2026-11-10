# Reverse-engineered big moves: FROZEN candidates (written before any 2018-2025H1 test)

Frozen at: 2026-11-09 14:56 MST. Code: `v3/signal_lab/reverse_signals.py` (sha256 2ace4cd40029bdfd...), metrics `v3/signal_lab/reverse_feats.py` (sha256 b24be36dacb0d7d5...).
Discovery: `reverse_discover.py` on sessions 2010-2017 only, ES and NQ 15-min bars (YM has no data before 2018, so it is a fully fresh market in the test). Raw table: `out/reverse/discovery_2010_17.csv`, log `out/reverse_discover.log`.

## How the discovery was done
- Big moves (per market): the top 5% of next-1-hour moves (and of moves to 16:45) for each 15-minute time of day, measured in average bars (R20); strong trend days = the 09:30-16:45 move in the top 15% of days AND the net move at least 60% of the 09:30-16:45 high-low range.
- Each metric was compared at the bar BEFORE the move with ordinary bars of the same market, same 15-minute time slot and same volatility decile (metric standardised inside each such group).
- Every number was also computed for each year 2010-2017 separately; "t" below is the year-to-year t-value (8 years), "yrs" the number of years with the same sign.

## What the discovery showed (plain words)
1. **Before big moves, price was already moving the SAME way** (EMA8 distance, last hour, new high/low of day): big up hours followed bars that were stretched up, big down hours followed bars stretched down (ES t 6-7, NQ t 6-8, 8/8 years). **But over ALL bars the same metrics point the OTHER way** (a mild 1-hour fade, 8/8 years in both markets). This is the hindsight trap the user worried about: what you see before big moves is not what pays on average. Tested as the fade (the side that holds on all bars).
2. **"A big move is coming" is easy to see; its direction is not.** A big last bar (t 15 ES / 12 NQ) and a volume surge vs the usual for that time of day (t 18 / 7) come before bigger next-hour moves; a narrowest-of-7 bar comes before SMALLER moves (t -9 / -16; no "squeeze" breakout). None of these says up or down (direction t about 1).
3. **Trend days:** at 09:30, recent average bar vs the last 100 bars was LOW before up trend days and HIGH before down trend days (ES t -8.0, 7/8 years; NQ t -3.2, 6/8), even inside the same volatility decile.
4. Outside bars were followed by drift UP to 16:45 (IC t 3.9 ES 8/8 yrs, 4.6 NQ 7/8), inside bars by drift DOWN (t -4.4 ES, -6.4 NQ). No story for this; included because it was consistent in both markets.

## The 10 frozen candidates (sign and hold fixed now)
| # | Name | What it is | Claim | Expected sign | Primary hold | Discovery evidence 2010-17 (ES / NQ) |
|---|---|---|---|---|---|---|
| 1 | rev_stretch_ema8 | close minus EMA8, in average bars | direction | negative (fade) | 1 hour | all-bar IC t -8.4 / -5.8, 8/8 yrs each |
| 2 | rev_last_hour | last hour's move, in average bars | direction | negative (fade) | 1 hour | IC t -10.7 / -5.4, 8/8 yrs |
| 3 | rev_new_day_extreme | +1 new high of day, -1 new low | direction | negative (fade) | 1 hour | IC t -7.9 / -5.0 |
| 4 | rev_surge_fade | EMA8 distance only when volume >= 1.65x usual | direction | negative (fade) | 1 hour | IC t -7.8 / -4.7 (0/8 yrs positive) |
| 5 | rev_outside_up_eod | outside bar | direction | positive (up) | to 16:45 | IC t 3.9 / 4.6 |
| 6 | rev_inside_down_eod | inside bar | direction | negative (down) | to 16:45 | IC t -4.4 / -6.4 |
| 7 | rev_volratio_0930 | at 09:30: avg bar last 20 / last 100 | direction | negative | to 16:45 | trend-day t -8.0 / -3.2 |
| 8 | rev_bigbar_size | last bar range / average bar | size | bigger | 1 hour | big-move t +14.7 / +11.8 |
| 9 | rev_volsurge_size | volume vs usual for the time of day | size | bigger | 1 hour | big-move t +17.6 / +6.7 |
| 10 | rev_nr7_quiet | narrowest bar of last 7 | size | smaller | 1 hour | big-move t -8.7 / -16.1 |

## Test rule (fixed before the test)
- ONE batch: the 10 candidates x ES, NQ, YM on 15-minute bars, sessions 2018-01-01 to 2025-06-30 only (the discovery years are not in the panels), signal lab v1.1 defaults (6 holds per metric with Bonferroni, session bootstrap, re-pairing placebo, Benjamini-Yekutieli false-discovery control over all 60 direction+size tests, replication across alternate calendar quarters, look-ahead truncation check on every function).
- A DIRECTION candidate survives in a market if the lab says CONFIRMED and the effect has the expected sign; it is worth trading only if the class is REAL & TRADABLE (cautious $ edge per micro per trade above the round-trip cost).
- A SIZE candidate survives if the size verdict is CONFIRMED with the expected sign.
- The primary-hold effect is also reported. Nothing is re-tuned after the test.
