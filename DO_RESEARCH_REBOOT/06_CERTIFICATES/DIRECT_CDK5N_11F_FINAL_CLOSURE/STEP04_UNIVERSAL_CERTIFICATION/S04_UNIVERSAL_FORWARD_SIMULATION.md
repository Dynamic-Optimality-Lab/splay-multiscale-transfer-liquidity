# S04_UNIVERSAL_FORWARD_SIMULATION.md — Gate G U1-U16 (F04-27)

For arbitrary W in W_5^9 with M=G(W)=K(W) (Gate B) and stable S=C_M, |S|=9:
segment W into macro intervals (legs cover all accesses, U11). Map each boundary
(state at macro start) to its abstract S-vector (U1 valid; U2 mask = ordered
5-of-9 of G(W); U3 same S throughout by constancy; U4 B-core agrees by replay;
U5 fringe saturated counts; U6 shadows match by construction; U9 mu/sig static
across boundaries by relation equalities). Each interval maps by Gate D: H≤2 to
exact low edge (U7, w=2H-q), H≥3 through WQ midpoint (U8, w=6-q). U5 saturation
is per-macro (no global 2669-key claim). U13 diagonal = paired closure (GLOB).
U14 primitive/nonprimitive both in splay cases. U15 per-macro: low w=2H-q
(equality, hence ≤); high w=6-q ≤ 2H-q ⟺ H≥3 (class hypothesis). U16 sums to
w(P) ≤ 2A(W)-Q_B(W) (next document). Composition and closure by the boundary
theorem. This discharges every dependency; no OPEN lemma remains.
