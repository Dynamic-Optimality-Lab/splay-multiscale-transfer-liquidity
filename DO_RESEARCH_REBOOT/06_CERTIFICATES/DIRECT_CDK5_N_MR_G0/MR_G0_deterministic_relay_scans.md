# Deterministic relay scans (PROVED)

Per exception e: scan j=e+1,e+2,... consuming consecutive (c=1,H=1,q≤2);
stop at first failure; t_e = count; payer = next. Terminates (finite s;
bounded checks). Deterministic (exact predicates; no choices). Correct: H3
defines t_e as THE maximal run, H4 pins the payer — scan reproduces it.
Unique per exception. Distinctness of the full packet verified via H5 index
sets; scan order never reassigns. t_e≥2 excludes S1/S2 relay shapes; maximality
(not convenience) enforced by stop-at-first-failure. Witness: t=2 both. ∎
