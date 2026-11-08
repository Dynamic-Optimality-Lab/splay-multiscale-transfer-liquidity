"""Independent free-term audit of OR34 and obstruction localization.
No source replay, no new queries, no finite-BST universality inference.
"""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parent/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def labels(t):return set() if t is None else {t[0]}|labels(t[1])|labels(t[2])
def sub(t,k):
    if t is None:return None
    if t[0]==k:return t
    return sub(t[1],k) or sub(t[2],k)
def ancestors(t):
    out={}
    def rec(v,p):
        if v is None:return
        out[v[0]]=set(p);rec(v[1],p+[v[0]]);rec(v[2],p+[v[0]])
    rec(t,[]);return out
def right(t):
    g,p,D=t;k,A,B=p;return k,A,(g,B,D)
def left(t):
    g,A,p=t;k,B,C=p;return k,(g,A,B),C
def reflect(t):return None if t is None else (t[0],reflect(t[2]),reflect(t[1]))
def audit_chain(stages,pivots):
    initial,final=stages[0],stages[-1];rels=[ancestors(t) for t in stages];out=[]
    for j,pivot in enumerate(pivots):
        loss={(g,x) for x in rels[j] for g in rels[j][x]-rels[j+1][x]}
        assert all(g==pivot for g,x in loss)
        assert all(g in rels[0][x] and g not in rels[-1][x] for g,x in loss)
        assert sub(stages[j+1],pivot)==sub(final,pivot)
        out.append(dict(pivot=pivot,lost=sorted(loss),processed_subtree_rigid=True))
    losses=set().union(*({(g,x) for x in rels[j] for g in rels[j][x]-rels[j+1][x]} for j in range(len(pivots))))
    endpoint={(g,x) for x in rels[0] for g in rels[0][x]-rels[-1][x]}
    assert losses==endpoint and len(pivots)==len(set(pivots))
    return out
def main():
    A,Bb,C,D=[(x,None,None) for x in ('A','B','C','D')]
    ll=('G',('P',('y',A,Bb),C),D);ll1=right(ll);ll2=right(ll1)
    lr=('G',('P',A,('y',Bb,C)),D);lr1=('G',left(lr[1]),D);lr2=right(lr1)
    zig=('G',('y',A,Bb),C);zig1=right(zig)
    cases={}
    for name,stages,pivots in [('LL',[ll,ll1,ll2],['G','P']),('LR',[lr,lr1,lr2],['P','G']),('L',[zig,zig1],['G'])]:
        cases[name]=audit_chain(stages,pivots)
        cases[{'LL':'RR','LR':'RL','L':'R'}[name]]=audit_chain([reflect(t) for t in stages],pivots)
    docs=['OPERATION_RETIREMENT_EXACTNESS.md','MINIMAL_GLOBAL_OWNER_OBSTRUCTION.md']
    result=dict(status='PASS_SYMBOLIC_FREE_TERM_RETIREMENT_EXACTNESS_AND_OBSTRUCTION_AUDIT',free_term_cases=cases,proof_method='six exhaustive operation frames plus written induction over arbitrary outer frames; each A/B/C/D is an independent arbitrary rigid BST term',new_source_queries=0,source_queries=0,source_engine_calls=0,source_scope='OR34 all ordinary A splays; exterior PR compatibility conditional on inherited maximal-core extreme ticket theorem',minimal_obstruction='at least two macros, one excess, one interior, connected complete-neighborhood overlap; hypothetical cuts only',principal_JIO34='OPEN',universal_global_expansion='OPEN',universal_Bank25='OPEN',trust='same-agent distinct implementation/static audit; not external review or a proof assistant',input_sha256={d:sha(F/d) for d in docs})
    with (F/'independent_retirement_exactness_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    assert time.process_time()-START<CAP-1
    print(result['status'],flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify83_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
