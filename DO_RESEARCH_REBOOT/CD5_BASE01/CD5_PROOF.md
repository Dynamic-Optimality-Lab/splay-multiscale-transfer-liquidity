# CD(5): complete original closed-walk base

## Exact statement and conventions

Let K be any finite totally ordered key set. Let gamma be any finite original
Pair Access walk reachable from a common-tree diagonal, with exact labeled
paired closure `(A_end,B_end)=(A_start,B_start)`. Reachability may use a prefix;
the closed walk is not required to start with A=B. KEEP splays its present key
in both trees; DELETE splays A and freezes B. No BST key is deleted. Define

    a_i=ceil(d_A(x_i)/2),
    q_i=floor(d_B(x_i)/2) on KEEP, and q_i=0 on DELETE,
    A=sum a_i, Q_B=sum q_i.

Depth counts edges. Define G(gamma) as the set of target keys of KEEP
occurrences which genuinely change the exact B tree. Let M(gamma) be all
KEEP target keys. The claim is

\[
\boxed{|G(\gamma)|\le5\quad\Longrightarrow\quad Q_B(\gamma)\le2A(\gamma).}
\]

All finite ambient sizes, all lengths and KEEP/DELETE patterns, arbitrary
repetitions, sparse labels, zero-cost events and nongenuine KEEPs are included.
This is the original closed-walk CD(5) statement; no prefix conclusion is made.

## 1. Genuine-support normalization, including the exceptional zero case

For present-key bottom-up splay, the final root is the accessed key. A root
access performs no rotation and preserves the full labeled tree. A nonroot
access changes its root and hence the tree. Therefore a KEEP is nongenuine
if and only if its target is the current B root; its q is then zero.

If G is empty, every KEEP has q=0 and DELETE has q=0 by definition. Thus
Q_B=0<=2A. This also covers the empty walk, no-KEEP walks and the empty key set.

Suppose G is nonempty. Extend the B-closed word periodically, which is valid
because its full B endpoint equals its start. Before any occurrence there is
a latest preceding genuine KEEP in this cyclic period. Its target is the B
root; every intervening operation leaves that root unchanged. Each nongenuine
KEEP therefore targets a key in G, as does every genuine KEEP. Hence M subset G.
The reverse inclusion is definitional, so **M=G**. This argument uses B closure,
not diagonal equality, and remains valid at an arbitrary cyclic seam.

## 2. Uniform five-key geometry at every boundary

For nonempty marked M, C_M(B) is the union of root-to-mark paths, with original
key identities and inherited edges. Reuse the banked arbitrary-M K4-L1 theorem:
marked splay never increases its size; unmarked splay increases it by at most2.

Here is the stronger set inclusion needed to avoid a gap between whole-walk
classes. If x is marked, every rotating operand lies on its path and hence in
the old C_M. Each old hanging subtree disjoint from C_M has no marked key.
Its internal key set and structure remain rigid throughout the splay because
no rotating operand is inside it; reattachment moves the whole subtree.
Consequently no node outside the old C_M can become an ancestor of a mark:

    C_M(S_x(B)) subset C_M(B).

Every KEEP target is in M; DELETE freezes B. Exact B closure therefore yields
a cyclic chain of inclusions with equal first/last set. Each inclusion is
equality. Thus one fixed labeled core S=C_M(B_t) serves every boundary.

For completeness, the banked growing-visited-set argument bounds |S|. Cut the
cycle immediately after a KEEP of k1, and start with V={k1}. Its core is the
root singleton. Revisited targets cannot increase the current V-core. On first
visiting x outside V, the unmarked K4-L1 bound adds at most2. After splaying x,
x is root and already belongs to the nonempty V-core, so adjoining x to V adds
no further core node. Induction gives c_V<=1+2(|V|-1). After a whole period,
V=M and B has returned to the cut state. Core constancy transfers the bound
to every original boundary:

\[
|M|\le |S|\le2|M|-1.
\]

For |M|=5, the single whole-walk core size c is an integer in[5,9]. Therefore
either c<=8 at every boundary, or c=9 at every boundary. No walk can cross
between these two branches. This uses no finite-state enumeration.

The old CDK5-LOW paragraph suggesting core-key label swaps is not used.
The rigid-hanger/set-inclusion proof above agrees with the later sealed11F
core-constancy theorem. The old size/shape overapproximation certificate
remains sufficient for its stated <=8-core projection theorem.

## 3. Exhaustive application of completed class theorems

Fix gamma with |G|<=5. The G=empty case is already proved. Otherwise M=G:

| Whole-walk hypothesis | Completed theorem applied | Conclusion |
|---|---|---|
| 1<=|M|<=3 | RT2 root-return/idempotence/depth4 class theorem | Q_B<=2A |
| |M|=4 | CDK4 all-size reduction and one-bit closed-cycle certificate | Q_B<=2A |
| |M|=5 and c in[5,8] | CDK5-LOW all-size reduction and sealed reduced certificate | Q_B<=2A |
| |M|=5 and c=9 | RESTRICTED_CD_STEP04 universal original W_5^9 certificate | Q_B<=2A |

For the first three nonzero branches, the already proved charge chain is
Q_B<=2C_KEEP<=2C_full<=2A. Both cyclic seams are covered by exact paired closure.
The A charges include DELETEs and nongenuine KEEPs, and each charge is used
once. For the last branch, the completed11F simulation and full M3 sign bound
give the original total inequality directly. We do NOT replace its A cost by
C_KEEP; the known nine-core obstruction to Q_B<=2C_KEEP is irrelevant here.

Each leaf theorem is uniform in ambient size and word length. The lower-core
certificates enter only through their completed all-size reduction theorems;
they are not assumed to cover arbitrary trees by finite testing. The nine-core
leaf retains all126 masks, arbitrary admissible fringe/signatures, its raw
ordinary/midpoint interfaces and the h0 correction. No functions/potentials
from different leaves are combined, and no abstract graph is changed.

The cases are exhaustive: for integer k with0<=k<=5, either k=0,1<=k<=3,k=4,
or k=5; the last case has exactly the two core alternatives above. Applying
the appropriate completed theorem proves Q_B<=2A for every gamma in CD(5).

## Dependencies, scope and closure

Original supporting files and their declared historical hashes appear in
`dependency_pins.json`. `DOMAIN_AUDIT.md` identifies each imported theorem and
the source/closure bridges. The separate checker validates exact scope,
dependency closure, symbolic integer interval coverage and universal affine
identities; it reuses accepted proofs and never replays old semantic checks.

This seals the complete support<=5 base. It supplies neither a support-lifting
lemma for six or more genuine keys nor a bound for arbitrary nonclosed prefixes.
Unrestricted CD and Dynamic Optimality remain open. Bank25 remains25. The
independent audit is a separate derivation/checker in this campaign, not external
peer review or formal verification of the whole compiler. Publication requires
the audit, controllers and final resource/integrity gates to pass.
