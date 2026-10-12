# SELR IN replay and strict classification (expected values; recompute)

IN 8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd:
D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,
D8,D4,D2,D5,D6,D1,D9 (n=31, A=53, Q=36, C_K=16; verified by replay).
Five genuine KEEP keys {1,3,5,7,9}; core-nine at all 32 boundaries; exact
closure; 31/31 distinct pre-closure pair states (primitive).
E={4} (H=1,c=1,q=3,w=1,R=0). Successor j=5: c=1,H=2,q=2 → maximal
creditless relay t_e=0. Donor p=0: H=18,c=1,q=3,w=1,R=34; ¬K (dA=0);
¬P (preceding DELETE same key). U={0,4}. Joint: w_4+w_0=2≤34.
Others: j=8 (H=4,q=3,w=1,R=6; K+P overlap, single cover); j=12
(H=2,q=3,w=1,R=2; K). Σw=4, ΣR=74 (4≤74 ⇒ 36≤104). Finite replay values
corroborate; universal proof is L1–L9, not these numbers.
