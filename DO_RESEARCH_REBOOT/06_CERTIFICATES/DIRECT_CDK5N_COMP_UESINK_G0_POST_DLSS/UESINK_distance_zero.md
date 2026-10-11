# Distance-zero five-seed audit (all classified BEFORE any mutant)

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
0 qualifying OUT, 0 indeterminate → mutant search authorized.
Record: UESINK_distance_zero.json (re-runnable driver: UESINK_driver.py).
