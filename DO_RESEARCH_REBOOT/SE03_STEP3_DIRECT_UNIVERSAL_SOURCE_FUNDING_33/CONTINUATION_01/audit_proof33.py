"""Add complete B10 actions against three explicit one-event A templates."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,sys
from pathlib import Path
from uniform_feature_basis import metadata,features
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    from scipy.optimize import linprog
    z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,z['trees']));idx={t:i for i,t in enumerate(T)};dest=np.array(z['destination']);H=np.array(z['H']);Q=np.array(z['Q']);N=len(T);meta=metadata(T,10);roots=np.array([t[0] for t in T]);sources=[];targets=[];costs=[];records=[]
    def fill(lo,hi,kind):
        if lo>hi:return 'F'+str(hi)
        k=lo if kind==0 else (hi if kind==1 else (lo+hi)//2);return (k,fill(lo,k-1,kind),fill(k+1,hi,kind))
    for g in range(1,11):
        bb=np.flatnonzero(roots==g)
        for x in range(1,11):
            if x==g:continue
            used=set()
            for kind in range(3):
                tree=(g,(x,fill(1,x-1,kind),fill(x+1,g-1,kind)),fill(g+1,10,kind)) if x<g else (g,fill(1,g-1,kind),(x,fill(g+1,x-1,kind),fill(x+1,10,kind)));a=idx[tree]
                if a in used:continue
                used.add(a);assert H[a,x-1]==1;aa=np.full(len(bb),a);at=np.full(len(bb),dest[a,x-1]);bt=dest[bb,x-1];sources.extend(zip(aa.tolist(),bb.tolist()));targets.extend(zip(at.tolist(),bt.tolist()));costs.extend((2-Q[bb,x-1]).tolist());records.extend((a,int(b),x) for b in bb)
    pairs=np.array(sources,dtype=np.int32);newpairs=np.array(targets,dtype=np.int32);X=features(meta,newpairs[:,0],newpairs[:,1],10)-features(meta,pairs[:,0],pairs[:,1],10);w=np.array(costs,dtype=np.int16);prior=np.load(B/'uniform_feature_synthesis_arrays.npz');Xall=np.concatenate((prior['X'][:,:20],X));wall=np.concatenate((prior['w'],w));assert len(Xall)<5000000 and len(pairs)*2+184041<2000000
    np.savez_compressed(B/'uniform_feature_extended_arrays.npz',X=Xall,w=wall,native10_records=np.array(records,dtype=np.int16),native7_count=len(prior['w']));allowed=min(8,max(.2,CAP-(time.process_time()-START)-2));res=linprog(np.zeros(20),A_ub=-Xall,b_ub=wall,bounds=[(None,None)]*20,method='highs',options={'time_limit':allowed});result={'status':'FINITE_FEATURE_MODEL_INFEASIBLE' if res.status==2 else ('FINITE_FEATURE_CANDIDATE_NOT_PROOF' if res.success else 'LP_LIMIT_NO_CLAIM'),'LP_status':int(res.status),'LP_message':res.message,'feature_count':20,'features':'same 20 support-independent integer features as proof32, omitting exact geodesic distance','native7_rows':len(prior['w']),'new_native10_template_rows':len(w),'total_constraint_rows':len(wall),'coefficients':res.x.tolist() if res.success else None,'source_rule':'every B10 genuine primitive, all three prescribed synchronized A-root/child templates; exact action cache reused','new_source_queries':0,'source_realization_needed_for_refutation':res.status==2,'principal_U33':'OPEN'};out('uniform_feature_extended_result.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof33_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
