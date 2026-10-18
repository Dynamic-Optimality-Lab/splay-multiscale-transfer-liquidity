# G03R Resource Reconciliation (additive erratum to G03_RESOURCE_LEDGER.json)

The committed ledger zeroed usage despite executed runs. Reconciliation:
embedded `cpu_s` harvested from every Step-03/Rescue JSON (contracted
witnesses ~466s, cycle search 300s, rescue rebuild 164s, chains 208s,
piecewise falsify 525s, verifier 217s); pre-rescue falsify stdout lost with
the session — estimated ~3694s from the run record, flagged ESTIMATED, plus
entry/spotcheck ~1800s. No overlapping subruns summed (disjoint processes).
Step-03 total ~2.07h of 3.5h (headroom ~1.4h); campaign ~4.1h of 12h; 1.8h
reserve untouched. All figures conservative; uncertainty stated, not hidden.
(`G03R_RESOURCE_LEDGER.json`.)
