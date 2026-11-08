"""Factor the full current original-packet grammar by the15 comparisons."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
from diagonal_zero_feature_basis import transform
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    old=np.load(B/'diagonal_vine_graph.npz');f=transform(old['source_features'],10);keys,inv=np.unique(f,axis=0,return_inverse=True);src=inv[old['src']];dst=inv[old['dst']];w=old['w'];N=len(keys);E=len(w);assert N<2000000 and E<5000000;order=np.argsort(src,kind='stable');offset=np.concatenate(([0],np.cumsum(np.bincount(src,minlength=N))));np.savez_compressed(B/'nonlinear15_projected_graph.npz',keys=keys,src=src,dst=dst,w=w,order=order,offset=offset,source_records=np.arange(E,dtype=np.int32)[:,None])
    with (B/'nonlinear15_work_00.pkl').open('xb') as f:pickle.dump({'level':np.zeros(N,dtype=np.int64),'parent':np.full(N,-1,dtype=np.int32),'queue':list(range(N)),'pending':np.ones(N,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    out('nonlinear15_source_spec.json',{'status':'COMPLETE_CURRENT_SOURCE_PROJECTION','summary_coordinates':15,'nodes':N,'edges':E,'source_edge_record':'one-column reference into diagonal_vine_graph, preserving template/corpus/vine provenance','scope':'test ANY F of these15 comparisons, not all source invariants','actual_source_path_lifting_not_assumed':True,'new_source_queries':0,'principal_U33':'OPEN'});print(json.dumps({'status':'NONLINEAR15_PROJECTION_BUILT','nodes':N,'edges':E}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof49_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
