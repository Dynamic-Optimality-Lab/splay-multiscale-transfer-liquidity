# Distance-zero six-seed audit (all classified BEFORE any mutant)

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
search authorized per §13. Record: ZULR_distance_zero.json (re-runnable
driver: ZULR_driver.py). Priority (mutually exclusive): INVALID >
non-R5 > MEMBER > BANKED-direct > BANKED-recursive > OUT-eligible.
