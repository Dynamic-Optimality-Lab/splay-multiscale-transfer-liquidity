# G03R Feature-Semantic Audit

All 16 features total on 80 real endpoints (no None); pure functions of the
147 abstract pins (only hit for "witness" is the header comment disclaiming
witness use); sentinels (`kl/kr==2`, ref 19) excluded; unreachable targets
return None (never observed on valid states). `core_size` = ancestor-closure
of marked S-indices: observed sizes {5..9} are NORMAL (closure of 5 marked
nodes), resolving the old "<9" worry — it was never a full-core claim.
`b_rank_*`/`a_rank_*` are valid G-star vertex functions (exact within the
frozen window) but NOT full-tree Sleator-Tarjan ranks; any ST-classic reading
is invalid. No witness data smuggled into Phi inputs. (`G03R_FEATURE_MATRIX.json`.)
