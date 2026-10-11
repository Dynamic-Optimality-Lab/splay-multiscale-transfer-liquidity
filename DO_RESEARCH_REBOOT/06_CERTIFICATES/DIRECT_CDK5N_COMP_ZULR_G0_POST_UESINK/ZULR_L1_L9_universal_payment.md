# ZULR L1–L9 universal payment proof (Gate R2 — reconstructed)

Domain H1–H6 frozen (five genuine keys, core nine, ZERO exceptions, UNIQUE
self-payer H≥2, strict K/P elsewhere). Claim Q≤2A. All values below
recomputed from source (IN 593b3f3a: n=32, A=56, Q=36, Ck=16, E=[],
p=0 H=18, others iv4/iv8/iv12 strict; Sw=4, SR=80).

## L1 — Interval identities

Cyclic KEEP intervals partition accesses exactly once (seam by closure):
sum-H=A, sum-q=Q_B, sum-c=C_K, sum-w=Q_B−2C_K, sum-R=2(A−C_K).

## L2 — Baseline

H>=c: c=0 trivial; c=1 by A-root-change (a=0 iff current A-root; root
splays are no-ops; H=0 would freeze the root at the previous key,
contradicting a different-key KEEP). R>=0. No-ops/DELETEs unrestricted.

## L3 — Nine-core bound (arbitrary ambient trees)

Marked core = ancestor-closed union of root-to-marked-key paths; |core|=9
at every state (H1). Genuine KEEP keys are marked, so root paths lie inside
the core: <=8 edges, d_B<=8, q<=4. c=0 implies B still rooted (DELETEs
freeze; single KEEP per interval), so q=0 and w=0. Hence w>0 implies c=1,
q in {3,4}, w in {1,2}. (Ambient size unrestricted; paths stay in core.)

## L4 — Zero-exception classification (NOT solvency)

E empty excludes (c=1,q=3,H=1) slots only. It does NOT exclude (c=1,q=4,
H=1) with w=2 — such a slot would need H>=2 reserve via H3/H5, not via H2.
E=∅ alone never implies per-interval solvency (the invalid inference
"E=∅ ⇒ all w<=R" is explicitly rejected; audit §L9).

## L5 — Unique untyped payer (sharp case included)

U={w>0,¬K,¬P} has exactly one element p (H3). H4 gives H_p>=2 for that same
p. Positive debt gives c=1 (L3), q in {3,4}. So R_p=2(H_p−1)>=2 and
w_p=q_p−2<=2, hence w_p<=R_p intrinsically — no borrowed credit.
Sharp case q=4,H=2: w=2,R=2, equality 2=2 (included, not omitted).
q=3,H=2: 1<=2. IN: p=0, H=18, q=3, w=1, R=34 (1<=34).

## L6 — Others (predicates first)

j≠p: w<=0 gives w<=R (R>=0); w>0 gives strict-K (d_A>=3 gives a>=2, so
H>=2) or strict-P (a>=1 both, so H>=2) by H5; with c=1, R=2(H−1)>=2>=w.
H>=2 is a CONSEQUENCE of the frozen predicates, never their definition.

## L7 — No double spending

Every interval pays only its own debt: p uses R_p; others use R_j;
nonpositives need nothing. No sink exists; no credit transfers; no reserve
reused; no A-cost in two H intervals; K/P overlap never duplicates credit;
seam covers wrap exactly once.

## L8 — Telescoping

Sum-w <= Sum-R gives Q−2C_K <= 2(A−C_K), so Q<=2A (IN: 4<=80).

## L9 — Classification independence audit

Five keys/core-nine used only via the debt bound; E=∅ only classifies
(no solvency inferred — L4); uniqueness is load-bearing (two untyped
payers would each need own-reserve proof — NOT claimed here); H_p>=2 is
exactly the reserve threshold (H=1 untyped payers excluded). No
generalization to H3-free/multi-payer/larger-core variants (separate
authorizations required). QED.
