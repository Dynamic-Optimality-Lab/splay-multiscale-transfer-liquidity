"""Cumulative, checkpointed source-inequality synthesis. Finite pass != proof."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
B=Path(__file__).resolve().parent
def run(number,cap):
    import numpy as np
    from scipy.optimize import linprog
    start=time.process_time();graph=np.load(B/'nonlinear_feature_projected_graph.npz');src=graph['src'];dst=graph['dst'];w=graph['w'].astype(np.float64);q=np.load(B/'quadratic_feature_basis.npy').astype(np.float64);scale=np.maximum(abs(q).max(0),1);q/=scale
    with (B/('quadratic_feature_work_%02d.pkl'%(number-1))).open('rb') as f:s=pickle.load(f)
    chosen=set(s['constraints']);status='SYNTHESIS_CHECKPOINT';theta=None
    while time.process_time()-start<cap-3:
        ids=np.array(sorted(chosen));X=q[dst[ids]]-q[src[ids]];available=cap-2-(time.process_time()-start)
        if available<.5:break
        res=linprog(np.zeros(q.shape[1]),A_ub=-X,b_ub=w[ids],bounds=[(None,None)]*q.shape[1],method='highs',options={'time_limit':max(.1,available-1)})
        s['iterations']+=1
        if res.status==2:status='QUADRATIC_MODEL_NUMERICALLY_INFEASIBLE_EXACT_CERTIFICATE_PENDING';break
        if not res.success:status='SOLVER_CPU_CHECKPOINT';break
        theta=res.x;phi=q@theta;value=w+phi[dst]-phi[src];bad=np.flatnonzero(value < -1e-7);history={'iteration':s['iterations'],'constraints':len(ids),'violations':len(bad),'minimum_margin':float(value.min())};s['history'].append(history);print(json.dumps(history),flush=True)
        if not len(bad):status='FINITE_QUADRATIC_SOURCE_CANDIDATE_NOT_UNIVERSAL';s['coefficients_unscaled']=(theta/scale).tolist();break
        worst=bad[np.argsort(value[bad])[:40]];chosen.update(worst.tolist())
    s.update(constraints=sorted(chosen),status=status)
    with (B/('quadratic_feature_work_%02d.pkl'%number)).open('xb') as f:pickle.dump(s,f)
    result={'status':status,'number':number,'basis_columns':q.shape[1],'iterations':s['iterations'],'selected_constraints':len(chosen),'latest_history':s['history'][-1] if s['history'] else None,'coefficients_unscaled':s.get('coefficients_unscaled'),'source_queries':0,'new_source_engine_invocations':False,'uniform_proof':False,'principal_U33':'OPEN'}
    with (B/('quadratic_feature_result_%02d.json'%number)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
