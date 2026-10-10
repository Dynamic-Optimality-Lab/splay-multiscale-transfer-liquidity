# GATE0 Rule 2 audit — interval-charging proof (MECHANISM SOUND)

Verified line by line against source definitions (KEEP splays A+B, DELETE
splays A only, a=⌈d_A/2⌉, KEEP q=⌊d_B/2⌋, DELETE q=0, exact closure).

1. **Partition.** Cyclic KEEP intervals I_j are disjoint and cover every access
   (each access follows exactly one preceding KEEP). ✓
2. **Baseline H_j≥c_j.** After prev KEEP, A is rooted at x_{j−1} (KEEP splays A).
   If c_j=1 (x_j≠x_{j−1}), some access in I_j changes A's root ⇒ d_A≥1 ⇒ a≥1
   there ⇒ H_j≥1=c_j. If c_j=0, H_j≥0. ✓ First such StepEv is the baseline;
   the rest is extra credit, never reused (disjoint intervals). ✓
3. **Reserve identity.** ΣH_j=A, Σc_j=C_K ⇒ ΣR_j=2(A−C_K), seams included. ✓
4. **Debt bound.** Nine nodes ⇒ d_B≤8 ⇒ q≤4. c_j=0 ⇒ B still rooted at x_j
   (DELETEs freeze B) ⇒ q_j=0 ⇒ w_j=0. Positive debt needs c_j=1, q_j∈{3,4} ⇒
   0<w_j≤2 with no A-depth assumption. ✓
5. **Type K.** d_A≥3 ⇒ a_j=⌈d_A/2⌉≥2 ⇒ H_j≥2. ✓
6. **Type P.** Preceding DELETE y≠x_j lies in I_j (it follows prev KEEP, else
   the preceding occurrence would be that KEEP); a(D_y)≥1 plus a(K_j)≥1 are
   two distinct accesses in I_j ⇒ H_j≥2. Same-key shadows correctly rejected
   (y≠x_j required). ✓
7. **Local payment.** c_j=1: R_j=2(H_j−1)≥2≥w_j. w_j≤0: R_j≥0≥w_j. ✓
8. **Telescoping.** Σw_j=Q_B−2C_K≤ΣR_j=2(A−C_K) ⇒ Q_B≤2A, arbitrary n/length. ✓

**Verdict: Rule 2 PASS.** The charging proof is complete and sound for eligible
walks. (It is not promoted to a theorem here: eligibility coverage failed at
Rule 4. No potential, matching, or E/S content used.)
