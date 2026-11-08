"""Uniform-form feature-potential synthesis; finite grammar is discovery only."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,sys,hashlib,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    from scipy.optimize import linprog
    z=json.loads((B/'geodesic_seven_metric_table.json').read_text());T=z['trees'];N=len(T);depth=[];masks=[];parents=[];sizes=[];ranks=[]
    for tree in T:
        d=[0]*7;m=[0]*7;p=[0]*7
        def walk(t,dep,par):
            if isinstance(t,str):return 0
            k,l,r=t;p[k-1]=par;d[k-1]=dep;m[k-1]=(1<<(k-1))|walk(l,dep+1,k)|walk(r,dep+1,k);return m[k-1]
        walk(tree,0,0);s=[v.bit_count() for v in m];depth.append(d);masks.append(m);parents.append(p);sizes.append(s);ranks.append([v.bit_length()-1 for v in s])
    d=np.array(depth);m=np.array(masks);p=np.array(parents);s=np.array(sizes);rank=np.array(ranks);a=np.arange(N)[:,None];b=np.arange(N)[None,:];broadcast=lambda v:np.broadcast_to(v,(N,N));pop=np.array([v.bit_count() for v in range(128)]);F=[];names=[]
    def add(name,v):names.append(name);F.append(broadcast(v).reshape(-1))
    for name,v in (('depth',d),('depth_squared',d*d),('subtree_size_squared',s*s),('floor_log_subtree',rank)):
        add('sum_A_'+name,v.sum(1)[:,None]);add('sum_B_'+name,v.sum(1)[None,:])
    add('common_parent_edges',(p[:,None,:]==p[None,:,:]).sum(2));add('common_subtree_intervals',(m[:,None,:]==m[None,:,:]).sum(2));add('common_ancestor_incidence',pop[m[:,None,:]&m[None,:,:]].sum(2));add('depth_L1',abs(d[:,None,:]-d[None,:,:]).sum(2));add('depth_inner_product',(d[:,None,:]*d[None,:,:]).sum(2));add('subtree_size_inner_product',(s[:,None,:]*s[None,:,:]).sum(2));add('sum_min_subtree_size',np.minimum(s[:,None,:],s[None,:,:]).sum(2));add('rank_inner_product',(rank[:,None,:]*rank[None,:,:]).sum(2));add('rank_L1',abs(rank[:,None,:]-rank[None,:,:]).sum(2));add('equal_depth_count',(d[:,None,:]==d[None,:,:]).sum(2));add('A_shallower_count',(d[:,None,:]<d[None,:,:]).sum(2));add('equal_subtree_size_count',(s[:,None,:]==s[None,:,:]).sum(2));add('exact_single_rotation_distance',np.array(z['distances']))
    feature=np.stack(F,axis=1).astype(np.int16);src=[];dst=[];cost=[];records=[];dest=np.array(z['source_destinations']);H=np.array(z['source_H']);Q=np.array(z['source_Q']);roots=np.array([t[0] for t in T])
    for g in range(1,8):
        ids=np.flatnonzero(roots==g);aa,bb=np.meshgrid(ids,ids,indexing='ij');aa=aa.reshape(-1);bb=bb.reshape(-1)
        for x in range(1,8):
            if x==g:continue
            at=dest[aa,x-1];bt=dest[bb,x-1];src.extend((aa*N+bb).tolist());dst.extend((at*N+bt).tolist());cost.extend((2*H[aa,x-1]-Q[bb,x-1]).tolist());records.extend(zip(aa.tolist(),bb.tolist(),[x]*len(aa)))
    X=(feature[np.array(dst)]-feature[np.array(src)]).astype(np.int16);w=np.array(cost,dtype=np.int16);np.savez_compressed(B/'uniform_feature_synthesis_arrays.npz',features=feature,X=X,w=w,records=np.array(records,dtype=np.int16));assert len(records)<5000000 and N*N<2000000
    allowed=min(8,max(.2,CAP-(time.process_time()-START)-2));res=linprog(np.zeros(len(names)),A_ub=-X,b_ub=w,bounds=[(None,None)]*len(names),method='highs',options={'time_limit':allowed});result={'status':'FINITE_CANDIDATE' if res.success else ('FINITE_GRAMMAR_INFEASIBLE' if res.status==2 else 'SOLVER_LIMIT_NO_CLAIM'),'feature_names':names,'feature_count':len(names),'source_packet_rows':len(records),'source_state_feature_records':N*N,'LP_status':int(res.status),'LP_message':res.message,'coefficients':res.x.tolist() if res.success else None,'new_source_queries':0,'uniform_source_proof':False,'principal_U33':'OPEN','only_model':'fixed linear combination of stated support-uniform features; c=WHOLE_H on direct genuine packets'}
    out('uniform_feature_synthesis_result.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof32_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
