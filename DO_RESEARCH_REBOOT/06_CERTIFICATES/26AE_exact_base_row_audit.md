# 26AE exact base-row audit (certificate companion)

## Premises (all independently established)

- **UG twin equations** (8 proven pairs: F1 δ∈{−1,0,1,2}@d2; F3 δ∈{−3,−2}@d4; F5 δ∈{−5,−4}@d6): `J[lam2]−J[twin]=1`. Source: `j4_gapdomain.json` overlap census + xclean substitution. Scope: finite listed triples.
- **Root normalization** `J[(r,c)]=c` (slope a=1 measured over 18842 occurrences, `j4_ugar_a.json`): banked architecture identity.
- E has 33 rows; verified full row rank (exact sympy) ⇒ consistent (solution exists).
- Excluded: target pair rows (circular), SELF/DIAM inequalities (unproved-global), LP witnesses (numerical), DTQ (optional subclass), new constraints.

## Domain

Canonical `B_0=[n+1,T,None]`, `|T|∈{3,4,5,6}` (Catalan shapes 5+14+42+132=193 trees), all distinct same-side pairs with equal B_0-depth and S-probe fold equality (fold stability across S by T-path fixity). **124 candidates** (reconstructed count; the prior "64" belonged to a different census and was not copied).

## Control

26AD pair (T=[4,[2,[1],[3]]],(1,3)): verdict **FREE** (rejected as required). Its residual direction is banked in 26AD artifacts.

## Audit outcome (exact rational RREF per candidate)

- **CONST: 10** (all with forced constant C=0 ∈ [−2,2]).
- **FREE: 114** (representative nullspace witness recorded in `26AE_audit.json`).
- Selection (§8: smallest |T| → n=4; single n=4 CONST → no tie-break needed): **P_* = (T_*=[1,None,[3,[2],[4]]], u=2, v=4, d=3), C=0**.
- Selected certificate: β=0 (mirror-symmetric rows Jat(B_0,2)=Jat(B_0,4) as multisets), c0=0, α=0. Verified by independent recomputation + residual check.

## Machine records

- `06_CERTIFICATES/26AE/ae_audit.py` (procedure), `06_CERTIFICATES/26AE/26AE_audit.json` (124 verdicts).
- Erasure spot-checks (∅/singleton/vine/branched S): D-form stays identically zero.
