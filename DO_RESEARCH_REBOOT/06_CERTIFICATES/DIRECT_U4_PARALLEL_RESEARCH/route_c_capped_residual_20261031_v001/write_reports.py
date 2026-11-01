"""Save the capped construction, exact safeguard and architectural review."""
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent
def put(name,s):
    with (OUT/name).open('x',encoding='utf-8',newline='\n') as f:f.write(s.strip()+'\n')
def js(name,v):put(name,json.dumps(v,indent=2))
def main():
    c=json.loads((OUT/'capped_residual_certificate.json').read_text(encoding='utf-8'))
    a=json.loads((OUT/'independent_audit.json').read_text(encoding='utf-8'));assert a['status']=='PASS'
    assert len(json.loads((OUT/'entry_source_pins.json').read_text(encoding='utf-8'))['files'])==15
    assert len(c['closed_witness']['word'])==13
    put('CR03_EXACT_SOURCE_AND_REPLAY.md',r'''
# Exact source controls and the new closed safeguard

The cap pays the old six-key starved KEEP and retains all prior named source controls. A different six-key KEEP underpays q by one. Both claims use exact residual matching values and full physical source replay.

## Fixed values

| Whole KEEP | F source to destination | Ehat source to destination | J source to destination | a | q | Budget |
| --- | --- | --- | --- | --- | --- | --- |
| Opposite vines, n=6, access 6 | 5 to 4 | 5 to 2 | 5 to 3 | 0 | 2 | -2 |
| Established L helper, m=0 | 4 to 3 | 2 to 2 | 3 to 2 | 1 | 2 | 0 |
| Established R helper, m=0 | 3 to 3 | 3 to 1 | 3 to 2 | 1 | 2 | 0 |
| Old hook-vine starved KEEP 1 | 5 to 2 | 1 to 2 | 4 to 2 | 0 | 2 | -2 |
| Known starved B phase of the L helper | 5 to 3 | 2 to 2 | 4 to 2 | 0 | 2 | -2 |
| New padded-hook starved KEEP 1 | 4 to 2 | 1 to 2 | 3 to 2 | 0 | 2 | -2 |

Both m=1 helper controls and the reflected m=0 controls also pass. The all-size DELETE/vine/helper claims are the analytic arguments in CR01; no finite control is promoted to a universal proof.

## Complete new source word

Use A_P,B_P from CR02. Starting from (B_P,B_P), execute

    D1 D3 D1 D5 D1 K1 K1 K2 K3 K4 K5 K6 K5.

The first five DELETEs reach exactly (A_P,B_P). The sixth operation is the new failed KEEP 1, with a=0,q=2,z=0 and J=3->2. The common ascending pass K1 through K6 brings both trees to L6, and the last K5 returns both to B_P. The actual full paired endpoint equals the initial diagonal.

The totals are A=15,Q_B=4,Z_B=4, so Coarse-Double holds on this walk (4<=30). The failure concerns this candidate's pointwise source bound, not the original closed-walk conjecture.

One bounded n=6 single-tree BFS located the DELETE prefix: 104 distinct trees visited, 61 expanded and 366 source requests examined. It was a connector search only, not a fitted potential, a new paired source graph or an enlarged corpus. The saved complete word and full shared-state replay are the certificate; shortest-path optimality is not needed.

## Exact matching and independent verification

The producer reuses previously pinned Ehat matching certificates when a physical pair is identical and constructs a residual graph only for other fixed evaluation points. Each value includes all forced exact pairs, a residual matching and an equal-cardinality vertex cover. Capping the resulting integer rank is a deterministic formula, not an optimization over potential labels.

independent_verify.py imports neither the producer nor its matching routine. It regenerates every proper subtree set, residual graph edge and nonedge, verifies all exact-pair constraints, and checks the matching/cover equality proving each residual maximum. It then recomputes F, Ehat, t_n and J for every source, after-A and destination state.

The verifier replays all 23 saved whole source edges through the frozen pointer engine, checks oriented events and exact d_A,d_B,a,q,z costs, and verifies the complete thirteen-operation paired closure. It also checks the realized coordinates and incompatible integer bounds in the monotone-aggregation proof. independent_audit.json reports PASS for all 39 matching values and the source audit.

All larger helper cases are handled by the inherited uniform identities and max closure, not a new fringe sample. No coefficient or cap was fitted, no larger potential system was solved, and Stage 11G was not modified.
''')
    put('CR04_STRATEGY_REVIEW.md',r'''
# Strategy review after capping the residual discount

The explicit cap repairs the requested six-key starved KEEP while retaining the three earlier named properties for one function. A new six-key consumer still refutes universality, and the same source data exclude the entire class of monotone scalar combinations between F and Ehat.

## Before and after

BEFORE: Ehat obeyed DELETE, all-size opposite-vine repayment and the established arbitrary-fringe helper laws. It failed the old six-key hook consumer: a=0,q=2,Ehat=1->2. Its helper B phase also exposed the distinction between whole-helper compensation and universal starved repayment.

RESULT: Define t_n=max(0,floor(n/2)-2) and J=max(Ehat,F-t_n). Max closure retains the DELETE bound and the whole-helper laws. The cap is determined by the analytic all-size vine inequality, not fitted from finite data; opposite-vine change is exactly -q for n>=4. At the old hook the correction J-Ehat drops from three to zero, giving J=4->2 and full q=2. The known starved L-helper phase is paid as well.

AFTER: All four named acceptance requirements hold for J. The independently registered padded-hook access has a=0,q=2 but J=3->2, where a drop of two is required. Thus J itself is REFUTED as a universal potential. Universal Coarse-Double and the existence of a complete source potential remain OPEN.

NAMED ACCEPTANCE REQUIREMENTS ACHIEVED: universal DELETE; all-size opposite vines and reflections; both established arbitrary-fringe whole-helper branches and reflections; the previously failing six-key hook KEEP and reflection. The original source inequality is proved on the union of those edge classes. Closed walks using only that explicitly restricted union satisfy Q_B<=2A by telescoping this SAME J. No assertion is made that all original walks lie in the union, or that this subclass was previously unresolved in the repository or literature.

ORIGINAL LOAD-BEARING PREMISES DISCHARGED: none. NET ADVANCEMENT OF THE FULL ORIGINAL PROOF: zero. POSITIVE PARTIAL CONTENT: the stated capped construction and four named laws. STRATEGIC ELIMINATION: all coordinatewise nondecreasing scalar functions phi_n(F,Ehat) satisfying Ehat<=phi_n<=F are excluded as universal solutions by two actual six-key B accesses.

NEW ASSUMPTIONS FOR THE ORIGINAL THEOREM: none. No unknown selector, future credit object, all-size fitting premise or compatible-label existence assertion is appended to the pipeline.

## Why another cap cannot supply the full proof

The new padded source has (F,Ehat)=(4,1), whereas the opposite-vine destination has (4,2). To pay both B demands, a normalized scalar reserve must assign the former at least four and the latter at most three. Monotonicity requires the reverse order. These are realized states reachable from the same diagonal, not extraneous symbolic constraints.

Every nonnegative scalar cap is in that excluded class: at size six opposite vines require cap>=1, while the padded source requires cap=0. Increasing the finite fit size or selecting another cap per n cannot remove this contradiction.

This is not a no-go theorem for all tree potentials. A function using additional structural information, leaving the bracket, or abandoning the stated monotonicity lies outside the theorem. Merely naming such an unspecified function would not construct it or count as proof advancement. Any future proposal must state its explicit new mechanism and prove its own source laws.

## Gate decision and stop

CR00 froze the cap formula, max-closure proofs, prior controls, new safeguard and same-witness scalar obstruction before execution. CR01 achieves the four named partial goals; CR02-CR03 provide the exact original-source failure of the full candidate and the broader architectural contradiction.

The prior subtree/matching reviews remain intact. The cap does not reset their count of non-advancing audits of the full original premise. This review records the genuine partial success without relabeling it a global theorem. Under RESEARCH_RULES, the refuted universal mechanism stops here. No other cap, scalar aggregation, weighted matching, blend, selector or enlarged finite fit is launched automatically.

The remaining original Step 3 obligation is a complete explicit function obeying both full source laws. It has not been replaced by an equally hard auxiliary premise. Downstream Dynamic Optimality assembly remains conditional.

All old reports, failures, source engines, Stage 11G graph/solvers/contracts/certificates and proof statuses remain read-only. Final source hashes, tracked state, branch and HEAD are recorded in final_integrity.json.
''')
    put('CR05_FINAL_REPORT.md',r'''
# The cap repairs the named KEEP and exposes a scalar obstruction

An explicit repair pays the previously failing six-key starved KEEP while retaining DELETE, all-size opposite-vine q and both established arbitrary-fringe whole-helper laws. It still fails another B consumer. The same source witnesses prove that no monotone scalar aggregation constrained between F and Ehat can be a universal solution.

Define

    t_n=max(0,floor(n/2)-2),
    J(A,B)=max(Ehat(A,B),F(A,B)-t_n)
          =F(A,B)-min(mu(A,B),t_n),

where mu is the residual endpoint matching rank in Ehat. The cap follows from the exact opposite-vine formulas. There are no fitted coefficients or unknown global labels.

The proved laws for the SAME J are:

* DELETE: Delta J<=d_A<=2a on every finite same-key source pair.
* Opposite vines: Delta J=-q for n>=4; smaller cases also pay q.
* Established arbitrary-fringe whole helpers: Delta J<=0 for both branches, every same-key U,V,m>=0 and reflections, by max closure of the inherited uniform laws.
* Requested old six-key starved KEEP: J=4->2 at a=0,q=2, exactly paying the required drop. Its added correction relative to Ehat drops by three.

See [the construction and uniform proofs](CR01_EXPLICIT_CAP_AND_UNIFORM_LAWS.md).

The new six-key safeguard has (F,Ehat)=(4,1)->(2,2) and a=0,q=2, but J=3->2, underpaying by one. Comparing it with opposite vines gives, for any coordinatewise nondecreasing phi_6 between Ehat and F,

    4<=phi_6(4,1)<=phi_6(4,2)<=3.

This exact contradiction excludes that entire scalar aggregation class, including every nonnegative size-dependent cap. It does not refute all structural potentials or Coarse-Double. See [the obstruction and its scope](CR02_MONOTONE_AGGREGATION_OBSTRUCTION.md).

[Independent verification](independent_audit.json) passed on 39 residual matching/cover certificates and the full thirteen-operation source replay. The closed totals A=15,Q_B=4 satisfy Coarse-Double. [Source details](CR03_EXACT_SOURCE_AND_REPLAY.md) and [reproducibility](CR06_REPRODUCIBILITY.md) are saved here.

The [four-rule gate](CR00_FOUR_RULE_GATE.md) preceded execution, and the [updated strategy review](CR04_STRATEGY_REVIEW.md) stops further scalar variants. No larger finite fits or Stage 11G edits occurred. The full source potential and Universal Coarse-Double remain open.
''')
    put('CR06_REPRODUCIBILITY.md',r'''
# Reproducing the capped residual audit

The scripts use Python's standard library and the frozen source engines. No packages are installed. From the repository root, the original invocations were

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_capped_residual_20261031_v001/audit_capped_residual.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_capped_residual_20261031_v001/independent_verify.py
```

Outputs use exclusive creation. Do not rerun in this populated directory. To reproduce, copy the scripts into a fresh versioned sibling under DIRECT_U4_PARALLEL_RESEARCH and substitute its path in the commands. Preserve the prior fixed-exact-pair and clade-correction input directories.

The producer reuses the prior fixed Ehat source controls and their residual matching certificates, adds a derived already-known starved helper phase, and evaluates one new six-key padded source. Its one bounded six-key single-tree BFS only locates a DELETE prefix for the source closure. No larger helper sample, expanded potential system, parameter search or source-state pair graph is used.

capped_residual_certificate.json contains all complete source states and oriented events, residual matching/covers and their origin, deterministic cap values, the exact scalar-obstruction coordinates, the connector word and full thirteen-operation paired replay. Matching graphs are current-pair ingredients of the function, not fitted source potential labels.

independent_verify.py does not import the producer or call a matching solver. It regenerates residual vertices and adjacencies, verifies every matching/cover equality, recomputes all cap values, checks the forced scalar bounds and coordinate comparison, and independently replays the frozen pointer source with exact paired closure.

The all-size laws in CR01 follow from the prior source proofs and exact max/cap identities. The two scalar inequalities in CR02 are actual fixed source obligations, not a finite-fit extrapolation. The independent audit certifies the finite data used by those analytic arguments.

entry_source_pins.json records fifteen inherited hashes, HEAD and branch. integrity.json checks them after evaluation; final_integrity.json checks them at delivery. delivery_manifest.json hashes the new output files, excluding itself. Existing proofs, certificates, failures, source engines, Stage 11G assets and statuses remain read-only.
''')
    js('proof_status_ledger.json',{'date':'2026-10-31','candidate':'J=max(Ehat,F-t_n)=F-min(mu,t_n), t_n=max(0,floor(n/2)-2)',
      'claims':[
        {'claim':'J is explicit and Ehat<=J<=F','status':'SOURCE DEFINITION','proof':'CR01_EXPLICIT_CAP_AND_UNIFORM_LAWS.md'},
        {'claim':'Universal DELETE for J','status':'PROVED—UNIVERSAL','scope':'all finite same-key present-key source pairs; Delta J<=d_A<=2a','proof':'CR01_EXPLICIT_CAP_AND_UNIFORM_LAWS.md'},
        {'claim':'Full opposite-vine q','status':'PROVED—RESTRICTED DOMAIN','scope':'all sizes and both orientations; exact -q for n>=4, boundaries separately paid','proof':'CR01_EXPLICIT_CAP_AND_UNIFORM_LAWS.md'},
        {'claim':'Established arbitrary-fringe whole-helper compensation','status':'PROVED—RESTRICTED DOMAIN','scope':'both RA02 branches, arbitrary same-key U,V,m>=0 and reflections; Delta J<=0','proof':'CR01_EXPLICIT_CAP_AND_UNIFORM_LAWS.md'},
        {'claim':'Requested old six-key starved KEEP is paid','status':'FINITE-EXACT','scope':'a=0,q=2,J=4->2; reflection follows by source/function invariance','proof':'independent_audit.json'},
        {'claim':'Known starved phase of empty L helper is paid','status':'FINITE-EXACT','scope':'a=0,q=2,J=4->2; derived from inherited physical states','proof':'independent_audit.json'},
        {'claim':'J is a universal full-repayment source potential','status':'REFUTED—EXACT','scope':'new reachable six-key padded KEEP: a=0,q=2,J=3->2','proof':'CR02_MONOTONE_AGGREGATION_OBSTRUCTION.md'},
        {'claim':'A monotone scalar aggregation between Ehat and F can supply universal B repayment','status':'REFUTED—EXACT','scope':'any coordinatewise nondecreasing phi_n(F,Ehat) with Ehat<=phi_n<=F; contradiction at n=6','proof':'CR02_MONOTONE_AGGREGATION_OBSTRUCTION.md'},
        {'claim':'Capped values, residual maxima and full source replay','status':'FINITE-EXACT','scope':'39 residual graphs;10 controls;13-operation closed replay;23 whole source edges','proof':'independent_audit.json'},
        {'claim':'Complete uniform source potential','status':'OPEN','scope':'this candidate and aggregation class do not resolve it'},
        {'claim':'Universal Coarse-Double','status':'OPEN','scope':'no universal proof or counterexample'},
        {'claim':'Downstream Dynamic Optimality assembly','status':'CONDITIONAL','scope':'inherited original premises unchanged'}],
      'four_named_requirements_achieved':['pay the known six-key starved KEEP','universal DELETE','all-size opposite-vine q','established arbitrary-fringe whole-helper compensation'],
      'covered_restricted_source_cases':'union of named edge classes and reflections; closed walks in this union obey Coarse-Double by telescoping J',
      'original_load_bearing_obligations_discharged':[],'net_advancement_of_full_original_proof':0,
      'strategic_elimination':'all normalized monotone scalar aggregations of F and Ehat as universal potentials',
      'new_assumptions_for_original_theorem':[],'updated_strategy_review':'CR04_STRATEGY_REVIEW.md','next_automatic_campaign':None,
      'finite_potential_fits':0,'new_pair_state_graphs':0,'Stage11G_writes_performed':False})
    print(json.dumps({'reports_written':4,'ledger_written':True,'four_named_laws':'achieved on stated domains',
      'full_potential':'refuted','monotone_scalar_class':'refuted as a universal solution','independent_audit':'PASS'}))

if __name__=='__main__':main()
