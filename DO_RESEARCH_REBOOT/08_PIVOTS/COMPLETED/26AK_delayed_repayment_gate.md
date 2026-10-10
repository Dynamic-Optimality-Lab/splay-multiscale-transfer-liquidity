# PIVOT-26AK (MECHANISM GATE) REPORT — PROVED NEW DELAYED CLASS

## Verdict

```text
PROVED:
NEW UNIVERSAL DELAYED-REPAYMENT
COARSE-DOUBLE CLASS WITH
GENUINE ACTIVE INTERVENING B SPLAY
```

## A. Safety
Branch `coarse-double-branch`, HEAD `88d3007` (+ only 26AJ/26AK untracked artifacts;
tree was clean at session start). No reset/clean/stash/commit/branch-switch.
All writes inside `DO_RESEARCH_REBOOT/`. 26AJ foundation re-read for defects:
none affecting reuse (block structure, depth lemma, successor repayment, m=1 case).

## B. 26AJ foundation
Reused, not rebuilt: cyclic A-root blocks (≤1 nontrivial B splay, single-key,
A=a_i, Q=q_i, Σδ=Q−2A), former-root depth ≤2, immediate repayment q≤1, witness.
Defect scan: none found.

## C. Target
Positive block + one genuine intervening B splay (y≠x,r) + delayed former-root
access, opposite-branch geometry, capacity-gated.

## D. Displacement law (PROVED, not assumed)
`d_{S_y(B)}(r) = d_{S_y(B)}(x) + d_B(r)` for opposite-side r,y with B rooted at x:
rotation-case proof in companion audit (non-final ops carry the opposite subtree
intact; final zig/zig-zig/zig-zag preserve it; the restructuring zig-zag is
unrealizable on the opposite side by path containment). Corroboration:
36272/36272 (n≤7 exhaustive) + 1338/1338 (n=8..10) + 400/400 engine agreement.
Same-side falsified (identity fails commonly; d=5 observed) — side condition
is load-bearing, not decorative.

## E. B-double cap
`q_{i+2} ≤ ⌊(h_i+2)/2⌋ = c_i ∈ {1,2}` from D + former-root lemma on the
intervening splay. Strongest proved form; frozen-detour corollary (cap 1) recorded.

## F. Capacity + H5 + disjointness (exact)
`δ_i ≤ (2a_{i+1}−q_{i+1}) + (2a_{i+2}−c_i)`; H5 keeps the middle block
nonpositive; triples of distinct positives proved disjoint (shared block with
slot ≥1 is forced nonpositive; m=1,2 self-overlap makes positivity jointly
inconsistent with H2/H4). No overlap, no double-spending, wraparound covered.

## G. Disjointness
Proved as above (modular indexing, small-m degenerates closed).

## H. Restricted theorem (26AK-T)
As stated in `02_PROVED` doc: H1–H6 ⇒ Q_B ≤ 2A. All quantifiers explicit.

## I. Nonvacuity (validated witness, NOT 26AJ's pattern)
n=7 shape-1: prefix D6,D1 + 11-block cycle (triple K6,K7,K1 + 8-tail), closed
exactly on the authoritative engine, sole positive (K6, δ=+1), genuine
opposite-branch intervening KEEP (B-root==6 verified), delayed r (h=2, c=2),
H5, capacity 1≤4, total −25. Repetition ⇒ arbitrarily long covered walks.
Outside zero-A, n≤6 closure, bounded-depth charging; successor ≠ r (not 26AJ).

## J. Four-rule audit
RULE 1 — STRICTLY SMALLER: PASS (triple-conditioned closed walks).
RULE 2 — CONCRETE SOURCE MECHANISM: PASS (run structure + rotation cases).
RULE 3 — ONE-SESSION CLOSURE: PASS (lemma + capacity + disjointness + witness).
RULE 4 — NEW OBLIGATION DISCHARGED: YES (delayed-repayment closed class).

## K. Pipeline effect
Direct branch now: C.ZIG decomposition → bounded-depth charging [banked] →
26AJ immediate repayment [proved] → **26AK delayed repayment [proved]** →
longer-delay/general overflow [OPEN] → unrestricted CD [OPEN] (+ C.ZIG ≤ A
banked → B ≤ 3A conditional → PIVOT-2/LT/DO conditional-open). Unrestricted
Coarse-Double NOT claimed.

## L. Terminal verdict: PROVED (above). No 26AL launched.
Artifacts: `02_PROVED/26AK_delayed_coarse_double_repayment.md`,
`06_CERTIFICATES/26AK_opposite_branch_displacement.md`,
`06_CERTIFICATES/26AK/{ak_disp.py,ak_deep.py,ak_wit*.py,ak_close*.py,ak_validate.py,
ak_disp.log,ak_deep.log/json,26AK_witness.json,26AK_validated.json,ak_close2.log,
ak_validate.log,ak_wit*.log}`,
`08_PIVOTS/COMPLETED/26AK_delayed_repayment_gate.md` (this report).
