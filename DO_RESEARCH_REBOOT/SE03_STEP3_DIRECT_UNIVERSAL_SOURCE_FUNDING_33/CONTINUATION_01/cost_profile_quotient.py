"""Source-factorization tests; every weighted edge keeps its original handle."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
B=Path(__file__).resolve().parent
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def build(mode):
    import numpy as np
    z=json.loads((B/'native10_source_actions.json').read_text());D=np.array(z['destination']);H=np.array(z['H']);Q=np.array(z['Q']);N=len(D);physical=B/'cost_profile_physical_states.npz'
    if not physical.exists():
        endpoints=[]
        def add(rec):
            a,b=rec[:,0],rec[:,1];y=np.zeros(len(rec),dtype=np.int32) if rec.shape[1]==3 else rec[:,2];x=(rec[:,2] if rec.shape[1]==3 else rec[:,3])-1;ay=a.copy();mask=y>0;ay[mask]=D[a[mask],y[mask]-1];endpoints.append(np.stack((a,b,D[ay,x],D[b,x]),axis=1))
        add(np.load(B/'nonlinear_feature_projected_graph.npz')['source_records']);idx={fr(t):i for i,t in enumerate(z['trees'])};corpus=json.loads((B/'uniform_feature_dual_source_certificate.json').read_text())['witnesses']+[json.loads((B/'native10_width2_source_countercertificate.json').read_text())];origins=json.loads((B/'diagonal_zero_source_spec.json').read_text())['extra_source_origins'];rr=[]
        for origin in origins:
            zz=corpus[origin['source_number']];rm={r['occurrence']:r for r in zz['rows']};seg=[rm[t] for t in origin['occurrences']];rr.append([idx[fr(v)] for state in (seg[0]['before'],seg[-1]['after']) for v in state[:2]])
        endpoints.append(np.array(rr,dtype=np.int32));add(np.load(B/'diagonal_zero_vine_full_arrays.npz')['source_records']);add(np.load(B/'nonlinear15_batch_01_actual_source_records.npz')['records']);add(np.load(B/'nonlinear15_transfer_01_actual_source_records.npz')['records']);pairs=np.concatenate(endpoints);unique_pairs=np.unique(np.concatenate((pairs[:,0].astype(np.int64)*N+pairs[:,1],pairs[:,2].astype(np.int64)*N+pairs[:,3])));assert len(unique_pairs)<2000000;np.savez_compressed(physical,endpoints=pairs,unique_physical_pairs=len(unique_pairs))
    data=np.load(physical);pairs=data['endpoints'];w=np.load(B/'nonlinear15_transfer_01_graph.npz')['w'];assert len(pairs)==len(w)
    if mode=='signed':base=13;name='signed_deficit_profile';definition='ordered delta_i=q_B(i)-2a_A(i), including every negative capacity coordinate'
    elif mode=='joint':base=30;name='joint_access_cost_profile';definition='complete ordered vector of (a_A(i),q_B(i)) for all ten genuine KEEP keys'
    else:raise ValueError('unknown source profile')
    powers=base**np.arange(10,dtype=np.int64)
    def encode(a,b):
        v=Q[b]-2*H[a]+10 if mode=='signed' else 5*H[a]+Q[b];assert v.min()>=0 and v.max()<base;return v@powers
    src0=encode(pairs[:,0],pairs[:,1]);dst0=encode(pairs[:,2],pairs[:,3]);E=len(w);ids=np.arange(E);sort=np.lexsort((ids,w,dst0,src0));ss=src0[sort];tt=dst0[sort];first=np.ones(E,dtype=np.bool_);first[1:]=(ss[1:]!=ss[:-1])|(tt[1:]!=tt[:-1]);chosen=sort[first];codes=np.unique(np.concatenate((src0[chosen],dst0[chosen])));src=np.searchsorted(codes,src0[chosen]);dst=np.searchsorted(codes,dst0[chosen]);nn=len(codes);ee=len(chosen);assert nn<2000000 and ee<5000000 and nn+ee<4000000;order=np.argsort(src,kind='stable');offset=np.concatenate(([0],np.cumsum(np.bincount(src,minlength=nn))));np.savez_compressed(B/(name+'_graph.npz'),keys=codes[:,None],src=src,dst=dst,w=w[chosen],order=order,offset=offset,source_records=chosen[:,None])
    with (B/(name+'_work_00.pkl')).open('xb') as f:pickle.dump({'level':np.zeros(nn,dtype=np.int64),'parent':np.full(nn,-1,dtype=np.int32),'queue':list(range(nn)),'pending':np.ones(nn,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    result={'status':'COMPLETE_CURRENT_SOURCE_COST_PROFILE_PROJECTION','mode':mode,'definition':definition,'original_actual_packets':E,'unique_synchronized_full_pairs':int(data['unique_physical_pairs']),'profile_nodes':nn,'actual_representative_edges':ee,'base':base,'profile_offset':10 if mode=='signed' else 0,'new_source_engine_calls':0,'new_source_queries':0,'scope':'arbitrary nonlinear fixed function of this ordered source-state annotation, no arbitrary-support passing inference','principal_U33':'OPEN'}
    with (B/(name+'_source_spec.json')).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
