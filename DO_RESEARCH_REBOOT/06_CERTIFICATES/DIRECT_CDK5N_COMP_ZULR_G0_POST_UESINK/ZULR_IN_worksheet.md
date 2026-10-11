# ZULR IN worksheet (frozen: 593b3f3a…, n=32, A=56, Q=36, Ck=16)

Word: `D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9`
SHA `593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9`.
Pointer+tuple lockstep replay: closed exact, engines agree, genuine keys
{1,3,5,7,9}, core 9 ×33, primitive (32/32 distinct pre-closure states).
Strict ZULR: E=[] (zero (c=1,q=3,H=1) slots — verified by scan); unique
untyped payer p=0 (x=3,H=18,c=1,q=3; w=1,R=34; dA=0 so not-K; prev access
D3 same key so not-P); H_p=18≥2 ✓ intrinsic solvency (1≤34); other
positives iv4 (x=5,H=2,q=3,w=1,R=2; dA=4 strict-K), iv8 (x=3,H=6,q=3,w=1,
R=10; dA=3 strict-K + strict-P via prev-D4 distinct, a≥1 both), iv12
(x=5,H=2,q=3,w=1,R=2; dA=4 strict-K). Stage: member.
Σw=4, ΣR=2(56−16)=80; 4≤80 ⇒ 36≤112.
Direct bank-23: all negative (UESINK: |E|=0≠1; DLSS/MSINK: |E|=0≠2;
NP: iv0 (w=1) lacks strict-K/P so not all-positives-covered; S1/S2/VR/MR:
exception-count/shape fails; AJ–AS exact negatives; AO/AP/AQ/AR/AS REJECT).
Recursive C23*: primitive (32 distinct) ⇒ no partition at any rotation ⇒
uncovered (1 subproblem, 0 budget hits). IN ∈ S_ZULR ∩ R_5,9^*.
