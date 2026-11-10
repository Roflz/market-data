"""Event-level comparison of implementer A and B outputs (reads their CSVs only)."""
import numpy as np
import pandas as pd

D = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/caltests"
A, B = f"{D}/A", f"{D}/B"


def t(x):
    x = np.asarray(x, float)
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


pairs = [
    ("1-primary", "events_1_primary.csv", "t1_primary_events.csv", "month", "month"),
    ("1a", "events_1a.csv", "t1a_events.csv", "month", "month"),
    ("1b", "events_1b.csv", "t1b_events.csv", "month", "month"),
    ("2-primary", "events_2_primary.csv", "t2_2-primary_events.csv", "date", "E"),
    ("2a", "events_2a.csv", "t2_2a_events.csv", "date", "E"),
    ("3-primary", "events_3_primary.csv", "t3_3-primary_events.csv", "month", "month"),
    ("3a", "events_3a.csv", "t3_3a_events.csv", "month", "month"),
    ("3b", "events_3b.csv", "t3_3b_events.csv", "month", "month"),
    ("4-primary", "events_4_primary.csv", "t4_4-primary_events.csv", "month", "month"),
    ("4a", "events_4a.csv", "t4_4a_events.csv", "month", "month"),
]
for tid, fa, fb, ka, kb in pairs:
    a = pd.read_csv(f"{A}/{fa}")
    b = pd.read_csv(f"{B}/{fb}")
    a["k"] = a[ka].astype(str).str[:10]
    b["k"] = b[kb].astype(str).str[:10]
    m = a.merge(b, on="k", how="outer", suffixes=("_A", "_B"), indicator=True)
    only = m[m._merge != "both"]
    both = m[m._merge == "both"]
    dn = np.abs(both.net_usd_A - both.net_usd_B)
    dbp = np.abs(both.net_bp_A - both.net_bp_B)
    print(f"{tid}: A n={len(a)} B n={len(b)} only-one-side={len(only)} | max|net$ diff|={dn.max():.6f} "
          f"n events with net$ diff>1e-6: {(dn > 1e-6).sum()} | max|net bp diff|={dbp.max():.6f}")
    if (dn > 1e-6).sum():
        print("   differing events:", list(both.k[dn > 1e-6])[:30])
    # excess comparisons where present
    if "ex_gross_bp" in a.columns and "ex_bp" in b.columns:
        print(f"   A mean ex_gross_bp {a.ex_gross_bp.mean():.4f} t {t(a.ex_gross_bp):.3f}; "
              f"B mean ex_bp {b.ex_bp.mean():.4f} t {t(b.ex_bp):.3f}; B ex_usd mean {b.ex_usd.mean():.3f} t {t(b.ex_usd):.3f}")
        print(f"   A net-excess bp t {t(a.ex_net_bp):.3f}; B net-excess bp t {t(b.netex_bp):.3f}; "
              f"B net-excess $ t {t(b.netex_usd):.3f}")
    if tid.startswith("1"):
        print(f"   net$ t {t(a.net_usd):.3f}; net bp t {t(a.net_bp):.3f}")
    if tid.startswith("3"):
        pa = a[a.post]
        pb = b[pd.to_datetime(b.key) >= "2014-01-01"]
        print(f"   post-paper n A {len(pa)} B {len(pb)}: A net-ex bp {pa.ex_net_bp.mean():.3f} t {t(pa.ex_net_bp):.3f}; "
              f"B net-ex bp {pb.netex_bp.mean():.3f} t {t(pb.netex_bp):.3f}; B net-ex $ {pb.netex_usd.mean():.3f} t {t(pb.netex_usd):.3f}")
        bench_diff = (both.bench_bp_A - both.bench_bp_B).abs()
        print(f"   bench bp max diff {bench_diff.max():.4f}; bench_n A vs B differ on {(both.bench_n_A != both.bench_n_B).sum()} events")
    if tid == "1b":
        ca = a.cal_T4.values
        cb = b.cal_m4.values
        print(f"   Cal_T-4 agreement A vs B: {(ca == cb).mean():.3f}")

# 1b cross-check: A's NQ-signal side calc vs B's headline; B's ES-signal sensitivity vs A's headline
a1 = pd.read_csv(f"{A}/events_1_primary.csv")
b1 = pd.read_csv(f"{B}/t1_primary_events.csv")
print("T1 primary Cal_T-4 agreement A vs B:", (a1.cal_T4.values == b1.cal_m4.values).mean())
# test 4 overnight leg t: bp vs $
b4 = pd.read_csv(f"{B}/t4_4-primary_events.csv")
print(f"T4 overnight leg: mean bp {b4.on_bp.mean():.3f} t(bp) {t(b4.on_bp):.3f}; mean $ {b4.on_usd.mean():.3f} t($) {t(b4.on_usd):.3f}")
print(f"T4 intraday leg: mean bp {b4.intra_bp.mean():.3f} t(bp) {t(b4.intra_bp):.3f}; mean $ {b4.intra_usd.mean():.3f} t($) {t(b4.intra_usd):.3f}")
