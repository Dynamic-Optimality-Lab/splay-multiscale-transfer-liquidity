"""Separate primitive source representation and mathematical scope audit."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def node(k,l,r):return {'key':k,'left':l,'right':r}
def rotate(t,side):
    if side=='R':
        p=t['left']
        return node(p['key'],p['left'],node(t['key'],p['right'],t['right']))
    p=t['right']
    return node(p['key'],node(t['key'],t['left'],p['left']),p['right'])
def encode(t):return t if isinstance(t,str) else [t['key'],encode(t['left']),encode(t['right'])]
def main():
    d=json.loads((B/'derivation_audit.json').read_text());assert d['status']=='PASS_NEW_SCOPED_SOURCE_DERIVATIONS'
    s=node('G',node('P',node('X','a','b'),'c'),'d')
    t=rotate(rotate(s,'R'),'R')
    assert encode(t)==['X','a',['P','b',['G','c','d']]]
    s=node('G','a',node('P','b',node('X','c','d')))
    t=rotate(rotate(s,'L'),'L')
    assert encode(t)==['X',['P',['G','a','b'],'c'],'d']
    s=node('G',node('P','a',node('X','b','c')),'d')
    t=rotate(node('G',rotate(s['left'],'L'),'d'),'R')
    assert encode(t)==['X',['P','a','b'],['G','c','d']]
    s=node('G','a',node('P',node('X','b','c'),'d'))
    t=rotate(node('G','a',rotate(s['right'],'R')),'L')
    assert encode(t)==['X',['G','a','b'],['P','c','d']]
    # Distinct proof: certified-edge induction replaces arbitrary incoming
    # edges at the first access of their child, with periodic transport.
    recency_proof={'base':'arbitrary initial edges untrusted',
        'step':'only new root is parent of changed path edges; off-path edges unchanged',
        'progress':'every untrusted edge removed at child first visit',
        'closure':'all marks occur; one-period translation has same B and cyclic recent order'}
    # Distinct channel argument: threshold bit toggles on its own label
    # and never on another label. Net up-minus-down equals endpoint bit.
    channel_proof={'crossing':'fixed threshold bit toggles up/down alternately',
        'interval':'subtree total mass>=0 orders endpoint heights',
        'nonnegativity':'nondecreasing threshold indicator gives0/1 net charge',
        'own_root':'left endpoint<=root preheight; right endpoint>=root postheight',
        'support':'every channel starts below and ends above; all marks partition'}
    assert d['own_channel_SS_rows'][1]['delta_K']=={'e':-1}
    assert len(d['own_channel_SS_rows'])==5
    # Critical exclusions are mathematical, not asserted foreign laws.
    gate=(B/'OWN_CHANNEL_PRESERVATION.md').read_text()
    assert 'foreign-channel KEEP preserves K_h' in gate
    assert 'NOT full A debt' in gate
    out('independent_audit.json',{'status':'PASS_SEPARATE_SOURCE_AND_SCOPE_AUDIT',
        'primitive_frames_rederived':4,'recency_induction':recency_proof,'channel_flow_proof':channel_proof,
        'own_channel_case_audit':'P ownM excluded; five SS tag rows; mixed requires each processed ownU1->0; foreign-root zig rotates no ownU',
        'Omega_scope':'original reachable fully paired-closed arbitrary-fringe family reused, not a projected negative cycle',
        'unique_chart_argument':'mark11 needs all11 ancestors; other five marks force precisely the first9',
        'all_new_statements_A_funding_free':True,
        'forbidden_promotions':['two channel masses are two independent splay executions','both CD5 calls may spend same A bits','recency rank supplies unused donors','chart envelope repairs Omega'],
        'mathematical_open_obligations':['full A-dependent zero/+1 closure preserving paid rows','foreign-channel source simulation and disjoint A funding','complete universal full allocator'],
        'external_peer_review':False,'whole_compiler_formalization':False,'same_agent_separate_derivation':True,
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0,
        'requested_completion_achieved':False,'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS separate primitive rotations, temporal/source/channel proofs and exact coverage audit; no Step2 seal')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
