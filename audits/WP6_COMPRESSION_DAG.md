# WP6 Compression DAG — failure-side chain from ¬8AC (C118 execution instrument)

Terse. Statuses: PROVED / PROVED_KERNEL / CONDITIONAL / FIRST-UNSUPPORTED / OPEN.
Update by editing statuses only; do not expand into prose.

```
¬8AC  [ASSUMED, Mode B: some present-legal instance defeats cap-3 routing]
  =>[PROVED] deficient Q exists (negation unfolding: unmatched demand set)
  =>[PROVED] minimal-deficient core Q (finite descent; shrink_minimal code)
  =>[PROVED_KERNEL] 8A: Delta(Q)=1 (AR-20)
  =>[PROVED_KERNEL] 8B: mindeg(N(Q))>=4 (AR-21)
  =>[PROVED_AUTHOR] 8C: connected core
  =>[PROVED_AUTHOR] 8J: latest access L with |Q_L| >= 3|U_L|+1, U_L = N(Q_L)\N(Q_<L)
  =>[PROVED] some block B-heavy-Q (8H contrapositive: non-heavy Q never violates;
       8I residual Delta <= sum q_j forces a positive q_j block)
  =>[CONDITIONAL] fresh analysis at L (8E: E1(L) complete to Q_L; E1<>empty =>
       |Q_L|>=4; E1-empty => repeat-habitat demand-without-supply)
  =>[CONDITIONAL] anchored present (8U: past-x-Aevs K-anchor; FRESH-CHANNEL:
       every demand has E1<>empty or E4-pristine setup (banked C31))
  =>[FIRST UNSUPPORTED] transient/old escape closure: anchored + E2/W/E7/E4
       supply at heavy blocks is cap-exhausted or thin, AND no new supply
       arrives (cap-exhaustion universals + variation universals all open;
       finite faces: varhole/new>=4, steer N~=4e_B, pack overlap>=1, K2A<=-2)
  =>[OPEN] HEAVY-POSITIONAL-SEAL-IMPOSSIBLE (heavy block with every augmenting
       escape sealed under valid splay dynamics)
  =>[OPEN] rigid forbidden migration configuration (leaf target: local splay/
       BST/path/rotation fact; must satisfy leaf criteria 1-8)
```

Mode-A compression (sufficient lemma, assembly verified C118):
  8Q (smaller-Hall + mindeg<=3 => Hall(Q)) [PROVED_AUTHOR conditional]
  + strong induction on |Q| (well-founded finite; base Delta(empty)=0)
  + 8AC-ZONE: every Q with mindeg(N(Q))>=4 satisfies Delta(Q)<=0 [OPEN]
  => GC-STATIC (forall Q). Proof: IH gives smaller-Hall; case mindeg<=3 by 8Q;
  case mindeg>=4 by 8AC-ZONE. No circularity (8AC-ZONE is standalone universal
  on the violator zone; smaller-Hall never assumed for same-size Q).
  8AC-ZONE falsifiable: mindeg>=4 + Delta>=0 is a Hall kill (Mode B trigger).

Bookkeeping (binding on 8AC closure): combined accounting
  sum|new_j| + sum c_j <= |R| (no new/reuse double-count); residual-capacity
  formulation equivalent accepted. Do not mark 8AC proved without it.

Alternating-path note (Berge, constructive use): stuck allocator + reachable
unsaturated source => augment; stuck + closed saturated reachable set => Hall
obstruction = the trap to compress (not a slogan: trap anatomy vs 8S/8T/8U/8W/
8A/B/C/E/J/H/I/Q/R/BST facts is the Phase-2 work).
