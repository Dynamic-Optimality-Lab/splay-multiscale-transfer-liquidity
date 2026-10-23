# DH-01 Substitution Weight Theorem (CONDITIONAL, proved)

ASSUME: (i) L3 (all deep low closed walks nonnegative); (ii) for every
deep high edge e, a low-only deep path P_e with w(P_e) <= w(e).
THEN: every deep closed walk C has w(C) >= 0. Proof: replace each high
edge by its P_e (endpoints match, all vertices stay deep by (ii));
result is a low-only deep closed walk C' with w(C') <= w(C) (additivity
+ dominance per edge); by L3, w(C') >= 0; hence w(C) >= 0. Exact for
arbitrary high counts/interleavings; preserves weights by construction;
no hidden liftability (endpoints match in the frozen graph; witnesses
need not compose). Both premises are OPEN (L3 open; substitution
unproved for every high edge). The theorem is valid; its hypotheses are
not discharged.
