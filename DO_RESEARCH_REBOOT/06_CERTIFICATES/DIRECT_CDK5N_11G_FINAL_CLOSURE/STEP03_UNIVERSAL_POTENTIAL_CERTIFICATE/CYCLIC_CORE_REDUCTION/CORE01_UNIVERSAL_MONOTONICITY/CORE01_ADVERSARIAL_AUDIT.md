# CORE-01 Adversarial Audit (Gate H/J3, existing evidence only)

Tested for rho(t) > rho(s): 38 seeds + 40 ledger + 18 falsify + 2 CL-02
FULL + 6 SR-02C counterexamples + 4 CL-02 feature excursions = 108
endpoints-pairs with core_size on both sides: ZERO violations. Inclusion
C(t) subset C(s) on 48 full-state edges (40 ledger + 6 SR-02C + 2 CL-02):
ZERO violations. Killers audited: rank-jump/marked-jump/E4/deep-chain
edges all satisfy monotonicity (rank/depth move WITHOUT growing marked
ancestor closure — consistent with the rotation analysis: mass moves,
ancestry of marked shrinks-or-holds). Nongenuine-key and DELETE edges in
samples: consistent. No counterexample discarded (none found). The hole
remains theoretical: predicate-admitted but uncertified.
