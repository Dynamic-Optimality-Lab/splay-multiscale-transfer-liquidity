# Coupled source closure across arbitrary many ordered anchor excursions

**PROVED—UNIVERSAL at the explicit root-word domain below.** The
theorem composes the FULL original source actions, including base lifts
and boundary corrections. A/B interiors may be arbitrarily unequal.
It permits any number of left/right excursions and arbitrary alternation
of their sides, without treating comparison rotations as physical credit.
It is a restricted coupled closure theorem, not full arbitrary-overlap FE02.

## 1. Exact source and cyclic excursion domain

Use original maximal cyclic A-root blocks with a>=1, B-double demand q
and delta=q-2a. Their costed KEEP projection preserves complete boundary
trees while retaining the actual A leader/B-first-KEEP event owners.
A KEEP-less block is negative, delta=-2a, and already supplies a spare unit.

Choose an ACTUALLY VISITED key g. An excursion begins AFTER one complete
g block and includes all subsequent blocks through the NEXT g block.
The starting g block is not counted again: each block of the cyclic
period belongs to exactly one such excursion, as an interior or return.
Call an excursion ordered if its interior keys are either

    g<r0<r1<...<rk,       or       g>r0>r1>...>rk,

followed by return to g. The number k>=0, source depths, key gaps,
support in each excursion and total number of excursions are arbitrary.
Excursions may alternate sides in any order and use different keys.

The theorem assumes the cyclic root word admits such a g with EVERY
excursion ordered. It does not assert that an arbitrary FE02 word does.
All original masks and zero-cost same-key followers remain permitted.

## 2. Side-isolation lemma for the full source

Let a single source tree initially be ROOTED AT g. Execute any history
whose targets are <=g. Then the ENTIRE initial right subtree of node g
remains attached as its right subtree throughout the history. The
reflected statement holds for targets>=g and g's left subtree. Interior
targets can approach or turn; ordering is unnecessary for this lemma.

Proof: initially all keys>g are in precisely that right subtree R.
A search for a target<=g never enters R. Rotations away from node g
leave R as a whole untouched subtree. A rotation involving g with a
smaller accessed target can only rotate a left descendant over g,
preserving g.right=R. No node of R can be promoted above g, since
none is on that search path. At a direct access to g, every ancestor
of g lies on its <=g side; promoting g above those ancestors affects
its left side and still preserves R. This inductive invariant follows
equivalently from all six original source formulas. Empty R is included.
QED.

The initial-root condition matters; no such claim is made for an
arbitrary nonroot g with pre-existing ancestors on its opposite side.
The two trees may have completely DIFFERENT R subtrees: each preserves
its OWN whole subtree. A frozen B DELETE action changes nothing.

At the common anchor cuts of a no-negative walk, every block contains
KEEP and both trees are rooted at g. Thus a right excursion leaves
each tree's entire left subtree at g unchanged, and a left excursion
leaves each entire right subtree unchanged, even though g is not
the global root during intermediate steps.

## 3. Exact reserve and strict source-child drift

Consider one right ordered excursion, with both initial trees rooted
at g and all its blocks KEEP-containing. Apply the inherited exact
old-root/far-side epsilon law to the departure and helpers. Each
epsilon_C,i belongs to{1,2}, is computed from the ORIGINAL source path,
and is the exact depth shift of g. For the returning g block,

    d_A=sum_(i=0)^k epsilon_A,i,
    d_B=sum_(i=0)^k epsilon_B,i,
    D=sum_(i=0)^k(2epsilon_A,i-epsilon_B,i)=2d_A-d_B>=0,
    2a_g-q_g=(d_A mod2)+ceil(D/2).                    (1)

This is the actual return capacity minus its own B-double demand,
not an abstract potential. If the excursion has no negative block,
its return cannot have negative excess, so (1) forces ZERO reserve.
Consequently all paired epsilons are(1,2), d_A=k+1 is even, and k
is odd. A single-target excursion(k=0) therefore always has a negative
return, so cannot appear in a no-negative candidate.

Let p0 be B's ORIGINAL source depth1 child at the first departure.
The final outer RR of that departure gives

    B.right_child_at_g_before=p0,       g<p0<r0.

Let p_k be B's ORIGINAL source depth1 parent at its last helper.
The exact final outer LL at the return, including all base/correction
effects, gives

    B.right_child_at_g_after=p_k,
    r0<=r_(k-1)<p_k<rk.

Therefore in EVERY no-negative right excursion,

    B.right_child_after > B.right_child_before.      (2)

By side isolation, B.left_subtree_after=B.left_subtree_before EXACTLY.
Reflection proves that a no-negative left excursion strictly DECREASES
B's left child key while preserving its whole right subtree.

This is a coupled A/B statement: zero reserve is forced using BOTH
trees' epsilon sums and physical return costs. It is not a universal
B-only monotonicity claim on arbitrary source operations. Negative or
nonordered phases may reset the child; no monotonicity is asserted there.

## 4. Coupled closed-walk theorem

**Theorem.** Every nontrivial exactly closed original paired walk whose
cyclic root word admits an anchor g with all excursions ordered has
at least one genuine negative block.

Proof: assume all blocks are nonnegative. A KEEP-less block would be
negative, so all blocks have KEEP and their complete projected anchor
cuts have common root g. On every right excursion, (2) strictly increases
B's right child while side isolation fixes B's left subtree. On every
left excursion, the symmetric law strictly decreases B's left child
while fixing B's entire right subtree.

Thus across ALL excursions, B's right child never decreases and B's
left child never increases. At least one of these coordinates changes
strictly at EVERY excursion. There is at least one excursion in a
nontrivial walk. The final B tree cannot have the same child keys as
its initial source. This contradicts exact full paired closure. QED.

Opposite-direction excursions cannot undo each other's source defect:
each preserves the OTHER entire child subtree. This is the required
joint composition argument on this domain. It does not separately
cancel formal comparison rotations, erase base factors, assume matching
interiors or invent units from a returned ancestor.

## 5. Quantitative finite-progress bound

At an anchor cut let S_+ and S_- be the actual full key sets greater
and smaller than g. If nonempty, let rho_R be the rank of B's right
child in increasing S_+, and rho_L the rank of its left child in
increasing S_-. Define

    room_R=|S_+|-rho_R,      room_L=rho_L-1.

An empty side contributes0 and cannot support an excursion. For any
continuation of COMPLETE ordered excursions with no negative block,
the number N_R of right excursions is at most room_R and the number
N_L of left excursions at most room_L. Indeed every corresponding
child rank moves strictly by at least1, and opposite phases fix it.
Thus there can be at most room_R+room_L such unpaid excursions.

This counts finite source progress, not credit capacity. No rank jump
is assigned as a physical unit. If a longer open continuation does
not occur, no further event is claimed. For a closed period the direct
endpoint contradiction in section4 already forces a negative WITHIN
THAT period; no repeated-period capacity is imported to use the bound.

## 6. FE02 and distinct physical units

Under FE02's hypothesis of one positive(1,3) block and all others
delta<=0, the theorem forces one other block j with delta_j<=-1.
Then sum delta<=1-1=0, so Q<=2A on this root-word class.

Assign each nonpositive block's own q doubles to its first q actual
A units in event-index/bit order. The positive uses its own two bits
for its first two doubles. Choose the first negative block after it
in one cyclic traversal; its last A-event bit1 is unused after own
payment because q_j<=2a_j-1. Assign that one actual unit to the
positive's third double. Units and demands remain distinct, original
mixed owners stay at leader/first KEEP, and no startup or another
period is used. No FI/PF/FE algorithm or reservation is changed.

If the entire closed walk has only one unchanged root, exact closure
permits no once-only B-root change and Q=A=0. Empty/single-key cases
cannot have a positive(1,3). They are not nontrivial excursions.

## Domain limit

The root-word condition is substantial. An arbitrary FE02 history
need not admit such an anchor; CE02 gives an exact reachable closed
counterexample to that unqualified coverage claim. Whether hypothetical
one-positive ALL-SATURATED candidates are excluded when every possible
anchor has nonordered phases remains OPEN. This theorem does not
replace that remaining domain by an unproved good-anchor assumption.
