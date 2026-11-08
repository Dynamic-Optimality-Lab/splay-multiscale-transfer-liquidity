# Parallel Route 03 — signed support-erasure induction, Step 01

Date: 2026-11-08 (Asia/Karachi).

**Verdict: OUTCOME B — PARTIAL INDUCTION PROGRESS.** The universal implication
`CD(r) => CD(r+1)` remains unproved. The new result is a source-valid theorem
about the choice of an erased recurrent orbit: cyclically transporting an
existing erased orbit preserves its normalized charge, whereas starting
erasure afresh at a different reached full-source boundary can select a
different orbit and a different charge. Section D proves this distinction and
an explicit arbitrary-support family with marginal `2m` for one erasure seed
and marginal zero for another. It also gives an exact, restricted
lower-support comparison for the latter seed.

This is structural progress for the signed-erasure route, **not new CD-domain
coverage**: the displayed family's full sources already satisfy a direct
elementary cost bound. No uniform repayment, favorable-key selection theorem,
Universal CD, `B <= 3A`, or Dynamic Optimality conclusion is claimed.

## A. Inherited theorem ledger

### A.1. Immutable source and cost contract

An original source uses a finite totally ordered, physically present key set
`K`. An ordinary bottom-up splay is performed in A on EVERY request. B splays
only on KEEP. DELETE is an A-only access and removes no physical key. A root
access is an identity; a nonroot splay genuinely changes the tree, including
a depth-one zig whose B-double cost is zero.

Reachable means reachable by a finite legal original prefix from a permitted
common-tree diagonal. A paired-closed source may start at a nondiagonal pair;
its COMPLETE labeled A and B trees must each return to their own starting
trees. The reaching prefix is not a source of credits for the closed period.
The support restriction applies to the closed source, not to an invented
restriction on its reaching prefix.

The original weights are

\[
a_t=\lceil d_A(x_t)/2\rceil,\qquad
q_t=\begin{cases}\lfloor d_B(x_t)/2\rfloor&\mathrm{KEEP},\\0&\mathrm{DELETE},\end{cases}
\qquad \Delta(W)=2A(W)-Q_B(W).
\]

Every A terminal zig contributes one A StepEv. A B terminal zig still executes
and changes the tree even though it contributes no double. All arbitrary A
ancestors, helpers, B hangers, DELETE populations and source lengths remain
permitted. The induction variable is distinct genuine KEEP keys.

### A.2. CD(6), including its actual base interface

The authoritative
[CD6 final certificate](../SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_FINAL_CERTIFICATE.json)
has status `PROVED_COMPLETE_ORIGINAL_SIX_KEY_COARSE_DOUBLE`. Its literal
statement is an explicit injection for **exactly six** genuine KEEP keys on
original reachable exactly A/full-B paired-closed sources. The
[CD6 theorem](../SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_THEOREM.md) explicitly
combines it with the sealed CD(5) base to obtain support **at most six**.
That is the inherited scalar `CD(6)` used here.

The proof was read through its
[full assembly](../SE03_STEP2_CD6_FINAL_ASSEMBLY_14/FULL_PROOF.md), source
specification, core exhaustion/constancy, class ledger, absolute-period
transport, signed charts, owner exchange, carry proof, independent audit and
adversarial audit. The imported class proofs inspected were Campaign 10's
`RESIDUAL_SLOT_THEOREM.md`, Campaign 13's `CORE7_FULL_FUNDING.md` and
`CORE8_FULL_FUNDING.md`, and unary-lift 14's unrestricted `FULL_PROOF.md`.

The assembly uses one fixed labeled full marked core of size 6 through 11,
selects ONE complete whole-period class constructor, and counts the resulting
injection into the original two bits per A StepEv. The necessary core masks
number `1/5/13/21/16/1`, totaling 57. These are proof domains, not six-node
ambient trees or an assumption about a fixed B word. The full 9–11 import
retains unrestricted private A ancestors and source helpers; its title is
not a restriction to one unary A example. Its certified working bound is 11
under unchanged Bank25.

The [CD5 proof](../CD5_BASE01/CD5_PROOF.md) covers at most five genuine keys
with arbitrary physical support. Its branches are support at most three,
four, five/core at most eight, and five/core nine. Only the appropriate
branches prove the stronger B-only change-count bound. General scalar CD5
does not imply that stronger bound or a new physical allocator on every
auxiliary domain.

The certificate's 44 listed file entries were checked against their literal
SHA256 values, all matching; the metadata result is
[CD6_CERTIFICATE_METADATA_CHECK.json](CD6_CERTIFICATE_METADATA_CHECK.json).
This checks those publication contents, including repeated references. It is
not a rerun of the historical semantic audits or a new verification of all
2,746 transitive pins. The inherited trust scope remains computer-assisted
symbolic proof with a distinct implementation operated by the same agent,
not external review or proof-assistant certification. The base is inherited,
not reproved here.

### A.3. Signed erasure, representation and repairs

| Inherited source | Exact conclusion and scope | What it does not establish |
|---|---|---|
| [CD_UNIFORM01/SUPPORT_ERASURE_CLOSURE.md](../CD_UNIFORM01/SUPPORT_ERASURE_CLOSURE.md) | For any genuine erased key, actual changed-mode repetition from a reached pair eventually gives a reachable fully closed lower-support source. All erasures can be aligned by common multiples. | No sign for the full-minus-erased charge. |
| [SE02/ERASURE_ALIGNMENT.md](../SE02_ERASURE01/ERASURE_ALIGNMENT.md) | On the ACTUAL recurrent interval, `R_I=R_z,I-Delta_z,I`, with `Delta_z,I=D_z,I+J_z,I`; exact transient subtraction and common normalization. | No repayment or favorable-key theorem. |
| [SE03/UNIFORM_B_PAIR_PROJECTION.md](../SE03_NONREJOIN01/SE03_UNIFORM_B_PAIR_PROJECTION.md) | Both actual B histories use the same fixed full-core label set S, `|S|<=2|M|-1`, with all original gap BSTs rigid. Every original core label stays in the raw skeleton. Search depths, parity, ordinary splays and complete endpoint equality are preserved. | Not a projection that physically removes an erased key; not a claim that arbitrary skeleton pairs are reachable. |
| [SE03/EXACT_NONREJOINING_SOURCE_IDENTITIES.md](../SE03_NONREJOIN01/SE03_EXACT_NONREJOINING_SOURCE_IDENTITIES.md) | Exact primitive depth/parity transport and queried-coordinate renewal. Summing the tracked discrepancy leaves a cross-key transport term. | Equal retained roots do not imply full rejoining; no favorable sign for the cross-key term. |
| [Step1/SOURCE_BRIDGE.md](../SE03_STEP1_FUND01/SOURCE_BRIDGE.md) and [AUXILIARY_FUNDING_THEOREM.md](../SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md) | Five genuine keys/core nine: `Q_E<=2 sum min(H_i,3)`, with a source-valid explicit allocation, carry at most two, working queue at most eight and identified tail/surplus reserve. | Not an all-support local certificate or full-interference payment. |
| [REPAY02/RETAINED_GAP_RESERVATION.md](../SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md) | At that same five-key/nine-core scope, partition after EVERY retained KEEP. A positive repeat gap has `H>=2`; the refined independent gE uses at most its first A event and excludes both bits of every later event, giving `2(H-1)` identified protected units. | gE is not the fixed fE; those units are not automatically unowned under fE or g1. |
| [REPAY02/B_RETURN_PULSE_EXTENSION.md](../SE03_STEP2_REPAY02/B_RETURN_PULSE_EXTENSION.md) | Complete six-key B-return-pulse repair, including five-key/core-nine auxiliaries, arbitrary A changes and DELETEs; exact full-B inverse pulses rejoin and distinct second-event donors pay their two doubles. | No universal pulse partition, no persistent-disagreement theorem. Supersedes the older pulse result's auxiliary-core-eight funding restriction for this class. |
| [SE03/EXCURSION_RESERVATION_LEMMA.md](../SE03_NONREJOIN01/SE03_EXCURSION_RESERVATION_LEMMA.md) | Disjoint A-identity intervals containing only DELETE/Kz can be removed after erasure. CD on the resulting valid lower-support source excludes their real units from auxiliary funding. An independently proved marginal bound can then use those units. | Neither universal existence of those intervals nor their required marginal bound. |
| [SE03/CORE_DEFICIENCY_AND_LEAF_SELECTION.md](../SE03_NONREJOIN01/SE03_CORE_DEFICIENCY_AND_LEAF_SELECTION.md) | For full support s/core c, growing-visited losses sum to `2s-1-c`. Marked-leaf erasure at a reached cut bounds the recurrent erased core by `min(c-1,2s-3)`. | No favorable signed marginal. Maximal-core restrictions are necessary geometry, not payment. |
| [SE03/INDUCTIVE_STARTUP_AND_SAFE_PIECES.md](../SE03_NONREJOIN01/SE03_INDUCTIVE_STARTUP_AND_SAFE_PIECES.md) | Under the smaller-support hypothesis, cycle excision bounds an open lower-support segment below by `-(Cat_n^2-1) floor((n-1)/2)`. Its safe-piece consequence has an explicit capacity guard. | No ambient-independent reserve; repeated separations can repeat startup costs. |
| [C14/UNIFORM_R_TRANSFER.md](../SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md) | U-B: specified source-local credit licenses plus the actual smaller physical interface suffice for a constructive transfer. Uniform low-cost A syntax retains at most `2s+2H-3` known nodes and arbitrary private terms. | Universal source sign/supply hypotheses remain OPEN; scalar CD is weaker than the witness-rich invariant. |

The older Campaign 10 `UNIFORM_R_INTERFACE.md` and Campaign 13
`UNIFORM_R_TRANSFER.md` were also inspected. Their historical OPEN labels
for six-key subclasses are superseded by the final CD6 assembly, not by an
unrestricted support theorem.

The literal primitive left-rotation depth changes in the inherited convention
are `p:+1, c:-1, L:+1, M:0, R:-1` for
`p(L,c(M,R)) -> c(p(L,M),R)`; right rotation is its reflected formula. For a
retained key of pre-depths f,e,

\[
j_t=\lfloor f/2\rfloor-\lfloor e/2\rfloor
    =(f-e-(f\bmod2)+(e\bmod2))/2.
\]

The full and erased source frames can differ. These are equality rules,
not a cumulative interference bound.

### A.4. Later results and corrections that constrain this route

The following later material was checked for a superseding universal theorem:

* [C23/ERASED_FULL_B_RETURN_CLASSIFICATION.md](../SE03_STEP3_NONIDENTITY_A_TREE_FLIP_23/ERASED_FULL_B_RETURN_CLASSIFICATION.md) and `CD6_LEGAL_TRANSFER_INTERFACE.md` provide exact, restricted top-root return tests and corrected shadow-source transfer. Their stated status is mathematical derivation with independent audit pending; that status is retained.
* [C35/SC35 source reduction](../SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_02/SIMPLE_CYCLE_SOURCE_REDUCTION.md) already removes repeated COMPLETE A/full-B boundary states and partitions original inventories into valid source children. Its state-simple large-support leaves remain unpaid. This is not rediscovered as a new induction theorem here.
* C35's `CONTINUATION_04/ARBITRARY_SUPPORT_ANCHORED_WORD_FUNDING.md` and `ALL_SUPPORT_RETURN_ESCAPE_NECESSITY.md` prove restricted source-family statements, with their recorded review-pending qualifications. They do not cover every source or provide a generic erased interference law.
* [C35/ROUTE3_SIGNED_CERTIFICATE_GATE_VERDICT.md](../SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ROUTE3_SIGNED_CERTIFICATE_GATE_VERDICT.md) and `ROUTE12_COMBINED_FUNDING_GATE_VERDICT.md` explicitly leave the all-support source/sign/owner bridge open. No pending result from Routes 01 or 02 is used here.

Read the SE03 transport identities with
`SE03_SOURCE_CONVENTION_CORRECTION.md`: an erased request has zero B CHARGE
by mode, not necessarily zero erased pre-depth. Read the negative-block
classification with `SE03_BLOCK_CLASSIFICATION_CORRECTION.md`: positive
preterminal requests in an H-at-most-two genuine macro are DELETEs. Read
the older SE02 depth-vector prose with `SE03_DEPTH_VECTOR_CLARIFICATION.md`:
complete labeled depths and key order DO determine a BST; roots, selected
depths or floor-depth differences alone do not.

## B. Exact support-reduction contract

Fix arbitrary `r>=6`, assume `CD(r)`, and let W be an original admissible
source with exactly `r+1` genuine KEEP keys. By inherited cyclic root
provenance, its set M of all KEEP targets equals its genuine target set.
Choose `z in M`. Change every `KEEP(z)` to `DELETE(z)`, retaining every
occurrence and key. This is the only basic erasure used here.

### B.1. What is preserved and what needs recurrence

A receives the identical request sequence from the identical A start.
Determinism preserves every complete A tree, depth, primitive rotation,
StepEv and bit ID at every occurrence. Its one-period cost is exactly A(W).
No physically erased key, interval trimming or synthetic operation occurs.

B performs the retained KEEP subsequence as actual ordinary splays on all
original keys. It need not return after one erased word. Let F_z be its
one-period map. Start at the original reached pair, keep the original
reaching prefix, and then repeat the changed word. This ENTIRE prefix is
legal from the original permitted diagonal. At each word boundary A returns.
Finiteness gives a reached preperiod u and recurrent period p. If L is a
positive multiple of p, the actual interval

\[
I=[uN,(u+L)N)
\]

is a lower-support paired-closed source. Its starting B need not equal the
original B start. It has at most r genuine KEEP keys, because all its KEEP
targets lie in `M\{z}`. Therefore `CD(r)` applies to THIS source.

This resolves diagonal REACHABILITY rather than assuming it from finiteness:
the diagonal belongs at the beginning of the complete legal reaching history.
The recurrent interval need not itself begin on the diagonal. If the original
definition had required each closed interval to start with A=B, this argument
would fail; the read CD5/CD6 definitions explicitly permit reached pairs.

A cyclic cut of the original closed source is reached by extending its
original prefix to that boundary. A cyclic cut of an erased source is reached
by extending that erased source's OWN prefix. Section D distinguishes this
transport from restarting erasure at the corresponding full-source pair.

### B.2. Common skeleton, physical support and period identities

The full original marked core S has at most `2r+1` labels. Both B histories
can use the inherited common S skeleton with every original label retained,
plus its exact fixed gap BSTs. In particular, an erased mark that drops from
the smaller marked core is still a physically present raw-skeleton key.
Rigid-hanger pruning preserves each actual search depth and all ordinary
zig/double formulas. Full equality of skeleton endpoints restores all fixed
gap terms and hence the entire B tree.

The A history is not projected to this B skeleton. Anonymous A nodes touched
by DELETEs or KEEP splays remain in A with their actual costs.

Each occurrence in I has its own copy/occurrence/event/bit ID. The original
full source on I has costs `LA(W), LQ_B(W)`. Auxiliary p-period totals cannot
be compared with one original period without dividing EVERY scalar term by
the same positive L. Division does not turn a multi-copy physical map into a
one-copy map, nor authorize borrowing from the preperiod.

## C. Exact signed cost comparison

Use the literal inherited names, with subscripts showing the ACTUAL interval:

\[
\begin{aligned}
R_I&=2LA-LQ, & R_{z,I}&=2LA-Q_E(I),\\
\Delta_{z,I}&=LQ-Q_E(I),\\
D_{z,I}&=\sum_{t\in I:\,Kz}q_t^F,\\
J_{z,I}&=\sum_{t\in I:\,Ky,\ y\ne z}(q_t^F-q_t^E).
\end{aligned}
\]

Here inherited `Delta_z,I` is a MARGINAL, whereas the user's `Delta(W)`
is the original CD SLACK. Thus

\[
\boxed{R_I=R_{z,I}-D_{z,I}-J_{z,I}},\qquad R_I=L\Delta(W).
\]

D is nonnegative; J is signed. A genuine full depth-one Kz contributes
zero to D but can alter subsequent retained costs. A full root-identity KEEP
can become genuine in E and contribute negatively to J. All A work is kept.

For complete prefix-period totals `Q_E[0,k)`, the aligned marginal is exactly

\[
LQ-Q_E[0,u+L)+Q_E[0,u).
\]

The transient must be subtracted; it has no assumed sign. Root equality is
not a telescoping boundary condition for these cost sums. On an actually
closed full/erased pair a genuine state boundary difference cancels, but
the queried-depth sum can still be positive.

At retained occurrences pair the first `min(qF,qE)` demand ordinals. If P is
the unmatched full inventory (including erased demands) and N the unmatched
auxiliary inventory, then `|P|-|N|=D+J`. An existing injective auxiliary map
releases precisely its N-owned units upon retirement, disjoint from its unused
reserve. The signed identity creates no new bit and does not by itself show
that all P demands fit. No claim is made that a raw unit is free under fE,
the prior full map, or g1 merely because another independent comparison
does not use it.

`CD(r)` gives `R_z,I>=0`. It does NOT give `D+J<=R_z,I`. By the boxed
identity that latter assertion is exactly the desired full-source conclusion,
so naming it a repair lemma would be circular.

## D. New theorem: reached phase seeds and erased recurrent-orbit transport

### D.1. Transporting an erased orbit preserves its charge

**Theorem R03-T (cyclic transport with its actual erased state).** Split an
original full closed word as `W=UV`, where U may end at any actual occurrence
boundary. Fix z. Let u and v be the B maps of the erased U and V. Suppose a
reached erased recurrent state E belongs to a p-cycle of

\[
f=v\circ u.
\]

Then `u(E)` belongs to a p-cycle of the rotated map `g=u∘v` for the erased
word VU. The rotated erased source is reachable with the correct original
A tree at that cut, closes in both complete trees after p words, and has
the SAME total erased B charge over those p words. Hence its normalized
erased charge and normalized signed marginal are unchanged by this transport.

**Proof.** Associativity gives `g∘u=u∘f`. On the f-cycle, f is bijective.
If `u(E1)=u(E2)` for two states of that cycle, applying v gives
`f(E1)=f(E2)`, so `E1=E2`. Thus u maps this cycle bijectively onto a
g-cycle, preserving its exact period p. Inverse transport on that cycle
is `f^{-1}∘v`; no inverse splay operation is being proposed.

For source legality, take the actual reaching prefix for `(A_start,E)`,
then execute the erased U. A reaches its original U-cut tree, while B reaches
u(E). Now repeat the erased VU p times. Its A request sequence is the cyclic
rotation of a closed original A word, so A returns. The map calculation
proves complete B return. Every operation is an original KEEP or DELETE.

For costs, start the length-p erased W orbit at E and read it cyclically
beginning just after its first U. Its segments are

`V_0, U_1, V_1, ..., U_(p-1), V_(p-1), U_p`.

Because `f^p(E)=E`, the final U_p starts in exactly the state of U_0 and
has exactly its charge. This replaces U_0 by the equal U_p charge and
otherwise just rotates the same operations. The total is unchanged. The
same statement holds for full costs and original A costs. Distinct physical
copies remain distinct; this is a scalar comparison and an actual-period
occurrence transport, not a donation from U_0 to a different source period.
QED.

**Consequence.** R03-T transports u(E), NOT the original full B tree after U.
Those trees can differ. Starting erasure afresh at the latter tree is a new
legal source construction, with a different reaching prefix and potentially
a different recurrent orbit. It is not a coordinate change of the old erased
source. No computational experiment is run here.

### D.2. Phase seeding is source-valid

**Lemma R03-S (phase-seeded comparisons).** For each reached boundary s of
an original paired-closed W, it is legal to follow the original reaching
prefix and the original word up to s, then begin erasure and repeat the
rotated word `W_s`. Its eventual recurrent erased interval is a valid
lower-support source with the unchanged cyclic original A trajectory.
Transporting THAT interval back to the displayed original seam uses R03-T.

**Proof.** The prefix is a legal original full-source prefix. The subsequent
changed-mode word is also legal and A-closed word by word. Apply the inherited
finite-map closure argument to its actual B orbit. Transport uses the actual
erased prefix map, so both its reaching condition and complete-state closure
are preserved by R03-T. QED.

This adds freedom to the comparison construction; it does not assert that
one of these seeds is favorable for an arbitrary W.

### D.3. A source family with two distinct recurrent prices

**Theorem R03-B (phase-dependent interference at every support size at least
seven).** For every `k>=4` and `m>=1`, there is an arbitrary-fringe original
closed B source with `k+3` genuine KEEP keys and an erased key p such that:

1. Erasure seeded at one reached full boundary has a one-period transient,
   then persistent full/erased disagreement, `Q_E=0`, `D_p=0`, `J_p=2m`
   per original period.
2. Erasure seeded at another reached full boundary closes in one period,
   with `Q_E=Q_F=2m`, `D_p=J_p=0`.
3. p is the minimum genuine key, and at the second boundary it is a leaf
   of the full marked core. The first erased orbit has the smallest possible
   retained marked core, yet has the larger signed marginal.

The B statements apply to ANY original paired-closed A history with this
full B orbit, arbitrary legal DELETE interleaving, helpers and inserted
current-B-root identity KEEPs. No A reset across the blocks is required.

**Construction.** Choose physical keys

\[
p<x<s<g<h_1<\cdots<h_k.
\]

Let `L0,L1,L2,L3` be arbitrary BSTs, respectively below p and in the
gaps `(p,x),(x,s),(s,g)`. Let `E0,...,Ek` be arbitrary BSTs in
`(g,h1),(h1,h2),...,(hk,infinity)`. These terms contain no named key.
Define the common right vine

\[
R=h_1(E_0,h_2(E_1,\ldots,h_k(E_{k-1},E_k)\ldots)).
\]

Use these complete trees:

\[
\begin{aligned}
T&=g(p(L_0,s(x(L_1,L_2),L_3)),R),\\
U&=x(p(L_0,L_1),s(L_2,g(L_3,R))),\\
V&=p(L_0,x(L_1,s(L_2,g(L_3,R)))).
\end{aligned}
\]

Let

\[
P=(Kp,Kx,Kp,Kg),\qquad
C_k=(Kh_1,\ldots,Kh_k,Kh_{k-1},\ldots,Kh_1,Kg),
\qquad W_{m,k}=P^m C_k.
\]

The descending portion of C_k contains k accesses, including its final Kg;
the whole padding word has `2k` accesses. It operates only on the right vine
above g; the entire g-left subtree is an opaque term.

**Full ordinary-splay proof.** The inherited universal P identity gives

`T --Kp--> p(L0,g(s(x(L1,L2),L3),R)) --Kx--> U --Kp--> V --Kg--> T`.

Its pre-depths are `(1,3,1,3)` and its double charges `(0,1,0,1)`.
These formulas use a zig, an LL double followed by a right zig, a zig,
and an RR double followed by a right zig, respectively. Thus each P restores
every term and contributes two doubles. Both erased Kp occurrences are
genuine depth-one full changes with zero doubles.

In C_k every ascending access is to the current root's right child, so it
is one right zig. It builds the corresponding left vine. The descending
accesses are precisely the inverse left zigs in reverse order. They restore
the COMPLETE input tree, including every E_i and its arbitrary g-left term.
Each has B depth one and q zero. This is a parametric rotation-word proof,
not a replay of concrete trees or a physical-node contraction.

Consequently full B returns to T with

\[
Q_F(W_{m,k})=2m,\qquad G=\{p,x,g,h_1,\ldots,h_k\}.
\]

Every displayed KEEP is genuine. The full marked core contains exactly
`p,x,s,g,h1,...,hk`, of size `k+4`; all other nodes are rigid gap BSTs.
At U, p is a marked core leaf and is the minimum genuine key. Its physical
left/right hangers L0,L1 need not be empty.

A nonempty source witness exists for every parameter and all gap populations:
start at the common diagonal `(T,T)` and use the displayed all-KEEP word.
A=B throughout and returns, with

\[
A(W_{m,k})=6m+2k,\qquad \Delta(W_{m,k})=10m+4k>0.
\]

These counts are consequences of the free-term formulas, not executable
source queries. The rest of the proof concerns B and therefore permits any
other A realization satisfying the original full-source closure hypothesis.

**First seed: erase p starting at the full T boundary.** Write

\[
X_0=x(p(L_0,L_1),g(s(L_2,L_3),R)),\qquad
G_0=g(x(p(L_0,L_1),s(L_2,L_3)),R).
\]

In the first P, erased Kp freezes B. Its retained Kx has path L,R,L:
the original RL double and terminal left zig give X0. Its Kg is a
right-child zig and gives G0. Thus this first P costs E one double.
From G0, every subsequent Kx/Kg pair is a left/right child-zig inverse,
returns G0, and has zero doubles. C_k is a complete identity on G0 too,
because its g-left subtree is opaque to every padding zig.

The first entire W therefore has erased charge one and ends at G0. Each
subsequent W returns G0 and has erased charge zero. Original A and full B
return word by word; the auxiliary start `(A_T,G0)` is reached after one
legal erased word from the original reached pair. Use `u=1,L=1`, or any
positive L after that warmup. On an aligned L-word interval,

\[
Q_F=2mL,\qquad Q_E=0,\qquad D_p=0,\qquad J_p=2mL.
\]

The unaligned first-word marginal `2m-1` is NOT the recurrent marginal.
For n words from T the marginal is `2mn-1`; subtract the first-word
marginal to obtain the aligned value `2m(n-1)` exactly.

At retained x boundaries the full right-child root is s in U, whereas it
is g in X0. At g boundaries the full left-child root is p in T, whereas
it is x in G0. At omitted Kp the full root is p and the erased root is not
p. Padding zigs carry these different g-left terms rigidly and invert them
without identifying them. Thus the two complete B trees do not rejoin after
the first full Kp; in particular disagreement persists throughout the aligned
recurrent history. Its retained marked core is just
`{x,g,h1,...,hk}`, of size `k+2`, the minimum possible for that retained
support. The still-present physical p and s lie in unmarked hangers.

**Second seed: begin erasure at the full U boundary after the first Kx.**
Reach that boundary through the original full prefix, then erase p in the
rotated W. Define

\[
G_1=g(s(x(p(L_0,L_1),L_2),L_3),R).
\]

The actual erased Kg from U has path RR and is one parent-first RR double:

\[
U\ \xrightarrow{S_g}\ G_1.
\]

The actual next erased Kx has path LL and is precisely its inverse double:

\[
G_1\ \xrightarrow{S_x}\ U.
\]

Erased Kp occurrences between them are identities by mode. At the seam
containing C_k, that word is again a complete identity on G1. Hence every
retained x/g pair contributes two erased doubles and returns to U; after
one whole rotated word B_E returns to U with charge `2m`. Original A follows
the unchanged rotated closed source, so its complete tree returns as well.
There is no auxiliary preperiod and this is a reachable original
lower-support source.

Full q at each retained x or g is one; erased q is also one. Padding full
and erased q are both zero. Every erased full Kp has q zero. Therefore,
at the literal corresponding occurrences,

\[
\boxed{Q_E=Q_F=2m,\quad D_p=0,\quad J_p=0.}
\]

Its retained core has size `k+3`: the unmarked s remains an ancestor of
x or g. The larger retained core here has the SMALLER marginal.

All formulas retain arbitrary gap populations, every physical key, all
zigs and both complete endpoints. Extra DELETEs alter neither B calculation;
A costs at those DELETEs are retained, and the asserted A closure is the
original source hypothesis. Current-full-root identity KEEPs also have
zero charge in both erased orbits: at an omitted-root p they are erased,
and at every retained root both histories have that root. They therefore
preserve the displayed statements. QED.

### D.4. Why this is not the same as transporting the first erased orbit

Transport the first orbit's G0 state from the T seam through the erased
prefix `Kp,Kx`. Its actual destination is X0, **not U**. The transported
rotated source therefore still has erased charge zero by R03-T. The second
seed uses the actual FULL prefix to reach U before activating erasure; it
selects another recurrent orbit. This accounts for the different prices
without contradicting cyclic invariance of a fixed execution.

Indeed both erased orbits can be represented at the original T seam. From
the reached U pair, execute the erased suffix back to that seam. A returns
to its original T-phase tree and B reaches G1. Repeating the erased original
word from G1 costs `2m` and returns G1. The source start is legally reached,
although it differs from the G0 start of the canonical T-seeded comparison.
Thus the phase-seeded comparison can be aligned back without changing
original A work or borrowing prefix credits.

The new structural lesson is exact: **an erased comparison is determined by
its reaching history and recurrent orbit, not by the erased cyclic target
word alone.** Minimizing the erased core is not a theorem minimizing the
signed erasure marginal. These conclusions follow from explicit original
tree identities and a source-valid construction, not just rewriting slack.

### D.5. Scope and novelty audit

The three-key P identity, its T-seeded zero-direct persistent discrepancy
and arbitrary-fringe interpretation are inherited from
`SE03_ZERO_DIRECT_PERSISTENT_INTERFERENCE.md`; they are not new claims here.
The new derivation is the alternate U-seeded recurrent orbit, its complete
source-valid cyclic transport, and the all-support right-vine extension
proving that different erased recurrent prices occur at every support size
at least seven. These conclusions were not stated in the inspected erasure
reports; no claim is made about exhaustive novelty outside that record.

This family is NOT a hard new CD class. Each P uses four genuine full
macros with q at most one; the padding uses genuine zero-double zigs.
At every genuine full macro the A root must move between its two different
marked boundary roots, so its true A cost H is at least one. These disjoint
macros already give a direct safe inequality for every A realization under
discussion. The all-KEEP witness also splits into old small-support closed
pieces. The theorem advances erasure-state selection, not original CD-domain
coverage or the universal compensation gate.

## E. Induction assembly: achieved part and smallest missing bridge

### E.1. Exact restricted implication supplied by the new result

Let `r=k+2>=6` and assume scalar `CD(r)`. Let W have exactly the B orbit
of R03-B and satisfy the original full-source A reachability/closure
conditions. Choose p and the reached U seed. The auxiliary source has r
genuine KEEP keys, the SAME cyclic A trajectory and exact one-period
A/B_E closure. It lies in the original CD(r) domain. Hence

\[
Q_E(W_U)\le 2A(W_U)=2A(W).
\]

R03-B proves occurrencewise `Q_F=Q_E` and `D_p=J_p=0`, so

\[
\Delta(W)=\Delta_E(W_U)\ge0.
\]

This is a genuine source-valid support-erasure implication for its explicit
restricted family at every r. Its independent direct-safe proof means it
does not establish new CD coverage. No general source is assumed to possess
that B orbit, an inverse x/g pair, or a favorable phase seed.

### E.2. Universal obligations that remain

For arbitrary W with r+1 genuine keys, the following are established:

1. KEEP-to-DELETE erasure preserves the entire A inventory and all physical
   keys; actual recurrence and the legal reaching prefix supply a lower-
   support paired-closed source.
2. An erased orbit can be transported across cyclic cuts without changing
   its price, provided its ACTUAL state is transported.
3. Additional reached full-source seeds are legal comparison choices, but
   can have different prices, as R03-B proves.
4. The full signed identity includes every direct and retained charge.

The missing bridge is still a **source-complete quantitative theorem**.
One must prove that every such W has some admissible erased comparison
(possibly using the additional phase-seed freedom), or a justified family
of lower-support comparisons, whose independently certified source reserves
and signed cancellations pay ALL full-minus-erased demands without repeated
use of an A unit. No theorem here establishes that existence or payment.

For an excursion-based implementation the concrete residual is: find
disjoint removable A-identity intervals of total cost E, then prove from
original rotations that the aligned marginal is at most `2LE`. This is
more informative than an unspecified slack assertion because the excluded
units are explicitly identified. Universal existence and that signed bound
remain unproved. Phase seeding alone creates no such intervals or units.

Merely requiring a selected comparison to satisfy `D+J<=Delta_E` restates
the desired conclusion; it is not presented as a smaller solved obligation.
Similarly no nonnegative-combination inequality for arbitrary W has been
constructed. Consequently the formal universal step cannot be completed,
and ordinary induction from CD(6) cannot yet be invoked.

## F. Reserve extension, global composition and rejected candidates

### F.1. What does and does not generalize in the repeat-gap reserve

For ANY support size a gap starting and ending with retained target y has
`q_E=0`, and H is zero or at least two. The elementary root argument is
uniform: if A leaves y at a positive event, it needs a later positive event
to return. This proves actual A work, not its exclusion from an auxiliary
allocation.

At the certified five-key/nine-core scope, the existing debt range is two.
For a positive repeat gap, spending one selected A event covers the worst
endpoint difference; hence the refined gE can exclude `2(H-1)` actual bits.
The range and complete local law, not H alone, license that allocation.

The unsupported extrapolation is

`H>=2, q_E=0  =>  after any lower-support funding, 2(H-1) units are free`.

It does not follow from scalar `CD(r)`, which does not localize its use of
A capacity. Nor is gE freedom freedom under frozen fE or g1. No counterexample
to every possible universal reserve theorem is asserted; the named inference
is unsupported. In an analogous range-K allocator, the repeat-gap range
argument would need `c>=ceil(K/2)` selected events when that choice is
possible, not necessarily c=1. No arbitrary-r K or local law is supplied.

The known Gamma_r full-price packet has H=2, Q=r, price `4-r`. It refutes
constant width three on the unchanged paired-packet architecture for r at
least eight and forces the old incoming-carry architecture beyond Bank25
for sufficiently large r. This is a separate certified failure of that
architecture; it is not a proof that every scalar all-r reserve or signed
induction is impossible.

### F.2. Composition rules actually justified

R03-T composes along successive actual cuts because its maps act on the
actual recurrent orbit and the charges are those of the same continued
execution. R03-B's good comparison closes EXACTLY in one rotated period;
the RR/LL pair restores U and the padding restores each g-root input.
Therefore arbitrary P repetitions and the padding require no unaccounted
boundary term. Different words/copies use different occurrence IDs.

In the inherited removable-excursion and return-pulse constructions, auxiliary
and repair pools are disjoint by a proved source rule. Negative interference
releases previously assigned units, rather than minting new ones. These are
valid composition mechanisms only on their stated domains.

For arbitrary W, there is no proved disjoint partition paying all divergent
excursions and persistent regions. Local rejoining at some boundaries does
not imply every region rejoins. Repeating W repeats unresolved costs too;
a bounded endpoint error cancels only with an actual equality or after a
separately justified limiting argument. No bounded endpoint error is simply
discarded here. No family of different erased comparisons is billed against
the same original A inventory simultaneously.

### F.3. Failed or unsupported implications

| Candidate | Precise obstruction/status | Consequence for Universal CD |
|---|---|---|
| Erasure closes after the original one period at the original cut. | False in general; inherited recurrence is needed. R03-B's T seed has transient one, whereas its U seed closes immediately. | None. |
| Eventual B periodicity alone makes its start diagonally reachable. | Insufficient. The actual legal original-plus-changed-mode prefix supplies reachability in B.1. | Basic closure is resolved, not quantitative repayment. |
| A cyclic cut transports an erased orbit to the corresponding FULL B state. | False: in R03-B the erased T orbit transports to X0, while the full state is U. | Starting anew is a distinct comparison, not a relabeling. |
| The erased cyclic target word determines a unique recurrent charge, independently of reaching history. | R03-B: the same erased word has reached recurrent prices zero and `2m`. | More comparison choices exist; no favorable universal choice follows. |
| A smaller erased marked core automatically gives a smaller marginal. | R03-B's minimum core `k+2` has marginal `2m`; its other core `k+3` has marginal zero. | Leaf/core selection needs a signed theorem as well as a size theorem. |
| `J<=0`, or `J<=cD`. | Inherited exact return examples and zero-direct persistent families; R03-B's bad seed has D zero and J positive. | These sign rules fail; CD is not refuted. |
| A fixed repair fee per erased occurrence or its local preparation pays all future J. | The inherited six-key/core-nine backbone family has only two omitted zero-double accesses and normalized `J>=2m-2` through arbitrarily many retained accesses. | Continued retained A work or another cumulative law is necessary for that route. |
| Queried-depth interference telescopes because the full pair closes. | The inherited renewal formula retains a cross-key term, including parity transfer. | A genuine sign theorem for the remainder is missing. |
| Marked-leaf or extremal erasure automatically has the desired signed repair. | Leaf erasure controls core size only. R03-B shows an extremal erased key can have a bad seed; the existence of its good leaf seed is family-specific. | No all-source favorable-leaf theorem is proved or refuted. |
| Physically remove an extreme key, then splay the projection. | [SE03/CONTRACTION_NONCOMMUTATION.md](../SE03_NONREJOIN01/SE03_CONTRACTION_NONCOMMUTATION.md) gives different full output shapes after an RL-plus-zig versus an LL double. | Keep-to-DELETE erasure avoids physical removal but still needs a price theorem. |
| Trim to a key interval and invoke a smaller theorem on the resulting splays. | [INTERVAL_PROJECTION_OBSTRUCTION.md](../SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/INTERVAL_PROJECTION_OBSTRUCTION.md) gives different endpoints and event pairing. Its recorded replay-pending qualification is retained. | This projection fails, not all induction mechanisms. |
| Always use an immediate predecessor's spare units or reuse fixed-width carry. | Sigma defeats predecessor capacity; Gamma_r defeats unchanged fixed-width paired packets. | Those donor architectures fail. |
| R03-B or the old pulse classes prove unrestricted induction. | They have explicit restricted B orbits; R03-B already has elementary direct-safe funding. | This promotion is unsupported. |

No algebraic negative projected cycle is called a negative complete original
source. The existing maximum-debt, positive discrepancy-sum, rotation-distance,
interval-count and fixed-summary potential failures retain their exact
restricted scopes. No new potential is introduced in this report.

## G. Final proof-status and resource record

**OUTCOME B — PARTIAL INDUCTION PROGRESS.** The elementary new results are
R03-T, R03-S and R03-B: actual-orbit cyclic transport, legal phase seeding,
and an explicit all-support separation of two reachable erased recurrent
prices, including a zero-marginal restricted support reduction. Their proofs
are complete free-term and deterministic-map arguments above. They have been
checked analytically here; no separate machine, external or formal audit is
claimed. The source identities inherited from P are clearly separated from
the new U-seeded RR/LL pair and right-vine extension.

The universal source-complete signed repayment/selection theorem is still
missing. Thus `forall r>=6, CD(r)=>CD(r+1)`, unrestricted Universal CD and
its stated downstream consequences remain OPEN. This report is the Step 01
research deliverable, not a successful completion certificate for the
ultimate universal theorem.

All new filesystem writes are confined to this previously nonexistent
Route 03 directory. Historical source artifacts, states, physical IDs,
source periods, g1, fE, h0, prior full assignments, R1–R4 and Bank25 are
unchanged. No output from concurrent Routes 01/02 is assumed or edited;
no C01–C09 campaign or Bank25 construction is restarted.

There were zero new source queries, splay-engine calls, semantic row replays,
state/shape/mask searches, experiments, solver runs, potential constructions
or imports/execution of research programs. File discovery, reading, writing
this report and SHA256 publication checks are metadata operations. Existing
source rows in historical audit JSON were read as existing evidence, not
reexecuted. No claim of new computational verification is based on them.

The latest inspected compatibility gate records cumulative global CPU
`6392.953125/7200`, symbolic `2451.21875/2640`, independent
`740.359375/750`, and queries `3050330/3100000`. Those historical ledger
values are quoted, not installed, reset or presented as a live aggregate
including other running routes. No semantic/proof-computation process was
launched here, and no permission to use the other routes' remaining budgets
is inferred. Metadata follows the inherited metadata-only exclusion.

### Analytic checks on the new claims

* Period/orbit direction: the erased W map is `v∘u`; the rotated map is
  `u∘v`. The injectivity proof uses bijectivity ONLY on a recurrent cycle.
* Cost transport: U_p equals U_0 in its complete starting B state, so their
  entire charge words match; a transient state is not substituted.
* New U seed: expanding the parent-first RR formula gives G1; its inverse
  LL gives exactly U with L0–L3 and R restored. Both pre-depths are two.
* Bad seed: the first erased x uses RL then a zig at actual depth three;
  its later x/g accesses are actual child zigs. Zero charge is never
  misreported as zero pre-depth.
* Support: k+3 full genuine labels become k+2 retained genuine labels.
  The physical separator s and the erased p remain present in both raw
  B skeletons. Neither has been physically removed.
* Reachability: each seed follows its own legal prefix from the permitted
  original diagonal. The good seed's prefix ends at a FULL U boundary;
  transporting the bad seed ends at X0 instead.
* Arbitrary populations: every named rotation acts only on displayed keys;
  each gap BST is moved whole. Increasing/decreasing padding words are
  literal inverse zig sequences, not an auxiliary tree operation.
* General A histories: no B argument requires A=B or an A identity on P.
  Original complete A closure is explicitly retained as a hypothesis.
* Novelty/scope: direct-safe funding of the displayed B orbit is acknowledged;
  the result concerns erasure-state choice and does not pay arbitrary W.
