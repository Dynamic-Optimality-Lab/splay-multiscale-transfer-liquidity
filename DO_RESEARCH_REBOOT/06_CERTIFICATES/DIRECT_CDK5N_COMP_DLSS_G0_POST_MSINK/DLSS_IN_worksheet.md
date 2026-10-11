# DLSS IN worksheet (frozen: b8b02be7…, n=34, A=55, Q=36, Ck=16)

Word: `D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9`
SHA `b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3`.
Pointer+tuple lockstep replay: closed exact, engines agree, genuine keys
{1,3,5,7,9}, core 9 ×35.
Strict DLSS: E=[4,12] (x=5,(1,3,1) twice); relays t=(2,2) both long ✓ H3;
unique joint sink p=0 (x=3,H=18,c=1,q=3; w=1,R=34; joint 1+1+1=3≤34);
other-positive iv8 (x=3,H=4,q=3,w=1,R=6): strict-K (dA=3) and strict-P both
hold. Stage: member. Σw=4, ΣR=2(55−16)=78; 4≤78 ⇒ 36≤110.
Direct bank-21: all negative (incl. MSINK: t mixed-fail; MR: H6 iv0 dA=0/a=0;
NP/S1/S2/VR/AJ–AS: exact predicates).
Recursive C21*: primitive (33 distinct pre-closure states — independently
reverified) ⇒ no partition at any rotation ⇒ uncovered (1 subproblem,
0 budget hits). IN ∈ S_DLSS ∩ R_5,9^*.
