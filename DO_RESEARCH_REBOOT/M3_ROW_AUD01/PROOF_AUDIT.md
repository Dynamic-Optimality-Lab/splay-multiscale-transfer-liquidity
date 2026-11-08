# Exact original LOW realization of the weight+1 obstruction

Status: FINITE-EXACT original witness, independently verified. This proves
existential realizability of the SPECIFIED row. It is REFUTED-EXACT for
the sign-run formula on the original LOW relation, not for M3.

The shared signature is sigma=(4,1,0,...,0), legal mask341={0,2,4,6,8}.
The full original states have core/profile IDs
(1647,2073)->(2403,2072). Their normalized A shadows are root1,L0,R4,
RL2,RR6 followed by root4,L1,R6,LL0,LR2 (other positions opaque/empty).
One terminal KEEP of Score4 is at A depth1 and B depth2. Thus original
H=1,q=floor(2/2)=1,w=2H-q=+1. Both states satisfy chi8; all147 original
coordinates at each endpoint, including unused alpha fields and B lo/hi,
are saved in witness.json along with ALL9544 original input variables.

The complete unchanged original LOW predicate accepts this assignment.
This includes its structural, inventory, weak-LE, beta/shadow, repair,
root-termination, event/path and exact B-controller obligations. A concrete
SAT witness supplies private variables; the chosen completion is not made
into an admissibility rule. No universal uniqueness/completion assumption
or restriction of G/other private cases is introduced.

Independent verification rebuilds the original predicate under ROWV,
checks an exact bijection from saved MXL names, validates every variable's
type/width, evaluates the root TRUE and extracts/computes ALL147 source
and destination coordinates anew. No witness factory is invoked. It
additionally reconstructs this witness's visible prefix and replays the
A splay and the B splay with the separate parent-map implementation.
The A/B depths, target, H,q,w and normalized profiles match exactly.
The full original environment is the authoritative check; opaque/empty
erasure is only an auxiliary view for this concrete independent replay.

Reused independent formula-value audits give D_run(s)=2,D_run(t)=0,
so J_run(s)=-2,J_run(t)=0. Therefore

   w-J_run(t)+J_run(s)=1-0-2=-1.

Since chi8 is unchanged, the full correction W=-D_run-5chi8 has the
same residual. This is an ACTUAL original inequality violation. The
existing valid table instead gives J_old(s)=-2,J_old(t)=-1 and residual0.
Any candidate that assigns J(s)=-2 here must assign J(t)<=-1 to respect
this actual edge. This alone does not force every future candidate to
choose J(s)=-2; no unvalidated predecessor trace is assumed original.

The edge has positive weight and its FULL endpoints do not close. It
is not a negative cycle and does not refute M3. The 3761 existing signature
certificates, including this sector's valid table, remain intact. No
formula or signature enumeration was tried in this audit.
