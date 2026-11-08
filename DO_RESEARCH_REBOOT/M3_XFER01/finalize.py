"""Publish proof/audit/resource provenance; no mathematical tests."""
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
    assert a['status']=='UNIVERSAL_OPAQUE_PREFIX_SATURATION_AUDIT_PASS'
    assert a['simultaneous_h_target2_proved'] and not a['marked_root_destination_c2_assumed']
    assert a['reverse_weight_depth1']==2 and a['reverse_weight_depth2']==1
    assert not a['all_H1_transfers_solved'] and not a['full_compiler_formalization_claimed']
    assert r['new_child_process_CPU']<r['allocated_cap']<=120
    charge=r['new_child_process_CPU']+e['whole_process_CPU_seconds'];total=756.140625+charge
    assert total<7200-5
    resources={
        'prior_uniform_CPU_charge_retained':756.140625,
        'new_symbolic_checker_CPU':r['new_child_process_CPU'],
        'new_controller_CPU_through_finally':e['whole_process_CPU_seconds'],
        'new_compute_CPU':charge,'cumulative_accounted_CPU':total,
        'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'reserve':5,
        'old_signature_campaign_ledger_unchanged':7195.203125,
        'new_finite_population_tests':0,'new_source_transition_queries':0,
        'new_original_root_evaluations':0,'new_label_fits':0,'new_bank_censuses':0,
        'completed_semantic_checks_replayed':0,'symbolic_phase_CPU_cap':120,
        'construction_CPU_cap':300,'audit_source_CPU_cap':300,
        'canonical_query_live_record_limit':2000000,'DAG_limit':4000000,
        'stored_edge_limit':5000000,'RAM_GiB_limit':32,'current_caps_preserved':True,
        'metadata_hashing_convention':'entry/final immutable-file bookkeeping excluded as previously',
    }
    write('resources.json',resources)
    dependencies=[
        'RESEARCH_RULES.md','M3_E1_01/E1_THEOREM.md','M3_E1_01/OUTSIDE_E1.md',
        'M3_E1_01/PROOF_AUDIT.md','M3_E1_01/resources.json','M3_E1_01/final_manifest.json',
        'M3_AER01/RESULT.md','M3_EXPOSURE02/HELPER_REDUCTION.md',
        'M3_EXPOSURE02/ADDENDUM_RANGE_ARGUMENT.md','M3_COMB_AUD01/AUDIT_REPORT.md',
        'M3_POP5_RISK01/SOURCE_LIFT.md','M3_LDR01/full_run_controls.json',
        'M3_LDR01/zero_reset_control.json','M3_UNITPAIR01/B_bank.json',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_SOURCE_REPAIRS.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_INVENTORY.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py',
        '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_H2R01_TERMINAL_DEBT_REPAYMENT.md',
    ]
    write('dependencies.json',{'completed_proofs_reused_not_replayed':True,'files':[{'path':(BASE.parent/n).as_posix(),'sha256':sha(BASE.parent/n)} for n in dependencies]})
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
        'status':'PROVED_UNIVERSAL_SAFE_SATURATION_AND_RESTRICTED_LOW_WALK_THEOREM',
        'Q_source':'root Score r, one marked Score child x!=r, other nonroot alpha positions port/empty',
        'explicit_debt':'D_Q=max(Lambda,h), h=Q*min(2,2-floor(depth_B(x)/2)+2)',
        'private_inventory_independent':True,
        'original_H1_augmentation':'for Lambda<=D<=2, max(D,h) preserves each previously valid H1 inequality',
        'original_LOW_coverage':'ALL original LOW edges with source Q',
        'Gamma1_source_Q':'impossible; exactly two present real A nodes, both Scores',
        'Gamma0':'completed actual-preterminal floor/range proof reused',
        'outside_E1_debt_by_unique_target_depth':{'4_or5':2,'6_or7':1,'8':0},
        'incoming_weight0_and1_to_Q_depth4_5':'PROVED',
        'incoming_weight1_to_Q_depth6_7':'PROVED',
        'incoming_weight0_to_Q_depth6_7':'PROVED when source debt<=1',
        'finite_walk_bound_for_LOW_sources_Q':-7,'closed_walk_bound_for_LOW_sources_Q':0,
        'all_H1_transfers_solved':False,'non_Q_exposing_transfers':'OPEN',
        'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
        'new_signature_certificates':0,'original_negative_cycle_certified':False,
        'new_finite_tests':0,'R1_R4_preserved':True,'corrected_h0_preserved':True,
        'proof_correction_recorded_before_audit':'PRE_EXECUTION_v2.md',
        'independent_audit':'universal symbolic terms/slacks plus analytic source proof; not full compiler formalization',
        'NET_ADVANCEMENT':'explicit safe debt on Q and source-complete restricted signed-walk theorem for arbitrary signatures',
        'resources':resources,'integrity':integrity,
    }
    write('certificate.json',cert)
    report=f'''# Restricted outside-E1 transfers proved; general transfers remain open

An explicit public saturation and a restricted signed-walk theorem are
proved and independently symbolically audited, with NO finite tests.

Q is the opaque two-core source shape: a core root r, one marked core
child x, and three port/empty side cuts. It can hide arbitrary compatible
Score/anonymous inventories. Define h=min(2,w_x+2) on Q, zero elsewhere,
and D_Q=max(Lambda,h), using the completed E1/capacity seed Lambda.

For every public Lambda<=D<=2, max(D,h) preserves all its already valid
original H1 inequalities individually. All Q-source H1 edges are directly
valid for D_Q. Simultaneous saturation gives the successor debt2; this
uses reverse weights2/1 at B depths1/2, correcting the draft arithmetic
before the single independent audit ran.

Outside E1, Q targets at B depths4/5 get source debt2 and their weight0
exit preserves debt2. All incoming weight0/+1 transfers to these states
are safe. At depths6/7 the source debt is1: incoming+1 transfers are safe,
as are zero transfers from debt<=1. At depth8 it remains0. These are
universal structural deductions, not population samples or label fits.

Q has only two present real A nodes, both Scores, so no Gamma1 anonymous
helper can occur; H2/Gamma0 reuses the completed range/floor law. Hence
EVERY original LOW edge with Q source satisfies the signed inequality.
The inherited universal HIGH glue/h0 correction gives finite walks>=-7
and fully closed walks>=0 whenever all LOW sources satisfy Q. This is
a restricted-domain theorem for arbitrary compatible signatures, not M3.

Non-Q transfers that expose more visible structure remain OPEN. The
explicit seed is not claimed globally valid; no new signature certificate
or original negative cycle is claimed. Full M3/Dynamic Optimality OPEN.

See SATURATION_THEOREM.md and PROOF_AUDIT.md for the complete proof,
quantifiers, semantic lift, dependencies, corrected arithmetic and limits.
The independent checker uses arbitrary symbolic terms/slacks and AST
provenance; it is not a full formalization of the original compiler.
Completed proofs were reused. New finite tests/source transition queries/
original root evaluations/label fits/bank censuses=0.

R1-R4, full147-O/127-M closure, independent witnesses/SAME midpoint,
weak LE/G/unused fields, free high v and corrected h0 preserved.
All{len(pins)} pinned prior files and Git HEAD/tracked tree are unchanged.
Charged CPU this campaign={charge}; cumulative={total}/7200 seconds;
remaining={7200-total}, including the5-second reserve. Caps unchanged.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',cert)
    print(json.dumps({'status':cert['status'],'M3':'OPEN','new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)

if __name__=='__main__':main()
