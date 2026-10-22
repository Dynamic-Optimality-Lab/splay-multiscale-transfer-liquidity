# CORE-01B H-Cost Constraints (Gate G1/G2)

H = sum over active events of a(ev_d), a = ceil(d/2), d<=4 per event;
H<=2 for low edges (frozen). H bounds A-side work ONLY: a B-changing
intermediate KEEP can have dd_A=0 (a=0) while dd_B>0 (B splays). Hence H
does NOT bound the number, depth, or B-effect of unmarked-target
intermediate events. Proven: no H-derived bound on B-changing intermediates
(the zero-A-cost channel). DELETE contributes a=0 and B-identity. A8's
genuineness test is B-change-sensitive, not H-sensitive. Consequence: the
low-cost classification provides no compensation mechanism by itself
(G3: cost != structure; a weighted growth bound is not monotonicity).
