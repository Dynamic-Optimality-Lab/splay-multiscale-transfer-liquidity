# Source-exact positive prefix; the recurrent-cycle gate remains unmet

The requested non-scanning A/B cycle with G_B,J_B>=5, exactly two one-StepEv resets and E>C_D remains OPEN. A positive-excess source prefix can be derived exactly, but it does not supply recurrent amplification or closure. The cycle proposal fails rules2–4 of the four-rule gate in RG00, so no new finite-search campaign was launched.

## Exact source calculation

The authoritative tuple source is python/independent/splay.py, functions _rebuild and trace. Its parent-first RR frame is

    g(A,p(B,x(C,D))) -> x(p(g(A,B),C),D).

The independent pointer source python/liquidity/legacy_embedding.py implements the same order by left-rotating g and then p. Both source definitions were read for this algebraic derivation. No engine was imported or replayed in this run.

Let F be any finite BST whose keys exceed7, possibly empty. Start diagonally with the right chain on1,...,7 and F attached as the right child of7. For the thirteen-key example, take F=R_[8,13]. Write k(L,R) for a node, a bare key for a leaf node, and . for empty.

Perform

    D3, D5, K7.

On A, the two DELETEs and the KEEP each apply a single RR frame at depth two:

    A0=1(.,2(.,3(.,4(.,5(.,6(.,7(.,F))))))),
    A1=3(2(1,.),4(.,5(.,6(.,7(.,F))))),
    A2=5(4(3(2(1,.),.),.),6(.,7(.,F))),
    A3=7(6(5(4(3(2(1,.),.),.),.),.),F).

Equivalently A1 has root3 and its complete left vine1..2, A2 has root5 and left vine1..4, and A3 has root7 and left vine1..6. The three A event intervals are RR[1,3], RR[3,5], RR[5,7]. Each is exactly one grouped StepEv, with no final zig.

B is unchanged during both DELETEs. Its first KEEP7 still has input depth six. Rebuilding the right path bottom-up gives the three events

    RR[5,7], RR[3,7], RR[1,7]

and the exact output

    B3=7(2(1,4(3,6(5,.))),F).

The two DELETE leaders are pure: their keys3 and5 differ from the following action keys5 and7, and each action changes A's root. Their prefix capacity is therefore two distinct two-unit pools, totaling four. At the KEEP leader,

    a_A=1, q_B=3, q_B-2a_A=1.

Thus this reachable open prefix has one positive block. Its aggregate A cost is3 and its B demand is3; it is not a Coarse-Double counterexample. The scalar positive prefix excess is1, below the four-unit pure reset capacity. The closed-walk minimum-cut funding lemma cannot be applied to an open prefix, and early pools are not silently banked for future demands.

The output pair differs from the input: both output roots are7, whereas both initial roots are1. The output A/B trees also differ, because A3's left-subtree root is6 and B3's is2. Consequently this is neither a closed A/B cycle nor a proof about its cyclic J_B. The cycle quantities G_B and J_B remain unassigned. The single KEEP's raw max(q-2,0) contribution is1; it cannot be promoted to a five-unit recurrent budget.

## All-size scope and reflection

The derivation is valid for every F because no query enters it and all RR formulas preserve the same attached fringe. In particular it holds for every right vine R_n with n>=7 by choosing F=R_[8,n]. This is an algebraic arbitrary-fringe proof, not a fit across finite sizes.

For the vine case, reflect keys by k->n+1-k and swap left/right. The mirrored prefix from L_n is

    D_(n-2), D_(n-4), K_(n-6).

Its A events are the corresponding three LL frames and its B input KEEP depth is again six, giving a_A=1,q_B=3 and positive prefix excess one. RR event intervals [a,b] become LL[n+1-b,n+1-a]. This establishes both orientations directly from the source formulas. No independent runtime pointer replay is claimed.

Status of this local calculation: PROVED—RESTRICTED DOMAIN, for the displayed reachable prefix and arbitrary outer fringe. Verification attribute: derived algebraically from both source definitions; no new runtime corpus or finite-source certificate was generated.

## Why the immediate continuations do not amplify it

After K7, another K7 is a root no-op on both A and B. It creates no new A event, B double or positive block. Repeating it cannot multiply the one-unit excess.

After the first prefix, A is7(L_[1,6],F). The next DELETE3 would follow7->6->5->4->3, depth four, and cost two grouped StepEvs. Literal repetition of D3,D5,K7 therefore does not preserve the one-StepEv reset property. It also adds two reset occurrences per copy, violating the exact-two-reset requirement even if every copied cost had remained one. Reusing a fresh diagonal prefix in each copy would supply external state/work outside the proposed cycle.

A suitable shared-KEEP continuation would need to produce enough further positive excess, attain both B thresholds and return a valid recurrent pair without further pure work or a scan-tail obstruction. No exact continuation identity is established here. Requiring that an unspecified word perform all those tasks is the original open joint-cycle problem restricted to this seed, not a new independent premise or a completed proof.

## Final status and preservation

The positive local seed is retained, while the requested recurrent construction remains OPEN. The gate requires stopping rather than launching another unsupported clock/word enumeration. No general two-reset impossibility, new CD subclass, FI-only coverage, cycle G/J value or completed amplification mechanism is claimed.

Only file/Git integrity auditing was executed: zero new splay source calls, zero finite runtime cases, zero fits, zero new word classes and zero old status-writer runs. All813 earlier/source files and all125 Stage11G files with exact inventory are unchanged, as are branch/HEAD and clean tracked status. Matching-terminal remains FROZEN. No automatic successor was launched.
