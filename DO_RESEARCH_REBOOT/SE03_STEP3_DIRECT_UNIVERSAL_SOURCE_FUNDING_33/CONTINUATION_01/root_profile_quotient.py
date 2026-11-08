"""Root-aware state factorization. Preserve every actual edge's provenance."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
B=Path(__file__).resolve().parent
def build(mode):
    import numpy as np
    native=json.loads((B/'native10_source_actions.json').read_text());roots=np.array([t[0] for t in native['trees']]);physical=np.load(B/'cost_profile_physical_states.npz')['endpoints'];old=np.load(B/'ordered_deficit_profile_original_edges.npz');w=old['w']
    if mode=='positive':src0=old['src_codes'];dst0=old['dst_codes'];name='root_positive_deficit_profile'
    elif mode=='signed':
        H=np.array(native['H']);Q=np.array(native['Q']);powers=13**np.arange(10,dtype=np.int64);src0=(Q[physical[:,1]]-2*H[physical[:,0]]+10)@powers;dst0=(Q[physical[:,3]]-2*H[physical[:,2]]+10)@powers;name='root_signed_deficit_profile'
    else:raise ValueError(mode)
    src0=src0*10+roots[physical[:,0]]-1;dst0=dst0*10+roots[physical[:,2]]-1;E=len(w);ids=np.arange(E);srt=np.lexsort((ids,w,dst0,src0));ss=src0[srt];tt=dst0[srt];first=np.ones(E,dtype=np.bool_);first[1:]=(ss[1:]!=ss[:-1])|(tt[1:]!=tt[:-1]);chosen=srt[first];codes=np.unique(np.concatenate((src0[chosen],dst0[chosen])));src=np.searchsorted(codes,src0[chosen]);dst=np.searchsorted(codes,dst0[chosen]);N=len(codes);EE=len(chosen);assert N<2000000 and EE<5000000 and N+EE<4000000;order=np.argsort(src,kind='stable');offset=np.concatenate(([0],np.cumsum(np.bincount(src,minlength=N))));np.savez_compressed(B/(name+'_graph.npz'),keys=codes[:,None],src=src,dst=dst,w=w[chosen],order=order,offset=offset,source_records=chosen[:,None])
    with (B/(name+'_work_00.pkl')).open('xb') as f:pickle.dump({'level':np.zeros(N,dtype=np.int64),'parent':np.full(N,-1,dtype=np.int32),'queue':list(range(N)),'pending':np.ones(N,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    result={'status':'ROOT_AWARE_SOURCE_PROFILE_PROJECTED','mode':mode,'retained_current_root':True,'nodes':N,'actual_representative_edges':EE,'original_actual_packets':E,'code':'10*ordered_profile_code+(current_root_rank-1)','new_source_queries':0,'not_an_actual_full_state_history_graph':True,'principal_U33':'OPEN'}
    with (B/(name+'_source_spec.json')).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
