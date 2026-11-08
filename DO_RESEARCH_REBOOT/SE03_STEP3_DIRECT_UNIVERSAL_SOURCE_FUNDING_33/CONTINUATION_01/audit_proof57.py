"""Test arbitrary functions of the ORDERED positive per-key deficit vector."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
B=Path(__file__).resolve().parent
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    z=json.loads((B/'native10_source_actions.json').read_text());D=np.array(z['destination']);H=np.array(z['H']);Q=np.array(z['Q']);powers=3**np.arange(10,dtype=np.int64);sources=[];targets=[];prices=[]
    def encode(a,b):
        p=np.maximum(Q[b]-2*H[a],0);assert p.max()<=2;return p@powers
    def add(records):
        a,b=records[:,0],records[:,1];y=np.zeros(len(a),dtype=np.int32) if records.shape[1]==3 else records[:,2];x=(records[:,2] if records.shape[1]==3 else records[:,3])-1;ay=a.copy();mask=y>0;ay[mask]=D[a[mask],y[mask]-1];at=D[ay,x];bt=D[b,x];hh=H[ay,x].copy();hh[mask]+=H[a[mask],y[mask]-1];sources.append(encode(a,b));targets.append(encode(at,bt));prices.append(2*hh-Q[b,x])
    add(np.load(B/'nonlinear_feature_projected_graph.npz')['source_records']);idx={fr(t):i for i,t in enumerate(z['trees'])};corpus=json.loads((B/'uniform_feature_dual_source_certificate.json').read_text())['witnesses']+[json.loads((B/'native10_width2_source_countercertificate.json').read_text())];origins=json.loads((B/'diagonal_zero_source_spec.json').read_text())['extra_source_origins'];aa=[];bb=[];at=[];bt=[];ww=[]
    for origin in origins:
        zs=corpus[origin['source_number']];rm={r['occurrence']:r for r in zs['rows']};rr=[rm[t] for t in origin['occurrences']];a,b=(idx[fr(v)] for v in rr[0]['before'][:2]);a2,b2=(idx[fr(v)] for v in rr[-1]['after'][:2]);aa.append(a);bb.append(b);at.append(a2);bt.append(b2);ww.append(2*sum(r['a'] for r in rr)-sum(r['qF'] for r in rr))
    sources.append(encode(np.array(aa),np.array(bb)));targets.append(encode(np.array(at),np.array(bt)));prices.append(np.array(ww));add(np.load(B/'diagonal_zero_vine_full_arrays.npz')['source_records']);add(np.load(B/'nonlinear15_batch_01_actual_source_records.npz')['records']);add(np.load(B/'nonlinear15_transfer_01_actual_source_records.npz')['records']);s=np.concatenate(sources);t=np.concatenate(targets);w=np.concatenate(prices);old=np.load(B/'nonlinear15_transfer_01_graph.npz');assert np.array_equal(w,old['w']);E=len(w);ids=np.arange(E);order=np.lexsort((ids,w,t,s));ss=s[order];tt=t[order];first=np.ones(E,dtype=np.bool_);first[1:]=(ss[1:]!=ss[:-1])|(tt[1:]!=tt[:-1]);chosen=order[first];codes=np.unique(np.concatenate((s[chosen],t[chosen])));src=np.searchsorted(codes,s[chosen]);dst=np.searchsorted(codes,t[chosen]);weight=w[chosen];N=len(codes);edges=len(chosen);order=np.argsort(src,kind='stable');offset=np.concatenate(([0],np.cumsum(np.bincount(src,minlength=N))));np.savez_compressed(B/'ordered_deficit_profile_graph.npz',keys=codes[:,None],src=src,dst=dst,w=weight,order=order,offset=offset,source_records=chosen[:,None]);np.savez_compressed(B/'ordered_deficit_profile_original_edges.npz',src_codes=s,dst_codes=t,w=w)
    with (B/'ordered_deficit_profile_work_00.pkl').open('xb') as f:pickle.dump({'level':np.zeros(N,dtype=np.int64),'parent':np.full(N,-1,dtype=np.int32),'queue':list(range(N)),'pending':np.ones(N,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    result={'status':'ORDERED_POSITIVE_DEFICIT_SOURCE_PROJECTION_BUILT','original_actual_packet_edges':E,'distinct_profiles':N,'distinct_profile_pairs_with_actual_minimum_edge':edges,'profile_code':'sum_i max(0,q_B(i)-2a_A(i))*3^(i-1)','scope':'arbitrary fixed function of the complete ordered positive deficit vector, at native-ten support','minimum_edge_is_an_actual_original_packet':True,'not_an_actual_source_history_graph':True,'new_source_queries':0,'principal_U33':'OPEN'};out('ordered_deficit_profile_source_spec.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof57_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
