# A universal Paired Ordered-Retreat Compatibility Lemma

**PROVED—UNIVERSAL at the stated source scope.** This genuinely compares
both trees. It permits arbitrarily long return intervals and arbitrary key
support/fringes. It does not assume that every closed walk contains an
interval of this kind, or that the lemma by itself closes FE02.

## 1. Exact paired source law at a shared root

Let A,B be ANY finite ordered BSTs on the same keys with common root r,
possibly different interiors. Execute ordinary source splaying at x!=r in
each. Let epsilon_C be the final depth of the old root r in C, C=A,B.
The inherited exact source theorem gives epsilon_C in {1,2}: it is2 for
even access depth and final outer LL/RR, and1 for a final zig or outer cross.
It is computable from the ORIGINAL source path.

For y=r, its depth shift is epsilon_C. For a tracked y on the OPPOSITE
side of r from x, its depth shift is ALSO exactly epsilon_C. Indeed the
search path enters the other child of r. Every earlier consumed site
excludes r's original far-side subtree. At the last operation that subtree
remains attached below r: LL/D and RR/A shift it by2, cross LR/D and RL/A
by1, and the old-root outer zig fringe by1. Every internal descendant has
the same shift; subtree shape and internal depth cancel.

Define the paired depth gap g(y)=d_B(y)-2d_A(y). On either of these roles,

    g_after(y)-g_before(y)=epsilon_B-2epsilon_A<=0.          (1)

The possible increments for (epsilon_A,epsilon_B)=(1,1),(1,2),(2,1),(2,2)
are respectively -1,0,-3,-2. Equality occurs ONLY for (1,2).
This is an actual coupled inequality. It is not the independent +2 bound,
an assumed matching, or an equivalent form of Coarse-Double.

## 2. A return of arbitrary length

Use the inherited complete-block projection only on a recurrent candidate
saturated return. Every block must contain KEEP; at its boundaries the roots
agree. Original mixed timing remains in its A-leader and first-KEEP owner
maps. A KEEP-less block already supplies negative slack and settles FE02-CD
by its established arithmetic branch, so it is never silently discarded.

Track y between two consecutive same-key macro occurrences p and j, gap
L=j-p>=2. At p both trees end with root y. The first departure at p+1
uses y as the common old root. Call the interval **retreat-only** if at every
later intermediate block t=p+2,...,j-1, y and the new target x_t lie on
opposite sides of the common old root r_t=x_(t-1):

    (y-r_t)(x_t-r_t)<0.                                    (2)

Thus after departure all those roots move strictly farther away from y on
one ordered side. They may be arbitrarily many distinct keys. No constant
lag, support, fringe bound or prescribed repayment time is imposed.

By the EXACT individual far-side identities, not merely their paired sign,

    d_A,j(y)=sum_(t=p+1)^(j-1) epsilon_A,t,
    d_B,j(y)=sum_(t=p+1)^(j-1) epsilon_B,t.                  (3)

Consequently g_pre_return is the sum in (1), so g<=0. This is a local source
trajectory theorem: no global closure/cost inequality was used to prove it.
Cyclic extension locates predecessors, never extra credit supply.

## 3. Complete saturation/equality classification

Write d=d_A,j(y) and a=ceil(d/2). Since d_B<=2d,

    q_B=floor(d_B/2)<=d<=2a.                               (4)

Every retreat-only return is therefore NONPOSITIVE. A positive(1,3)
return can NEVER have such an interval. For a return to be SATURATED,
q_B=2a, equality must hold throughout (4). This forces:

1. d is even;
2. d_B=2d (the bound and q_B>=2a leave no other value);
3. EVERY paired step has (epsilon_A,epsilon_B)=(1,2).

Conversely these conditions give saturation. Under condition3, (3) gives
d_A=L-1 and d_B=2(L-1). Thus saturation is equivalent to

    all paired departures (1,2), AND L odd.                 (5)

If any paired departure is different, or L is even, the return has
q_B<=2a-1 and a genuine last-unit donor. This is a sufficient direct source
repayment criterion independent of FE reservations, with arbitrary other
closed-history geometry. It does not require every return to be short.

In an arbitrary hypothetical single-positive saturated return, (5) is
MANDATORY at every retreat-only interval. Its B departure flag eta is0,
and the old source condition L>=2a+1+eta is then tight: L=2a+1. The unique
positive block must instead have an approaching/overlapping interval. These
are strengthened necessary compatibility constraints, not full impossibility.

The paired bound can also detect loss missed by the OLD initial-departure
gap bound: if L is odd, all A epsilons are1, the first B epsilon is2 but
some LATER B epsilon is1, the old ceiling L-1 equals capacity2a. Equation(3)
instead gives d_B<=2(L-1)-1, hence q_B<=2a-1. This is an algebraic strengthening;
strict new closed-walk coverage is not inferred without a separate witness.

## 4. A source separator witness for every equality step

At an equality step (epsilon_A,epsilon_B)=(1,2), B's last double is same-side.
Let p_B be its ORIGINAL source depth1 parent, distinct from r and x. Its
key lies strictly between r and x. B ends with x->p_B->r along that side.
A ends with r as a CHILD of x because epsilon_A=1. Since p_B is between
x and r, BST order places it inside r's inward subtree in A. Therefore

    r ancestor_A p_B, but p_B ancestor_B r.                 (6)

Before the access r was the root in BOTH trees and ancestor of p_B in both.
Equation(6) is thus a NEW ancestor-discordance pair, with explicit source
provenance. It is not a virtual credit, setup, terminal matching or potential.

During a retreat-only interval the open intervals between successive roots
are disjoint, so their p_B witnesses are distinct and none is a later target
before the final return. After a witness is created, both its keys lie in
the far-side subtree of every subsequent retreat root. That whole subtree's
internal ancestry is preserved by the original source rotations. Hence
all these witnessed inversions persist up to the return's entering state.

In particular a saturated retreat interval of gap L carries L-1 DISTINCT
separator witnesses. Its A path to y is the chain of earlier roots; the B
path interleaves each of the corresponding separators. This is a concrete
paired structural consequence of saturation, with no assumption about
whether those separator keys are accessed elsewhere in the closed period.

## 5. Why this is not FE02 closure

The final return or an approaching/crossing access may erase or transfer
these inversions. Different return intervals may overlap. No global theorem
has shown that their lifecycles force a negative block or enough DISTINCT
actual A capacity. PC03 supplies an exact obstruction to the simplest scalar
ancestor-discordance monotonicity extension.

A real closed four-key source control with KEEP(1,3,2,4) has NO retreat-only
return at all. It has no FE02 positive signature and refutes only the
unqualified existence assertion; a special existence theorem under saturation
would still require proof. Likewise no universal constant gap bound is
assumed. The diagonal ascending scan on s keys closes at the left vine
and has return gap s, arbitrarily large: by induction each successor access
extends the visited left spine, so the final tree is again the left vine.
This construction is an algebraic source observation, not a size sweep.

The principal FE02-RIGIDITY and FE02-CD objectives therefore remain OPEN.
This lemma preserves the full arbitrary-size target while excluding precisely
the retreat/equality violations described above. It does not silently replace
arbitrary histories by retreat-only, scanning or bounded-support histories.
