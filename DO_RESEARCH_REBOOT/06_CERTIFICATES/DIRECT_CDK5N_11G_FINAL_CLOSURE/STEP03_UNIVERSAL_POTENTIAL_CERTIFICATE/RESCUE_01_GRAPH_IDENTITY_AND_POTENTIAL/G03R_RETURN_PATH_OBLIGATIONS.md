# G03R Return-Path Obligations

For each of 4 witnessed negative edges `u -r-> v`, bounded simple-path search
(depth <= 5) for returns `v -c-> u`: none found in the sparse 40-edge sample
(`G03R_RETURN_PATH_RESULTS.json`). 11 constructed 2-leg continuations all join
but yield 0 two-cycles, 0 negative totals (`G03R_CHAINED_WALKS.json`). D3
symbolic `E_{-r} /\ Path_{<=k,<r}` queries NOT executed (Step-03 allocation
near cap; recorded as open obligation with exact query spec). D5
classification vacuous on current data (no abstract closed walk found):
TYPE-A/B/C/D undetermined for any future cycle. No abstract-only cycle is
evidence against the terminal inequality; any future verified negative
abstract cycle refutes only the full-graph potential objective.
