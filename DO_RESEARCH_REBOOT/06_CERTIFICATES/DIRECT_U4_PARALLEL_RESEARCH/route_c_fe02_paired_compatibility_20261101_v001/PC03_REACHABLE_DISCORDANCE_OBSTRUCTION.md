# A reachable saturated transfer refutes the scalar discordance bridge

**REFUTED—EXACT:** the proposed law that ancestor-discordance D never
increases on any reachable saturated common KEEP transition. This does NOT
refute FE02-CD, Coarse-Double, a cycle-restricted invariant, or every possible
paired compatibility theorem.

## 1. Explicit candidate and its exact source decomposition

For each unordered key pair{u,v}, a BST has one of three ancestry relations:
u ancestor of v, v ancestor of u, or unrelated. Let D(A,B) count pairs on
which the two source trees disagree. This is a specified finite structural
state function, not a potential assigned by assuming any desired inequality.

After both trees splay x, all pairs involving x agree. If D_x counts the
source disagreements involving x, and T_x is the SIGNED change among all
other pairs, then exactly

    Delta D=T_x-D_x.                                       (9)

Also D_x>=|d_B(x)-d_A(x)|, since the symmetric difference of the two original
ancestor paths contributes disagreements involving x. The tempting bridge
was that saturation might bound T_x by D_x, with strictness at the positive.
The inherited W's nonnegative steps pass this test, but the universal law
is false on the following original reachable edge.

## 2. Fixed source counteredge, with arbitrary common fringe

Let x>4, and let F be ANY finite BST with keys strictly between4 and x,
empty allowed. Use

    A=1(.,x(2(.,3(.,4(.,F))),.)),
    B=1(.,2(.,3(.,4(.,x(F,.))))).

Both roots are1. On KEEP x the ORIGINAL source depths are d_A=1,d_B=4.
The actual cost is a=1,q=2,delta=0: a saturated block. The source identities
give exactly

    A'=x(1(.,2(.,3(.,4(.,F)))),.),
    B'=x(2(1,4(3,F)),.).

The A event is one right zig; B has two RR doubles, in the required
parent-first convention. Their full event identities are certified.

For the five core keys alone, D_before=3 and D_after=4. Originally the
three target inversions are x against2,3,4. Afterwards the four disagreeing
pairs are{1,2},{1,3},{1,4},{3,4}. Thus D_x=3 and T_x=4.

For EVERY key f in F, before the operation its core ancestors are ALL five
core keys in BOTH trees (in different path order). Afterwards its A core
ancestors are still all five, but its B core ancestors are only{x,2,4}.
Precisely the pairs{1,f} and{3,f} become disagreements. Internal F ancestry
is identical and unaffected. Hence, with m=|F|,

    D_before=3,
    D_after=4+2m,
    Delta D=1+2m.                                         (10)

This is a literal source/fringe polynomial, not a larger finite fit. Integer
realizations use core keys1,2,3,4,m+5 and fringe keys5,...,m+4, or any ordered
relabeling. At m=0 the actual physical source has just five keys, already
enough to refute monotonicity even if D counts only the eventual KEEP support.

## 3. Original diagonal reachability is explicitly supplied

It is not enough to display arbitrary BSTs. Begin at the diagonal pair(B,B).
The ORIGINAL A-only DELETE word

    D_x,D3,D_x,D1

produces exactly (A,B). Its actual grouped event costs are recorded, not
assumed to be one root zig each. The initially attempted root-child-only
connector was insufficient; it was not promoted to unreachability. PC00B
recorded the provenance refinement BEFORE the successful original-operation
connector audit, with the same pair and same five-core size.

For an actual closed diagnostic history, append to that startup KEEP x,
then the fixed common word

    K(1,2,3,4,x,4,3,2,1).

The complete pair returns to (B,B). Both original implementations verify
the five-key physical cycle; the opaque-F source identity proves the same
connector and return for every allowed F. This is a reachable saturated
edge on a legal closed source history. The rest of this diagnostic contains
negative blocks; it is NOT a single-positive saturated return and has no
Coarse-Double violation. It refutes only the proposed UNIVERSAL saturated-
edge transition law, not a law restricted by an independently proved global
saturated-cycle compatibility condition.

The connector search was bounded to the SAME five-key single-tree domain
(at most42 BST shapes), found the fixed target after38 discovered shapes,
and supplied the concrete DELETE word. No paired graph, larger core,
alternative target, horizon increase or coefficient fit was used.

## 4. Exact consequence for this architecture

An all-size uniform bound Delta D<=c*a on saturated transitions is impossible
for any finite constant c: a=1 while (10) is unbounded. Likewise no repair
Phi=D+R with a size-independent absolute bound |R|<=M can make Phi
nonincreasing on ALL reachable saturated transitions: its change is at least
1+2m-2M, positive for sufficiently large m.

These are immediate scoped corollaries of the same family, not new potential
campaigns. They do not exclude unbounded corrections, interval-sensitive
quantities, selective source witnesses or other state functionals. No such
replacement is silently introduced here. Matching-terminal stays frozen.

## 5. Precise unresolved paired bridge

PC02's far-side control and persistent separator witnesses are genuine.
Approaching/overlapping accesses can, however, transfer conflict to non-target
pairs on a zero-excess step, including arbitrarily many unaccessed fringe
keys. Counting all such disagreements as owed B doubles would be incorrect;
these structural changes create no extra demand or credit.

The remaining theorem must identify WHICH source transfers actually restore
the particular positive key's gap and prove their eventual closure requires
distinct physical capacity, or an incompatible source configuration. Neither
unqualified retreat-interval existence nor scalar D monotonicity supplies
that bridge. Its global proof remains open. FE02's objective is retained;
the present continuation does not force a completed verdict or replace it
with an equivalent unproved cut/existence premise.
