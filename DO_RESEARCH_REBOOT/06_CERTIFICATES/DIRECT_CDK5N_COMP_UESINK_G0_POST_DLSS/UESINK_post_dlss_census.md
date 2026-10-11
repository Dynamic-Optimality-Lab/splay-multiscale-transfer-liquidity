# Post-DLSS 384-word census (bank-22 reconstruction, verified figures)

Engine: bank-22 direct battery (20 + MSINK-exists + DLSS-exists at every
test) + recursive C22* DP (nested rotations, memo-exact, budgets untouched)
+ strict-UESINK comparison.

## Result: 378 DIRECT-BANKED + 6 CYCLIC-ADDITIVE-BANKED + 0 residual = 384.

Covered: 384. Uncovered: 0. Disjoint categories, sums verified.
Direct flags (multi-membership): MR 122, DLSS 125, VR 73, AMG 9, AMS 6,
NP 8, S1 12, MSINK 160. (RT2/CDK4/CDK5L fire on no whole word — all
survivors carry five keys + core9; small-domain paths implemented and
exercised via A0-trivial segments + synth positives.)
6 cyclic, all depth 1.
DLSS min-first vs exists: 125 == 125 (equivalent on all 384 — no missed
DLSS coverage from the screening proxy).
Strict-UESINK members in corpus: 73, all bank-22-covered (hence no archived
OUT candidate; mutant search required and executed).
Both former residuals (b8b02be7, 6b242e23) now DIRECT via DLSS only.
0 INDETERMINATE, 0 SOURCE-INVALID, 0 budget hits.

Record: UESINK_post_dlss_census.json (per-word status + mechanisms).
Finite corpus statement only; no universal closure claim. (Census re-ran
byte-identically; mechanism figures above independently recomputed.)
