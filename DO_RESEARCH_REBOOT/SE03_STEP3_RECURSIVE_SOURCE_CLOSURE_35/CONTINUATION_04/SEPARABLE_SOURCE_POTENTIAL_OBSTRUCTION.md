# SP35 — uniform obstruction to separable source-pair potentials

Status: MATHEMATICAL DERIVATION; independent audit not yet attached.
This theorem restricts a sufficient proof architecture. It does not refute
Joint Repayment, a physical matching, CD, or Dynamic Optimality.

## Frozen IAGS Box

Target: determine whether a repayment potential can separate into an
A-only state term and a B-only state term while covering every actual
two-genuine-access root-return packet. Conditions: finite ordered physical
key set K, |K|=r>=1024, every physical key is genuinely kept during the
containing closed period; fixed anchor g in K. A-only term may depend on
the full labeled A tree, K and M, without a width bound. B-only term may
depend on full BF, actual erased BE for a fixed erasure, and their actual
finite recent-key charts. No A-dependent owner coordinate is hidden in
the B-only term. Constants may depend on r and K.

Inheritance: ordinary bottom-up splay, all-original-op costs; exact
root-return zig identities with arbitrary rigid ordered hanging trees;
the independently inherited UNIFORM_A_REALIZATION_OVER_CLOSED_B theorem,
including its source transformation premise and actual BE/chart recurrence.
The source realization theorem supplies separately containing histories;
its added A-only costs are outside the tested packet and never counted
as donors forced to occur in another history.

Ambiguities excluded: this is NOT a negative actual A/B source cycle.
It does not address a genuinely joint potential, history/owner-dependent
state, or a rule whose inequalities are asserted only on larger source
blocks rather than on every root-return pair. No Bank25 impossibility
follows. The original universal JR35 target is unchanged.

Bridge: a source-valid collection of root-return pairs can have a closed
B-only state walk with negative total price, while each pair has its OWN
A realization returning to its own initial tree. Thus any A-only term
cancels separately, and a B-only term telescopes on the closed B walk.

## Statement

For every r>=1024 there are no real state functions F and G such that

  4 - Q(P) + [F(A_end)-F(A_start)] + [G(Z_end)-G(Z_start)] >= 0

for EVERY source-valid root-return packet P=(KEEP x, KEEP g), x!=g,
at the preceding declared original paired-closed r-key scope when A's
actual packet event count is H=2. Here Z is the specified B-only state.
The same conclusion holds if the left price is reduced by selecting
fewer than H actual event pairs. No bound on the values of F or G is used.

## 1. Exact A return, including every private subtree

If x<g, choose the actual A source tree

    g(x(L,R),C).

BST order partitions all other physical keys into the three indicated
ordered subtrees. The two ordinary zigs give, literally,

    g(x(L,R),C) -> x(L,g(R,C)) -> g(x(L,R),C).

Both accesses have depth1, hence actual a=1 and total H=2. All L,R,C
payloads return exactly, not merely their roots or marked projection.
For x>g use g(L,x(C,R)); its right and then left zig give the same exact
return. Every key of K is physically retained. Thus F cancels on each
such pair independently of F's formula. No future A depth is inferred.

## 2. A uniformly negative available B-only edge

Consider ANY B tree on r physical keys with root g. Height h obeys
r<=2^(h+1)-1. Since r>=1024, h>=10. Choose a deepest key x, with a fixed
key-order tie break; x!=g. Its first ordinary B splay has

    q_x=floor(depth_B(x)/2)>=5.

The genuine return KEEP g has q_g>=0. Therefore this B-only pair has
Q>=5 and original price 4-Q<=-1. This bound uses all physical keys, all
of which will be genuine in the constructed containing history. It does
not assume same-side doubles, maximal core, or q_g=1.

## 3. Finite actual B state graph; all keys remain genuine

Start from any common diagonal tree rooted at g and its actual empty or
warmed recent-key records. Consider all states Z reachable by concatenating
the literal pairs (KEEP x, KEEP g), x in K-{g}, in full BF and actual BE.
Include the finite full/erased recent-key records in Z. There are finitely
many such states; each transition is the specified original pair, never
physical deletion. The reachable directed graph has at least one sink
strongly connected component C. It is closed under EVERY pair choice.

At each vertex choose the deepest BF key as in section2. This map stays
in C and has a directed cycle L of strictly negative edge prices. All
states and edge choices are actual reachable B-only executions.

Choose a vertex z on L. Inside C build a finite closed walk V based at z
which includes every target choice x!=g: for each such x, take its available
pair edge, and return to z by strong connectivity. Every x access and its
following g are genuine in BF because their consecutive roots differ.
Thus V visits all r genuine KEEP keys. Its price w(V) is finite, without
any assumed sign. Choose a positive integer N such that

    N*w(L)+w(V)<0.

The B-only walk L^N V is actually closed in BF, BE and both charts and
has genuine support exactly K. It uses one finite original period. Its
edges are not borrowed from other cyclic copies. Reachability is by the
literal reaching prefix used to define the graph.

## 4. Source validity of each tested packet

For each edge of this fixed closed B walk, choose its A tree As from
section1. The following refinement of the inherited realization proof
preserves the SPECIFIED already reachable BE/chart state, rather than
claiming that its separate recurrence automatically selects that state.

Let u be the full-B target of the preceding root-return pair. Just before
its final KEEP g, the full B root is u!=g. Let Zprev be the actual BF/BE/
chart state at that operation, reachable by the literal reaching prefix
followed by a walk inside C. Rotate the fixed closed B word to start at
THIS KEEP g, followed by the chosen pair P and the rest Vrest back to
Zprev. Rotation at this original operation is legal even though it splits
one displayed pair outside the tested P.

Run the reaching prefix from a common diagonal. Its A endpoint is A0.
Perform DELETE Gamma(A0,As), leaving Zprev unchanged. Now execute the
period

    KEEP g; P; Vrest; DELETE Gamma(Av,As),

where Av is A's actual endpoint after the full displayed KEEP segment.
The first KEEP g is GENUINE in full B (old root u!=g), but costs zero in A
because As has root g. It ends the preparation's natural macro. Thus P
starts at exactly As and the specified Z state, and costs exactly H=2.
After Vrest the specified B-only state is Zprev again; the final A-only
Gamma returns A to As without changing BF, BE or either chart. Full A,
both B executions and charts close exactly on this one period. Genuine
support is K, and every actual preparation/reset event is retained OUTSIDE
P, including the reset in the cyclic macro ending at the next KEEP g.

This proves the required prescribed-state source embedding using the same
ordinary-splay transformation dependency. No new numerical Gamma replay
or minimum preparation cost is asserted. It avoids assuming the erased
execution's independently selected recurrent phase equals a desired one.

IMPORTANT: the A tree may differ between edges. The proof establishes
separate source-valid inequalities, not an artificial common A walk.

## 5. Contradiction

Assume the proposed separable law. On each source-valid edge in L^N V,
section1 makes the F difference zero. Summing the resulting real
inequalities gives

    0 <= sum_P (4-Q(P)+G(Z_next)-G(Z_old))
       = N*w(L)+w(V) < 0,

since Z closes exactly. Contradiction. This is uniform for every finite
r>=1024 and all real coefficients/functions in the stated class. QED,
using the explicitly pinned source-realization dependency.

## Exact consequence for the open root

A successful all-source small-packet certificate must retain genuine
A/B interaction, or use a different source-block/history architecture.
Neither a larger range nor arbitrary separate F and G functions repairs
this class. This is not evidence that a closed original A/B source has
negative total price: the edgewise A resets deliberately have different
representatives. JR35, reservation compatibility, UCF35 and Gate U remain
OPEN. Existing CD6 and the new all-A maximal-seven certificate are intact.
