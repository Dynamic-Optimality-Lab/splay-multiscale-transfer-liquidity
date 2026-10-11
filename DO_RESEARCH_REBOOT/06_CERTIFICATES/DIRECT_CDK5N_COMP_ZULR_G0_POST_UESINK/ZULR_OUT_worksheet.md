# ZULR OUT worksheet (frozen: 8cd970c71989…, n=31, A=53, Q=36, Ck=16)

Word: `D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9`
SHA `8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd`.
Provenance: in-seed L1 idx4, op rm7 (remove DELETE at zero-based position 7,
the D8 before K9); first fully certified qualifying OUT in global order
(in-L1 idx0–1 non-closed, idx2 NP-banked, idx3 ZULR-member — all recorded
by re-executed screening).
Pointer+tuple replay: closed exact, engines agree, genuine {1,3,5,7,9},
core9 ×32.
Strict ZULR: E=[4] only (iv4: H=1,q=3; every other (1,3,·) slot has H≥2 —
iv12 carries H=2) → H2 fails (|E|=1≠0). First-failed hypothesis: H2.
Positive debts (moot for membership, listed for the record): iv0
(x=3,H=18,q=3,w=1,R=34,dA=0), iv4 (x=5,H=1,q=3,w=1,R=0), iv8
(x=3,H=4,q=3,w=1,R=6,dA=3), iv12 (x=5,H=2,q=3,w=1,R=2,dA=4).
Direct bank-23: all negative (machine battery: NP/S1/S2/VR/MR need exception
shapes or all-K/P; AJ–AS exact negatives; AO/AP/AQ/AR/AS REJECT; MSINK/DLSS/
UESINK count/shape fails).
Recursive C23*: primitive (31/31 distinct pre-closure states) ⇒ no proper
closed segment at any rotation ⇒ uncovered (1 subproblem, 0 budget hits).
OUT ∈ R_5,9^* ∖ S_ZULR. Q−2A = 36−106 = −70 (no violation; this word is the
correct owner of the −70 value misattributed in the CRA doc — see erratum).
