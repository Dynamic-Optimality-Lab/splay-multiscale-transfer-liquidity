"""Human reports from the exact SHARP-02 certificates; no new source search."""
from fractions import Fraction
import sys
from sharp02_common import *

def tree_text(st):
    def f(k):
        if k is None:return '-'
        a,b=st['children'][str(k)]
        return str(k) if a is None and b is None else f'{k}({f(a)},{f(b)})'
    return f(st['root'])

with Run(sys.argv[1] if len(sys.argv)>1 else 'write_reports_v001',limit=30) as run:
    hall=read(BASE/'SHARP02_HALL_RESULTS.json');cert=hall['principal_counterexample'];l=read(BASE/'SHARP02_MINIMAL_SOURCE_LEDGER.json')
    control=read(BASE/'SHARP02_CONTROL_CERTIFICATES.json');episodes=read(BASE/'SHARP02_ANCESTRY_EPISODES.json')
    src=cert['source'];sm=cert['summary'];g=cert['deficient_gaps'][0]
    word='; '.join(tag+str(x) for tag,x in src['operations'])
    costtable=[]
    for op in l['operations']:
        gap=next((z for z in l['gaps'] if z['KEEP_operation_id']==op['operation_id']),None)
        tail='- | - | - | - | -' if gap is None else ' | '.join(str(gap[k]) for k in ('H','p','q','u','c'))
        costtable.append(f"| {op['operation_id']} | {op['tag']}{op['target']} | {op['a']} | {op['q']} | {tail} |")
    gainrows=[]
    for unit in cert['all_eligible_units']['16']:
        own=next(gg for gg in l['gaps'] if gg['gap_index']==unit['gap_index'])
        gainrows.append(f"| {unit['id']} | {unit['created_ancestor']} -> 9 | {own['gap_index']} | {own['H']} | {min(own['q'],2*own['p'])} | {own['c']} | reserved |")
    ep=next(z for z in episodes['sources'] if z['source']==src['name']);eprows=[]
    for rel in sorted(ep['relations'],key=lambda z:z['ancestor']):
        ref=rel['positive_gap_references'][0]
        gains=[e['id'] for e in rel['changes'] if e['actor']=='A' and e['truth_after']]
        eprows.append(f"| {rel['ancestor']} -> 9 | {ref['last_A_loss']} | {gains} | {ref['B_relation_loss_in_consuming_KEEP']} | yes |")
    c15table=[]
    for z in control['C15']:
        row=z['summary'];ff=z.get('first')
        c15table.append(f"| {z['source']['name']} | {row['n']} | {row['A']} | {row['Q']} | {row['U']} | {('-' if ff is None else ff['unmatched'])} | {z['all']['unmatched']} |")
    rect=hall['inherited_reconstruction']['sources'];positive=sum(z['summary']['U']>0 for z in rect)
    tokentable='\n'.join(f"| {mode} | {sum(z['token_models'][mode]['unmatched']>0 for z in rect)} |" for mode in ('outermost','innermost','extra_double'))
    report=r'''# SHARP-02 — nonlocal ancestry conservation

Date: 2026-11-10, Asia/Karachi. **Final verdict: TARGETED REFUTATION, Type II.**

The exact SHARP-HALL hypothesis with SHARP-01's chronological baseline reservation
is FALSE. A complete ten-key, seventeen-operation source has one excess unit and
NO eligible remaining unit, despite 47 units of total remaining capacity. All six
actual eligible A recreations exist but are baseline-reserved. One legitimate
within-gap reservation swap repairs the source. Universal Q_B<=2A remains OPEN;
the counterexample has A=35,Q_B=24 and is not a sharp-theorem counterexample.

## 1. Original source/theorem scope and provenance

Repository: `C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2`.
Branch `coarse-double-branch`, HEAD `6d532b2c795c0778f57d8023b23b5fedfc48b010`.
Execute SHARP-02 only. All writes are confined here. SHARP-01's complete delivery
manifest is checked byte-for-byte before use; the original reports, ledgers,
physical oracle, immutable reference and source words are pinned in
`SHARP02_INPUT_HASHES.json`. Source and owner passages of Pair Access, S/SET,
BB-02, CD6-TRANSFER, RG01/RG04, Campaign 14/15 and research rules retain their
actual scopes. Previously read mathematical text is reused only at matching
bytes. No historical certificate is promoted to new external/formal certification.
No EXP-01/02 or D5/D6 campaign is reopened.

A and B contain EVERY physical key of their fixed finite ordered universe.
KEEP splays A then B; DELETE splays only A and removes no key. Both COMPLETE
labelled trees return. Legal reaching prefixes establish admissibility but provide
no period capacity. Costs are original ceil(d_A/2) StepEv and floor(d_B/2)
KEEP doubles. B terminal zigs remain in the trajectory but are not double demands.
An A zig has one real rotation and a virtual counting companion. Preserve
R_A=2A-V_A and D_B=B_1+2B_2+Z_1=P_A-N_A. The ten-key witness satisfies
R_A=60,V_A=10,D_B=P_A=55,N_A=0,Z_B=9. Its 117 real A/B rotations are
independently reconstructed with immutable trees.

## 2. Exact inherited SHARP-01 identity

For every original cyclic KEEP gap, including B-root identities and every
intervening DELETE, use H=A(gap), p=ceil(initial d_A(x)/2), q=floor(initial
d_B(x)/2), u=(q-2p)_+, c=2H-min(q,2p). The original root-necessity bound
p<=H is retained. Then u-c=q-2H, and a KEEP-bearing complete source has
Q_B-2A=sum u-sum c. The algebra is inherited, not new conservation.

No KEEP means Q_B=0 and no KEEP partition; the empty gap sum is NOT equated
to -2A. A=0 implies K_B=Q_B=0. No ratio divides by zero. All cost and
Hall computations use integers; reported cost ratios are reduced fractions.

## 3. Frozen actual-unit reservation and eligibility

Each gap has 2H named original accounting units, in chronological StepEv/bit
order. Reserve exactly the first min(q,2p); the remaining c units each have
capacity one. A virtual unit names its original zig and shares that zig's real
rotation witness. It is not a second rotation or SET change.

For positive gap i, x_i is its next KEEP target and Y_i consists of the STRICT
physical B ancestors of x_i absent from its A ancestor path at gap start. An
edge to an unreserved unit exists exactly when the attached actual A rotation
CREATES y->x_i for some y in Y_i. Every genuine recreation in the ONE cyclic
period is eligible regardless of its displayed chronological position. A
repeated reference never creates another unit. No temporal-proximity edge or
unrelated donor is added.

The search oracle keeps all physical keys and literal rotations. Its costs,
every unit identity, real/virtual status, created ancestry and both reserved/all
adjacency sets agree with the frozen SHARP-01 ledger on all 79 sources. Full
important witnesses are subsequently checked by the frozen pointer oracle,
the original separate immutable-frame replay and a further immutable primitive
reconstruction. No projected pair is accepted as a physical source.

## 4. Independent reconstruction of inherited controls

All 79 complete sources and 25,807 operations reproduce. The broad fixed-unit
graph is feasible on all of them; @POSITIVE@ have positive demand. The minimum
NONEMPTY Hall margin in that corpus is +6, on `warmed_random_13`. Vacuous
zero-demand sources contribute no Hall-margin evidence.

The known C15 r7/r8 first-return obstructions reproduce with NEW eligibility
construction from complete relation histories, not just copied flow answers.
Every primitive of the four unreflected owner/zero controls is independently
checked; full copied ledgers and immutable A geometries are in `controls/`.
The r7 deep gap has H=p=1,q=6,u=4,c=0 and first-return neighbor units
A(18,2,0), A(18,2,1) [virtual], A(21,1,1): capacity three, deficiency one.
r8 gives deficiency two. All recreations repair those historical cases.

| Control | physical keys | A | Q_B | U | first-return unmatched | all-recreation unmatched |
|---|---:|---:|---:|---:|---:|---:|
@C15@

The new r=10,12,16,24,32 rows use the literal Gamma_r C_run,r formula;
they are complete prefix-free physical periods, independently checked. The
unbounded historical zero-run theorem retains its original scope and unfinished
owner-seal qualification. Its owner map and old audit allowance are untouched.
H/W same-gap and same-target obstructions remain validation controls, not new claims.

## 5. Broad versus physically tokenized demand

There is a useful UNIVERSAL local path identity. For u>0 let a=d_A(x),b=d_B(x),
Xonly=Anc_A(x) minus Anc_B(x), epsilon_A=2p-a and epsilon_B=b-2q. Then

    |Y| = 2p+2u+epsilon_A+epsilon_B+|Xonly|,
    epsilon_A,epsilon_B in {0,1}, hence |Y|>=2p+2u>=2u+2.

Proof: at a post-KEEP gap start both roots coincide. A positive u target is
different, so p>=1. Set cardinality gives |Y|-|Xonly|=b-a. Substitute
q=2p+u, b=2q+epsilon_B and a=2p-epsilon_A. All ancestors are actual
physical keys, so no contracted vertex is counted. The new counterexample
attains the lower bound: p=u=1, a=2,b=6, Xonly empty and |Y|=4.

Thus at least u distinct explanatory ancestors can always be chosen in physical
path order. Model A keeps broad gap eligibility. Model B assigns each unit
either the u outermost or u innermost B-only ancestors, with only its own
pair's recreation eligible. A third diagnostic uses one B-only pivot of each
actual double after ordinal 2p, if such a pivot exists. On the 79-source corpus:

| Token restriction | sources with unmatched demand |
|---|---:|
@TOKENS@

Exact token Hall certificates and original source words are exported. These
failures refute the specified token models, not existence of every possible
tokenization. The universal path identity alone supplies no capacity theorem.

An especially transparent positional obstruction occurs in the NEW source's
final KEEP 9. Its actual B doubles are RL on (8,10,9), RR on (6,7,9), and
RR on (2,5,9). The arithmetic excess is the one double after ordinal 2p=2,
but both of that double's old ancestors 2,5 are COMMON A/B ancestors. The
four B-only ancestors occurred in the earlier two doubles. Consequently
"every arithmetic excess double contains a B-only old pivot" is FALSE even
before testing its matching. Distinct ancestral explanations exist; that
particular ordinal explanation does not.

## 6. Targeted source-generation strategy

The exact search uses seed 20261111, recurrent transformations of COMPLETE
pairs (maximum 32 word iterations), targeted mutations of tight eligible
rotation operations, independently sampled periodic words/diagonals and
controlled suffix removal from the known C15 family. Transients are explicit
reaching prefixes and never period capacity. Word deletion/key-universe
minimization creates NEW complete sources and rechecks closure; it does not
compute costs on a projected fragment of an old source.

The first search proposes 453 words, encounters 30 duplicate complete periods,
and evaluates 423 distinct candidate periods: 214 positive-demand and 209
zero-demand. It stops at its FIRST fixed-Hall failure, proposal 452. A second
bounded run reproduces the same raw counterexample BYTE-EXACTLY and records
every candidate's exact costs, ratios and nonempty-cut result in
`SHARP02_SEARCH_LOG_v002.jsonl`. The repetitions are not counted as new discoveries.
This is targeted mutation, not CD(7) state enumeration or an exhaustive theorem test.

Greedy deletion and fresh-universe construction reduce the 15-key, 50-operation
raw obstruction to ten keys and seventeen operations after 103 trials. No
globally shortest source or smallest possible physical population is claimed.
All 148 exported sources, including the 79 inherited ones, selected tight
sources, counterexamples, parameter controls and cuts, have complete words,
initial pairs and reachability provenance. The 32 selected search witnesses
are independently replayed; unsaved candidate histories regenerate from the
deterministic driver and their recorded hashes.

## 7. Hall-tight and Hall-deficient measurements

The main hardness metric is min over NONEMPTY D of |N(D)|-sum_D u. The
implementation obtains this exactly by forcing each demand node in turn onto
the source side of a min-cut network. Identical resource neighborhoods may
be grouped with their exact integer multiplicities; no capacity changes.
The network implementation also passes 480 independent brute-subset tests,
covering fixed reservation and optimized per-gap reservation.

| Source | A | Q_B | U | C | Q_B/A | U/C | tight nonempty margin |
|---|---:|---:|---:|---:|---|---|---:|
| inherited warmed_random_13 | 65 | 30 | 1 | 101 | 6/13 | 1/101 | 6 |
| search proposal 349 | 80 | 43 | 1 | 118 | 43/80 | 1/118 | 0 |
| first obstruction, proposal 452 | 74 | 44 | 1 | 105 | 22/37 | 1/105 | -1 |
| minimized principal source | 35 | 24 | 1 | 47 | 24/35 | 1/47 | -1 |
| largest measured Q_B/A, proposal 43 | 169 | 182 | 21 | 177 | 14/13 | 7/59 | 63 |

The last row is an independently replayed, 47-key recurrent C15-derived
control. High Q_B/A and Hall tightness are different phenomena. The failing
source has large GLOBAL slack but zero eligible remaining neighbors. No
tested source has Q_B>2A. Zero-demand cases retain exact scalar data but
do not dominate the margin comparison.

## 8. Exact new principal counterexample

Let X={1,...,10} and start A=B=T, with EMPTY reaching prefix, where
`v(L,R)` denotes the full BST, a bare number a leaf and `-` an empty slot:

    T = 9(5(2(1,3(-,4)),7(6,8)),10).

Execute the COMPLETE original period

    @WORD@

DELETE 9 at operation 13 splays 9 in A; the key remains present. Both full
trees return exactly to T at operation 17. This is itself an admissible common
diagonal. An independently checkable optional right-vine reaching prefix is
also exported; its cost is excluded and unnecessary for the period proof.

| op | original request | a_t | q_t | H of ending KEEP gap | p | q | u | c |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
@COSTS@

The DELETE's cost is included in the gap ending at KEEP 1, operation 14.
The sums are A=35,Q_B=24,U=1,C=47, Q_B-2A=U-C=-46. All 16 KEEPs are
genuine; every key is visited, S=X, and K_B=16<=35.

The sole excess is gap 16, final KEEP 9. Its COMPLETE pre-gap pair is:

    A = @PREA@
    B = @PREB@

Thus the actual paths are A: 2,5,9 and B: 2,5,6,7,8,10,9.
H=p=1,q=3,u=1,c=0 and Y={6,7,8,10}. The full final A/B splay states
are both T. The first two B doubles process 8,10 and 6,7; the last processes
2,5. Applying those literal RL/RR/RR formulas returns B to the displayed T,
while A returns by one RR double on 2,5,9. Full earlier states, exact real
rotations, original SET signs and unit geometries are exported in the principal
ledger and immutable-geometry certificate.

## 9. Reservation and nonlocal exchange results

The following are ALL accounting units whose actual A rotations recreate a
relevant y->9 anywhere in the complete period. Every one is REAL, so this
failure cannot be blamed on mishandling a virtual zig companion.

| actual unit | created pair | gap | H | baseline units reserved | remaining c | status |
|---|---|---:|---:|---:|---:|---|
@GAINS@

There are no other such A gains. All six units occur among the first min(q,2p)
units of their respective gaps. Therefore the one-node demand set {gap16}
has weight one and N(D)=empty. The minimum cut has capacity zero; maximum
matched demand is zero; minimum-cardinality deficient subset size is one.
This REFUTES the precise fixed-reservation SHARP-HALL claim.

An alternative exact reservation repairs it without changing any eligibility:
in gap 2 release A(2,1,1) from baseline, reserve A(2,2,0) instead, and fund
the excess with A(2,1,1). Both are actual real units in that SAME gap. Baseline
cardinality remains two, capacity remains two, and the excess unit really
creates 8->9. The other 23? No: there are 23 baseline demands TOTAL; exactly
ONE of their owners changes, B(2,2). All other 22 baseline owners stay fixed.
The exported full 24-demand injection checks every actual B double and uses
24 distinct original A counting units.

This is **Type II**, a reservation counterexample. It is NOT a refutation of
all possible restoration reservations and is NOT Type III. No old C14/C15
allocator is supplied on this new ten-target source. The swap proves a legal
change of the exploratory baseline convention; it does not override an
external lock. C14's finite owner-exchange algebra cannot create missing
source supply or preserve an incompatible frozen unit by assumption.

There is a useful exact FINITE exchange formulation. Put ALL A units in the
graph and cap the units selected from gap j at c_j. A matching in this
partition-capacity network is equivalent to some reservation of exactly
min(q_j,2p_j) units per gap: complete the selected units to a c_j-element
free set and reserve its complement. The converse is immediate. Equivalently,
the cut capacity for a demand set is

    R(D)=sum_j min(c_j, number of ALL eligible units in gap j adjacent to D).

The network certifies this finite formulation, not R(D)>=sum_D u on every
physical source. On the principal singleton R(D)=6, so optimized matching
succeeds. A generic swap preserves protected assignments only when its new
reserved unit is not already protected/used and the released unit is not
externally locked. Those conditions hold for this declared exploratory swap.

## 10. Complete ancestry-episode lifecycle

`SHARP02_ANCESTRY_EPISODES.json` reconstructs complete chronological A/B
truth-change streams for every relevant pair on all 79 inherited sources and
both new raw/minimized counterexamples: 81 sources, 3,099 relation streams.
It records every gain/loss, all later recreations, the real rotation and
reservation status, cyclic absence episodes and discrepancy births. Each
individual A and B gain count equals its loss count around its full period.
Several records referring to one rotation do not multiply that rotation's units.

The principal source has the following four histories; all gains shown occur
earlier in the displayed word and later on the cyclic lift after the demand:

| pair | last A loss before demand | ALL A recreations in the period | B losses at consuming KEEP | A absence spans seam? |
|---|---|---|---|---|
@EPISODES@

All four relevant last A losses occur during DELETE 9, a single A access
costing three. B freezes during that operation. Its descendants then retain
the relevant B-only ancestry until the consuming KEEP, with all intervening
physical transfers recorded. All four pairs ARE recreated by A; none is a
never-recreated exception. There is only ONE positive demand, so simultaneous
competition between different demand nodes is not the cause. Every available
recreation has instead been removed by baseline reservation.

A second finite physical repair makes the distinction explicit: A(13,1,1)
is an UNRESERVED real unit in gap 13 which DESTROYS 8->9 while B still has
that relation. Sending the one excess to that actual origin-loss unit preserves
ALL 23 original chronological baseline owners. This is a genuine source event,
not an arbitrary donor, but it is NOT a recreation and therefore lies outside
the refuted graph. `SHARP02_ORIGIN_LOSS_REPAIR.json` exports its full injection.
No universal origin-loss or combined loss/gain conservation theorem is asserted.

## 11. Strongest new invariant and arbitrary-size obstruction family

The local path identity in Section 5 is proved universally, but it is not
a compensation theorem. The strongest new global conclusion is a PARAMETRIC
REFUTATION of the frozen Hall rule.

For any integer r>=1 and any finite BST H of new keys greater than 10, attach
the complete H at T's empty right slot of key 10. Start both actors at this
full common diagonal and execute the seventeen-operation word r times.
All original target paths and rotations are unchanged: no target is inside H,
so every primitive carries it as a complete off-path component. Its internal
geometry never changes. Full old-tree closure restores its unique >10
attachment slot, so BOTH enlarged labelled trees close exactly.

No added key becomes an ancestor of an old target. The relevant Y sets,
StepEv/bit inventories and chronological reservations therefore repeat exactly.
For copy j, IDs get actual operation offset 17(j-1); no previous-copy unit
is minted again. The complete exact formulas are

    A=35r, Q_B=24r, U=r, C=47r, Q_B-2A=-46r.

The r excess gaps are all isolated in the fixed all-recreation graph: every
one of their 6r physical gain units is reserved. Their full set has Hall
deficiency r. The single swap from Section 9 in each copy gives distinct
eligible units and an explicit repaired 24r-demand injection. Reflection
preserves the conclusion. This proves a false matching rule with arbitrary
physical population, arbitrary repeated copies and exact cyclic closure;
it does not create a sharp scalar counterexample.

Fourteen finite parameter/reflection controls check r=1,2,3,7 and untouched
tails through 257 extra keys, plus both reflected examples. All seventeen
operation cuts of the base cycle preserve the failure; the cut after DELETE
9 starts at different A/B roots and still closes with a legal excluded prefix.
The proof for arbitrary H and r is the literal hanger/copy argument above,
not extrapolation of those finite values.

## 12. Source-derived cut theorem: exact obstruction

A cut theorem using the frozen eligibility cannot hold even for ONE positive
excess gap. On this source there is no other positive gap that a nonempty
closure operation could add: the only nonempty demand collection is already
deficient. Laminarity, nonmerging, distant recreation or ancestor birth/death
conservation cannot rescue that same false graph without changing its
reservation or eligibility.

The first obstruction is completely identified: source-valid physical gains
exist, but every associated unit is baseline-owned under the stipulated rule.
There is no seam error, no missing A recreation and no multi-demand occupancy
collision. All 47 remaining units are physically real/virtual inventory, yet
none meets the principal recreation predicate. The within-gap swap and the
alternative origin-loss edge show two different exact ways to escape that
restriction on this source. Neither supplies a universal replacement proof.

If optimized reservation is investigated later, the missing physical theorem
would concern the simultaneous rank capacity R(D) above, including arbitrary
shared episodes and actual unit quotas. Its existence is OPEN. This report
does not rename that assertion as proof progress or start a second campaign
after the principal model has been refuted.

## 13. Connection to coefficient-two Coarse-Double

A universal saturating fixed Hall matching WOULD imply sum u<=sum c and then
Q_B<=2A by the inherited identity. The counterexample invalidates the proposed
universal matching premise, not that implication and not its scalar conclusion.
The base source instead has 24<=70; the whole parameter family has 24r<=70r.
The exact repaired injections are certificates only for those named sources.

No tested source violates coefficient two. No universal 2A proof, relaxed
constant, R6 reclassification, Dynamic Optimality conclusion, CD(7) enumeration
or abstract bootstrap is produced. The central conservation question survives
through allocation/eligibility choices that the stipulated frozen rule cannot handle.

## 14. Explicit comparison with SHARP-01 failures

Same-gap compensation remains false on H, same-target restriction remains
false, and first-return C15 failures remain deficiency one/two. Five scalar
potentials stay refuted; none is resurrected or fitted here. SHARP-02 adds an
exact refutation of the broad ALL-return fixed-reservation rule itself.

Unlike first-return C15, the principal source cannot be repaired merely by
looking further around the SAME fixed remaining-unit graph: all six gains
have already been included. It requires changing which units baseline owns,
or admitting a different actual physical event. Root-normalized excess is
not pinned to an individually expensive B double's own pair of old ancestors,
as the positional counterexample shows. The failed old statements and their
original scopes are retained throughout.

## 15. Reproducibility, resources and verification limits

The seven requested deliverables and all isolated scripts/certificates are
present. `SHARP02_REPRODUCTION.md` gives standalone checking of the principal
source and full in-repository reconstruction. All 148 exported sources have
physical-execution SHA-256 values. The exact per-candidate search log includes
nonempty Hall margins, assignments, graph edges and named incident units for
positive cases; empty cases explicitly have no nonempty margin.

Verification is same-agent distinct implementations, not another person,
formal proof assistant or external peer review. The search is bounded and
not exhaustive. Source minimality is greedy/local. The optimized-reservation
model and the origin-loss enlargement are NOT proved universally. No old
common-owner policy or Bank25 schedule is certified by this new source map.

Every numerical pipeline invocation has a versioned receipt with process CPU,
wall time, peak working set, parameters and status, written in finally and
checkpointed during longer work. Earlier versions/failed-or-running statuses
are not relabelled PASS. Final receipt aggregation is in
`SHARP02_RESOURCE_SUMMARY.json`; static authoring/read-only inspection probes
are outside that numerical-process sum, which is not claimed as total session
CPU. SHARP-01's original missing CPU/peak memory stays explicitly missing.
One attempted report regeneration was rejected at startup because its receipt
name already existed; no data processing or source replay occurred. Its command
wall time and unavailable CPU/peak values are recorded separately in
`SHARP02_STARTUP_REJECTIONS.json`, not hidden in the measured stage sum.
No historical research or audit balance is reset or borrowed. The new 900-second
cumulative numerical ceiling and 1-GiB process ceiling are respected.

Historical files and Git are read-only. New writes stay in SHARP-02. Exact
hash/branch/HEAD/diff checks distinguish any concurrent unrelated work from
this campaign. No external mathematical theorem is needed to validate the
new finite obstruction; the parametric lifting uses literal complete-tree rigidity.

## 16. Final mathematical verdict

**TARGETED REFUTATION — Type II reservation obstruction.** SHARP-HALL as
stated with chronological baseline reservation is false. Its deficiency is
proved on an exact complete prefix-free source and extends to an arbitrary-size
physical/copy family. A single allowed reservation exchange repairs it; a
different origin-loss eligibility also repairs the particular source without
moving its baseline owners. Neither repair is promoted to a universal law.

BEFORE: all-recreation fixed-unit matching passed 79 sources. RESULT: those
controls reproduce, targeted Hall search finds a real obstruction, independent
replay confirms it, and the physical reservation cause is isolated. AFTER:
the fixed Hall route is eliminated, the universal coefficient-two theorem
remains open, and no later campaign is executed. Net proof advancement is
strategic elimination of this exact certificate mechanism, not proof of Universal CD.
'''
    rep={'@POSITIVE@':str(positive),'@WORD@':word,'@C15@':'\n'.join(c15table),'@TOKENS@':tokentable,
         '@COSTS@':'\n'.join(costtable),'@GAINS@':'\n'.join(gainrows),'@EPISODES@':'\n'.join(eprows),
         '@PREA@':tree_text(l['states'][g['start'][0]]),'@PREB@':tree_text(l['states'][g['start'][1]])}
    for key,value in rep.items():report=report.replace(key,value)
    report=report.replace('The other 23? No: there are 23 baseline demands TOTAL; exactly','There are 23 baseline demands in total; exactly')
    (BASE/'SHARP02_DISCOVERY_REPORT.md').write_text(report,encoding='utf-8')
    ledger=r'''# SHARP-02 theorem and refutation ledger

Date 2026-11-10, Asia/Karachi. Verdict TARGETED REFUTATION, Type II.

## T02-1 — exact physical path identity

**PROVED — UNIVERSAL, local path statement; not compensation.** On every positive
canonical excess gap, strict physical ancestor sets obey

    |AncB(x) minus AncA(x)|
      =2p+2u+(2p-dA)+(dB-2q)+|AncA(x) minus AncB(x)|.

Proof: subtract path cardinalities b-a=|Y|-|Xonly| and substitute q=2p+u.
The two parity terms lie in {0,1}. Both post-KEEP roots coincide, so u>0
implies x is different and p>=1. Thus |Y|>=2p+2u>=2u+2. Choosing u
outermost or innermost Y ancestors gives a canonical distinct tokenization.
The ten-key counterexample attains equality. This does not force distinct
eligible free A units: both specific token matchings and the broad model can fail.

## T02-2 — principal SHARP-HALL

**REFUTED — EXACT.** Full common diagonal

    T=9(5(2(1,3(-,4)),7(6,8)),10)

and W=`K2 K8 K4 K7 K2 K10 K8 K1 K4 K5 K6 K3 D9 K1 K5 K2 K9`.
Both complete trees return; no prefix is required. A=35,Q=24,U=1,C=47.
Final gap H=p=1,q=3,Y={6,7,8,10}; its one demand has no neighbor among
remaining chronological units. ALL six eligible physical gains are reserved.
One-node Hall deficiency one is a complete minimum-cut certificate. See
`SHARP02_PRINCIPAL_COUNTERCERTIFICATE.json` and the full immutable geometries.
Scope refuted: exactly the fixed chronological reservation plus all-A-gain
eligibility. Universal coefficient-two CD itself is NOT refuted.

## T02-3 — extra-double positional token lemma

**REFUTED — EXACT.** In the same final gap, the doubles after the initial two
have old grandparent/parent (2,5). Both are common A/B ancestors, so that
arithmetic excess double has no B-only pivot. The B-only pairs appear in
earlier doubles. This does not refute all source-defined ancestral tokenizations.
The outermost/innermost model failures on the saved W family are separately
certified in `SHARP02_CONTROL_CERTIFICATES.json`.

## T02-4 — finite reservation exchange / partition-capacity equivalence

**PROVED — finite combinatorial statement, NOT source supply.** For any actual
unit inventory partitioned into gap groups U_j of size 2H_j, let c_j be the
required free cardinality. A matching using all units with at most c_j selected
from group j exists iff some reservation of 2H_j-c_j units per group leaves
a saturating eligible matching.

Proof: given the quota-respecting matching, extend its used units in each group
to a c_j-element free set and reserve the complement. Conversely a matching
in any such free set respects the group quota. A change from an old free set
can be implemented by same-group swaps of wanted reserved units with unused
old free units. Protect previously used/locked units explicitly; no such unit
can be swapped contrary to its contract. When a quota is full, an augmentation
needs a legal reallocation; existence is not implied by raw inventory.

For a demand set D, its partition rank is
R(D)=sum_j min(c_j,|N_all(D) intersect U_j|). The associated finite cut theorem
is the exact min-cut of the unit/group network. It does NOT prove
R(D)>=sum_D u_i for every original physical source. That global assertion
remains OPEN. C14's actual locked-owner theorem is not extended to ten-target
sources, and no old map is modified.

On the explicit source, free A(2,1,1) and reserve A(2,2,0) instead. The
released real unit creates 8->9 and pays the excess. Baseline cardinalities
and all other baseline owners stay unchanged. The full 24-demand injection
is in `SHARP02_REPAIRED_SOURCE_INJECTION.json`.

## T02-5 — arbitrary-population, arbitrary-copy refutation family

**PROVED — PARAMETRIC INTERMEDIATE-LEMMA REFUTATION.** Append any complete
physical hanger on keys >10 in T's empty key-10 right slot and repeat W r>=1
times. No old target path enters the hanger. Literal rotations carry it
intact; old-tree closure returns its unique ordered attachment. All complete
trees therefore close. Relevant pairs, original paths, costs and reservations
are unchanged and replicate with actual operation offset 17(j-1).

Hence A=35r,Q=24r,U=r,C=47r,Delta=-46r. Every excess node has no fixed-
reservation neighbor, so the r-node set has deficiency r. The exact swap in
each copy gives distinct restored gain units and a repaired injection. This
works for arbitrary hanger size/shape and reflection. Finite controls through
257 extra keys and all seventeen base seams corroborate the primitive proof.
It does not establish a divergent Q/A family or a new unrestricted CD proof.

## T02-6 — actual A-origin-loss repair

**FINITE-EXACT, scoped alternative eligibility only.** A(13,1,1) is an
unreserved real unit destroying 8->9 while B retains it. Using that unit for
B(17,3) preserves all 23 original baseline assignments and gives 24 distinct
accounting-unit owners. See `SHARP02_ORIGIN_LOSS_REPAIR.json`. The unit is
ineligible under the principal GAIN rule. No universal loss/gain compensation,
bounded episode congestion, frozen-owner extension or Bank25 result follows.

## Preserved inherited results and remaining debt

BB-02 identity and p<=H remain unchanged. C15 first-return deficiencies one/two,
same-gap H failure, same-target failures and SHARP-01 potential refutations
are reproduced or retained at their exact scopes. C15's old final seal stays
pending. Neither pure pair gain/loss conservation nor total global C guarantees
usable remaining units, as T02-2 shows even for a singleton demand set.

Universal Q_B<=2A remains OPEN. A source-uniform alternative allocation or
different physical compensation law is required. No unproved Hall assertion,
optimized flow on finite data or this constructed source family is promoted
to a universal sharp theorem. Stop after SHARP-02.
'''
    (BASE/'SHARP02_THEOREM_LEDGER.md').write_text(ledger,encoding='utf-8')
    repro=r'''# SHARP-02 reproduction

Current exact corpus provenance: branch `coarse-double-branch`, commit
`6d532b2c795c0778f57d8023b23b5fedfc48b010`. Standard-library Python only.
All writes/caches/logs stay here. Run with `-B`; do not execute a script from
SHARP-01 that would rewrite an old receipt. The four vendored SHARP-01 modules
are byte-identical read-only snapshots used by SHARP-02 scripts.

## Standalone principal-counterexample check

The artifact bundle contains everything needed for the new counterexample.
From its extracted directory run:

```powershell
python -B sharp02_standalone_verify.py local_replay_v001
```

Choose a fresh receipt name if repeating. This checks the exact full source,
alternate legal right-vine prefix, both complete endpoints, all 117 primitive
rotations/ancestry changes, original gap costs, ALL eligible named gain units,
fixed Hall failure and explicit repaired maps. It uses a full pointer replay,
an immutable-frame replay and immutable primitive reconstruction. No historical
repo input or installed dependency is needed for this principal check.

`SHARP02_MINIMAL_SOURCE_LEDGER.json` resolves every tree reference in its
`states` table. `SHARP02_MINIMAL_INDEPENDENT_GEOMETRY.json` contains complete
pre/post A trees for each real A rotation. The principal certificate lists
every eligible unit, not just the selected one. Original source identity is
(source name, actor, operation, StepEv, bit); virtual companions are marked.

## Full in-repository reconstruction

Preserve this run. Make a NEW versioned sibling directly under
`DO_RESEARCH_REBOOT`, copy the `*.py` scripts into it, and run there with the
unchanged SHARP-01 directory available beside it:

```powershell
python -B sharp02_common.py
python -B sharp02_reconstruct.py
python -B sharp02_fast.py
python -B sharp02_network_tests.py
python -B sharp02_search.py
python -B sharp02_search.py adversarial_search_v002
python -B sharp02_confirm.py
python -B sharp02_minimize.py
python -B sharp02_certificate.py
python -B sharp02_controls.py
python -B sharp02_episodes.py
python -B sharp02_assemble.py
python -B sharp02_standalone_verify.py independent_replay_v001
python -B sharp02_write_reports.py
python -B sharp02_final_verify.py
```

The two search passes must reproduce proposal 452's same source bytes, costs
and graph. The final driver records all 423 unique complete candidate rows;
the original first-run log recorded only its 214 positive-demand rows. The
authoritative full data are in the v002 log. New timing/peak memory and receipt
names may differ. All numerical results and physical source hashes should agree.
For an exact seeded generator replay, match the Python implementation/version
recorded in `SHARP02_ENVIRONMENT.json`. Direct saved-witness verification uses
only exact operations and does not depend on regenerating the randomized search.
The source minimization is a deterministic local deletion/universe procedure,
not a claim to global source minimality. It returns the 10-key, 17-operation case.

## Exact algorithms and proof checks

Fixed graph resources are original remaining A units after first-min(q,2p)
reservation. Pattern grouping merges ONLY resources with identical demand
neighborhoods, retaining their integer multiplicity and actual-unit catalog.
Integral max-flow gives assignments and deficient cuts. Minimum NONEMPTY Hall
margin is computed by forcing each positive-demand node into the source side
in turn. Cases with zero demand have margin null. Up to 14 demand nodes,
minimum-cardinality deficient sets are also exhaustively checked. Larger
deficient sets are only inclusion-minimized, with that qualification recorded.

Optimized reservation uses ALL original units and a per-gap sink quota c_j.
This is a different exploratory allocation question. The concrete repair swaps
A(2,1,1) with A(2,2,0) within gap 2. The origin-loss repair changes eligibility
instead and preserves every chronological baseline owner. Neither is a proved
universal mechanism or an imported C14/C15 owner certificate.

The numerical pipeline receipts include CPU, wall-clock duration and peak
working set, including repeated versions. Finally blocks persist failures;
longer stages write checkpoints while running. A forced OS termination can
leave an explicitly RUNNING checkpoint, never a fabricated PASS. The new
cumulative ceiling is 900 numerical process CPU seconds, 1 GiB per process,
600 keys and 20,000 operations per period. Search limit is 500 CPU seconds /
50,000 candidates / 32 recurrence iterations, and stops at the first principal
failure. No historical allowance is borrowed/reset. SHARP-01's missing initial
CPU and peak-memory measurements remain missing.

## Artifact map

* `SHARP02_DISCOVERY_REPORT.md`: sixteen-section research report and exact verdict.
* `SHARP02_HALL_RESULTS.json`: reconstructed corpus, exact graphs/cuts, controls and principal result.
* `SHARP02_ANCESTRY_EPISODES.json`: complete relevant cyclic relation streams for 81 sources.
* `SHARP02_SOURCE_WITNESSES.json`: 148 explicit complete source words/states/prefixes and execution hashes.
* `SHARP02_COUNTEREXAMPLE_CERTIFICATES.json`: exact principal, parametric and token obstructions.
* `SHARP02_THEOREM_LEDGER.md`: proofs, refutations, finite exchange scope and open debt.
* `SHARP02_PRINCIPAL_COUNTERCERTIFICATE.json`: full six-unit reservation obstruction.
* `SHARP02_REPAIRED_SOURCE_INJECTION.json`: all 24 original-double owners after the swap.
* `SHARP02_ORIGIN_LOSS_REPAIR.json`: all 24 owners under the separate origin-loss eligibility.
* `controls/`: complete C15 ledgers and independently reconstructed A geometries.
* `SHARP02_INPUT_HASHES.json`, final verification, delivery manifest and `receipts/`: provenance/integrity/resources.

The fixed SHARP-HALL rule is refuted (Type II). Q_B<=2A is not refuted.
The statement that an optimized/expanded physical model works universally is OPEN.
'''
    (BASE/'SHARP02_REPRODUCTION.md').write_text(repro,encoding='utf-8')
    run.check(report_bytes=len(report.encode()),positive_inherited_sources=positive)
    print(json.dumps({'report_bytes':len(report.encode()),'positive_inherited_sources':positive,'sections':16}))
