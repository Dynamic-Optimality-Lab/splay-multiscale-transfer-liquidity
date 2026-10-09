# PIVOT — COUPLED EVENTUAL MONOTONICITY: LITERATURE + FIRST CANDIDATE

Branch `wp5x-k6c2-specialized`, HEAD `88f344d` + C181–C193 tree (preserved).
Old critical path (GC factor-3, D6, 14P, H1/H2/R3, Bellman, fixed-chain,
generic Hall) RETIRED from critical path; retained as lemmas/regression.

## 1. External theory (exact, from source)

- Levy–Tarjan 1907.06310v3: DO ⟺ approx monotone (Thm 3.5, via coercible
  simulation embedding); eventual monotone + repeatable + coercible ⟹ DO
  (Thms 4.1–4.3, repeater absorbs g). Crossing bound Λ approx monotone
  overhead ≤4 (Thm 7.5, max-heap/window proof, no potential). Per-removal
  bound FAILS for Splay (explicit (1)⊕Y example). Conjectures 8.1 (Splay
  crossing approx monotone) + 8.3 (bookkeeping ≤ mult of crossing+|T|)
  ⟹ DO. Suggested potentials: heap-violation edge count; crossing-depth
  weighted refinement (cap O(|T|)); bookkeeping proxy (spine max).
  Cost: splay Σ node-depths; rotational ≡ within ×2 (Thm A.1).
  Consequence: repeater/coercibility BANKED — only the coupled bound
  E_B ≤ C·S_A + g(T0) is needed, then LT gives DO.
- Chmel et al. 2607.18498v1: Õ(log log n)-competitive (Thm 1, +(n) term,
  needs Ω~(n log log n) length). Cost 1+#rotations (App B ≡ standard).
  Comparator: near-optimal T*, serialized, ribless/O(log n)/O(1)-rotations.
  Potential: contracted point gaps over heavy paths (rank = depth in T*),
  lazy intervals, pairings, bends. Losses (all from arbitrary-T* rank
  dynamics): boundary Θ(log n)→contraction; G per Insert; log G per
  ValueChange (τ block-shrink); O(log G) important boundary; G log G
  absorption. NO Wilber/lower-bound/subsequence charging.
- Chmel-under-coupling verdict (analytic): rank ValueChanges, interval
  histories, block-shrinkage all persist when comparator = coupled Splay
  A (deep, splay-bundled rank changes). Degrades to polylog, NOT
  constant. No n-factor kill visible. (Not finite-implemented; analytic.)

## 2. Cost translation (closed, kernel green)

Local e=ceil(d/2) (root 0) vs LT d+1 vs Chmel 1+rots: per-access
`stepev_lt_upper`, `stepev_le_lt`; aggregate `cost_translate` gives
LT(Y) ≤ (2C+1)·LT(X) + 2g from E_B ≤ C·S_A + g (+ monotonicity lemma).

## 3. LT heap-violation candidate: DEAD

Psi = viol(B) − viol(A), X-clock recency, frozen snapshots (telescoping
exact). Epoch scan (micro/walks/steered): C=6 clean on corpus BUT via
constant papering (steer [23→21]: 6−1−C·1 needs C≥5; potential released
only 1 of 6). C_min scale law: 1.0 → 2.33 → 15.0 → 15.5 at n=16/32/64/128
(driven by terminal B/A ratios). Zero-A-cost analysis done right (DELETE
costs included; true zero+positive impossible). KILLER: steered n=64
epoch needs C≥15. Candidate dead for universal C. Exact witness +
artifacts in pivot_epoch/heapviol.json. (Weighted refinement would need
Ω(depth) weights with O(1)-local creation — contradiction; reduces to
Chmel-like polylog.)

## 4. Falsification (eventual monotonicity)

Ratio E_B/S_A bounded ~1.68 (consistent with GC C=3); no growth in m/n.
SA-max/beam/greedy/micro to n=128: minPhi never <0. No END-B family.

## 5. Standing

Proved: literature chain (only coupled bound missing), cost translation,
twin/steered sanity, macro/induction banked. Dead: heap-viol faithful,
Chmel-transplant-for-constant (analytic), B-prepend, pure-B lemma.
Open: coupled bound E_B ≤ C·S_A + g (firewall holds: universal epoch
inequality is terminal-hard; bystander control is the invariant wall
across potential forms). No A/B/C endpoint met. GC-STATIC OPEN.
