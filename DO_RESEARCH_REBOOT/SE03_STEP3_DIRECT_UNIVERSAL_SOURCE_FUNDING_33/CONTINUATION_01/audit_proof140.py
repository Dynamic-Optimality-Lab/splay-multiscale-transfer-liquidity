"""Actual-B-guided private-node joins on retained original source constraints.
This is falsification/discovery, not a passing finite-prefix proof.
"""
import json,pickle,time,sys,hashlib
from pathlib import Path
from interior_projection_source_tools import fr,known,normalize,isnode
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])

def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)

def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,Z['trees']));N=len(T);idx={t:i for i,t in enumerate(T)};mir=Z['mirror']
    O=pickle.loads((B/'native10_B_modal_factored_debt.pkl').read_bytes())
    def D(a,b):return O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    with (B/'full_geometry_work_02.pkl').open('rb') as f:w=pickle.load(f)
    stats={};bad={};checked=0;selected={};methods=('B_root_depth_left_tie','B_root_depth_right_tie','B_minimum_subtree_depth')
    def depths(b):
        if b not in stats:
            result={}
            def walk(t,d):
                if isnode(t):result[2*t[0]]=d;walk(t[1],d+1);walk(t[2],d+1)
            walk(T[b],0);stats[b]=result
        return stats[b]
    def choose(A,b,name):
        dep=depths(b)
        def merge(L,R):
            if not isnode(L):return R
            if not isnode(R):return L
            if name=='B_minimum_subtree_depth':
                lp=min(dep[v] for v in known(L));rp=min(dep[v] for v in known(R));assert lp!=rp
            else:lp=dep[L[0]];rp=dep[R[0]]
            takeleft=lp<rp or lp==rp and name=='B_root_depth_left_tie'
            return (L[0],L[1],merge(L[2],R)) if takeleft else (R[0],merge(L,R[1]),R[2])
        def walk(t):
            if not isnode(t):return t
            return merge(t[1],t[2]) if t[0]==5 else (t[0],walk(t[1]),walk(t[2]))
        return idx[normalize(walk(A),{k:k//2 for k in known(A) if k!=5})]
    for e in w['edges'].values():
        for name in methods:
            if name in bad:continue
            a=choose(e['source_A'],e['source_B_core_index'],name);at=choose(e['actual_A_target'],e['B_target_core_index'],name)
            ds=D(a,e['source_B_core_index']);dt=D(at,e['B_target_core_index'])
            assert a in e['source_contraction_indices'] and at in e['target_contraction_indices']
            if e['price']+dt-ds<0:
                r=e.copy();r.update(projection_rule=name,old_source_A_index=a,old_projected_target_index=at,D_source=ds,D_target=dt,signed_margin=e['price']+dt-ds);bad[name]=r
        checked+=1
        if len(bad)==len(methods) or time.process_time()-START>CAP-4:break
    out('B_guided_contraction_candidates.json',{'status':'ALL_THREE_B_GUIDED_JOINS_FAILED_RAW' if len(bad)==len(methods) else 'B_GUIDED_JOIN_DISCOVERY_OPEN','methods':methods,'failures':bad,'constraints_read':checked,'B_depth_maps':len(stats),'scope':'same original one-private-gap2 source; selectors use actual full source and target B separately','closed_source_embedding':'not yet newly replayed; exact failed source edges retained','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'})
    print(json.dumps({'status':'B_GUIDED_JOIN_DISCOVERY','checked':checked,'failed':{k:{x:e[x] for x in ('H','Q','price','D_source','D_target','signed_margin')} for k,e in bad.items()}}))

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof140_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
