"""Source branch retirement: test the precise ordinary-preimage mechanism.
An absent witness is discovery only; an explicit failure can refute the
mechanism after source/closure auditing. No Coarse-Double implication alone.
"""
import json,pickle,sys,time
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z)
    with (B/'full_geometry_sparse_work_06.pkl').open('rb') as f:w=pickle.load(f)
    bad=None;cases=0;Ascount=0;complete=True;hist={}
    for As in w['A']:
        p=S.sub(As,5)
        if not isnode(p[1]) or not isnode(p[2]):continue
        pi=tuple(S.idx[t] for t in projections(As,5));options=[]
        for x in known(As):
            if x in (5,As[0]) or len(path(As,x))>4:continue
            At,H=S.access(As,x);options.append((x,H,None,At))
        for y in known(As):
            if y==As[0] or len(path(As,y))>2:continue
            mid,H=S.access(As,y);assert H==1
            for x in known(mid):
                if x in (5,mid[0],As[0]) or len(path(mid,x))>2:continue
                At,H=S.access(mid,x);assert H==1;options.append((x,2,y,At))
        Ascount+=1
        for x,H,y,At in options:
            pt=S.sub(At,5)
            if isnode(pt[1]) and isnode(pt[2]):continue
            target=tuple(S.idx[t] for t in projections(At,5));assert len(target)==1;target=target[0];found=None
            for a in pi:
                proxies=(None,) if y is None else range(1,11) if y==5 else (y//2,)
                for z in proxies:
                    mid=a if z is None else Z['destination'][a][z-1];h=0 if z is None else Z['H'][a][z-1];end=Z['destination'][mid][x//2-1];h+=Z['H'][mid][x//2-1]
                    if end==target and h<=H:found=(a,z,h);break
                if found:break
            cases+=1;kind='direct' if y is None else 'private_helper' if y==5 else 'old_helper';hist[kind]=hist.get(kind,0)+1
            if found is None:
                bad={'source_A':As,'actual_A_target':At,'private_key':5,'target_actual_key':x,'H':H,'DELETE_helper':y,'source_contraction_indices':pi,'target_contraction_index':target,'operation_word':([['D',y]] if y is not None else [])+[['K',x]],'comparison_rule':'old helper unchanged; private helper may use ANY anchor proxy, even root, at whole old H<=actual H','all_permitted_old_source_projections_and_proxies_checked':True};break
        if bad:break
        if time.process_time()-START>CAP-3:complete=False;break
    out('single_private_retirement_preimage_candidate.json',{'status':'SINGLE_PRIVATE_RETIREMENT_PREIMAGE_RAW_FAILURE' if bad else 'SINGLE_PRIVATE_RETIREMENT_PREIMAGE_DISCOVERY_OPEN','candidate':bad,'source_shapes':Ascount,'retirement_cases':cases,'case_kinds':hist,'known_prefix_complete':complete and bad is None,'source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'})
    print(json.dumps({'status':'RETIREMENT_PREIMAGE_PROBE','counter':None if bad is None else {k:bad[k] for k in ('H','DELETE_helper','target_actual_key')},'source_shapes':Ascount,'cases':cases,'case_kinds':hist,'known_prefix_complete':complete and bad is None}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof155_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
