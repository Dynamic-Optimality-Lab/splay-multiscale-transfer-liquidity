# Frozen OUT complete residual audit (tasks G3 + L)

Word (34 accesses, A=55, Q=36, Ck=16):
`D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9`
SHA `b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3`.

Fresh dual-engine replay: closed exact, engines agree, genuine keys
{1,3,5,7,9}, core 9 at all 35 boundaries. All 34 pre-closure pair states
pairwise distinct (F7 primitive — independently verified, not presumed).

Strict MSINK: E=[4,12], relays (2,2) → fails mixed gate (no short relay).
Stage `mixed-relay-[2,2]`. Non-member under frozen H3 (no strengthening:
bound is exactly one-short-one-long).

Direct banked (20 mechanisms, pointer-push AS): all negative. In particular
MR-H6 fails at interval 0 (x=3,q=3,w=1,dA=0,KEEP a=0: not K, strict-P needs
a≥1 both); NP/S1/S2/VR fail (|E|=2 + exception H=1); AJ/AK/AL/AM/AN fail
(successor/plus-2/plus-3 ≠ rb 9; zero valid AN packets); AO/AP/AQ/AR/AS
executable REJECT.

Cyclic additive: primitive (F7) → no ≥2-partition exists; DP confirms
(34 rotations exhausted, 0 closed segments). Whole-word battery
rotation-invariant (4 rotations tested identical).

## Verdict: OUT `b8b02be7` REMAINS IN THE CORRECTED RESIDUAL (CRA-C).

Negative-coverage certificate: `CRA_corpus_classification.jsonl` record
(status CORRECTED-RESIDUAL/NON-MSINK) + regression record
`CRA_cyclic_coverage_regressions.json`. Q−2A = −70 (no violation signal).
