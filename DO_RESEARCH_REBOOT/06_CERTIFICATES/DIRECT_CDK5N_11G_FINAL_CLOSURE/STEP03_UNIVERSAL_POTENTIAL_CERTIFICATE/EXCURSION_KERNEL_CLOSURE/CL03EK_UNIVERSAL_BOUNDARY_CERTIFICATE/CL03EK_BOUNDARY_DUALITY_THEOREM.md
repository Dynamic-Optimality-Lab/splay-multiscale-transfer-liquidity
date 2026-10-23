# CL-03EK Boundary Duality Theorem (EK-4 SUFFICIENCY proved; EK-5 completeness cited)

EK-4: Assume NonNegCycles(G_D) and a function F:L->R with F(v)-F(u)<=w
for every 00 edge and F(v)-F(u)<=K(u,v) for every kernel edge (equivalently
F(t)-F(s)<=w(P) for every complete excursion). Then every Q_min closed walk
telescopes to total >= 0; by EK-3, every frozen closed walk is >= 0.
Proof is telescoping + EK-3. EK-5 (completeness): by the frozen G01
finite-graph duality (super-source Bellman-Ford distances), NonNegCycles
of any finite weighted digraph is equivalent to potential existence;
applied to Q_min (finite: shallow vertex subset of a finite state space)
this yields F whenever Q_min is nonnegativity-certified — a mathematical
existence statement, NOT a construction and NOT a decision procedure.
STATUS: EK-4 proved (conditional); EK-5 cited from Step 01 (verified
reference, not re-proved). Neither certifies the missing sign inputs
(H3, F itself).
