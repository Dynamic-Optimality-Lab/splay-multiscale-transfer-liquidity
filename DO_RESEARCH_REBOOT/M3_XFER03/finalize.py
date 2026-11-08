"""Result/resource/integrity publication only; no mathematical tests."""
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
    assert a['status']=='UNIVERSAL_BURIED_CUT_THREE_CLAUSE_AUDIT_PASS'
    assert a['each_operation_preserves_each_previously_valid_LOW_inequality']
    assert a['all_final_L_and_T_LOW_sources_proved'] and a['S_LOW_coverage_requires_final_debt_at_most1']
    assert not a['all_S_debt2_sources_claimed'] and not a['buried_port_reconstructed_or_persistent_witness_assumed']
    assert not a['all_buried_states_or_M3_solved'] and not a['full_compiler_formalization_claimed']
    assert a['new_finite_tests']==a['new_source_transition_queries']==a['new_original_root_evaluations']==0
    assert r['child_CPU']<r['allocated_cap']<=120
    charge=r['child_CPU']+e['whole_process_CPU_seconds'];total=756.859375+charge
    assert total<7200-5
    resources={
        'prior_uniform_CPU_charge_retained':756.859375,'new_symbolic_checker_CPU':r['child_CPU'],
        'new_controller_CPU_through_finally':e['whole_process_CPU_seconds'],'new_compute_CPU':charge,
        'cumulative_accounted_CPU':total,'finite_CPU_ceiling':7200,'guaranteed_remaining_CPU':7200-total,'reserve':5,
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
        'RESEARCH_RULES.md','M3_XFER02/CUT_PAIR_THEOREM.md','M3_XFER02/PROOF_AUDIT.md',
        'M3_XFER02/resources.json','M3_XFER02/final_manifest.json',
        'M3_XFER01/SATURATION_THEOREM.md','M3_XFER01/PROOF_AUDIT.md',
        'M3_E1_01/E1_THEOREM.md','M3_E1_01/OUTSIDE_E1.md','M3_E1_01/PROOF_AUDIT.md',
        'M3_AER01/RESULT.md','M3_EXPOSURE02/HELPER_REDUCTION.md','M3_EXPOSURE02/ADDENDUM_RANGE_ARGUMENT.md',
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
        'status':'PROVED_UNIVERSAL_THREE_CLAUSE_LOW_SAFE_OPERATION_AND_RESTRICTED_BURIED_CUT_REPAYMENT',
        'small_end_pair':'two smallest marked a<b, b in4/5',
        'large_end_pair':'two largest marked a<b, a in3/4; order-dual guards',
        'L':'port source root b,aLL,b.right PORT,V={a}; dual root a,bRR,a.left PORT',
        'T':'buried boundary root a,bRR,V={b},Bdepth(b)<=3; dual root b,aLL,Bdepth(a)<=3',
        'S':'release root b,aLL,Bdepth(a)<=3,other marks allowed; dual root a,bRR,Bdepth(b)<=3',
        'input_class':'explicit public Lambda<=D<=2; no global feasibility premise',
        'three_ordered_operations':['max(D,1_S)','max(previous,2_T)','max(previous,2_L)'],
        'final_explicit_debt':'D_cut=max(D_R,1_S,2_T,2_L)',
        'each_previously_valid_LOW_inequality_preserved':True,
        'new_all_LOW_source_coverage':['L','T','S only where FINAL D_cut<=1'],
        'previous_Q_R_LOW_coverage_preserved':True,
        'all_missing_LL_RR_port_sources_outside_E1_for_extreme_pair_covered':True,
        'central_root_auxiliary':'Gamma1 source core r in[3,5] has w>=1',
        'fresh_hidden_branch_marked_exposure_allowed':True,
        'lost_port_inferred_or_private_witness_persisted':False,
        'incoming_protected_transfers':'0/+1 to L/T; +1 to S; zero to S from source<=1',
        'covered_walk_LOW_sources':'Q union R union L union T union{S:D_cut<=1}',
        'finite_walk_bound':-7,'full_state_closed_walk_bound':0,
        'remaining_open':['uncovered S debt2 zero releases','buried states without T B-depth guard','other marked configurations and noncovered LOW sources'],
        'all_S_debt2_solved':False,'full_M3_status':'OPEN','DynamicOptimality_status':'OPEN',
        'new_whole_signature_certificates':0,'original_negative_cycle_certified':False,
        'new_finite_tests':0,'R1_R4_preserved':True,'h0_correction_preserved':True,
        'full_compiler_formalization_claimed':False,
        'NET_ADVANCEMENT':'two-credit same-direction burial/return plus one-credit marked-exposure release, with precise S2 frontier',
        'resources':resources,'integrity':integrity,
    }
    write('certificate.json',cert)
    report=f'''# Buried cut: burial and return proved; two-credit release still open

The missing same-direction LL/RR cut-burial transfers are proved and
independently symbolically audited, with NO finite tests. The construction
does not infer the depth3 port from alpha or persist a private witness.

It adds three explicit public clauses to D_R:

    D_cut=max(D_R,1_S,2_T,2_L).

L is the observed port source with the other extreme-pair mark at LL/RR;
T is the resulting buried boundary with a shallow B return target; S is
the return state, where further marked keys may now be visible. For the
two smallest marked keys, the central source root is4/5; the largest-pair
dual uses3/4. Counting proves that these include all missing same-direction
port sources OUTSIDE E1 for those extreme marked pairs.

All original LOW edges from L and T are covered, including relevant H2
forms. S is covered when its FINAL debt is at most1. The former port can
become actual marked nodes in a fresh T witness: the return is still safe.
A new exact core-count/rotation argument handles its zero-weight release
into E1 at one credit, including the source-slot0 alias cases.

Each of the three ordered max operations preserves every previously valid
LOW inequality. Thus Q/R coverage stays valid. The inherited HIGH/h0 glue
gives finite walks>=-7 and full closed walks>=0 whenever LOW sources are
in Q,R,L,T or S with final debt<=1. Full147-O/127-M closure and SAME actual
midpoint/private scopes are retained. This is a restricted source theorem.

IMPORTANT LIMIT: general S debt2 releases are NOT proved. Nor are arbitrary
buried states without the T B-depth guard or other marked configurations.
T lies in E1, but its new debt2 theorem goes beyond the old one-credit
augmentation; the latter was never a proof of every E1 debt2 source.
Full M3/Dynamic Optimality remain OPEN; no negative cycle or new whole-
signature certificate is claimed.

See BURIED_CUT_THEOREM.md and PROOF_AUDIT.md for all public guards, complete
original LOW coverage, counter-scope and the independent audit. It verifies
16 universal four-core spine schemas with order-duals, arbitrary A terms,
alias-owner behavior and count/slack identities. No numerical core trees,
population instances, source roots or proposed labels were tested. Completed
semantic proofs/checks were reused, not replayed. The audit is not a full
formalization of the original compiler.

R1-R4/current caps, weak LE/G/unused fields, free high v and corrected h0
remain. All{len(pins)} pinned prior files and Git HEAD/tracked tree are
unchanged. New charged CPU={charge}; cumulative={total}/7200s; remaining
{7200-total} including reserve5. New finite tests/source queries/roots=0.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as stream:stream.write(report)
    cert['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    write('final_manifest.json',cert)
    print(json.dumps({'status':cert['status'],'M3':'OPEN','new_compute_CPU':charge,'cumulative_CPU':total,'remaining_CPU':7200-total,'integrity':integrity},indent=2),flush=True)
if __name__=='__main__':main()
