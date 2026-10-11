# Distance-zero audit + search manifest (§12/§13)

## Distance-zero (all five seeds classified BEFORE any mutant)

Order: in, exIN, exCTL, mr33, concat35. Pointer+tuple lockstep replay.
- in (a7c6504c, 33 acc, 56/36/16): closed, engines agree, genuine
  {1,3,5,7,9}, core9 ×34, primitive (32 distinct) → strict UESINK member
  (E=[12], t=2, sinks=[0]) → UESINK MEMBER — NOT OUT.
- exIN (b8b02be7, 34 acc, 55/36/16): direct [DLSS] (strict-DLSS member;
  E=[4,12] so UESINK-H2 fails) → PREVIOUSLY BANKED — NOT OUT.
- exCTL (6b242e23, 34 acc, 55/36/16): direct [DLSS] → PREVIOUSLY BANKED.
- mr33 (MR INC, 33 acc, 55/36/16): direct [DLSS, MR] (multi-membership
  recorded) → PREVIOUSLY BANKED.
- concat35 (35 acc, 64/36/16): direct [MSINK] (promoted-bank regression),
  strict nonmember, recursive covered → PREVIOUSLY BANKED.
No qualifying distance-zero OUT (0 eligible, 0 indeterminate) → mutant
search authorized per §13. Record: UESINK_distance_zero.json.

## Mutant search frontier (global order: distance, seed, parent, op, index, key)

- in-L1: 442 distinct parents (459 raw − 17 insertion collisions beside
  existing identical DELETEs; dedup by canonical content, first-seen order).
  Screened idx0–8: idx0 rm0 non-closed; idx1 rm1 non-closed; idx2 rm2
  UESINK-member; idx3 rm5 UESINK-member; idx4 rm7 MSINK-banked; idx5 rm13
  non-closed; idx6 rm14 non-closed; idx7 rm17 non-closed; idx8 rm19
  OUT-HOPEFUL → FROZEN as OUT (593b3f3ac561). STOP. in-L1 idx9+ unexecuted
  (correct early stop).
- No exIN/exCTL/mr33/concat35 L1, no L2 executed anywhere.
- Caps: tested 9 mutants total, distinct 9; per-seed 60k / total 300k caps
  never approached — no truncation (stop was by freeze, not budget).
- Dedup: global sha set (no cross-seed collisions possible — distinct frozen
  KEEP orders per seed — enforced anyway).
- Screening: syntax→replay→closure→R5→strict-UESINK→direct-22→recursive-22
  (recursive only for hopefuls); pointer+tuple lockstep throughout;
  INDETERMINATE would abort (none occurred).
