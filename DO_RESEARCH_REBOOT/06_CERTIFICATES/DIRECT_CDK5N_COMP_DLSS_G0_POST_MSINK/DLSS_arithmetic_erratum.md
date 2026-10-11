# Arithmetic documentation erratum (§15, append-only)

## Finding 1 — OUT Q−2A misattribution (CONFIRMED, corrected here)

`CRA_OUT_complete_residual_audit.md:29` reports "Q−2A = −70" for OUT
(`b8b02be7`). Recomputed from source totals (A=55, Q=36, verified by fresh
replay): **Q−2A = 36−2·55 = 36−110 = −74.** The −70 value belongs to another
corpus word's range endpoint (corpus range was [−100,−70]) and was
misattributed to OUT. Historical file left untouched. No violation either
way (−74 < 0); positive Q−2C_K (=4) never implied one (different quantity).

## Finding 2 — Type-K shorthand (CONFIRMED, nonfatal)

Old notes sometimes wrote "Type K follows from large H". Strict Type K is
d_A≥3 ONLY (H≥2 is its consequence for payment, never its definition).
This campaign uses strict predicates exclusively (0/384 discrepancies in
the prior audit; strict re-verified here); no classification relied on the
shorthand.

## Frozen values (authoritative recomputation)

OUT (b8b02be7): A=55, Q=36, C_K=16; Q−2A=−74; Q−2C_K=4.
OUT-new (a7c6504c): A=56, Q=36, C_K=16; Q−2A=36−112=−76; Q−2C_K=4.
Neither violates Q≤2A.

## Filing note

This erratum was written during the campaign but found missing from the
Gate-0 commit; it is filed here by append-only follow-up with no other
changes. Content identical to the campaign record.
