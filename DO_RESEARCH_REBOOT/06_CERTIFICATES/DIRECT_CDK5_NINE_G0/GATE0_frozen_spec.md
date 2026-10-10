# GATE0 frozen spec — CDK5N-DP (v1.0, frozen before testing, unaltered after)

**Class.** Source-valid reachable exactly-closed pair-walks with: exactly five
genuinely-accessed KEEP keys; complete marked B-core size exactly nine at every
cyclic state; every KEEP occurrence with w_j=q_j−2c_j>0 satisfies Type K or
Type P below. No conclusion assumed; eligibility is source-observable only.

**Intervals.** Cyclic KEEP list K_1..K_s; I_j = (prev KEEP, .., KEEP j].
c_j=1[x_j≠x_{j−1}]; q_j=⌊d_B/2⌋; H_j=Σ_{t∈I_j}a_t; w_j=q_j−2c_j; R_j=2(H_j−c_j).

**Type K.** d_A(x_j)≥3 immediately before KEEP j (⇒a_j≥2, H_j≥2).
**Type P.** Immediately preceding full-word occurrence is DELETE y≠x_j with
a(D_y)≥1, and a(K_j)≥1 (two distinct accesses in I_j ⇒ H_j≥2).
Type D same-key shadows permanently excluded (no such rule exists).

**Claim (to be proved in a future run, NOT here).** Eligible walks satisfy
Q_B≤2A. Gate 0 does not prove it; Gate 0 audits the mechanism (Rule 2) and
freezes the target.
