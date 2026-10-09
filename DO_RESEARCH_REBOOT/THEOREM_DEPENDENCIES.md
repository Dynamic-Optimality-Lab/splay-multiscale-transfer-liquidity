# Dependency graph and proof-state labels

Edges below are sufficient mathematical implications, not equivalences unless stated. A proved implication with an open premise does not mark its destination proved.

```mermaid
flowchart TD
  PA[Pair Access encoding: PROVED] --> CD[COARSE-DOUBLE: OPEN]
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
