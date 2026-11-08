# The sign-run candidate

Fix a signature and use the established source-complete LOW proof
superrelation on existing observables. Define C(v) as the maximum debt
transported from a psi seed along NONNEGATIVE rows, including empty paths.
It always exists in[0,2]. Paths with positive resulting debt use at most
one+1 row and arbitrarily many zero rows; costs>=2 are dominated by a
fresh nonnegative seed at the negative-run entry. C is an unconditional
monotone two-level reachability closure, not signed-potential feasibility.

Define D(v) as the capped maximum of C(u)-weight along one negative-only
run u->v. The pinned negative B graph is acyclic, max deficit2, max length2.
This is a fixed sign language, not arbitrary alternation of cheap and
negative phases. No new state/history coordinate is added.

Exact simplification using the already proved negative-row law
psi(Bv)>=psi(Bu)-w:

 * psi(v)=0: there is no negative incoming row, so D(v)=C(v).
 * psi(v)=2: D(v)=2 already.
 * psi(v)=1: every negative incoming row has w=-1,psi(u)=0.
   Such a source has no negative predecessor, so D(u)=C(u).
   Thus D(v)=max(C(v),2*I[exists u->v,w=-1,psi(u)=0,C(u)>0]).

The displayed promotion is the entire nontrivial negative phase. It proves
0<=D<=2 and D>=psi universally; it does NOT prove the un-clipped original
edge inequalities. In particular a new negative row out of promoted debt
or a cheap row AFTER promotion can still falsify the candidate J=-D.

On a corpus with an existing valid debt D_old=-J_old, induction on the
nonnegative derivation shows C<=D_old, and then on the negative run gives
D<=D_old. This is a regression/upper bound only on that ALREADY proved
corpus; it is not used as an assumption for unproved populations. For the
old audited+1,-1 trace, membership gives destination debt>=2 and the old
certificate gives<=2. The old failure is therefore fixed exactly.

Independent C audit checks finite seed-path derivations AND every needed
nonnegative row inequality. These two directions prove equality to the
path formula; mere agreement with old labels is insufficient. Independent
negative audit checks every promotion trigger and an attaining incoming
row for every actual promotion. A direct incoming-row computation at any
failed endpoints then verifies the formula without reading final D labels.

Universal LOW closure w+D(t)-D(s)>=0 remains the ONE principal claim.
Only after that proof could the old source lift/HIGH/h0 argument give
W(O)=-D-5chi8,W(M)=-5chi8, closed walks>=0 and finite walks>=-7.
Finite fits, a clipped range, and an unlifted proof-row failure do not
establish or refute the original M3 theorem.
