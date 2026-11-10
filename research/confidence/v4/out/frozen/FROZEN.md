# v4 frozen unsupervised models

Frozen 2026-11-09 16:14 local, fitted on DISCOVERY 2018-01-01..2021-12-31 only (ES+NQ+YM pooled). No forward return / target column was loaded or examined before freezing (load() reads feature columns only).

- states: GaussianMixture(k=12, full cov) on PCA(13 comps, 0.905 var) of 31 standardised, winsorised features
- motifs: KMeans(k=10) on 12-point path shapes, re-z-normalised per row
- k chosen by max min(seed ARI, market ARI), ties within 0.01 -> lower held-out BIC/SSE (out/kselect.csv)

| file | sha256 |
|---|---|
| state_prep.pkl | 48d675aa1879b28754a635656ef24e9db42da54be93171163339d79f526a1b9d |
| state_gmm.pkl | c84c4c4400ee6071cdae136ffdd4e6470b5e7039c99ca1e3f66bb2fd9f736bbe |
| shape_kmeans.pkl | 12e5f2c3cae06aa36305ee7edffd6f435631aec1169322f355069e2f525214ed |
| v4/discover.py (source) | eededf947170108cd89bbff5368382acdecb5ee66f44769206e39b758cf5c5dd |

## Notes (appended after freezing; the hashes above are unchanged)
- Correction: load() reads the whole parquet and then drops every non-feature column, so the target columns were in memory for a moment. None was used, summarised or printed.
- A first run at 16:08 had a bug: clock_min was treated as minutes since 18:00 when it is the ET minute of the day. That run's frozen files were overwritten and are not valid. The files above come from the corrected run at 16:14. Both runs are in out/trials.csv.
- After freezing, the motif descriptions in out/discovery_motifs.csv were rewritten by hand from the centroids, because the automatic labels were too coarse. The automatic labels are kept in the words_auto column. The models are unchanged.
