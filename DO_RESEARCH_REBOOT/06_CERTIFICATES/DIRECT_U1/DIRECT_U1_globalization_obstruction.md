# DIRECT-U1-07/08: universal proof attempt and obstruction classification

## Attempted globalization routes (all blocked)

1. Summed 26AS-L1 pair savings: each B-splay belongs to Θ(k²) tracked pairs;
summing favorable pair bounds spends the same rotation event many times
(N18). No canonical pair partition exists for arbitrary walks. BLOCKED.
2. Rank/log potentials (classic splay analysis): change O(log n) per splay
but single-step weights are Θ(n) (deep-narrow KEEP). Cannot dominate. BLOCKED.
3. Depth-sum potentials: total depth-sum is near-conserved (zig-zig 0,
zig-zag −2, zig 0 per splay), but weights need Θ(n) drops on paid steps while
the potential moves O(1). BLOCKED (wrong direction).
4. θ-aggregates (sum/max/saturating): refuted by (C1-parametric), (M), and
exact-drop requirements respectively; see frozen spec. BLOCKED.
5. Cycle-rotation charging (AJ–AR style) without returns: positive blocks
with no former-root return anywhere in the walk cannot be charged to any
source event. The 26AS archive shows 944/1000 sampled closed walks outside
all packet domains — yet all have W≪0, so the missing proof is about
unstructured walks, not missing credit. BLOCKED (no structure to charge).

## Obstruction classification

- Potential creation: YES (A-only DELETEs create unbounded θ-exposure;
  measured scaling residuals −1,0,+2,+7).
- Potential non-discharge: YES (M-transfer mode).
- Overlapping pairwise credits: YES (L1 double-spend).
- A-only DELETE geometry: central (creation mechanism).
- A-root no-op KEEP geometry: central (positive weight without A-payment).
- Incomplete old packet coverage: YES (944/1000 sampled uncovered; 3 certified).
- The remaining obligation is a genuinely new global conservation idea, not a
  bigger packet family (charter §19 respected: no new Hall mechanism invented).

## Standing evidence FOR the inequality (not proof)

11,985 distinct closed walks (26AS family): ZERO with W>0 (all strongly
negative). n=7 BFS (50k states, 195k transitions, truncated): no positive
cycle in explored subgraph. Both engines agree everywhere tested.
