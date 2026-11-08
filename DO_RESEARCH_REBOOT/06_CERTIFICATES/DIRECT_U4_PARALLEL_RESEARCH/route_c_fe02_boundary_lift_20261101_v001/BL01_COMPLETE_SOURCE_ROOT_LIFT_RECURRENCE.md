# Step1: complete source root-lift recurrence

**PROVED—UNIVERSAL as a source tree identity.** This recurrence covers
even/even, odd/odd and both mixed parity cases, arbitrary unequal A/B
interiors, arbitrary external path length and both orientations. It
does not by itself prove a closed-walk cost inequality.

## 1. One ancestor, exactly

Let T=g(S,Q), let x be a present key in S, and put u=depth_S(x).
Let R=S_x(S), using the ORIGINAL parent-first ordinary source splay.
First form the one-zig lift over g:

    Z_g(R)=x(R.left, g(R.right,Q)).

Here g's child S is on the left. The right-child formula is its mirror.
Let p be the ORIGINAL root of S. Then

    S_x(T)=Z_g(R),

except when u is odd and x<p (the first internal source direction agrees
with g->S). In that exceptional same-side case, rotate the g node in
Z_g(R)'s right child to the right, promoting p. The resulting tree is
EXACTLY S_x(T).

Proof: if u is even, all internal frames are consumed by doubles and
the final source operation is the zig over g. If u is odd, internal
doubles consume u-1 frames; one original frame at p remains. The
global final operation combines g,p into a double. If the directions
cross, that double equals the internal final zig followed by the
outer zig. If the directions agree, the two parenthesizations are

    child-first split: x(L, g(p(R,C),Q)),
    original LL:       x(L, p(R,g(C,Q))).

They differ by precisely the stated internal right rotation. This
is the literal original LL identity with arbitrary subtree variables.
RR is the mirror; LR/RL have no correction. The u=0 case has R=S
already rooted at x and is just the outer zig. QED.

The correcting rotation is a COMPARISON between two factorizations.
It is not an extra operation of the original history, not an extra
A StepEv, and not an unused physical credit. In the same-side case
the split uses one more comparison rotation than the original physical
rotation path; its length must never replace original a or q.

## 2. Canonical common prefix and source notation

Use UI's canonical prefix K(A,B): recursively expose equal root keys,
and stop at first differing roots. Its holes are disagreement intervals
with equal key SETS but arbitrary unrelated A/B shapes. A common opaque
subtree is wholly agreed if its attachment path is common; it is not
a scalar credit or a sample fringe size.

For a target x outside K, let the first disagreement interval have
common external ancestor keys g_0,...,g_(h-1), from root inward. Let
t_0,...,t_(h-1) be their common source directions toward the interval.
Let u_A,u_B be the original depths of x inside its two interval trees.
Total source depths are d_C=h+u_C. If u_C>0, let s_C be the ORIGINAL
first direction from that interval root toward x.

When h=0 the global roots already disagree and K is empty. When x
itself is in K, its whole ancestor path is common; treat its subtree
as the initial body rooted at x with internal depth0 in both trees.
That common-target case is separately negative for a nontrivial block.

## 3. Deterministic recurrence for every outer word

Independently splay x inside each interval body, obtaining R_A,R_B.
For j=h-1,h-2,...,0, apply the one-ancestor identity to original g_j.
The ORIGINAL depth inside its child is

    v_C(j)=d_C-j-1=u_C+h-j-1.

Use the original sibling subtree at that frame. Form its base zig
lift and correct it iff

    v_C(j) is odd AND the next original source direction equals t_j.

For the innermost frame j=h-1 that next direction is s_C. For any
outer frame j<h-1 it is the shared t_(j+1). The original child root
is the relevant interval root at the innermost frame and the COMMON
g_(j+1) at every outer frame. These facts determine all names and
parities from the pre-access source; no output or future payer demand
selects a correction.

Induction: at each stage R_C is EXACTLY the original splay of x in
the original child subtree of the next frame. The one-ancestor source
identity therefore gives its exact larger-subtree splay. At the root
the recurrence yields S_x(A),S_x(B). This induction proves arbitrary
h and arbitrary interior depths. A finite outer-path table or bounded
fit is neither used nor needed.

This is a divide-and-conquer construction: solve the two interval
interiors, then lift their results through the common external context.
It keeps arbitrary paired sibling subtrees exactly and does not
pretend the remaining state is a bounded finite descriptor.

## 4. Actual source event provenance

When a comparison correction occurs at original source index j,
d_C-j is even and at least2. The original splay has the same-side
double at precisely that site, with bottom-up event index

    e_C(j)=(d_C-j-2)/2.

Its original source triple is(g_j,p_C,x), where p_C is that frame's
original child root. Its actual case is LL or RR according to t_j.
Both unmodified original engines verify these event IDs in the fixed
certificate. Cross doubles are also real demand/work, although they
require NO comparison correction. Formal base zigs at intermediate
lift levels are generally not physical terminal zigs of the history.

Thus the recurrence supplies a precise original-event label for each
correction, while explicitly forbidding the inference that the count
of corrections equals A capacity, B demand or spare units.

## Evidence boundary

Six primitive opaque identities verify LL,RR,LR,RL and the two zigs.
The fixed inherited audit has179 physical-source rows, all four parity
pairs and the13-core maximum already used in earlier campaigns. Each
larger source-prefix subproblem is drawn from those same trees; there
is no new source-size, horizon, repetition or coefficient sweep.
The all-size result is the source identity plus induction above.
