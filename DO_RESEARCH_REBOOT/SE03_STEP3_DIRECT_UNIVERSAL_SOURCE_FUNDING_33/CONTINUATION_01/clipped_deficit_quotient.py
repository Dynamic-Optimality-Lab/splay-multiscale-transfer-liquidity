"""Explicit candidate: ordered signed deficits censored below-k, plus root."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
B=Path(__file__).resolve().parent
def build(k):
    import numpy as np
    native=json.loads((B/'native10_source_actions.json').read_text());roots=np.array([t[0] for t in native['trees']]);H=np.array(native['H']);Q=np.array(native['Q']);physical=np.load(B/'cost_profile_physical_states.npz')['endpoints'];w=np.load(B/'ordered_deficit_profile_original_edges.npz')['w'];base=k+3;powers=base**np.arange(10,dtype=np.int64)
    def encode(a,b):return ((np.maximum(Q[b]-2*H[a],-k)+k)@powers)*10+roots[a]-1
    s=encode(physical[:,0],physical[:,1]);t=encode(physical[:,2],physical[:,3]);E=len(w);ids=np.arange(E);sort=np.lexsort((ids,w,t,s));ss=s[sort];tt=t[sort];first=np.ones(E,dtype=np.bool_);first[1:]=(ss[1:]!=ss[:-1])|(tt[1:]!=tt[:-1]);chosen=sort[first];keys=np.unique(np.concatenate((s[chosen],t[chosen])));src=np.searchsorted(keys,s[chosen]);dst=np.searchsorted(keys,t[chosen]);N=len(keys);EE=len(chosen);assert N<2000000 and EE<5000000 and N+EE<4000000;order=np.argsort(src,kind='stable');offset=np.concatenate(([0],np.cumsum(np.bincount(src,minlength=N))));name='root_clipped%d_deficit_profile'%k;np.savez_compressed(B/(name+'_graph.npz'),keys=keys[:,None],src=src,dst=dst,w=w[chosen],order=order,offset=offset,source_records=chosen[:,None])
    with (B/(name+'_work_00.pkl')).open('xb') as f:pickle.dump({'level':np.zeros(N,dtype=np.int64),'parent':np.full(N,-1,dtype=np.int32),'queue':list(range(N)),'pending':np.ones(N,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    result={'status':'ROOT_AWARE_CENSORED_SIGNED_PROFILE_BUILT','negative_cutoff':k,'definition':'current root plus ordered max(q_B(i)-2a_A(i),-k), for every marked key','nodes':N,'edges':EE,'original_actual_packets':E,'base':base,'source_edge_ids_preserved':True,'new_source_engine_calls':0,'new_source_queries':0,'principal_U33':'OPEN'}
    with (B/(name+'_source_spec.json')).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
