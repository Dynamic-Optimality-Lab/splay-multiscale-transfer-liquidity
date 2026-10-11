# UESINK IN worksheet (frozen: a7c6504c…, n=33, A=56, Q=36, Ck=16)

Word: `D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9`
SHA `a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8`.
Pointer+tuple lockstep replay: closed exact, engines agree, genuine keys
{1,3,5,7,9}, core 9 ×34.
Strict UESINK: E=[12] unique (x=5,(1,3,1)); relay t=2 (bridges iv13,14
H=1/q=2; payer iv15 H=2 stops scan) ✓ long; unique joint sink p=0
(x=3,H=18,c=1,q=3; w=1,R=34; joint 1+1=2≤34); other positives iv4
(x=5,H=2,q=3,w=1,R=2; dA=4 strict-K) and iv8 (x=3,H=6,q=3,w=1,R=10; dA=3
strict-K + strict-P via prev-D4 distinct, a≥1 both). Stage: member.
Σw=4, ΣR=2(56−16)=80; 4≤80 ⇒ 36≤112.
Direct bank-22: all negative (MSINK: |E|=1; DLSS: |E|=1; NP: E-slot;
S1: |E|... S1 needs exactly-1 exception ✓ count ok but successor iv13 H=1
fails H≥2; VR: payer ok but other-positive iv8... verified False via exact
predicates; MR: |E|=1; AJ/AK/AL/AM/AN/AO/AP/AQ/AR/AS: exact negatives).
Recursive C22*: primitive (32 distinct pre-closure states — verified) ⇒
no partition at any rotation ⇒ uncovered (1 subproblem, 0 budget hits).
IN ∈ S_UESINK ∩ R_5,9^*.
