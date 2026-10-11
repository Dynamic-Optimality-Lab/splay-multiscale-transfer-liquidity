# UESINK L1–L7 universal payment proof (Gate C — reconstructed)

Domain H1–H6 frozen (five genuine keys, core nine, UNIQUE exception e with
long relay t_e>=2, joint existential sink p, strict K/P). Claim Q<=2A.
All values below recomputed from source (IN a7c6504c: n=33, A=56, Q=36,
Ck=16, E=[12], t=2, sinks=[0]; joint 1+1=2<=34; others iv4 strict-K dA=4,
iv8 strict-K dA=3 + strict-P; Sw=4, SR=80).

## C1 — Interval identities

Cyclic KEEP intervals partition accesses exactly once (seam by closure):
sum-H=A, sum-q=Q_B, sum-c=C_K, sum-w=Q_B-2C_K, sum-R=2(A-C_K).

## C2 — Baseline

H>=c: c=0 trivial; c=1 by A-root-change (a=0 iff current A-root; root
splays are no-ops; H=0 would freeze the root at the previous key,
contradicting a different-key KEEP). R>=0. No-ops/DELETEs unrestricted.

## C3 — Nine-core bound (arbitrary ambient trees)

Marked core = ancestor-closed union of root-to-marked-key paths; |core|=9
at every state (H1). Genuine KEEP keys are marked, so root paths lie inside
the core: <=8 edges, d_B<=8, q<=4. c=0 implies B still rooted (DELETEs
freeze; single KEEP per interval), so q=0 and w=0. Hence w>0 implies c=1,
q in {3,4}, w in {1,2}.

## C4 — Unique exception

|E|=1, (c,q,H)=(1,3,1): w=1, R=0. Strict K (d_A>=3 gives a>=2) and strict P
(two a>=1 accesses) each imply H>=2, not 1 — the exception satisfies
neither. E complete by definition.

## C5 — Joint sink (full q_p table)

There exists p not in E with c=1, H>=3 (all candidates enumerated):
R_p>=4 and w_p=q_p-2<=2. Table: q=0->w=-2 (need -1<=R, holds); 1->-1 (0<=R);
2->0 (1<=R); 3->1 (2<=R); 4->2 (3<=R, tight at H=3: 3<=4 included). So
w_e+w_p = 1+w_p <= 3 <= R_p. IN: p=0, H=18, q=3, w=1, R=34 (2<=34). QED.

## C6 — Others

j not in {e,p}: w<=0 gives w<=R; w>0 gives strict-K (d_A>=3 gives a>=2,
so H>=2) or strict-P (a>=1 both, so H>=2) by H5; with c=1, R=2(H-1)>=2>=w.

## C7 — Disjointness

{e,p} distinct; pair + singletons partition intervals; sink spent once;
exception never recharged; accesses counted once.

## C8 — Telescoping

Sum-w <= Sum-R gives Q-2C_K <= 2(A-C_K), so Q<=2A (IN: 4<=80).

## C9 — Relay-independence audit

Payment steps C1-C8 never query the relay length; bridges are ordinary
w<=R singletons. The t>=2 gate is domain membership only. No short-relay
assumption; no H3 change. An H3-free single-exception variant is NOT
claimed here. QED.
