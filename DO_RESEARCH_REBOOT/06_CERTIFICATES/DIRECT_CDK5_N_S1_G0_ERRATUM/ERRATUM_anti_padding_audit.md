# Anti-padding + source-integrity audit (PROVED genuine)

- Exact closure both trees, both words (labeled serials). All keys present.
- Five KEEP keys genuine each (B-changing ≥1; pointer-trace verified).
- Core 9 at every state, both words. DELETEs freeze B (traced); A StepEvs exact.
- No a=0 accesses in INC (17 blocks = 17 accesses); CTL likewise per its replay.
- D5 (idx4, a=2) genuinely splays A before K1; K5 sees dA=1 (not 0 — no shadow).
  (Charter §14 prose "depth one" corrected to measured dA=1/a=1 for K5 — same
  StepEv cost; trajectory-change point stands: 15-access K5 had dA=5/a=3.)
- Removing DELETEs yields a different walk (different A depths/costs/blocks);
  no banked DELETE-removal invariance exists (ledger/domains checked) — none
  assumed either way. Not reducible to the failed 15-access control (different
  fourth block D4-vs-K9, different K5 costs, different closure states).
- Charter prose corrections (cost-neutral): K5 dA 1 (not 2); K5 predecessor is
  KEEP K9 (not DELETE D6) — exception therefore unambiguous; K9(idx11) a=2
  (not 1) — flips predicted K5-G5-FAIL to PASS, global exclusion via K3 kept.
