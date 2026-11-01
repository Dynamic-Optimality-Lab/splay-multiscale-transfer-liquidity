"""Save the completed bounded endpoint-matching audit without overwrites."""
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent
def put(name,s):
    with (OUT/name).open('x',encoding='utf-8',newline='\n') as f:f.write(s.strip()+'\n')
def js(name,x):put(name,json.dumps(x,indent=2))
def main():
    c=json.loads((OUT/'endpoint_matching_countercertificate.json').read_text(encoding='utf-8'))
    assert json.loads((OUT/'independent_audit.json').read_text(encoding='utf-8'))['status']=='PASS'
    bad=c['controls'][-1]
    assert c['closed_witness']['initial_A']==c['closed_witness']['initial_B']==bad['source_B']
    put('EM03_EXACT_HELPER_OBSTRUCTION.md',r'''
# The first six key helper refutes endpoint matching

The nonlinear endpoint repair pays full q on opposite vines and obeys DELETE universally, but it fails the required arbitrary-fringe helper law already at the permitted empty fringe. This is a whole source KEEP with zero budget, not an extra micro-step requirement.

## Full physical source operation

Use the L branch of the established six-core family, with no additional fringe keys. Omitted children and bare key children are empty and leaves respectively. The initial trees are

    A0=6(2(1,3(empty,4(empty,5))),empty),
    B0=6(5(4(1(empty,2(empty,3)),empty),empty),empty).

KEEP 2 gives

    A1=2(1,6(3(empty,4(empty,5)),empty)),
    B1=2(1,5(4(3,empty),6)).

The source A access has depth one and performs one left-oriented zig. B has depth four and performs LR then LL, so

    a=1, q=2, z=0, required upper bound 2a-q=0.

The actual grouped events are A: ZIG on keys 2,6 with orientation L; B: LR on 1,2,4 followed by LL on 2,5,6. Both the pointer and frame engines agree on every event and complete tree endpoint.

## Exact proper subtree vertices

Intervals denote exact key sets on these consecutive keys. They do not encode subtree shape.

| Tree | Proper subtree key intervals |
| --- | --- |
| A0 | [1,1], [1,5], [3,5], [4,5], [5,5] |
| B0 | [1,3], [1,4], [1,5], [2,3], [3,3] |
| A1 | [1,1], [3,5], [3,6], [4,5], [5,5] |
| B1 | [1,1], [3,3], [3,4], [3,6], [6,6] |

## A matching and equal size cover at the source

The following four disjoint graph edges form a matching in the A0,B0 endpoint graph:

    A[1,1] -- B[1,3],
    A[1,5] -- B[1,4],
    A[3,5] -- B[3,3],
    A[4,5] -- B[1,5].

The left vertices A[1,1], A[1,5], A[3,5], together with right vertex B[1,5], cover EVERY graph edge. This cover has size four. A matching cannot be larger than any vertex cover, so nu(A0,B0)=4 and

    E(A0,B0)=5-4=1.

## A matching and equal size cover at the destination

Three disjoint edges are

    A[1,1] -- B[1,1],
    A[3,5] -- B[3,3],
    A[3,6] -- B[6,6].

The only non-isolated left vertices are A[1,1], A[3,5] and A[3,6]. They cover all edges, so nu(A1,B1)=3 and

    E(A1,B1)=5-3=2,
    Delta_KEEP E=+1>0=2a-q.

These hand-readable matching/cover certificates are independently verified in addition to the algorithm-generated certificates. The arithmetic proves the violation without trusting an optimizer's assertion.

## Why the correction loses helper safety

After A alone moves, E(A1,B0)=2; during the B phase E remains two. The matching ranks along the whole source operation are 4 -> 3 -> 3. Thus the B phase creates no net matching augmentation to compensate for A motion, despite creating exact agreements.

The old F values are 4 -> 5 -> 3, so F's whole change is -1 and its B-phase drop is two. For H=E-F,

    H_source=-3, H_destination=-1, Delta H=+2.

The helper allowed H to increase by at most one, because Delta F=-1 and the whole budget is zero. The endpoint repair exceeds that allowance by one. E<=F at every state did not preserve F's transition inequality.

The arbitrary-fringe contract explicitly includes m=0. This in-domain empty-fringe witness therefore refutes preservation of the entire stated family. It does not claim that every nonempty fringe also fails. No larger fringe controls, alternative matching cost or hook-vine test were run after this first obstruction.
''')
    put('EM04_SOURCE_REPLAY_AND_VERIFICATION.md',r'''
# Exact source replay and matching verification

The candidate was evaluated on two prescribed opposite-vine controls and then the first six-key helper. That helper failed, so the audit stopped candidate testing and reused an existing exact closed word to certify physical reachability.

## Fixed values

| Whole KEEP | E source | E after A | E destination | a | q | Delta E | Budget |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Opposite vines, n=6, access 6 | 5 | 5 | 1 | 0 | 2 | -4 | -2 |
| Opposite vines, n=7, access 7 | 6 | 6 | 1 | 0 | 3 | -5 | -3 |
| Six-key L helper, access 2 | 1 | 2 | 2 | 1 | 2 | +1 | 0 |

The all-size opposite-vine claim is proved by symbolic matchings and covers in EM02. The two controls only check source wiring and parity values. There was no fitted table or larger tree corpus.

## The closed physical witness

Start from the diagonal (B0,B0), with B0 as displayed in EM03. Execute

    D1 D3 D6 D2 D6 K2 D5 D2 K1 K4 K6.

The first five operations reach exactly (A0,B0), and the sixth is the failing zero-weight KEEP 2. The final physical pair equals the initial diagonal. This exact word was inherited read-only from route_c_analytic_20261030_v001/six_key_closed_controls.json, control zero. The new audit replays the whole word with both source engines and attaches the new matching certificates at every state.

Its totals are A=16, Q_B=4 and Z_B=2. Coarse-Double holds on this walk (4<=32). Only the proposed E edge inequality is refuted; no negative closed-walk claim is made. No connector search was needed.

## Independent exact verification

audit_endpoint_matching.py constructs maximum matchings in the CURRENT-pair endpoint graphs and supplies equal-cardinality vertex covers. These graphs are part of E's definition; they are not source-state graphs or potential-feasibility systems.

independent_verify.py imports neither the producer nor its matching algorithm. It regenerates every proper subtree interval, every endpoint edge and nonedge, and checks that each saved matching has distinct valid endpoints. It checks every cover covers all edges, and that its size equals the matching size. Weak duality then certifies all eighteen maximum matching values exactly, without another solver or a fitted coefficient.

The verifier also checks the two hand-readable certificates in EM03. It independently replays all fourteen recorded whole source edges using the pointer engine, verifies oriented events and the original d_A,d_B,a,q,z conventions, and checks complete shared tree states and exact paired closure. independent_audit.json reports PASS.

No singleton-fringe controls, port-embedding search, hook-vine control, graph enlargement, new tree corpus, coefficient search or finite potential fit followed the first helper failure. Those were conditional audit branches, not unfinished proofs needed for this exact refutation.
''')
    put('EM05_MANDATORY_STRATEGY_REVIEW.md',r'''
# Strategy review after two subtree set audits

The endpoint matching repair solves the old opposite-vine deficit while retaining DELETE, but destroys helper safety. No single potential now has all three required properties. The two consecutive subtree-set audits have discharged no load-bearing premise of the original proof, so RESEARCH_RULES requires this strategy review.

## Before and after the endpoint audit

BEFORE: F counted exact common subtree key sets. One-set replacement made it DELETE-safe. A root-conditioned B splay created at least one new common set and lost none. This proved arbitrary-fringe helpers with d_A=1,q=2, but opposite vines gained only one or two sets and failed full q. Scalar rescaling was already excluded.

RESULT: The explicit nonlinear E=(n-1)-nu uses maximum proper-subtree endpoint matching. It remains one-Lipschitz per primitive A rotation and therefore DELETE-safe at every size. On opposite vines, the matching bonus supplies an unbounded extra decrease: Delta E=-(q+2) for n>=4, with the smaller boundary cases also paying q.

The FIRST six-key helper, however, changes E from one to two on a zero-budget whole KEEP. Its A-phase matching rank falls by one; its B phase recovers no rank. Full physical source replay and exact matching/cover certificates establish the failure. This refutes preservation of the arbitrary-fringe family because empty fringes are explicitly allowed.

AFTER: E is an exact positive construction for DELETE and the opposite-vine family, but not a valid helper-safe repair of F. F retains its own valid helper proof and its own opposite-vine failure. Combining those two functions' component laws is invalid. The universal A/B potential and Universal Coarse-Double remain OPEN; downstream Dynamic Optimality assembly remains conditional.

GENUINELY DELETED ORIGINAL LOAD-BEARING OBLIGATIONS: none. NET ADVANCEMENT OF THE FULL ORIGINAL PROOF: zero. POSITIVE PARTIAL CONTENT: universal DELETE for this explicit nonlinear E and a uniform full-q opposite-vine proof. STRATEGIC ELIMINATION: this proper endpoint-matching repair as a simultaneous solution. No literature novelty or previously unresolved original subclass is claimed.

NEW ASSUMPTIONS FOR THE ORIGINAL THEOREM: none. Maximum matching here is a finite independently computable current-state operation, not a hidden existence assertion over potential labels. No all-size feasibility, selector, weighted matching compatibility or unproved matching-augmentation premise is appended to the pipeline.

## The specific obstruction to the mechanism

At opposite vines the extra endpoint matches act like useful credit. At the helper, previously inexact matches compete for the same vertices as the newly exact sets. Exact agreements can be created without increasing maximum matching rank. Thus the old F argument that each new common set lowers the reserve cannot be inherited by the matching deficit.

For this H=E-F, the opposite-vine correction supplies Delta H=-floor(n/2), but the fixed helper gives Delta H=+2 where only +1 is allowed. An alternative correction must control its release on that actual source operation while producing the required unbounded decrease elsewhere. Naming an unspecified compatible matching credit would just restate the missing construction.

## Gate decision and stopping rule

EM00 froze the graph, proper/full-set convention, source tests, conditional port-transfer mechanism and original success obligation before execution. EM01 and EM02 prove the successful component laws. EM03 refutes the helper condition, so the full registered candidate fails. Its positive restricted laws do not satisfy the gate's full original success criterion.

The prior F and present E audits use subtree key sets and the one-set A-motion identity. Their two non-advancing outcomes trigger the mandatory review; the nonlinear name does not reset that count. The rule to stop on a refuted mechanism applies. No weighted matching, altered edge cost, selector, blend, another subtree statistic, larger finite fit or additional helper family is launched.

The skipped port-embedding and hook-vine branches are unnecessary after this valid first counterexample. A future campaign requires a fresh explicit cancellation/augmentation mechanism and its own written four-rule gate. No extra user workspace authorization is needed for the existing append-only scope.

Stage 11G, its graph, solvers, contracts, certificates and proof status are not edited or promoted. All old successes and failures remain intact. Final source hashes, HEAD, branch and tracked state are recorded in final_integrity.json.
''')
    put('EM06_FINAL_REPORT.md',r'''
# Nonlinear endpoint matching repairs vines but fails helpers

No nonlinear repair satisfying all requested conditions was found. The explicit endpoint-matching candidate proves DELETE universally and pays full q on every opposite-vine access, but it fails the first six-key arbitrary-fringe helper at the allowed empty fringe.

For each tree, take its proper nonempty subtree key sets and fix the full-set match separately. Join two proper sets when their minima agree or their maxima agree. If nu is the maximum one-to-one matching cardinality, define

    E(A,B)=(n-1)-nu(A,B).

This is a nonlinear repair of F: E-F equals the number of exact common proper sets minus nu. It uses only the current physical trees.

One primitive A rotation replaces one vertex, so Delta_DELETE E<=d_A<=2a on every size. On opposite vines, explicit matchings and equal-size covers prove

    Delta_KEEP E=-(q+2), n>=4,

and all smaller cases also pay q. The nonlinear bonus therefore repairs the old unbounded opposite-vine deficit without breaking DELETE. See [the definition and DELETE proof](EM01_DEFINITION_AND_DELETE.md) and [the all-size vine proof](EM02_OPPOSITE_VINE_PROOF.md).

The helper requirement nevertheless fails:

    E source=1, E after A=2, E destination=2,
    a=1, q=2, Delta E=+1 > 0=2a-q.

The old F decreases from 4 to 3 on the same operation. The matching correction itself increases by two and loses F's helper safety. [The exact obstruction](EM03_EXACT_HELPER_OBSTRUCTION.md) includes the full trees and small hand-checkable optimal matching certificates.

[Independent verification](independent_audit.json) passed: eighteen graph values have equal-cardinality matching/cover certificates, and the complete eleven-operation source replay closes exactly. Its totals A=16,Q_B=4 do not refute Coarse-Double. See [the replay audit](EM04_SOURCE_REPLAY_AND_VERIFICATION.md).

The [four-rule gate](EM00_FOUR_RULE_GATE.md) preceded execution. Testing stopped at the first helper failure, and the [mandatory strategy review](EM05_MANDATORY_STRATEGY_REVIEW.md) records two unsuccessful subtree-set repairs without combining their incompatible component proofs. No larger finite fits, new source-state graphs or Stage 11G edits occurred. Universal Coarse-Double remains open.
''')
    put('EM07_REPRODUCIBILITY.md',r'''
# Reproducing the fixed endpoint matching audit

Use the existing Python standard library and frozen source engines; no packages are installed. From the repository root the original invocations were

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_endpoint_matching_20261031_v001/audit_endpoint_matching.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_endpoint_matching_20261031_v001/independent_verify.py
```

Outputs use exclusive creation. Do not rerun in this populated directory. To reproduce, copy the scripts into a fresh versioned sibling under DIRECT_U4_PARALLEL_RESEARCH, preserving the prior route_c_clade_correction_20261031_v001 and route_c_analytic_20261030_v001 input directories, and substitute the new directory in the commands.

Only two opposite-vine accesses at n=6,7 and the first empty-fringe six-key helper are tested as candidate controls. Once that helper fails, the producer reuses the saved eleven-operation six-key source word from the earlier analytic audit. No connector BFS, new source-state graph, enlarged corpus or potential fit is performed.

endpoint_matching_countercertificate.json records every full source state and oriented event, all exact graph vertices and adjacencies, and a matching plus equal-size vertex cover for every distinct evaluated graph. independent_verify.py regenerates the graphs and checks those certificates without invoking a matching solver. It verifies the hand-readable helper certificate and the complete closed replay independently through the pointer source engine.

The analytic proofs EM01 and EM02 establish the universal DELETE law and all-size opposite-vine law. The finite checks do not replace their quantifiers. EM03 is an exact in-domain refutation of helper preservation, since the arbitrary-fringe contract includes m=0. No claim is made about every nonempty fringe.

entry_source_pins.json records fourteen inherited file hashes, HEAD and branch. integrity.json checks them after source evaluation. final_integrity.json checks them again at delivery and validates saved reports and certificates. delivery_manifest.json hashes the new output files and excludes itself. The prior certificates, source engines, old research, Stage 11G assets and proof statuses remain read-only.
''')
    js('proof_status_ledger.json',{'date':'2026-10-31','candidate':'E=(n-1)-maximum proper-subtree endpoint matching cardinality; min=min OR max=max; full sets fixed together',
      'claims':[
        {'claim':'E is an explicit nonlinear repair of F with 0<=E<=F','status':'SOURCE DEFINITION','proof':'EM01_DEFINITION_AND_DELETE.md'},
        {'claim':'E obeys DELETE on every finite same-key source pair','status':'PROVED—UNIVERSAL','scope':'Delta E<=d_A<=2a; all orientations, fringe shapes and present keys','proof':'EM01_DEFINITION_AND_DELETE.md'},
        {'claim':'E pays full q on opposite-vine root-conditioned accesses','status':'PROVED—RESTRICTED DOMAIN','scope':'all sizes and both orientations; Delta E=-(q+2) for n>=4; boundary cases separately proved','proof':'EM02_OPPOSITE_VINE_PROOF.md'},
        {'claim':'E preserves the arbitrary-fringe zero-weight helper family','status':'REFUTED—EXACT','scope':'six-key L branch at allowed m=0: a=1,q=2,Delta E=1>0','proof':'EM03_EXACT_HELPER_OBSTRUCTION.md'},
        {'claim':'E satisfies the complete uniform source-potential inequality','status':'REFUTED—EXACT','scope':'same whole KEEP counterexample, not an extra micro-step constraint','proof':'EM03_EXACT_HELPER_OBSTRUCTION.md'},
        {'claim':'Matching values, hand certificates, costs and paired source closure','status':'FINITE-EXACT','scope':'18 certified graphs; 3 prescribed controls and 11 closed replay operations; 14 source edges','proof':'independent_audit.json'},
        {'claim':'Some nonlinear subtree-set repair satisfies all requested laws','status':'OPEN','scope':'this one candidate is excluded; other constructions are not refuted'},
        {'claim':'Universal Coarse-Double','status':'OPEN','scope':'neither a universal proof nor a counterexample was obtained'},
        {'claim':'Downstream Dynamic Optimality assembly','status':'CONDITIONAL','scope':'original obligations and statuses unchanged'}],
      'original_load_bearing_obligations_discharged':[],'net_advancement_of_full_original_proof':0,
      'positive_partial_content':['universal DELETE for explicit nonlinear E','uniform full-q opposite-vine proof'],
      'new_assumptions_for_original_theorem':[],'first_obstruction_stop':True,
      'mandatory_strategy_review_completed':'EM05_MANDATORY_STRATEGY_REVIEW.md',
      'two_nonadvancing_subtree_set_audits':['route_c_clade_correction_20261031_v001','route_c_endpoint_matching_20261031_v001'],
      'next_automatic_campaign':None,'finite_potential_fits':0,'new_source_state_graphs':0,'Stage11G_writes_performed':False})
    print(json.dumps({'new_reports_written':5,'ledger_written':True,'independent_audit':'PASS','mandatory_strategy_review_completed':True}))

if __name__=='__main__':main()
