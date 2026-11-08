# Buried cut: burial and return proved; two-credit release still open

The missing same-direction LL/RR cut-burial transfers are proved and
independently symbolically audited, with NO finite tests. The construction
does not infer the depth3 port from alpha or persist a private witness.

It adds three explicit public clauses to D_R:

    D_cut=max(D_R,1_S,2_T,2_L).

L is the observed port source with the other extreme-pair mark at LL/RR;
T is the resulting buried boundary with a shallow B return target; S is
the return state, where further marked keys may now be visible. For the
two smallest marked keys, the central source root is4/5; the largest-pair
dual uses3/4. Counting proves that these include all missing same-direction
port sources OUTSIDE E1 for those extreme marked pairs.

All original LOW edges from L and T are covered, including relevant H2
forms. S is covered when its FINAL debt is at most1. The former port can
become actual marked nodes in a fresh T witness: the return is still safe.
A new exact core-count/rotation argument handles its zero-weight release
into E1 at one credit, including the source-slot0 alias cases.

Each of the three ordered max operations preserves every previously valid
LOW inequality. Thus Q/R coverage stays valid. The inherited HIGH/h0 glue
gives finite walks>=-7 and full closed walks>=0 whenever LOW sources are
in Q,R,L,T or S with final debt<=1. Full147-O/127-M closure and SAME actual
midpoint/private scopes are retained. This is a restricted source theorem.

IMPORTANT LIMIT: general S debt2 releases are NOT proved. Nor are arbitrary
buried states without the T B-depth guard or other marked configurations.
T lies in E1, but its new debt2 theorem goes beyond the old one-credit
augmentation; the latter was never a proof of every E1 debt2 source.
Full M3/Dynamic Optimality remain OPEN; no negative cycle or new whole-
signature certificate is claimed.

See BURIED_CUT_THEOREM.md and PROOF_AUDIT.md for all public guards, complete
original LOW coverage, counter-scope and the independent audit. It verifies
16 universal four-core spine schemas with order-duals, arbitrary A terms,
alias-owner behavior and count/slack identities. No numerical core trees,
population instances, source roots or proposed labels were tested. Completed
semantic proofs/checks were reused, not replayed. The audit is not a full
formalization of the original compiler.

R1-R4/current caps, weak LE/G/unused fields, free high v and corrected h0
remain. All13616 pinned prior files and Git HEAD/tracked tree are
unchanged. New charged CPU=0.359375; cumulative=757.21875/7200s; remaining
6442.78125 including reserve5. New finite tests/source queries/roots=0.
