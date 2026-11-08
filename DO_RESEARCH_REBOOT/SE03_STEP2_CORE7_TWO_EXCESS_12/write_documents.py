"""Publication prose/provenance metadata; mathematical checks are separate phases."""
import hashlib,json,textwrap
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(textwrap.dedent(s).strip()+'\n')
docs={
'SOURCE_SPEC.md':r'''
# Campaign12 — frozen source and theorem

Theorem C7-TWO-SLOT-FUNDING: for every admissible original finite reachable
exactly paired-closed six-genuine-KEEP full-core7 source period Pi, with
EXACTLY TWO physical excess slots on ONE actual aligned interval I,
construct an injective source-eligible fstar:Pstar->Wstar, keeping every
previous full assignment a(d) and common frozen fE owner exactly fixed.
Pstar has size0,1 or2; all three branches are included. See FULL_PROOF.md.

A processes EVERY original present-key access. BF processes every KEEP,
including identities; BE omits only KEEPs of its fixed erased key. DELETE
is A-only, not physical key deletion. Ordinary bottom-up splays give
a_t=ceil(depth_A/2), qF_t=floor(depth_BF/2) on KEEP, qF_t=0 on DELETE.
Terminal zigs are actual events/states, not extra BF-double demands.
U={(t,j,b):1<=j<=a_t,b in{0,1}} and D={(t,k):1<=k<=qF_t} use actual I IDs.

Natural full macros end at genuine BF root changes and include all
intervening original operations. For each e, H_e is actual UNCLIPPED
A work and Q_e full doubles. h0 pairs its first min(Q_e,2H_e) demands
with its own first bits. R=D\dom(h0) is the actual last (Q_e-2H_e)_+
demand slots, not residual roots, donors or a normalized fractional count.
|R|=2 is imposed on aligned I BEFORE dividing any period multiplier L.

C pairs full/erased demands by same occurrence/double ordinal, not equal
rotations. l:C->U is the supplied certified fE pulled back to common full
demands. Campaign10's partial exchange defines a, Pstar=D\dom(a),
Wstar=U\im(a), and the explicit injection alpha:Pstar->R. Definitions and
original archive/retirement rules are unchanged.

The funding policy is the original actual-ID COUNTING-bit/block-cyclic
one with independent complete full receipts followed by the licensed
common-owner exchange. Source matching-terminal semantics stay fixed.
No stricter donor-target-key or arbitrary-fixed-seam causal rule is
introduced. FULL_PROOF sections3–5 certify selected edges jointly;
unused cardinality alone never licenses them.

All source modes, erasures, chart changes, root repeats, private BSTs,
source lengths, orientations, reachability and full-state closure remain
quantified. This lemma is restricted by its stated source class; it
does not redefine original CD or restrict the original global target.
No solver, state coordinate, graph, raw state, midpoint, Bank25 or cap
changes. Old changing-chart normalization stays REFUTED. Step2/CD6 and
Step3 stay OPEN. No arbitrary core7 slot-count campaign is executed.

Authoritative local branch/HEAD and full preexisting worktree inventory
are in entry.json. SOURCE_PROVENANCE.md and dependency_pins.json record
paths, hashes, proof-inspection status and exact inherited scopes. Entry
CPU3415.84375/7200, remaining3784.15625; symbolic66.5/120 and independent
147.96875/300. All cumulative and per-phase caps/reserve remain unchanged.
''',
'CORE7_TWO_SLOT_CLASSIFICATION.md':r'''
# Complete necessary two-slot source classification

Exact closure plus marked-core monotonicity fixes one labeled seven-key
core S throughout BF boundaries. All BF paths stay in S; arbitrary eight
ordered private gaps lift by rotation commutation. After normalization,
one unmarked core label is at role2..6, all remaining six labels marked.

| Unmarked role | Necessary contexts | Genuine edges | Q3 sectors |
|---|---:|---:|---:|
|2|255|1095|34|
|3|269|1189|22|
|4|272|1216|20|
|5|269|1189|22|
|6|255|1095|34|

All429 skeletons/3003 accesses are retained. This covers1320 necessary
contexts/5784 admitted genuine edges, not a claim every graph path is
realizable. Both physical source orientations and every private gap BST
remain. Actual A is unrestricted and never identified with the BF core.

H>=1,Q<=3 imply excess iff H1/Q3, then exactly one slot (t,3). Hence
exactly two slots means two DISTINCT genuine macros. Same-macro slots
are impossible. Each critical macro's immediate predecessor has Q<=1;
distinct critical macros have distinct, noncritical predecessors. Thus
critical macros cannot be adjacent in cyclic genuine-macro order, nor
can their terminal occurrences be consecutive original operations.
Their two [predecessor,critical] blocks have disjoint macro indices.

Targets may be the same or different; no target-equality restriction
appears in the construction. It uses actual IDs, so both target cases
are covered whenever source-valid. Charts may agree or differ; hits,
misses and arbitrary successive mark switches require no separate debt
formula. Erased shape/core and persistent BF/BE disagreement remain actual.
Different common-lock sectors give zero, one or two residual roots, each
either its own noncommon R slot or a blocked root anchored at common R.

DELETEs/zero-A accesses/nongenuine KEEPs belong to their literal macros.
They cannot create an H0 genuine macro, duplicate a bit, add a second
slot to one macro or change BF between the actual consecutive genuine
boundaries. Arbitrary A helpers merely contribute their true event IDs
to H. The forced predecessor supply makes Splus>=2; zero/one raw surplus
are impossible. Locked availability is resolved by the exact owner exchange.

The necessary shape grammar is reproduced in geometry_certificate.json
and independently derived again. FULL_PROOF gives the universal source
partition argument without finite realization, source-word length or
private-population assumptions. There are no omitted core6/core8 branches
inside the frozen core7 domain, and no Q5 pairing at this core size.
''',
'TWO_ANCHOR_PROVENANCE.md':r'''
# Literal two-anchor provenance

R={r1,r2}, r_i=(t_i,3), consists of the third actual BF double of each
actual H1/Q3 macro, at two distinct source occurrences t_i in aligned I.
The slot is a DEMAND. It is never an A-credit unit or a fictitious debt.

The inherited partial h0/l construction gives

    Pstar = ((D\C) intersect R) disjoint_union blocked_roots.

For the first part alpha(p)=p. For a blocked root p, follow its original
h0/l path to its missing common owner r in C intersect R and set
alpha(p)=r. Injectivity of h0,l prevents roots meeting, so blocked owners
are distinct. The two images lie in R\C and R intersect C respectively;
alpha is injective. A residual root can lie in an otherwise safe packet;
its anchor stays the actual excess double. Pstar need not equal R.

Two residuals therefore have distinct source demand anchors; this alone
does not prove donor separation. NEW source supply uses the actual cyclic
predecessor b_i of each critical macro. Equal b_i would force equal
critical macro, so their original operation/event inventories differ.
No extracted one-slot subperiod or abstract splice is invoked.

physical_receipts2.json retains every source word/tree/operation, chart,
macro occurrence list, each actual R, seed (t,j,b), all six erased runs,
logical common owners, blocked paths, alpha and final receipts. The
independent checker recomputes those IDs from original rotations. Logical
test maps are explicitly not numerical realizations of the sealed fE;
preservation of actual supplied fE is a parametric proof.
''',
'PHYSICAL_BIT_INVENTORY.md':r'''
# Exact physical inventory and certified joint neighborhoods

On the ONE fixed actual aligned I, U is every original (t,j,b), b0/1.
Different descriptions are the same unit iff all three actual IDs agree.
A0 has no units. BF doubles are D with separate (t,k) demand identifiers;
BE demand ordinals are tagged by their execution before common pairing.

| Authoritative class | Definition/status |
|---|---|
|Locked common owners|im(l), values fixed and contained in im(a)|
|Other already paid full owners|im(a)\im(l), old successful path endpoints|
|Available full bits|Wstar=U\im(a), no availability inferred from chart names|
|Original E-unused bits|U_E, archived exact original event IDs|
|Retired E-only claims|fE(N), old alternative-full allocation retirement only|
|Source seeds v_i|first h0-unused own bit of b_i; distinct but may be locked|
|Certified donors u_p|free endpoints of complete h against fixed a|
|Other available bits|no extra eligibility asserted without a source receipt|

The disjoint equalities U=im(l) union U_E union fE(N) and
U=im(a) union Wstar preserve the original retirement authority. Old
successful endpoints belong to im(h0); therefore each v_i outside that
image is either common-locked or free in the ACTUAL partial construction.
Neither v_i is blindly assumed usable. Wstar is not redefined after tests.

As exact accounting, |U|-|D|=Splus-2, so
|Wstar|=Splus-2+|Pstar|. These are CHECKS, not the proof of supply or
eligibility. Source predecessor geometry constructs h without the desired
inequality; disjoint owner paths construct the eligible free endpoints.

Let J(h,l) be the licensed full/common exchange receipt. Every new pair
(p,u_p) appears in J(h,l), every old partial path is identical, and all
new terminals are jointly distinct in Wstar. This supplies a certified
SUBRELATION of the original N_I(p), rather than an unverified exhaustive
static eligibility graph. For two roots, selected singleton neighborhoods
are distinct; thus their original neighborhoods satisfy the two-demand
Hall inequalities as a CONSEQUENCE. If eligibility is exchange-dependent,
J is the simultaneous feasibility witness; independent edge legality is
never substituted for joint compatibility.

No chart difference, normalized debt, comparison-only event, copied
timestamp or fE/gE substitution enters the physical inventory.
''',
'CAMPAIGN11_TRANSFER_AUDIT.md':r'''
# Exact inheritance from the one-slot theorem

| Component | Original scope | Campaign12 use |
|---|---|---|
|Full labeled core constancy/pruning|all actual closed fixed-support histories|same actual S; no new source restriction|
|H>=1,Q<=3|natural core7 full macros|applied to each original macro|
|Incoming Hamiltonian Q<=1|ordinary same-Score splay, any Score count/free hangers|applied to actual predecessor of each Q3|
|Whole one-slot positive supply|period with exactly one R|NOT invoked as a period theorem|
|First positive-macro donor rule|one-slot h completion|replaced by each critical macro's own predecessor bit|
|One-hole endpoint argument|one missing root|new disjoint multi-root proof supplied|
|Original common-path stability|completion equal h0 on old paths|reproved for two missing edges, same C|
|Both-endpoint period transport|one actual recurrent aligned period|applied simultaneously to all receipts|
|Old global chart normalization|REFUTED|not a premise|

The new bridge is cyclic predecessor injectivity plus disjoint actual
macro inventories. No one-slot theorem is applied to an extracted interval
that has not been proved a closed admissible one-slot period. Seed bits
are explicit source units and can be initially locked. The new owner
proof runs both residual paths against the SAME fixed a and proves they
cannot meet. It preserves all old successful endpoints, not only common
owners or aggregate demand counts.

All prioritized Campaign11 proofs, final seal2/manifest and resource
checkpoint were inspected. Every manifest/dependency hash was verified.
The full transitive pin set is preserved, including old superseded files
at their historical statuses. No accepted11 source or certificate is edited.
''',
'DONOR_COLLISION_LEDGER.md':r'''
# Complete two-demand collision ledger

N below means the ORIGINAL licensed source neighborhoods; we certify a
jointly feasible subrelation using complete h/l, not an exhaustive guessed
static graph. FULL_PROOF sections2–5 resolve all cases.

| Class | Disposition |
|---|---|
|E1 disjoint nonempty neighborhoods|certified distinct terminal pairs lie in them|
|E2 overlapping with sufficient union|same complete exchange supplies a distinct pair; overlap need not be classified numerically|
|E3 both original neighborhoods singleton same bit|impossible: two disjoint certified terminal edges contradict it|
|E4 one original neighborhood empty|impossible for a residual root: total h and finite injective owner path give a licensed terminal|
|E5 exchange-dependent legality|one complete h/l receipt witnesses all new pairs jointly, all old paths unchanged|
|E6 incompatible period copies|both endpoint IDs transported by one bijection onto fixed I, so no incompatible copy is selected|
|A same raw candidate chosen twice|avoided by explicit distinct predecessor seed selection, then disjoint owner paths|
|B macro aliases give same event|genuine cyclic macro partition disjoint in actual occurrences; equal IDs cannot be two resources|
|C first route consumes second donor|paths computed simultaneously against frozen a are disjoint; sequential addition yields same second endpoint|
|D both seeds locked|follow exact common owners; endpoints, not seeds, are spent; locked values fixed|
|E unused but ineligible spare|not assumed spendable; source stream/transport/common receipt licenses selected terminals|
|F adjacent cyclic copies|rejected outside actual U; no two copies for one physical resource|
|G chart correction consumes supply|all actual full doubles already in D and funded once; potential differences are no physical demand|
|H zero/one Splus|universally excluded by two distinct predecessor spare contributions|
|I private helper changes access|its actual A events remain in H/U; BF free-gap lemma unchanged|
|J individual proofs fail to compose|not used: a complete source h and ONE licensed joint receipt construct both assignments|

The illustrative same-first-free algorithm duplicates a unit on actual
source IDs with logical owner placements. This rejects that heuristic
only; the placements are not asserted to be numerical sealed fE. No
source counterexample to the main theorem or CD(6) is claimed. Historical
Sigma45/46 failure remains REFUTED unchanged at its old local-rule scope.
''',
'SECOND_DONOR_THEOREM.md':r'''
# Source-derived second donor theorem

Let c1,c2 be the distinct critical macros. Their actual predecessors
b1,b2 are distinct and noncritical because incoming Hamiltonian Q<=1.
Select v_i as bit Q(b_i)+1 of b_i's actual own event list. Disjoint macro
occurrence inventories imply v1!=v2 and both outside im(h0). Thus
h=h0 union{r1->v1,r2->v2} is a complete SOURCE-CONSTRUCTED injection.
This is the simultaneous supply theorem; neither a spare count nor
individual one-slot theorem applications substitute for this proof.

For each residual p, follow h through a owners until free. Such a finite
path cannot enter a cycle or meet another missing-root path, because
injectivity forces unique predecessors and missing roots are not paid.
The terminal u_p lies in Wstar. For two roots u1!=u2. In the actual
partial10 interface the complete original h/l exchange preserves every
old successful path, so both endpoints carry licensed source receipts.

Suppose p1 is funded by its certified terminal u1. Since p2's whole path
and terminal were disjoint from p1's path against fixed a, adding p1->u1
does not change p2's path or endpoint. Hence u2 remains unused and legal;
the final map adds both pairs and leaves every previous paid value fixed.
This proves second-donor availability FOR THIS JOINT MECHANISM. It does
not assert any arbitrary individually legal first choice can always be
extended under an unspecified stricter eligibility policy.

Both initial seeds may be locked. The final donors may be nonlocal and
may differ from the initial seeds. Source eligibility follows from the
original common-set receipt, not from permission to use any numeric free
unit. FULL_PROOF gives termination, nonintersection, exact period and
original common-owner licensing without any Hall/CD assumption.
''',
'ZERO_SURPLUS_TWO_SLOT.md':r'''
# Zero and low surplus: source exclusion and owner availability

The unchanged source-defined raw surplus is
Splus=sum_e max(2H_e-Q_e,0). It counts h0-unused own bits, not necessarily
currently free eligible donors. In the TWO-slot class, two distinct
critical macros have two distinct actual predecessors b_i with H>=1,
Q<=1. Each contributes at least one DIFFERENT own spare. Therefore

    Splus >= (2H_b1-Q_b1)+(2H_b2-Q_b2) >=2.

Zero raw surplus and exactly one raw spare are universally IMPOSSIBLE.
This is a new two-slot proof, not an unproved transfer of11's one-slot
zero exclusion. It uses full BF geometry alone; no positive anonymous
helper, A/B convergence or desired total inequality is assumed.

The inherited H1 normal form remains valid: before its sole event A
accesses the old root g; after that event it accesses final marked x.
The word is {Dg,Kg}* Kx or {Dg,Kg}* Dx(Dx)*Kx. If Splus=0 all safe
macros would be H1/Q2, contradicting both forced Q<=1 predecessors.
At Splus=1 at least one of their distinct positive contributions would
still have to be omitted. Thus the source argument already excludes
both candidate regimes without a same-word periodicity theorem.

At Splus>=2, both seed bits can be locked under frozen owners. This
does not license spending locked units or prove they are free: complete
h plus original common exchange yields distinct unused endpoints while
keeping all owners fixed. For Pstar=0 there need be no available full
spare; returning a is valid. For Pstar=1/2 the endpoint construction
proves the required1/2 availability; |Wstar|=Splus-2+|Pstar| is only its
exact inventory check. Marked-event and anonymous-helper supply have
the same original event IDs and no different capacity rule.
''',
'TWO_DEMAND_EXCHANGE.md':r'''
# Simultaneous fixed-owner exchange

Input: actual D,U, original locked common l and partial h0/l map a;
independent source-certified complete injection h agreeing with h0 on
dom(h0). No previous value may be changed. The residual roots are Pstar.

Algorithm: for each p in Pstar against the SAME fixed a, repeat
u=h(d), then d=a^{-1}(u) if u already paid; otherwise save (p,u).
After ALL roots terminate, return a union all saved pairs.

In the demand-owner graph each vertex has at most one predecessor by
injectivity of h and a. Starting roots have no incoming edge because
they lie outside dom(a). Entered cycles and merging paths would force
predecessors back to a paid starting root or two equal roots, impossible.
Finite D and total h imply termination. Paths and their terminal units
are disjoint, so all saved units are different and outside im(a).
All previous a values, not just common owners, remain literally fixed.

Eligibility bridge: each old successful h0/l path avoids R and remains
IDENTICAL in complete h/l on the EXACT original common set C. Blocked
paths continue and previously missing noncommon R roots start. Complete
exchange disjointness forbids any new terminal equaling an old endpoint.
Thus licensed full h/l is exactly the old a plus these residual pairs.
The all-paid walks compute those same new terminals. This proves joint
source legality without enlarged auxiliary claims, guessed fE, altered
eligibility, assumed cardinality or any reassignment of old paid roots.

The algebraic path proof has no fixed two-root bound and is sufficient
for any finite residual set IF a complete independent source h is supplied.
It does not independently supply arbitrary-support h. Here the actual
two-slot predecessor theorem supplies it. The public allocator rejects
more than two residuals/slots so the executed campaign remains bounded.
''',
'PERIOD_CUT_VALIDITY.md':r'''
# Two receipts on one legal actual source period

Keep the inherited recurrent aligned I=[a,a+T),T=L*N and the fixed fE
maximum-debt auxiliary cut. Reachability uses the histories' actual
reaching prefixes; prefixes/transients are NEVER a funding pool.

The independent full construction chooses a separate full cut J just
before b1. Since the two [b_i,c_i] blocks are disjoint, neither starts
with a missing carry at that cut. Each selected v_i is minted in b_i
before its critical demand in c_i. h0 pays all other doubles using own
actual events, with A replay before B at a KEEP. Carry starts/ends0,
at most1 between macros; working<=4. This is a physical receipt, not
a numerical telescoping inequality or virtual two-unit initialization.

For t in J map to t if t<a+T, otherwise t-T. Apply to BOTH donor and
demand endpoints, preserving local event/double/bit ordinals. Periodic
actual states certify that this is a bijection onto one I. Both seeds
and all routed terminals then belong to that same actual I; no earlier
or future copy is simultaneously spent. Old fE/a are already on I and
are unchanged. |R|=2 is physical on I, never divided before construction.

The resulting final exchange uses the inherited block/cyclic receipt.
A later-in-I bit may fund an earlier demand under that interface; no
stronger native online/key-matching claim is added. Only original legal
cuts are used; choosing a full cut does not overwrite the Step1 cut.

Mandatory original Gamma26 replay: A34,QF30,QE24; forced D12=0,D13=2
exclude maximum cut12 and there are no genuine auxiliary cuts inside
the two blocks. Actual event(10,3) is auxiliary event4, outside the
first-three selector, and its two bits pay(9,1),(13,5). Occurrences9,10,13
lie in the same permitted actual copy. Both temporal directions retain
their original authority. historical10_gamma_period_ownership_audit.json
recomputes this and Sigma45/46/reflections preserve their old failures.

Independent new receipts check2904 cut transports over48 actual erased
source reports. These audits support the bijective proof, not replace it.
''',
'SOURCE_LIFTING.md':r'''
# Universal private-source, chart and length coverage

Every actual closed full history fixes its labeled marked ancestor core
by monotonicity around the exact closed period. Thus full BF paths never
enter a Score-free private BST. Each ordinary rotation commutes with
substitution of arbitrary ordered BSTs into the eight gaps. The LL/RR
permanent-fork argument is a free-tree induction, valid for ANY hangers
and Score count; no finite/private population bound is inferred.

No pruning is imposed on actual A. It executes EVERY original helper
and DELETE access. Their actual StepEv indices contribute to H and U.
H>=1 and complete actual unit lists suffice even with arbitrarily large
private inventories or many positive anonymous operations. The chosen
predecessor spare is its first h0-unused actual unit, which may be from
any original event; no private-node independence assumption is needed.

Order-preserving normalization gives all five unmarked roles. Reflection
reverses Score order/gaps, with a separate RR fork proof as well as LL.
The proof does not assume all actual accesses use same-side doubles:
only the extremal target of a Hamiltonian DESTINATION has that property.
Mixed actual critical paths are retained.

Recent-five charts and the erased execution are not used to infer full
source geometry. All actual chart changes, erasure choices and full/erased
disagreement enter the literal C/P/N ledger. Every actual full double,
including a chart correction's physical demand, lies in D exactly once.
Neither chart representative choice nor old normalized M3 debt is used.

The argument takes the original finite cyclic macro list of ANY length;
cyclic predecessor is injective with no length bound. Owner walks terminate
by finite injectivity, not a bounded search depth. Source/cut reachability
and full A/BF/BE closure remain actual hypotheses. No reverse realization,
abstract concatenation or equality-of-root closure is assumed. Hence the
proof quantifies all admitted lengths/private BSTs/helpers/orientations.
''',
'UNIFORM_TWO_SLOT_INTERFACE.md':r'''
# Gate U12 — reusable source nonoverlap/exchange interface

U12.1 source invariant: each critical H1/Q3 at core7 has an actual
Q<=1,H>=1 predecessor, giving its actual own-unused unit Q+1. Cyclic
predecessor is injective on distinct critical indices, and no predecessor
is critical. Distinct source inventories therefore give distinct seed
bits, not just distinct demand anchors. The source consequence is verified
here for exactly TWO critical macros on the actual aligned I.

U12.2 generalized exchange state: (actual D,U,C,l,h0,a,h) on one legal I,
with a the partial h0/l exchange and independent complete source h extending
h0. The licensed complete h/l receipt defines a jointly feasible donor
subrelation for Pstar. If static neighborhoods apply, these certified edges
belong to original N. If legality is exchange-dependent, use this receipt
as the joint-state witness; no guessed static graph is complete by decree.

U12.3 sufficient general theorem: for ANY finite such actual-ID system,
complete h plus licensed common exchange yields disjoint free endpoints
for all Pstar while keeping EVERY old successful assignment fixed. Proof:
old successful paths are unchanged when h extends h0; new paths cannot
meet or enter a cycle by injectivity. This proves |N(S)|>=|S| for all
subsets S as a CONSEQUENCE whenever the licensed static interpretation
applies. It assumes neither a matching nor a desired global inequality.

U12.4 two to three: the path termination/disjointness proof itself works
for any finite number of missing roots. Small384 three-hole MAP controls
audit this algebra only; no three-slot source campaign is executed. For
a concrete source domain one must still construct the independently valid
h and its period receipt. Pairwise compatibility by itself is insufficient:
three abstract demands each adjacent to the same two units satisfy every
two-demand test but fail the triple Hall condition. This is not a source
counterexample. Our sufficient theorem uses complete h, not that shortcut.

U12.5 dependencies: exchange is independent of support size/core size,
ordinary rotations and debt widths once actual source receipts/owners
are supplied. The present SUPPLY uses maximum depth6 on seven Scores,
one-unit H1Q3 deficit and distinct preceding macros. Larger cores can
have multiple slots per packet; Sigma45/46 refutes blanket adjacent supply
there. Arbitrary-r source supply/capacity and legal disjoint charging are
still unproved. The inherited r-4 width-growth issue remains unchanged;
no uniform width-two potential or support descent is inferred.

Gate U12 status: U-B — a correct general sufficient owner-exchange theorem
is proved, but arbitrary-support source hypotheses remain OPEN. The
executed source theorem stays exactly two-slot core7, not unrestricted
core7 or Step3. Campaign13 must first determine the legitimate slot-count
range, then assemble/verify source nonoverlap and common-owner preservation
for the whole actual core7 domain. It is not automatically executed here.
''',
'FINAL_VERDICT.md':r'''
# OUTCOME A — C7-TWO-SLOT-FUNDING universally proved

For every Pi in the declared original six-genuine-KEEP full-core7 class
with exactly TWO physical excess slots on ONE actual aligned period,
the inherited Pstar (size0,1 or2) admits a jointly source-eligible
injection fstar:Pstar->Wstar. Every previous full assignment and common
frozen fE owner remains exactly fixed. All physical demands are paid once.

The decisive construction is source-derived: two critical H1/Q3 macros
have two distinct actual Q<=1 predecessors, whose separate original
event inventories supply two different h0-unused bits. These complete h0
independently of fE. Disjoint terminating owner paths yield free endpoints.
The ORIGINAL complete h/l exchange leaves every old successful path
unchanged, thereby licensing the final simultaneous extension. No Hall
premise, numerical CD inequality or invented auxiliary allocation is used.

Zero/one raw-surplus regimes are impossible. Root repeats, DELETE-origin
events, arbitrary helpers/private BSTs, every chart and erasure, both
orientations and actual source-period transport are covered symbolically.
The theorem uses the inherited counting-bit/block-cyclic interface, with
no new strict fixed-seam online or terminal-key donor claim.

Independent source/ownership checking uses a distinct immutable splay
engine and backwards ownership traversal by the SAME agent. It is not
external peer review or formal proof-assistant certification. Failed
checker drafts are preserved, superseded and fully charged; none is
treated as evidence for Outcome A. Accepted checks and exact provenance
appear in INDEPENDENT_AUDIT.md, seal_audit.json and campaign_manifest.json.

Consequence: complete core7 exactly-TWO-slot physical funding, complementing
Campaign11's exactly-ONE-slot theorem. QF<=2A holds on this subclass by
the constructed injection. Unrestricted core7, other cores, full CD(6),
Step2, Step3, Universal CD and Dynamic Optimality remain OPEN. No claim
that either larger theorem was proved follows from this campaign.

Gate U12: U-B, general sufficient exchange proved; arbitrary-support
source supply open. Next is Campaign13 COMPLETE CORE7 RESIDUAL-SLOT
FUNDING, beginning with actual possible slot counts and a global source
donor injection. That successor is not executed in Campaign12.
''',
'CHECKPOINT.md':r'''
# Campaign12 sealed checkpoint — exact two-slot interface closed

Outcome A: C7-TWO-SLOT-FUNDING at the frozen original source/ownership/
actual-period scope. FULL_PROOF.md and final seal/manifest are authority.
No source case remains inside this declared two-slot theorem.

Keep Campaign11 one-slot theorem, actual R/Pstar/Wstar/alpha definitions,
all old a values and frozen common fE owners. New proved interface:

1. Two critical H1Q3 macros have distinct noncritical actual predecessors
   Q<=1,H>=1; their actual own-unused bits Q+1 are distinct outside im(h0).
2. h=h0 plus both excess pairs is independent full source funding, with
   disjoint predecessor/critical blocks, carry<=1, working<=4 and empty
   carry endpoints at its full cut. Both IDs transport to fixed aligned I.
3. Simultaneous fixed-a owner paths do not merge or enter cycles. Complete
   original h/l exchange leaves all old successful partial paths identical;
   new pairs are jointly licensed while EVERY previous value remains fixed.
4. Zero/one raw Splus are impossible; locked seeds are handled by exchange.

Smallest NEXT task: CAMPAIGN13 — COMPLETE CORE7 RESIDUAL-SLOT FUNDING.
First determine the actual possible/maximal slot-count range on legitimate
aligned periods (count before dividing L). Do not assume an unbounded
problem or a small maximum. Establish source nonoverlap and receipt/owner
coverage for ALL legitimate residual roots, using U12's arbitrary finite
exchange lemma only after independent source h is available. Do not
replace global compatibility by pairwise Hall conditions. No successor
source campaign has been executed or promoted here.

Gate U12=U-B. Full core7/other cores, Step2/CD6, Step3, Universal CD and
Dynamic Optimality remain OPEN. Old chart normalization stays REFUTED.
06–09 results and Sigma/Gamma controls keep their exact inherited scopes.
R1–R4, Bank25, graph/solver/raw states, shared midpoint, all original
operations and caps persist. No solver/controller state was added.

Branch coarse-double-branch, HEAD8c378d49283b3738b18e7175886772a98025e4e9;
tracked tree clean and old untracked research preserved. Only new12 files
written. Read resources_checkpoint.json for exact cumulative CPU (no
renewal/reset), all failed and accepted run charges and remaining group
allowances; read dependency_revalidation.json for frozen byte integrity.
''',
'IAGS_CLOSURE.md':r'''
# IAGS reconstruction and net advancement

BEFORE: Campaign11 closed one physical excess slot; two-slot simultaneous
donor supply and fixed-owner compatibility were OPEN. Main frozen target
was C7-TWO-SLOT-FUNDING, not complete core7/CD6/Step2.

Freeze preserved original domain and policies. Inherit used only true-scope
Hamiltonian/source/period/anchor facts. Alter changed the sufficient seed
rule from first-positive selection to each actual critical predecessor.
Recurse split source separation, simultaneous owner paths and same-period
licensing. Create proved cyclic-predecessor nonoverlap and disjoint finite
owner-path lemmas. Reconstruct completed the ORIGINAL h/l exchange, with
all previous path values fixed. Close follows accepted independent checks
and L1–L16 assembly, not finite SAT success or absent counterexamples.

RESULT: complete source theorem on zero/one/two residuals in actual two-slot
periods. Source Splus>=2, independent h and licensed simultaneous extension
are proved without a new existence premise. Failed checker drafts were
syntax/test-coverage/representation issues, preserved and charged; no
source counterexample or load-bearing inherited error was found.

AFTER: exactly the declared two-slot core7 obligation is deleted. No new
mathematical assumption is introduced. General sufficient exchange U-B
is available, arbitrary-support supply remains open. NET advancement is
genuine original restricted source-domain coverage. Campaign13 remains
the next unexecuted scope; no arbitrary core7/Step2 promotion is made.

Immutable R1–R4 retain exact original target/closure, weighted product and
source semantics, frozen solver/architecture/observables/caps, and evidence
discipline. The separate four research-methodology pre-execution tests
are not substituted for that contract. Bank25 remains25.
'''
}
for n,s in docs.items():write(n,s)
e=read('entry.json');pins=read('dependency_pins.json');by={v['path']:v for v in pins['pins']}
sources=[
('ORIGINAL_PIPELINE.md','SOURCE DEFINITION; original present-key costs/model inspected'),
('RESEARCH_RULES.md','SOURCE RULES; exact proof/status/scope discipline inspected'),
('06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md','R1–R4 SOURCE CONTRACT; literal frozen architecture inspected'),
('SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','PROVED special five-key/core9 explicit bank at exact scope; inspected, no selector extension'),
('SE03_STEP1_FUND01/SOURCE_IDS_AND_CYCLIC_CUT.md','PROVED aligned period/canonical legal cut; inspected'),
('SE03_STEP1_FUND01/SIGNED_CANCELLATION.md','PROVED exact common/full-only/E-only retirement; inspected'),
('SE03_STEP2_REPAY01/IMPROVED_FULL_DEBT_TARGET.md','CONDITIONAL debt; ONLY PROVED complete-full/common-owner exchange used; inspected'),
('SE03_STEP2_REPAY01/PACKET_PERIOD_TRANSPORT.md','PROVED both-endpoint actual period bijection; inspected'),
('SE03_STEP2_REPAY01/CYCLIC_DONOR_ID_AUDIT.md','PROVED Gamma legal-copy interface; inspected/fresh historical replay'),
('SE03_STEP2_FULL_FUNDING_CLOSURE_10/RESIDUAL_SLOT_THEOREM.md','PROVED general actual-ID partial map/anchors; full proof inspected'),
('SE03_STEP2_FULL_FUNDING_CLOSURE_10/PHYSICAL_DONOR_LEDGER.md','PROVED exact inventory; old OPEN supply not assumed'),
('SE03_STEP2_FULL_FUNDING_CLOSURE_10/FROZEN_FE_AUDIT.md','PROVED ownership interface at true scope; inspected'),
('SE03_STEP2_FULL_FUNDING_CLOSURE_10/SIX_KEY_SOURCE_PARTITION.md','PROVED necessary core/macro partition; inspected'),
('SE03_STEP2_FULL_FUNDING_CLOSURE_10/CHART_BOUNDARY_CORRECTIONS.md','PROVED identities; no chart-sign repayment imported'),
('SE03_STEP2_FULL_FUNDING_CLOSURE_10/PERIOD_CUT_VALIDITY.md','PROVED transport component; inspected'),
('SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py','IMMUTABLE exact partial/common algorithm; inspected and reverse-audited'),
('SE03_STEP2_FULL_FUNDING_CLOSURE_10/deficient_source_schemas.json','EXACT source-family data, inspected and replayed; not universal evidence'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/FULL_PROOF.md','PROVED one-slot only; local structural facts independently re-established'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/CHECKPOINT.md','SEALED one-slot checkpoint; inspected'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/FINAL_VERDICT.md','OUTCOME A at exact ONE-slot scope; inspected'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/CORE7_ONE_SLOT_CLASSIFICATION.md','PROVED necessary source grammar; inspected/regenerated'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/ZERO_SURPLUS_RIGIDITY.md','PROVED H1 necessary normal form; inspected, no convergence assumption'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/ZERO_SURPLUS_DONOR.md','PROVED incoming-path free-tree lemma; inspected and reproved'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/NONLOCAL_DONOR_LEMMA.md','PROVED original-common receipt interface; inspected, simultaneous bridge supplied'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/PHYSICAL_SINGLE_SLOT_INJECTION.md','PROVED single-slot construction; inspected, not applied wholesale'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/AVAILABLE_BIT_INVENTORY.md','PROVED one-slot inventory, exact definitions reused'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/POSITIVE_SURPLUS_PROOF.md','PROVED one-slot source stream, new two-block stream supplied'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/INDEPENDENT_AUDIT.md','Accepted same-agent distinct implementation scope; inspected'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/ADVERSARIAL_AUDIT.md','Accepted limitations/counterrules, inspected'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/UNIFORM_SINGLE_SLOT_INTERFACE.md','U11 component proved/general U OPEN; inspected, U12 separately scoped'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/seal_audit2.json','AUTHORITATIVE final11 seal; inspected/hashed'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/resources_checkpoint.json','AUTHORITATIVE3415.84375 cumulative CPU, entry exact'),
('SE03_STEP2_CORE7_SINGLE_EXCESS_11/campaign_manifest.json','AUTHORITATIVE109-file manifest; every hash verified')]
lines=['# Exact local provenance and dependency status','',f"Branch {e['branch']}; HEAD {e['head']}. Tracked tree clean at entry;",
    'entry.json preserves the exact full untracked inventory. Authoritative local',
    f"state used; no remote snapshot substituted. All{len(pins['pins'])} transitive pins",
    'plus external directives verified at entry and revalidated at final seal.',
    'The table distinguishes direct proof inspection from transitive byte checks.',
    'Other inherited pinned proofs are reused at their sealed scopes, not all',
    'independently rederived in Campaign12. No missing critical premise remains.','',
    '| Repository-relative exact path | Status / proof inspection / use | SHA256 |','|---|---|---|']
for rel,status in sources:
    path='DO_RESEARCH_REBOOT/'+rel;assert path in by,path
    lines.append('|'+path+'|'+status+'|'+by[path]['sha256']+'|')
for path in ('DO_RESEARCH_REBOOT/SE03_STEP2_COLD_NEG2_01/source_model.py','python/independent/splay.py'):
    lines.append('|'+path+'|IMMUTABLE primary/independent source rotations inspected, no legacy depth+1 proxy used|'+by[path]['sha256']+'|')
lines+=['','External original IAGS/R1–R4 and current Campaign12 directive are pinned',
    'by exact absolute path/hash in dependency_pins.json. The refuted changing-',
    'chart Hamiltonian normalization remains REFUTED; only its independently',
    'reproved structural fork lemma is inherited. CD5/M3/Step1 and06–09 stay',
    'at their sealed scopes. Campaign10 full funding stays UNRESOLVED.','']
write('SOURCE_PROVENANCE.md','\n'.join(lines))
print(json.dumps({'status':'DOCUMENTS_AND_PROVENANCE_WRITTEN','documents':len(docs)+1,'pins':len(pins['pins'])}))
