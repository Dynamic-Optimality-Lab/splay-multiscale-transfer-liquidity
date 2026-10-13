# AF-1..AF-4 proof record (Steps 04-07)

## AF-1 cone-cut substitution (STEP 04): PROVED

Induction over primitive rotations: accessed targets/pivots lie in retained
region (L1/L2: depth ≤4 < frontier ≥7; fuzz-verified); opaque blocks move
rigidly (rotation code; step-type agreement verified); output top-3 from
initial ≤6 (L5: displacement ≤4). No prune-then-splay commutation assumed
(Control F honored). Evidence: AFSP_FUZZ (572 corrected-sequential cases)
+ G/J (60) + B-side projected successors (30,773), 0 mismatch.

## AF-2 integer allocation (STEP 05): PROVED

Max-flow lower-bound circulation; exact demand equations p_i+Σz=σ_i;
S-less-nonempty lower bounds; interval compatibility; S uniqueness.
Soundness+completeness vs brute force 80/80; reconstruction valid 64/64
(frozen inorder+balanced rebuild). Evidence: AFSP_allocate.py +
AFSP_AF2_SELFTEST.json.

## AF-3 saturated pumping (STEP 06): PROVED (stated discipline)

Reservoir extends OCCUPIED deep frontiers below active cone only (never
fills empty holes); preserves depths/costs/steps/H/S-skeleton/emptiness/
signature. Tests: AFSP_pump2 (30 occupied-extension cases) + saturation
fuzz (gaps to 2000 keys) + boundary sweep (264/265/266/267), 0 mismatch.
Development failures correctly classified as test artifacts (chain-into-
empty-hole variant; β-renumbering), not mechanism refutations. Integer-tight
intervals: below-cone room argument (true fit ⇒ capacity; loud failure if
insufficient — never triggered).

## AF-4 guard factorization (STEP 07): PROVED (construction + solver)

Templates (prefix, word, B-transition, S-assignments) + AF-2 integer guard;
guard theorem (satisfiable ⟺ realizable) via AF-2 biconditional + AF-1
substitution; Catalan completions never enumerated. H=1 kernel: 5,280
templates over canonical 9-key shadows (all step cases; D(v)+K(v) pattern
included after correcting an enumeration exclusion).
