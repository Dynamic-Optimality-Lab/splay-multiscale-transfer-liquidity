# WQ-1/WQ-2/WQ-3 theorems (Steps 06-08; analytic proofs)

## WQ-1 stability (STEP 06)

m_C(x) = min{w(x,y): y∈C} (+∞ if none). Stable ⟺ x,y∈B ⇒ m_C(x)=m_C(y)
∀B,C. Well-defined quotient edges B→C with weight m_C then exist.
Stability is CHECKABLE given (graph, partition) — no existence claim.
Refinement (STEP 09) splits by min-weight signatures until stable or cap.

## WQ-2 forward + reverse (STEP 07)

Forward: detailed x→y (w) maps to [x]→[y] with ŵ=m≤w (min over members;
m exists by stability applied to x's block/target block). So detailed
closed walks map to quotient closed walks with ≤ total weight.
Reverse (uniform lifting): quotient edge B→C (weight m) realizable from
EVERY x∈B at weight m — HOLDS AUTOMATICALLY under stability (m_C(x)=m
means x HAS an edge into C of weight m; pick y as its endpoint).
Thus stability ⟹ uniform reverse lifting (no extra assumption). The
refinement's job is exactly to enforce stability; reverse lifting comes
free. (This is why §12's requirement is satisfiable by construction.)

## WQ-3 reflection (STEP 08)

Forward: detailed negative cycle maps (forward sim) to quotient closed
walk with ≤ (negative) weight ⇒ contains quotient negative cycle
(standard: negative closed walk contains a negative simple cycle).
Reverse: quotient negative closed walk B_0→...→B_k=B_0 (weight W_Q<0),
from any x_0∈B_0 follow uniform lifts (WQ-2) with EXACT quotient weights;
repeat indefinitely; finiteness of G ⇒ some B_0-boundary detailed state
repeats; intervening segment is closed with weight m·W_Q<0 ⇒ contains
detailed negative cycle. ∎ (Finite G required — symbolic G finiteness is
part of Stage-11 completeness, separately established/blocked.)

## Scope notes

WQ-1..WQ-3 are pure graph theorems (no source content). Their FORCE for
the terminal program comes from: (a) stability checkable on explicit
graphs ( Gate-D validated below), (b) refinement algorithm converging
to stability (rounds capped at 256), (c) symbolic G finiteness (Stage-11
C-obligation — OPEN universally). Status: PROVED (graph-theoretic).
