"""Prepare a genuine nonlinear candidate family on the exact feature grammar."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
B=Path(__file__).resolve().parent
def main():
    import numpy as np
    z=np.load(B/'nonlinear_feature_projected_graph.npz');k=z['keys'].astype(np.int32);columns=[k[:,i] for i in range(20)]+[k[:,i]*k[:,j] for i in range(20) for j in range(i,20)];q=np.stack(columns,axis=1);np.save(B/'quadratic_feature_basis.npy',q);weights=z['w'];negative=np.flatnonzero(weights<0);dual=json.loads((B/'uniform_feature_exact_dual.json').read_text())['certificate'];ids=set(dual['edge_indices_native10']);ids.update(negative[::max(1,len(negative)//32)].tolist())
    with (B/'quadratic_feature_work_00.pkl').open('xb') as f:pickle.dump({'constraints':sorted(ids),'history':[],'iterations':0,'status':'DISCOVERY_INITIALIZED'},f)
    print(json.dumps({'status':'QUADRATIC_SOURCE_CANDIDATE_INITIALIZED','basis_columns':q.shape[1],'projected_source_nodes':q.shape[0],'source_edges':len(weights),'new_source_queries':0,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof37_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
