# Post-UESINK 384-word census (bank-23 reconstruction)

Engine: bank-23 direct battery (20 + MSINK-exists + DLSS-exists +
UESINK-exists at every test) + recursive C23* DP (nested rotations,
memo-exact, budgets untouched) + strict-ZULR comparison.

## Result: 378 DIRECT-BANKED + 6 CYCLIC-ADDITIVE-BANKED + 0 residual = 384.

Covered: 384. Uncovered: 0. Disjoint categories, sums verified.
Direct flags (multi-membership): MSINK 160, DLSS 125, MR 122, UESINK 73,
VR 73, AMG 9, AMS 6, NP 8, S1 12. (RT2/CDK4/CDK5L fire on no whole word —
all survivors carry five keys + core9; small-domain paths implemented and
exercised via A0-trivial segments + synth positives.)
6 cyclic, all depth 1.
UESINK min-first vs exists: verified equivalent on census rerun (both 73 —
no missed UESINK coverage from the screening proxy).
Strict-ZULR members in corpus: recorded per residual (none — every
ZULR-shaped word is bank-23-covered; hence the mutant search for OUT).
0 INDETERMINATE, 0 SOURCE-INVALID, 0 budget hits.

Record: ZULR_post_uesink_census.json (per-word status + mechanisms).
Finite corpus statement only; no universal closure claim.
