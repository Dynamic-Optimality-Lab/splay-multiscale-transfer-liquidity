"""Attack actual zero/+1 LOW exits of states carrying current projected debt.
Every edge is direct KEEP or one original DELETE plus KEEP. Cached, certified
ordinary primitives are composed; no new engine or abstract HIGH edge is used.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,sys,pickle
from pathlib import Path
from uniform_feature_basis import metadata,features
from diagonal_zero_feature_basis import transform
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    graph=np.load(B/'nonlinear15_batch_01_graph.npz');keys=graph['keys'];Nold=len(keys);Eold=len(graph['w'])
    with (B/'nonlinear15_batch_01_work_01.pkl').open('rb') as f:oldstate=pickle.load(f)
    assert oldstate['head']==len(oldstate['queue']);level=oldstate['level'];native=json.loads((B/'native10_source_actions.json').read_text());T=native['trees'];N=len(T);D=np.array(native['destination']);H=np.array(native['H']);Q=np.array(native['Q']);roots=np.array([t[0] for t in T]);meta=metadata(T,10);raw=np.load(B/'nonlinear15_batch_01_actual_source_records.npz')['records'];a,b,x=raw.T;x=x-1;codes=np.unique(D[a,x].astype(np.int64)*N+D[b,x]);ids=np.linspace(0,len(codes)-1,min(20000,len(codes)),dtype=np.int64);codes=codes[ids];aa=codes//N;bb=codes%N;vv=transform(features(meta,aa,bb,10),10);dtype=np.dtype([('f'+str(i),'<i4') for i in range(15)]);keyview=np.ascontiguousarray(keys,dtype=np.int32).view(dtype).reshape(-1)
    def lookup(v):
        view=np.ascontiguousarray(v,dtype=np.int32).view(dtype).reshape(-1);at=np.searchsorted(keyview,view);ok=at<len(keys);loc=np.flatnonzero(ok);ok[loc]=keyview[at[loc]]==view[loc];ans=np.zeros(len(v),dtype=np.int64);ans[ok]=level[at[ok]];return ans
    ds=lookup(vv);good=np.flatnonzero(ds>0);aa=aa[good];bb=bb[good];vv=vv[good];ds=ds[good];newrecords=[];newbefore=[];newafter=[];price=[];checked=processed=0;limit=min(100000,(1990000-Nold)//2);assert limit>0
    for lo in range(0,len(aa),200):
        az=aa[lo:lo+200];bz=bb[lo:lo+200];vz=vv[lo:lo+200];dz=ds[lo:lo+200];cand=[];source_indices=[]
        for y in range(11):
            at=az if y==0 else D[az,y-1];hy=np.zeros(len(az),dtype=np.int16) if y==0 else H[az,y-1]
            for x in range(10):
                hh=hy+H[at,x];qq=Q[bz,x];ww=2*hh-qq;mask=(roots[bz]!=x+1)&(hh>0)&(hh<=3)&(ww<dz);ix=np.flatnonzero(mask)
                if len(ix):cand.extend(zip(az[ix].tolist(),bz[ix].tolist(),[y]*len(ix),[x+1]*len(ix),hh[ix].tolist(),qq[ix].tolist(),D[at[ix],x].tolist(),D[bz[ix],x].tolist()));source_indices.extend(ix.tolist())
        if cand:
            c=np.array(cand,dtype=np.int32);si=np.array(source_indices);after=transform(features(meta,c[:,6],c[:,7],10),10);wd=2*c[:,4]-c[:,5];margin=wd+lookup(after)-dz[si];bad=np.flatnonzero(margin<0);checked+=len(c)
            for k in bad:
                if len(newrecords)>=limit:break
                newrecords.append(c[k,:6].tolist());newbefore.append(vz[si[k]].tolist());newafter.append(after[k].tolist());price.append(int(wd[k]))
        processed+=len(az)
        if len(newrecords)>=limit or time.process_time()-START>CAP-7:break
    assert newrecords;before=np.array(newbefore,dtype=np.int32);after=np.array(newafter,dtype=np.int32);combined=np.concatenate((keys,before,after));newkeys,inv=np.unique(combined,axis=0,return_inverse=True);oldmap=inv[:Nold];newsrc=inv[Nold:Nold+len(before)];newdst=inv[Nold+len(before):];src=np.concatenate((oldmap[graph['src']],newsrc));dst=np.concatenate((oldmap[graph['dst']],newdst));w=np.concatenate((graph['w'],np.array(price)));nn=len(newkeys);ee=len(w);assert nn<2000000 and ee<5000000 and nn+ee<4000000;order=np.argsort(src,kind='stable');offset=np.concatenate(([0],np.cumsum(np.bincount(src,minlength=nn))));np.savez_compressed(B/'nonlinear15_transfer_01_graph.npz',keys=newkeys,src=src,dst=dst,w=w,order=order,offset=offset,source_records=np.arange(ee,dtype=np.int32)[:,None]);np.savez_compressed(B/'nonlinear15_transfer_01_actual_source_records.npz',records=np.array(newrecords,dtype=np.int32),global_edge_start=Eold)
    lv=np.zeros(nn,dtype=np.int64);lv[oldmap]=level;pa=np.full(nn,-1,dtype=np.int32);pa[oldmap]=oldstate['parent']
    with (B/'nonlinear15_transfer_01_work_00.pkl').open('xb') as f:pickle.dump({'level':lv,'parent':pa,'queue':list(range(nn)),'pending':np.ones(nn,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    result={'status':'ACTUAL_SIGNED_TRANSFER_VIOLATIONS_ADDED','positive_physical_source_states_considered':processed,'candidate_actual_packets_checked':checked,'violations_added':len(newrecords),'source_record_fields':['A','B','DELETE_helper_or_0','KEEP_target','whole_H','Q'],'nodes':nn,'edges':ee,'global_edge_start':Eold,'old_source_minimum_credit_reused':True,'new_source_engine_calls':0,'new_source_queries':0,'new_source_pair_compositions':checked,'no_HIGH_ANY_edges':True,'principal_U33':'OPEN'};out('nonlinear15_transfer_01_source_spec.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof53_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
