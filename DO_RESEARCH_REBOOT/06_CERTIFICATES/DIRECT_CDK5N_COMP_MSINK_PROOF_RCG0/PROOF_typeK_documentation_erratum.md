# Type-K documentation erratum (Gate A §6 mandatory audit — NONFATAL)

## The loose phrase

Committed `RCG0_no_double_spend.md` (recursive Gate-0) describes the IN sink
as "K-eligible by H=13". Strict Type K requires d_A(x_j)≥3; the recorded sink
(iv0: x=3, H=13, q=3) has KEEP-leg d_A=0. Taken literally as a membership
claim, the phrase is FALSE.

## Why nonfatal (verified, not assumed)

1. The universal joint payment (L4) uses only H_p≥3 (R_p≥4) and q_p≤4
   arithmetic — 2+w_p≤R_p over the full q_p table. No Type-K premise enters
   L4 for the sink. The sink's d_A is irrelevant to the joint inequality.
2. Disjointness (L6) assigns p to the triple only; p is excluded from the
   singleton loop, so its pseudo-"K-eligibility" is never charged as a
   singleton credit. No double spending is possible from the phrase.
3. The only other-positive interval on the certified witness (iv8) satisfies
   STRICT Type P (preceding D4, distinct key, both a≥1 — recomputed from
   source legs), so no payment step depends on a misclassified K either.
4. The universal L5 proved here applies strict predicates first (hypothesis
   H5 → d_A≥3/prev-DELETE facts → H≥2 → paid). "H≥2" appears only as a
   consequence, never as the definition of K.
5. Corpus-wide: zero strict-vs-proxy discrepancies (384/384), so no archived
   classification relied on the loose reading.

## Disposition

Explanatory error only. The universal proof as reconstructed is unaffected.
Historical file left untouched per preservation rules. No STOP condition met.
