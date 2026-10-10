# 26AK-L1: opposite-branch preservation (PROVED) + falsification boundary

## Lemma (exact)

Let B be a finite valid BST rooted at x. Let r, y be present keys distinct
from x and each other, on opposite sides: `(r−x)(y−x) < 0`. Let `h = d_B(r)`.
Splay y bottom-up (authoritative rotations:
`scripts/wp6_eventflow.py:111-182`, same cases in `python/independent/splay.py:92-152`).
Then the child subtree of x opposite the search path survives intact, and:

\[
\boxed{d_{S_y(B)}(r) = d_{S_y(B)}(x) + h.}
\]

## Proof (rotation cases; both orientations by L/R symmetry)

Take `r < x < y` (mirror case symmetric). The search path from x stays strictly
inside x's right subtree (BST order), so every rotation triple before the final
operation lies strictly below x; x's left subtree (∋ r) is carried as an intact
sibling object (verified per rotation branch in both engines: carried subtrees
q/c/a/d/t1/t2 are reattached, never restructured). For the final operation with
grandparent/parent x, the realizable turn pairs are: zig (y child of x),
zig-zig RR, zig-zag RL — in each, x's left child subtree is reattached unchanged
(shown term-by-term from both implementations). The remaining pairs (LR/LL with
grandparent x) would require the path's parent level to sit in x's left subtree
while y lies right — impossible by path containment. Hence the left subtree
keeps internal structure; with x at final depth D', the carried child sits at
D'+1 with r exactly h−1 edges below it, so r sits at D'+h. The case y<x<r mirrors.
Empty protected subtree is impossible (r is present in it). DELETEs freeze B
(engine semantics), so intra-block DELETEs do not affect the claim.

## Finite corroboration (not the proof)

- Exhaustive n≤7 (all shapes, all root-fixed triples): **36272/36272 hold**, 0 violations.
- Random n=8..10: **1338/1338 hold**.
- Engine agreement tuple-vs-ptr on 400 paired trials: **400/400**.
- Records: `06_CERTIFICATES/26AK/ak_disp.log`, `ak_deep.log/json`.

## Falsification boundary (why the side condition is load-bearing)

Same-side y (no side restriction): identity fails commonly at n=3 already, and
`d'(r) = 5` observed at n=6 (samples in `ak_disp.log`). Hence no unrestricted
constant-depth displacement law follows; the opposite-branch hypothesis is
necessary. Same-side transport is NOT pursued here.

## Consequence used downstream

With former-root `h ≤ 2` (26AJ Lemma 2 applied to block i's splay), a delayed
access to r after one genuine opposite-branch intervening splay costs
`q ≤ floor((h+2)/2) ≤ 2`. The structural cap is `c_i = floor((h_i+2)/2) ∈ {1,2}`.
