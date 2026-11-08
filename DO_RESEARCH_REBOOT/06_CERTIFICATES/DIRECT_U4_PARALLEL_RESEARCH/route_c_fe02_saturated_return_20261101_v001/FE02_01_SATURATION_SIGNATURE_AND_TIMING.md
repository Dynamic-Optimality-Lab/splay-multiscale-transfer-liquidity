# FE02 exact arithmetic signature and original mixed-block timing

**PROVED—UNIVERSAL reductions**, with original finite ordered BST, present
key, cyclic closure and positive-block hypotheses unchanged. These are not
yet a proof that a saturated return is impossible.

## 1. Block arithmetic

Assume precisely one positive cyclic maximal A-root block i has a_i=1,q_i=3.
A nontrivial block begins with its root-arrival leader; every leader has
a_j>=1. Subsequent zero-A followers request the SAME present root key x_j:
a different present key has positive search depth and would begin the next
block. Thus the leader supplies the only A StepEvs in that block.

Before the block's first KEEP, if any, all operations are same-key DELETEs
and B is frozen. The first KEEP splays its root key in B; all later same-key
KEEPS are B-root no-ops. Therefore the block has at most one genuine B
change, all actual A/B events are counted once, and

    Q_B-2A=sum_j(q_j-2a_j)=1-sum_(j!=i)(2a_j-q_j).           (1)

The other summands 2a_j-q_j are nonnegative integers. If any is at least1,
(1) proves FE02-CD immediately. Consequently an actual counterexample in
this EXACT class must have

    delta_i=1, delta_j=0 for every j!=i,
    Q_B-2A=1.                                               (2)

Conversely an admissible reachable exactly closed source walk with (2)
would violate CD. Thus FE02-RIGIDITY and FE02-CD are equivalent on this
restricted class. Equation(1) does not establish rigidity.

## 2. Necessary original-source saturation conditions

For each nonpositive saturated block j:

- q_j=2a_j>=2. It must contain a genuine B-changing KEEP. A KEEP-less block
  has q=0 and delta=-2a<=-2, and a nongenuine B KEEP also has q=0.
- Its actual B search depth at its FIRST KEEP is4a_j or4a_j+1, since
  floor(d_B/2)=2a_j. The possible final zig is genuine and is not a double.
- Its actual A leader depth is2a_j-1 or2a_j. A cost a_j does not mean2a_j
  rotations when the leader has a final zig.
- The positive block's B depth is6 or7; its A leader depth is1 or2.
- A-root keys change between adjacent nontrivial blocks, including the cyclic
  seam. At a KEEP-containing block's end both roots equal its key.

These conditions include mixed DELETE/KEEP blocks, arbitrary fringes,
arbitrary a, both orientations and all source costs. They are jointly
NECESSARY, not a feasibility certificate. A=0 or a single cyclic constant-root
block cannot contain the assumed positive nontrivial leader on a closed walk.

## 3. Costed boundary normalization, with real timing preserved

Consider any COMPLETE block at key x, beginning at original pair (A,B).
Its leader may be KEEP or DELETE. At the leader A becomes S_x A and creates
its actual StepEv units. Every later A splay in the block is a root no-op.
If the leader is DELETE, B remains the original B through all initial
DELETE followers. Only at its first KEEP does B become S_x B and create
its actual double demands; every later B KEEP is a no-op.

Hence every KEEP-containing block has end pair (S_x A,S_x B), exactly the
leader's A event list and the first KEEP's B event list. Its endpoint/cost
projection equals a single ordinary KEEP x on the entering pair. The
component maps commute because they act on different trees. This proves
the projection WITHOUT treating them as simultaneous or moving B work into
a DELETE. In the original history A units belong to the physical leader
occurrence ell_j, and B demands to its actual first changing KEEP occurrence
kappa_j; these may be DIFFERENT request occurrences. Keep that provenance.

In a candidate saturated return every block is KEEP-containing by section2.
Collapsing each complete block therefore gives a recurrent all-KEEP macro
word with exactly the SAME paired boundary states, A/B costs, closure and
positive/saturated signatures. Conversely any such recurrent all-KEEP word
from a reachable source pair is itself an allowed original history. So the
existence question reduces exactly to recurrent KEEP macro words.

This statement is about COSTED BOUNDARIES, not identity of every intermediate
source state, masks, or old creator/setup eligibility edges. None of those
unneeded historical objects is silently transported. A direct physical
injection below always lifts units/demands back to ell_j/kappa_j.

The entering macro pair has common root x_(j-1), since the preceding cyclic
block ended in a KEEP. It need not have equal trees. The reachable startup
may contain DELETEs and remains unchanged. Assuming an ALL-KEEP startup
from a diagonal would force A=B forever and would falsely eliminate the
off-diagonal recurrent domain; no such assumption is made here.

## 4. A direct physical injection whenever slack is forced

Rotate the ORIGINAL physical word to start at the unique positive leader.
Pay its first two B doubles from its single A event's bits0,1. Its third
double remains outstanding. Each nonpositive block pays its own q_j doubles
from its first q_j units, in source event order.

If a source argument supplies j with q_j<=2a_j-1, choose the LAST actual
A unit of j, (cycle occurrence,ell_j,A-event a_j-1,bit1), and assign it to
the outstanding positive demand (cycle occurrence,kappa_i,B-event index
of its third double). Own units at j have indices below q_j<=2a_j-1;
the donor has index2a_j-1 and is disjoint. No other block lends. Every other
unit/demand carries its own physical occurrence identity. This is a complete
one-period injection with no startup, second-period, other-cut or repeated
credit. It need not obey FE's precommitted reservations.

Donor availability may be established at the original block entrance:
A leader depth determines a_j; before its first KEEP, B is still the
entrance B. Its present-key search depth determines q_j exactly. Alternatively
FE02_02's source return bound can prove q_j<=2a_j-1 before that demand is
evaluated. This uses actual source geometry permitted by the revised user
directive, never an invented cost or observed future-period demand.

Until source rigidity is proved, this construction is conditional on real
slack or a proved source criterion forcing it. It is not a proof that every
one-positive walk possesses a donor.
