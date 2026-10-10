# DIRECT-CWC technical audit: ECT construction, refutation, frontier

## A–D. Safety, pipeline, costs, flux

coarse-double-branch @88d3007; writes confined; AJ–AS/DIRECT-U1 preserved.
KEEP/DELETE/a/q/no-op costs per source. Depth-flux + parity identities
re-verified as bookkeeping (code-level: token counts |B|=Q, 2|E|=2A asserted
on every build); ancestor-pair cycle cancellation holds per ordered pair.
None of these is a sign theorem (N1/N2 ✓).

## E–G. Frozen tokens, epochs, contacts (PASS1/2)

Spec v1.0 hashed 6381feb0… BEFORE testing; v1.1 (087524d6…) amends ONLY the
root-first path-indexing convention (§18 allowance) after a caught
implementation indexing error — pairs/eligibility mathematically identical,
both hashes preserved. PASS1: pushed-pair grouping == consecutive pre-access
path pairs on all traces (asserted per double; zig parity asserted); mirror A
splay serial-equal to source on every access; RotA sizes 2/3 asserted.
PASS2: edge⇒predicate re-verified; rotation invariance PASS (identical flow
on rotated basepoint); capacities exact; no post-hoc edges.

## H. Cut-expansion (REFUTED — no proof attempted past refutation)

PASS4 on 3 U1 gaps (frozen graph, deterministic Dinic): 46/46, 44/44 full
flows (finite success, correctly NOT promoted §15/N16/N26) vs 43/44 DEFICIENT
on walk 3. Min-cut S={tok16} (access 8 = K15, pushed pair (7,6), q=3 genuine),
N(S)=∅: 1>0. Independently verified by separate code path from fresh replay:
H-timelines, births (5 and 6), windows ({6,7,8},{7,8}), exhaustive C1/C2
recheck over all in-window StepEvs = 0 eligible events. Mechanism: epochs born
just before death leave almost no access window; keys 7/6 never rotated nor
net-ancestry-owned therein. Walk W=−96 (Coarse-Double intact on this walk).

## I–J. Regressions and conclusion

PASS5 skipped per charter (candidate did not survive). No supplementary
corpus run (would not change the verdict). No positive-weight walk found or
claimed (N20 ✓). ECT cut-expansion conjecture: FALSE as stated. Failure mode:
overly strict contact incidence (N18 anticipated) — NOT a Coarse-Double
counterexample (N19 ✓). Universal Coarse-Double: OPEN. Proof obligations
P1–P16 (construction/correctness) PASS; P17 REFUTED; P18–P20 vacuous.
Controls N1–N30 honored; no redesign (N24), no new architecture (N25),
no finite-to-universal leap (N26), AJ–AS/U1 untouched (N27), no 26AT (N28).
