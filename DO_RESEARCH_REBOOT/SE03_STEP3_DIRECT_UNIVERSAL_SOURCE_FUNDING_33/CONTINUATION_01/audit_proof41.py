"""Prepare complete template constraints + every accepted-source natural packet."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle,hashlib
from pathlib import Path
from uniform_feature_basis import metadata,features
from diagonal_zero_feature_basis import transform,quadratic
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    import numpy as np
    graph=np.load(B/'nonlinear_feature_projected_graph.npz');keys=graph['keys'];src=graph['src'];dst=graph['dst'];w=graph['w'];native=json.loads((B/'native10_source_actions.json').read_text());trees=list(map(fr,native['trees']));idx={t:i for i,t in enumerate(trees)};meta=metadata(trees,10);base=len(keys);source=json.loads((B/'uniform_feature_dual_source_certificate.json').read_text());sources=source['witnesses']+[json.loads((B/'native10_width2_source_countercertificate.json').read_text())];pairs=[];prices=[];origins=[]
    for si,z in enumerate(sources):
        rows=z['rows'];ends=[i for i,r in enumerate(rows) if r['genuine_F']]
        for j,end in enumerate(ends):
            p=ends[j-1];rr=rows[p+1:end+1] if p<end else rows[p+1:]+rows[:end+1];pairs.extend([(idx[fr(s[0])],idx[fr(s[1])]) for s in (rr[0]['before'],rr[-1]['after'])]);prices.append(2*sum(r['a'] for r in rr)-sum(r['qF'] for r in rr));origins.append({'source_number':si,'occurrences':[r['occurrence'] for r in rr]})
    pairs=np.array(pairs);extra=features(meta,pairs[:,0],pairs[:,1],10);allkeys=np.concatenate((keys,extra));mat=transform(allkeys,10);q=quadratic(mat);assert q.shape[1]==135;np.save(B/'diagonal_zero_quadratic_basis.npy',q);es=base+np.arange(0,len(extra),2);ed=es+1;np.savez_compressed(B/'diagonal_zero_source_graph.npz',src=np.concatenate((src,es)),dst=np.concatenate((dst,ed)),w=np.concatenate((w,np.array(prices))),source_features=allkeys);negative=np.flatnonzero(w<0);selected=set(negative[::max(1,len(negative)//32)].tolist());selected.update(range(len(w),len(w)+len(prices)));selected.update(json.loads((B/'uniform_feature_exact_dual.json').read_text())['certificate']['edge_indices_native10'])
    with (B/'diagonal_zero_work_00.pkl').open('xb') as f:pickle.dump({'constraints':sorted(selected),'history':[],'iterations':0,'status':'SOURCE_CEGIS_INITIALIZED'},f)
    out('diagonal_zero_source_spec.json',{'status':'DISCOVERY_MODEL_FROZEN','linear_comparison_features':15,'quadratic_columns':135,'template_edges':len(w),'accepted_actual_natural_packets_added':len(prices),'nodes':len(allkeys),'edges':len(w)+len(prices),'extra_source_origins':origins,'new_source_queries':0,'identity':'ALL15 comparison coordinates vanish identically when A=B, for every n','no_universal_signed_law_proved':True,'principal_U33':'OPEN'});print(json.dumps({'status':'DIAGONAL_ZERO_SOURCE_MODEL_BUILT','columns':135,'source_edges':len(w)+len(prices),'nodes':len(allkeys)}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof41_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
