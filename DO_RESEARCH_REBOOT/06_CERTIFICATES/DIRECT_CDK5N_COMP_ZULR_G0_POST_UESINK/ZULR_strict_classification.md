# Strict classification record: E-set, unique payer, strict K/P, reserves

IN (593b3f3a, 56/36/16): E=[] (zero (c=1,q=3,H=1) slots by exact scan —
H2 satisfied). Positive debts {0,4,8,12}, all w=1. Untyped set U={0}
(x=3,H=18,q=3,dA=0: not-K since dA<3; not-P since prev access is DELETE(3),
same key). Unique: U has exactly one element. H_0=18≥2 (intrinsic reserve
R_0=34 ≥ w_0=1, self-financed, no borrowing). Others: iv4 strict-K (dA=4);
iv8 strict-K (dA=3) + strict-P (prev DELETE(4) distinct, a≥1 both); iv12
strict-K (dA=4). H≥2 is a consequence of the predicates (a≥2 / a≥1+both),
never their definition.

OUT (8cd970c7, 53/36/16): E=[4] only (iv4 H=1,q=3; iv12 H=2) → H2 fails.
Positives {0,4,8,12} with (H,q,w,R,dA): (18,3,1,34,0), (1,3,1,0,2),
(4,3,1,6,3), (2,3,1,2,4). Nonmembership decided at H2; listed for record.
