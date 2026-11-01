"""Save the achieved partial construction and its separate full-law failure."""
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent
def put(name,s):
    with (OUT/name).open('x',encoding='utf-8',newline='\n') as f:f.write(s.strip()+'\n')
def js(name,v):put(name,json.dumps(v,indent=2))
def main():
    c=json.loads((OUT/'fixed_exact_pair_certificate.json').read_text(encoding='utf-8'))
    a=json.loads((OUT/'independent_audit.json').read_text(encoding='utf-8'));assert a['status']=='PASS'
    assert len(c['closed_witness']['word'])==14
    put('FX04_FULL_LAW_COUNTEREXAMPLE_AND_REPLAY.md',r'''
# The three repaired tests do not give universal B repayment

The repaired Ehat meets all three named requirements, but a different six-key starved KEEP refutes its full B-repayment law. This safeguard prevents a restricted construction from being promoted to Universal Coarse-Double.

## Exact hook vine pair

Let L_[a,b] denote the left vine on all integer keys a through b, rooted at b. Use

    A_H=1(empty,L_[2,6]),
    B_H=L_[1,6].

KEEP 1 does not move A_H. B_H has depth five at 1, so a=0,q=2,z=1 and the whole required upper bound is -2. The source proper subtree sets are

    C0(A_H)={[2,k]: k=2,3,4,5,6},
    C0(B_H)={[1,k]: k=1,2,3,4,5}.

They have no exact common sets. The only residual endpoint edges match [2,k] to [1,k] for k=2,3,4,5. These four disjoint edges and either endpoint set as a four-vertex cover prove mu=4. Therefore

    Ehat_source=5-0-4=1.

After the B splay,

    B'_H=1(empty,6(4(2(empty,3),5),empty)).

Its proper sets are [2,6],[2,5],[2,3],{3},{5}. The three exact pairs [2,6],[2,5],[2,3] are now fixed. The residual graph has A vertices {2},[2,4] and B vertices {3},{5}; it has no endpoint edge. Thus c=3,mu=0 and

    Ehat_destination=5-3=2,
    Delta_KEEP Ehat=+1>-2=2a-q.                         (10)

The new forced pairs consume the endpoint capacity that previously supported four inexact matches. Preserving exact matches repairs the designated helpers but does not guarantee a matching-rank increase for every B access.

## Full source closure

The fixed n=6 source-only connector BFS found the following DELETE prefix from L6 to A_H:

    D3 D5 D1 D4 D1 D6 D1.

Starting from the diagonal (L6,L6), append the failing K1 and then a common ascending pass K1 K2 K3 K4 K5 K6. The complete source word is

    D3 D5 D1 D4 D1 D6 D1 K1 K1 K2 K3 K4 K5 K6.

The eighth operation is exactly (10). The last six requests turn both trees back into L6, and both actual source engines verify every shared full state and exact paired closure. The totals are A=19,Q_B=5,Z_B=4. Coarse-Double holds on this walk (5<=38); only Ehat's pointwise source inequality is refuted.

There was one source-only search on the fixed six-key single-tree universe, examining 132 distinct trees and 786 requests. It located a finite connector, not a potential or graph-wide inequality. No source-state pair graph, larger corpus or finite fit was constructed. The full word and replay are the actual certificate; shortest-path optimality is not a proof premise.

## Exact checks and the helper distinction

The positive prescribed controls were the n=6 opposite-vine access, both m=0 helpers, both m=1 helpers and both reflected m=0 helpers. They all passed. The hook-vine safeguard then failed, and no replacement candidate was tested.

The L-helper's whole compensation is compatible with this failure: its source, after-A and destination Ehat values are 2,2,2. Its whole budget is zero, so it passes; its B phase alone does not pay q=2. If the preparation is a separate DELETE and the next KEEP is starved, the latter is a different required edge. The successful named whole-helper theorem never asserted a universal B-phase law.

independent_audit.json reports PASS on 38 protected matching evaluations, each with all exact pairs verified and a matching plus equal-size cover proving the residual maximum. It also checks 12 symbolic core/port reductions, 16 actual source endpoint tables, 22 complete source edges and the fourteen-operation closed replay. The arbitrary-fringe proof is the analytic cancellation in FX03, not an inference from the two sampled fringe cardinalities.
''')
    put('FX05_UPDATED_STRATEGY_REVIEW.md',r'''
# Strategy review after fixing exact pairs

This construction achieves the user's three named requirements for one explicit function: universal DELETE, full q on opposite vines and compensation for both established arbitrary-fringe helper branches. It still fails a valid off-family B consumer, so the original universal potential premise is not discharged.

## Before and after

BEFORE: F obeyed DELETE and the helper laws but failed opposite vines. E's nonlinear endpoint matching obeyed DELETE and paid opposite vines, but its matching bonus lost helper compensation. The prior mandatory review stopped further variants without a concrete cancellation mechanism.

RESULT: Ehat fixes every exact common proper subtree pair before solving the residual endpoint matching. A constrained rematching argument preserves the one-unit A-rotation bound. The opposite-vine drop becomes exactly -(q+1), retaining full repayment. A symbolic private-edge reduction handles every internal fringe graph: branch L has the same c_int+3+mu_LH protected rank before and after; branch R gains 2+mu_L-mu_LH in {1,2}. Thus the old incompatible named tests now hold for the SAME function, uniformly in n and arbitrary U,V.

AFTER: The three named partial obligations are achieved. The independent hook-vine safeguard, however, has a=0,q=2 and Ehat=1->2, refuting the full source law. Ehat is therefore a proved restricted construction and a refuted universal candidate. Neither the old E/F laws nor the new Ehat laws are spliced across functions.

NAMED ACCEPTANCE OBLIGATIONS DISCHARGED FOR EHAT: all DELETE edges; every opposite-vine access and its reflection; both established arbitrary-fringe whole-helper branches and their reflections. The source inequality is proved on their union. Any closed walk using only these source edges consequently satisfies Q_B<=2A by telescoping Ehat. This is an explicitly restricted domain, not an assertion that general source walks belong to it or that the subclass was previously unresolved in the repository or literature.

ORIGINAL LOAD-BEARING PREMISES DISCHARGED: none. Universal Coarse-Double remains OPEN; the complete uniform A/B potential remains OPEN as an existence problem, while Ehat itself is REFUTED as a universal solution. NET ADVANCEMENT OF THE FULL ORIGINAL PROOF: zero. The achieved named construction is genuine partial content, not a Dynamic Optimality proof.

NEW ASSUMPTIONS FOR THE ORIGINAL THEOREM: none. D, mu_L and mu_LH in the helper proof are explicit graphs/ranks attached to the existing current U,V. They cancel identically or differ by one added vertex. No assumption about their values, global feasibility or compatible labels is made.

## What the mechanism establishes and what it misses

Fixing exact pairs changes the earlier helper's initial reserve from 1 to 2 and leaves its destination at 2, repairing its +1 violation. It does so through an exact rank identity. It does not require larger finite fits or an unspecified fringe correction.

At the hook-vine safeguard, several new exact pairs instead displace a larger set of inexact matches. Protected matching rank falls from four to three during a starved B access. Exact-pair protection and endpoint capacity do not encode a uniform charge for all B doubles. A new global proof cannot consist of assuming that missing rank gain.

The whole-helper law is weaker than the separate root-conditioned B law needed by the original Step 3 sufficient potential criterion. The L prototype already has a zero B-phase change at q=2. This distinction is maintained in every status label.

## Gate decision and stop

FX00 froze the construction, constrained rematching proof, opposite-vine count, arbitrary-fringe rank cancellation and independent safeguard before execution. FX01-FX03 achieve the three registered partial goals. FX04 supplies the valid original-source obstruction to the full candidate, as required by the safeguard.

The previous F/E mandatory review remains intact, and this update does not reset the count of non-advancing subtree/matching audits of the full original premise. The named partial success is recorded without relabeling the global failure. Under RESEARCH_RULES, the refuted universal mechanism stops here. No weighted, selective, blended or parameter-adjusted matching, larger fit or fourth repair is launched automatically.

The next original obligation is still an explicit global function obeying both full source laws, including the displayed reachable starved consumer. No new equivalent existence premise is installed in its place. Further research would need a fresh concrete mechanism and written gate, within the already authorized append-only workspace.

Stage 11G's graph, solvers, contracts, certificates and status remain read-only. Old successes, negative examples and proof statuses are preserved. Final inherited-file hashes, tracked state, branch and HEAD are recorded in final_integrity.json.
''')
    put('FX06_FINAL_REPORT.md',r'''
# Exact common pairs repair the three named tests

An explicit repair of E satisfies all three named requirements: universal DELETE, full q on opposite vines and both established arbitrary-fringe whole-helper laws. It is not a universal B-repayment potential; a separate six-key source consumer refutes that larger claim.

Keep E's proper-subtree endpoint graph. Fix every exact common pair I--I first and remove its vertices. If c is their number and mu is the maximum matching size in the residual graph, define

    Ehat(A,B)=(n-1)-c-mu.

This is a determined current-state construction with E<=Ehat<=F, without fitted coefficients or unknown global labels.

The proved laws for this SAME function are:

* DELETE: Delta Ehat<=d_A<=2a for every finite same-key pair. A rematching argument controls changes in the forced pairs. See [FX01](FX01_DEFINITION_AND_DELETE.md).
* Opposite vines: Delta Ehat=-(q+1) for n>=2; n=1 is a no-op. See [the all-size count](FX02_OPPOSITE_VINE_PROOF.md).
* Established arbitrary-fringe helpers: branch L has Delta Ehat=0; branch R has Delta Ehat in {-2,-1}, for arbitrary paired U,V and all m>=0, including reflections. Both have a=1,q=2 and budget zero. See [the uniform helper proof](FX03_ARBITRARY_FRINGE_HELPER_PROOF.md).

The helper proof reduces every possible internal fringe graph to the SAME kernel with one left and one right boundary vertex. L cancels exactly. For R, removing one right vertex changes maximum matching rank by at most one. Thus the all-fringe result is analytic, not extrapolated from larger finite tests.

The full-law safeguard still fails. At A=1(empty,left-vine2..6), B=left-vine1..6, KEEP 1 has a=0,q=2 but Ehat rises from 1 to 2, where a drop of at least 2 is required. The complete fourteen-operation closed replay has A=19,Q_B=5 and does not refute Coarse-Double. See [the exact counterexample](FX04_FULL_LAW_COUNTEREXAMPLE_AND_REPLAY.md).

[Independent verification](independent_audit.json) passed on 38 residual matching/cover certificates, all symbolic core reductions and complete source replay. The [four-rule gate](FX00_FOUR_RULE_GATE.md) preceded execution, and the [updated strategy review](FX05_UPDATED_STRATEGY_REVIEW.md) records the achieved partial construction and the remaining global failure separately.

No larger finite fits or Stage 11G edits occurred. The universal potential and Coarse-Double remain open. Reproducibility is in [FX07](FX07_REPRODUCIBILITY.md); preservation checks are in final_integrity.json.
''')
    put('FX07_REPRODUCIBILITY.md',r'''
# Reproducing the fixed exact pair audit

The scripts use Python's standard library and the frozen source engines. No packages are installed. From the repository root, the original invocations were

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_fixed_exact_pairs_20261031_v001/audit_fixed_pairs.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_fixed_exact_pairs_20261031_v001/independent_verify.py
```

Outputs use exclusive creation. Do not rerun in this populated directory. To reproduce, copy these scripts and helper_boundary_certificate.json into a fresh versioned sibling under DIRECT_U4_PARALLEL_RESEARCH and substitute its path in the invocations. Preserve the prior E, F and analytic input directories.

The primary audit evaluates one n=6 opposite-vine access, both helper branches at m=0 and m=1, the two reflected m=0 helpers, and one fixed n=6 hook-vine safeguard. It then uses one single-tree n=6 BFS only to locate a DELETE prefix for an explicit closed witness. There is no potential fit, larger tree corpus, source-state pair graph or parameter search.

fixed_exact_pair_certificate.json saves the complete trees, a,q,z and oriented source events; all exact common pairs; the residual graph for each distinct evaluated pair; and a matching plus equal-size cover proving every residual maximum. It also includes the full fourteen-operation paired replay.

helper_boundary_certificate.json is a SYMBOLIC five-core-vertex/port certificate. independent_verify.py checks all four reductions with distinct fringe extrema, coincident extrema and the empty substitution, and verifies the actual core endpoint tables in the fixed source controls. These checks support the structural proof in FX03; they do not enumerate or fit arbitrary fringes. The only rank inequality for the unknown-size interior is the proved one-added-vertex lemma, valid for every finite graph.

The independent verifier does not import the producer or invoke a matching algorithm. It regenerates residual graphs, checks all forced exact pairs, validates matching/cover equality, replays the pointer source and checks exact full paired closure. independent_audit.json is its PASS record.

entry_source_pins.json records fourteen inherited inputs, HEAD and branch. integrity.json checks them after the source audit. final_integrity.json checks them again at delivery and validates report/certificate links. delivery_manifest.json hashes every new file except itself. Existing research, sources, solver data, Stage 11G assets and proof statuses remain read-only.
''')
    js('proof_status_ledger.json',{'date':'2026-10-31','candidate':'Ehat=(n-1)-c-mu: fix every exact common proper pair, then maximum residual endpoint matching',
      'claims':[
        {'claim':'Ehat is explicit, finite and E<=Ehat<=F','status':'SOURCE DEFINITION','proof':'FX01_DEFINITION_AND_DELETE.md'},
        {'claim':'Universal DELETE for Ehat','status':'PROVED—UNIVERSAL','scope':'all finite same-key present-key BST source pairs; Delta Ehat<=d_A<=2a','proof':'FX01_DEFINITION_AND_DELETE.md'},
        {'claim':'Full q on opposite vines','status':'PROVED—RESTRICTED DOMAIN','scope':'all sizes, both orientations; exact Delta=-(q+1) for n>=2; n=1 noop','proof':'FX02_OPPOSITE_VINE_PROOF.md'},
        {'claim':'Established arbitrary-fringe whole-helper compensation','status':'PROVED—RESTRICTED DOMAIN','scope':'both RA02 branches, every same-key U,V,m>=0 and reflections; L Delta=0,R Delta in {-2,-1}','proof':'FX03_ARBITRARY_FRINGE_HELPER_PROOF.md'},
        {'claim':'Closed-walk Coarse-Double on the union of the named source-edge classes','status':'PROVED—RESTRICTED DOMAIN','scope':'all DELETEs and the specified opposite-vine/helper KEEPs only; no assertion general walks have this restriction','proof':'FX05_UPDATED_STRATEGY_REVIEW.md'},
        {'claim':'Full root-conditioned B repayment for Ehat','status':'REFUTED—EXACT','scope':'reachable n6 hook-vine KEEP1,a=0,q=2,Ehat=1->2','proof':'FX04_FULL_LAW_COUNTEREXAMPLE_AND_REPLAY.md'},
        {'claim':'Ehat is a universal source potential','status':'REFUTED—EXACT','scope':'same legal whole KEEP counterexample'},
        {'claim':'Residual maxima, symbolic core reductions and full source replay','status':'FINITE-EXACT','scope':'38 residual matching/cover certificates,12 symbolic reductions,16 actual core tables,22 source edges,14 closed operations','proof':'independent_audit.json'},
        {'claim':'A complete uniform A/B potential exists with the required laws','status':'OPEN','scope':'Ehat does not solve the full original Step3 obligation'},
        {'claim':'Universal Coarse-Double','status':'OPEN','scope':'no full proof or counterexample'},
        {'claim':'Downstream Dynamic Optimality assembly','status':'CONDITIONAL','scope':'inherited load-bearing premises unchanged'}],
      'named_acceptance_obligations_achieved':['universal DELETE','all-size full-q opposite vines','both all-size arbitrary-fringe whole-helper families'],
      'original_load_bearing_obligations_discharged':[],'net_advancement_of_full_original_proof':0,
      'genuinely_covered_restricted_source_cases':'union of all DELETE edges, stated opposite-vine KEEPs and established helper families with reflections',
      'new_assumptions_for_original_theorem':[],'full_candidate_refuted':True,
      'updated_mandatory_strategy_review':'FX05_UPDATED_STRATEGY_REVIEW.md','next_automatic_campaign':None,
      'finite_potential_fits':0,'new_source_state_graphs':0,'Stage11G_writes_performed':False})
    print(json.dumps({'remaining_reports_written':4,'ledger_written':True,'three_named_laws':'PROVED on stated domains',
      'full_potential':'REFUTED by separate source safeguard','independent_audit':'PASS'}))

if __name__=='__main__':main()
