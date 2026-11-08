# F20 — forced joint supply for G<R<x<C and reflection

Status: MATHEMATICAL DERIVATION COMPLETE FOR THIS SOURCE CLASS;
INDEPENDENT AUDIT PENDING. Original maximal-core/deep/two-arrival hypotheses
and the exact post-own-tail comparison h_B are those of G20. This is not
a theorem about arbitrary extra immutable comparison extensions.

In this Hamiltonian extreme order, G,R are the lowest two marked keys
and C is the highest; x is another mark. All other marked keys lie in
(R,C). No restriction is imposed on anonymous physical keys outside M.

## 1. A source exclusion at a unary old root

If the old marked B root Y is unary in a macro and becomes a leaf there,
its immediately preceding genuine access created a root of degree1.
The root-degree formula forces that access to be Q1,z1. Thus the present
birth of Y is NOT selected by T19's H1/Q2,beta2 zero-death rule.
If this macro has u unary births, its selected arrivals satisfy k<=u-1.

Consequently, when2H>=Q+z (instead of the strict bound), the last unit
is fresh after all own payments: occupied own ordinals are at most
beta+z+k<=Q+z-1<2H. This is source-derived excluded-root supply, not an
unused-donor premise.

## 2. Saturated branch-root alternative before v

G20 already supplies all but H_p=H_v=1, vQ2/u1/beta1/z1. First let the
old B/A root before v be C. A one-event access R<C is zig, LR or LL.
Zig/LR leave old C on x's path below R; after the one-event return to
G<R that path contains R,C and has depth>=3, impossible for H_e=1.
Thus v is LL with middle x: its initial A has

    C(x(R(A,B),D),E).

The p access must leave R directly below G; otherwise x would be even
deeper. In the marked B history, the previous macro t creates C with
two NONLEAF children G and the other chain. Hence t is Q1,z0 or
Q2,u0,beta2,z1. Q1,z0 has a fresh last bit by strict surplus. If Q2 and
H_t>=2 it does too. H_t=1 is impossible: a single access to maximal
marked C ending with left child x and x.left=R must start with marked
root x or R (zig/mixed gives x, SS gives R). The actual old B root of
t is one of its ancestor children G or the chain root, neither x nor R.
Thus this alternative always has a donor in t (third predecessor).

## 3. Saturated unary-root alternative: the exact frame

Let the old B root before v be G. If t has H>=2 its Q1/u0/beta1/z1 tail
supplies the donor. Otherwise t,v,p,e are allH1, and the necessary original
A form before t is the proven FLIP_FRAME form

    C(x(G(A,R(B0,B1)),D),E).                    (F)

Let s be the preceding genuine macro (fourth before e); it ends at C.
Its marked B destination has children G (leaf), R (leaf), and one marked
chain ending at x. The root-degree identity gives exactly

    Q_s=1,z_s=0;  Q_s=2,z_s=0;  or Q_s=3,z_s=1.

In the last case u_s=2,beta_s=1. All strict-surplus cases supply s's
last bit immediately, leaving only the following small source cases.

### 3a. H_s=1,Q_s=2,z_s=0

For a SINGLE access to maximal marked C, the final top frame puts its old
root either at C.left=x (zig/mixed), or at x.left=G (SS). This holds even
for a longer single access. The old marked B root must be a direct marked
child of C afterward; x is deep in the other chain, so it cannot be x.
Thus the old root is G, a unary ancestor which becomes a leaf. Its birth
is excluded by part1. The equality2H=Q+z leaves s's last bit fresh.

### 3b. H_s=2,Q_s=3,z_s=1

The old marked root is one of G,R or the other chain root H. If G or R,
it is unary and part1 again leaves the last of the4 units free. Suppose
instead it is branching H, with R<H<C and H!=x. This source possibility
is ruled out by the TWO-EVENT EXPOSURE LEMMA proved below. Thus a fresh
last bit in s is source-forced in every actual case here.

### 3c. H_s=1,Q_s=3,z_s=1

The same final-top-frame observation forces the old root to be G. The
one event is RR on G->x->C; hence immediately before s A has G.right=x
and x.right=C. Let g be the genuine macro before s (fifth before e).
Its destination root G is unary in B, so g is Q1,u0,beta1,z1.

If H_g=1, a single A access to minimum marked G can yield that right
chain only by starting at marked root x (zig/mixed) or C (SS middle x).
But in B the old root becomes the unique marked child of G. If it were C,
the following access to C would have Q1, contradicting Q_s=3. If it were x,
x would be an ancestor of C and become a DIRECT marked child of C after s;
instead x lies deep in the other chain. Both contradict the actual B
history. Therefore H_g>=2 is FORCED, and g's last bit is unused after
all own-tail payments (u_g=0).

## 4. Two-event exposure lemma, including outside anonymous helpers

Claim: start with marked A root H, R<H<C,H!=x. No natural H=2 macro
ending at maximal marked C can end in(F).

One positive access to C, of cost2, is impossible by its final top frame:
the old root must be G or x, not H. Otherwise there are exactly TWO
changing accesses y then C, each one event; all other operations are
root repeats and remain in the original word.

If y<C, the final one-event C access requires y=x (zig/mixed) or y=G
(SS), from C.left=x,x.left=G.

* y=G: from old H>G, one-event access G yields right child H (zig/LR)
  or a middle child P with P.right=H (LL). The required pre-C right chain
  G->x->C would force H=x or H=C, impossible.
* y=x, H<x: before the final C access, its untouched x.left subtree is
  G(A,R(B0,B1)). The old root H lies below R, at depth>=3 from x, but
  one ordinary one-event splay can leave its old root only at depth1 or2.
* y=x, H>x: since C>H, the first access to x preserves H as an ancestor
  of C in its rigid right subtree. The final C access would need C to be
  x's direct right child or depth2 through a parent ABOVE C (RL), leaving
  no position for the intermediate ancestor H. RR cannot have the required
  final left child x. Thus it cannot cost one event.

If y>C, it is necessarily anonymous, so it MUST NOT be omitted. A
one-event access y from H<C gives either y.left=H (zig/RL) or
y.left=P with P.left=H (RR). To access C next in one event:

* in the first form, C must be H.right and the final mixed frame gives
  C.left=H, not the required x;
* in the second, P=C gives final C.left=H; P<C gives final C.left=P and
  P.left=H (forcing H=G); P>C puts C below H at depth>=3.

All contradict(F). y=C cannot be a first distinct changing access followed
by another changing C without an additional event. Thus all actual
two-event possibilities, including private keys outside the marked range,
are excluded. This proves the claim and part3b.

## 5. Joint physical source consequence

For every recovery in this order choose the first applicable source case:
G20 p/v; t in part2 or H_t>=2; s in3a/3b/strict surplus; g in3c.
Use that supplier's LAST actual physical bit. Each was proved comparison-
unused AFTER all own payments. This is at most FIVE preceding genuine
macros. Deep accesses have at least r-2>=5 intervening genuine macros,
so their five-predecessor windows are disjoint. Donors are globally distinct
for any finite repeated/shared collection, including collections mixed
with the other proved order classes. No global capacity assumption.

The result is joint source comparison supply, with the same complete-
cover/owner-exchange consequence and remaining physical-policy conditions
as O20. It does not supply the still-open order G<x<C<R or nondeep
larger-support fixed-Q6 classes. All new reasoning awaits independent audit.
