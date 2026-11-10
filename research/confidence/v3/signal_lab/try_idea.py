"""
v3/signal_lab/try_idea.py - test ONE new idea (or a few) with the signal lab in one command.

    cd research/confidence
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3:v3/signal_lab \
      OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3 nice -n 5 \
      python3 v3/signal_lab/try_idea.py v3/signal_lab/ideas/example_idea.py [ES,NQ,YM] [15,60] [nolog]

The idea file defines METRICS = {name: dict(fn=function(bars) -> Series, kind=..., desc=...)}, exactly like
ideas/example_idea.py. `bars` has columns O H L C V, ema8 ema20 ema50, mom14, vwap, atr14, plus session columns
(seg, run, session); a value must be known at that bar's CLOSE. kind: 'continuous' (any number),
'state' (a few ordered levels), 'event' (0/1), or 'sided' (+1 long / -1 short / 0 nothing).

Defaults: ES, NQ, YM on 15- and 60-min bars (the calibrated combinations; 5-min is uncalibrated and needs the shared
heavy lock). Writes impact cards to out/ideas/<idea file name>/cards/<metric>.md and a one-row-per-panel
batch_summary.csv. Every metric x market x timeframe is logged to research/confidence/out/trials.csv (module
v3-lab-idea-<file name>) unless 'nolog' is given, so the data-snooping tally stays honest.
Each metric is look-ahead checked (cut at 40 of its own signal bars + 60 random bars); a failure makes every
verdict INVALID. Holdout: harness.bars only returns bars before 2025-06-30 18:00 ET.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab as L  # noqa: E402


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    path = argv[0]
    rest = [a for a in argv[1:] if a != "nolog"]
    markets = tuple(rest[0].split(",")) if len(rest) > 0 else ("ES", "NQ", "YM")
    tfs = tuple(int(x) for x in rest[1].split(",")) if len(rest) > 1 else (15, 60)
    stem = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(f"idea_{stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    metrics = mod.METRICS
    out_dir = os.path.join(L.OUT, "ideas", stem)
    if 5 in tfs:
        print("[try_idea] note: 5-min verdicts are UNCALIBRATED and 5-min panels need ~2.5 GB: run under the heavy flock")
    batch, res = L.evaluate_many(metrics, markets=markets, tfs=tfs, out_dir=out_dir,
                                 log_tag=None if "nolog" in argv else f"idea-{stem}")
    cols = [c for c in ["metric", "market", "tf", "lookahead", "best_dir", "dir_effect", "q_dir", "dir_verdict",
                        "dir_class", "best_size", "size_pct", "q_size", "size_verdict"] if c in batch.columns]
    print(batch[cols].to_string())
    print(f"\n[try_idea] impact cards: {os.path.join(out_dir, 'cards')}")


if __name__ == "__main__":
    main(sys.argv[1:])
