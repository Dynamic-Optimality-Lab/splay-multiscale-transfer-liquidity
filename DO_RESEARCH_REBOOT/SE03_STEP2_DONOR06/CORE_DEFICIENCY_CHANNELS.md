# Exact signed channels for deficient closed cores

Theorem. Let an original B-closed history have r genuine KEEP marks,
fixed full marked core S and deficiency delta=2r-1-|S|>=0. Its fixed
inorder labels partition canonically into delta+1 channels. In EACH
channel the filtered label word is marked,unmarked,...,marked. Every
actual core subtree has channel mass0 or1, and a marked-rooted subtree
has mass1 in the channel of its root. This is a source theorem; it
does NOT construct independently evolving projected splay trees.

## Global prefix heights

Use CLOSED_CORE_SUBTREE_DENSITY.md, including its complete simultaneous
constraints on all marked-root cuts. Give a mark weight+1 and an unmarked
core node weight-1. In the fixed inorder label word let H(t) be the signed
prefix sum before position t, with H(0)=0. Before every marked label,

    0<=H(t)<=delta.

After it the height is at most delta+1. Between consecutive marks there
are only downward unit steps, whose final height is the next marked
prefix and is nonnegative. There are no core labels outside the extreme
marks. Hence the ENTIRE path stays in[0,delta+1], starts0 and ends
delta+1. This holds for all actual sorted masks, not a tested mask list.

For h=0,...,delta, give every up-step h->h+1 and down-step h+1->h the
channel h. Each core label has exactly one such channel. Crossings of a
fixed threshold necessarily alternate: up,down,up,...,up, because the
path starts below that threshold and ends above it. Thus each channel
has r_h>=1 marked labels and r_h-1 unmarked labels, in alternating order.
The marked sets partition M and sum_h r_h=r. No fictitious key is added.

## Every subtree has Boolean mass in each channel

Any actual rooted core subtree is a contiguous inorder interval[L,R).
Its total signed mass is H(R)-H(L)>=0 by the completed density theorem.
Define B_h(t)=1 if H(t)>h and0 otherwise. The channel-h signed mass of
that interval telescopes EXACTLY to

    mu_h([L,R))=B_h(R)-B_h(L).

Since H(R)>=H(L), this is0 or1, never-1. Summing the channel masses
recovers H(R)-H(L); each original node contributes to exactly one channel.

If the subtree root is a marked label of channel h, its left-child
subtree has nonnegative total mass, so H(L)<=h. Its right-child subtree
has nonnegative total mass, so H(R)>=h+1. Thus its own channel mass is1.
This also proves that EVERY unmarked node in channel h has at least one
channel-h marked descendant: its own contribution is-1 and both child
channel masses are nonnegative, so at least one child has positive mass.
The statement is uniform over arbitrary actual fringes and all delta.

## Exact core10 consequence

For r6,core10,delta1 there are TWO channels. Their marked supports are
nonempty, disjoint and total six, hence EACH has at most five marks.
The sixteen old necessary P-bit masks are expressed by the SAME two
threshold channels; no unproved monotonicity of P is imposed and no
actual mask is removed. Core11 has one channel and recovers alternating
labels. The deficiency-zero all-SS theorem is not imported at delta1.

## Why two CD5 calls do not close core10

The channels partition labels and signed mass, NOT original source
operations or capacity. An actual foreign-channel KEEP still rotates
the full B tree. It is not a DELETE in a physical channel projection
unless a separate source simulation theorem proves that statement.
The two genuine erased CD5 comparisons both retain the SAME actual A
trajectory. Adding their inequalities would spend its capacity twice.

A valid use therefore needs a source-exact channel simulation together
with a disjoint A-bit allocation, or a proved signed interface ledger
whose cross-channel terms cancel with established ownership. Neither is
implied by Boolean subtree masses or by the support sizes. This is a new
structural representation for attacking core10, not its repayment proof.
