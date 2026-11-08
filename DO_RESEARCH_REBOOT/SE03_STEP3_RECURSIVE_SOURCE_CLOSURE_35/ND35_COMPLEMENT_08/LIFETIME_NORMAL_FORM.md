# Exact cyclic missing-cluster lifetimes

Status: new uniform symbolic derivation, review pending. This is an exact
annotation/reduction of an actual source, NOT an exhaustive grammar of
which annotated histories are source-realizable.

## Local changes retain identities

At each fine step put Z=J_S(B) minus J_S(A). The ND35 local proof gives:

- A step: |Z_old minus Z_new|<=1 and |Z_new minus Z_old|<=1.
- B step: one label I is removed; if neutral at rotation level, one
  different label J is added; otherwise nothing is added.

The nonempty labels are intervals in the sorted actual S: a BST subtree
occupies a key interval. No interval rank replaces its original key set
or actual source occurrence. All A rotation bits, including steps where
Z does not change, and all virtual zig units remain explicit resources.

At every fine boundary create one vertex for each ACTUALLY missing
label. Join a persistent label to its next boundary occurrence. When
one label is removed and another added in a single step, join those two
occurrences as a transfer. A pure A addition is a birth with its real
rotation-bit ID. A deletion without addition is a death, retaining its
actual A-negative/B-payment/B-release slot. There are no B births.
Use the actual common boundary to glue final to initial equal labels.

Every vertex has indegree/outdegree at most1, hence each finite connected
component is either a birth-to-death path OR a directed cycle. This
classification follows by following unique neighbors; no forest premise
is used. A cycle can wind around the original period more than once as
an abstract label trajectory: its vertices and resources are nevertheless
different actual occurrences on the ONE original period. No duplicate
copy or extra bit is introduced. Initial arbitrary names for strands
may be permuted at the seam.

## An alternative ND35 nonneutral matching

Every death lies at the end of a path with a unique A birth. A death
cannot lie on a directed cycle, and a birth path cannot enter a cycle:
that would create two incoming edges. Assign each nonneutral double's
first death its path's original birth bit. Distinct deaths have distinct
path births. This gives a source-defined injective g_life on ALL D+.
It may differ from g+ defined by scalar-level pairing; neither is silently
identified with the other. Each is a legal RAW provisional matching.

No cyclic history is supplied a nonexistent birth credit. The complete
analytical complement of g_life is exactly:

1. every actual A unit not used as an A-birth bit;
2. birth bits whose death is an A-negative, extra B2 or terminal B-zig
   release slot.

It has the SAME count2A-P+N+B2+Z1. Source assignment depends on whole
physical histories, not a fixed-depth chart or first-loss/return window.
This equivalence does not prove neutral endpoint existence.

## Neutral-double incidences

A neutral B double has TWO transfer incidences, one for each original
rotation. During any one B splay to x, a transferred strand gets a label
excluding x. Every subsequently removed B label in that splay contains
x. Therefore that strand cannot be transferred again DURING THAT same
access. The two incidences of one neutral double are distinct LIVE
strands at that access.

They need not belong to different GLOBAL components: cyclic seam
permutations can connect strands elsewhere. The reduction permits this
and retains both incidence ports. Discarding one port, assuming two
different global vertices, or assuming acyclic dependence is unjustified.

## Remaining mathematical implication

The lifetime construction accounts for every neutral demand and every
raw unit, uniformly in support, source length, private shape and helper
choice. It has not proved expansion, endpoint availability or a donor
license for all those incidences. In particular A steps which change
no missing label can create crucial physical capacity. A source-complete
neutral theorem must justify their relationships to unpaid components
as well as handle directed cycles and shared demand incidences.

This is a complete FORWARD annotation of actual histories. There is no
reverse realization claim, no smaller finite all-support state bound,
and no assertion that the displayed graph by itself preserves all
constraints of original source dynamics. Those distinctions prevent an
abstract cut or cycle from being misreported as a CD counterexample.
