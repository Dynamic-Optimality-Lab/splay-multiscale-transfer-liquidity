# Parallel Route 03 — Step 03: global reduction and its exact obstruction

Date: 2026-11-08 (Asia/Karachi).

**OUTCOME C — STRUCTURAL ONLY AT THE UNIVERSAL INDUCTION GATE.**

Partial Step 02 removal is admissible. Consequently a hypothetical shortest
negative source has no eligible packet. The missing converse has NOT been
proved: negativity and complete paired closure have not been shown to force
a packet, and the packet-free class has not been proved nonnegative.

This continuation establishes three precise limits and compatibility facts:

1. Every KEEP of full-B depth at least three, with its complete source input,
   survives every Step 02 rewrite unchanged. Its target cannot be eliminated
   by that rewrite system.
2. The rewrite preserves both extra A work above one event per genuine KEEP
   and the demand above two B doubles per genuine KEEP. It removes only
   shallow positive surplus. Its positive price does not itself pay the
   permanent deep demands.
3. For one fixed erased key, whole-period compatibility is equivalent to an
   explicit test on its maximal target runs. If every such local test passes,
   the selected packets are automatically disjoint. No global overlap
   hypothesis needs to be invented for that fixed-key construction.

The maximal-core source theorem gives an exact obstruction to automatic
guarded support closure: on a core of size 2s-1 with s genuine keys, no
Step 02 packet exists at any phase or for any key. Existing original source
families realize that case at every support size. They have positive total
slack, so they refute unqualified packet-availability/support-closure claims,
NOT the stronger conjecture about negative sources and NOT Universal CD.

There is no new sign theorem for the remaining large-support sources. The
verdict is therefore not upgraded to Outcome B merely for these structural
and inventory facts. Scoped candidate refutations are recorded separately.

## A. Exact inheritance, guards and audit scope

The complete
[Step 02 report](PARALLEL_CD_INDUCTION_STEP02.md) was read, followed by the
complete [Step 01 report](PARALLEL_CD_INDUCTION_STEP01.md) and the exact
dependencies listed below. Neither report is modified. Entry hashes are:

* Step 01: `4b26f5071b193f3fafcf1d79d57629d4c173057d584a5afcea81ecab58f0b056`.
* Step 02: `49024ecaf32e016dfe2c9cb6e86b62937af1344a7cd292f8f90e5baae9997553`.

The accepted CD6 theorem and CD5 base are inherited at support at most six,
with arbitrary physical populations, A ancestors, helpers, DELETE targets,
lengths and exact labeled paired closure. CD6 has its historical computer-
assisted symbolic certificate; it is not externally or formally certified.
Step 01's 44 publication hash checks are metadata, not new semantic audits.
The R03-T/R03-S/R03-B and Step 02 proofs have analytic, author-checked status;
they have no additional independent machine, external or formal audit.
This continuation does not promote those audit qualifications.

The read dependencies include:

* [CD5 original-domain proof](../CD5_BASE01/CD5_PROOF.md),
  [CD6 theorem](../SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_THEOREM.md), and its final certificate.
* [Exact erasure alignment](../SE02_ERASURE01/ERASURE_ALIGNMENT.md),
  [common labeled B skeleton](../SE03_NONREJOIN01/SE03_UNIFORM_B_PAIR_PROJECTION.md),
  [exact depth/parity transport](../SE03_NONREJOIN01/SE03_EXACT_NONREJOINING_SOURCE_IDENTITIES.md),
  and `SE03_SOURCE_CONVENTION_CORRECTION.md`.
* [A-identity excursion reservation](../SE03_NONREJOIN01/SE03_EXCURSION_RESERVATION_LEMMA.md),
  [retained-gap reservation](../SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md),
  and [restricted B-return pulses](../SE03_STEP2_REPAY02/B_RETURN_PULSE_EXTENSION.md).
* [Core deficiency and leaf selection](../SE03_NONREJOIN01/SE03_CORE_DEFICIENCY_AND_LEAF_SELECTION.md),
  [subtree density](../SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md), and
  [closed maximal-core same-side theorem](../SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md).
* [Gamma support-uniform source proof](../SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md),
  [modified Gamma paired source](../SE03_STEP2_REPAY01/PAIRED_RANGE_TWO_TARGET.md),
  and [complete-state cycle reduction](../SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_02/SIMPLE_CYCLE_SOURCE_REDUCTION.md).

### A.1. Original source scope

A executes ordinary present-key bottom-up splays on every request. Full B
executes them on KEEP only. DELETE is A-only and removes no key. A source
starts at a pair reached by a legal prefix from a permitted common-tree
diagonal, and its COMPLETE labeled A and full-B trees each return to their
own starting tree. The prefix need not have the reduced source's KEEP
support; it is never a funding pool for the closed period.

Costs remain

\[
a_t=\lceil d_A(x_t)/2\rceil,\quad
q_t=\lfloor d_F(x_t)/2\rfloor\text{ on KEEP},\quad
q_t=0\text{ on DELETE},\qquad \Delta=2A-Q_F.
\]

A genuine depth-one B zig has q=0 but changes the tree. A root KEEP has
q=0 and does not change it. They cannot be substituted for each other.
An erased request has zero B charge by mode, not necessarily zero pre-depth.

Fix r>=6, assume CD(r), and put s=r+1. A putative negative source has
exactly s genuine keys: smaller support is ruled out by CD(r). The finite
physical key set K is arbitrary and remains fixed in every comparison.

### A.2. Literal Step 02 packet theorem

The following is extracted from R03.2-A/D/I/N, not reproved here.

A packet has two adjacent nonempty constant-target runs, first z then y,
with z!=y and at least one KEEP in EACH run. Each other request inside the
runs may only be KEEP or DELETE of that run's same target. No third-target
helper is permitted inside. Outside selected packets helpers are arbitrary.

In EACH actual input tree A and F, z must be a child of that tree's old
root g, and y must be either a child of z or g's other child. The keys
g,z,y are distinct. The A and B roots and orientations need not agree;
both actual trees must individually satisfy an admitted frame. The six
oriented frames are these three and their exact order reflections:

| B type | Input full tree | Common endpoint S_y S_z(T)=S_y(T) | beta |
|---|---|---|---:|
| S | g(U,z(V,y(X,Y))) | y(z(g(U,V),X),Y) | -1 |
| M | g(U,z(y(V,X),Y)) | y(g(U,V),z(X,Y)) | 0 |
| O | g(y(U,V),z(X,Y)) | y(U,g(V,z(X,Y))) | 1 |

All capital terms are arbitrary valid ordered BSTs. Beta is the full
two-run B-double cost minus the direct retained-y cost. First KEEP(z)
has depth one; the first KEEP(y) has depth one or two after that z splay;
direct y has depth one or two. Both first A accesses cost one StepEv;
direct A-y costs one. Every zig and both floor/ceil conventions are retained.

For m DISJOINT cyclic eligible packets, remove their complete first runs
in a proof comparison, keeping every other request and mode. At a reached
packet-boundary cut the resulting W_hat is a valid original source and

\[
A(\widehat W)=A(W)-m,\quad
Q_F(\widehat W)=Q_F(W)-\sum_i\beta_i,\quad
\boxed{\Delta(W)=\Delta(\widehat W)+\sum_i(2-\beta_i)
                    \ge\Delta(\widehat W)+m.}
\tag{1}
\]

Each price 2-beta is respectively 3,2,1. The complete A and full-B
endpoints agree with the original at every selected packet exit. Arbitrary
outside operations therefore retain their actual inputs and costs. The
shadow A unit map excludes the two original first-z bits per packet and
maps the shadow y event to the actual first-y event. It is an independent
comparison, not a declaration of freedom under frozen g1 or fE.

Full key coverage is needed ONLY to conclude smaller genuine KEEP support.
If every KEEP(z) is in the removed runs, |G(W_hat)|<=r and CD(r) gives
Delta(W)>=3n_S+2n_M+n_O. Partial removal still has (1), source legality,
complete closure and strict request-count decrease.

### A.3. Phase, compatibility and irreducibility

R03-T transports an existing ACTUAL erased orbit and its actual erased
state. R03-S permits a new legal phase seed from an actually reached full
pair. Those operations have different meanings; R03-B proves different
seed prices can occur. Neither changes the original full A/F pre-states.

With a total B-guarded cover, R03.2-O proves canonical erased recurrence
after at most one period for fresh phase seeds. R03.2-H additionally covers
actual reached, retained-core-congruent seeds under its complete packet
hypotheses. It does not infer raw closure from core equality.

A current comparison source is Step-02-irreducible when no eligible
packet exists at ANY cyclic phase or for ANY first target key. This is
not merely failure to cover an entire key. R03.2-N strictly reduces request
count until this condition holds. Newly adjacent packets are checked in
the current actual source, not assumed valid from old inputs. Disjoint
source-bit injections compose; a unit removed at one step is outside every
later shadow inventory. Both endpoints are transported to one fixed original
occurrence set across any proof cut. No prefix or extra copy funds it.

## B. Partial removal and the correct minimality consequence

**Partial-removal verdict: ADMISSIBLE, not merely conditional on full key
coverage.** This is already the literal scope of R03.2-D/N. Its five
required interfaces are:

| Interface | Exact inherited reason |
|---|---|
| Original operation semantics | Only requests in the first run are omitted in a comparison word. Every surviving request is an ordinary splay with its actual new input. All physical keys stay present. |
| Reachability | Use the original legal reaching prefix to the chosen packet-boundary pair. No auxiliary abstract state is invented. |
| Complete closure | S_y S_z=S_y in EACH actual A/F input; both complete trees resynchronize at packet exit and all later outside inputs agree. |
| Strict well-founded decrease | A nonempty first run is deleted, so the number of closed-word requests decreases. A cost also decreases by one per packet. |
| Signed price | Equation (1) holds for the actual whole-source counts; no favorable erasure sign is assumed. |

If only one occurrence-run of z is removed, other KEEP(z) occurrences may
remain. It is then invalid to invoke CD(r) merely because one packet was
deleted. This is the precise distinction between length reduction and
support reduction.

### B.1. Fixing a genuine minimal negative source

Suppose a counterexample exists on some finite physical K. Among ALL
reachable paired-closed negative sources on that same K with support at
most s, choose one of minimum closed-word request count. The nonempty
set of such counts is a subset of the positive integers, so this choice
exists. The reachability prefix is not part of the minimized source count;
it is not part of the cost to be funded either.

By CD(r), this minimum W has exactly s keys. If it contained one eligible
packet, partial removal would give another source on K in the same
admissible class, with support at most s and

\[
\Delta(\widehat W)=\Delta(W)-(2-\beta)<0,
\qquad |\widehat W|<|W|.
\]

That contradicts the defined minimum. Thus

\[
\boxed{\text{minimum negative W}\ \Longrightarrow\
       \text{no eligible Step 02 packet at any phase or key}.}
\tag{2}
\]

This conclusion EXPLOITS partial admissibility; it does not force existence
of a packet. Proving that such a minimum must also contain a packet would
complete the contradiction, but requires a new source theorem.

The inherited complete-state cycle reduction is another restriction: a
shortest negative source cannot split at repeated complete A/F states into
two nonempty shorter closed children, since at least one child would be
negative. This observation is not a new proof of the sign of a state-simple
leaf. Equal roots, cores or selected depths are not complete-state repeats.

## C. A rewrite invariant preventing automatic support elimination

### Theorem R03.3-P — deep KEEP occurrences are permanent under Step 02

Let T_3(W) be the set of actual KEEP occurrence IDs having full-B pre-depth
at least three. Under any Step 02 rewrite, and under any finite sequence
of them, T_3 is preserved bijectively. Each such occurrence retains its
target, complete A/F pre-state, pre-depth and original q value.

Define the protected-key set

\[
P_3(W)=\{x:\text{some KEEP(x) in W has }d_F(x)\ge3\}.
\]

Then P_3 is invariant and every resulting comparison W' satisfies

\[
\boxed{|G(W')|\ge |P_3(W)|.}
\tag{3}
\]

No key in P_3 can be eliminated by any sequence of these guarded deletions.

**Proof.** Inside a valid packet, every KEEP in the first run has full
pre-depth one at its first occurrence, then zero. Every KEEP in the second
run has full pre-depth one or two at its first occurrence, then zero.
No original KEEP of depth at least three lies inside the packet.

After deletion, the first retained y KEEP has depth one or two from the
direct frame, and subsequent same-target KEEPs have depth zero. Thus no
new depth-at-least-three KEEP is created inside the replacement. Every
outside input is the same COMPLETE A/F state by R03.2-D. All original
depth-at-least-three occurrences therefore survive unchanged, and all such
occurrences in the new word come from those old ones. This proves the
one-step bijection and pre-state statement. Compose it over the finite
rewrite sequence, including its actual occurrence maps at any cyclic cut.

Each preserved occurrence is nonroot and hence genuine. Its target remains
in the new genuine support, proving (3). QED.

The threshold is exact for this invariant. In type O the retained y KEEP
has old pre-depth two and new pre-depth one. Depth-two pre-states cannot
be declared invariant. Conversely depth three has q=1 and is already
protected: depth and double cost must not be conflated.

**Consequences for key and phase selection.** A key with one such occurrence
cannot have all its KEEP requests removed. Moving a seam only reorders
the same full-source occurrences; reseeding erased B changes E, not their
full pre-states. Repeating the word creates new copy IDs for the same
protected events and does not make any original copy deletable. If all s
keys belong to P_3, no Step 02 reduction sequence can reduce genuine support
at all, even if other shallow packets are available and deleted.

This is an obstruction to THIS rewrite system. It does not rule out a
different source-valid reduction acting on those deep requests.

### C.1. Exact quantitative invariants

Let C(W) count genuine KEEP OCCURRENCES, including genuine depth-one changes
with q=0. It is not the number of distinct keys. Cyclic natural intervals
between successive genuine KEEPs have different endpoint roots in A and
therefore at least one A StepEv each. Hence A>=C at the unrestricted original
source scope, with all helper work retained.

Define whole-period inventories

\[
E_{\rm src}=A-C\ge0,\quad
S_{\rm sh}=\sum_{\text{genuine }t}(2-q_t)_+,\quad
D_{\rm deep}=\sum_{\text{genuine }t}(q_t-2)_+.
\tag{4}
\]

These are source counts, not a new potential or proposed state certificate.
D_deep is NOT the historical erasure term D_z. Protected depth-at-least-three
requests and positive D_deep demands are also different sets: the latter
requires q>=3, thus depth at least six.

Per-occurrence positive/negative-part accounting gives

\[
\Delta=2E_{\rm src}+S_{\rm sh}-D_{\rm deep}.
\tag{5}
\]

Equation (5) by itself proves no new global sign. The following rewrite
invariance, rather than merely this identity, is the relevant new fact.

### Theorem R03.3-Q — the rewrite removes only shallow surplus

For m selected packets,

\[
\begin{aligned}
C(\widehat W)&=C(W)-m,\\
E_{\rm src}(\widehat W)&=E_{\rm src}(W),\\
D_{\rm deep}(\widehat W)&=D_{\rm deep}(W),\\
S_{\rm sh}(\widehat W)&=S_{\rm sh}(W)-\sum_i(2-\beta_i).
\end{aligned}
\tag{6}
\]

These identities compose for sequential reductions, including newly
adjacent packets checked in the current word.

**Proof.** A packet has precisely two genuine KEEPs: the first z KEEP
and the first y KEEP. All later same-target KEEPs are root identities.
Its replacement has precisely one genuine y KEEP, at direct depth one or
two. Outside genuine statuses are unchanged. Thus C decreases by one,
just as A does, and E_src is unchanged.

Every old or replacement packet q is zero or one. No packet contributes
to D_deep; all outside q values are identical. D_deep is consequently
unchanged. The shallow contributions before/after are respectively
4/1 for S, 3/1 for M and 3/2 for O. Their decreases are 3,2,1,
which equal 2-beta. Disjointness and then composition prove (6). QED.

For a hypothetical negative source,

\[
D_{\rm deep}>2E_{\rm src}+S_{\rm sh}.
\tag{7}
\]

At least one genuine q>=3 request is therefore present. Its full pre-depth
is at least six and it is permanent by R03.3-P. Step 02 leaves the extra
A-work inventory and these deep demands unchanged while reducing shallow
surplus. It makes a negative candidate more negative; it does not itself
provide a new comparison paying or eliminating the deep demands.

The concrete sign conclusion available without any new geometry is only
the elementary safe branch D_deep=0, namely every genuine q<=2. Then
Delta>=0 by (5). More generally D_deep<=2E_src is sufficient. Neither
inequality has been derived for every irreducible source. Presenting
D_deep<=2E_src+S_sh as a new lemma would merely restate Delta>=0.

## D. A family-wide obstruction at maximal marked core

### Theorem R03.3-M — maximal-core sources have no Step 02 packet

Let an admissible full B-closed source have s>=2 genuine keys and fixed
marked core of size 2s-1. Then it has no eligible Step 02 packet, for any
key or legal phase, regardless of the actual A tree, helpers, repetitions
or erased orbit seed.

**Proof.** The inherited closed maximal-core theorem states that every
genuine full KEEP has EVEN positive pre-depth. Its stronger version also
restricts every double to LL/RR with the marked/unmarked operand roles,
but parity alone suffices here. A Step 02 packet would begin with a genuine
full KEEP(z) of depth ONE. That contradicts the source theorem. Nongenuine
root KEEPs have depth zero and cannot satisfy that guard either. A cyclic
cut and an erased reseed do not change these original full-source depths.
QED.

Equivalently, an eligible packet requires positive marked-core deficiency:
its depth-one genuine KEEP forces c<=2s-2 by the inherited deficiency
theorem. The Step 02 rule is inoperative throughout the entire deficiency-
zero source domain, not just on a special choice of an erased key.

### D.1. Original-source witnesses already in the inherited record

No new source instance is run or searched. Use the existing arbitrary-fringe
right-vine family in UNIFORM_RANGE_OBSTRUCTION.md, with n=2s-1 and odd KEEP
labels. Its word

    W_s = K3 K5 ... Kn K(n-2) ... K3 K1

returns the complete labeled right vine. Every KEEP is genuine of depth
two. With the original diagonal all-KEEP A realization it is exactly
paired-closed and

\[
|G|=s,\quad c=2s-1,\quad
A=Q_F=C=2s-2,\quad \Delta=2s-2>0.
\tag{8}
\]

This is a real original source for every s>=3, hence for every required
s=r+1>=7. It is already a terminal Step 02 source, retains ALL s keys,
and stays so under every legal phase, key choice and repeated period.

Consequently these UNQUALIFIED candidates are REFUTED:

* Every admissible s-support closed source contains a guarded packet.
* Termination of Step 02 normalization must eliminate a genuine key.
* A different reached phase or erased orbit can always enable the full-
  source guards on a previously packet-free source.

They are refuted at their all-source scopes by (8). Since Delta is positive,
this does NOT refute the negative-source-only candidate in I1.

### D.2. The unhandled domain contains the original deep-price controls

The inherited H_s word in the same report is also maximal-core closed.
Its first maximum access has depth 2s-2, its ascending intermediate marked
accesses have depth four, and its other accesses have depth two. For s>=3,
all odd marked labels except 1 therefore belong to P_3. The rule cannot
eliminate any of those s-1 protected keys. The maximal-core theorem blocks
even the first rewrite on the remaining key.

The old Gamma_s and modified Gamma_s have this same full B word structure
with original A-only preparations and repairs. They satisfy respectively

\[
(A,Q_F,\Delta)=(6s-2,6s-6,6s+2),\qquad
(6s,6s-6,6s+6).
\]

These are inherited positive full-source formulas, not new CD coverage.
Their full core is maximal, so Step 02 has no packet anywhere.

In modified Gamma_s the actual critical maximum KEEP and its actual
return KEEP have H=2 and Q=s. Their original segment price is

\[
2H-Q=4-s,
\tag{9}
\]

which is negative and unbounded below as support grows. This refutes a
proposed LOCAL rule assigning nonnegative cost to every guard failure or
to every uncovered root-return pair. It does not refute a sign theorem
for the WHOLE closed packet-free source: Gamma_s has positive total slack
and keeps all preparation/recovery work.

The critical A access also illustrates why failing the A-child guard
does not automatically mint an extra A event: its depth is two, so it
still costs one StepEv. No general reserve follows from that guard failure.

Thus the first difficult source regime already lies completely outside
the guarded reduction's availability. A proof of its sign needs a new
A/full-B law, not a favorable erased-orbit selection within the old guard.

## E. Exact guard analysis and fixed-key cover compatibility

### E.1. What each guard does and does not follow from

In this table, "not proved from negativity" is intentional. Positive
source witnesses do not logically disprove an implication whose premise
includes negative slack.

| Guard | Exact requirement | Closure / genuine-source failure | Consequence of failure and phase/key issue |
|---|---|---|---|
| Two adjacent constant-target runs | Only z requests, then only y requests, with no intervening third target | Closure permits arbitrary DELETE helpers and third targets | No legal skipping of such operations follows. A phase cut cannot remove an internal third target. Another reduction needs an endpoint proof. |
| Both runs contain KEEP | The first run must contain the omitted genuine access; the next target run must contain a retained KEEP | Gamma preparations contain actual DELETE-only runs | A different target run cannot be used as the second run by silently dropping intervening requests. Such DELETE work is real A cost, but not automatically free under an auxiliary map. |
| A child z | Before its first request A has z as a physical child | Critical Gamma A depth two violates this while still costing one event | Neither extra A cost nor this guard is forced by negativity/minimality as proved here. A full-source phase cut preserves its input geometry. |
| A y locality and g_A!=y | y is a child of z or the opposite child of the old A root | R03-B has the next target deeper; root-return words can have y=g_A | Without this guard no A saving/end-state identity is certified. Particular failures may force more A work, but no universal disjoint reserve follows. |
| Full-B child z | First KEEP(z) has full pre-depth exactly one | Every maximal closed core forbids it | This is the first source-geometric availability barrier. Resampling E does not change it. |
| Full-B y locality and g_F!=y | Direct and after-z y lie in the exact S/M/O frames | R03-B violates it even with a child z; Gamma critical pairs are old-root returns | The absorption identity can fail; no universal price beta<=1 has been proved outside these frames. |
| Disjoint packet inventory | Selected packets do not share requests | Different-key neighboring packets may share their middle run | Use one packet at a time or the fixed-key construction below. Do not sum conflicting original inventories. |
| Full key coverage | Every KEEP(z), including root repeats, is in removed first runs | A protected depth-at-least-three occurrence can never be covered | The absence of this condition blocks CD(r), not partial length reduction. It cannot be repaired for that key by a cyclic cut. |

Minimality supplies the exclusion (2), not any one of the positive guards.
None of the listed guards has been derived from negative scalar cost.
Complete closure supplies the admissible cyclic context; it does not force
the local frames. The maximal-core result supplies a whole closed domain
where the necessary B-child guard fails everywhere.

### Theorem R03.3-C — constructive fixed-key coverage criterion

Partition the CYCLIC request word into maximal constant-target runs. The
one-target case has zero full closed B charge and is irrelevant to a
negative source. Fix a genuine key z. Let I_z be the runs targeted to z
that contain at least one KEEP. For each run i in I_z, let i+1 be its
immediate next maximal target run, with target y_i!=z.

A disjoint complete Step 02 cover of all KEEP(z) exists if and only if
EVERY i in I_z satisfies:

1. Run i+1 contains a KEEP.
2. The actual A and F inputs before run i satisfy their exact guards for
   z,y_i, including the distinct-root conditions.

When these tests hold, select each full pair of runs [i,i+1]. This is
a constructive source rule, not a desired-capacity oracle. It yields
m=|I_z| packets and the inherited positive bound
Delta(W)>=3n_S+2n_M+n_O under CD(r) when |G(W)|=r+1.

**Proof of necessity.** A valid first z-run cannot start inside an existing
maximal z-run: after an earlier request to z, A is already rooted at z,
contradicting the A-child guard. It starts at the maximal run's beginning.
Its first run must continue to the next target change, because the second
run has a different target. It therefore contains that whole maximal z-run.
Its second run is an initial part of the immediate next maximal run, and
must contain a KEEP. The actual frame guards are exactly the stated tests.

**Proof of sufficiency and compatibility.** Extend the second run to its
maximal endpoint. After its first request A stays rooted at y_i; after
its first KEEP, B stays rooted there too. This extension adds only relevant
root identities within the same target and changes no packet endpoint law
or price. Distinct z-runs have distinct successor runs. A successor has
target different from z, so it is not a first run of another selected
packet. Two distinct successors cannot be the same run because cyclic
successor has a unique predecessor. Hence all selected pairs are disjoint,
including at the cyclic seam.

They cover every KEEP(z) in the original word. Every endpoint and guard
comes from the actual original source. Cut at a packet boundary, apply
the inherited source theorem to that disjoint cover, and retain the
original occurrence/copy IDs before any period division. Full key removal
and the positive cost bound now follow from R03.2-I. QED.

This resolves the fixed-key compatibility question rather than assuming it.
It DOES NOT prove that a key passes all tests. Under CD(r), a negative
source must have, for every genuine key z, at least one i in I_z failing
one of these tests. A protected occurrence gives such an obstruction for
its key. A legal phase only rotates this same cyclic run list.

Across DIFFERENT keys the pairs [i,i+1] and [i+1,i+2] can overlap. They
cannot be simultaneously used against their original inputs. R03.2-N's
one-step-at-a-time reduction avoids this problem, but must recheck all
guards after each deletion. No assertion here converts arbitrary crossing
or newly nested comparison intervals into jointly legal original packets.

## F. Irreducibility, direct sign and the first missing arrow

### F.1. Restrictions with concrete consequences

The preceding results give these actual deductions, not a claimed exclusion
of all negative sources:

* An eligible packet gives an admissible shorter negative source if W is
  negative, by (1). Thus a shortest negative source has none.
* Complete fixed-key local eligibility gives a disjoint key cover and a
  strictly positive full-source sign under CD(r), by R03.3-C. Negativity
  therefore forces a failed local test for EVERY key.
* A deep KEEP is a permanent genuine access, by R03.3-P. It blocks key
  elimination through that occurrence under every later guarded rewrite.
* Extra A work E_src and positive deep deficit D_deep are unchanged by
  those rewrites, by R03.3-Q. One cannot count the local price as a new
  decrease in the deep deficit or an increase in that A reserve.
* If D_deep=0, direct original-source counting gives nonnegative slack.
  Every negative candidate must instead contain a permanent q>=3 request.
* Equality of retained ancestor cores on a retained-only region gives
  J=0 there by R03.2-C. Persistent disagreement with differing cores has
  no such price guarantee; the exact cross-key term remains.

Earliest and latest occurrences have no absolute cyclic meaning until a
cut is chosen. A protected occurrence has a fixed full source input in
every presentation. Reordering which occurrence is called first or last
cannot erase it, create a missing source event or pay it from a transient.
The phase/key choice can change E, but never these full-source facts.

### F.2. Exact missing implication

Already the following NECESSARY preliminary availability implication for
the guarded route is unproved:

\[
\begin{gathered}
CD(r),\quad W\text{ original admissible},\quad |G(W)|=r+1,
\quad\Delta(W)<0\\
\stackrel{?}{\Longrightarrow}
\exists\text{ genuine KEEP }t\text{ with }d_F(x_t)=1.
\end{gathered}
\tag{10}
\]

Even (10) would not provide the A guard, y-locality or the adjacent mode
condition. For a minimum negative source, the FULL missing statement is
that one such occurrence participates in an eligible A/F packet, OR that
some different independently signed source reduction exists, OR that a
source counting argument contradicts its negative slack.

On maximal cores, (10)'s conclusion is impossible. Thus that route must
first prove nonnegative slack on ALL original maximal-core sources at the
new support, or use a different reduction that acts without a depth-one
full KEEP. No inspected theorem supplies that arbitrary-support A/F sign.
CD(r) cannot be applied to an r+1-key maximal-core source itself, and its
erased r-key source still has the signed correction in (1) of Step 02.

The general dichotomy requested in I4 is consequently OPEN. Its reduction
branch is established conditional on actual eligibility. Its direct-sign
branch is established on the elementary D_deep=0 subdomain and existing
certified classes, not on their entire irreducible complement.

It would be circular to assert "every minimum negative source contains a
packet" just because that would contradict (2). Given the valid reduction
and well-ordering, proving that assertion for all minimum negatives is
itself equivalent to excluding negative sources. An independent geometric
argument is still required.

### F.3. Exact induction assembly and where it stops

For any actual finite reduction sequence W=W_0 -> ... -> W_k, all sources
are reachable, completely paired-closed and on the same physical K, and

\[
\Delta(W)=\Delta(W_k)+
\sum_{j=0}^{k-1}\sum_{i\in\mathcal P_j}(2-\beta_{j,i}).
\tag{11}
\]

The added terms are positive. The composed A unit maps have disjoint
omitted original pools. A unit omitted at one stage cannot be an image
of any later shadow unit; cyclic transport maps both endpoints into
one fixed source inventory. These inherited interfaces prevent repeated
credit. This is composition across proved parent/child comparisons, not
unsupported telescoping of queried-depth differences.

If |G(W_k)|<=r, CD(r) applies and (11) proves the full-source inequality.
If W_k has r+1 keys and an independently proved nonnegative sign, (11)
also proves it. The false shortcut is to infer either alternative merely
from termination. W_s in (8) terminates immediately with r+1 keys.
For negative W, a terminal negative W_k must still have r+1 keys by CD(r);
its nonexistence is exactly what has not been established.

There is no unconditional CD(r)=>CD(r+1), so induction from CD(6) cannot
be completed. No unrestricted CD or downstream conclusion is claimed.

## G. Mandatory adversarial controls and gate matrix

### G.1. Existing original-source controls

| Control | Consequence for this continuation |
|---|---|
| R03-B two-seed family | Changing E's price does not change full-source guard eligibility. The first p-to-x packet from T has x too deep; core/orbit optimization alone cannot supply its missing absorption identity. |
| Persistent amplification with D_z=0 and unbounded J_z | The [existing six-key family](../SE03_NONREJOIN01/SE03_SIX_KEY_PERSISTENT_AMPLIFICATION.md) rules out a bounded fee per omitted KEEP or its bounded preparation. No such bound is used. |
| Nonrejoining full/erased histories | Complete raw equality is not assumed from common roots. Core-congruent regions have zero price only under their proved hypotheses; other persistent regions remain unpaid. |
| Gamma_s unbounded packet width | Equation (9) is an actual negative LOCAL price inside a positive paired-closed source. It prevents automatic nonnegative pricing of all uncovered pieces and does not refute full CD. |
| Physical-key removal | [Extreme-key noncommutation](../SE03_NONREJOIN01/SE03_CONTRACTION_NONCOMMUTATION.md) remains. Every source comparison here retains all keys and uses ordinary splays. |
| Interval trimming | The [existing RL-plus-zig versus RR obstruction](../SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/INTERVAL_PROJECTION_OBSTRUCTION.md) keeps its recorded source-replay-pending qualification. No trimmed history is treated as an original source. |
| Restricted return pulses | The original six-key pulse class is retained, including its five-key/nine-core funding proof. It does not establish a return-pulse cover of all maximal-core or irreducible sources. |
| No immediately usable packet | W_s is a complete original diagonal paired-closed witness, not an abstract state cycle. It has no eligible packet at any phase. |
| Cyclic seams and overlapping detours | One fixed key has the proved disjoint successor construction. Different-key overlap is not simultaneously removed; sequential rewrites use actual current states and original-ID maps. |

### G.2. A concrete failed weakening of the guard

The proposal "a child z in both input trees is enough; allow any next y"
is FALSE. Use the existing R03-B T with m=1:

\[
T=g(p(L_0,s(x(L_1,L_2),L_3)),R),\quad
U=x(p(L_0,L_1),s(L_2,g(L_3,R))),
\]

and its established direct-x output

\[
X_0=x(p(L_0,L_1),g(s(L_2,L_3),R)).
\]

The original first Kp,Kx ends at U. Deleting Kp and directly accessing x
ends at X0. Their right-child roots s and g differ for EVERY legal hanger
substitution. The original source P C_k is fully paired-closed from the
diagonal by Step 01. Symbolically continuing the shortened Kx,Kp,Kg suffix
gives the already displayed G0, whose g-left root x differs from T's p;
the inherited padding C_k is an identity on either g-left term. Thus this
naive deletion also fails complete closure from that original starting pair.

This uses the existing free-term identities, not a splay replay. The result
refutes the weakened endpoint guard; it neither refutes R03.2-D nor supplies
a negative original CD source.

### G.3. Proof-obligation matrix

| Gate | Required theorem |
|---|---|
| R3-1 | **PROVED at the inherited analytic scope:** Exact Step 02 guarded reduction inherited at its certified scope. R03.2-D/I/N and equation (1) retain their author-checked, non-formal and non-external audit qualification. |
| R3-2 | **OPEN:** Valid reduction exists for every minimal negative source, OR the unreducible class has nonnegative slack. Even necessary depth-one availability (10) is unproved; the full packet existence/direct-sign dichotomy is not established. |
| R3-3 | **PROVED for eligible Step 02 steps:** Every reduction preserves original source legality and exact paired closure. Partial key removal is included; unguarded or overlapping removals are not. |
| R3-4 | **PROVED:** The reduction strictly decreases a well-founded measure. A nonempty request run is removed, so closed-word request count decreases. |
| R3-5 | **PROVED for those actual steps:** All signed inequalities and packet costs compose without loss. Equation (11), price 2-beta in {1,2,3}, and composed original-unit maps give the scalar and nonduplication statement. No new frozen-owner extension is asserted. |
| R3-6 | **CONDITIONAL on actual support reduction:** CD(r) applies to the resulting source when support is reduced. Its legality is proved, but a terminal source with r+1 keys is outside CD(r). |
| R3-7 | **OPEN:** Universal CD(r) => CD(r+1) follows only after R3-2 or another complete source bridge is supplied; termination and a positive local price do not supply it. |

For R3-2 the exact missing implication is (10) followed by actual guarded
eligibility in a minimum negative source, or an independent nonnegative
sign theorem on every eligible-packet-free original source with r+1 keys.
Maximal-core sources are a necessary untreated part of that latter domain.
No proof excluding their negativity from the original A/full-B geometry
is given. For R3-7 the exact missing input is that same implication for
EVERY r>=6; no remaining closure or well-foundedness lemma can substitute
for it. These are unsolved assertions, not renamed certified lemmas.

## H. Verdict, claim boundaries and isolation

**OUTCOME C — STRUCTURAL ONLY at the requested universal sign/reduction
gate.** The continuation proves an exact deep-occurrence survival invariant,
quantitative rewrite invariants and a constructive fixed-key cover test.
It also establishes a family-wide obstruction to THIS guarded mechanism:
the entire maximal-core domain admits no Step 02 step. None of these proves
that a hypothetical negative source cannot inhabit the remaining domain.

The following candidates receive **scoped Outcome F / REFUTED** status:
unqualified packet availability for all original sources; automatic support
drop on termination; phase reseeding as a universal repair of full-source
guards; the child-only weakening of absorption; and nonnegative price for
every uncovered local segment. Their witnesses and exact scopes are above.
The negative-source-only availability implication and Universal CD remain
OPEN, not REFUTED. Positive W_s/Gamma sources are not counterexamples to
either statement.

No new paid elimination of an irreducible r+1-support source is established.
The first missing arrow is source negativity to a usable reduction or a
source-derived contradiction. This report does not disguise that missing
arrow with the inventory identity or the new structural restrictions.

All new mathematical checks are free-term/source arguments operated by the
same author. No new independent machine or external audit is claimed.
All new filesystem writes are confined to the new Step 03 report and its
metadata in this Route 03 location. Steps 01/02, original evidence, physical
IDs, reaching prefixes, actual historical periods, frozen g1/fE/h0 owners,
R1-R4 and Bank25 remain unchanged. Comparison maps refer back to actual
original events; they do not edit archived executions or install new owners.

There were zero new source queries, splay-engine calls, semantic replays,
experiments, state searches, potential constructions, solver runs or research-
program executions. Existing reports were read directly and their symbolic
results used at their declared scopes. File identity/reference checks are
metadata operations. No other route, subagent, C01-C09 restart, cap increase
or resource reset is used.

The historical ledger inherited through Step 02 is global CPU
6392.953125/7200, symbolic 2451.21875/2640, independent
740.359375/750 and queries 3050330/3100000. It is quoted as historical
context, not replaced by a new live aggregate or charged against another
route's reservation. No proof-computation process was launched here;
metadata follows the inherited exclusion. Unrestricted CD and all downstream
claims remain unproved by this route.
