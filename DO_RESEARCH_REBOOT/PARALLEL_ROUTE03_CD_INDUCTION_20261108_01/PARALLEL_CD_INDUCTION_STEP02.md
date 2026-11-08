# Parallel Route 03 — Step 02: orbit restrictions and source detour repair

Date: 2026-11-08 (Asia/Karachi).

**OUTCOME B — NEW VALID INDUCTION MACHINERY; UNIVERSAL BRIDGE OPEN.**

The new source rule removes a guarded, nonidentity two-run detour through an
erased key. It saves exactly one actual A StepEv and changes the full-minus-
comparison B cost by exactly -1, 0, or 1. Thus each removal has a strictly
positive signed price, at least one. If all KEEP occurrences of one key are
covered, scalar CD on the smaller-support source proves CD on the original
source, with an explicit positive margin.

There are also two structural consequences. A total cover by the B guards
forces every fresh phase seed into the same periodic erased execution after
at most one word. More generally, equality of the retained ancestor cores
makes arbitrarily persistent hidden B disagreement cost-neutral. Finally,
any hypothetical counterexample can be reduced to one with no applicable
two-run detour. These conclusions have complete symbolic proofs below.

No theorem here forces an arbitrary source to have a covered key or proves
CD on every resulting irreducible source. Outcome A is therefore not claimed.

## A. Exact inheritance and proof status

This report continues
[PARALLEL_CD_INDUCTION_STEP01.md](PARALLEL_CD_INDUCTION_STEP01.md), whose
entry SHA256 is
`4b26f5071b193f3fafcf1d79d57629d4c173057d584a5afcea81ecab58f0b056`.
That file and its metadata manifest remain unchanged.

The following results are inherited, not re-established as new results:

| Result | Inherited conclusion and audit scope |
|---|---|
| Certified CD(6) | The final six-key theorem plus the CD(5) base covers at most six genuine KEEP keys, with arbitrary physical support, helpers and private ancestors. The inherited trust scope is computer-assisted symbolic proof and a distinct implementation operated by the same agent, not external or formal certification. Step 01 checked the 44 publication-file entries; no semantic audit is rerun here. |
| Lower-support recurrence | KEEP(z)-to-DELETE(z) preserves the entire original A trace. Repetition from an actually reached pair gives an eventual fully closed erased source. Its legal prefix from the permitted diagonal, not finiteness alone, supplies reachability. |
| Signed accounting | On one actual aligned interval, full slack equals erased slack minus the direct cost D_z and signed retained interference J_z. Preperiods are excluded and every normalized term uses the same period multiplier. |
| R03-T | Transport an ACTUAL erased recurrent orbit across a cyclic cut using its erased prefix map. Complete closure and normalized charge are preserved; the transported erased state need not equal the full state at that cut. |
| R03-S | Starting erasure at any reached full-source phase is legal. Each seed has its own reaching prefix and eventual orbit. No favorable seed is guaranteed. |
| R03-B | An explicit arbitrary-support family has different reached erased prices for different seeds. It has an elementary independent CD proof and supplies no new CD-domain coverage. |
| Common B skeleton and exact transport | Both actual B histories retain every original label of the fixed full core S, with its original rigid gap BSTs. Exact depths, primitive rotations, parity and labeled closure are retained. The cross-key term in the inherited queried-depth transport identity has no assumed sign. |
| Earlier reservation results | A-identity excursion deletion is conditional on an independently proved marginal bound. The five-key/nine-core protected repeat-gap allocation remains at that exact scope; its gE is not the frozen fE or g1. |

The relevant historical proofs used here are
[ERASURE_ALIGNMENT.md](../SE02_ERASURE01/ERASURE_ALIGNMENT.md),
[the common-core representation](../SE03_NONREJOIN01/SE03_UNIFORM_B_PAIR_PROJECTION.md),
[exact depth/parity transport](../SE03_NONREJOIN01/SE03_EXACT_NONREJOINING_SOURCE_IDENTITIES.md),
[the A-identity excursion lemma](../SE03_NONREJOIN01/SE03_EXCURSION_RESERVATION_LEMMA.md),
and [retained-gap reservation](../SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md).
The corrections and status qualifications recorded in Step 01 continue to
apply, including zero charge versus zero depth and complete depths versus
partial observations.

The elementary rotation formulas used below are the original ordinary-splay
formulas. Their use is not a new auxiliary tree operation or a new potential.
The new results are the resulting source-word deletion, its signed price,
the restricted orbit law and the obstruction reduction. Proofs are analytic
and author-checked; no new machine, external or proof-assistant audit is
claimed. No broad historical priority claim is made.

### A.1. Frozen source and notation

Fix r >= 6 and assume scalar CD(r). W is any finite original reachable
exactly A/full-B paired-closed source with r+1 distinct genuine KEEP keys.
Every physical key remains present. A splays on every KEEP and DELETE;
full B splays only on KEEP. DELETE never removes a key. The starting pair
is reached by an actual legal prefix from the permitted original diagonal.
The closed source itself may start at a nondiagonal pair.

Write F for full B, E for an actual erased B comparison, and

\[
a_t=\lceil d_A(x_t)/2\rceil,\qquad
q_t=\lfloor d_B(x_t)/2\rfloor\quad\text{on KEEP},
\qquad q_t=0\quad\text{on DELETE}.
\]

Set A=A(W), Q_F=Q_B(W), and Delta_F=2A-Q_F. Let M be the genuine KEEP
support. In this nonempty closed domain all KEEP targets belong to M by
the inherited root-provenance theorem. For z in M let R=M minus {z}.
It is nonempty. Costs and IDs always refer to actual source occurrences.

For an uncompressed erased comparison with unchanged A,

\[
\Delta_F=\Delta_E-(D_z+J_z).
\tag{1}
\]

Changing Q_E changes Delta_E and D_z+J_z by opposite amounts in (1).
There is no argument here from minimizing J_z alone. The new proof instead
constructs a DIFFERENT valid ordinary-splay comparison word with A cost
A-m, identifies its omitted original A events, and proves a local B price.

## B. A restriction on persistent disagreement

For a nonempty retained set R, let C_R(T) be its labeled ancestor core:
the root-to-R paths, with their actual left/right edges. Say two trees are
R-core-congruent when these rooted labeled core trees are identical.
Corresponding external gap BSTs may have different internal shapes. This
is an equality test on the existing source representation, not a new
potential or a replacement for full-state closure.

### Lemma R03.2-C — retained-core congruence is preserved by retained splays

Suppose F and E are BSTs on the same physical key set and are R-core-
congruent. For any y in R:

1. Their actual y pre-depths, and therefore their floor-depth charges,
   are identical.
2. After ordinary S_y in both trees, the trees are again R-core-congruent.
3. A sequence of retained splays has zero retained interference at EVERY
   occurrence, for arbitrary length. DELETEs do not affect this statement.

**Proof.** Every operand on either search path to y belongs to the common
core. The two paths have exactly the same labeled edges and length. The
ordinary bottom-up zig/double decomposition therefore uses the same core
operands, grouping and parity in both trees. Each off-core BST moves only
as an intact hanger. Induct on the original primitive rotations. The raw
tree on the old common core labels has the same output in both histories.
The new R-core, possibly a subset of those labels, is consequently identical
as a rooted labeled tree. No physical node is removed in either execution.
This proves 1 and 2. Induct over the actual retained requests for 3. QED.

This lemma does NOT assert complete tree equality. If an initial difference
is confined to the internal structure of a corresponding R-free hanger,
retained-only splays never enter that hanger. It can remain a different
opaque subtree through arbitrarily many requests while contributing zero
to J_z. The assertion is about actual histories; core equality by itself
does not manufacture diagonal reachability for a proposed pair.

Thus persistent disagreement with a nonzero retained price must involve
different retained ancestor cores somewhere in that region. Hidden raw
disagreement alone is insufficient. This gives a useful restriction on
the general persistent-disagreement problem, not a bound for the visible
cross-key transport term when the cores differ.

## C. The elementary ordinary-splay absorption calculation

Use u(L,R) for a BST node with its complete hanging terms. In every formula
below the four capital terms are arbitrary valid BSTs in their inorder
gaps. The named keys g,z,y are distinct. The reflected case in each row
reverses key order and child sides in the original rotation formulas.

### Lemma R03.2-A — three absorption frames

In any of these frames,

\[
\boxed{S_y(S_z(T))=S_y(T).}
\tag{2}
\]

The first access z is a child splay. A subsequent y access costs one
StepEv, and a direct y access from T also costs one StepEv.

| Type | Complete input T | Complete common output |
|---|---|---|
| S: straight grandchild, g < z < y | g(A,z(B,y(C,D))) | y(z(g(A,B),C),D) |
| M: mixed grandchild, g < y < z | g(A,z(y(B,C),D)) | y(g(A,B),z(C,D)) |
| O: opposite children, y < g < z | g(y(A,B),z(C,D)) | y(A,g(B,z(C,D))) |

The type names refer only to these source geometries, not to assigned costs.
They describe z a child of g, with y either a child of z or the other child
of g. The old root g is NOT the final target y.

**Proof of S.** The z zig gives z(g(A,B),y(C,D)); the y zig gives
y(z(g(A,B),C),D). Direct y is the original parent-first RR double and
has that same output. Reflection is the parent-first LL case.

**Proof of M.** The z zig gives z(g(A,y(B,C)),D). The ensuing y LR
double gives y(g(A,B),z(C,D)). Direct y uses the original RL double
and gives the same tree. Reflection exchanges these orientations.

**Proof of O.** The z zig gives z(g(y(A,B),C),D). Its y LL double
gives y(A,g(B,z(C,D))). Direct y is one left zig with that output.
Reflection exchanges left and right.

The relevant depths are recorded in the following table, so every ceil,
floor and zig is explicit. No double is replaced by one primitive rotation.
QED.

| B-frame type | d_T(z) | d_(S_z T)(y) | d_T(y) | q(z) + q(y after z) | q(y direct) | beta = difference |
|---|---:|---:|---:|---:|---:|---:|
| S | 1 | 1 | 2 | 0 | 1 | -1 |
| M | 1 | 2 | 2 | 1 | 1 | 0 |
| O | 1 | 2 | 1 | 1 | 0 | 1 |

For A, the two successive accesses cost 1+1=2 StepEvs in ALL cases,
whereas direct y costs one. For B, the actual double costs differ by beta.
In particular O produces positive retained interference with ZERO direct
erased doubles. The elementary A saving below pays that price without
asserting J_z is controlled by D_z.

## D. Source packets, phase restriction and explicit recurring-orbit selection

### D.1. Inspectable packet guard

A detour packet consists of two adjacent nonempty constant-target runs:

    a run of requests to z; then a run of requests to y, with y != z.

Each run contains at least one KEEP. Every other request in either run
may be KEEP or DELETE of that SAME target. All modes and all repetitions
are retained in the full source. No third target is admitted inside the
packet. Outside selected packets all original requests and helpers are
arbitrary.

The B guard is: at packet entry full B has one of the six oriented frames
of Lemma R03.2-A for the actual z and y. The first KEEP(z) therefore has
full depth one. The old B root and y differ.

The A guard is the same structural test in the ACTUAL A input tree. Its
old root need not be the old B root, and its frame type need not be the
B type. Only combinations that really occur in the actual ordered trees
are used. Neither tree is replaced by an arbitrarily spliced representative.

Because A accesses every request, exactly the first request of each run
has positive A cost: one StepEv. Later requests in its run are actual root
identities. A's two-run endpoint equals the endpoint of deleting the z-run
and ordinarily splaying the first y request from the original A input.

For B, earlier DELETEs in a run do not change its input tree. Its first
KEEP is the only B-changing request in that run; later KEEPs are identities.
Thus the B table in C applies to the literal first KEEP occurrences,
including when their simultaneous A costs are zero.

### Theorem R03.2-O — a total B cover removes phase-dependent recurring prices

Choose z and a disjoint CYCLIC packet cover of EVERY original KEEP(z),
with all B guards satisfied. The A guards are not needed for this theorem.
Let beta_i be the B-frame value for packet i.

There is a canonical one-word-periodic erased B execution with these
properties:

* Outside packets it equals the original FULL B tree exactly.
* Inside each packet it freezes across the erased z-run and takes the
  actual retained y splay at the first KEEP(y).
* Its charge per original period is

\[
\boxed{Q_E=Q_F-\sum_i\beta_i.}
\tag{3}
\]

Moreover EVERY fresh full-source phase seed permitted by R03-S enters this
same canonical execution, up to actual-orbit transport R03-T, after at most
one original period. Its erased period multiplier is one after that warmup.
Consequently all those phase seeds have the same normalized recurring price.

**Proof.** First cut at a packet boundary. Start E in the original full B
tree there. Outside packets both histories take the same retained splays
and DELETE identities. At a packet with input T, full B ends in
S_y S_z(T), while E ends in S_y(T). Formula (2) proves complete equality
at its exit. Induction over packets and intervening operations proves exact
outside equality. The original full B closure then proves one-word E
closure. The table in C computes the difference at each packet, and no
outside difference exists, proving (3).

Now activate erasure at an arbitrary actual phase of the full source.
If it lies outside packets, equality persists to the next packet and the
preceding argument applies. If it lies inside a packet before its first
KEEP(z), both B trees still have that packet's input T, so (2) gives equality
at the first following KEEP(y). If it lies after the first KEEP(z) but before
the first KEEP(y), both trees start at S_z(T); the remaining KEEPs of z
are full-root identities and their erasure freezes E. Both therefore execute
the same S_y from S_z(T). That output is the canonical S_y(T) by (2).
If the phase lies after the first KEEP(y), they already share the canonical
exit state. No unhandled B-changing operation occurs in these constant-target
runs.

Thus the first packet exit reached after activation, at most one word later,
puts E into the canonical execution. Subsequent packet entries/exits and
outside operations remain canonical. At the next occurrence of the displayed
phase the canonical state is reached, and each ensuing word returns that
complete B state. A is the original unchanged phase-rotated closed trace.
Reachability is the actual original reaching prefix followed by the actual
erased word; no preperiod credit is used. R03-T transports that canonical
orbit and its charge, rather than replacing its state by another full tree.
QED.

This theorem proves an actual restriction on phase selection. It does not
assert a total B cover for every key or every source. The phase-sensitive
family R03-B is outside this restriction for its erased p: its first p-to-x
transition from T has x at depth three, and its next p-to-g transition
from U has g beyond the opposite child. Those are not the three-node B
frames above. Altering the erased seed does not change these FULL source
geometries.

## E. Quantitative source repair from identifiable A events

### Theorem R03.2-D — guarded detour deletion and exact signed price

Let W be any original reachable paired-closed source. Select m disjoint
cyclic detour packets satisfying BOTH A and B guards. Their first targets
may be denoted z_i for this general deletion theorem. Cut at a packet
boundary so no selected packet is split.

Construct W_hat by deleting the ENTIRE first-target run of every selected
packet and retaining every other request with its original mode. Every
physical key remains present. Then W_hat is an original reachable
paired-closed ordinary-splay source and

\[
\begin{aligned}
A(W_{\rm hat})&=A(W)-m,\\
Q_B(W_{\rm hat})&=Q_B(W)-\sum_i\beta_i,\\
\boxed{\Delta(W)&=\Delta(W_{\rm hat})+
                   \sum_i(2-\beta_i).}
\end{aligned}
\tag{4}
\]

In particular each selected packet contributes 3, 2, or 1 to the slack
difference for B type S, M, or O respectively. These are source-derived
local prices, independent of the desired sign of either full-period slack.

**Proof of source legality and full endpoints.** Use the actual reaching
prefix to the chosen original boundary. At a selected packet, its original
A input obeys Lemma R03.2-A. Omitting its first run leaves the first y
request as an ordinary present-key access from that input, with complete
output S_y(T_A). Formula (2) equates this to the original complete output
of the two runs. Both histories then remain rooted at y throughout the
rest of that y-run. The full B argument is identical, applied at the first
KEEP(y). Its actual input is T_B because earlier DELETEs freeze B.

Consequently both complete trees at every packet exit equal the original
trees. Outside packets the entire subsequent input states, requests and
costs agree. Induction over the disjoint packets proves that W_hat returns
to the same original starting A/B pair. The original prefix reaches that
pair, so the shorter closed source is diagonally reachable. We have removed
requests in a proof comparison, not keys or rotations within a retained
ordinary splay.

**Proof of the A count and physical reserve.** The first actual request to
z_i in its run performs exactly one original A zig. The first actual y_i
request also has exactly one A StepEv. All other accesses in those two
runs have zero A cost. In W_hat, direct y_i still has exactly one StepEv,
possibly of a different zig/double type, with the same complete endpoint.
Thus precisely one A StepEv is saved per packet. No primitive rotation of
the direct shadow access is misidentified as an original rotation.

There is a specified injection of the shadow A unit inventory into the
original one: the two bits of the shadow first-y event map to the two bits
of the ORIGINAL first-y event, retaining occurrence, event ordinal 1 and
bit index; every other surviving event keeps its original ID. The image
excludes exactly both bits of each original first-z event. These m events
are distinct and have been identified solely by A geometry and source
occurrences, before invoking any CD inequality or computing any full slack.

The A cost is therefore A-m, with an independently identified excluded
pool of 2m original units. A shadow event's rotation type can differ;
the map is a proved map of StepEv counting units, not a false assertion
of identical rotation histories inside the packet.

**Proof of the B count and signed price.** The first full KEEP(z_i) has
pre-depth one and zero doubles. The full versus shadow charges at the first
KEEP(y_i) are precisely the two columns of the B table in C. Their difference
is beta_i. Later same-target KEEPs and every outside request have identical
charges. Summing gives the second equality in (4), with both signs kept.
Combining this independently calculated B difference with the established
A saving proves the final equality. QED.

This is a new nonidentity source reduction. A packet moves the old A root
to a different y and the old B root to a different y. No A-identity packet
or paired-closed subinterval was presumed. The inherited A-identity
excursion theorem and complete-state cycle excision therefore do not by
themselves supply this deletion. The elementary rotations are inherited;
the source comparison and its uniform signed price are the present result.

### Corollary R03.2-I — a genuine conditional support-induction step

Assume CD(r). Let W have r+1 genuine KEEP keys. Suppose some key z has
a disjoint cyclic cover of ALL its KEEP occurrences by packets satisfying
both guards. Let n_S, n_M, n_O count their B types and m their sum.

W_hat from R03.2-D has no KEEP(z); its KEEP targets are a subset of
M minus {z}. Its source legality and complete closure have just been
proved. Hence it has at most r genuine KEEP keys, and CD(r) applies.
Equation (4) gives the quantitative conclusion

\[
\boxed{\Delta(W)\ge 3n_S+2n_M+n_O\ge m>0.}
\tag{5}
\]

The existence of the cover is an explicit source restriction. It is not
defined by the sign of a slack, by existence of a desired matching or
by a favorable erased cost. The old root, child operands, modes and run
boundaries are all actual inspectable source data.

### E.1. The same proof in the original signed-erasure notation

Use the canonical z-erased execution of R03.2-O at a packet-boundary cut.
Its A trace is the ORIGINAL trace, so it has cost A, as required for (1).
All B changes outside packets agree. The literal per-packet erased marginal is

\[
D_{z,i}=0,\qquad J_{z,i}=\beta_i.
\tag{6}
\]

The shorter W_hat has exactly the same B execution as this uncompressed
erasure, because all removed commands would freeze erased B. It has the
smaller actual A cost A-m and the proved full A endpoint. Therefore CD(r)
on W_hat establishes the NON-CIRCULAR independent auxiliary budget

\[
Q_E\le2(A-m),\qquad \boxed{\Delta_E\ge2m.}
\tag{7}
\]

This is more than CD(r) on the uncompressed erased source: it excludes
the actual first-z events from the auxiliary A inventory. Together with
the independently computed local bound sum beta_i <= m, (1) yields (5).
The beta sum was not bounded by assuming Delta_F was nonnegative.

If the displayed original seam is inside a packet, apply the source proof
at an actual reached packet boundary and use actual-period transport.
For a fresh phase seed R03.2-O supplies at most one transient word and then
L=1. No transient event is a donor. On an aligned L-copy statement, the
reserve is 2Lm, D+J=L sum beta_i and all source-copy IDs are distinct before
any scalar division by L. No fixed historical fE cut is altered.

### E.2. Disjoint counting units and the frozen-owner limitation

An independent auxiliary allocation, obtained on the smaller source, uses
only shadow A units. Their injection into the original inventory excludes
the 2m actual first-z bits. At each retained occurrence pair common double
ordinals. A type O packet has one extra original y double and can use its
own first-z bit 0; these donor IDs are distinct across packets and lie
outside that independent auxiliary image. Type S has an auxiliary-only
y double; retiring its assignment releases a DIFFERENT unit in that image.
Type M has equal demand counts. Negative interference is retained, not
turned into a duplicated source unit. This also explains the exact gains
1, 3 and 2 in (4) respectively.

This is an independent scalar/source-inventory comparison. An original
first-z bit may already have an owner under archived g1 or fE. Nothing here
declares it raw-free under those maps, changes their values, or installs a
new effective allocation. Any stronger frozen-owner extension must use its
own accepted same-period exchange license. No new bank implementation or
Bank25 bound is inferred from this independent counting argument.

## F. Quantitative repair can coexist with hidden persistent disagreement

### Theorem R03.2-H — core-compatible orbit extension

Retain the hypotheses of Corollary R03.2-I. Instead of a fresh full seed,
suppose an ACTUALLY REACHED erased source starts at a packet-boundary A
state with B_E R-core-congruent to B_F. Its A tree is the same original
A tree at that phase. Do not presume complete F/E equality or one-period
raw E closure.

Then core congruence holds at every subsequent packet boundary and outside
packet transition. On every complete original word the exact marginal is
again (6) summed over packets. Erased recurrence plus compression proves
the same reserve and lower bound (5), even if raw F/E states never rejoin.

**Proof.** On retained-only intervals, Lemma R03.2-C gives core congruence
and zero per-occurrence interference. At a packet entry let the current
full tree be F and the erased tree E. The full packet output is
S_y S_z(F)=S_y(F), by the actual full B guard. The erased packet output
is S_y(E). Since y is retained, Lemma R03.2-C applied to F,E shows these
outputs are core-congruent. The pre-depth of retained y in E equals its
direct pre-depth in F, so the actual packet cost difference is still the
beta from C, regardless of different off-core hanger shapes. D remains
zero because full z has depth one.

Induction proves the claimed structural and per-word charge statements.
Run the compressed auxiliary word W_hat from this actual reached pair.
It has the same raw B map as uncompressed erasure: every removed command
freezes E. Its complete A tree returns word by word, with cost A-m, by
the A absorption proof. The finite raw B orbit has some actual preperiod
u and cycle multiplier L. The reaching prefix and repeated compressed
ordinary word are legal, so its recurrent L-word interval is a reachable
lower-support paired-closed source. CD(r) gives Q_E(I)<=2L(A-m).

Full A/full B and all packet frames are periodic on the original repeated
word. Each erased period has the same charge Q_F-sum beta_i because the
core congruence and exact local table hold throughout the warmup and
recurrence. Hence D_I+J_I=L sum beta_i. Combining these established bounds
gives Delta_F(I)>=L sum(2-beta_i); normalize every term by L. All excluded
source units on I have distinct original copy IDs. The preperiod is not
funding. QED.

This theorem does not claim every hypothetical core-congruent pair is
reachable with the required A tree. It assumes an actual reaching history.
It does not guarantee such a nonidentical seed for every W. Its use is to
avoid demanding full F/E rejoining where the existing common-core geometry
already proves zero interference. Persistent differences that change
retained ancestor cores and lie outside the packet calculation remain open.

## G. A smaller class of possible genuine support-erasure obstructions

### Theorem R03.2-N — detour normalization of a hypothetical counterexample

For any original reachable paired-closed W, R03.2-D can be applied to ONE
guarded packet, whether or not that packet covers all accesses of its first
target key. The resulting source W' satisfies

\[
|W'|<|W|,\qquad
|G(W')|\le |G(W)|,\qquad
\boxed{\Delta(W)=\Delta(W')+(2-\beta),\quad 2-\beta\ge1.}
\tag{8}
\]

Therefore a negative-slack source reduces, in finitely many such deletions,
to a negative-slack source with NO applicable guarded packet at ANY phase
or for ANY first target. All physical keys remain present. Under CD(r),
an initial r+1-support counterexample can never fall to support at most r;
its terminal source must still have exactly r+1 genuine KEEP keys.

**Proof.** The one-packet case of R03.2-D proves legality, full closure
and the exact price. At least one request is deleted. No new KEEP target
is introduced. Nonempty closed-source root provenance ensures that the
remaining KEEP target set bounds its genuine support, so it cannot exceed
the old genuine support. The zero-genuine case has Q=0 and cannot be a
negative leaf.

If Delta(W)<0, (8) gives Delta(W')=Delta(W)-(2-beta)<0. Choose an
applicable packet in the current actual comparison source, if one exists,
and repeat this mathematical reduction. Request count decreases at each
step, so it terminates. Each new source has its own valid reaching prefix
and ordinary-splay semantics by the same source proof. If its support ever
dropped to at most r, CD(r) would contradict its negative slack. This proves
the structural restriction on a hypothetical counterexample. No source
search or reduction program is executed here. QED.

The reduction can equivalently be used positively. If every guarded-packet-
irreducible original source with exactly r+1 genuine KEEP keys is proved
nonnegative, then CD(r) plus (8) proves CD(r+1) for ALL original sources:
normalize, use CD(r) if support drops or the irreducible theorem otherwise,
then restore the positive local prices. That irreducible-source theorem
has NOT been proved here.

### G.1. Nonduplication under repeated or newly adjacent deletions

Different deletions may become adjacent in a compressed comparison word.
They need not correspond to disjoint contiguous packets in the initial W.
This does not license spending an original event twice.

At each step the shadow A inventory injects into its parent's A inventory;
the only omitted positive event is that step's first-target event. Compose
these injections back to the original W. If an event is omitted at one
step, it is outside the image of every later shadow inventory. Thus the
images of the omitted two-bit pools at different steps are disjoint.
Every surviving occurrence retains its original ID and event ordinal;
the catcher has one StepEv on both sides of each individual rewrite,
even when its rotation type changes. The same statement follows by induction
on the exact inventory partitions.

For scalar composition the equality of slacks telescopes along the actual
parent/child source comparisons. This is not the false claim that queried
full/erased depth interference telescopes on its own. Every local change
has the independently proved source price (8).

Keep one fixed set of original-period occurrence IDs throughout this
composition. If a later packet crosses the displayed seam, prove its local
rewrite at a reached packet-boundary cut, then restore BOTH sides of the
inventory correspondence to that fixed original ID set by the actual-period
bijection. The shorter comparison has its own reached starting pair; it
need not start at a position deleted by the rewrite. No modular relabeling
creates a second copy of an original donor, and no previous/future-period
unit is added to the fixed inventory.

### G.2. The restricted class is nonempty at arbitrary support

For a symbolic illustration choose y < g < z and the complete B input
T=g(y(A,B),z(C,D)). Use Kz,Ky,Kg. The first two requests form an O
packet; deleting Kz leaves the actual child zig Ky. Both versions followed
by Kg restore T. A diagonal all-KEEP realization has the same A frame,
so the guard is nonempty.

Put a chain h_k < ... < h_1 < y of additional marked left children under
y. From root g, append the retained access word

    Ky, Kh_1, ..., Kh_k, Kh_(k-1), ..., Kh_1, Ky, Kg.

The descending-in-key child zigs followed by their exact inverse zigs
restore the whole input, including all arbitrary ordered gap hangers.
They never access z. For k>=4 the full source has k+3 genuine KEEP keys,
so this supplies examples at every support at least seven. This is a
symbolic free-term existence proof, not a new source replay or test.

These examples already have elementary safe proofs and old small-support
compositional coverage. They establish nonvacuity and a strict source
restriction, not new difficult CD-domain coverage. The useful result is
that the deletion rule also applies to such packets inside an otherwise
arbitrary original lower-support backbone; that backbone is paid by CD(r),
not by a false universal B-only change-count estimate.

## H. Exact remaining induction obstruction and rejected promotions

### H.1. What is now established

The source guards give a concrete phase-and-key selection rule:
choose a key z whose complete cyclic occurrence set has a disjoint guarded
two-run cover, and cut at a packet boundary. This rule is justified ONLY
when that actual cover exists. It proves, rather than assumes:

1. Ordinary-splay source reduction, complete endpoint closure and original
   diagonal reachability of the smaller comparison.
2. One independently excluded original A event per packet, hence 2m units.
3. Exact signed marginal sum beta_i, with each beta_i at most one.
4. Phase-seed synchronization under the B cover, and a core-compatible
   extension that does not require full-state rejoining.
5. The quantitative conditional implication (5) using scalar CD(r).
6. A terminating source reduction leaving no guarded packets in a minimal
   negative obstruction.

These are source-derived restrictions and inequalities, not optimization
of the invariant difference in (1). In particular (7) comes from an actual
cheaper ordinary A comparison, not an assertion that an unspecified
auxiliary allocation has leftover slack.

### H.2. What prevents Outcome A

No proof shows that every arbitrary r+1-support source has a covered key.
No proof shows that repeated detour deletions must remove an entire genuine
key. They may stop with r+1 keys and no guarded packet. Such a remaining
source can have deep erased targets, third-target helper interventions,
different retained ancestor cores and persistent signed cross-key transport.
The present three-node identities do not bound that transport.

Thus the now smaller missing bridge is a source theorem for those residual
sources: either a different quantitatively paid legal support reduction,
or a proof that EVERY detour-irreducible r+1-support source has nonnegative
slack. The latter is explicitly still a hard source theorem, not a result
obtained by renaming the original target. No finite bound on ambient A
support, word length or active helpers has been obtained for this class.

The following promotions are unsupported and are not made:

* A marked leaf, extremal key, smallest retained core or smallest marginal
  need not satisfy the frame/run guards. R03.2-O is not a favorable-key
  theorem for all sources.
* A root-return, a third-key intervening word or a deeper access cannot
  be substituted for (2) without a new ordinary-splay proof. Noncommutation
  under physical node removal and interval trimming remains in force.
* Positive A work alone does not imply the protected reserve. Here the
  reserve follows from actual source deletion and its unit injection;
  the general five-key repeat-gap certificate is not extrapolated.
* Equal roots do not imply core congruence or full equality. Core congruence
  controls costs but does not supply full source closure. In R03.2-H
  closure comes from actual raw recurrence and the legal prefix.
* The known unbounded zero-direct persistent interference is not paid by
  a universal fee per omitted KEEP. Our per-packet bound uses a specific
  full-source absorption identity that those general examples need not have.
* Independent excluded units are not automatically free under frozen g1,
  fE or old full assignments. No effective owner map is changed here.

No general candidate is falsely certified or declared refuted. The complete
detour-cover implication is proved at its explicit scope. The attempted
universal promotion is unsupported. These facts warrant Outcome B for the
new machinery, not Outcome A or a counterexample to Universal CD.

## I. Proof audit, isolation and resource record

The new local equality was checked analytically by expanding all three
right-oriented frames with arbitrary gap terms; reflection is the literal
left/right order isomorphism. The depth table independently retains both
floor and ceil conventions: a zig costs one A StepEv and zero B doubles.
In O, the positive retained double is at the first actual KEEP(y), whereas
the excluded A event is the first actual request to z, even if it is DELETE.
No event is fabricated at a starved KEEP.

Closure checks are of COMPLETE labeled trees. The direct deletion theorem
resynchronizes both trees at packet exits. The hidden-disagreement extension
uses actual raw B recurrence for its full endpoint, not a core endpoint
as a replacement. The phase theorem separates a fresh full seed from
transport of an existing erased state and counts at most one transient
word without using it as funding.

No source queries, splay replays, experiments, state searches, new potentials,
solver runs or research-program executions were performed. Known inherited
reports and the existing Step 01 artifact were read directly. File existence,
hashing and publication of this report are metadata operations. No agents
or concurrent routes were used for this derivation. No independent machine
or external audit is asserted.

All new writes are confined to this Route 03 location and new Step 02 files.
Step 01, all historical source evidence, R1-R4, original reaching prefixes,
physical key universes, frozen g1/fE/h0 assignments, old source periods and
their occurrence IDs remain unchanged. A comparison uses its own surviving
occurrence map; it does not overwrite the original execution. No C01-C09
campaign is restarted and no budget reset, cap increase or other route's
reserved resource is used. No new physical bank is implemented; Bank25 is
unchanged.

The last ledger inherited through Step 01 quotes global CPU
6392.953125/7200, symbolic 2451.21875/2640, independent
740.359375/750 and queries 3050330/3100000. These are historical ledger
values, not a new live aggregate across concurrent work. No semantic or
proof-computation process was launched in Step 02; no new resource
authorization is inferred. Metadata follows the inherited exclusion.

**Final status: Outcome B.** Guarded detour deletion has a proved uniform
signed price, a source-valid lower-support comparison and a terminating
obstruction reduction. The theorem that pays every remaining arbitrary
source is still missing. Universal induction, unrestricted CD and the
downstream conclusions remain OPEN.
