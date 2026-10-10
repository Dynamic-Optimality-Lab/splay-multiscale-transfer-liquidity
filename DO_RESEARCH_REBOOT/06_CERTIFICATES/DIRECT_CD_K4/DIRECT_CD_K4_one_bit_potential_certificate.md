# One-bit potential certificate (PROVED: 68,876/68,876, both engines)

**Frozen potential.** η_M(U) = 1[max_{z∈M} d_U(z) = 6]; inequality per marked
access x in core U: ⌊d_U(x)/2⌋ − 2·1[x≠root(U)] + η_M(U') − η_M(U) ≤ 0,
U'=S_x(U). Coefficients frozen at Gate 0; unmodified after testing.

**Enumeration (over-approximation, hence sound).** All Catalan BST shapes on
keys 1..n (n=4..7 via shapes_of: 14/42/132/429), all C(n,4) marked 4-subsets,
all 4 marked accesses, both engines with full tree-equality + depth agreement:

| n | shapes | subsets | ×accesses | transitions |
|---|---|---|---|---|
| 4 | 14 | 1 | 4 | 56 |
| 5 | 42 | 5 | 4 | 840 |
| 6 | 132 | 15 | 4 | 7,920 |
| 7 | 429 | 35 | 4 | 60,060 |
| total | | | | **68,876** |

Every enumerated shape is a valid core superset (real cores are ancestor-closed
rooted BSTs; any unrealizable shape only strengthens the certificate).

**Result.** 68,876 transitions checked, **0 violations**, 0 engine mismatches
(pointer `splay_A` vs tuple `S.trace`, exact integer arithmetic, deterministic
order). Positive raw-weight transitions at n=7: **1,280**, all covered by the
η term (matches prior screening exactly). Nontrivial depth-six events occur
(Control A: q=3 at d=6) and are paid by η-drops. Certificate:
`DIRECT_CD_K4_finite_verification.json` (+ verifier script + log).

**Status.** The certificate is a universal proof component together with the
all-size reduction (§5/§6: every real B-step projects to a certified
core transition). Alone it would not suffice; combined it does.
