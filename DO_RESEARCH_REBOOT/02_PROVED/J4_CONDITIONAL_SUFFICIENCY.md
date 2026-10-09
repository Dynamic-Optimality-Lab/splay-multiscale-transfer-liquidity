# J4 → COARSE-DOUBLE: reconstructed sufficient implication

STATUS: CONDITIONAL. The shared global witness and its row inequalities are OPEN. This document proves the implication, not witness existence.

Use the source-defined H_y and b_y=[root(B)=y]. Suppose ONE shared assignment j,rho satisfies, for every finite BST B and every present x:

\[
H_x(B)-H_x(S_xB)\ge R_{static}(B,x)-2(1-b_x)\quad\text{(J-SELF)},
\]

and, for every distinct r,x in B,

\[
H_r(B)-H_x(B)\ge-2+2(b_r-b_x)\quad\text{(ROW-DIAMETER)}.
\]

Equivalently the adjusted rows H_y−2b_y have diameter at most 2. This is stronger than raw |H_r−H_x|≤2 when one node is the root; for a root/nonroot pair the exact raw range is 0≤H_root−H_child≤4. Same-child and cross-child nonroot pairs have raw width 2.

Let D_B(B)=sum_y d_B(y), t(A,B)=[root(A)=root(B)], r=root(A), and

\[
\Phi(A,B)=D_B(B)-2t(A,B)+H_r(B).
\]

An additional mechanics premise is R_static(B,x)=q_B(x)−(D_B(B)−D_B(S_xB)). The source describes the static fold as the backward expansion of the depth-change formulas for LL/RR/LR/RL and final zig and finite-validates it. A complete universal derivation linking this evaluator to actual splay depth change was not independently re-proved in this run; the implication below explicitly assumes that identity. Formal certification of those mechanics is another separate verification attribute.

For KEEP x, let a=ceil(d_A(x)/2), q=floor(d_B(x)/2), B'=S_xB, and A'=S_xA. After KEEP both roots are x. The residual after removing the baseline D_B−2t drop is R_static(B,x)−2a−2(1-b_r). If x=r then a=0 and J-SELF pays this residual. Otherwise a≥1 and ROW-DIAMETER gives

\[
H_r(B)-H_x(B)\ge-2a+2(b_r-b_x).
\]

Add J-SELF to obtain H_r(B)−H_x(B')≥R_static(B,x)−2a−2(1-b_r). Hence q−2a≤Phi(A,B)−Phi(A',B').

For DELETE x, q=0, B'=B and root(A')=x. The baseline drop is 2(b_x−b_r), so the residual is −2a−2(b_x−b_r). If x=r it is zero and the row does not change; otherwise the same ROW bound pays it. Thus the same edge inequality holds in both modes. Sum along a closed pair walk: Phi telescopes to zero, giving Q_B≤2A.

No positivity or uniform magnitude bound on Phi is necessary for a closed walk. Shared coordinate values and a fixed state function are necessary: separately fitted values for each row/tree do not telescope. This proof neither shows the sufficient row conditions are necessary nor excludes another direct route to COARSE-DOUBLE.

Source: scripts/wp6_j4shared.py:94-117,125-150 contains exactly these SELF/DIAM rows; audits/PIVOT_CONSTRAINT_GUIDED_DUAL.md:1277-1359 gives the residual decomposition; scripts/wp6_staticR.py gives the fold; scripts/wp6_jextract.py contains the older switch formulation. R_static's universal mechanics must be included in any full formal assembly; finite validation alone is insufficient.
