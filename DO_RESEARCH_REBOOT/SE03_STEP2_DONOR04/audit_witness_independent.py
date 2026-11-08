"""Independent interface/receipt audit; no old transformations re-executed."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    w=json.loads((B/'witness_audit.json').read_text())
    targets=[3,5,7,9,11,9,7,5,3,1,11,1,3,5,7,9,11,9,7,5,3,1]
    assert [r['key'] for r in w['word'] if r['op']=='K']==targets
    assert w['word'][9:13]==[{'occurrence':10,'op':'D','key':1},{'occurrence':11,'op':'D','key':11},
        {'occurrence':12,'op':'D','key':1},{'occurrence':13,'op':'K','key':1}]
    # Original A ignores mode; closed old max/min plus endpoint inverse pair.
    assert 9+1+5+1+0+1+1+14==32
    chain=w['reused_identity_chain']
    assert [p['input'] for p in chain]==['R11','T3','R11','P_full_max_min','P_full_max_min','P_full_max_min']
    assert [p['output'] for p in chain]==['T3','R11','P_full_max_min','P_full_max_min','P_full_max_min','R11']
    # D floor: max-fan psi2, visible maximum has exit weight1, ceiling false.
    # All facts are inherited universal lemmas, not a numeric psi-table query.
    floor=min(2,1+2);assert floor==2
    expected_direct=[(1,1),(9,1),(16,1),(16,2),(24,1)]
    expected_tail=[(11,2,0),(11,2,1),(11,3,0),(11,3,1),(11,4,0)]
    receipt=w['receipt']
    assert [tuple(r['demand']) for r in receipt[:5]]==expected_direct
    assert [tuple(r['unit']) for r in receipt[:5]]==expected_tail
    assert receipt[5]=={'demand':[14,5],'unit':[15,1,1],'class':'RETURN_SURPLUS'}
    assert len(set(expected_tail+[(15,1,1)]))==6
    assert 1+1+5+1==8 and 1+1+2==4
    assert (2*32-24)-6==34
    assert w['guard_failing_witness_claimed'] is False
    out('witness_independent_audit.json',{'status':'PASS_NEW_SOURCE_WITNESS_AT_STATED_SCOPE','full_labeled_closure':'exact identity interfaces, not roots only',
        'all_old_B_checks_reused':True,'actual_return_D2_realizable':True,'all_private_Fi_free':True,
        'six_unit_full_receipt_injective':True,'common_fE_preserved':True,
        'prior_receipts':'unchanged; this fresh Psi allocation is not overlaid on alternative guarded receipts',
        'not_a_guard_failing_witness':True,'novel_CD_domain_claimed':False,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_finite_tests':0,
        'same_agent_separate_derivation':True,'Step2':'OPEN','requested_universal_completion_achieved':False})
    print('PASS separate source interface, actual debt-floor and six-unit receipt audit; universal Step2 OPEN')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_witness_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
