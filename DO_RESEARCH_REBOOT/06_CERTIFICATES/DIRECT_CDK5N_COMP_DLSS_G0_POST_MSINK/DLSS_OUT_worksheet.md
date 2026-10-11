# DLSS OUT worksheet (frozen: a7c6504c…, n=33, A=56, Q=36, Ck=16)

Word: `D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9`
SHA `a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8`.
Provenance: in-seed L1 idx4, op rm7 (remove DELETE at position 7); first
fully certified qualifying OUT in global order (in-L1 idx0–1 non-closed,
idx2 DLSS-member, idx3 AMG-banked — all recorded).
Pointer+tuple replay: closed, engines agree, genuine {1,3,5,7,9}, core9 ×34.
Strict DLSS: E=[12] only → H2 fails (|E|=1≠2). First-failed hypothesis: H2.
Direct bank-21: all negative — NP (E-slot + iv0 dA=0/a=0 fail), S1 (successor
iv13 H=1<2), VR (payer iv15 ok but other-positive iv0 fails K/strict-P),
MR (|E|=1), AJ/AK/AL/AM/AN (successors/plus-keys ≠ rb 9; zero AN packets),
AO/AP/AQ/AR/AS executable REJECT.
Recursive: primitive (33/33 distinct) ⇒ no partition ⇒ uncovered.
OUT ∈ R_5,9^* ∖ S_DLSS. Q−2A = 36−2·56 = −76 (no violation).
