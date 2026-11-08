"""Immutable result/resource publication; no mathematical tests."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def read(name):return json.loads((BASE/name).read_text())
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def main():
    assert not (BASE/'final_manifest.json').exists()
    r,e,a=read('run_result.json'),read('controller_exit.json'),read('symbolic_audit.json')
    assert r['status']=='PASS' and r['error'] is e['error'] is None
    assert a['status']=='UNIVERSAL_CUT_PAIR_LOW_AUGMENTATION_AUDIT_PASS'
    assert a['new_R_sources_all_LOW_proved'] and a['individual_previously_valid_LOW_inequalities_preserved']
    assert not a['helper_Score_empty_premise_used'] and not a['all_transfers_or_M3_proved']
    assert a['B_old_root_final_depth_bound']==3 and a['allowed_Gamma1_other_terminal_schemas_with_duals']==8
    assert r['child_CPU']<r['allocated_cap']<=120
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=756.5+charge
    assert total<7200-5
    resources={
        'prior_uniform_CPU_charge_retained':756.5,'new_symbolic_checker_CPU':r['child_CPU'],
        'new_controller_CPU_through_finally':e['whole_process_CPU_seconds'],
        'new_compute_CPU':charge,'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,
        'guaranteed_remaining_CPU':7200-total,'reserve':5,
        'old_signature_campaign_ledger_unchanged':7195.203125,
        'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
        'new_label_fits':0,'new_bank_censuses':0,'completed_semantic_checks_replayed':0,
        'symbolic_phase_CPU_cap':120,'construction_CPU_cap':300,'audit_source_CPU_cap':300,
        'canonical_query_live_record_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,
        'RAM_GiB_limit':32,'current_caps_preserved':True,
        'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously',
    }
    write('resources.json',resources)
    names=[
        'RESEARCH_RULES.md','M3_XFER01/SATURATION_THEOREM.md','M3_XFER01/PROOF_AUDIT.md',
        'M3_XFER01/symbolic_audit.json','M3_XFER01/resources.json','M3_XFER01/final_manifest.json',
        'M3_E1_01/OUTSIDE_E1.md','M3_E1_01/PROOF_AUDIT.md','M3_AER01/RESULT.md',
        'M3_EXPOSURE02/HELPER_REDUCTION.md','M3_EXPOSURE02/ADDENDUM_RANGE_ARGUMENT.md',
        'M3_POP5_RISK01/SOURCE_LIFT.md','M3_COMB_AUD01/AUDIT_REPORT.md','M3_UNITPAIR01/B_bank.json',
        '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_H2R01_TERMINAL_DEBT_REPAYMENT.md',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_SOURCE_REPAIRS.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_INVENTORY.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py',
    ]
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,'files':[{'path':(BASE.parent/n).as_posix(),'sha256':sha(BASE.parent/n)} for n in names]})
    old=read('entry_baseline.json');pins={v['path'] for v in old['files']}
    for i,v in enumerate(old['files']):
        assert sha(Path(v['path']))==v['sha256'],v['path']
        if (i+1)%1000==0:print(json.dumps({'prior_files_unchanged':i+1,'total':len(pins)}),flush=True)
    additions=[p for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in pins]
    assert all('/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/' in p.as_posix() for p in additions),[p.as_posix() for p in additions]
    write('concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==old['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    integrity={'status':'PASS','old_files_unchanged':len(pins),'HEAD':old['head'],'tracked_tree_clean':True,'this_campaign_writes_confined_here':True,'unrelated_concurrent_U4_additions':len(additions)}
    write('integrity.json',integrity)
    cert={
        'status':'PROVED_UNIVERSAL_LOW_SAFE_OPERATION_AND_RESTRICTED_Q_UNION_R_WALK_THEOREM',
        'R_small_end':'two smallest marked a<b; root b with a at L/LR and b.right PORT, or root a with b at R and b.right PORT',
        'R_large_end':'two largest marked a<b; root a with b at R/RL and a.left PORT, or root b with a at L and a.left PORT',
        'additional_guards':'root sync, valid core B, V exactly the other pair member',
        'explicit_operation':'F=max(D,h_R), h_R=min(2,w_x+2) on R,0 elsewhere',
        'operation_premises':'public psi<=D<=2; no global feasibility assumption',
        'each_previously_valid_original_LOW_inequality_preserved':True,
        'Score_bearing_Gamma1_helpers_included':True,
        'private_inventory_invariance_or_extremizer_transport_assumed':False,
        'B_after_extreme_helper_then_other_core_old_root_depth_at_most':3,
        'explicit_combined_debt':'D_R=max(D_Q,h_R)',
        'LOW_source_coverage':'ALL original LOW edges with source in Q union R',
        'protected_incoming_LOW_transfers':'weights0/+1 to debt2 R; +1 to debt1 R; zero to debt1 R from source<=1',
        'finite_walk_bound_when_LOW_sources_in_Q_union_R':-7,
        'full_state_closed_walk_bound_when_LOW_sources_in_Q_union_R':0,
        'remaining_open':['cut below depth-two shadow','additional exposed marked targets','other non-Q/non-R H1/H2 transfers'],
        'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
        'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
        'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
        'full_compiler_formalization_claimed':False,
        'NET_ADVANCEMENT':'LOW-safe public clause handles anonymous exposure and Score-bearing helper sources in R, preserving completed Q coverage',
        'resources':resources,'integrity':integrity,
    }
    write('certificate.json',cert)
    report=f'''# Cut-separated marked pair: new LOW-safe repayment theorem

A larger class beyond opaque two-core Q is proved and independently
symbolically audited. It allows newly exposed anonymous/unmarked nodes
and includes Score-bearing H2/Gamma1 helpers. No finite tests were run.

The two smallest marked keys a<b are separated from all other marked
keys by an observed PORT at b.right. Root b may have a at L or LR;
root a may have b at R. Include the order-dual for the largest marked
pair and a.left PORT. These guards use only the frozen shared state.

Set h_R=min(2,w_x+2) on this region R,0 elsewhere. For EVERY public
psi<=D<=2, max(D,h_R) preserves each previously valid ORIGINAL LOW
inequality, including Score-bearing helpers. It assumes no globally
feasible D. This is stronger than an H1-only augmentation.

The explicit D_R=max(D_Q,h_R) satisfies ALL LOW edges with source in
Q union R. Outside E1, unique-target B depths4/5 give debt2 and safe
zero-weight exits/incoming0/+1 transfers; depths6/7 give debt1 and
safe incoming+1 transfers (zero incoming requires source<=1).
The proof permits fresh anonymous exposure while the separating port
remains observed. A new symbolic B lemma bounds the entry core's
depth by3 after an extreme helper and a different core access, giving
the required destination debt2. Actual H2,H/q/weights are unchanged.

The existing HIGH glue gives finite walks>=-7 and fully closed walks>=0
when every LOW source lies in Q union R. This is a RESTRICTED DOMAIN
theorem for arbitrary compatible signatures. It does not prove all
remaining transfers or M3. Cases with the cut below the visible shadow,
additional marked targets, and other non-Q/non-R sources remain OPEN.
No new whole-signature certificate or original negative cycle is claimed.

See CUT_PAIR_THEOREM.md and PROOF_AUDIT.md. The independent audit checks
six H1, eight allowed helper and four excluded helper schemas (including
duals), arbitrary-depth B parity/order branches and signed residuals.
Analytic nonvacuity includes a Score-bearing helper family with weights
0/+1 outside E1/Q; no new finite source/root test or label lookup is used.
Source semantic dependencies are reused; this is not a full compiler
formalization. All previous completed checks are preserved, not replayed.

R1-R4/current caps, weak LE/G/unused fields, full147-O/127-M closure,
independent witnesses/SAME midpoint/free high v and corrected h0 remain.
All{len(pins)} pinned prior files and Git HEAD/tracked tree are unchanged.
New charged CPU={charge}; cumulative={total}/7200s; remaining={7200-total}
including reserve5. New finite tests/source queries/root evaluations=0.
Full M3 and Dynamic Optimality remain OPEN.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',cert)
    print(json.dumps({'status':cert['status'],'M3':'OPEN','new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)
if __name__=='__main__':main()
