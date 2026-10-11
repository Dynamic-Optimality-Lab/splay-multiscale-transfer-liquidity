# MSINK finalization novelty audit (task H)

## Complete operative bank inventory for R5 words

Coverage mechanisms (each with exact executable test used):
AJ, AK, AL-G, AL-S, AM-G, AM-S, AN (7 direct block predicates, exact per
26AJ/26AK/26AL/26AM/26AN theorems incl. capacities/geometries/disjointness),
AO/AP/AQ/AR/AS (5 unmodified banked recognizers; AO per-leg, AP/AQ/AR merged,
AS merged + pointer push sets + B-depth snaps), NP/S1/S2/VR/MR (5 exact
interval predicates per CDK5NP/S1P/S2P/VRP/MRP frozen classes incl. d_A≥3-K,
strict-P, exception counts, relay/payer shapes, disjointness) = 17.
Structurally inapplicable (documented per witness, not executed):
RT2-A (needs ≤3 KEEP keys; witnesses have 5), CDK4-A (needs ≤4), CDK5L-A
(needs core ≤8; witnesses core 9 throughout). 26AE/AF/AG/AH, U1, CWC are
obstruction/audit results, not coverage classes. No other coverage theorem
exists in `02_PROVED/` + banked certificates for five-key nine-core walks.

## Battery reproduction (unmodified banked code)

`MSINK_battery_selftest.py` rerun at finalization: PASS — 13 synthetic
self-tests; real-word matrix NP-WIT→NP-only, S1W→S1-only, S2-INC→S2-only,
VR-INC→VR-only, MR-INC→MR-only; 28 AJ/AK/AL/AM/AN negatives on real words.
Recognizer modules loaded from banked paths, unmodified (AO/AP/AQ/AR/AS
`recognize` entry points; AR `enrich`; AS push/snap semantics per
26AS valid_AS: dual-push W, t0 depths, kappa flow).
IN battery: 17/17 negative. OUT battery: 17/17 negative.
MR-H6 pinpoint on OUT re-verified from source trace (iv0: x=3, w=1, dA=0,
KEEP a=0; fails K and strict-P). MSINK-H1–H6 on IN re-verified entire
(exists-sinks=[0..3,8..11], min-first-eligible p=0; narrow-H5 via strict-P
on iv0/iv8; joint 1+1+1≤24; telescoping Σw=4≤90=ΣR). OUT MSINK-fail = mixed
gate (t=(2,2)), no H3 strengthening (bound is exactly one-short-one-long).

## Additive closure (exact algorithm, no aperiodicity shortcut)

Subset-partition segment analysis over exact S0 pair-state splits, every part
tested with the full 16-battery + relativized H1 domain (code:
`additive_status`/`part_covered` in finalization verifier):
IN splits=[] → excluded; OUT splits=[] → excluded;
CONCAT splits=[17] → covered partition [(0,17),(17,35)] flags [[S1],[VR]].
Required outcomes all hold. Interior repeats: see aperiodicity audit
(decomposition-impossibility lemma; loop batteries disclosed).

## Historical S1-script discrepancy (out-of-scope, recorded)

- File: `DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_S1_G0/S1_authoritative_replay.py:160`.
- Old assert: `{"A": 33, ...}` for its `INC` word (which equals the NP-WIT word).
- Actual replay today: A=29, Q=18 (both engines agree; closure True).
  (Script raises AssertionError if run; left untouched per directive.)
- Correct S1P fixture: SHA `ff156d94…` (S1W, 17 accesses), replays 33/18/8
  under current engines (control replay PASS), matches `S1P_inclusion_and_
  control_certificate.json` INC_sha.
- No impact on MSINK: all MSINK controls/novelty use proof-dir fixtures
  (S1W/VRW/MRW) re-verified above; the stale G0 assert is never executed by
  the MSINK pipeline (battery uses S1W as S1I with S1=True verified).
