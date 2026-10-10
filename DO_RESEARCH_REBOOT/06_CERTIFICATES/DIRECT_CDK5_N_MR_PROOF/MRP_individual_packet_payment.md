# MRP per-packet payment (PROVED — L6 per packet, all cases)

Per exception e with relay t_e≥2 and payer (c=1,H≥2,q≤3): exception (1,0) +
bridges (each w≤0,R=0; q∈{0,1,2} incl. negative-debt bridges) + payer (w≤1 at
q≤3 worst, R≥2) gives 1+0+1≤0+0+2 at worst values. Joint charge, once per
packet. Payer needs no K/P (paid jointly); bridges need none. No K/P inside
packet slots by construction (bridge predicate H=1,q≤2 excludes K/P-eligible
H≥2... a bridge could still satisfy K/P predicates coincidentally — e.g. H=1
cannot (needs H≥2); so no overlap issue arises inside packets at all). ∎
