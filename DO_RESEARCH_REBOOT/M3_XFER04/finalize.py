"""Immutable publication/resource bookkeeping only; no mathematical tests."""
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
    assert a['status']=='UNIVERSAL_TWO_CREDIT_RELEASE_CAPACITY_AUDIT_PASS'
    assert a['all_J_source_LOW_inequalities_proved'] and a['each_previously_valid_LOW_inequality_preserved']
    assert a['observed_Score_separator_required'] and not a['RR_lost_separator_and_other_B_patterns_claimed']
    assert a['Gamma1_weight_at_least2_including_Score_bearing_helpers']
    assert a['old_saved_psi_values_queried']==0 and not a['all_debt2_releases_or_M3_solved']
    assert not a['full_compiler_formalization_claimed']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    assert r['child_CPU']<r['allocated_cap']<=120
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=757.21875+charge
    assert total<7200-5
    resources={
        'prior_uniform_CPU_charge_retained':757.21875,'new_symbolic_checker_CPU':r['child_CPU'],
        'new_controller_CPU_through_finally':e['whole_process_CPU_seconds'],'new_compute_CPU':charge,
        'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'reserve':5,
        'old_signature_campaign_ledger_unchanged':7195.203125,
        'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
        'new_label_fits':0,'new_bank_censuses':0,'completed_semantic_checks_replayed':0,'old_saved_psi_values_queried':0,
        'symbolic_phase_CPU_cap':120,'construction_CPU_cap':300,'audit_source_CPU_cap':300,
        'canonical_query_live_record_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,
        'RAM_GiB_limit':32,'current_caps_preserved':True,
        'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously',
    }
    write('resources.json',resources)
    names=[
        'RESEARCH_RULES.md','M3_XFER03/BURIED_CUT_THEOREM.md','M3_XFER03/PROOF_AUDIT.md',
        'M3_XFER03/resources.json','M3_XFER03/final_manifest.json',
        'M3_XFER02/CUT_PAIR_THEOREM.md','M3_XFER02/PROOF_AUDIT.md',
        'M3_XFER01/SATURATION_THEOREM.md','M3_E1_01/E1_THEOREM.md','M3_E1_01/OUTSIDE_E1.md',
        'M3_AER01/RESULT.md','M3_EXPOSURE02/HELPER_REDUCTION.md','M3_EXPOSURE02/ADDENDUM_RANGE_ARGUMENT.md',
        'M3_POP5_RISK01/SOURCE_LIFT.md','M3_COMB_AUD01/AUDIT_REPORT.md','M3_UNITPAIR01/B_bank.json',
        '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md',
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
        'status':'PROVED_UNIVERSAL_LOW_SAFE_TWO_CREDIT_RELEASE_AUGMENTATION_RESTRICTED_J5_J6',
        'J':'exact J5/J6 core patterns, observed Score4 at L, unmarked Score k at LL with first mark a<k<4; order-duals',
        'input_class':'public Lambda<=D<=2; no global feasibility assumption',
        'operation':'F=max(D,2*1_J)',
        'explicit_combined_debt':'D_release=max(D_cut,2*1_J)',
        'all_J_source_original_LOW_inequalities_proved':True,
        'each_previously_valid_original_LOW_inequality_preserved':True,
        'new_incoming_LOW_cases':'all nonnegative LOW edges ending in J, including debt2 P5/P6 zero releases at A R/RL',
        'Score_bearing_Gamma1_helpers_covered':True,
        'debt2_source_nonvacuity':'exact ordered-symbol depth8 predecessors plus completed psi law force source psi=2',
        'old_D_cut_refuted_at_target_claimed':False,
        'private_inventory_or_gap_color_inferred':False,
        'previous_coverage_preserved':'Q/R/L/T/S1 and all other previously valid D_cut LOW rows',
        'covered_walk_LOW_legs':'previous covered legs OR J-source legs OR nonnegative legs ending in J',
        'finite_walk_bound':-7,'full_state_closed_walk_bound':0,
        'remaining_open':['anonymous separator','RR loss of observed separator','other upper-spine/core arrangements','general debt2/+1 releases'],
        'all_debt2_releases_solved':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
        'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
        'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
        'full_compiler_formalization_claimed':False,
        'NET_ADVANCEMENT':'two original debt2 zero-release families now have a LOW-safe public debt2 successor, with outgoing +1 and H2 rows proved',
        'resources':resources,'integrity':integrity,
    }
    write('certificate.json',cert)
    report=f'''# Two debt2 zero-release families closed; general releases remain open

A public two-credit successor rule is proved and independently symbolically
audited for J5/J6 and their order-duals. No finite tests were run. The new
rule handles the specified P5/P6 weight0 releases from a debt2 S source
when the A target is at R/RL and the observed separator is an unmarked
Score k. It retains debt2 at the successor, giving residual0.

The explicit augmentation is D_release=max(D_cut,2*1_J). Every original
LOW edge with source in J is proved, including outgoing+1 and Score-bearing
H2/Gamma1 helpers. Each previously valid LOW inequality remains valid;
all Q/R/L/T/S1 coverage is preserved. The proof requires no hidden private
color, completion coupling or persistent witness.

The paid exits have weight2; the+1 exits have exact E1 successors carrying
at least1. The only possible extreme helper pushes the lower marked key
deeper, and eligible terminals stay in a five-core group, giving w2>=2.
Gamma0 reuses its completed actual-preterminal floor proof. Exact ordered-
symbol negative predecessors force psi=2 at nonempty source families,
so this is genuine debt2 coverage rather than a vacuous conditional.
No saved psi labels or original roots were queried to prove this.

The inherited HIGH/h0 law yields finite walks>=-7 and full closed walks>=0
when LOW legs are previous covered cases or the new J-source/nonnegative-
incoming cases. Full147-O/127-M closure, SAME midpoint and independent
witnesses remain literal. This is a restricted theorem, not full M3.

Still OPEN: anonymous separators, A-RR releases that lose the separator,
other upper-spine/core arrangements and general debt2/+1 releases. No old
candidate refutation, original negative cycle or new whole-signature
certificate is claimed. Full M3 and Dynamic Optimality remain OPEN.

See RELEASE_CAPACITY_THEOREM.md and PROOF_AUDIT.md for the exact public
guards, core patterns and complete LOW proof. The checker verifies exact
identities on unassigned ordered symbols/arbitrary subtree variables,
alias-owner visibility, helper terminal bounds and signed slacks. It is
not a full compiler formalization. Completed semantic checks are reused,
not replayed. Numerical populations/trees/proposed labels are not tested.

R1-R4/current caps, weak LE/G/unused fields/free high v and corrected h0
are preserved. All{len(pins)} pinned prior files and Git HEAD/tracked tree
are unchanged. New charged CPU={charge}; cumulative={total}/7200s;
remaining={7200-total} including reserve5. New finite tests/source
queries/root evaluations/label fits/bank censuses=0.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',cert)
    print(json.dumps({'status':cert['status'],'M3':'OPEN','new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)
if __name__=='__main__':main()
