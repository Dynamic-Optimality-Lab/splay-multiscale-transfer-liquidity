# CORE-01B Low-Macro Event Grammar (Gate A)

A low witness = nev active events (nev<=5 slots; ssertify pins nev=len(word)).
Per active event e, in order: (i) verify path/dirs against CURRENT B-state;
(ii) optional B-splay (skipped iff DELETE or inactive); A-side splay in
lockstep. Event types: TERMINAL (e==last): KEEP, marked target, B-changing
(enforced). INTERMEDIATE active: DELETE (B-identity), B-unchanged KEEP
(any target; B-identity), or nongenuine KEEP (any B effect; A8 forces
unmarked target). Inactive (e>=nev): identity. ROTATION FACT (code-derived):
every single_rot rewires (x=child, p=parent, S=x's rotation-side child,
middle, gp); only x gains descendants (p-subtree), all others lose-or-keep.
H = sum of per-event a=ceil(d/2); DELETE contributes a=0; zero-A-cost events
allowed (dd=0).
