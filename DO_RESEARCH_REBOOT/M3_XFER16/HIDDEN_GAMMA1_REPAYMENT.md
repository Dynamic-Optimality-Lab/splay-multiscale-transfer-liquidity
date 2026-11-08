# A safe public source ceiling closes all eight hidden Gamma1 profiles

The theorem below constructs a NEW explicit debt F from the saved D_exp.
It does not claim that an old D_exp row with debt2->1 was nonnegative.
It proves the ceiling preserves EVERY previously valid original row and
makes every hidden Gamma1 zero row valid. Original graph/target/caps are
unchanged. Publication requires the separate new audit to pass.

## 1. Public ceiling region and theorem

Use the frozen full ordinary state s=(mu,b,alpha7,sigma). Let B be its
valid ordered nine-core projection, r its root, and h(B) its height in
edges. Require A's root to be Score r. Root's unused kind and all other
unused/raw fields are free. Write An(i) for the EXISTING alpha field
condition kind0,isS=false; it does not constrain the unused index.

H_min consists of the full states satisfying:

    r in{7,8}, B.left(r)=0, h(B)>=7;
    alpha L has kind0;
    An(LL) OR (An(L) AND An(LR));
    no position i=1..6 with kind0,isS=true has index0.          (1)

H_max is an ACTUAL second predicate: r in{0,1}, B.right(r)=8,
h(B)>=7, alpha R kind0, An(RR) OR (An(R) AND An(RL)), and no
nonroot kind0 Score observation has index8. Let H be their union.
These are formulas over existing coordinates, without a private helper
gap/identity, inventory split, port bill, new observable or extra state.
They apply even at incoming boundaries without a fresh LOW completion.

Set D=D_exp from Transfer13 and define

    F(s)=min(D(s),1) if H(s), and F(s)=D(s) otherwise.          (2)

THEOREM. F has range0..2 and the original psi floor. Every original
LOW row already valid for D remains valid for F; HIGH/h0 retains the
completed range glue. Every original zero Gamma1 edge in any of the
eight hidden profiles has source F<=1, target F>=1, and signed residual
nonnegative. All prior certificates are kept unchanged as dependencies.

The new potential is NOT claimed pointwise >=Lambda. The c/Lambda
normalization was only proved safe for H1, not WLOG for Score-bearing
Gamma1. Preserving its unnecessary source2 assignments is not the M3
target. We instead prove preservation of its actual valid ROWS. Future
uses of an operation requiring F>=Lambda must re-establish that premise;
it is not silently inherited for this new function.

## 2. Tall cores have psi0: a universal height proof

Consider any ordinary core access at depth d=6,7 or8. Delete off-path
cores temporarily, keeping the access-path spine and its formal cuts.
After k>=1 bottom pairs, the processed ancestor skeleton has height at
most k+1. To see the induction, each next pair moves either existing
target-side subtree down by at most ONE edge and inserts only a chain
of at most TWO new ancestors. Thus h_new<=max(h_old+1,2). This holds
for LL,RR,LR,RL; the new checker derives the four arbitrary-block terms.
A final zig adds at most1. The spine bounds are consequently:

    d6: height<=4; d7: height<=5; d8: height<=5.

There are exactly8-d off-path cores. On any final root-to-leaf path,
inserting all of them can add at most8-d edges. Hence the COMPLETE
destination height is at most6,6,5 respectively. Side proxies/junk
are not additional core vertices; the old core-projection theorem
handles their transported pairs. No path directions are sampled.

The fixed old psi is defined by the completed incoming-negative-deficit
recurrence on ALL proper nine-core trees, with virtual value0 at every
vertex. A tree of height>=7 has NO incoming negative-core edge by the
preceding bound. The recurrence therefore gives

    h(B)>=7 implies psi(B)=0.                               (3)

This is a proof about that already constructed psi, without reading any
new table value. In particular H has psi0, so (2) retains F>=psi. A
negative original H1 cannot enter H, since its core is precisely one
of those negative-access outputs. Transfer15's GLOBAL Gamma1 zero
destination floor psi>=1 also excludes every zero Gamma1 incoming to H.

## 3. Exhaustive zero-H1 incoming classification

Take ANY original zero H1 edge u->v with v in H_min. Its B target is
r=7 or8 at TRUE source depth4/5. Its normalized A access has depth1/2,
and the old source Score root is visible at the ACTUAL final A depth
1/2. This last assertion is the three zig/pair identities, without
mark filtering: the old Score remains in an inserted known real pair.
It cannot be removed from the authoritative shadow by G aliases.

For r=8, its source B path is all-right. At depth4 the destination's
left root has an ACTUAL nonempty core left child (mandatory fork), so
cannot be0. At depth5 its left root is the old source core root. Thus
B.left(8)=0 forces old source root0, which would be observed in alpha(v)
and contradict (1). There is NO zero H1 incoming to the r8 part of H_min.

For r=7, height>=7 forces ALL seven cores0..6 into one path below7.left;
the sole upper core8 is the right leaf. A path to7 in the source has
only increasing lower ancestors, with at most one higher ancestor8.
If8 is absent, every direction is R. If it is at ancestor position j,
the only L is the edge leaving8. Arbitrary off-path blocks remain free.
The complete paired-spine classification is:

| Original B depth | Location of8 on path | Forced result |
|---:|---|---|
|4|absent|mandatory lower fork: impossible|
|4|j0 (old root)|only exceptional family, old root8|
|4|j1|destination left root is old root, hence0|
|4|j2,j3|mandatory lower fork: impossible|
|5|absent|mandatory lower fork: impossible|
|5|j0|mandatory lower fork: impossible|
|5|j1,j2|destination left root is old root, hence0|
|5|j3,j4|mandatory lower fork: impossible|

These11 free-constructor schemas are exhaustive by the order path, not
a finite-state test. A mandatory fork contains distinct actual lower
core ancestors on both sides and cannot be repaired by arbitrary side
blocks. The old-root0 cases contradict its required alpha observation.
Thus the ONLY possible incoming zero has old root8, target7, B depth4.

In its exceptional source, let a<b<7 be the two other lower ancestors.
The all-core source and destination terms are

    U=8(0(E,a(B,b(C,7(D,E)))),E),
    V=7(0(E,b(a(B,C),D)),8(E,E)).                         (4)

V's lower subtree must be ONE path on0..6. The actual child a below b
forces D=E, and then b=6 because no key between b and7 can be absent.
The a-subtree is a path on1..5: a is1 or5 and the other four cores lie
in exactly one of B,C as a four-node path. In U, B starts at depth3
and C at depth4. Its height is therefore at least6. The saved negative
core law at such a depth gives psi(U)<=1 (or (3) gives0 if height>=7).

Marked target7 belongs to V(u), its original H1 price is0, and its
destination core has psi(V)=0 by (3). Hence

    c(u)=0, Lambda(u)=psi(U)<=1.                          (5)

It remains to check the ACTUAL D_exp, not assume it equals Lambda.

## 4. Every old cap vanishes at that exceptional source

An actual original source rooted at8 can access7 only at L,LL,LR.
The exact A source/target schemas with arbitrary compatible blocks are

    8(7(A,B),C) -> 7(A,8(B,C));
    8(p(7(A,B),C),D) -> 7(A,p(B,8(C,D)));
    8(p(A,7(B,C)),D) -> 7(p(A,B),8(C,D)).                (6)

Since the target is H_min, its left child is real. In the first case
the source's LL=A is real. In the second case p lies strictly between
Scores7,8 and is anonymous. In the third, either A (source LL) is
anonymous, or p (source L) is anonymous. No0 observation is allowed.
Marked7 is always present;8 may be marked or unmarked.

CAP_EXCLUSION.md audits EVERY term in the existing explicit maximum:

* Q and interval-child I fail their nonreal exterior cuts: when7 is a
  child, LL is real; a different marked child cannot be the sole V target.
* R_plus with marked8 has second-largest mark7 but needs a port below
  that child, or puts the other mark at a different position. Both fail.
  If8 is unmarked, its marked-root guards fail. The opposite R_minus
  cannot have8 as its second-smallest mark in a five-bit mask.
* The unmarked-ancestor grandchild cap fails: parent7 is marked in the
  child case, anonymous in LL, and in LR either its parent is anonymous
  or the required nonreal LL cut is an actual anonymous node.
* The remaining central/auxiliary caps fail by their central marked-pair
  order, their B prefix (U.left=0), their real-anonymous A cut, or their
  exact mask. In particular7 is marked; a largest marked8 cannot have
  second-largest3/4. Transfer13's two masks contain no7.

This is an inspection of a FINITE EXPLICIT FORMULA, not a psi fit or an
assumption that a new region is closed. It gives D_exp(u)=Lambda(u)<=1.
No generic cap theorem is extended beyond its exact old guard.

For an incoming zero to H_max the ACTUAL order path has old root0,
target1 at B depth4, source B.right=8 and height>=6. Its three real A
accesses are R,RR,RL. The same direct actual-field guard audit uses
marked1 (and0 marked/unmarked), the empty upper observation8, and the
opposite central-pair/mask exclusions. The negative-core law is applied
on that actual source, not to a reflected psi label. Thus

    u->v zero H1, v in H  implies D_exp(u)<=1.              (7)

## 5. Safe ceiling preserves all prior signed rows

Let an original row be valid for D_exp. If its target is unchanged by
(2), lowering its source can only improve its residual. Otherwise its
target lies in H, D_exp(target)>1, and F(target)=1.

For H1 incoming: negative weights are impossible by section2. Weight0
uses (7) and F(source)<=D_exp(source)<=1. Weight>=1 uses F(source)<=2
and gives residual>=1+1-2=0. Thus EACH previously valid H1 row survives;
indeed all H1 rows into a changed target are valid without an old sign
premise. The complete old negative H1 theorem consequently remains true.

For Gamma1 incoming: its weights are nonnegative by the completed H2
normal form/terminal depth bound. Weight0 cannot enter H by (3) and
Transfer15's target floor. Weight>=1 is range-safe at target1. Every
previously valid Gamma1 row therefore survives as well.

For Gamma0, reuse its already proved ACTUAL preterminal-floor theorem:
EVERY original Gamma0 row is valid for ANY public psi<=F<=2. Section2
established exactly that premise, without requiring F>=c or Lambda.
The completed normal forms exclude other LOW cases. This proves full
row preservation on the original graph. HIGH/h0 glue uses only the
range and unchanged absorbing-region law, so remains valid globally.

## 6. All eight hidden sources fall inside the ceiling

Minimum hidden profiles have root7/8, original core left child0 and
terminal source B depth7. Hence core height>=7. Their actual A sources
are

    r(p(f(A,y(B,C)),D),E), helper LL;
    r(p(A,f(B,y(C,D))),E), helper LR.                       (8)

In LL, f is anonymous and p>y>0, so Score0 is either hidden below y
or its opaque support at depth>=4. The other branches are above p/r.
In LR, p/f precede Score0, so both are anonymous and LL contains no
Score. Right branches exceed r. A fresh source G reads slot0=r or an
actual root child; it cannot fabricate0. Thus every original hidden
source satisfies (1), with all unused/raw fields retained. The actual
maximum sources RR/RL have the corresponding explicit upper-side
order, no observed8, and satisfy H_max. No restriction on private
support is assumed: these are consequences of each actual edge.

Transfer15's target floor is independent of the debt assignment, so
F(target)>=psi(target)>=1 on every Gamma1 zero. Equations(2),(8) give
F(source)<=1. The EXACT original signed repayment is

    w_original+F(t)-F(s)
       = F(t)-F(s) = [F(t)-1]+[1-F(s)] >=0.                (9)

All8 hidden profile IDs are therefore CLOSED for F. Full original H2,
q4,w0 and endpoints are unchanged. The previous visible Gamma1 theorem
also remains valid: it is a previously valid row theorem, and (2)
preserves all such rows. All previously completed source/incoming proofs
transport by signed row preservation even though F is below Lambda on
some H states. Full147-O/127-M, SAME actual midpoint, independent scopes,
free HIGH v, weak LE/G/unused fields and corrected h0 remain literal.

The original signed-walk bridge now includes these eight new zero rows;
the saved endpoint range still gives bound-7 and fully closed bound0
on walks under its stated row coverage. Full Step4 is NOT inferred:
the36 residual H1 schemas still need a proof for F. An old critical-seed
classifier need not survive a downward ceiling by its former proof;
the new preservation argument identifies any NEW failure into H as
impossible, so only old unproved H1 rows with unchanged targets can
remain. PARTITION_UPDATE.md states this interface precisely.

No original negative cycle or whole-signature certificate is claimed.
No finite tests, original root/psi queries, bank censuses or label fits
are used. The one principal theorem is the incoming-safe ceiling, not
a statement that a new global J exists.
