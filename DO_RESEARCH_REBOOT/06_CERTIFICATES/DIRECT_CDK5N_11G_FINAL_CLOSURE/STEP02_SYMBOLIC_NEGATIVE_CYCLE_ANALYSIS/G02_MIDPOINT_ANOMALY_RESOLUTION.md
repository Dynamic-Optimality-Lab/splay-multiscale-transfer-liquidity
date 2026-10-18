# G02_MIDPOINT_ANOMALY_RESOLUTION.md — Gate A verdict (A1-A5)

Reproduced on frozen stack: w=-4 UNSAT (tier2, ~10s, diagnosed: q=10 needs
B-depth>=20 impossible); w=-3 UNKNOWN (60s and 240s timeouts; exact formula,
solver stats recorded in G02_OM_WEIGHT_RESULTS.json — recorded obstruction, not
absence); w in {-2..1} SAT with extracted witnesses (267 model keys; witness
details retained); w in 2..6 SAT (marked q=0..4 correspondence). Classification:
no source-exactness defect found (predicates behave as compiled); SAT anomalous
edges are retained (never silently dropped); the w=-3 case is UNKNOWN with full
provenance. Contracted existence: E^H_w verified for w=3 by construction
(EOM+EMO with shared fiber + Tier-1); C1/C2 give the general argument;
anomalous weights follow the same construction (executed for w=3, stated for
the rest). A1: matrix reproduced. A2: witnesses extracted+checked where SAT.
A3: w=-3 unresolved-with-reason (NOT claimed absent). A4: contracted edges
follow by shared-fiber construction. A5: per-weight answers recorded.
