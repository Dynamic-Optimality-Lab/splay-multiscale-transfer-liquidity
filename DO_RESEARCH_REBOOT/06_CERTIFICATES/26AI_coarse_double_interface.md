# 26AI Coarse-Double interface reconstruction (gate companion)

## Exact theorem (stage_04_coarse_double.md)
`Q_B(γ) ≤ 2A(γ)` for every reachable closed present-key pair walk γ
(diagonal start T0, arbitrary length). Q_B counts B-doubles; A counts all A
StepEvs incl. DELETE. Constants: 2, no startup term on cycles. Status OPEN
(n≤6 analytic via PIVOT-12 cycle ratios + zero-A theorem; n≥7 open).

## ROW-DIAMETER interface (THE ROW-DIAMETER INTERFACE)
Source: `02_PROVED/J4_CONDITIONAL_SUFFICIENCY.md:11-14,27-35`,
`01_MAIN_PIPELINE/stage_06_row_diameter.md:7`,
`scripts/wp6_j4shared.py:94-150` (row constructors).
- **Adjusted ROW**: `H_r(B) − H_x(B) ≥ −2 + 2(b_r − b_x)` ∀ distinct ordered (r,x),
  ∀ finite BST, one shared J. (Nonroot pairs: symmetric [−2,2] via both orders;
  root/nonroot: raw [0,4].)
- **J-SELF**: `H_x(B) − H_x(S_xB) ≥ R_static(B,x) − 2(1−b_x)` (`stage_07`; OPEN).
- **Use in KEEP step** (x≠r, a=ceil(d_A/2)≥1): residual `R_static−2a−2(1−b_r)`
  paid by J-SELF + ROW in the form `H_r−H_x ≥ −2a+2(b_r−b_x)` (follows from
  ROW since a≥1 ⇒ −2≥−2a); x=r (a=0) by J-SELF alone. DELETE analogous.
- **Telescoping**: `q−2a ≤ Φ−Φ'` per edge with shared Φ ⇒ sum over closed walk = 0.
- Static mechanics identity (`R_static` = depth-drop) assumed; separately recorded.

## Dependency graph (minimal, source-derived)
CD ← per-edge Φ-telescoping ← {J-SELF (OPEN), ROW −2a-form (OPEN), static
mechanics (assumed), shared Φ/J (OPEN), closed-walk quantifiers}.
Neither J-SELF nor ROW is separately dischargeable now. 26AE/26AF zero-families
cover fixed pairs, not walk-edge classes. SHMAP/quotient machinery is not in
this deduction path.

## One-sided relaxation audit (exact)
The staged interface quantifies over EVERY ordered distinct pair ⇒ both orders
required for nonroot pairs ⇒ symmetric [−2,2] already at the interface. A
walk-restricted one-sided variant would need a reachability theorem (which
orders occur in closed walks) with no source basis; 2-cycle closedness is
unproven. REJECTED (not weaker where needed; unproved where restricted).

## Direct-component audit
- x=r edges: need J-SELF (OPEN) ⇒ not now.
- Zero-A accesses: universally proved already (PIVOT-12 A1) — banked, not new.
- DELETE q=0: per-access trivial (0≤2a) but Φ-edge still needed ⇒ not separable.
- Per-access KEEP bound: FALSE (`(1,3,0)`: q=3 > 2·1, banked) ⇒ amortization essential.
- 26AE/26AF zero pairs: no systematic walk-edge coverage ⇒ no deletion.
- Aggregate escape: needs new telescoping (no source basis); any J-linear walk
  aggregate spans 26AG-free directions (491/510) uncontrolled by EQs.

## F0-filter application (§8)
The 26AD residual direction defeats every equality-only aggregate control; no
aggregate candidate with exact cancellation was exhibited in source. Filter holds.
