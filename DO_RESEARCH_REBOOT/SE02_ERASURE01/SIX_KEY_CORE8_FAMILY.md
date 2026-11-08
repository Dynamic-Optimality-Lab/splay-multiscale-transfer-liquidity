# Six genuine KEEP keys, core8: an all-fringe signed-transfer family

Choose eight ordered skeleton keys

    z < p < b1 < b2 < b3 < b4 < b5 < b6.

Start from the diagonal (S,S), where

    S=b1(p(z,empty), right-vine(b2,b3,b4,b5,b6)).

Every empty pointer may be replaced independently by any mark-free BST in its
inorder interval. There are nine such hanger slots. Mark only

    M={z,b1,b2,b3,b4,b6};

p and b5 are unmarked Steiner nodes. This is a symbolic source family with
arbitrary ambient fringe, not a generated finite tree or sampled population.

Let y=b1 and define

    P = Dz, Kz, Ky,
    W = Kb2,Kb3,Kb4,Kb6,Kb4,Kb3,Kb2,Kb1,
    gamma_m = P^m W, for every integer m>=1.

## Complete source closure

At the beginning of P, z is y's same-side LEFT grandchild via p in both trees.
Dz performs one A LL DOUBLE; Kz is an A-root identity and one B LL DOUBLE.
Ky performs the inverse RR DOUBLE in both, restoring the full input pair S,S.
All nine hanger terms are restored, not just the roots or depth vector.
Thus P^m returns exactly S,S for every m by induction.

For W, the three accesses b2,b3,b4 successively perform child ZIGs on the
right spine. Access b6 performs one RR DOUBLE through the unmarked b5. Access
b4 is the exact inverse LL DOUBLE. Accesses b3,b2,b1 are the three inverse
child ZIGs in reverse order. Consequently W restores the complete S, including
its left p(z,empty) hanger and every other arbitrary fringe. The same identity
holds in A and B. The whole gamma_m is reachable from its starting diagonal,
fully paired-closed and legal for all m and all admissible hanger substitutions.

## Exact original and erased costs

P has A=2,Q=2. W has8 A events, each a=1, and exactly two B DOUBLEs (at b6
and its return b4), so A_W=8,Q_W=2. Repetition therefore gives

    A(gamma_m)=2m+8,
    Q_full(gamma_m)=2m+2.

Erase Kz to Dz. Every P becomes Dz,Dz,Ky, whose B remains S throughout;
A has the identical LL/noop/RR trajectory and returns S. W is unchanged.
The auxiliary already closes with u=0,L=1 and

    Q_erased=2,
    D_z=m, J_z=m, Delta_z=2m,
    R_z=4m+14, R=2m+14=R_z-Delta_z.

The m direct marginal demands occur at the starved Kz accesses (a=0,q=1).
The m indirect demands occur at Ky, which has q_full=1,q_erased=0. The actual
source A LL event at each Dz supplies its two distinct bit units to precisely
these two demands. No event from W or from another repetition is used. The
A RR return events are additional unused block capacity. This exhibits
positive signed marginals at the smallest support/core corner not covered at
entry: six genuine keys and core8, with an unbounded2m marginal as m grows.

## Strict domain separation from the two entry classes

Every KEEP in P or W changes the B root: consecutive retained targets differ,
including every join and the cyclic seam. The genuine support is EXACTLY M,
so |G|=6. At the start the two marked paths y->p->z and y->b2->...->b6 cover
all eight skeleton keys; no hanger contains a mark. Thus the marked core has
exactly8 nodes. Marked-core inclusion and full B closure force that same core
set at every boundary. Hence EVERY family member lies outside CD(5) and
outside the certified core<=7 class.

This proves strict enlargement of those two entry coverage domains by the
protected compensation theorem, without a finite novelty search. It does not
certify novelty against every historical packet/concatenation closure: P and W
are themselves closed components with previously familiar rotation mechanisms.
Bank25 is not changed. The new result is the explicit signed erasure accounting,
reserved physical compensation and proved source-contraction theorem at the
stated class, not an unrestricted support induction.
