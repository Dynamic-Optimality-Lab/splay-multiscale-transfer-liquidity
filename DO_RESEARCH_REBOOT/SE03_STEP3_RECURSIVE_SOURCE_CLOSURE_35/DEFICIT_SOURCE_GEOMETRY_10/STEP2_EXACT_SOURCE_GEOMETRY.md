# Step 2 — exact original-source geometry of residual deficits

Status: universal symbolic derivation. Verification and terminal outcome
are recorded in STEP2_VERDICT.md. This is a structural theorem, not a
new matching, potential, source reduction or proof of global repayment.

Branch coarse-double-branch; HEAD
8c378d49283b3738b18e7175886772a98025e4e9.

## Frozen IAGS Box and pre-execution R1–R4

Target: characterize every residual double left by the frozen Step 1
map g_1, using literal full-B frames, exact A-cluster tests, and an
actual-source provenance/collision theorem for arbitrary collections.
Conditions: the original reachable, finite, exactly paired-closed W;
its fixed genuine support M and original full-B carrier S; every original
A operation, physical bit and existing assignment retained. No new cap.
Inheritance: ND35 SET potential and slot proof; ZRC35 final-rotation
theorem; PC35 and completed Step 1; accepted lifetime/root-entry lemmas.
Ambiguities: the new theorems give a FORWARD description of actual
sources. They do not characterize which abstract annotations are
realizable, promise global capacity, or certify frozen-policy freedom.
Bridge: four literal rotation identities -> exact LCA/blocker tests ->
canonical A-origin incidences -> nested collision chains at actual A
root changes. STEP2_INTERACTION_THEOREM.md proves the last implication.

R1: only geometry/provenance of the already fixed residual set is at
issue; no existential all-source donor construction is a premise.
R2: the exact two rotations enumerate LL,RR,LR,RL; LCA characterizes
subtree-label equality; B-subtree laminarity bounds shared incidences.
R3: one structural theorem and one bounded cached/symbolic audit. No
search, new splay execution, new potential, Gate U or Step 3 allocation.
R4: close the previously unspecified A-shadow conditions and the shape
of many-to-one preparation/root-entry collisions. Do not present the
remaining funding theorem under a different name as an advancement.

## 1. Frozen source and accepted dependencies

A performs every ordinary bottom-up access. B_F performs KEEP, including
identity root repetitions; DELETE is A-only, never physical deletion.
Each original A StepEv (u,j) has two distinct units (u,j,0),(u,j,1).
The virtual second unit of a zig is retained. No operation is suppressed.
At a KEEP t write A^t for the actual A tree AFTER its whole splay; its
root is x=x_t. It stays fixed throughout that occurrence's B phase.
Use S-descendant labels of actual subtrees; anonymous unary duplicates
in A count once. The old potential is Psi=|J_S(B_F) minus J_S(A)|.

The frozen Step 1 map g_1 preserves every g_plus and g_Z value and pays
all same-access release-payable neutral demands. Its unassigned demands
are an explicitly determined set F(W) of internal neutral doubles, with

    |F(W) at t| = d_t = (B0_t-B2_t-Z_t)_+.

Their IDs are exactly the tails of the increasing-index neutral lists
after Step 1, not a newly chosen selection of double representatives.
This document never changes g_1 or any historical map.

Inspected accepted sources:

* CONTINUATION_04/NEUTRAL_DOUBLE_SOURCE_DECOMPOSITION.md and its pinned
  independent_core_sector_neutral.json: universal raw ND35 and controls.
* ND35_COMPLEMENT_08/ND35_UNIVERSAL_AUDIT.md,
  ZIG_RELEASE_COMPLEMENT_THEOREM.md, LIFETIME_NORMAL_FORM.md,
  ROOT_ENTRY_LEMMA.md and independent_audit.json: verify159 accepts their
  stated raw/forward geometry scopes; no reverse realization or capacity.
* CONTINUATION_04/PROJECTED_CLUSTER_ACCESS_THEOREM.md and
  independent_projected_cluster_theorem.json: access-level release use.
* PC35_RELEASE_COMPLETION_09/STEP1_PC35_RELEASE_COMPLETION.md,
  STEP1_EXACT_RESIDUAL_IDENTITY.md and independent_release_audit.json:
  completed Step 1, including all parity and root-repeat cases.
* CONTINUATION_04/TOP_INTERVAL_AND_MARKED_DEMOTION.md: only its original
  marked-demotion specialization, not its separate potential, is used.

Exact dependency hashes and reused receipts appear in the verification
artifact. Same-agent separate implementation is not external review.

## 2. One literal rotation and exact A neutrality

Write L_B(v) for the S-descendant set of an actual B vertex v. In any
B rotation after A has root x, the promoted child's old proper label I
contains x. It is absent from J_S(A^t). The demoted pivot's new proper
label J excludes x. The whole frame label persists at its new root;
all other B labels persist. Thus

    Delta Psi = -1 + 1_{J absent from J_S(A^t)}.

This is exact, including the first parent rotation of LL/RR. Both operands
are in the actual carrier S, so I,J are nonempty, distinct, and the
exchanged labels are distinct from the other B labels.

For any nonempty K subset S let v_A(K) be the LCA in the FULL actual A
tree of the physical vertices with keys in K. Define its blocker set

    E_A(K) = (S intersect descendants_A(v_A(K))) minus K.

Then

    K in J_S(A)  iff  E_A(K) is empty.                 (LCA)

Proof: if an actual A subtree rooted at w has label K, then w is an
ancestor of v_A(K); the latter subtree contains K and is contained in
the former, hence has the same S-label K. Conversely v_A(K) itself
supplies the label when its S-descendants are exactly K. This argument
allows any number of anonymous/private nodes and duplicate labels.

Consequently one B rotation is neutral iff E_A(J) is nonempty. An
outside key z in this set is a real S vertex below the actual LCA of
J; it is not an imaginary donor or necessarily a genuine KEEP key.
If J lies entirely to one side of x, the LCA and every such blocker lie
in the corresponding actual root-side subtree of A^t, on that same side.

## 3. Exhaustive four-frame theorem

Write k(L,R) for an ordered physical BST node. T0,T1,T2,T3 are arbitrary
ordered hanging subtrees, including empty, private and S-bearing terms.
The displayed frame sits in an arbitrary unchanged full-B context.
Set U_i=S intersect keys(T_i). All unions below are set unions.
g,p,x are distinct actual S operands; x is the access target. Put

    W={g,p,x} union U0 union U1 union U2 union U3.

W is the whole original grandparent-frame S label. The identities are:

    LL, x<p<g:
      g(p(x(T0,T1),T2),T3)
        -> p(x(T0,T1),g(T2,T3))
        -> x(T0,p(T1,g(T2,T3))).

    RR, g<p<x:
      g(T0,p(T1,x(T2,T3)))
        -> p(g(T0,T1),x(T2,T3))
        -> x(p(g(T0,T1),T2),T3).

    LR, p<x<g:
      g(p(T0,x(T1,T2)),T3)
        -> g(x(p(T0,T1),T2),T3)
        -> x(p(T0,T1),g(T2,T3)).

    RL, g<x<p:
      g(T0,p(x(T1,T2),T3))
        -> g(T0,x(T1,p(T2,T3)))
        -> x(g(T0,T1),p(T2,T3)).

The exact removed/created proper labels, in rotation order, are:

| Form | I1 removed | J1 created | I2 removed | J2 created |
|---|---|---|---|---|
| LL | {p,x}+U0+U1+U2 | {g}+U2+U3 | {x}+U0+U1 | {p,g}+U1+U2+U3 |
| RR | {p,x}+U1+U2+U3 | {g}+U0+U1 | {x}+U2+U3 | {g,p}+U0+U1+U2 |
| LR | {x}+U1+U2 | {p}+U0+U1 | {p,x}+U0+U1+U2 | {g}+U2+U3 |
| RL | {x}+U1+U2 | {p}+U2+U3 | {p,x}+U1+U2+U3 | {g}+U0+U1 |

Here '+' abbreviates union, not cardinality addition. These formulas
follow by reading subtree descendants in the literal terms. Reflection
interchanges LL/RR and LR/RL, reversing key order and hanger order.

EXACT NEUTRALITY: the double is neutral iff BOTH E_A(J1) and E_A(J2)
are nonempty. If exactly one is empty it is B1; if both are empty it is
B2. No depth-only or contracted-A approximation is involved.

## 4. Outside-frame blocker geometry

Because W is an actual B-subtree label, it is an interval of sorted S.

LL: J1 is strictly contained in J2, and J2=W intersect {z:z>x}.
If neutral, a blocker for J2 is >x and outside W, hence >max(W).
A blocker for J1 may be in J2 minus J1 or beyond max(W); the same
outside key may block both. Two different blockers are NOT asserted.

RR: the reflected statement holds: J1 strictly contained in J2,
J2=W intersect {z:z<x}, and neutrality forces an actual blocker
<min(W). Inner and outer tests can again share a blocker.

LR: J1=W intersect {z:z<x}, J2=W intersect {z:z>x}. Neutrality forces
an A-LCA blocker <min(W) and another >max(W). They are distinct keys
in opposite actual A root-side subtrees. RL has the same two-sided
requirement, with J1 right and J2 left.

These conditions are necessary consequences of the EXACT LCA test.
The mere existence of outside S keys is not sufficient: they must lie
below the specified LCAs in A^t, for each created label separately.
The table plus these LCA conditions is necessary AND sufficient for
neutrality of an ACTUAL source frame, with all original source constraints
still retained. No claim makes an arbitrary formal frame reachable.

## 5. Whole-access path rewrite and deficit placement

Let the original full-B depth of x be h. The h proper B-subtree labels
containing x, one at each nonroot vertex of its original ancestor path,
form a strictly nested chain. All are absent from A^t rooted at x.
Every B rotation removes one such label and creates a label excluding x.
No created label can be removed by a later rotation of this same access,
whose removed label must contain x. There are h rotations. Therefore:

* The removed labels are EXACTLY the h original proper path labels,
  each removed once. Every neutral port is one of these actual path
  occurrences, not a fresh or duplicable cluster.
* The h created labels are distinct and persist to the end of this B
  access. Each is wholly on one side of x in the final B tree.
* The whole grandparent frames of successive doubles strictly expand
  by original S operands. Outside-frame blockers can be reused until
  an expanding frame absorbs their keys; they are not fresh work.

Let delta_t count created labels present in A^t. Then exactly

    delta_t=B1_t+2B2_t+Z_t,
    d_t=(q_t-delta_t)_+.

The fixed Step 1 residual IDs select certain internal neutral pairs of
this path rewrite. No other local form generates a residual demand.
The counts determine how many pairs remain; the literal order and g_1
determine WHICH original pairs remain.

Every genuine access has a final Psi-decreasing rotation. Thus delta_t>=1
and d_t<=q_t-1. If d_t>0, q_t>=2. At even depth h>=4, Z_t=0 and
B0_t>B2_t; at odd depth h>=5, Z_t=1 and B0_t>B2_t+1.

A final even-depth double cannot be neutral: its frame is the whole B
tree, leaving no required outside blocker. At odd depth the final
double's frame is a child of the old root, so outside-W keys lie on
only one side of W. Thus a neutral final double MUST be same-side and
aligned with its subsequent zig (LL then right zig, or RR then left
zig). A final opposite-side double cannot be neutral. Step 1 already
pays every neutral last double; all selected residual frames are internal.

## 6. Source-forced A work, without future-depth assumptions

Each residual pair supplies two removed missing labels, hence two actual
source incidences. Trace a label to its latest SET addition on W. If A
added it, that precise A rotation is mandatory; if B added it, A must
subsequently enter it before the port removes it. The interaction theorem
gives a canonical choice and proves exactly how these incidences can
share physical events. This is the required preparation/root-entry
interface. No future recovery or expensive A access is forced by it.

At maximal B core, the inherited same-side/no-zig source grammar applies.
For a residual double with marked old grandparent G and target x, the
original preceding genuine KEEP G left A rooted at G. Before B accesses
x, A is rooted at x, so at least one intervening actual A rotation loses
G's ancestry of x, with demoted pivot exactly G. All helpers are included.
The inherited G-tenure shrink rule makes repeated colliding targets
monotone on either side. It does NOT make their loss events disjoint or
automatically available under g_1. Other cores use the general port rule.

This is complete forward coverage of every actual residual frame and
its required A-source incidences. It is not a smaller finite grammar
with a reverse realization theorem and does not assert adequate funding.
