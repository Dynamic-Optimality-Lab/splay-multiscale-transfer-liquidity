# K4-L1 marked-core growth (PROVED from source rotation geometry)

**Definitions.** Core_M(T) = union of root-to-m paths (m∈M), with parent-child
relations; c_M(T) = node count. A node is in the core iff it is an ancestor of
a marked key (self included). Rotations preserve key sets and BST order; a
subtree whose key set is unchanged keeps its internal core statuses (membership
is determined by downward descendant marks, and rigid subtrees keep theirs).

## Single-rotation lemma

Rotate child c over parent p (pivot subtree S, same keys/attachment before/after).
Only p,c can change core status (all other subtrees A,B,C rigid with unchanged
descendant-mark sets; outside S, paths and marks unchanged).
- subtree_before(c)={c,A,B}, subtree_before(p)=S; subtree_after(c)=S,
  subtree_after(p)={p,B,C}.
- c: before [c-sub marked] → after [S marked]. p: before [S marked] → after
  [p-sub' marked].
- If c-sub (old) marked: before {p:1,c:1}=2; after c=1, p∈{0,1} → change ≤0.
- Else (c-sub unmarked): before p=[S marked]∈{0,1}, c=0. After c=[S marked],
  p=[p-sub' marked]. If S unmarked: 0→0 (exactly 0). If S marked (via p/C):
  at most 1→2, i.e. **increase ≤1**, and the enlarged unit (now containing the
  mark from C or p) is marked afterwards.
- Hence: **per rotation +1 max; 0 if c-subtree marked (in fact nonincreasing);
  exactly 0 if the whole pivot subtree S is mark-free.**

Checked on zig, LL, RR, LR, RL with hanging subtrees A,B,C (source cases
wp6_eventflow.py:111-182; same tables as RT2 file).

## Marked access (x∈M): nonincreasing

Every bottom-up rotation splays x or an ancestor of x: zig (c=x), zig-zig rot1
(c=p∋x), rot2 (c=x-unit∋x), zig-zag rot1 (c=x), rot2 (c=x-unit∋x). Each c-subtree
contains x, hence a mark → each rotation nonincreasing ⇒ c_M(S_x(T)) ≤ c_M(T). ∎

## Unmarked access (x∉M): at most +2

x's subtree grows monotonically (each step attaches more ancestors; never
detaches x) — so once it contains a mark it stays marked. Rotations before the
first S-marked rotation have mark-free S ⇒ exactly 0 each. Let k be the first
rotation whose pivot subtree S is marked (if none, total is 0):
- Rotation k: ≤+1 by the lemma; afterwards the x-ancestor-unit contains the
  mark (absorbed from C or p, both inside the restructured unit) ⇒ marked.
- Any remaining rotation(s) of the same StepEv (at most one: a StepEv has ≤2
  rotations): c is x or an ancestor-unit containing x… except possibly rotation
  k+1 = second rotation of the StepEv whose c is x's own (still mark-free)
  subtree with S marked ⇒ ≤+1. Total for the StepEv ≤+2.
- Every later rotation has a marked c-subtree (ancestor-units contain x's now
  marked unit… more precisely they contain the absorbed mark) ⇒ nonincreasing.
Total ≤ +2. Zig StepEvs (1 rotation) give ≤+1. ∎

No finite-n assumption; arbitrary hanging-subtree sizes cancel (rigid carriers).
Constants frozen: +0 marked, +2 unmarked.
