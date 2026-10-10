# 26AS: source-derived shared-credit allocation (universal theorems PROVED; OUTCOME B)

**Status: universal restricted theorems PROVED; strict novelty NOT certified
(complete precommitted hunt negative) — FINAL VERDICT: OUTCOME B.** No J4, ROW-DIAMETER, J-SELF, DTQ, UG, potentials, LP, or compactness. Private
A-depth thresholds are openly declared restricted-domain hypotheses (§12
equivalence stated); κ is a bound-saving, never a spendable sink.

## 26AS-L1 — coupled straddling displacement (PROVED universally)

For r<y<s: d_{S_y}(r)+d_{S_y}(s) ≤ d(r)+d(s)+2. Proof: six rotation-case
region tables (gaining regions y-monochromatic; every gain enters y's
subtree; inside-future ≤0; max single gain +2; no dual-gain step) +
entering-step composition (total ≤ first-gainer's gain ≤2). Full proof:
`06_CERTIFICATES/26AS/26AS_coupled_root_universal_proof.md`. Corroboration:
18136 triples / 5448 steps exhaustive, both engines.

## 26AS-L2 — multi-splay conservation (PROVED by induction)

Tracked r,s, interval of h genuine B splays avoiding both, g straddling
(key strictly between): d(r)+d(s) ≤ d_r^0+d_s^0+4h−2g. Each non-straddling
non-target splay: separate 26AL-L1 per node (+4); each straddling: L1 (+2).
B-root no-ops excluded (not genuine). L1's strict r<y<s matches g's
strict-between count.

## Parity identity (PROVED arithmetically; fuzz-verified)

U_r=⌊(d_r^0+2h)/2⌋, U_s=⌊(d_s^0+2h+2)/2⌋ (+2 levels for KEEP r between),
U_rs=⌊(d_r^0+d_s^0+4h−2g+2)/2⌋: U_r+U_s−U_rs = g−ε with ε=1 iff both initial
depths odd (α+β−γ=2ε by parity case split). κ=g−ε≥1 is source-computable.

## 26AS-E — dual-push eligibility (PROVED from trace semantics)

Push_B(W) = union of source-emitted pushed ancestors (verified: equals the
exact proper-ancestor set on all shapes n≤8... n≤7 corpus). E1 (strict order,
1≤dB≤3, genuine, post-runs pre-returns) + E2 (r,s ∈ Push and on path) ⟹ both
anchors are proper ancestors at W (hence rotation participants, active
lifetimes separately checked, opposite sides of new root y by key order).
Key order alone insufficient (Test C: between-key off-path anchor REJECTED).
Edges P_r↔W, P_s↔W admitted only after E1–E3; private returns single-group.

## Hall cuts (PROVED conclusions; A-depths admitted as restrictions)

C_R=2a_r−q_r ≥ m_r−1, C_S ≥ m_s−1 (thresholds ⟺ exactly these; stated
explicitly), C_W ≥ 1 (shallow). Cut1/2: +C_W. Union: C_R+C_S ≥
(2a_r−U_r)+(2a_s−U_s)+κ ≥ (m_r−1)+(m_s−1)+κ, plus C_W ≥ m_r+m_s. κ only
strengthens private bounds (never a separate sink). Integral allocation
constructed explicitly (frW=max(0,m_r−C_R), fsS=min(m_s,C_S); cuts imply
feasibility); fuzz-verified. Flow uses W at most once; no double-spend.

## Global ASmix theorem (PROVED)

C_ASmix: disjoint partitions into banked-exact ARmix packets (validators
imported verbatim), AS components (above), nonpositive singletons; all
positives covered; shared capacities spent once. Each piece ≤0 (banked
theorems / Hall+allocation); Σδ≤0 ⟹ Q_B≤2A. C_ARmix⊆C_ASmix (executed:
AP Direct p=3, AQ Bridge, AR Split all ACCEPTED unchanged). Admissibility
not claimed universal. Recognizer: all-cuts × DP, sound/complete/rotation-
invariant (self-tests 10/10).

## Scope

Two maximal unit-positive groups, one dual-push W (C_W≥1), consecutive
private returns, κ≥1. NOT covered: more groups, non-unit deficits,
multi-shared-sinks, general allocation, unrestricted Coarse-Double.
Downstream unchanged.
