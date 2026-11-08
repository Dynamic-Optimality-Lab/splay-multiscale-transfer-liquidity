# Branch-retaining source representation for sigma=(1,1,0,...,0)

This is a source-complete SUPERRELATION, not an equivalence with physical
eleven-key trees. It includes every compatible private allocation. It
does not assert that every generated row lifts to an original transition.
In particular, weak LE hidden-population tests are not strengthened.

## 1. Size and order, without a chosen hidden split

Use the exact integer conservation in PC_ATOM_INVENTORY.Inventory.valid.
All z cells are nonnegative finite-domain integers. The DAG's add/sub
operators evaluate exact integers; their width annotations do not impose
modular arithmetic (PC_TYPED_DAG.ev_ground). For sigma0=sigma1=1 and all
other components zero, at most one present anonymous slot has gap0 and
at most one has gap1. Every other exposed-gap count is zero. Thus there
are at most two present anonymous slots. Present S-index uniqueness gives
at most nine present S slots: at most eleven present nodes in total.

For completeness this count does not assume hidden anonymous populations
occupy literal integer room. The actual LE compatibility constraints are
retained in the original graph and discarded only in the superrelation.

Erase kind0 refs127..255 to see the real prefix. Original parent/link/depth
constraints connect every present node to slot0; real child bounds give
strict ordered subintervals. Each active port is a frontier interval.
Its hidden S claims lie strictly below its upper bound and at least its
lower bound. Two distinct frontier intervals are separated by their first
distinct exposed ancestor, and an ancestor's own rank belongs to neither
child interval. Consequently an exposed anonymous rank cannot equal a
hidden S rank: if the port is below it, the left bound is strict above or
the right bound strict below its rank; otherwise the first separating
ancestor already strictly separates both ranks. Present-rank distinctness
handles exposed S. Fullrank S order therefore places every exposed
anonymous strictly in its indicated gap. Its ordered symbolic label is
f0=-8 or f1=8, with S_i=16*i. Each label appears at most once.

Every missing S key remains hidden in a frontier port. Its set depends on
the PRIVATE anonymous-gap choices. Do not make that choice a shared
coordinate, and do not fill that port in the shared observation. The
enumerator instead includes every ordered prefix on these eleven labels,
allowing a cut P at any off-path observation position. A cut can hide all
remaining S labels in its interval. Anonymous population bills are omitted
from the proof image. This omission can add rows; it cannot delete an
original row or create a new active original A operand.

Thus GAPMULTI01's two different hidden splits are both represented and
have the SAME source and destination potential keys. No deterministic
completion lemma is reused.

## 2. Raw alpha and dangling references

The shared normalization keeps the seven observed kind0 labels and
S-indices, forgets unused index fields, normalizes unused root kind, and
maps kind1/kind2 to P. Descendants of such a coarse child also become P.
Anonymous gap labels are PRIVATE and disappear from the shadow key.
These operations are a deterministic function of original alpha alone.
Different complete original states are not identified in the graph.

A dangling kind0 ref is G, not P. All original refs127..255 take the same
mux fallback to LITERAL slot0. Its label is the entry root S label; after
rotations this is not generally the current root. A depth1 G observation
also reads the CURRENT children of slot0. shadow(tree,owner) implements
that exact lookup, with owner fixed at the entry-root label. G is allowed
only in a real-prefix interval containing no S key, as exact S cover and
the absence of a real node or active port require. It need not have literal
room for a hidden anonymous unit; private bills were deliberately forgotten.

The AER01 real-path induction uses present targets, root termination and
no repetition, and applies with either signature: active operands are
real present nodes. Rotations move side (kind,ref) pairs intact. A G side
pair therefore moves as a leaf in the real tree while retaining its mux
alias observation. This is not erasing its shared alpha label.

## 3. Complete access profiles

Use the already established source H1 normal form: one core access at
A depth1 or2 with the SAME shared endpoints/H/actual terminal q. Use the
Gamma1 H2 normal form: two accesses of depth1 or2, first the unique changing
fringe helper, then the terminal core. A changing interior fringe cannot
end childless; only gaps0/9 can be that helper. Here only gap0 is occupied.
Gamma0 H2 requires no A enumeration: its ACTUAL preterminal debt bound
psi(destination)>=q-2 for q=3/4 is inherited. It permits changing unmarked
core KEEPs. There is no false H1 fusion of arbitrary H2 macros.

For each of the six H1 paths, or each of the 36 ordered H2 path pairs,
rotate a tree whose nodes are symbolic source addresses. Protect all real
active operands, all nodes read at depth<=2 at either endpoint, and the
two final children of the original slot0 (needed for depth1 G lookups).
Include every prefix ancestor of those addresses. All other blocks can
be replaced by P: their roots are neither observed nor active. Tree
rotation is substitution in the same fixed path context, so this pruning
commutes with the chosen word, including the slot0 observation. Required
path positions cannot be cut. First/terminal target labels have the
specified fringe/core types, and source root is core. Recursive ordered
root choice plus P/G alternatives enumerates every possible protected
assignment; labels skipped in an interval remain hidden in P blocks.

For the six H1 paths there are381618 assignments. The six nonempty H2
path-pair families have81298 assignments; all remaining pairs have zero
ordered assignments. Total462916, below the original1m source-case cap.
Maximum source observation depth among nonempty families is4; there is no
depth-cut conflict. The enumeration yields29397 normalized alpha classes
and430806 distinct (H,target,destination) options. These are complete
superrelation profiles for the required normal forms, not samples.

## 4. Direct signed-bound connection and scope

Let J on a synchronized (core B, normalized alpha) class use the constructed
sparse table, default -psi(B). Use -psi(B) also on unlisted alpha classes.
Thus J is defined even on Gamma0 or high-only states and satisfies
-2<=J<=-psi<=0 everywhere with a valid mathematical core B. It reads no
private variable. It is independent of the mask and fixed signature's
private allocation. On other signatures no claim is made by this file.

H1 and Gamma1 pull into the prefix rows with original q. Gamma0 uses the
inherited floor: for q<=2, w=4-q>=2 covers range; for q3/4,
J(t)-J(s)<=2-psi(t)<=4-q. Invalid/non-low-realizable high alpha can use
the same default range. Source B's other childless gap1 leaf does not
change core depths or the gap0-helper kernel; leaves never lie on an
active core path. The inherited low/high core projection applies in both
chi8 regions without reflecting or removing their sentinel semantics.

Subject to checking the resulting finite table, use the existing formula
W(O)=J(O)-5*chi8(O.b), W(M)=-5*chi8(M.b). Universal within-region high
toll2 and the entering high bound-3 discharge high legs; a high exit from
chi8 is impossible. In particular the corrected h=0, declared-depth18,
weight-3 entering edge is retained. This would give finite-walk bound-7
and closed mixed-walk nonnegativity for this fixed signature. Closure and
midpoint equality always refer to ALL original shared fields.

The present campaign performs construction and bounded source controls.
Independent certification of the complete new certificate is step3, still
to be requested/performed. Other two-gap positions, larger populations and
larger supports are step4 and remain OPEN. Full M3 remains OPEN.
