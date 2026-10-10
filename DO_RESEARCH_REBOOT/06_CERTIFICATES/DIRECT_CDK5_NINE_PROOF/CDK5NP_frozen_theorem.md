# CDK5N-DP frozen theorem (v1.0 — identical to CDK5NG-A authorization)

**Domain.** Arbitrary original-source admissible, reachable, exactly closed A/B
pair-walks W with: (i) exactly five genuinely accessed KEEP keys (|supp|=5);
(ii) complete marked B-ancestor core size exactly nine at every cyclic state;
(iii) every KEEP occurrence with w_j=q_j−2c_j>0 satisfies Type K or Type P.

**Intervals.** Cyclic KEEP order K_1..K_s; I_j = (prev KEEP,..,KEEP j];
c_j=1[x_j≠x_{j−1}]; q_j=⌊d_B(x_j)/2⌋; H_j=Σ_{t∈I_j}a_t; w_j=q_j−2c_j;
R_j=2(H_j−c_j). a_t=⌈d_A/2⌉; KEEP q as above; DELETE q=0; depths pre-access.

**Type K.** d_A(x_j)≥3 at KEEP j. **Type P.** Immediately preceding full-word
occurrence is DELETE y≠x_j with a(D_y)≥1 and a(K_j)≥1. Same-key shadows excluded.

**Claim.** Q_B(W)≤2A(W). Hypotheses contain no aggregate cost condition; the
predicate is unchanged since authorization. Full proof in files 3–8 of this
directory; independent 18-point audit in file 12.
