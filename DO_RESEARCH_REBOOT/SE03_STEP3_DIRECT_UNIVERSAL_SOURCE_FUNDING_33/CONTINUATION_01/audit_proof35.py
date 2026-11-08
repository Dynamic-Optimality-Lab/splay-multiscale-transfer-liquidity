"""Projected source grammar for an arbitrary nonlinear function of20 features."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,sys,pickle
from pathlib import Path
from uniform_feature_basis import metadata,features
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    z=json.loads((B/'native10_source_actions.json').read_text());prior=np.load(B/'uniform_feature_extended_arrays.npz');rec=prior['native10_records'];a,b,x=rec.T;a=a.astype(np.int32);b=b.astype(np.int32);x=x.astype(np.int32)-1;dest=np.array(z['destination']);meta=metadata(z['trees'],10);before=features(meta,a,b,10);after=features(meta,dest[a,x],dest[b,x],10);mat=np.concatenate((before,after));keys,inverse=np.unique(mat,axis=0,return_inverse=True);N=len(keys);E=len(a);assert N<2000000 and E<5000000;src=inverse[:E];dst=inverse[E:];w=2-np.array(z['Q'],dtype=np.int8)[b,x];order=np.argsort(src,kind='stable');counts=np.bincount(src,minlength=N);offset=np.concatenate(([0],np.cumsum(counts)));np.savez_compressed(B/'nonlinear_feature_projected_graph.npz',keys=keys,src=src,dst=dst,w=w,order=order,offset=offset,source_records=rec)
    with (B/'nonlinear_feature_work_00.pkl').open('xb') as f:pickle.dump({'level':np.zeros(N,dtype=np.int64),'parent':np.full(N,-1,dtype=np.int32),'queue':list(range(N)),'pending':np.ones(N,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    out('nonlinear_feature_projected_spec.json',{'status':'COMPLETE_FINITE_TEMPLATE_PROJECTION_NOT_A_UNIVERSAL_PROOF','features':20,'nodes':N,'edges':E,'scope':'native-ten B complete grammar, three synchronized one-event A templates per target/root','refutable_candidate':'ANY nonlinear fixed F of the20 summaries on natural packets, if a source-realized negative projected cycle exists','actual_source_cycle_not_assumed':True,'new_source_queries':0,'principal_U33':'OPEN'});print(json.dumps({'status':'PROJECTED_GRAMMAR_BUILT','nodes':N,'edges':E}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof35_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
