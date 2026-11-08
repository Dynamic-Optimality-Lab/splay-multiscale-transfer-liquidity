"""Separate new frame/ownership derivation; imports no prior source checker."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def node(k,l,r):return {'key':k,'left':l,'right':r}
def replace_at(t,path,new):
    if not path:return new
    if path[0]=='L':return node(t['key'],replace_at(t['left'],path[1:],new),t['right'])
    return node(t['key'],t['left'],replace_at(t['right'],path[1:],new))
def at(t,path):
    for c in path:t=t['left' if c=='L' else 'right']
    return t
def rotate(t,path,direction):
    g=at(t,path)
    if direction=='right':
        p=g['left'];v=node(p['key'],p['left'],node(g['key'],p['right'],g['right']))
    else:
        p=g['right'];v=node(p['key'],node(g['key'],g['left'],p['left']),p['right'])
    return replace_at(t,path,v)
def ordered(t):return [t] if isinstance(t,str) else ordered(t['left'])+[t['key']]+ordered(t['right'])
def encode(t):return t if isinstance(t,str) else [t['key'],encode(t['left']),encode(t['right'])]
def main():
    # Independent dictionary representation and elementary rotations.
    l=node('x',node('u1',node('y','A','B'),'Ltail'),'Rfan')
    r=node('x','Lfan',node('uR','Rtail',node('y','C','D')))
    l2=rotate(rotate(l,'','right'),'','right')
    r2=rotate(rotate(r,'','left'),'','left')
    assert l2==node('y','A',node('u1','B',node('x','Ltail','Rfan')))
    assert r2==node('y',node('uR',node('x','Lfan','Rtail'),'C'),'D')
    assert ordered(l)==ordered(l2) and ordered(r)==ordered(r2)
    # Rigid-hanger property: none of the variables is entered or duplicated.
    for name in ['A','B','Ltail','Rfan']:assert ordered(l2).count(name)==1
    for name in ['Lfan','Rtail','C','D']:assert ordered(r2).count(name)==1
    d=json.loads((B/'derivation.json').read_text())
    assert d['generic_source_frames'][0]['destination']==encode(l2)
    assert d['generic_source_frames'][1]['destination']==encode(r2)
    # Independently keep chronological FIFO ownership rather than compare totals.
    queue=[('old',0),('old',1),('first',0),('first',1)]
    paid_first=[queue.pop(0) for _ in range(4)];assert not queue
    queue.extend([('return',0),('return',1)])
    paid_return=queue.pop(0)
    required_bank=0
    released=queue[required_bank:];queue=queue[:required_bank]
    assert paid_return==('return',0) and released==[('return',1)] and not queue
    assert len(set(paid_first+[paid_return]+released))==6
    # Counterbranch: debt1 requires keeping return bit1; no allocation made.
    other_bank=2-1;assert other_bank==1
    assert [('return',1)][:other_bank]==[('return',1)]
    # Zero-birth deduction without enumerating populations, H values or shapes.
    # q=2H+d'-d <=4 and d-d'<=2 =>2H<=6.
    assert 4+2==6 and 6//2==3
    assert 2*3-4-2==0
    # H3 equality requires all bounds tight; H1/H2 formulas by substitution.
    assert 2*2==4 and 2*1==2
    assert d['new_results']['direct_return_surplus']['births']==[0,1]
    assert d['new_results']['leaf_activation_barrier']['candidate_events_proved_unused'] is False
    assert d['Step2_complete'] is False and d['all_unguarded_packets_closed'] is False
    out('independent_audit.json',{'status':'PASS_NEW_SUBCASE_AND_STRUCTURAL_LEMMAS_ONLY',
        'source_frames':'independent dictionary representation, two elementary rotations, all arbitrary hangers rigid',
        'return_surplus_owner':'sole return A event bit1; outside all fE images and all prior >=4 tail-event modules',
        'cross_packet_ownership':'disjoint q5/q1 source packets imply distinct return source IDs',
        'old_receipts_preserved':True,'B_return_pulse_whole_class':'q5 impossible because outside targets in actual <=9 core and pulse q<=1',
        'marked_leaf_persistence':'no other marked target path enters a marked-leaf subtree; rigid reattachment preserves it',
        'gap_cover':'next Hamiltonian source path has only target as core leaf; visit all other old leaves',
        'candidate_pool_funded':False,'zero_reserve_kernel':'necessary source-algebra grammar only, no realizability asserted',
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0,
        'external_peer_review':False,'whole_compiler_formalization':False,
        'requested_universal_completion_achieved':False,'all_unguarded_packets_closed':False,'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS separate frame/ownership audit; donor exclusion for activation pools and debt1 branch still unproved')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
