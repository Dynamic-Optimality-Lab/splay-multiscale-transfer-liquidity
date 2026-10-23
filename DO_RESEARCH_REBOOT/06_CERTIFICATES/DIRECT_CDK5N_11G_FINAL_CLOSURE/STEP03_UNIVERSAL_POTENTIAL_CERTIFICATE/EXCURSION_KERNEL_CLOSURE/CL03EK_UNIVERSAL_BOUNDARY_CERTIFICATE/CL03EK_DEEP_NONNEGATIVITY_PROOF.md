# CL-03EK Deep Nonnegativity — OPEN (attempt documented, no foothold)

Attempted universal proof that every deep-only closed walk has w>=0.
Approaches tried: (1) rank/window potential restricted to deep states —
fails the same way as the refuted global candidates (no new mechanism,
and CEGIS-style fitting forbidden); (2) structural induction on deep
closed walks — no monotone measure available (ranks/depths move both
ways; core size nonincreasing only where CORE-01 applies, which does
not bound weight); (3) minimal-counterexample shape analysis — vacuous
without an instance; (4) single-vertex deep loops (no negative self-loop
argument does not extend: rotations always rewrite parent/child links,
but multi-edge returns are unconstrained). RESULT: unproved; the EXACT
missing lemma is a universal lower bound for deep closed walks, with no
candidate proof rule identified. H3 remains the first blocker.
