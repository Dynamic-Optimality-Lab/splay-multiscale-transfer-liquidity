# STRICT_MARKED_CORE_MONOTONICITY.md — Gate B (per-operation investigation + verdict)

## Definitions
M = five marked keys. `C_M(B) = union over x in M of Path_B(root,x)` (paths include endpoints).
Domain: admissible original cases only (legal BSTs, source-original ops); diagnostic samples with
non-genuine cores classified separately (none used here: S is the genuine nine-core throughout).

## Theorem 1 (marked-target splay is C_M-nonincreasing) — PROVED
By single-rotation induction. Right rotation at p (x = p.left): x gains p's-right-subtree as
descendants; p loses x's-outside parts; ancestors above keep key sets; rigid subtrees keep status.
Nodes that can JOIN C_M: only nodes gaining marked descendants = x (gains C-side). If x is marked,
x is already a member (self-membership) → no joins. Nodes may LEAVE (p losing its last marked
subtree while unmarked) — allowed (⊆). Left rotation symmetric. Zig (root case) same with no
grandparent. Hence every primitive rotation of a marked target preserves `C_M(t+1) ⊆ C_M(t)`;
full splays compose. Measured: 0 growth in 1118 marked splays (375 shrink, 743 same).

## Theorem 2 (unmarked-target growth characterization) — PROVED
Same analysis with x unmarked: x JOINS iff x was outside C_M and the gained C-side (resp. B-side)
contains a marked key x wasn't already ancestral to. All other nodes shrink-or-hold. Hence at most
the target joins; everything else is monotone. Measured: growth happens (978/1882 unmarked splays).

## Minimal counterexample (universal monotonicity REFUTED, admissible)
B = 10(1, 20) [keys: root 10 fringe, left leaf 1 fringe, right 20 marked], M = {20}.
`C_M` before = {10, 20}. Source-original `KEEP(1)` (legal nongenuine KEEP): zig (right rotation).
After: root 1, `C_M` = {1, 10, 20}. Grown by {1} (unmarked target). Replay-verified (pointer +
tuple engines agree). The claimed universal `C_M(B_{t+1}) ⊆ C_M(B_t)` is FALSE for R1-T-admissible
nongenuine KEEPs.

## Other operations
DELETE: B untouched → C_M identical (all cases). Zero-cost KEEP/DELETE (root target): splay root
is identity (no rotations) → C_M identical (V1-tested identity included).

## C_M(B_t) = S — REFUTED as universal state claim
Admissible boundary witness (post-genuine-KEEP(5), root marked 5): marked key 9 has fringe
ancestors [12, 7] (S = [2,4,5,8,9,10,11,13,14], M = [2,5,9,10,11]). So C_M ∋ {12,7} ⊋ S.
Measured class rate: fringe-ancestor boundaries common (skip censuses 120/720, 52/480, 182/720).

## R3 consequence
Universal monotonicity is refuted (minimal admissible counterexample above); marked-splay
monotonicity is proved (not universal). Full q correspondence via C_M = S cannot be established
in the frozen representation (no new observables permitted). Lemma status: universal claim
REFUTED; marked restriction PROVED. SC10 cannot PASS. HARD STOP per R3/Gate-B rules.
