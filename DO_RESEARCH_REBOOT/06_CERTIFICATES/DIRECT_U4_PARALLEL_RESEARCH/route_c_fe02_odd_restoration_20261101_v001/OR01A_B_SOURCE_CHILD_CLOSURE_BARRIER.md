# A stronger source-closure consequence of the same normal form

This addendum strengthens OR01's closure branch without changing its
ordered-helper hypothesis or imposing a fresh-pair agreement assumption.
It uses the SAME original parent keys; no new source audit is run.

## The original B child cannot return in the unpaid branch

Start BEFORE departure at the common root g, with g<r0, as in OR01.
Suppose the first return to g after r0<r1<...<rk has zero reserve.
The exact reserve identity forces every pair of source epsilons,
INCLUDING departure, to equal(1,2), and k to be odd.

Let p0 be B's original source depth1 parent at that departure. Its
last outer double is RR, so the B SOURCE BEFORE departure has

    right-child_B(g)=p0,      g<p0<r0.

OR01's last-return LL identity gives

    right-child_B(g after return)=p_k,
    r0<=r_(k-1)<p_k<rk.

Thus the original and returned B child lie on OPPOSITE SIDES of the
first departed target r0:

    p0<r0<p_k.                                      (B)

The full B tree cannot equal its source before departure. This is an
unconditional source NONCLOSURE result in the zero-reserve ordered
branch; it does not require any assumption about unrelated interior
ancestry. It also explains why restoration of g, even together with
the COMPLETE A tree, need not close the paired state.

Reflection gives p0>r0>p_k on the other side of g. Off-path subtree
sizes/shapes, different A/B interiors, arbitrary helper source depths
and original mixed masks do not affect the source child identities.

## Closed one-excursion source theorem

If a proposed exactly closed FE02 period begins at common root g,
departs to r0, has only the ordered-away helpers of OR01, and ends
at this FIRST return to g, then it has a real negative block.
Proof: if there is no earlier negative block, the returning block
either has the spare unit from the reserve identity, or (B) prevents
exact B-source closure. Since exact closure is the hypothesis, only
the spare-unit alternative remains. Assign its last actual A bit as
in OR01. The theorem has arbitrary size/interiors and no short-lag
bound, but its one-ordered-excursion ROOT-WORD scope is explicit.

This supplies a precise source spare-or-closure-contradiction theorem
on this subclass. An arbitrary overlapping closed walk is not proved
to have such an excursion as its full period. Do not use this result
to silently replace that arbitrary domain by scans or ordered walks.

## The remaining first-reset obstruction is now source-identifiable

In the full arbitrary FE02 case, the first restoration may be unpaid,
so (B) is a concrete remaining B-source defect. Exact later paired
closure at g requires its B child eventually to return from above r0
to the original p0 below r0. Consider successive later actual visits
to g: there must be a FIRST such child reset across r0 before closure.
Without any later nontrivial access, the already different B tree
could not change back, so this reset cannot be supplied by no-op
root followers.

What is missing is a proof that this source child reset, through
arbitrary approaching/crossing helpers and unequal interiors, forces
one spare physical A unit or another well-founded source obstruction.
No such reset theorem is established here. Counting all hidden keys,
assuming another ordered excursion, or iterating a depth signature
that no longer holds would be invalid.

In the actual OR02 control, p0=2, r0=7 and p1=8. The first restoration
returns B to child8 instead of its original child2. Later K2 supplies
a spare unit and the full common scan restores the original B source.
The exact source child barrier is independently visible in the
already checked full trees. B_child_barrier_certificate.json records
these source keys and their strict order, not a new finite fit.
