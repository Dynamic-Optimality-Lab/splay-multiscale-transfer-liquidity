# DIRECT-CDK5N-COMP-MSINK-G0-R1HARD verdict: GATE 0 PASS (OUTCOME A)

## Verdict

MSINK shared-sink joint-payment class is PROVED non-empty and proper: IN
(`19ff110a7c60`, 61/36/16, MSINK-member) and OUT (`b8b02be76c04`, 55/36/16,
R5-non-MSINK) witnesses, both five-key nine-core closed aperiodic walks outside
all 17 banked mechanisms and additive closure. Universal payment L1–L7 covers
the frozen joint H4–H5 rule. No promotion beyond Gate 0 claimed.

## Rule checks

- R1 STRICTLY SMALLER: IN satisfies five-key + core9 + exactly-two-exception +
  mixed (0,2) relays + joint H4–H5 sink (p=0,H=13) + K/P others (L1–L7 verified
  on the word). Disjointness executed: IN outside NP/S1/S2/VR (battery False),
  outside MR (t=0 vs H3 all-long), outside AJ/AK/AL/AM/AN + AO/AP/AQ/AR/AS.
  OUT in R5∖S_raw (t=(2,2) breaks mixed gate) also fully excluded. Properness
  witnessed both sides.
- R2 SOLVABILITY: L1–L7 (`MSINK_universal_payment_proof.md`): baseline,
  debt classification (nine-core q<=4), exceptions (1,0)x2, joint sink
  (1+1+w_p<=R_p explicit), others (explicit w<=R each + K/P case), disjoint
  triple+singletons, telescoping to Q_B<=2A. Bounded, explicit, no oracle.
- R3 ONE-PROMPT SCOPE: one theorem, one mechanism, one deterministic campaign
  (2 seeds, DELETE-only, edit-dist asc, fixed op order, sha-dedup), one pair.
  Enumeration STOPPED at L0L1 by early-stop (both roles frozen): 956 distinct
  words (496 concat35 + 460 mr33) << caps (250k/seed, 500k total). No L2 run.
- R4 UPWARD PROGRESS: IN in S_raw∩R5; OUT in R5∖S_raw; neither is an old
  control (both n=34 mutants, shas pinned); banked union (12 exact membership
  predicates + 5 unmodified recognizers incl. pointer-push AS) + additive
  closure (aperiodicity: 35 distinct pair-states each) excluded. W=4 noted;
  residual status via full exclusion, never via W alone.

## Campaign record

- Seeds: concat35 (S1-half + VR-half, closed 64/36/16, split@17) and mr33
  (MR INC, closed 55/36/16). Entry verified; controls replay PASS (S1/VR/
  concat totals + additive regression at split 17).
- L0L1 census: 956 tested; 422 closed, of which 420 R5 survivors (2 rejected:
  non-R5/badblocks; none A0, none 4-recognizer-banked). The layer-0 mr33 seed
  (MR-covered old control)   sits among survivors and was skipped per R4. Survivors: 179 msink-tractable
  (152+27), 241 nonmsink-tractable (23+218).
- Landscape: IN-tractable 45, ALL 16-clean (first=19ff110a, frozen).
  OUT-tractable 207: 132 MR / 67 VR / 5 MR+AMG+AMS / 1 VR+AMG+AMS / 2 CLEAN
  (first=b8b02be7, frozen; spare 6b242e23).
- Battery (`MSINK_battery_selftest.py`): 13 synth + 5 real-word matrices
  (NP/S1W/S2/VR/MR INCs each exactly-one-True) + 28 real-word negatives: PASS.
- Attacks (`MSINK_attacks.py`, 41): 12 closed, all Q<=2A, payment identities
  hold wherever msink fires; neighbors fall into MR/VR/NP or spare
  MSINK/R5-clean words (reported, L2, consistent). PASS, 0 hard fails.
- Harness validated before discovery (4 recognizer positives ACCEPT through
  project block builders; CONCAT msink-True correctly flagged additive).

## Files (all under 06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/)

Charter, semantics, no-double-spend, universal proof L1–L7, controls replay
(+json), bounded-search engine, membership battery (+selftest), pointer audit,
worksheet builder, reasons printer, rescreener, attacks (+json), IN/OUT
worksheets, state_concat35/{seen,census,survivors,parents}, state_mr33/{...},
audit/worksheet JSONs for both witnesses. Ledger + dependency updates pending
with this verdict.

## Observations (no impact on verdict)

- S1_G0/`S1_authoritative_replay.py` at HEAD asserts A=33 for its INC word but
  current engines give A=29 (script fails if run; stale assert). The PROVED S1
  witness is the S1P-certificate word ff156d94 (used in our battery as S1I).
  MSINK uses only proof-dir fixtures; unaffected. Flagged, not fixed (out of
  scope).
- `merged_blocks` rotates to first a>=1 leg (cyclic AJ-block exactness); block
  `l1` stored as original index+1 so AS snaps stay correct. Validated via
  witness-ACCEPT harness.

## Scope

Exactly the frozen MSINK class. No nine-core complement, no K>=6, no universal
Q_B<=2A, no Dynamic Optimality. Universal Coarse-Double and DO remain OPEN.
