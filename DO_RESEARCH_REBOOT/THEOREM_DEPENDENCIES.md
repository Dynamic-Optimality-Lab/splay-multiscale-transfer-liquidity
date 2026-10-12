# Dependency graph and proof-state labels

Edges below are sufficient mathematical implications, not equivalences unless stated. A proved implication with an open premise does not mark its destination proved.

```mermaid
flowchart TD
  PA[Pair Access encoding: PROVED] --> CD[COARSE-DOUBLE: OPEN]
  AL1[One-splay displacement +2: PROVED] --> ALG[26AL-G/S delayed repayment: PROVED conditional]
  ALG --> CDJ[Q_B<=2A on 26AJ/26AK/26AL-G closed classes: PROVED restricted]
  CDJ -.->|partial evidence only, no implication| CD
  J[One globally admissible J: OPEN] --> SELF[J-SELF: OPEN]
  J --> ROW[Adjusted ROW-DIAMETER: OPEN]
  SC[SAME-CHILD: OPEN] --> ROW
  CC[Cross-child and root-child: OPEN] --> ROW
  ER[REBOOT-01 erasure: PROVED restricted] --> BASE[Empty-sibling bases: OPEN]
  BASE --> SC
  OTHER[Unequal depth / unequal coefficient cases: OPEN] --> SC
  SELF --> RES[Residual edge bound: CONDITIONAL]
  ROW --> RES
  RES --> CD
  CD --> SUM[B <= 3A: CONDITIONAL]
  Z[C.ZIG: PROVED mathematical] --> SUM
  SUM --> EX[Cycle excision: proved implication]
  EX --> PRE[E_B <= 3 S_A + g: CONDITIONAL]
  PRE --> LT[LT(Y) <= 7 LT(X) + 2g: CONDITIONAL]
  LT --> RED[Levy-Tarjan v3 Thm 4.3: established]
  RED --> DO[Dynamic Optimality: OPEN]
```

Arbitrary-depth SAME-CHILD and its bases are subdivisions of the same global row obligation, not successive independent existence problems. The coefficient identity proved for REBOOT-01 is exact for arbitrary J and thus adds no witness premise. For other pairs, the same insertion identity produces different coordinates and does not cancel automatically.

Parallel historical branches (GC-STATIC, Hall routing, U4/overflow, finite Bellman-Ford) are optional sufficient routes or experiments. Their results are not automatically prerequisites of J4. The graph does not claim all-depth UG: existing finite substitutions are a chosen constrained system.

Formal verification overlay: source Lean arithmetic statements exist; tree validity/run partition/cycle excision/global J and their complete assembled dependency closure have not been kernel verified in this run. A grep for `sorry` alone is not a proof audit. No Lean build was executed because repository build outputs would violate the write boundary without additional isolation.

26AN append-only addendum: C13 (double-positive packet) depends on 26AJ Lemma 2 + 26AL-L1 + source cost defs only; it strictly enlarges the proved-domain union (C_old subsetneq C_old union C_26AN) and alters no prior node status (26AM Outcome B preserved).

26AO append-only addendum: C14 (consecutive-positive + two-order recognizer) depends on 26AJ Lemma 2 + 26AL-L1 + banked 26AN-P (Type I inherited verbatim) + source cost defs; C_26AN subsetneq C_two-order proved via DP-completeness; alters no prior node status.

26AP append-only addendum: C15 (bulk repayment + maximal-run recognizer) depends on 26AJ Lemma 2 + 26AL-L1 (iterated) + source cost defs only; strict extension via p=3 witness + banked-26AO rejection + parity; claims no witnesses for p other than 3; alters no prior node status (26AM Outcome B preserved).

26AQ append-only addendum: C16 (bridge cross-run + mixed recognizer) depends on 26AJ Lemma 2 + 26AL-L1 (iterated, p+1 splays) + source cost defs + banked 26AP-P (Direct transition verbatim); C_26AP subsetneq C_AQmix proved via preservation run + bridge witness; one bridge per packet only; alters no prior node status.

26AR append-only addendum: C17 (split-sink + ARmix recognizer) depends on 26AJ Lemma 2 + 26AL-L1 (iterated) + source cost defs + banked 26AP-P/26AQ-bridge (D/B validators imported verbatim); C_AQmix subsetneq C_ARmix proved via preservation runs + essential split witness (neither sink alone suffices); 14-key walk retained as inessential control only; alters no prior node status (26AM Outcome B preserved).

26AS append-only addendum: C18 (coupled displacement + Hall allocation + ASmix recognizer) depends on 26AL-L1 + source rotation-trace semantics + banked ARmix validators (imported verbatim); universal restricted theorems proved (L1/L2/parity/E/Hall/allocation/global); Outcome B — complete precommitted hunt (14742/40000) negative, no strict novelty; alters no prior node status.

DIRECT-U1 append-only addendum: U-B (coverage gap, universal open). Depends on banked AJ-AS artifacts + authoritative replays only. C1/M failures certified; no invariant candidate (obstruction filed, spec d819d0154b8c); 3 strictly-uncovered W<=0 walks; n=7 truncated screen (50k/195k) negative; no W>0 walk; alters no prior node status; no 26AT/U2.

DIRECT-CWC append-only addendum: CWC-C1 (ECT transport refuted). Depends on source rotation traces + U1 gap witnesses only. Frozen spec v1.0 6381feb0 / v1.1 087524d6 (indexing convention only); token/epoch/contact construction verified (PASS1/2); universal cut-expansion FALSE via certified deficient cut (tok16, 1>0, walk W=-96); 2/3 U1 gaps allocate fully (not promoted); no positive-walk claim; alters no prior node status; no 26AT/successor.

DIRECT-NFKS-RT2 append-only addendum: RT2-A. Depends on 26AL-L1 + 26AJ Lemma 2 (orientation) + source rotation tables only. RT2 (+2, all n) + two-key idempotence + depth-4 + <=3-KEEP-key class implication proved; no banked theorem previously discharged a KEEP-support class; nonvacuity walk certified (dA erratum documented); alters no prior node status; universal (>=4 keys) still OPEN.

DIRECT-CD-K4 append-only addendum: CDK4-A. Depends on source rotation geometry (K4-L1, pruning) + finite one-bit certificate (68876 cases, both engines) + banked A-charging (C_K<=C_X<=A). Four-key class proved; with RT2-A, <=4-key class proved. Gate-0 witness outside all AJ-AS domains (all recognizers REJECT). No E/S conjectures, no packet hypotheses. Alters no prior node status; 5+ keys, universal Coarse-Double, DO still OPEN.

DIRECT-CDK5-LOW append-only addendum: CDK5L-A. Depends on banked K4-L1/pruning (arbitrary M) + nine-bound/conservation (same induction) + 142385-edge 0/1-potential certificate (both engines + independent verifier) + banked A-charging. Five-key <=8-core class proved; nine-core class (Q-2C_K=+2 witness) correctly excluded; five-key witness strictly outside all prior domains. Alters no prior node status; nine-core, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-DP append-only addendum: CDK5NP-A. Depends on source KEEP/DELETE semantics + cyclic interval partition + baseline lemma + nine-core debt bound (banked marked paths) + frozen Type K/P + banked A-charging (C_K<=C_X<=A). Nine-core Type K/P class proved; GAP witness (K3:G4, K5:G5 exclusions) retained at current HEAD; excluded D3-control preserved. Alters no prior node status; nine-core complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-S1 append-only addendum: CDK5NS1P-A. Depends on source semantics + banked CDK5NP-A supporting lemmas (partition/baseline/debt/Type-KP — scope-noted reuse) + NEW paired-payment proof (exception+successor, disjointness, telescoping). S1 class (disjoint from CDK5NP-A by H=1 exception) proved; GAP witness retained (K3:G2+G4 fail; K5 local AM-G pass noted, global exclusion kept); SHA-pinned fixtures (forbidden c920… rejected). Alters no prior node status; complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-S2 append-only addendum: CDK5NS2P-A. Depends on source semantics + banked CDK5NP-A supporting lemmas (same scope-noted reuse) + NEW triple-payment proof (exception/creditless/paying-second, disjointness, telescoping). S2 class (disjoint from CDK5NP-A by H=1 exception and from S1 by H=1 successor) proved; INC witness retained (K3:G2+G4 fail; K5:G5 fail with a=1; five REJECTs); CTL-A (S1) and CTL-B (two-exception) exclusions verified. Alters no prior node status; complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-VR append-only addendum: CDK5NVRP-A. Depends on source semantics + banked CDK5NP-A supporting lemmas (partition/baseline/debt/Type-KP — scope-noted reuse) + NEW relay proof (maximal scan, arbitrary-t summation, payer, disjointness, telescoping). VR class (disjoint from CDK5NP-A/S1/S2 by frozen H-inequalities) proved; INC witness retained (K3:G2+G4 fail; K5 local AM-G/S pass noted with dA=2; five REJECTs); CTL-A (S2-shape) and CTL-B (S1-shape) exclusions verified; historical errata (K5-depth, CTL-B-description, K9-row) recorded cost-neutral. Alters no prior node status; complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-MR append-only addendum: CDK5NMRP-A. Depends on source semantics + banked CDK5NP-A supporting lemmas (same scope-noted reuse) + NEW multi-packet proof (complete exception set, maximal scans, per-packet payment, pairwise disjointness, telescoping). MR class (disjoint from CDK5NP-A/S1/S2/VR by frozen H-inequalities + exception count) proved; INC witness retained (K3a:G2+G4 fail; K5-local AM-G/S pass noted; five REJECTs; primitivity + anti-concatenation); CTL-A (S2), CTL-B (doubled-VR member-non-novel), CTL-C (doubled-S2) roles verified. Alters no prior node status; complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-MSINK append-only addendum: CDK5NMSP-A. Depends on source semantics + banked cyclic interval identities + A-root-change baseline + nine-core B-depth bound + frozen exception/relay predicates + NEW joint-sink L1-L7 universal proof + independent strict novelty certificates (recursive C* closure over pre-promotion bank: 20 mechanisms + Z, nested rotations, memo-exact; IN 19 subproblems + OUT primitive, two independent decision procedures agree, 0 budget hits). Restricted five-key nine-core class proved; IN strict member residual + OUT nonmember residual (R1 properness); K-eligibility loose phrase filed as nonfatal erratum. Alters no prior node status; complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-DLSS append-only addendum: CDK5NDLSP-A. Depends on source semantics + banked cyclic interval identities + A-root-change baseline + marked nine-core B-depth bound (arbitrary ambient) + frozen exception/dual-long predicates + NEW joint-sink L1-L7 universal proof + independent strict novelty certificates (recursive C21* over pre-DLSS bank: 21 mechanisms + Z, nested rotations, memo-exact; IN/OUT primitive, two independent decision procedures agree, 0 budget hits). Restricted five-key nine-core class proved; IN strict member residual + OUT nonmember residual (R1 properness); primitivity 34/33 erratum + K-eligibility phrase filed as nonfatal errata. Alters no prior node status; complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-UESINK append-only addendum: CDK5NUESP-A. Depends on source semantics + banked cyclic interval identities + A-root-change baseline + marked nine-core B-depth bound (arbitrary ambient) + frozen unique-exception/dual-long predicates + NEW joint-sink L1-L7 universal proof + independent strict novelty certificates (recursive C22* over pre-UESINK bank: 22 mechanisms + Z, nested rotations, memo-exact; IN/OUT primitive, two independent decision procedures agree, 0 budget hits). Restricted five-key nine-core class proved; IN strict member residual + OUT nonmember residual (R1 properness); Gate-0 metadata errata (checkpoint typo, 32/33 counts, hash suffix, d0 summary) + K-eligibility phrase filed as nonfatal errata. Alters no prior node status; complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-ZULR append-only addendum: CDK5NZULR-A. Depends on source semantics + banked cyclic interval identities + A-root-change baseline + marked nine-core B-depth bound (arbitrary ambient) + frozen zero-exception/unique-payer predicates + NEW local-reserve L1-L9 universal proof (sharp q=4/H=2 equality 2=2, predicates-first strict K/P, per-interval payment, no sink) + independent strict novelty certificates (recursive C23* over pre-ZULR bank: 23 mechanisms + Z, nested rotations, memo-exact; IN/OUT primitive, two independent decision procedures agree, 0 indeterminates, 0 budget hits; 384-word corpus regression 378+6 with 0 residual; 90-obligation adversarial audit PASS normal+-O with 7 fault injections detected). Restricted five-key nine-core class proved; IN strict member residual + OUT nonmember residual (R1 properness); R3 deviations adjudicated nonoperative (441 raw/425 distinct identity registration, SHA-dedup equivalent order, untriggered budget guards, manifest count corrected); proof-stage frozen-theorem copy footer + H2/H5 redundancy filed as nonfatal records. Alters no prior node status; remaining complement, K>=6, universal, DO still OPEN.

DIRECT-CDK5N-SELR append-only addendum: CDK5NSELR-A. Mathematical: source semantics + cyclic identities + A-root-change baseline + nine-core bound + unique bare exception + maximal short-relay classification + exact {e,p} untyped set + distinct q=3,H>=2 donor + strict K/P elsewhere + disjoint pair/singleton payment + universal telescoping (L1-L10). Novelty/properness: complete pre-SELR bank24 (3+9+12 incl. ZULR, SELR excluded) + rotation-aware C24* (Rot base at every level, two engines agree 15/15) + primitivity 31/31+30/30 + 1464 rotation decisions + complete negative certs + strong 22-check verifier + frozen rm18 provenance + strict proper-subclass proof + Gate-0 errata A-F adjudication (IN 36<=106; 19-count; rotation repair; recognizer INDETERMINATE wiring; -O-safe; rich certs). Alters no prior node status; remaining complement, K>=6, universal, DO still OPEN.
