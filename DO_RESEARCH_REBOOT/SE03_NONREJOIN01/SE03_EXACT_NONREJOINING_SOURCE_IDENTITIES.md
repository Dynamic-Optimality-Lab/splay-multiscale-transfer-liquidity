# Exact source transport through retained accesses

Status: universal source identities and signed accounting below. No uniform
repayment, six-key closed-class novelty, key selection or support induction
is claimed by this file. The campaign continues after these intermediate
identities. Node letters denote distinct ordered keys; capital letters are
independent arbitrary BSTs in the indicated inorder gaps.

## 1. Original operations and the complete pair recurrence

Let F_t and E_t be the full and erased B trees on one correctly aligned
closed comparison interval. S_x is the original bottom-up splay, with
parent-first LL/RR and edge depth0 at the root. At original Kz the update is
(F,E)->(S_z(F),E), with charge difference floor(d_F(z)/2). At retained Ky it
is (F,E)->(S_y(F),S_y(E)), with difference

    j_t=floor(d_F(y)/2)-floor(d_E(y)/2).

At DELETE both trees and their charges are unchanged. A root splay is the
empty rotation word. A genuine depth-one B change has q=0 but changes the
full state and the later discrepancy. Repeated targets, changing ancestors
and arbitrary hangers are included by using each tree's own source frames.
The full ordered pair is a sufficient state by definition; no reduced
coordinate is asserted to be sufficient.

Write h_T(v)=floor(d_T(v)/2) and e_t(v)=h_Ft(v)-h_Et(v) for each retained
key v. For any splay in either tree, its change in h(v) is computed exactly
from the original rotation gain g and parity epsilon=d mod2:

    h_after(v)-h_before(v)=(g-epsilon_after+epsilon_before)/2.

Sum this over that tree's actual primitive rotation word. Both signs and
parities are retained. This is an equality, not a +2 displacement estimate.

## 2. A nonrejoining discrepancy moved by three retained accesses

Let y<p<z<w and

    T=y(A,p(B,z(C,w(D,E)))).

Begin F=E=T. Original Kz uses one RR double in F, whereas E freezes:

    F1=z(p(y(A,B),C),w(D,E)),
    E1=T.                                                   (1)

The direct erased charge is1. Retained Kw has F depth1 and E depth3.
In F it is a right ZIG. In E it is RR at p,z,w then a right ZIG at y:

    F2=w(z(p(y(A,B),C),D),E),
    E2=w(y(A,z(p(B,C),D)),E).                                (2)

Thus j_w=0-1=-1. Both roots are w, but the left children z and y differ.
Retained Ky uses LL at z,p,y plus a left ZIG at w in F, and one left ZIG
in E:

    F3=y(A,w(p(B,z(C,D)),E)),
    E3=y(A,w(z(p(B,C),D),E)).                                (3)

Here j_y=1-0=+1. Both roots are y, but the w-left children p and z differ.
Finally retained Kp uses RL at y,w,p in F, and LL at w,z,p plus a right
ZIG at y in E:

    F4=p(y(A,B),w(z(C,D),E)),
    E4=p(y(A,B),z(C,w(D,E))).                                (4)

Here j_p=1-1=0. The discrepancy has moved into the opposite right subtree;
its roots w and z differ. No rejoining occurred at any of these retained
accesses. F/E source depths were respectively (2,0) at erased Kz, then
(1,3),(3,1),(2,3). The direct cost is1, signed retained sum0, marginal1
on this prefix. No closed marginal, recurrent period or CD conclusion is
inferred from a prefix. Every displayed distinction holds under every legal
substitution for A,B,C,D,E because different named keys occupy the positions.

## 3. A common retained access creates another unit of pending double debt

Let v<y<p<z, let L,R,B,C,D be arbitrary gap BSTs, and start before Kz at

    T=y(v(L,R),p(B,z(C,D))).

After the erased Kz:

    F1=z(p(y(v(L,R),B),C),D), E1=T.                         (5)

Retained Kv uses LL at p,y,v then a left ZIG at z in F, versus a left
ZIG at y in E:

    F2=v(L,z(y(R,p(B,C)),D)),
    E2=v(L,y(R,p(B,z(C,D)))).                               (6)

The retained charge difference is1. Key y has h difference1 both before
and after Kv: depths (2,0) become (2,1). If B is nonempty with root b,
key b's depths change from (3,2) to (4,3). Its h difference therefore
changes from0 to1 although neither history accesses b. The retained Kv
can consume one positive difference while creating another through parity.
Original constraints are v<y<b<p<z for b in B. No source word is shared
between the two different frames.

## 4. Exact renewal transport and its uncanceled term

Fix the retained support M0. Consecutive retained accesses to a fixed v
partition an aligned cyclic period into v-gaps. Immediately after each
such access, both trees have root v and e(v)=0. Hence at the next access

    j_t = sum over preceding v-gap, excluding its ending access,
                  (e_(s+1)(v)-e_s(v)).                      (7)

This holds even when one of the accesses was nongenuine and the other
genuine, and even if it had zero doubles. It retains every intervening
erased-key and other retained-key rotation; DELETE changes contribute0.

Equivalently define the explicitly source-based signed sum

    P_t=sum_(v in M0) e_t(v).

At a retained Ky, e_after(y)=0, so exactly

    j_t + (P_(t+1)-P_t)
        = sum_(v in M0, v!=y) (e_(t+1)(v)-e_t(v)).           (8)

At erased Kz the P change is the sum of changes over all M0; at DELETE
it is0. Summing (8) over the fully aligned period cancels the P boundary
and gives

    J = sum_(erased Kz) Delta P
          + sum_(retained Ky) sum_(v!=y) Delta e(v).          (9)

Thus a genuine telescoping identity exists, but it includes the cross-key
transport term. Dropping that term, or assigning it a favorable sign, is
unjustified. Equation (6) exhibits a positive parity transfer in it. All
quantities on a comparison block must be divided by the SAME repetition
factor before using a per-original-period version. Its preperiod is excluded
by the inherited transient subtraction; no transient unit enters the sum.

## 5. What these identities establish and what they do not

Equations (1)-(9) are uniform in source size, all legal hanger populations
and shapes, and any larger genuine support consistent with the histories.
They explain persistent disagreement, both interference signs, transfers
between retained keys and the exact extra term in a tempting telescoping
argument. They do not prove that the extra term is independently fundable,
that the illustrated prefix closes with a particular support, or that a
favorable erased key exists. No finite test or uniform induction follows.
