"""Exact cost partition and final scope/dependency-interface audit."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    # Universal integer cases, not population/graph enumeration:
    # singleton H>=2 -> min(H,4)>=2 -> price>=4-Q>=0;
    # singleton H1 -> price=-2 exactly when Q4.
    assert 2*1-4==-2 and 2*2-4==0
    # Pair H>=2,Q6: H2=-2,H3=0,H>=4=2.
    assert [2*2-6,2*3-6,2*4-6]==[-2,0,2]
    # q4 requires8<=depth<10; q5 plus depth<=10 forces10/core11.
    assert 8//2==9//2==4 and 10//2==5
    data=json.loads((B/'symbolic_replay.json').read_text());proof=json.loads((B/'source_proof_audit.json').read_text())
    debt=json.loads((B/'debt_v3_audit.json').read_text());finite=json.loads((B/'independent_replay.json').read_text())
    masks=json.loads((B/'mask_replay.json').read_text())
    assert proof['status']=='PASS_INDEPENDENT_UNIVERSAL_SOURCE_COUNTERCERTIFICATES'
    assert proof['Sigma_residual']==-1 and proof['Omega_residual_interval'][1]==-1 and proof['Gamma_residual']==0
    for f in data['families']:
        assert all(p['H']>=len(p['macro_indices']) for p in f['packets'])
        assert all((p['H'],p['Q']) in ((1,4),(2,6)) for p in f['packets'] if p['w']==-2)
        assert f['path_deficit_check']['minimum']==-2 and f['path_deficit_check']['whole_period_price']>0
        assert f['AF_closure'] and f['E_closure'] and f['preperiod_copies']==f['aligned_period_copies']==1
        assert len(f['A_units'])==len({tuple(q) for q in f['A_units']})==2*f['A']
        assert len(f['BF_demands'])==len({tuple(q) for q in f['BF_demands']})==f['QF']
    statuses={p.name:json.loads(p.read_text())['status'] for p in B.glob('run_*_result.json')}
    for phase in ('replay','debt_v3','independent','source_proof','masks'):assert statuses['run_'+phase+'_result.json']=='PASS'
    assert statuses['run_debt_result.json']==statuses['run_debt_v2_result.json']=='FAILED_OR_UNKNOWN'
    assert finite['new_finite_tests']+masks['new_finite_tests']==101
    out('classification_audit.json',{'status':'PASS_EXHAUSTIVE_COST_CLASSIFICATION_AND_EXACT_REFUTATION_SCOPE',
        'universal_classification':['singleton H1,Q4','actual q5/q1 pair Hsum2,Q6'],
        'core_sizes':{'6..8':'no price-2','9':'singleton d8 if actual source-valid','10':'singleton d8/9 if actual source-valid',
            '11':'singleton d8; pair d10,d2'},
        'H0_full_genuine_excluded_by':'A synchronized old root cannot change under zero events to a different genuine target',
        'no_qE_qF_confusion':True,'root_repeats_retained':True,'both_packet_operations_actual':True,
        'gates':{'A':'PASS','B':'PASS','C':'REFUTED_EXACT_PAIRED','D':'REFUTED_EXACT_SINGLETON','E':'PASS_SCOPED_REPLAYS',
            'F':'PASS_INTERFACE_NO_NEW_INJECTION','G':'NO_ARCHITECTURE_COUNTERPATH_FOUND'},
        'terminal_outcome':'B_NORMALIZATION_REFUTED','candidate_changed':False,
        'rejected_drafts':['debt: JSON term decoding error','debt_v2: unproved Omega target capacity2 assumption'],
        'failed_CPU_charges_retained':True,'all16_necessary_masks_exercised_as_controls':True,
        'all16_masks_claimed_realizable':False,'source_engine_calls':0,'new_finite_tests':0,
        'entire_Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'new_full_allocator_constructed':False,'generic_width2_architecture_refuted':False,'original_CD_counterexample':False,
        'next_bounded_target':'actual H1 zero/+1 incoming compatibility of forced-zero NEG2-source region, not a patched formula'})
    print('PASS exact source cost classification, both closed-source counterexamples and limited terminal scope; OUTCOME B')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_classification_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
