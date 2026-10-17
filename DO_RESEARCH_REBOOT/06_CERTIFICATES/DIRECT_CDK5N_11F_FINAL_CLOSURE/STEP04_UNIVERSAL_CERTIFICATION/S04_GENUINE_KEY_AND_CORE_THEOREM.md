# S04_GENUINE_KEY_AND_CORE_THEOREM.md — Gates B (F04-07/F04-08)

## K(W)=G(W) (exactly B-closed words, ≥1 genuine KEEP)
Re-audited proof (CW theorem, verified): Lemma 1 root-change (splaying non-root
changes root; contrapositive: B-unchanged access hit the root); Lemma 2 root
provenance (B changes only on genuine KEEPs; root = latest genuine target);
Lemma 3 cyclic initial root (B_T=B_0 puts root(B_0) in G). Every KEEP is genuine
or nongenuine-at-B-root-in-G. DELETEs B-invariant (dropped soundly). Re-tested:
80/80 closed survivor walks K==G here (fresh replay, independent helpers).

## Core invariance + constancy
C_M(B_{t+1}) ⊆ C_M(B_t) per operation (DELETE identity; zero-cost identity;
genuine marked-target splay adds only the already-member target; nongenuine at
marked B-root identity). B_T=B_0 gives constant C_M = S, |S|=9 (nine S identities
fixed per walk; may vary across walks — S-relabeling, no new observable).
Re-tested: 80/80 constancy with 9-sets here.
