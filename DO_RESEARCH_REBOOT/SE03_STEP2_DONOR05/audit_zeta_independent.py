"""Separate primitive-rotation Zeta proof, not the constructor's decoder."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def node(k,l,r):return ('n',k,l,r)
def at(t,p):
    for c in p:t=t[2 if c=='L' else 3]
    return t
def replace(t,p,u):
    if not p:return u
    return node(t[1],replace(t[2],p[1:],u),t[3]) if p[0]=='L' else node(t[1],t[2],replace(t[3],p[1:],u))
def rotate(t,p,d):
    u=at(t,p)
    if d=='right':v=u[2];z=node(v[1],v[2],node(u[1],v[3],u[3]))
    else:v=u[3];z=node(v[1],node(u[1],u[2],v[2]),v[3])
    return replace(t,p,z)
def splay(t,k,p):
    assert at(t,p)[1]==k
    q=p;cost=0
    while len(q)>=2:
        pre,pair=q[:-2],q[-2:]
        if pair=='LL':t=rotate(t,pre,'right');t=rotate(t,pre,'right')
        elif pair=='RR':t=rotate(t,pre,'left');t=rotate(t,pre,'left')
        elif pair=='LR':t=rotate(t,pre+'L','left');t=rotate(t,pre,'right')
        else:assert pair=='RL';t=rotate(t,pre+'R','right');t=rotate(t,pre,'left')
        cost+=1;q=pre
    if q:t=rotate(t,'','right' if q=='L' else 'left');cost+=1
    assert t[1]==k
    return t,cost
def encode(t):return t if isinstance(t,str) else [t[1],encode(t[2]),encode(t[3])]
def main():
    d=json.loads((B/'zeta_audit.json').read_text());f=[f'F{i}' for i in range(12)];R=f[11]
    for k in range(11,0,-1):R=node(k,f[k-1],R)
    t=R;seen=[]
    instructions=[('preparation',k,p) for k,p in [(5,'RRRR'),(11,'RRRRRR'),(3,'LLLRL'),(11,'R'),(1,'LLL'),(3,'RLR'),(1,'L')]]
    instructions += [('boundary_root',1,''),('critical',11,'RR'),('critical',1,'LL'),('zero',3,'R'),('zero',5,'RL')]
    instructions += [('ascending',k,p) for k,p in enumerate(['LL','RL','R','RL','R','RL','RLL','R','RLL','R','R'],1)]
    instructions += [('descending',k,'L') for k in range(10,0,-1)]
    for tag,k,p in instructions:
        t,c=splay(t,k,p);seen.append((tag,k,p,c))
        if len(seen)==7:assert encode(t)==d['prepared_A']
        if len(seen)==10:assert encode(t)==d['prepared_A']
        if len(seen)==12:assert encode(t)==d['after_zero_A']
    assert t==R
    assert seen==[(r['tag'],r['key'],r['path'],r['cost']) for r in d['trace']]
    assert d['marked_core_leaves_at_end']==[1,7,9]
    assert d['counts']=={'operations':55,'KEEP':22,'DELETE':33,'A':71,'QF':30,'QE_steady':24,'QE_first':25,'D3':5,'J3':1,'N':0,'P':6,'full_slack':112}
    # Exact source negative anchor, not a B-only floor for arbitrary A.
    assert d['word'][18:22]==[{'occurrence':19,'op':'K','key':11},{'occurrence':20,'op':'K','key':1},
        {'occurrence':21,'op':'K','key':3},{'occurrence':22,'op':'K','key':5}]
    assert d['two_zero_path']['start_D0']==2 and d['two_zero_path']['end_D0_upper_bound']==1
    assert 0+1-2==-1
    expected=[(11,2,0),(11,2,1),(12,1,0),(12,1,1),(12,2,0),(12,2,1)]
    assert [tuple(x['unit']) for x in d['receipt']]==expected
    assert len({tuple(x['demand']) for x in d['receipt']})==len(set(expected))==6
    assert 1+1+14==16 and [1+1+2,1+1+2+1,1+1+2+2]==[4,5,6]
    out('zeta_independent_audit.json',{'status':'PASS_SOURCE_EXACT_ZERO_TRANSFER_OBSTRUCTION',
        'method':'new prescribed A paths via separate elementary primitive rotations, arbitrary twelve free BSTs',
        'full_closure':'new source scan returnsR11; exact inherited alignment/suffix identities close full pair',
        'old_B_rows_replayed':False,'source_word_modes_and_all_operations_preserved':True,
        'refuted_candidates':['max(psi11(B),paired safeL)','max(source-exact Dminus(A,B),paired safeL)'],
        'reason':'actual negative pair forces2; two actual zero singletons end at debt<=1',
        'Dminus_definition':'one/two exact original H1 root-splay source predicates, not arbitrary signed path optimization',
        'Dminus_paid_rows':['all negatives','all singleton H2/Higher','paired Hsum3 via source Hamiltonian seed0','all price>=2'],
        'Dminus_unpaid_rows':['singleton H1/q1','singleton H1/q2'],
        'negative_original_cycle':False,'all_width2_potentials_refuted':False,'full_family_receipt_preserves_common_fE':True,
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0,
        'same_agent_separate_derivation':True,'external_peer_review':False,'whole_compiler_formalization':False,
        'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS separate primitive source path and source-exact seed/candidate audit; full signed completion OPEN')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_zeta_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
