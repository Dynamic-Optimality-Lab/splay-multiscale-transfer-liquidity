# First-gap predecessor projection: a source-geometric invariant

This projection keeps WHICH anchor arrangement is selected. It is not a
function only of the debt-value set or multiset, even when full B is given.

## Definition; arbitrary finite private populations

Fix n>=2 ordered designated anchors. Normalize the minimum two as1,2.
Every active private key lies strictly between them and is DELETE-only.
Other private subtrees are rigid ordered gap terms, never accessed. A may
have arbitrarily many first-gap private ancestors in arbitrary positions.
Full B has an n-anchor backbone and the entire private population in rigid
gaps; no such private node is an ancestor of an anchor in B's backbone.

Define rho on the ACTUAL A tree, only for certificate evaluation. Prune
anchor-free gap terms. At an anchor retain its projected child shapes.
At a first-gap private node p, its left subtree contains either no anchor
or ONLY anchor1. In the former case retain the projected right subtree.
In the latter, make anchor1 the root of that right projection, with its
empty old-anchor left gap. Thus rho promotes the minimum anchor whenever
an anonymous first-gap branch separates anchor1 from higher anchors.
The physical anchor1 and every private node remain in the actual source.
There is exactly one anchor1 in rho, and all n anchors are retained.

All inactive private unary insertions leave rho unchanged. The rule needs
no private inventory, population cutoff, or future helper information.

## Uniform H1 marked-access identity

At a marked-root source, an actual one-event access to an anchor x
projects to the ordinary anchor splay of x with the SAME one-event cost.
Root identities project literally.

If no private node is on the length<=2 path, ordinary source substitution
commutes with rho. Otherwise the path has one private p between root g
and target x. If g=1, x is p.right's root; the actual RR double projects
to the old right zig. If g>1, p is g.left. For x=1 the actual LL double
projects to a left zig; for a higher x=p.right.root it projects to the
old LR double g,1,x. The left private term contains exactly anchor1 in
the latter cases. These are all possibilities by key order. Every other
source subtree stays arbitrary. This is uniform for every n and private
population, not a test of a bounded number of BSTs.

## Uniform private H1 helper identities

An actual H1 DELETE p, from an anchor-root source, satisfies

                 rho(S_p A) = S_1(rho(A)).

The right-hand cost is0 if the old root is1, otherwise1. To see this,
the original path to p has at most one intermediate parent. That parent
is anchor1, another anchor, or another first-gap private key. The four
ordinary double orientations preserve the same old anchor1 result after
folding. The complete nine free-term schemas are recorded in
first_gap_private_helper_normal_forms.json. The ancestor cases have no
unbounded hidden path: only their arbitrary off-path terms are projected.

After that helper the actual root is private p and rho's root is1.
Any following actual H1 anchor access x obeys

                 rho(S_x A) = S_x(rho(A)),

with old cost<=1 (cost0 for x=1). A higher x lies to the right of p;
its at-most-two-edge source frame projects with p playing anchor1.
For x=1, every path ancestor is first-gap private, and contraction leaves
the same old anchor1-rooted tree. All six generic source schemas are
recorded separately, including arbitrary private payloads. They cover
both parent types and source orientations within this first-gap order.

Consequently every natural packet with two H1 accesses has a legitimate
old comparison word of whole cost<=2: an old-anchor helper stays itself,
a private helper maps to DELETE1, and the genuine terminal anchor stays
itself. All original zero operations and nongenuine KEEP occurrences remain
in the actual source. A lone positive private access cannot be followed
only by zeros and end at a different old-anchor genuine target. Thus
there is no omitted private-terminal LOW case. The original H=2 is NEVER
replaced in actual credit accounting by the smaller comparison cost.

## Direct H2 marked-access classification

An actual H2 access has length three or four. Expose EVERY path operand.
All private path labels lie between anchor1 and the remaining anchors.
If anchor1 is on the path, it is the smallest marked path label. Otherwise
it is the sole old anchor in the off-path term below the smallest private
path label. That entire term projects to an anchor1 leaf. Between private
path labels there are no other anchors; all higher ordered gaps project
to arbitrary old-anchor subtrees. This grammar is exhaustive independently
of how many private keys lie in those terms.

The complete46 colored source-path schemas (including H1) in
first_gap_predecessor_direct_LOW_normal_forms.json classify as follows:

| Class | Schemas | Required source property |
|---|---:|---|
| Ordinary comparison commutes |36|accepted old LOW inequality, old cost<=actual cost|
| Extra-event LL/RR reassociation |3|accepted critical-quartet property and reflection|
| LLL/LLR reassociation |3|accepted internal RRR/RRL coefficient property, reflected|
| RLL, old root is anchor1 |2|new complete2002-source-shape coefficient lemma|
| LRR, old immediate left child is anchor1 |2|new complete2002-source-shape coefficient lemma|

For the last two classes the whole actual and old costs both equal2.
Their all-positive-source checks have584 and1149 potentially constraining
couplings; zero source debts and all other couplings are automatic from
Q<=4 and D in[0,3]. They are independently audited in
first_gap_new_H2_coefficients_independent_audit.json. These are exact
finite coefficient lemmas on the frozen ten-anchor function, lifted by
the source terms; no finite private-population test is used as proof.

No old source primitive is assumed to reproduce the projected endpoint
at the same cost in a noncommuting case. The explicit reassociation laws
are precisely the necessary signed correction. The old cost-free unary
simulation counterexample remains valid and is not reopened.

For a GENERAL n-anchor coefficient, the H1/helper identities above are
unconditional source lemmas; its noncommuting H2 coefficient obligations
would still require proof. The verified numerical coefficient instantiation
here is ten anchors only. Do not promote it to all genuine support sizes.
