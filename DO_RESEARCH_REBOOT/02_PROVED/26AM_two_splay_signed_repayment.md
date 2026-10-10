# 26AM: two-splay displacement + generalized/signed four-block repayment (PROVED)

**Status: PROVED** — universal two-splay bound, generalized four-block theorem,
signed four-block theorem, containments, disjointness. New closed-walk coverage
NOT established (bounded hunt negative) — Rule 4 open. No J4/ROW/J-SELF/DTQ/UG
used anywhere.

## 26AM-L1 — two-splay displacement (PROVED by composition)

For any finite BST B, present keys y,z, and any tracked key r, two ordinary
bottom-up splays give `d_{S_z(S_y(B))}(r) ≤ d_B(r)+4`: apply banked 26AL-L1
(`d_{S} ≤ d+2`, proved by frame joining/re-carry analysis) twice.
Corroboration (supporting only): 216884 checks (exhaustive n≤7 + random n≤10),
max gain exactly +4, tight example (n=5, splays 3 then 5, tracked key 1: 0→4).
No stronger two-splay constant is claimed.

## 26AM-G — generalized four-block repayment (PROVED)

Closed walk, cyclic A-root blocks (26AJ decomposition). For every positive
block i with four DISTINCT cyclic positions (i,i+1,i+2,i+3) (hence m≥4;
for m<4 no positive block can satisfy the distinctness hypothesis, so all
blocks are nonpositive and the sum is ≤0 trivially): assume G1 (δ_i>0),
G2 (genuine B-changing KEEPs at i+1,i+2, keys ≠ r), G3 (δ_{i+1},δ_{i+2} ≤ 0),
G4 (block i+3 led by r), G5 (2a_{i+3} ≥ c_i with c_i = floor((h_i+4)/2) ∈ {2,3},
h_i ∈ {1,2} by 26AJ), G6 (capacity
δ_i ≤ (2a_{i+1}−q_{i+1})+(2a_{i+2}−q_{i+2})+(2a_{i+3}−c_i)), G7 (no geometry).
Then q_{i+3} ≤ c_i (L1 with h_i ≤ 2 gives depth ≤ 6), so
δ_i+δ_{i+1}+δ_{i+2}+δ_{i+3} ≤ 0 by G6. Disjointness: shared block with slot ≥1
in some triple is forced nonpositive by that triple, so distinct positives own
disjoint triples (m≥4 makes all slots distinct automatically); triple-less
blocks are nonpositive (else they'd own triples). Summing: Σδ ≤ 0, i.e. Q_B ≤ 2A.

## 26AM-S — signed four-block repayment (PROVED)

Under S1 (δ_i=1), S2/S4 (genuine, y,z distinct from x,r as stated),
S3/S5 (δ=0 ⟺ q=2a exactly), S6 (delayed r), S7 (a_{i+3}≥2), S8 (no geometry):
q_{i+3} ≤ 3 (displacement) gives δ_{i+3} = q−2a ≤ 3−4 = −1; with
1+0+0−1 ≤ 0 the group is nonpositive. Same disjointness. Containment
C_S ⊆ C_G: (2a−q) terms vanish by S3/S5, and 1 = δ_i ≤ 0+0+(2a_{i+3}−c_i)
since 2a_{i+3}−c_i ≥ 4−3 = 1. So every 26AM-S walk satisfies 26AM-G.

## Scope (exact)

Covers closed walks whose every positive block meets G (resp. S) four-block
conditions. Does NOT cover: multi-splay delays, deficits beyond capacity,
indirect repayment, unrestricted Coarse-Double. Strict same-side/new coverage
and Rule-4 promotion require a certified witness (open).
