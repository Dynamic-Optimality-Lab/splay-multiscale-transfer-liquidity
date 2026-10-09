# Absorbed H0 self control — recovered source-defined lemma

STATUS: PROVED — UNIVERSAL for the source-defined static fold and ordinary present splay's root delivery/key preservation. This is a reconstructed earlier lemma, not another new research pivot. It does not give a joint ROW witness.

Let G_y(B)=|B|−subsize_B(y) and H0_y(B)=−R_static(B,y)+4G_y(B), with no J charge. Then

\[
H0_y(B)-H0_y(S_yB)\ge R_static(B,y)-2(1-b_y).
\]

Proof. In each terminal fold state a_L,a_R≤0 and c=0. Every displayed Tmap decreases both a coefficients. Its increment to c is at most1 for LL/RR and at most0 for LR/RL. By induction on q double maps, c≤q. Every prepended fringe coefficient is at most2 since both current a values are nonpositive; the terminal odd-depth coefficient is1. If F is the total number of off-path fringe keys and d is the edge-depth of y, the fold definition gives R_static≤q+2F (descendant L/R terms are nonpositive). The outside-subtree keys partition into d ancestors and F fringe keys, so G=d+F. Since q=floor(d/2)≤2d, R_static≤2G. Splaying y makes it root while preserving keys, so G_y(S_yB)=0 and R_static(S_yB,y)=0 by the root fold definition. Thus H0 drop=−R_static+4G≥R_static, which is at least R_static−2(1−b_y). At d=0 both sides are zero. This covers every depth and both orientations.

It proves self control for J=0, not that J=0 satisfies ROW. Adding arbitrary charges may break SELF; a global assignment compatible with both SELF and DIAM remains open. The statement does not require the additional identity R_static=q−total-depth-drop, since it concerns the source-defined observable directly.

Sources: scripts/wp6_staticR.py:Tmap/R_static; scripts/wp6_j4shared.py:H0/SELF; audits/PIVOT_CONSTRAINT_GUIDED_DUAL.md:1310-1326 reports the absorbed-row proof. The report's kappa_* notation should not be read as a proof that4 is the sharp minimum; its own text leaves the sharp threshold open. No sharpness claim is made here.
