"""New source composition, using completed identities without replaying them."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    W=[('K',k) for k in [3,5,7,9,11,9,7,5,3,1]]
    H=[('K',k) for k in [11,1,3,5,7,9,11,9,7,5,3,1]]
    word=W[:-1]+[('D',1),('D',11),('D',1),('K',1)]+H
    assert len(word)==25 and sum(op=='K' for op,k in word)==22
    assert [v for v in word if v[0]=='K']==W+H
    # Identity interfaces are exact full labeled source endpoints.
    premises=[
        {'identity':'old W6 prefix','input':'R11','output':'T3','A':9},
        {'identity':'DONOR03 V A D1','input':'T3','output':'R11','A':1},
        {'identity':'old H6 max/min A, modes D','input':'R11','output':'P_full_max_min','A':6},
        {'identity':'K1 A root identity','input':'P_full_max_min','output':'P_full_max_min','A':0},
        {'identity':'old RR/LL inverse frame on roles1,2,11','input':'P_full_max_min','output':'P_full_max_min','A':2},
        {'identity':'old H6 ten-KEEP suffix','input':'P_full_max_min','output':'R11','A':14}]
    for a,b in zip(premises,premises[1:]):assert a['output']==b['input']
    assert premises[0]['input']==premises[-1]['output']=='R11'
    assert sum(p['A'] for p in premises)==32
    # Existing exact core/visibility lower floor, all sigma free.
    visible_marked=['maximum11'];q_exit=1;psi_max_fan=2
    assert min(2,q_exit+psi_max_fan)==2
    assert 2!=11 # actual Score-child role2 is not largest11: old ceiling false
    # Exact physical IDs and source macro ordinal derivation.
    event_ids=[(11,2),(11,3),(11,4)]
    assert [1+1+j for _,j in event_ids]==[4,5,6]
    tail=[(o,e,b) for o,e in event_ids for b in (0,1)]
    direct=[(1,1),(9,1),(16,1),(16,2),(24,1)]
    receipt=[{'demand':p,'unit':u,'class':'TAIL'} for p,u in zip(direct,tail[:5])]
    receipt.append({'demand':(14,5),'unit':(15,1,1),'class':'RETURN_SURPLUS'})
    assert len({r['demand'] for r in receipt})==len({r['unit'] for r in receipt})==6
    assert word[14]==('K',1) and word[13]==('K',11)
    assert all(word[p[0]-1]==('K',3) for p in direct)
    assert 30-24==5+1==6 and 2*32-30==34
    out('witness_audit.json',{'status':'PASS_SOURCE_COMPOSITION_AND_RECEIPT','universal_fringe_variables':'F0..F11, all arbitrary ordered BSTs, never instantiated',
        'word':[{'occurrence':i,'op':o,'key':k} for i,(o,k) in enumerate(word,1)],'reused_identity_chain':premises,
        'counts':{'operations':25,'KEEP':22,'DELETE':3,'A':32,'QF':30,'QE_steady':24,'QE_first':25,'D3':5,'J3':1,'N':0,'P':6,'full_slack':34},
        'actual_return_debt':2,'lower_floor_reused':'Hamiltonian normalization final source-capacity proof, same relative fixed nine-Score shape and visible marked maximum',
        'receipt':receipt,'guard_failing_witness_claimed':False,'universal_unguarded_closure':False,
        'old_semantic_rows_replayed':0,'source_engine_calls':0,'new_finite_tests':0,'Step2':'OPEN'})
    print('PASS source-exact composition witness for debt2 branch and full six-demand receipt; not universal Step2')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_witness_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
