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
