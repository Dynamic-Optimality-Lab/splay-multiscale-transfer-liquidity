"""Render the research deliverables from the verified finite artifacts."""
import json
from pathlib import Path
from fractions import Fraction
from collections import Counter
BASE=Path(__file__).resolve().parent
r=json.loads((BASE/'SHARP01_RESULTS.json').read_text())
unit=json.loads((BASE/'SHARP01_PHYSICAL_INCIDENCE.json').read_text())
receipt=json.loads((BASE/'SHARP01_RUN_RECEIPT.json').read_text())
ind=json.loads((BASE/'SHARP01_INDEPENDENT_VERIFICATION.json').read_text())
cert=json.loads((BASE/'SHARP01_COUNTERCERTIFICATES.json').read_text())
index=json.loads((BASE/'SHARP01_GAP_LEDGER.json').read_text())['ledgers']
summ=r['sources'];byname={s['name']:s for s in summ}
gaps=[];prep=base=simult=neutraluc=0;missing=0
for item in index:
    l=json.loads((BASE/item['path']).read_text())
    gaps.extend(l['gaps'])
    for g in l['gaps']:
        prep+=g['preparation_capacity'];base+=g['baseline_capacity']
        simult+=g['u']>0 and g['c']>0;neutraluc+=g['u']==g['c'] and g['u']>0
    for h in next(z for z in r['incidence'] if z['source']==item['name'])['positive_gap_histories']:
        missing+=sum(z['first_A_recreation_after_KEEP'] is None for z in h['B_only_ancestor_histories'])
best=max((s for s in summ if s['A']),key=lambda s:Fraction(s['Q'],s['A']))
table='\n'.join(f"| {s['name']} | {s['n']} | {s['operations']} | {s['A']} | {s['Q']} | {s['U']} | {s['C']} | {s['Delta']} | {s['Q_over_A'] or 'undefined'} |" for s in summ)
flows=[]
for rule in r['incidence'][0]['rules']:
    fails=sum(not s['rules'][rule]['success'] for s in r['incidence'])
    flows.append(f'| gap / {rule} | {len(summ)-fails}/{len(summ)} | {fails} |')
for rule in unit['sources'][0]['rules']:
    fails=sum(not s['rules'][rule]['success'] for s in unit['sources'])
    flows.append(f'| unit / {rule} | {len(summ)-fails}/{len(summ)} | {fails} |')
flowtable='\n'.join(flows)
pt='\n'.join(f"| {c['template']} | {c['source']}, gap {c['gap_index']} | {c['d']} | {c['Phi_start']} | {c['Phi_end']} | {c['delta']} |" for c in cert['potential_refutations'])
report=r'''# SHARP-01 — exact 2A conservation discovery report

Date: 2026-11-10, Asia/Karachi. **Verdict: TARGETED REFUTATION of intermediate rules.**
Universal coefficient-two Coarse-Double remains OPEN. No tested complete source has
Q_B>2A. The campaign establishes exact, replayable obstructions to same-gap repayment,
same-target funding, a specified first-restoration rule, and five scalar geometric
potential templates. A more permissive actual-ancestry-restoration incidence survives
this finite corpus, with its universal Hall obligation unproved.

## 1. Exact original source scope and provenance

Repository: `C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2`.
Branch `coarse-double-branch`; HEAD `6d532b2c795c0778f57d8023b23b5fedfc48b010`.
Execution is SHARP-01 only. All task writes are inside this directory. No old
owner map, source record, report, engine, resource controller or Git history is edited.

A performs ordinary bottom-up splay on every KEEP and DELETE; B performs KEEP
only. DELETE removes no physical key. Complete labelled trees individually return,
and every saved starting pair is checked against its explicit prefix from a common
diagonal. Prefix costs are excluded. Private ancestors, full physical fringes,
root repeats, terminal zigs and all middle subtrees are retained.

Costs are a_t=ceil(edge-depth_A/2), q_t=floor(edge-depth_B/2) on KEEP and zero
on DELETE. An A StepEv has two counting units; a terminal zig has one real bit
and one virtual companion. Virtual companions are never real rotations or SET changes.
The reference implementation's legacy depth-plus-one cost helper is not used.

`SHARP01_INPUT_MANIFEST.json` pins the historical inputs. Core definitions and
family constructions were read directly, including BB-02, BB-01, CD6-TRANSFER,
G0–D6, RG01/RG04, Pair Access, S/SET, TF2 and Campaign 14/15 material. The
historical proofs and their transitive certificate libraries are not newly certified.
The completed concurrent Global Boundary Reuse report was also inspected: its
all-R6 result remains BLOCKED, and it supplies no missing sharp conservation law.
The subsequently completed EXP-01 discovery report was read in full. It proves
a restricted return-normalized scan bound R6_return<=6 C_seq A, relative to its
inherited inputs; it leaves the original G witness and the unrestricted residual
open. Its new experiments are not attributed to SHARP, and that relaxed partial
bound does not establish the exact coefficient-two target.
No literature-dependent theorem is needed for the new numerical countercertificates.

## 2. Inherited BB-02 identity and gap classification

List EVERY cyclic KEEP occurrence, including B-root identities. A gap begins just
after the preceding KEEP and ends at the current KEEP, including every DELETE.
Use the actual complete post-KEEP starting state to define p=ceil(d_A(x)/2),
q=floor(d_B(x)/2), H=A(gap), u=(q-2p)_+ and c=2H-min(q,2p).
The inherited minimum-rooting theorem gives p<=H; the oracle checks this exactly.

The inherited identity is u-c=q-2H, hence U-C=Q_B-2A when a KEEP exists.
This is a verification target, not the campaign's discovery. The useful capacity
split is c=2(H-p)+(2p-q)_+. For excess gaps only the first summand remains.
For nonexcess gaps the baseline discount can also contribute. Neutral q=2H
does not imply u=c=0 or unchanged physical geometry.

With no KEEP there is no cyclic KEEP partition: gaps are empty, Q_B=0, and
the A work is explicitly recorded as unpartitioned. The empty sums are NOT
misreported as U-C=-2A in that case. A=0 implies K_B=Q_B=0; ratios are null.

## 3. Independently checked physical oracle

`sharp01_oracle.py` uses full parent/child pointer trees, without importing an old
engine. `sharp01_tuple_reference.py` is a pinned snapshot of the repository's
different immutable-frame implementation. `sharp01_validate.py` independently
replays prefixes and periods, compares every complete post-operation A/B state,
StepEv case sequence and exact cost, and reconstructs gaps by a different
last-KEEP unwrapping algorithm.

All 79 complete sources and 25,807 original operation transitions pass this check.
This is same-agent distinct-implementation verification, not an external auditor
or a formal proof kernel. Literal rotation ancestry and edge tables are also checked
on all 222 possible primitive rotations of all BST shapes with at most five keys.
The 288 primitive ancestry changes of the C15 Hall witness are reconstructed
separately with immutable subtrees.

## 4. Complete cyclic gap accounting and artifact format

`SHARP01_GAP_LEDGER.json` is the index of 79 chronological per-source JSON
ledgers in `ledgers/`, with SHA-256 for each. It is a logical complete ledger,
split into files to keep individual sources inspectable. Each file contains:

* a deduplicated table of COMPLETE labelled trees; start/end A/B references resolve there;
* every original operation, its pre/post pair, A/B search paths, depths and costs;
* every gap's original operation/DELETE IDs, preceding/current target, H,p,q,u,c,d;
* all A StepEv, real rotation IDs, B double IDs and terminal-zig IDs;
* each primitive's physical deleted/added edges, external attachment, middle subtree,
  exact ancestry changes, duplicate-suppressed full-carrier SET changes and sign;
* initial path set differences, common prefix, LCA diagnostics and five state features.

All operation IDs are source-local original positions; a globally unique event is
(source name,actor,operation,StepEv,bit). The exact source word and initial pair
are exported in `SHARP01_SOURCE_WITNESSES.json` and again with each ledger.
For every KEEP-bearing source, sum H=A, sum q=Q and U-C=Q-2A are exact integers.

All 34 cuts of H_(1,1), including DELETE-run seams, preserve the multiset of full
gap records after original-ID transport. This test includes physical primitive
records, not only scalar totals. Nine additional representative cyclic replays
cover H_(6,1), W_5, W_star, G, the full-fringe lift, I^3Z, a warmed period and
both C15 seven-key families. Rank reflections and three-copy sources are retained
with fresh occurrence IDs. No seam, prefix or adjacent source copy lends capacity.

## 5. Physical origin of positive excess — an exact parametric obstruction

Consider H_(p,q), N=2^(p+1)(q+1)+1, p,q>=1, from the common right vine.
Its ENTIRE word is D2,...,DN; descend every N,...,1 keeping exactly
N+1-2^j for j=0,...,p; K1,...,KN; K(N-1),...,K1. Both full trees close.

After DELETE preparation and KEEP N, A is the complete left vine. B's actual
RR splay of N has left spine 2,4,...,N-1, each with its physical odd left leaf.
The next KEEP N-1 therefore has A path N,N-1 and B path N,2,4,...,N-1.
Consequently, exactly,

    H=p_i=1, q_i=(N-1)/4,
    u_i=((N-1)/4-2)_+, c_i=0.

For N>=17 its net deficit is positive and unbounded with N. This PROVES that
extra A work in the SAME excess gap cannot universally compensate its excess.
It refutes a local statement, not Universal CD: the full source has A=4(N-1),
and the complete preparation/restoration remains inside it.

In H_(2,1), N=17, original KEEP 16 is operation 18, gap 2:
H=p=1,q=4,u=2,c=0,d=2. The B-only ancestors are 2,4,6,8,10,12,14.
Their last A losses are respectively A(2,1,0),A(4,1,0),...,A(14,1,0),
in the earlier DELETE preparation. The first subsequent A recreations occur at
operations 32,30,28,26,24,22,20. All these physical histories, and the later B
recreations, are exported. The discrepancy is inherited across a KEEP boundary;
it is not manufactured by ignoring DELETEs inside the current gap.

`SHARP01_ANCESTOR_EPISODES.json` additionally reconstructs the actual last birth
and next end of each B-only ancestor discrepancy at every positive-u gap start.
There are 3,884 A-loss references and 20 B-gain references in this dataset,
with duplicate references explicitly retained rather than counted as new work.
For example, in the complete C15 r7 owner source, relation 2->13 becomes
B-only at NEUTRAL B(14,1,0) during the previous KEEP and ends at B(15,6,1).
Thus a previous KEEP's physical rotation can expose the discrepancy; its
immediate origin need not be an A-only DELETE. Every recorded episode closes
consistently on the original complete pair, including wrapping episodes.

B's access removes those old target ancestors while transporting nonempty
middle subtrees. Some global disagreement measures increase during this very
access. A cheap target in A therefore need not consume a monotone scalar amount
of total paired-tree disagreement.

## 6. Physical composition of capacity

The first wrapping H gap includes the entire initial DELETE preparation. Its
H=N-1, p=(N-1)/2 and q=(N-1)/2 give c=3(N-1)/2. Its positive capacity
precedes the displayed positive second gap. The source exhibits nonlocal
preparation and return work; this observation does not reserve that whole
capacity independently for every later discrepancy.

H_(3,1), gap 3, operations D31;K30, is a separate physical case:
H=2,p=1,q=4,u=c=2,d=0. A uses two adjacent zigs where a direct initial
splay of 30 would have needed one StepEv. Its extra work locally covers this
gap's excess, and the complete paired geometry changes substantially. In
contrast, the preceding parametric second gap has no such local capacity.

H-p is not the DELETE cost. Exactly H-p=A_DELETE+(a_final_KEEP-p), and the
last summand may be negative. In `perturb_7_0`, gap 24, a positive DELETE
preparation is followed by H=p=2. Thus even positive DELETE work need not
produce preparation capacity. No scalar c unit is declared a vacant old donor.

Across the finite dataset there are @SIMULT@ gaps with both u,c>0, of which
@NEUTRALUC@ have u=c>0. Preparation and baseline contributions total
@PREP@ and @BASE@ units respectively; these are dataset counts, not universal constants.

## 7. Exact experimental source-family results

All ratios below are reduced rationals. No result is rounded and A=0 is not divided.
Sources include full H/W/W_hit/W_star/W_5/G, repeated short scans, physical
fringe lifts, I^rZ, C15 owner/zero-run histories, warmed periods, reflections,
three-copy controls, 15 seeded perturbations and four seeded recurrent periods.
The maximum physical population is 257. Every complete-source Delta is <=0.

| Source | keys | operations | A | Q_B | U | C | Delta | Q_B/A |
|---|---:|---:|---:|---:|---:|---:|---:|---|
@TABLE@

The largest observed Q_B/A is @BEST@. The corpus is far from testing a ratio
near 2; absence of a violation here is weak evidence for the universal inequality.
The original 65-key G has exact A=323,Q_B=156,U=21,C=511, so its previously
symbolic closing cost is 86. H_(6,1) has A=1024,Q_B=459,U=114,C=1703.
These exact finite measurements do not certify the historical R6 predicates.

## 8. Source-derived incidence rules

Demand nodes are gaps of weight u, capacity nodes gaps of weight c. A demand's
fingerprint is its target x and the physical B-only ancestors Y at gap start.
Each graph is independently specified before testing, rather than completed by
looking at total U,C:

1. `shared_endpoints`: the capacity gap has an actual A rotation involving x or Y.
2. `A_recreation`: some A rotation in that capacity gap creates y->x for y in Y.
3. `first_A_recreation`: restrict to the first such A recreation of each pair
   after the demanding KEEP, cyclically within the ONE period.
4. `same_target`: the capacity gap's KEEP target equals x, a narrow control.

Gap-level edges can conceal which cost unit performs that restoration. Therefore
a second check reserves the FIRST min(q,2p) chronological counting units in
each gap and exposes exactly c remaining named units. A real unit is eligible
only if its actual rotation creates y->x. A zig's virtual companion is tied to
its one real rotation, explicitly marked virtual. Each unit has capacity ONE.
Both all-recreation and first-recreation unit graphs are tested. This reservation
is a new exploratory convention, never an inherited frozen-owner assignment.

`SHARP01_PHYSICAL_INCIDENCE.json` exports each strict unit edge's demand,
capacity-unit ID, physical ancestor and exact creating rotation. It also gives
integer flows, assignments, demand subsets and Hall deficiencies. Every used
unit occurs at most once in a flow. Gap-level shared-endpoint edges remain
broad diagnostics; passing them is not a conservation proof.

| Physical rule | complete-source flow passes | failures |
|---|---:|---:|
@FLOWTABLE@

Zero-demand cases are included as vacuous passes. The permissive unit rule
passes every nonvacuous case too. That finite success supplies neither an
all-source eligibility theorem nor a uniform bound on prospective congestion.

## 9. Exact congestion and matching failures

`same_target` already fails on H_(3,1): total demand 9, matched demand 7.
One deficient demand gap suffices. Later repayment need not use the expensive
target again as its own capacity-gap target.

More significantly, the first-recreation GAP graph passes all 79 cases while
its UNIT graph fails 12. In the complete C15 seven-key owner source,
operation 15 is KEEP 13, gap 13. Its A path is 1,4,13 and its B path the
full right vine 1,...,13. Thus H=p=1,q=6,u=4,c=0,d=4.
Under the specified chronological reservation, first physical recreations
reach exactly these eligible capacity units:

    A(18,2,0), A(18,2,1) [virtual companion], A(21,1,1).

All three lie in capacity gap 15; their reasons are recreation of 2->13
and 3->13. The SINGLE demand node has weight four and neighbor capacity
three: a minimum-cardinality Hall obstruction of deficiency one. Immutable
primitive reconstruction checks the complete eligibility, not just a returned
flow value. The r8 instances give deficiency two for the analogous single node.

Later actual A recreations at operations 51,...,61 and other original events
supply alternatives under the all-recreation rule. This isolates a precise
failure of FIRST-return eligibility combined with this reservation, not a
failure of every first-return convention, every possible baseline reservation,
the old C15 owner map, or coefficient-two CD. No old owner is overwritten.

Gap-level Hall subsets are minimum-cardinality when at most 16 demands are
enumerated; otherwise the export makes only an inclusion-minimal claim.
The unit routine also claims only inclusion minimality except for the explicit
single-node certificate above. There is no hidden global-minimum assertion.

## 10. Explicit debt-potential templates and exact refutations

The five independently defined complete-state functions are:

* f_edge=|E(B) minus E(A)| on every physical key;
* f_anc=number of strict ancestor pairs true in B and false in A;
* f_SET=|J_S(B) minus J_S(A)| with full carrier and SET duplicate suppression;
* f_sum=sum_x max(d_B(x)-d_A(x),0);
* f_max=max_x max(d_B(x)-d_A(x),0).

Test Phi=lambda*f for a constant lambda>=0 against d<=Phi(start)-Phi(end).
Each row below has d>0 and f(start)-f(end)<=0. It therefore refutes EVERY
nonnegative constant multiplier of that function with one exact original gap.

| f | complete source / gap | d | f(start) | f(end) | difference |
|---|---|---:|---:|---:|---:|
@PT@

Here `W_5_1` means W_(p=5,q=1), N=129; it is distinct from the 33-key
within-hit recreation control named `W_5`. All words and complete states are
exported. These are exact intermediate-lemma refutations; they say nothing
against other weights, nonlinear functions, history coordinates or combinations.
No increasingly complex fitted potential is introduced after these failures.

Primitive update rules are physical. In a rotation promoting side-child v of u,
the only lost ancestor pairs are u above v and v's outer same-side component;
the gained pairs are v above u and u's opposite outer component. Middle-component
vertices remain below both. Consequently an A rotation changes f_anc by
|lost_A intersect Anc(B)|-|gained_A intersect Anc(B)|; a B rotation changes
it by |gained_B minus Anc(A)|-|lost_B minus Anc(A)|. The corresponding edge
formula uses the actual at-most-three deleted/added edges. SET changes use
the duplicate-suppressed subtree labels. Depths decrease by one on v and
its outer component, increase by one on u and its opposite outer component,
and stay fixed on the middle component; applying positive part or maximum
gives exact updates for the depth features. None of these quantities is
defined using Q_B-2A or a maximum-path construction.

## 11. Controlled perturbations and source completeness

Seed 20261110 fixes 15 initial words, three for each population 7,9,13,21,33.
Each has 4n genuine original operations with KEEP/DELETE choices, followed
by full increasing and decreasing KEEP sweeps. All that reset work is paid.
Four further fixed words on 9,13,21,33 keys are iterated to the first repeat
of the COMPLETE pair; only the recurrent period is charged, with the exact
diagonal reaching prefix exported. The finite orbit search is capped at 64
word iterations and succeeds in these cases.

G varies short-scan length and repetition. H/W vary support, dyadic scan
lengths and low hits; lifted H and I^rZ retain actual private/fringe keys and
closing builders. Reflection and repeated-copy controls preserve exact costs.
No arbitrary splicing is assumed closed. No CD(7) state enumeration is run.
This is a deterministic finite construction grid plus seeded bounded words,
not exhaustive enumeration or a search-complete optimal-ratio claim.

## 12. Net-gap versus root-normalized balance

There are @POSU@ positive-u gaps but @POSD@ positive-net gaps. The difference
comes from local A overhead already covering some root-normalized exposure.
For proving the scalar target, net positive/negative parts are simpler and
avoid counting simultaneous u,c. The p split nevertheless identifies a real
geometric question: is B deep relative to A BEFORE the gap's preparation?
It separates inherited exposure from changes caused inside that gap.

The H_(3,1) neutral example u=c=2 would disappear from net-only demand,
although it consumes and redistributes physical ancestry. H_(1,1), gap 2,
has d=u=c=0 yet edge disagreement increases 4->5 and ancestry disagreement
falls 12->7. Neutral cannot mean geometrically inert.

The split has diagnostic explanatory value here, but it has NOT produced a
proved stronger global compensation law. For pure cost optimization the net
split remains adequate; preserving p is justified by the fingerprints, not by
an established matching theorem.

## 13. Scoped counterexample registry

* Same-gap capacity always dominates u: REFUTED parametrically by H's second gap.
* Capacity with the same KEEP target suffices: REFUTED by the exact restricted graph.
* First A recreation plus chronological baseline reservation suffices: REFUTED
  by the one-node C15 unit Hall certificate, while the gap graph conceals the defect.
* A nonnegative scalar multiple of any one of the five geometric functions
  satisfies every gap inequality: REFUTED by the independently reconstructed rows above.
* Neutral gaps have no physical effect: REFUTED by the complete H witnesses.

No failed statement is silently replaced by a weaker one. Permissive eligibility
is reported separately as finite surviving evidence. No complete-source sharp
counterexample has been found, so coefficient two itself is neither refuted nor proved.

## 14. Strongest surviving relationships and debt-transfer interpretation

The inherited exact identity, disjoint KEEP partition and p<=H survive all checks.
The new parametric local obstruction is an all-parameter physical calculation,
not merely a finite numerical correlation. The finite unit incidence shows how
later recreations can repair the particular first-return congestion without
inventing capacity or relying on proximity in time.

For each fixed ordered physical pair, cyclic A and B ancestry gains equal
their respective losses. The primitive table proves this statement and records
its actual events. It does not bound how many excess gaps refer to one lost
wing or to one absence episode. A rotation can change arbitrarily many pairs.
Closure forces B recreation of a relation removed by B; it does not, by itself,
force a usable A recreation or an unoccupied capacity unit.

@MISSING@ B-only ancestor-history records in this finite corpus have no A
recreation in the period. This is a measured fingerprint count, not a theorem
excluding that case in other admissible sources. The surviving rule needs only
enough eligible units jointly; it does not require every ancestor to supply one.

## 15. D6/R6 comparison, at its proper scope

The physical controls preserve D1/D2/D3/D4 mechanisms, G's short progression,
D6's full-fringe construction, W_5's within-hit edge recreation, W_star's
full-Pi disqualification and the C15 owner/zero-run words. The oracle computes
original full-carrier SET signs and preserves the designated cuts.

No conservation candidate is proved here, so the requested R6 connection is
diagnostic only. SHARP does not implement a complete Pi/cohort/R6 classifier,
does not copy such predicates across a new cut, and does not claim that a
positive c gap pays an old R6 object. Historical CD6 and D6 retain their stated
qualifications. The new Global Boundary Reuse result likewise leaves global
earlier-loss reuse unresolved; its ancestry ledger is compatible with this finding.
The completed EXP-01 result is a separate scoped scan theorem and supplies
no exact u-to-c capacity rule. Its R6 counts and Pi certificates are not silently
imported as SHARP oracle outputs.

## 16. Candidate universal statement and the first missing proof

A falsifiable remaining candidate is the following STRONGER incidence claim:
for every admissible complete source with a KEEP, reserve the first min(q_i,2p_i)
chronological two-per-StepEv units in each gap; connect each excess gap to
remaining units whose actual A rotation recreates y->x_i for a B-only starting
ancestor y (with the stated virtual-zig convention). This graph covers all u_i.

This is OPEN, not a theorem or an accepted reduction of proof difficulty.
Its independently defined physical edges distinguish it from an all-to-all
matching. Nevertheless its first missing proof is a uniform Hall inequality
for EVERY demand subset using actual shared rotation inventories, including
ancestors never recreated by A and repeated absent episodes. Endpoint closure
does not establish that inequality. Merely asserting it would be an equally
hard new existence burden and would not complete SHARP.

The finite witness set suggests looking at nonlocal episode exchange rather
than first-return selection. No further campaign, fitted coordinate or abstract
bootstrap is executed. The proof of Universal Q_B<=2A remains missing.

## 17. Evidence, resource and verification limitations

The principal artifact checks are exact and use two implementations. They are
not formal certification, peer review, arbitrary-parameter verification of every
historical report, or exhaustive source coverage. C15's old audit seal is NOT
resumed or completed; its historical 299.125/300 record stays untouched.
The C15 replays here test new scalar gaps on the user-authorized SHARP corpus,
not old frozen-owner or Bank25 proofs. Only r7/r8 C15 instantiations are replayed;
the arbitrary-length zero-run theorem is retained at its historical proof scope.

Two provenance-only files changed concurrently: EXP01's constructor gained a
new unused function, and Global Boundary Reuse was completed. Their before/after
hashes are recorded. Executed SHARP constructors were already saved in this
directory, and the immutable reference and C15 fixture pins did not change.
No concurrent edit is attributed to SHARP. No old source was overwritten.

The first run finished all 79 replays but failed its final provenance hash
guard before writing its usage receipt. Exact first-run CPU and peak memory
therefore remain UNRECORDED; this is an instrumentation defect, not a mathematical
PASS for those measurements. A conservative 600 CPU seconds is charged to that
run, whose per-source CPU guard had passed. Saved-ledger finalization took
@FINALCPU@ CPU seconds; full immutable verification took @INDCPU@; strict unit
incidence took @UNITCPU@; the final geometric/Hall/cut checks took @CERTCPU@.
Earlier short acceptance/probe invocations also occurred; their numerical test
receipts are retained, and uninstrumented probe CPU is not guessed. The new
post-measurement work remains within the separate 120-second verification reserve.
No historical CPU/audit allowance is reset or borrowed. Peak memory of the
failed run is a real verification limitation; no fabricated number is supplied.

The original ledger files occupy @BYTES@ bytes. Reproduction uses only Python's
standard library and the pinned local immutable reference. No dependency installation,
external search, old engine/controller invocation, subagent or Git mutation is used.
The reproduction driver now persists an exit usage receipt even on failure.

## 18. Final research verdict and advancement record

**TARGETED REFUTATION — exact intermediate source rules.** The original sharp
theorem remains OPEN. New progress consists of the parametric same-gap
obstruction, exact scalar-potential countercertificates, and a physical
first-restoration congestion witness whose gap-level success disappears when
capacity is traced to its actual units. A broader source-defined eligibility
rule survives finite tests, with no claim of a uniform Hall theorem.

BEFORE: an inherited coefficient-preserving identity but no physical global law.
RESULT: independently checked complete ledgers and precise rejected mechanisms;
no genuine Q_B>2A source on the corpus. AFTER: local and simple scalar routes
are ruled out at their exact scopes; nonlocal shared-episode funding remains
unproved. No universal sharp obligation has been discharged and no Dynamic
Optimality conclusion is promoted. Stop after SHARP-01.
'''
replacements={'@TABLE@':table,'@FLOWTABLE@':flowtable,'@PT@':pt,'@BEST@':f"{best['Q_over_A']} ({best['name']})",'@SIMULT@':str(simult),'@NEUTRALUC@':str(neutraluc),'@PREP@':str(prep),'@BASE@':str(base),'@POSU@':str(sum(s['positive_excess_gaps'] for s in summ)),'@POSD@':str(sum(s['positive_net_gaps'] for s in summ)),'@MISSING@':str(missing),'@FINALCPU@':str(receipt.get('finalization_cpu_seconds',receipt.get('cpu_seconds'))),'@INDCPU@':str(ind['cpu_seconds']),'@UNITCPU@':str(unit['cpu_seconds']),'@CERTCPU@':str(cert['cpu_seconds']),'@BYTES@':str(receipt['ledger_total_bytes'])}
for k,v in replacements.items():report=report.replace(k,v)
assert '@TABLE@' not in report
(BASE/'SHARP01_DISCOVERY_REPORT.md').write_text(report,encoding='utf-8')
repro=r'''# SHARP-01 reproduction and artifact map

Use the repository root on `coarse-double-branch`, HEAD
`6d532b2c795c0778f57d8023b23b5fedfc48b010`. Python standard library only.
No installation, old source engine, old audit controller or network is needed.
Run Python with `-B` to avoid caches outside this directory.

The complete finite corpus is in `SHARP01_SOURCE_WITNESSES.json`. Its exact
initial states, KEEP/DELETE words, explicit diagonal prefixes, metadata and
reflection/repetition identities are sufficient for independent replay. Source
IDs are names; operation and rotation IDs are local to those original words.

`SHARP01_GAP_LEDGER.json` indexes full chronological ledgers under `ledgers/`.
Resolve each tree reference through that ledger's `states` object. It records
every operation, StepEv, real rotation, terminal zig, physical middle transfer,
signed full-carrier SET change and cyclic gap. Prefix events are not period events.
No-KEEP sources have no gap and explicitly unpartitioned A, with Q=0.

Read `SHARP01_DISCOVERY_REPORT.md` for the precise scope of the refutations.
`SHARP01_RESULTS.json` contains all reduced-rational family summaries,
gap-level flow graphs and potential constraints. `SHARP01_PHYSICAL_INCIDENCE.json`
gives strict unit eligibility reasons, flows and deficiencies. `SHARP01_COUNTERCERTIFICATES.json`
contains independently reconstructed potential and Hall obstructions.

## Check existing saved results

From this directory, these bounded commands verify the saved records:

```powershell
python -B sharp01_tests.py
python -B sharp01_validate.py
python -B sharp01_certificate_check.py
```

They rewrite only their own NEW SHARP verification receipts. The first checks
222 primitive rotations, every small-H seam including physical bit records,
reflection, copies, empty/zero/no-KEEP cases. The second independently replays
all 79 sources and 25,807 operations and constructs cyclic gaps by a different
algorithm. The third independently evaluates refuting features, replays nine
large cyclic cuts and checks all 288 primitive ancestry changes of the C15
Hall witness before recomputing its first-return eligibility.

## Fresh measurement reproduction

Preserve this run. Create a NEW sibling versioned directory under
`DO_RESEARCH_REBOOT`, copy the `sharp01_*.py` scripts into it, and run there:

```powershell
python -B sharp01_tests.py
python -B sharp01_experiments.py
python -B sharp01_validate.py
python -B sharp01_unit_incidence.py
python -B sharp01_certificate_check.py
python -B sharp01_ancestor_episodes.py
```

The scripts locate repository inputs relative to a directory directly under
`DO_RESEARCH_REBOOT`; do not put the fresh directory one level deeper. A fully
standalone copy outside the repository can verify saved witnesses by using the
three check commands above; source generation needs the pinned C15 fixture files.
Seed is 20261110. Source parameters are explicitly enumerated in `corpus()`.
The generated source-word hash, totals, cases and complete tree endpoints should
match; timing/peak memory and provenance hashes of concurrently edited research
can differ. Different JSON spacing is immaterial. All costs use integers and
ratios use `fractions.Fraction`.

The report is the original campaign manuscript. `sharp01_write_report.py`
renders that manuscript and its original recovery narrative from these records;
it is not required to reproduce numerical findings in a fresh run.

The measurement run caps itself at 220 sources, 600 keys, 20,000 operations
per source and 600 process CPU seconds. The separate verification reserve is
120 seconds. These are new SHARP ceilings, never resets of historical budgets.
This is a finite selected corpus, not exhaustive CD(7) enumeration. A confirmed
positive complete-source deficit stops the driver and exports its complete ledger.

## Recorded recovery and limitations

The actual first run finished all sources but its final hash check detected an
external change to the unused original EXP01 source file. Exact first-run CPU
and peak memory were not persisted before that guard. This defect is disclosed
in `SHARP01_RUN_RECEIPT.json`; a conservative 600-second charge is retained.
The main driver now writes `SHARP01_PROCESS_EXIT_RECEIPT.json` in `finally` on
future runs. The current dataset is recovered from already-saved ledgers using
`sharp01_finalize_saved.py`, WITHOUT replaying any source, and then independently
verified. The recovery script requires the original saved ledgers and is not
part of the normal fresh-run sequence.

`SHARP01_INPUT_MANIFEST.json` records the original pins, concurrent provenance
changes, executed constructor snapshot and immutable-reference hash. Other
agents' later changes cannot be called SHARP edits. The newer Global Boundary
Reuse report stays BLOCKED. No C15 proof seal or frozen owner is modified.

No finite flow proves Universal CD. In particular, a successful gap graph need
not give a successful event-unit graph. First-restoration fails under the
specified chronological reservation; all-restoration survives this finite set.
The universal Hall/episode-sharing argument is absent. Final verdict is TARGETED
REFUTATION of the stated intermediate rules; Q_B<=2A remains open.
'''
(BASE/'SHARP01_REPRODUCTION.md').write_text(repro,encoding='utf-8')
print(json.dumps({'report_bytes':(BASE/'SHARP01_DISCOVERY_REPORT.md').stat().st_size,'sources':len(summ),'simultaneous_uc':simult,'neutral_uc':neutraluc,'capacity_preparation':prep,'capacity_baseline':base,'missing_A_recreations':missing}))
