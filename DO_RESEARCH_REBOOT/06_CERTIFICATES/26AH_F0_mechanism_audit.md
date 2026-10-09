# 26AH F0-mechanism audit (gate companion)

## Target
`D_0 = −2 + ΔF_0`, `ΔF_0 = J[(F0,1,0,3)] − J[(F0,−1,0,3)]`, pair (1,3) in
`B_0=[5,[4,[2,[1],[3]],None],None]`. Need `ΔF_0 ≥ 0` or `ΔF_0 ≤ 4` from
independently justified premises (UG + normalization insufficient — 26AD exact).

## Candidate A — F0 key semantics / pair symmetry
Measured: (1,3): slot `('F',0)`, λ=+1; (3,1): slot `('F',0)`, λ=−1 (LL vs LR
fold patterns; source-structural). Same slot family, mirrored λ. NO source
identity relates λ=+1 to λ=−1 values (UG links 2↔1 only). Tree mirror symmetry
does not bind free J values. **FAIL** (no relation).

## Candidate B — DTQ forms (6 raw forms mention these keys)
Provenance: `j4_shiftdeep.json` (26 raw forms, meta/sup/fams/terms, no proof header);
`j4_dtqaug.json` (`neqs: 2`, joint feasible margin −0.0). Banked status across
26-core narrative: "currently chosen", "COMPATIBLE" — optional subclass, never
proved mandatory. Mere occurrence of F0 keys in a form is not justification.
**FAIL** (reaffirmed exclusion; no new derivation attempted per charter).

## Candidate C — SELF / prerequisite rows touching ΔF₀
Exact incidence (machine-checked): kA in DIAM (5,1),(4,1),(2,1),(1,5),(1,4),(1,2),
(1,3) + SELF x=1 Jat part; kB mirror + SELF x=3. Every touching row is either a
target pair row (excluded as circular) or a feasibility-grade SELF/DIAMETER row
whose use as an inequality premise requires global J existence (open).
**FAIL** (no feasibility-free row).

## Candidate D — structural symmetry / monotonicity / sign
No source function (slot_of, R_coeffs, H0, Jy) yields a sign or order relation
between free J values at distinct keys. Shiftval/SHMAP concern λ-transport maps,
not value bounds. **FAIL** (nothing to invoke).

## Free-direction status (unchanged)
`v = +1@(F0,1,0,3) −1@(F0,−1,0,3)`: `Ev=0`, `βv=2` under UG+normalization.
No candidate above restricts it. No exact obstruction to global J existence is
claimed (that would need feasibility analysis, out of gate scope).
