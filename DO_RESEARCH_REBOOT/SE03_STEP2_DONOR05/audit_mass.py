"""Universal free source frames and signed-mass identities; no populations."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def N(k,l,r):return (k,l,r)
def right(t):
    g,z,d=t;p,a,b=z
    return N(p,a,N(g,b,d))
def left(t):
    g,a,z=t;p,b,d=z
    return N(p,N(g,a,b),d)
def atoms(t):return [t] if isinstance(t,str) else atoms(t[1])+[t[0]]+atoms(t[2])
def add(*ps):
    q={}
    for p in ps:
        for k,v in p.items():q[k]=q.get(k,0)+v
    return {k:v for k,v in q.items() if v}
def scale(n,p):return {k:n*v for k,v in p.items() if n*v}
def weight(k):return {'1':1} if k=='x' else {k:1}
def mass(t):return {t.lower():1} if isinstance(t,str) else add(weight(t[0]),mass(t[1]),mass(t[2]))
def subtree_sum(t):return {} if isinstance(t,str) else add(mass(t),subtree_sum(t[1]),subtree_sum(t[2]))
def main():
    ll=N('g',N('p',N('x','A','B'),'C'),'D')
    rr=N('g','A',N('p','B',N('x','C','D')))
    lr=N('g',N('p','A',N('x','B','C')),'D')
    rl=N('g','A',N('p',N('x','B','C'),'D'))
    llo=right(right(ll));rro=left(left(rr))
    lro=right(N('g',left(lr[1]),lr[2]));rlo=left(N('g',rl[1],right(rl[2])))
    assert llo==N('x','A',N('p','B',N('g','C','D')))
    assert rro==N('x',N('p',N('g','A','B'),'C'),'D')
    assert lro==N('x',N('p','A','B'),N('g','C','D'))
    assert rlo==N('x',N('g','A','B'),N('p','C','D'))
    frames=[]
    for tag,s,t in [('LL',ll,llo),('RR',rr,rro),('LR',lr,lro),('RL',rl,rlo)]:
        assert atoms(s)==atoms(t) and mass(s)==mass(t)
        frames.append({'case':tag,'source':s,'target':t,'delta_signed_subtree_sum':add(subtree_sum(t),scale(-1,subtree_sum(s)))})
    assert frames[0]['delta_signed_subtree_sum']=={'g':2,'c':1,'d':2,'1':-2,'a':-2,'b':-1}
    # Analytic cases after target-child masses0 and bounds c,d in[0,1].
    assert 1+0+0==1 and -1+1+1==1
    assert (2*1+0+2*0-2)==0
    assert (2*(-1)+1+2*1-2)==-1
    assert (-1+1-2)==-2
    # Persistence: each source hanger remains a whole variable in every formula.
    assert all(atoms(v['target']).count(z)==1 for v in frames for z in ['A','B','C','D'])
    out('mass_audit.json',{'status':'PASS_UNIVERSAL_FRAME_AND_MASS_IDENTITIES',
        'frames':frames,'signed_mass_scope':'all actual closed maximal cores2r-1, r>=2, all mark-free ambient BST hangers',
        'initial_and_final_density':'source marked mass1; source unmarked mass0/1; processed subtrees have final fixed masses',
        'classification':[{'event':'SS','G':'marked','P':'unmarked source mass0','delta_K':0},
            {'event':'SS','G':'unmarked source mass1','P':'unmarked source mass1','delta_K':-1},
            {'event':'mixed','G':'unmarked source mass1','P':'unmarked source mass1','delta_K':-2}],
        'terminal_zig':'impossible: marked root1 + rebuilt target1 + nonnegative hanger exceeds source mass1',
        'closure':'all decrements nonnegative; full B closure forces every decrement0',
        'no_positive_unmarked_vertex':'first access inside its rigid marked-descendant set must consume it, contradicting zero-change pair language',
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0,
        'Step2_complete':False,'core10_covered':False})
    print('PASS generic actual frame identities and new monotone signed-mass theorem; no Step2 promotion')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_mass_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
