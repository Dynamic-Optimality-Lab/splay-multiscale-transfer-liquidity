# Recursive closure definition (tasks F1–F6)

W: universe of admissible reachable exactly closed state-labeled pair-walks
(accesses + actual initial state + transitions + closing state; strings alone
insufficient). Non-diagonal starts allowed (reachability via parent prefix).
B: union of banked domains above (MSINK excluded). Rot(B): cycles whose
state-trajectory rotation is banked-covered (rotation verified on states,
never restart-at-T0).
Z: exactly closed cycles with A=0, Q=0. Lemma (proved in soundness doc):
a closed A0 walk accesses a single key (A-root fixed, splay no-ops) and
closure forces every KEEP a B-root no-op, hence Q=0; 0≤0 holds.
C0 = Rot(B) ∪ Z, each member certified Q≤2A.
CycAdd(C_k): closed W with (1) valid rotation along actual trajectory,
(2) partition into ≥2 nonempty consecutive pieces, (3) each piece exactly
closed, (4) each piece in C_k (own start state, own domain), (5) pieces
exhaust accesses exactly once, (6) A/Q add exactly.
C_{k+1} = C_k ∪ CycAdd(C_k); C_* = ∪_k. Least fixed point; no MSINK in basis;
no new mechanisms. R_5^* = W_5^9 ∖ C_* (relative residual only).
