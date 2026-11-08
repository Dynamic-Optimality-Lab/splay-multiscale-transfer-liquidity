# E21-COMP — extreme-order joint COMPARISON second donors

**Mathematical derivation complete at the comparison stage; independent
audit pending. This is a smaller theorem than the frozen effective-owner
target.** It does not assume that a comparison-safe bit is unowned by a.

Use actual original maximal-core source, r>=7, Q_e=r-1,H_e=1, exactly TWO
selected T19 arrivals, and the specified post-ALL-own-tail comparison h_B.
For every extreme-order recovery e, there is a source-forced supplier in
at most SEVEN genuine predecessor macros. Its LAST actual A-bit is outside
the entire image of h_B. Suppliers can be chosen simultaneously without
collisions; the joint proof is in REPEATED_SHARED_EXTREME.

## 1. First source guards

Use G20's explicit p/v donor if applicable. Use t if its Q1,z0 strict case
occurs, or if its small-Q saturation has H_t>=2. These source counts give
freshness after ALL own payments, not merely the absence of a local debt.
The remaining t,v,p,e all have H1. EXTREME_ORDER_NORMAL_FORM proves the
unary V family and branch W family. We now close BOTH, including arbitrary
anonymous middle operands and the exact A return.

## 2. Branch t alternative — a forced donor within five predecessors

t has Q2,u0,beta2,z1,H1 and starts at a marked root G or K; its target C
ends in W1 or W2. A one-event C access ending there can only have old
marked root G. Indeed every marked old root <C must occupy C.left=G or
C.left.left<G; K cannot. Every old marked root >C would have to occupy
C.right or C.right.right; the sole such mark R is not one of t's actual
old B ancestors. Thus old root G is forced by BOTH actual source trees.

Let s be the preceding macro (fourth before e). Its destination in B is
G with two children: R(leaf), and K with children C(leaf), other chain
ending at x. Q+c=2 gives

    s: Q1,z0; OR Q2,u1,beta1,z1.

The Q1 case always has strict surplus. The Q2 case has it when H_s>=2.
Only H_s=1,Q2 remains; its actual old B root is R or K.

Invert the single C access from G ending in W:

    A_G1 = G(A,C(x0,R(D,E)));
    A_G2 = G(A,R(C(x0,D),E));
    A_Gextra = G(A,P(C(x0,R(D,E)),F)), P>R;
    where x0=x(B0,B1).

The extra case MUST be retained: it is W2's anonymous-parent RL preimage.
But it cannot be produced by a ONE-event G access from any marked root:
the old root would be G.right=P>R or an even larger outer grandchild,
both outside M. Thus it is impossible under H_s=1.

In A_G1 a one-event G access can have old marked root C (zig/LR) or R
(LL); in A_G2 it can have only R. The actual old B root is R or K, with
K!=C,R. Hence it is R. In B this R was unary with child K. Let g be the
preceding macro (fifth before e), ending at R. Root degree1 forces

    g: Q1,u0,beta1,z1.

If H_g=1, invert s's single G access from R. Before s A is one of

    A_R1 = R(C(G(A,x0),D),E);
    A_R2 = R(G(A,C(x0,D)),E);
    A_R3 = R(P(A0,G(A1,C(x0,D))),E), P<G.

For a one-event R access ending in A_R1 the old marked root must be C
or G. In A_R2,A_R3 it must be G or below G. But g's ACTUAL old marked
B/A root is K, with G<K<C,K!=x. None of these positions can be K.
Therefore H_g>=2 is FORCED. Its last bit is fresh: g has Q1,u0,beta1,z1
and uses only its first two own units. This closes the branch alternative.

## 3. Unary t alternative — the fourth predecessor

t is Q1,u0,beta1,z1,H1. Let s be the fourth predecessor, ending at C in
V1 or V2. In B its three marked children are G(leaf),R(leaf),K->...->x.
Q+c=3 yields exactly

    Q_s=1,z_s=0; Q_s=2,z_s=0; Q_s=3,z_s=1.

For Q3 the old ancestors are G,R,K, with u2,beta1. Strict surplus handles
Q1, Q2 with H>=2 and Q3 with H>=3.

If Q2,z0,H1, final-root placement in V forces s's old marked root to be
G or R. That key becomes a B leaf, hence was a unary ancestor. Its birth
is excluded from T19 by X21's incoming-degree1 rule. The equality2H=Q+z
therefore leaves the LAST bit fresh after all own payments.

If Q3,z1,H2, its old root is one of G,R,K. For G/R the SAME excluded-root
argument leaves the fourth bit fresh. Old root K is impossible by X21's
two-event exposure lemma: G<K<C, K!=x and V has G an ancestor of K below
x. This includes every possible anonymous helper. Thus this case also
has a donor in s.

Only H_s=1,Q_s=3 remains. The old marked root Y is G or R by final-root
placement. Let Z be the other of {G,R}. Both Y,Z are unary on the incoming
B path; K is the branching ancestor retaining the remaining chain.

## 4. Unary H_s1/Q_s3 — source recursion through two extremes

Let g be the fifth predecessor, ending at Y. Since before s its marked
root Y is unary, g has Q1,u0,beta1,z1. If H_g>=2 it supplies its last bit.
Suppose H_g=1. The ACTUAL old B root before g is either Z or K, the next
vertex of s's three-ancestor path. It cannot be K: g then s would be TWO
one-event accesses ending at C in V from initial root K, contrary to X21.
Thus it is Z. The pre-s B path is Y->Z->K->C, K branching toward C and
the remaining marked chain; no synthetic B transition is substituted.

Let h be the sixth predecessor, ending at Z. After h, Z has children
Y(leaf), K(with children C leaf and the remaining chain). Thus

    h: Q1,z0; OR Q2,u1,beta1,z1.

Strict surplus handles Q1 and Q2 with H_h>=2. Only H_h=1,Q2 remains.
Its old B root is Y or K. We next prove it must be Y, not assume it.

### Exact A inverse families

The following terms include the anonymous parents needed by all one-event
inverses. They are shorthand for actual globally ordered source operands:

    A_G1 = G(A,C(x0,R(D,E)));
    A_G2 = G(A,R(C(x0,D),E));
    A_G3 = G(A,P(R(C(x0,D),E),F)), P>R;

    A_R1 = R(C(G(A,x0),D),E);
    A_R2 = R(G(A,C(x0,D)),E);
    A_R3 = R(P(A0,G(A1,C(x0,D))),E), P<G.

These two triples must NOT be confused with the different A_Gextra in
the branch proof. A_G3 has P.left=R; A_Gextra has P.left=C.

If Y=G, invert s's C access and then g's G access from old root R. The
tree BEFORE g is in {A_R1,A_R2,A_R3}. A one-event R access ending there
can have an old marked root only in {C,G}: old root placement is R.left
or R.left.left. Since h's source root is G or K, it is G=Y, not K.

If Y=R, invert s's C access and then g's R access from old root G. The
tree BEFORE g is in {A_G1,A_G2,A_G3}. A one-event G access ending there
can have an old marked root only in {C,R}: old placement is G.right or
G.right.right. Since h's source root is R or K, it is R=Y, not K.

For completeness these inverses can be checked directly without any
finite-state argument: from R a G access ending at A_G1 is LL through C;
ending at A_G2 is zig or LR with private parent<G; ending at A_G3 is
impossible. From G an R access ending at A_R1 is RR through C; ending
at A_R2 is zig or RL with private parent>R; ending at A_R3 is impossible.
Those are all single-event ordinary formulas and retain every hanger.

### The seventh predecessor is forced expensive

Before h, B is rooted at Y, unary with child K, and K has three children
Z(leaf),C(leaf),remaining chain. Let j be the seventh predecessor, ending
at Y. Q+c=1 forces j:Q1,u0,beta1,z1. Its actual old B/A root is K.

If Y=G, invert h's one-event R access from G in the A_R family above.
The tree BEFORE h is in the A_G family. If Y=R, the analogous one-event
G inverse gives the A_R family. A ONE-event j access from root K could
put that old root only at the direct/outer child positions just listed:
{C,R} in A_G, {C,G} in A_R, or private keys outside the marked range.
K is none of these. Therefore H_j>=2 is FORCED by the original source.

j's last actual bit is outside im(h_B): it has Q1,u0,beta1,z1, so only
its first two units are used and H_j>=2. This is a physical comparison
donor even though the later R,G pair restores A exactly. The proof never
assumes the recovery/future x becomes deep and never spends the return
pair's already used bits.

## 5. Explicit deterministic rule and remaining interface

For each recovery take the first applicable case in this order: G20 p/v;
t's strict case; branch s/g rule; unary s/g/h/j rule. Assign the remaining
birth demand d_e to (tau_s,a_tau_s,1), where tau_s is the supplier macro's
LAST positive original A occurrence. It need not be its final KEEP.

Every case proves that bit is outside the WHOLE specified im(h_B) after
ALL own-tail payments. No desired matching/cardinality premise occurs.
REPEATED_SHARED_EXTREME proves simultaneous nonduplication and mixed-order
compatibility by actual deep-free source intervals, not a false extension
of the old five-window argument to seven windows.

This proves an injective COMPARISON extension. An a owner may already use
any of these bits. EXTREME_OWNER_EXCHANGE records the exact conditional
effective consequence and the still-open endpoint/immutable-policy and
Bank25 interfaces. Those are NOT part of the claim proved in this file.
