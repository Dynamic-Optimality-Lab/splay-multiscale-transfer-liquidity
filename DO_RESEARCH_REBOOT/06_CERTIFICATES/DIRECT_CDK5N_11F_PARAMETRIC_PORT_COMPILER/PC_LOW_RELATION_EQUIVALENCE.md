# PC_LOW_RELATION_EQUIVALENCE.md — G13/G14 (one parametric low relation; genuine weights)

## The relation (PC_LOW_COMPILER.py:build_low)
`L_{H,q}(s,t) <=> Exists xi [SourceStateValid /\ JointInventoryValid /\ MacroLegal_H /\
ExactPortReplay /\ BTransition_q /\ DestinationMatch]`, one shared circuit, same xi in every conjunct.
No per-macro circuits; no placement/signature enumeration. Weight `w = 2H-q` (signed 5-bit, exact).

## Equivalence evidence (V8)
138 grounded transitions: symbolic SAT ⟺ concrete replay (source H from evolving A-depths;
source q from pre-KEEP B-depth (C2); B-change genuine + marked terminal; destination A-shadow +
B-core + static mu/sig equalities). Zero mismatches. Skip census honest (wordshape/warmup/nongenuine/
fringe-anc/nontree/bev/apath/dst-nontree with counts in PC_LOW_EDGE_TESTS.json).

## Genuine weights (G14, C2)
q NEVER supplied: constrained from B-depth (`2q<=d<2q+2`, path-verified); DELETE q=0 (B identity).
5 certified genuine negative edges (H=1,q=3 E3-pattern; H=1,q=4 E4-pattern; full provenance:
universe/S/M/m0/x/trees/word/H/q/w/replay-agree/symbolic-SAT in PC_GENUINE_NEGATIVE_EDGES.json).
Synthetic q_terms tests recategorized diagnostic (prior campaign), not production evidence.

## Grammar (G02)
Effective H<=2 grammar proved (PC_EFFECTIVE_MACRO_GRAMMAR.md): root-run collapse lemma; <=5 events
(<=2 non-root + <=3 root-runs); KEEP/DELETE/multi-DELETE/zero-cost/nongenuine/terminal coverage with
boundary/cost/B-behavior preservation. Normalization as preprocessing (interpreter consumes
normalized words; collapse soundness proved, not assumed).

## Gates G13 (single relation compiled) + G14 (genuine weights): PASS.
