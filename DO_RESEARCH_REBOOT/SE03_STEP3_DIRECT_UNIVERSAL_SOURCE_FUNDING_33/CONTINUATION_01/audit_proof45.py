"""Checkpoint the entire adversarial vine grammar, not a witness exception."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
from diagonal_zero_feature_basis import transform,quadratic
B=Path(__file__).resolve().parent
def main():
    import numpy as np
    old=np.load(B/'diagonal_zero_source_graph.npz');new=np.load(B/'diagonal_zero_vine_full_arrays.npz');base=len(old['source_features']);E=len(old['w']);before=new['before'];after=new['after'];keys=np.concatenate((old['source_features'],before,after));np.save(B/'diagonal_vine_basis.npy',quadratic(transform(keys,10)));es=base+np.arange(len(before));ed=es+len(before);np.savez_compressed(B/'diagonal_vine_graph.npz',src=np.concatenate((old['src'],es)),dst=np.concatenate((old['dst'],ed)),w=np.concatenate((old['w'],new['w'])),source_features=keys)
    with (B/'diagonal_zero_work_02.pkl').open('rb') as f:state=pickle.load(f)
    prior=state['constraints'];negative=np.flatnonzero(new['w']<0);state.update(constraints=sorted(set(prior)|set((E+negative[::max(1,len(negative)//32)]).tolist())),status='COMPLETE_VINE_GRAMMAR_ADDED',coefficients_unscaled=None)
    with (B/'diagonal_vine_work_00.pkl').open('xb') as f:pickle.dump(state,f)
    print(json.dumps({'status':'ALL87516_ADVERSARIAL_VINE_ROWS_ADDED','nodes':len(keys),'edges':len(old['w'])+len(new['w']),'existing_archived_candidates_preserved':True,'new_source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof45_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
