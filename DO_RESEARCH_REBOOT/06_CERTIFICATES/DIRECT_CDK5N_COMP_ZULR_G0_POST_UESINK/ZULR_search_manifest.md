# Distance-zero audit + search manifest (§12/§13)

## Distance-zero (all six seeds classified BEFORE any mutant)

Order: in, exin, exdlss, exctl, mr33, concat35. Pointer+tuple lockstep replay.
- in (593b3f3a, 32 acc, 56/36/16): closed, engines agree, genuine
  {1,3,5,7,9}, core9 ×33, primitive (32 distinct) → strict ZULR member
  (E=[], p=0 H=18, others strict-K/P) → ZULR MEMBER — NOT OUT.
- exin (a7c6504c, 33 acc, 56/36/16): direct [UESINK] (strict-UESINK member;
  E=[12] so ZULR-H2 fails) → PREVIOUSLY BANKED — NOT OUT.
- exdlss (b8b02be7, 34 acc, 55/36/16): direct [DLSS] → PREVIOUSLY BANKED.
- exctl (6b242e23, 34 acc, 55/36/16): direct [DLSS] → PREVIOUSLY BANKED.
- mr33 (MR INC, 33 acc, 55/36/16): direct [DLSS, MR] (multi-membership
  recorded) → PREVIOUSLY BANKED.
- concat35 (35 acc, 64/36/16): direct [MSINK] (promoted-bank regression),
  strict nonmember, recursive covered → PREVIOUSLY BANKED.
No qualifying distance-zero OUT (0 eligible, 0 indeterminate) → mutant
search authorized per §13. Record: ZULR_distance_zero.json (priority:
INVALID > non-R5 > MEMBER > BANKED-direct > BANKED-recursive > OUT-eligible).

## Mutant search frontier (global order: distance, seed, parent, op, index, key)

- in-L1: 425 distinct parents (dedup by canonical content, first-seen order;
  removals/replacements/insertions over 16 DELETEs, KEEPs frozen).
  Screened idx0–4: idx0 rm0 non-closed; idx1 rm1 non-closed; idx2 rm2
  NP-banked; idx3 rm5 ZULR-member; idx4 rm7 OUT-HOPEFUL → FROZEN as OUT
  (8cd970c71989). STOP. in-L1 idx5+ unexecuted (correct early stop).
- No exin/exctl/mr33/concat35 L1, no L2 executed anywhere.
- Caps: tested 5 mutants total, distinct 5; per-seed 60k / total 300k caps
  never approached — no truncation (stop was by freeze, not budget).
- Dedup: global sha set (no cross-seed collisions possible — distinct frozen
  KEEP orders per seed — enforced anyway).
- Screening: syntax→replay→closure→R5→strict-ZULR→direct-23→recursive-23
  (recursive only for hopefuls); pointer+tuple lockstep throughout;
  INDETERMINATE would abort (none occurred).
