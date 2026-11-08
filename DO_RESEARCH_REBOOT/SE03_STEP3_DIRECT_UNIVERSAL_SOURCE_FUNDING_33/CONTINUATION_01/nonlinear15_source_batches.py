"""Cumulative exact negative-H1 source expansion, audited kernel reused.
No actual splay engine is invoked; count pair/schema instantiations separately.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle,hashlib
from pathlib import Path
from uniform_feature_basis import metadata,features
from diagonal_zero_feature_basis import transform
B=Path(__file__).resolve().parent
def build(number,cap,limit=500000):
    import numpy as np
    start=time.process_time();priorname='nonlinear15_projected_graph.npz' if number==1 else 'nonlinear15_batch_%02d_graph.npz'%(number-1);old=np.load(B/priorname);Nold=len(old['keys']);Eold=len(old['w']);limit=min(limit,(1990000-Nold)//2,3990000-Eold-Nold,4990000-Eold);assert limit>0
    native=json.loads((B/'native10_source_actions.json').read_text());T=native['trees'];N=len(T);roots=np.array([t[0] for t in T]);D=np.array(native['destination']);H=np.array(native['H']);Q=np.array(native['Q']);choices={(g,x):np.flatnonzero((roots==g)&(H[:,x]==1)) for g in range(1,11) for x in range(10)};cursor=(0,0,0) if number==1 else tuple(json.loads((B/('nonlinear15_batch_%02d_cursor.json'%(number-1))).read_text())['next_cursor']);b0,x0,j0=cursor;records=[];nextcursor=None;done=False
    for b in range(b0,N):
        for x in range(x0 if b==b0 else 0,10):
            if Q[b,x]<3:continue
            aa=choices[roots[b],x];jstart=j0 if (b,x)==(b0,x0) else 0;take=min(len(aa)-jstart,limit-len(records))
            if take>0:records.extend((int(a),b,x+1) for a in aa[jstart:jstart+take])
            if len(records)==limit:nextcursor=(b,x,jstart+take);done=True;break
        if done:break
    assert records;rec=np.array(records,dtype=np.int32);a,b,x=rec.T;x=x-1;meta=metadata(T,10);before=transform(features(meta,a,b,10),10);after=transform(features(meta,D[a,x],D[b,x],10),10);combined=np.concatenate((old['keys'],before,after));keys,inv=np.unique(combined,axis=0,return_inverse=True);oldmap=inv[:Nold];newsrc=inv[Nold:Nold+len(rec)];newdst=inv[Nold+len(rec):];src=np.concatenate((oldmap[old['src']],newsrc));dst=np.concatenate((oldmap[old['dst']],newdst));w=np.concatenate((old['w'],2-Q[b,x]));nn=len(keys);ee=len(w);assert nn<2000000 and ee<5000000 and nn+ee<4000000;order=np.argsort(src,kind='stable');offset=np.concatenate(([0],np.cumsum(np.bincount(src,minlength=nn))));name='nonlinear15_batch_%02d'%number;np.savez_compressed(B/(name+'_graph.npz'),keys=keys,src=src,dst=dst,w=w,order=order,offset=offset,source_records=np.arange(ee,dtype=np.int32)[:,None]);np.savez_compressed(B/(name+'_actual_source_records.npz'),records=rec,global_edge_start=Eold)
    with (B/(name+'_work_00.pkl')).open('xb') as f:pickle.dump({'level':np.zeros(nn,dtype=np.int64),'parent':np.full(nn,-1,dtype=np.int32),'queue':list(range(nn)),'pending':np.ones(nn,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    receipt={'status':'EXACT_CACHED_SOURCE_H1_NEGATIVE_EXPANSION','number':number,'added_actual_pair_packets':len(rec),'new_primitive_engine_calls':0,'new_source_queries':0,'new_source_schema_pair_compositions':len(rec),'nodes':nn,'edges':ee,'start_cursor':cursor,'next_cursor':nextcursor,'source_enumeration_complete':nextcursor is None,'previous_graph':priorname,'new_graph':name+'_graph.npz','source_records':name+'_actual_source_records.npz','global_edge_start':Eold,'current_CPU':time.process_time()-start,'principal_U33':'OPEN'}
    with (B/(name+'_cursor.json')).open('x') as f:json.dump(receipt,f,indent=2)
    print(json.dumps(receipt))
