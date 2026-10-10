# GAP AJ–AS domain-exclusion report — ALL EXCLUDED

Witness: 17-access nine-core walk (A=29,Q=18,C_K=8,W=−40, core 9, closure,
engines agree). Positives: K3 (blk 2, r=9), K5 (blk 8, r=9). h=2 both.

## Cardinality/size/baselines — EXCLUDED (verified, not assumed)

RT2-A (5>3), CDK4-A (5≠4), CDK5L-A (core 9>8). n=9 keys (n≤6 ✗). Positive dB=6
(depth≤5 ✗). A=29 (zero-A ✗).

## AJ — EXCLUDED (both)

Successor blocks: K3→K7 (7≠9), K5→K7 (7≠9). Former-root successor absent.

## AK/AL-G/S — EXCLUDED (both)

Second successors: K3→K1 (1≠9), K5→K1 (1≠9). Delayed-return identity fails;
capacity/S-triple moot. (AL-S⊆AL-G by banked containment.)

## AM-G/S — EXCLUDED (both, independently)

K3: G4 fails (D4≠9). K5: G5 fails (2a=2<3). Full G-tables in AM audit file.
AM-S fails (nonzero intermediates).

## AN/AO — EXCLUDED

Positives at blocks 2,8 (gap 5): not consecutive; zero Type-I/II matches at
all 17 cyclic positions (machine-checked); 26AO recognizer REJECTS.

## AP — EXCLUDED

Maximal +1 runs [2],[8] (length 1; neighbors nonpositive); successors K7≠9.
26AP recognizer REJECTS.

## AQ — EXCLUDED

Two length-1 runs, positive-run total 2 < 3 bridge minimum. 26AQ REJECTS.

## AR — EXCLUDED

No positive run ≥3. 26AR recognizer REJECTS.

## AS — EXCLUDED

Both anchors r=s=9 (distinctness required). 26AS recognizer REJECTS.

## Executable summary

26AO/26AP/26AQ/26AR/26AS: all REJECT (unmodified banked implementations,
hashes in outputs JSON; correct block+snap reconstruction, 17 blocks).

## Verdict

W_* ∉ C_old (complete union). Local compatibilities reported honestly (G1–G3
pass where they pass); no local pattern promoted to global cover.
