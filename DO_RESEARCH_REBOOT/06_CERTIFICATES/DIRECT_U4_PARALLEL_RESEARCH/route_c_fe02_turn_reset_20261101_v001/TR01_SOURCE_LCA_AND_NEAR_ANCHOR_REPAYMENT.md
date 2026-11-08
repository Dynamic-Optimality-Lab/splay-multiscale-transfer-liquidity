# Source-exact turns and near-anchor repayment

Status: **PROVED—UNIVERSAL for the source identity and the stated
repayment condition. PROVED—RESTRICTED DOMAIN for coupled closed-walk
closure. Full FE02-CD and FE02-RIGIDITY remain OPEN.**

This report uses the original parent-first bottom-up rotations. Depths
count edges; a=ceil(d_A/2) counts physical A StepEvs, and q=floor(d_B/2)
counts physical B doubles. A terminal B zig changes the source but is
not a double demand. Comparison rotations from BL are not credits.

## 1. Source setting and exact LCA identity

Fix any finite BST initially rooted at a present key g. Make any
sequence of accesses to keys strictly greater than g, before returning
to g. Keys, length, approaches, turns and off-path subtrees are arbitrary.
By CE's source side-isolation lemma, all initial keys below g remain
in g.left, and every ancestor of g is greater than g. Thus g remains
on the left spine. The initial-root premise is essential. Reflection
gives the complete statement for accesses strictly below g.

Immediately before an interior target x>g, define from the ORIGINAL
source tree T:

- h=depth_T(g).
- v=LCA_T(g,x), and j=depth_T(v).
- If v=x, set e=0. Otherwise put n=depth_(T_v)(x)>0, where T_v is
  the original subtree rooted at v. Set e=1 when n is odd. For even
  n, set e=2 when the first two original directions toward x agree,
  and e=1 when they cross.

Then, for the original complete source splay,

    depth_(S_x T)(g) = h-j+e.                         (TR1)

All definitions use the source before the access, not an observed
future payer or a fitted path description. In this right excursion,
v!=x means the local path leaves v to the RIGHT, while g lies at v
or in its left subtree. Its first two directions are therefore RR
or RL in the even case.

Proof. If v=x, the subtree at x already contains g at relative depth
h-j. Promoting x over the j outer ancestors preserves x.left on that
side, so the relative depth remains h-j.

If v!=x, first splay x in the original subtree T_v. The original
old-root epsilon identity gives depth(v)=e after that local splay.
The entire original v.left subtree is on the far side of this access
and remains attached to v. Consequently g has local depth h-j+e;
this includes v=g. This epsilon identity follows directly from the
last original source operation: odd n ends in a zig, even n ends
in RR or RL, giving old-root depth 1,2,1 respectively.

It remains to check that lifting through the original j outer frames
does not change that depth. All these frames go LEFT and their keys
are greater than x. Apply BL's exact one-ancestor root-lift identity,
not an assumed associativity of independent splay operations. Each
base lift leaves x.left unchanged. At the innermost outer frame the
local first direction is RIGHT, crossing its LEFT entry, so the odd
comparison correction is absent. At each more external frame any
same-side comparison correction lies entirely in x.right: its two
old ancestor keys are both greater than x. Thus every correction
also preserves x.left, which contains g. Induction through all j
frames proves TR1 for the original full source. The v=x case has
the same argument starting with internal depth zero. QED.

No bound on h, j, n, support, key gaps or excursion length enters
this proof. Arbitrary unequal A/B interiors are permitted because
the identity is proved separately in each original tree.

## 2. Coupled signed recurrence and actual return reserve

Apply TR1 in both trees at a KEEP-containing block, taking the whole
block's exact boundary projection while keeping physical owners:
the actual A leader owns A events, and the actual first KEEP owns
B events. Let h_C,j_C,e_C be the quantities for tree C=A,B. Then

    D=2h_A-h_B,
    D'=D-2j_A+j_B+2e_A-e_B.                          (TR2)

For a genuinely frozen B DELETE action, set its update j_B=e_B=0
as bookkeeping; its depth stays h_B and it has no B demand. Do not
pretend a frozen tree performed a splay. A nontrivial KEEP-less
block already has delta=-2a<0 and supplies physical capacity.

At the actual returning g block, if it contains KEEP, put

    z_A = d_A mod 2,        D_return=2d_A-d_B.

Exactly, including negative D_return,

    2a_g-q_g = z_A + ceil(D_return/2).               (TR3)

Indeed 2ceil(d_A/2)=d_A+z_A, and
d_A-floor(d_B/2)=ceil((2d_A-d_B)/2). This is actual capacity minus
actual B demand. An approach can make D negative; it is incorrect
to inherit the nonnegative ordered-excursion deficit from CE.
TR2 is an identity, not an endpoint bound or a proof of FE02.

## 3. Universal final-helper repayment theorem

Consider a one-sided excursion starting at a common-root g cut,
with arbitrary previous accesses, approaches, turns and unequal
interiors. Let x be its last interior helper. If a block in the
excursion or the returning block has no KEEP, that nontrivial
block is already negative. Otherwise inspect the ORIGINAL B
source immediately before the last helper and require

    h_B-j_B+e_B <= 3.                               (TR4)

Then the actual returning g block has

    q_g <= 1,       a_g >= 1,       2a_g-q_g >= 1.   (TR5)

Proof. TR1 makes the left side of TR4 the exact B depth of g
after x. Same-key zero-cost followers do not change it. The next
root block returns to g, so its genuine B KEEP has depth at most
three, even if its A leader was DELETE. Thus q_g<=floor(3/2)=1.
Consecutive maximal A-root blocks have different keys, so the
actual returning A leader has positive depth and a_g>=1. QED.

A convenient sufficient condition is j_B>=h_B-1: the last helper
branches at g or its parent, or is itself sufficiently deep on
the anchor spine. Since e_B<=2, TR4 follows. This criterion does
not assume that the return is short in elapsed blocks or in key
support. Only the named last-helper SOURCE geometry is restricted.
The more general exact TR4 condition also includes e_B=0 and e_B=1
cases farther from g. Reflection proves the left-excursion version.

Two-target approach corollary. Suppose a right excursion has
exactly the two interior targets r0,r1 with g<r1<r0, followed by
g. It has a negative block. With no KEEP-less block, the departure
from a g-rooted B tree gives anchor depth h_B<=2 by epsilon. At
the next approach, both g and r1 lie in r0.left, so their LCA has
j_B>=1. TR1 gives new depth <=2-1+2=3. TR5 pays at the actual
return. No hypothesis is imposed on the initial A/B interior shapes.
This corollary is not an assumption that arbitrary walks have
two-target or short returns.

## 4. Exact physical injection under the original FE02 hypotheses

Suppose an exactly closed FE02 walk has its unique positive block
p with (a_p,q_p)=(1,3), and all other deltas are nonpositive.
If it contains a phase satisfying TR4, TR5 supplies a negative
block d. It cannot be p. Enumerate each block's physical A units
in event order and bit order 0,1. Pay each nonpositive block's
q demands with the first q of its OWN 2a units. Pay the first
two demands at p with its two own units. Pay p's third B double
with d's last A unit (last event, bit1).

Because q_d<=2a_d-1, that last unit was not used by d's own
demands. All block/event/bit occurrences are distinct; thus all
B demands are injected into distinct actual A units of ONE
period. Cut just before d's actual A leader. The donor exists
before p in that cyclic period; own units precede their own B
KEEP. No startup, repeated-period or future unit is imported.
The donor is selected by a source condition at the actual final
helper, not from observed later payer demands. This does not
modify FI, PF or FE reservation algorithms or their certificates.

Mixed masks obey exactly the same assignment: a DELETE leader
still owns its A units; intervening zero-A DELETE followers
freeze B; the first KEEP owns B demands; later same-key followers
have no new source events. KEEP projection moves no physical IDs.

Consequently TR4 excludes an actual class of hypothetical
single-positive saturated CLOSED returns, not just an isolated
locally saturated edge. This is a restricted FE02 theorem.

## 5. Coupled closure on an explicit enlarged source domain

Let a nontrivial exactly closed original paired walk have an
actually visited anchor g such that every excursion from g through
the next g block is one-sided, and is either:

1. ordered away from g as in CE; or
2. an arbitrary approaching/turning excursion whose last helper
   satisfies TR4 (unless a KEEP-less block already pays).

Then the walk has a negative block. Assume otherwise. Every
block contains KEEP, so both source trees really start each
excursion rooted at g. An excursion of type2 gives a negative
return by TR5, contradiction. Thus all excursions must be type1.
CE's coupled outward B-child drift plus whole opposite-subtree
isolation then contradicts exact B closure. QED. Under the FE02
hypotheses, Section4 gives Q<=2A and the physical injection.

This theorem permits arbitrarily many excursions, alternation
of their sides, arbitrary sizes and long internal turning phases.
It does not assert that every FE02 history has this anchor or
qualifying last-helper geometry. At the minimum VISITED anchor
all excursions are necessarily right-sided, but TR4 is not forced.

## 6. What the source result does not settle

In a hypothetical no-negative FE02 counterexample, every actual
anchor return has q>=2 and therefore B depth at least four. In
particular every last-helper update must avoid TR4:

    h_B-j_B+e_B >= 4.                               (TR6)

For a helper off the anchor spine, e_B<=2 implies h_B-j_B>=2;
when e_B=1 the residual is at least three. For a helper on the
spine, e_B=0 requires residual at least four. These are necessary
source restrictions, not a full cyclic compatibility theorem.

TR02 shows an exact valid-source episode satisfying the first
of these deep boundaries while resetting B's anchor child inward
and creating no spare unit. It has no established diagonal or
closed provenance. Full FE02 needs a source argument coupling
these deep prefixes and their complete paired closure. TR1–TR3
alone do not supply that endpoint argument. No new potential,
unproved successful cut, or terminal-matching construction is used.

## 7. Independent evidence, separate from proof

`independent_verify_turn_reset.py` imports neither the producer nor
any new splay implementation. It replays both unmodified original
engines, compares whole destinations and physical events, and
obtains the LCA independently by intersecting source ancestor paths.
Its old-corpus audit has140 source updates and52 qualifying returns,
including reflected/symbolic repetitions, not52 new closed walks.
The 19-block walk's g=1 phase with internal keys5,6,4 turns; its
last helper has B(h,j,e)=(2,2,2), and actual block7 returns with
(a,q)=(1,1). Its last A-event bit1 pays positive block0's double2.
This is an actual closed nonordered phase, not hypothetical input.
The 19-block walk was already paid by PG02/FE01; no strict new
FI/PF/FE acceptance coverage is claimed.

The all-size claims above rest on the source proof, not on these
fixed finite audits. The sole new16-core episode is an exact
symbolic falsification template, with17 independent paired gap
bodies. It is disclosed as such; there is no larger finite fit.
