# MRP deterministic relay scans (PROVED)

Per exception e: scan j=e+1,e+2,... consuming consecutive (c=1,H=1,q≤2); stop
at first failure; t_e = count; payer = next interval. Terminates (finite s;
bounded checks). Deterministic (exact source predicates; no choices). Correct:
H3 defines t_e as THE maximal run, H4 pins the payer as first nonbridge — the
scan reproduces exactly this decomposition. Unique per exception. Distinctness
of the full packet verified via H5 index sets; scan order never reassigns.
t_e≥2 excludes S1/S2 relay shapes (S1: successor H≥2; S2: second H≥2) —
disjointness by frozen inequalities. Witness: t=2 both packets. ∎
