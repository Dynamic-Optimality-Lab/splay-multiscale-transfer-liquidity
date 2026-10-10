# MRP pairwise disjointness (PROVED — H5 index arithmetic)

Packets P_e={e..e+t_e,p_e} mod s with t_e+2≤s each. H5 requires pairwise
disjoint index sets (verified on witness: {4,5,6,7}∩{12,13,14,15}=∅, wrap-safe
by mod-s comparison). Consequences enforced: no shared payer (a payer index in
two packets ⇒ intersection ⇒ rejected); no shared bridge; no exception inside
another packet (an exception index in P_f ⇒ intersection since exceptions are
packet starts... precisely: e'∈P_e with e'≠e means e' consumed as bridge/payer,
but e' is exceptional (H=1,q=3): bridge needs q≤2 — fails; payer needs H≥2 —
fails. So an exception can never lie inside another packet's bridge/payer slots;
it can only start its own packet. Hence H5-disjointness is checkable and holds
on witness). No second-exception-inside-packet by construction. ∎
