# Forced debt and a universal core11 leaf-loss reduction

The main FZ-INCOMING return barrier remains OPEN. The following necessary
rules and restricted source theorems are proved without constructing Dstar.

## Box D1: elementary forced regions and path contradiction

Target: necessary consequences of a feasible Dstar in[0,2]. Conditions:
the frozen inequality on all actual packet edges. Inheritance: none
beyond real arithmetic and exact composability. Ambiguities: feasibility
is not assumed as a conclusion. Bridge: sum the inequalities on actual
edges, whose identical full boundary states telescope.

For w=-2, feasibility requires Dstar(t)-Dstar(s)>=2. Its maximum possible
value is2, so Dstar(s)=0,Dstar(t)=2. Thus F is forced0 and T forced2.
If z reaches f in F by a finite zero path, summation gives
0+Dstar(f)-Dstar(z)>=0. Nonnegativity forces Dstar(z)=0. This handles
arbitrarily long zero paths by a single finite-path argument, not a
bounded computation.

An incoming zero predecessor of Z belongs to Z. An incoming +1 source
has debt<=1. A negative edge entering Z would require a negative source
debt and is impossible under feasibility. An incoming weight>=2 imposes
no further source cap within[0,2]. These are NECESSARY, not a construction.

For a composable P:T->Z, feasibility gives

    w(P)+0-2>=0, hence w(P)>=2.

An actual return costing0 or1, an actual negative entry, or a genuine
T intersect Z state would refute all width-two potentials. Projected
state coincidence does not supply the needed telescope. The old
normalized source value1 at Omega/Sigma shows that formula must change;
it does not force a replacement to retain1 or imply a contradiction.

## Box D2: marked-leaf accounting on core11

Target: isolate which packet can lose the source marker along arbitrary
return chains. Conditions: actual closed core11 source, fixed six marks,
all-SS operations. Inheritance: MARKED_PARENT_PROJECTION.md and source fan
lemmas. Ambiguities: marked-leaf count alone is not a potential for the
desired law. Bridge: exact path-compression changes marked parents only
on the selected path.

Let L(B) count marked vertices with no marked descendant, equivalently
marked leaves of the actual marked core. In the marked-parent tree of
a genuine B splay to x, all q old proper marked ancestors become direct
children of x; all off-path marked vertices retain their parent. Let a
be the number of those q ancestors with NO off-path marked child in
the old marked-parent tree, and let b=1 if x was a marked leaf,0 otherwise.
Every ancestor was nonleaf before the access and is a leaf afterwards
exactly when counted by a. Only x can lose leaf status, precisely when
b=1. Thus the EXACT source identity is

    L(B_after)-L(B_before)=a-b.                    (L)

No unmarked separator is erased in the underlying execution; marked
parents are proof notation with an independently proved source bridge.
In particular every single splay loses at most one marked leaf.

For q3 there are only two off-path marks, so at least one of the three
ancestors has no off-path marked child: a>=1 and (L)>=0. For q4, only
one off-path mark remains: a>=3 and (L)>=2. For q5, all marks are on
the path, a=5,b=1, giving a gain4 from its Hamiltonian source leaf1.
The actual q1 successor loses at most one; its known fan gives exactly
four target leaves. These bounds hold for arbitrary fringe geometry.

Every source in F11 has at most two marked leaves. A q5 source has a
Hamiltonian path through all six marks and therefore one. A q4 source
has five marks on its target path and only one off that path. Any marked
leaf is the terminal path mark or that off-path mark, so there are at
most two. Every state in T11 has at least four leaves: the q4 output's
four path-mark leaves can only exchange one leaf for the single extra
marked block, never reduce their number; the q5/q1 target has exactly
four. This reuses the sealed negative-seed leaf-floor proof.

Consequences, all uniform:

1. F11 intersect T11 is empty (irrespective of A, BE and recent order).
2. No single splay, hence no direct zero or +1 singleton packet, sends
   T11 to F11, since it could lose at most one of at least four leaves.
   Paired targets have four leaves and cannot equal F11 either.
3. In a zero/+1 path, H2/Q4 zeros have nonnegative leaf change (indeed
   at least+2), H3/Q6 zeros have positive leaf change, and H2/Q3 +1
   packets have nonnegative leaf change. Only H1/Q1 or H1/Q2 singletons
   can LOWER the marker, by at most one each.

Now let P:T11->Z11 be an arbitrary actual zero/+1 path of total weight
c<=1. By the DEFINITION of Z choose any actual zero suffix from its
end to F11. Complete states agree, so concatenate it; no realization
bridge is presumed for observations. Fixed labeled core constancy
keeps the entire extended path in core11. Its leaf change is at most-2.
The number of +1 packets is exactly c; at most c leaf losses can come
from H1/Q1. All other losses must be H1/Q2 zero singletons. Therefore

    number of leaf-lowering H1/Q2 zero packets >= 2-c.       (R)

In particular a pure zero return requires at least two such losses;
a weight-one return requires at least one. This is a NEW UNIVERSAL
necessary source restriction for arbitrarily long actual return paths.
It is independent of all debt formulas and all tested tree populations.
It does NOT prove those leaf-lowering packets are impossible or paid.

The source first-entry lemma excludes H2/Q4, H3/Q6 and H2/Q3 immediately
before F11. Formula(R) locates the residual zero transfers even when
they occur much earlier in the chain. The unproved bridge is A-dependent:
show how actual one-event A visibility prevents, or charges for, the
required leaf losses after a cold negative-two target. B-only structure
cannot supply a full certificate, as B_ONLY_SOURCE_OBSTRUCTION.md proves.

## Box D3: restricted exact sources

For F_C=F intersect C11, no zero edge enters C11 at all, so its zero
closure equals itself and no negative packet enters it. No direct +1
edge comes from T11 by the leaf argument. A zero PREFIX from T11 to
an H1/Q1 predecessor of F_C remains unexcluded. Thus even this useful
last-entry result is not the whole arbitrary-length barrier.

## Current verdict of the return test

The bounded exact search found no candidate from the known T states,
within its explicitly restricted helper family. It proves no universal
absence. No actual negative entry into the full Z has been constructed,
and none has been excluded at general core9/10 or F11 outside C11.
No architecture-level countercertificate is claimed. No potential is
defined by these necessary conditions.
