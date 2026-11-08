# Step 2 — canonical source incidences and nested collision chains

Status: universal symbolic derivation at the exact original source scope.
The theorem decorates W and its frozen Step 1 map. It constructs NO
additional matching and never moves an established assignment.

## 1. Occurrences, cycles and the canonical A witness

Fix ANY subset F' of the residual original doubles F(W). Each d in F'
has two ports, its two original neutral B-rotation occurrences. A port
p removes one particular missing S interval I_p containing its access
target. The ports are distinct actual B rotations. During each B access
all removed labels are distinct original path labels, so a transferred
strand cannot transfer again within that access.

The accepted exact missing-label occurrence graph is a union of paths
AND directed cycles. This graph retains pure A births/deaths, transfers,
all unchanged steps, and the actual cyclic seam. The two ports of a
double are different live strands but may lie in the same GLOBAL cycle.
Nothing below assumes acyclicity, component births or bounded lookback.

For each port find the latest addition alpha(p) of THAT FIXED LABEL
I_p in cyclic order before its removal. This exists uniquely: removal
makes its indicator zero, so closure requires an earlier 0-to-1 change.
From alpha through just before p, I_p stays in the missing set. This is
a single label-run, not a whole transferred-strand component. The run
crosses the seam at most once; a multiwinding component has multiple
distinct such actual label-runs. No additional period copy supplies work.

Define the canonical witness beta(p):

* A-addition type: if alpha is an A rotation, set beta=alpha itself.
* Root-entry type: if alpha is a B rotation of target y, its created
  label excludes y. A's root is y, outside I_p. At p its actual root
  is the access target x in I_p. Choose the FIRST subsequent actual A
  rotation, before p in this cyclic interval, whose global root changes
  from u outside I_p to v inside I_p. Such a rotation exists, since only
  A rotations can change the A root. B does not change A.

The selected rotation has its original A-unit ID beta=(u_occ,j,b).
Naming it is a structural association, not an assignment of that bit
to a demand. Several ports may name the SAME physical bit.

## 2. No hidden duplication of one preparation occurrence

The map

    p -> ( beta(p), I_p )                            (TAG)

is injective on ALL selected ports, globally, across all accesses.

Proof: two A-addition tags at one rotation can use only its one added
missing label. For a fixed label-run, the first subsequent removal is
unique, hence so is its port. Two root-entry tags with the same beta,I
refer to the same active label-run through beta and the same unique
next removal. They are the same port. An A-addition tag has I absent
before beta; a root-entry tag has I active both before and after beta,
so these types cannot coincide at beta,I. This reasoning uses the
actual cyclic indicator, including runs wrapping the cut. QED.

In particular repeated preparations cannot be counted by tree shape or
key alone: actual beta IDs and label-run occurrences are essential.

## 3. Nested-chain collision theorem

Consider one actual A rotation beta. Let u,v be the FULL A roots before
and after it, and B_beta the actual full B tree frozen during this A
phase. Write n_F'(beta) for the number of selected ports naming beta.

If u=v, or if v is not in S, then

    n_F'(beta) <= 1.                                (NONROOT)

Indeed root-entry tags require a root change into a key belonging to
I subset S. Only A-addition tags remain, and a rotation adds at most
one missing label; TAG makes its port unique.

Otherwise u!=v and v in S. Define the existing-B-label chain

    K_beta={ K in J_S(B_beta): K!=S, v in K, u not in K }.

EVERY tag label at beta belongs to K_beta, and no label is repeated.
For root-entry type this is immediate from entry and persistence. For
A-addition type, the only A label that can be lost is the promoted
child's OLD subtree label. At a global-root rotation that child is v;
the label contains v (since v in S), excludes old root u, and is a
proper B label because it became missing. Thus it too lies in K_beta.

Every B subtree containing v is rooted at an ancestor of v. Such
subtrees form a strictly nested chain; TAG supplies distinct labels.
Consequently

    n_F'(beta) <= |K_beta|,                         (CHAIN)

and the shared incidences are nested ACTUAL B intervals, not arbitrary
sets. More explicitly, using actual B depths,

    |K_beta| = depth_B(v)-depth_B(LCA_B(u,v)),  if u in S;
    |K_beta| = depth_B(v),                    if u not in S.

For the second case u is not an element of ANY S label. The path to
v consists of S vertices by the carrier theorem; exclusion of the full
root label leaves exactly depth_B(v) labels. In the first case the
eligible roots are precisely the path vertices strictly below the LCA
through v. These formulas do not replace the actual A depth/cost.

Private A ancestors are fully admitted: they may change u, v and the
case of this formula. They are not silently compressed or charged as S.

## 4. Exact event-level interaction and storage-free accounting

In ordinary bottom-up splaying the global A root changes only during
the LAST StepEv of that original access. Before the last event all
rotation operands are strictly below the root. In a final same-side
double there can be two global-root changes; in a final opposite-side
double or zig there is one. Thus an event has at most two root-entry
chains, and all its other tag contributions have at most one port per
actual rotation.

All unbounded many-to-one canonical provenance loads are therefore
localized to root-changing rotations that promote an S key. Their
collisions have the CHAIN form. Internal A events have at most two
ports naming their two real rotations; a zig has only one rotation,
while its second actual accounting unit remains in C_A.

For any finite F', let B(F') be the DISTINCT physical A rotation IDs
that receive its tags, and group them by actual StepEv e=(t,j). Exactly

    2|F'| = sum_beta n_F'(beta)
           = sum_e sum_{beta in e} n_F'(beta).

NONROOT and CHAIN bound each summand by its actual source geometry.
An event is represented ONCE and has ONLY its two original bits. Its
many incident ports are separate structural claims, not extra capacity.
This is a nonduplicating work-incidence rule, NOT the inequality needed
for a matching. Chain lengths may grow with S.

The same physical event may supply an A-addition tag, one or two entry
chains, creator/loss evidence or a recovery description. All references
retain that SAME event ID; they cannot be added as independent work.
Different deficient accesses can share it only subject to the TAG and
CHAIN restrictions. Missing-label cycles and repeated keys do not
invalidate these rules or generate additional copies of an event.

## 5. What work is already raw-free, without assigning it

The Step 1 image consists ONLY of actual +1 A-rotation bits for Psi.
Therefore any provenance rotation with DeltaPsi<=0 has its bit outside
image(g_1). In particular an A-addition that also removes a missing
label is a zero-change transfer, and its original rotation bit is
raw-free. A pure +1 birth may already be assigned.

Every virtual second zig unit is also outside image(g_1). For a +1 bit,
its exact occupied/free status is determined by the existing lambda
slot and Step 1 selection; it is not guessed from a nearby surplus.
These are consequences of the frozen inventory, not a new donor rule.
They neither release an h0/fE owner nor assign even one residual claim.

A structural certificate may therefore retain one event node with its
two bit IDs, actual g_1 owner or raw-free flag, all attached tag labels,
their source runs and the applicable chain. This records competition
without double counting and without constructing Step 3's matching.

## 6. Exact returns, shared recoveries and maximal cores

For G<x<C<R with arbitrary ordered private terms A,B0,B1,D,E, the
inherited literal A pattern is

    U = G(A,C(x(B0,B1),R(D,E))).
    access R, RR: R(C(G(A,x(B0,B1)),D),E).
    access G, LL: U exactly.
    access x, RL: x(G(A,B0),C(B1,R(D,E))).

Every hanger is restored by the R,G pair. A future x can stay shallow.
Our provenance theorem uses only actual earlier label additions/entries;
it neither needs nor concludes a forced future depth, fresh recovery
or new spare. Shape return does not equate physical event occurrences.

The inherited shared-return families allow many claims to reference one
return event. They do not contradict CHAIN: CHAIN concerns the canonical
latest-addition/first-entry tag, NOT an arbitrary proposed return donor.
If a return also is that canonical tag, all its attached labels must
have the proved chain form. Existing successful earlier assignments
remain frozen, and no return-based allocation is constructed here.

At maximal core, the inherited marked-G loss witnesses give additional
source information: repeated B targets sharing a demotion are monotone
within one G tenure, and actual A loss rotations have pivot G. This is
compatible with overlapping preparation work and the general TAG rule;
it is not a second independently countable capacity inventory.

## 7. Precise structural interface and its boundary

For EVERY actual original W and ANY finite residual collection F', the
following objects are source-defined and the preceding proofs establish
their properties without any finite support bound:

1. Exact four-frame labels and necessary/sufficient A-LCA blocker tests.
2. The original path-label pairs selected by the unchanged Step 1 map.
3. Exact path/cycle lifetimes and unique fixed-label addition/removal runs.
4. A mandatory actual A-addition or first root-entry for every port.
5. An injective tag map into (physical rotation, actual B interval).
6. Singleton loads away from S-root promotions and nested chain loads
   at those promotions, with the explicit B-depth bounds above.
7. Original two-bit event nodes, frozen g_1 ownership and the retained
   nonpositive/virtual raw units, counted only once.

This is complete FORWARD coverage. No difficult residual form is excluded.
The original source stays attached, so none of these necessary constraints
is used to assert that an arbitrary abstract graph is source-realizable.
There is no smaller reverse-realizable state quotient claimed here.

For Step 3, sufficient simultaneous available capacity and preservation
of any stronger owner contract still require proof. The present structure
does not supply Hall expansion, a free augmentation endpoint, a bound
of two on top-event tag loads, or a Bank25 trace. No final matching is
constructed. Those are funding obligations, not omitted local forms in
the Step 2 structural theorem.
