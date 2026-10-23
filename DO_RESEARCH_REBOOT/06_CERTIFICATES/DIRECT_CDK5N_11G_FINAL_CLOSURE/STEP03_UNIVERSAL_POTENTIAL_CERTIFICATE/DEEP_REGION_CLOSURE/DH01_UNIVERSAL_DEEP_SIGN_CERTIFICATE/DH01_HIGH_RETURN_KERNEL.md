# DH-01 High-Return Kernel (EXACT, conditional on L3; sign OPEN)

Define J_D nodes = high edges; arc e->f with weight w_e + d_L(v_e, u_f)
whenever a low-only deep connector exists (d_L from minimum attainment,
conditional on L3). THEOREM (conditional): NonNegCycles(G_D) iff
[NonNegCycles(G_D^L) and NonNegCycles(J_D)]. Forward: a negative deep
cycle with high edges contracts (replace each low segment by a minimum
one; weights nonincreasing) to a negative J_D closed walk; without high
edges it is already low. Reverse: expand J_D arcs via attaining paths
(endpoints match, stay deep, weight preserved). PROOF complete given L3
+ attainment. SIGN STATUS: J_D's nonnegativity is UNPROVED (no vertex
potential constructed; circularity explicitly avoided; q'-credit and
interface-transport obstructions from RC-01 apply unchanged). The kernel
exactly localizes the missing sign work; it does not perform it.
