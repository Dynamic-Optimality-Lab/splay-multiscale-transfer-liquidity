# S1-L3/L4/L5: exception, successor, others (PROVED)

## S1-L3 (exception)

c=1,q=3,H=1 ⇒ w=1, R=0. Type K would need d_A≥3⇒a≥2⇒H≥2 — fails. Type P would
need two distinct costly accesses in I (H≥2) — fails with H=1. So the exception
is outside CDK5NP-A universally (H=1 excludes both, not just at witness K5).
Genuine underfunded debt (w=1>0=R).

## S1-L4 (successor, full q_k≤3 range)

c=1,q≤3,H≥2 ⇒ w=q−2≤1 (covers w_k<0: q≤1; w_k=0: q=2; w_k=1: q=3 — all three),
R=2(H−1)≥2. Pair: w_*+w_k≤1+1=2≤0+2=R_*+R_k. Successor needs no Type K/P;
no borrowing beyond k; fixed distance 1 (mod s).

## Other intervals (§9)

w≤0 ⇒ R≥0 (L1). w>0 + Type K: d_A≥3⇒a≥2⇒H≥2⇒R≥2≥w (w≤2). w>0 + Type P:
preceding DELETE y≠x in same I (it follows prev KEEP, else the preceding
occurrence would be that KEEP) with a(D_y),a(K)≥1 ⇒ H≥2 ⇒ R≥2≥w. Overlap
(K∧P) charged once (one inequality per interval; H fixed). Hypotheses exhaust
positive debts outside the pair. ∎
