# Distance-zero audit + search manifest (§12/§13)

## Distance-zero (all four seeds classified BEFORE any mutant)

Order: in, ctl, mr33, concat35.
- in (b8b02be7): 55/36/16, primitive, direct [] → strict-DLSS member (E=[4,12],
  t=(2,2), sinks=[0]) → DLSS MEMBER — NOT OUT.
- ctl (6b242e23): 55/36/16, primitive, direct [] → strict-DLSS member
  (E=[4,12], t=(2,2), sinks=[8]) → DLSS MEMBER — NOT OUT (supporting witness).
- mr33 (MR INC): 55/36/16, direct [MR] (+strict-DLSS member coincidentally) →
  PREVIOUSLY BANKED — NOT OUT.
- concat35: 64/36/16, direct [MSINK] (promoted-bank regression), strict
  nonmember, recursive covered → PREVIOUSLY BANKED — NOT OUT.
No qualifying distance-zero OUT (0 eligible, 0 indeterminate) → mutant search
authorized per §13.

## Mutant search frontier (global order: distance, seed, parent, op, index, key)

- in-L1: parents=459 (removal/replacement/insertion over 18 DELETEs, KEEPs
  frozen). Screened idx0–4: idx0 rm0 non-closed; idx1 rm1 non-closed;
  idx2 rm2 DLSS-member; idx3 rm5 AMG-banked; idx4 rm7 OUT-HOPEFUL →
  FROZEN as OUT (a7c6504c…). STOP. in-L1 idx5+ unexecuted (correct early stop).
- Disclosure: ctl-L1 idx0–3 were screened concurrently before the freeze
  registered (idx0 rm0 non-closed; idx1 rm1 non-closed; idx2 rm4 banked;
  idx3 rm6 hopeful de3dff28 — fully classified by the pipeline but
  SUPERSEDED by global order (seed 2 > seed 1); never frozen, never used;
  state files retained as-run for transparency). No mr33/concat35 L1, no L2
  executed anywhere.
- Caps: tested 9 mutants total, distinct 9; per-seed 60k / total 240k caps
  never approached — no truncation (stop was by freeze, not budget).
- Dedup: global sha set (no cross-seed collisions possible — distinct frozen
  KEEP orders per seed — enforced anyway).
- Screening: syntax→replay→closure→R5→strict-DLSS→direct-21→recursive-21
  (recursive only for hopefuls); pointer+tuple lockstep throughout;
  INDETERMINATE would abort (none occurred).
