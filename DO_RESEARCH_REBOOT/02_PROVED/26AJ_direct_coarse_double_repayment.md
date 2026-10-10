# 26AJ: Former-root successor repayment (PROVED)

**Status: PROVED** — universal restricted Coarse-Double theorem + validated witness.
No J4, ROW-DIAMETER, J-SELF, DTQ, UG, potentials, LP, or compactness used anywhere.

## Definitions (source: `scripts/wp6_eventflow.py:84-182`, `wp6_coarse_double.py:28-53`)

Closed present-key Pair-Access walk γ (diagonal start, finite). Per access:
`a=ceil(d_A/2)`; KEEP: `q=floor(d_B/2)`; DELETE: `q=0`. `A=Σa`, `Q_B=Σq`.
KEEP splays both trees; DELETE splays A only, B frozen; key set fixed.

## Lemma 1 (cyclic A-root blocks; cf. banked C.ZIG run structure)

If `A(γ)>0`, partition cyclically into maximal blocks, each a leader (`a≥1`)
plus following `a=0` accesses. Every access in a block targets its leader's key
(`a=0` ⟺ key is current A-root; leader splays it there; no-ops keep it).
DELETE never touches B; after a block key's first KEEP, B is rooted there, so
later same-key KEEPs are B-root no-ops. Hence **each block has ≤1 nontrivial B
splay**; with `a_i` (leader, ≥1) and `q_i` (that splay's doubles, else 0):
`A(B_i)=a_i`, `Q_B(B_i)=q_i`, deficit `δ_i=q_i−2a_i`, and
`Q_B−2A = Σδ_i`. (If `A(γ)=0`, banked zero-A theorem gives `Q_B=0`.)

## Lemma 2 (former-root depth ≤ 2)

Splay present x in B; let r=old root. Bottom-up rotation loop processes frames
innermost-first; outer frames (original ancestors) are untouched until consumed;
the final operation is the first involving the original root (depth counting:
pairs consume 2 levels, final single/double at depth ≤2). Cases from source:
zig→r at depth 1; zig-zig→r at depth 2; zig-zag→r,parent at depth 1;
x=root→depth 0. Therefore **`d_{S_x(B)}(r) ≤ 2`**, all sizes/depths. Corroborated:
2952 splay trials (both engines, n≤9), 0 violations, max 2
(`06_CERTIFICATES/26AJ/26AJ_depth_lemma_probe.json`).

## Lemma 3 (successor repayment)

Let block i be positive (`δ_i>0`, so `q_i>0`): its first KEEP (key x) is
nontrivial; let r_i = B-root before it (r_i≠x). If next block's leader accesses
`x_{i+1}=r_i`, then B is unchanged since the splay (same-key accesses + DELETEs
only), so its first B splay of r_i starts at depth ≤2: **`q_{i+1}≤1`**, whence
**`δ_{i+1} ≤ 1−2a_{i+1} ≤ −1`**. DELETE-leader and KEEP-less cases give q=0 ≤1 too.

## Theorem 26AJ-B (capacity form)

For closed γ, if every positive block has `x_{i+1}=r_i` and `0<δ_i≤2a_{i+1}−1`,
then `Q_B≤2A`. Proof: `δ_i+δ_{i+1} ≤ δ_i+1−2a_{i+1} ≤ 0`. Successor map
`i→i+1 (mod m)` is injective; successors have δ≤−1 (never positive), so pairs
are disjoint; leftovers are nonpositive. Sum ≤0. Degenerate m=1: a positive
block would need `x_1=r_1` yet `x_1≠r_1` (nontrivial splay), impossible — so
m=1 positive blocks cannot satisfy the hypotheses; sum ≤0 still holds.

## Theorem 26AJ-A (one-unit form)

Same with `δ_i=1` for positives (follows from B since `a_{i+1}≥1`).

## Witness (nonvacuous, source-validated)

Right vine n=7; prefix DELETE 7, DELETE 6; exact closed word:
`K7,K1,K4,K5,K3,K1,D7,D6`: A=14, Q=9, W=−19; per-access (a,q,δ) =
(1,3,+1),(2,1,−3),(2,1,−3),(1,1,−1),(2,2,−2),(1,1,−1),(3,0,−6),(2,0,−4);
B-depth max 6; both trees exactly restored (serial-compared);
`replay()` cross-check identical; former root before KEEP 7 is key 1;
next block KEEP 1; sole positive block δ=+1 ≤ 2·2−1. Repetition gives
arbitrarily long covered walks. Outside n≤6 analytic closure (n=7),
outside zero-A (A=14), genuine overflow (3>2·1), B-depth 6.

## Scope (exact)

Covers closed walks whose every positive block has a former-root successor with
repayment capacity. Does NOT cover: positive blocks without such successors,
larger deficits beyond capacity, indirect/multi-step repayment, or unrestricted
Coarse-Double. No statement about J4, ROW-DIAMETER, or Dynamic Optimality beyond
this restricted charge class.
