# Source-exact repayment after the inherited deep episode

**PROVED—RESTRICTED DOMAIN.** After TR's fixed deep episode,
every next nontrivial named-core access pays a spare physical A
unit. So does every next access in an initially paired identical
gap, of arbitrary size and shape. The proof has unbounded fringe
size, not an increasing finite fit. Unequal interiors are handled
by an exact escape condition, not silently assumed identical.

**Full FE02-CD, FE02-RIGIDITY and Universal Coarse-Double remain
OPEN.** Neither diagonal reachability nor actual closed nonvacuity
of this particular deep pattern has been established. The theorem
below excludes its specified saturated continuations if they occur;
it does not demonstrate strict new reachable closed-walk coverage.

## 1. Source pattern, physical meaning and full quantifiers

Use exactly TR's16 named ordered keys, its original source pair
and the five-block word P=KEEP(16,10,9,8,1). Each original inorder
gap i=0,...,16 may contain arbitrary paired BST bodies A_Fi,B_Fi
on the same finite ordered key set. The bodies need not be equal.
P never enters a body, so the unchanged original splay formulas
transport each body whole. Complete source rows and event IDs
are pinned in `terminal_depth_profile_certificate.json` and its
inherited raw source hash. No new source core was selected.

P has costs(1,3),(1,2),(1,2),(1,2),(1,2), hence one unpaid
B double over ten actual A units. Both endpoint roots are1.
Its complete endpoint pair differs from its initial pair in
explicit core parent links, irrespective of gap substitution.
P is not itself closed. Deleting B occurrences means masking
them, not removing keys from the BST. All depths below count
edges; a=ceil(d_A/2), q=floor(d_B/2).

## 2. Every next named-core access supplies a real unit

From the literal endpoint pair of P, the complete source table is:

| Next key | d_A | d_B | 2a-q |
|---:|---:|---:|---:|
|2|2|2|1|
|3|3|3|3|
|4|4|4|2|
|5|5|1|6|
|6|6|4|4|
|7|7|3|7|
|8|1|2|1|
|9|2|3|1|
|10|3|4|2|
|11|5|5|4|
|12|6|8|2|
|13|7|7|5|
|14|8|9|4|
|15|9|8|6|
|16|4|6|1|

This is an exhaustive15-target literal source classification,
not a claim inferred from sample n. None of these searches
enters a formal gap. Thus every row holds for arbitrarily
large, independently shaped gap substitutions. An access to
root1 creates no event and is not a new nontrivial A-root block.
An access with no KEEP has q=0 and pays even more capacity.

The two unmodified original engines agree on every complete
destination and physical event list. The table can also be
read directly from the pinned complete endpoint trees. It is
finite-exact core data used in a quantified substitution proof,
not a numerical feasibility certificate for general sources.

## 3. Every gap, with unbounded interiors

Let alpha_i and beta_i be the depths of the formal body root
at the endpoint in A and B. If target y lies in gap i with
local depths u_A,u_B, the complete source depths are EXACTLY

    d_A(y)=alpha_i+u_A,       d_B(y)=beta_i+u_B.       (DC1)

This follows by concatenating the explicit core search path
with the search path in the actual body. All earlier P accesses
were outside that body, so its shape is its original shape.
No match of the external A/B paths is assumed.

For u_A=u_B=u put

    r_i(u)=2ceil((alpha_i+u)/2)-floor((beta_i+u)/2).

Its exact integer recurrence is r_i(u+2)=r_i(u)+1. Consequently
r_i(2m+t)=r_i(t)+m for m>=0 and t in{0,1}. The following complete
two-parity table proves positivity for ALL u>=0:

| Gap i | alpha | beta | r(0) | r(1) |
|---:|---:|---:|---:|---:|
|0|1|1|2|1|
|1|3|3|3|2|
|2|4|4|2|4|
|3|5|5|4|3|
|4|6|5|4|5|
|5|7|5|6|5|
|6|8|5|6|7|
|7|8|4|6|8|
|8|3|4|2|2|
|9|4|5|2|3|
|10|6|6|3|5|
|11|7|9|4|3|
|12|8|9|4|5|
|13|9|10|5|5|
|14|10|10|5|7|
|15|10|9|6|7|
|16|5|7|3|2|

Thus if the paired bodies are identical, ANY first queried
key in that gap gives r>=1. Identity of shapes is sufficient,
not necessary: u_B<=u_A for the particular key also suffices,
by monotonicity of floor in DC1. Empty gaps have no queries;
their listed attachments describe possible nonempty substitutions.
The argument permits unbounded key sets and arbitrary internal
shape. No concrete fringe-depth sweep is used.

## 4. Exact unequal-interior escape signature

If there has been no next negative block after P in an FE02
candidate, that block cannot use a named key by Section2. It
must first enter an unequal gap. Since P has already used the
unique positive block, the new block must have delta=0, so

    floor((beta_i+u_B)/2)=2ceil((alpha_i+u_A)/2).

Equivalently, for the ACTUAL original terminal-zig bit z_B,

    u_B=4ceil((alpha_i+u_A)/2)+z_B-beta_i,
    z_B in {0,1}.                                    (DC2)

In particular u_B>u_A is necessary, since Section3 excludes
u_B<=u_A. DC2 is a necessary-and-sufficient source depth test
for that one query, with all BST compatibility still required.
It is not a new global invariant or a proof of cyclic feasibility.
DC02 supplies one explicit compatible source realization of it.

## 5. Exact paired closure and the distinct-unit reconstruction

Suppose an original exactly paired-closed FE02 walk contains
the P pattern. Same-key physical followers and mixed DELETE/KEEP
owners are allowed, using inherited complete-block projection.
P's explicit endpoint pair differs from its input. Thus a
closing continuation cannot consist solely of root1 no-ops:
there is a NEXT nontrivial root block in that physical period.
If it has no KEEP, it is negative. If it queries a named key,
Section2 forces negative. If it first queries an equal-depth
or A-deeper paired body key, Section3 forces negative.

In particular this proves FE02-CD for any such walk whose
next target after P is named-core, and for any such walk whose
paired initial gap bodies are all identical, with arbitrary
subsequent support and masks. Once the first real donor is
found, later history cannot undo the inequality under FE02's
fixed assumption that every other block is nonpositive.
No diagonal reachability premise is used by this local theorem;
it therefore applies to every reachable instance in this domain,
if any. This does NOT establish that such reachable instances
exist, or that all FE02 histories contain P.

For the actual donor block d, enumerate its 2a_d A units in
event/bit order. Use its first q_d units for its own B doubles,
and its last A-event bit1 for P's positive third B double.
Because q_d<=2a_d-1, that last unit is free. Every other
nonpositive block uses only its own first q units; the positive
block uses its own two bits on its first two demands. This
gives a complete distinct-unit injection over the actual period.
Choose a physical cyclic cut at d's A leader if chronological
availability is required; no startup or repeated unit is needed.

If the leader is DELETE, its A events still belong to that
leader. B is frozen until the block's first KEEP, which owns
its real B doubles. The depth calculations use the same
block entrance B, not a counterfactual B splay at the leader.
No source comparison correction is counted as physical work.

`core_repayment_injection_certificate.json` checks actual event
injections for P followed by EACH possible named next key.
Those prefixes are open; the certificate does not pretend they
are closed histories or causally earlier donors. The one-period
cut assertion above applies to an actual closed embedding only.

## 6. Reachability and cyclic closure are still essential globally

The unequal-gap escape in DC02 leaves the deficit unpaid with
exactly one positive and all other blocks saturated. It is an
OPEN prefix, not a reachable closed counterexample. It prevents
replacing the missing global theorem by the claim that P must
pay at its next block merely because gap key sets agree.

After an unequal-gap query, the original source rotations can
change external attachments as well as the interior body.
The terminal table in Sections2–3 no longer describes that new
pair. Reapplying it without proving a returned source pattern
would be an invalid invariant. No proof here forces successive
escapes to lie in strictly nested gaps, to use fresh keys, or
to terminate before exact paired source restoration.

The missing obligation remains an all-size COUPLED return bound
for that boundary/interior evolution, using actual reachable
paired cyclic closure. Merely assuming its eventual donor would
restate FE02. DC03 records the completed failed-global-gate review.
