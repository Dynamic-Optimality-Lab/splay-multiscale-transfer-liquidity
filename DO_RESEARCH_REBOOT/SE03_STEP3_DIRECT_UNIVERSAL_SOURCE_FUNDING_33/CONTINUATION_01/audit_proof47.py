"""Extract exact quadratic dual if the remaining cumulative allowance permits."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle,sys,fractions,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1]);F=fractions.Fraction
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    from scipy.optimize import linprog
    graph=np.load(B/'diagonal_vine_graph.npz');q=np.load(B/'diagonal_vine_basis.npy');src=graph['src'];dst=graph['dst'];w=graph['w']
    with (B/'diagonal_vine_work_01.pkl').open('rb') as f:s=pickle.load(f)
    assert 'INFEASIBLE' in s['status'];ids=np.array(s['constraints']);X=q[dst[ids]]-q[src[ids]];scale=np.maximum(abs(X).max(0),1);xx=X/scale;available=max(.1,CAP-(time.process_time()-START)-1.5);res=linprog(w[ids].astype(float),A_eq=np.concatenate((xx.T,np.ones((1,len(ids))))),b_eq=np.array([0.]*135+[1.]),bounds=(0,None),method='highs',options={'time_limit':available});assert res.success and res.fun < -1e-7;active=np.flatnonzero(res.x>1e-9);edges=ids[active];rows=(q[dst[edges]]-q[src[edges]]).T.tolist()+[[1]*len(edges)];rhs=[0]*135+[1]
    out('diagonal_zero_dual_numeric_checkpoint.json',{'status':'NUMERIC_QUADRATIC_DUAL_EXACT_EXTRACTION_PENDING','source_edge_ids':edges.tolist(),'weights_approximate':res.x[active].tolist(),'price_approximate':float(res.fun),'exact_integer_equation_matrix':rows,'rhs':rhs,'source_prices':w[edges].tolist(),'source_embedding':'PENDING for every newly selected edge; no family refutation promoted','new_source_queries':0,'principal_U33':'OPEN'});print(json.dumps({'status':'NUMERIC_DUAL_SAVED','support':len(edges),'objective':float(res.fun),'CPU_before_exact':time.process_time()-START}),flush=True)
    if time.process_time()-START>CAP-2:
        print('Exact extraction checkpointed under cumulative resource cap',flush=True);return
    from sympy import Matrix
    from sympy.polys.matrices import DomainMatrix
    M=DomainMatrix.from_Matrix(Matrix(rows));R=DomainMatrix.from_Matrix(Matrix(rhs));num,den=M.solve_den(R,method='rref');weights=[F(int(v),int(den)) for v in num.to_Matrix()];assert len(weights)==len(edges) and all(v>0 for v in weights) and sum(weights)==1;weighted=[sum(weights[j]*int(rows[k][j]) for j in range(len(weights))) for k in range(135)];price=sum(weight*int(w[e]) for weight,e in zip(weights,edges));assert not any(weighted) and price<0
    out('diagonal_zero_quadratic_exact_dual.json',{'status':'EXACT_ALGEBRAIC_DUAL_SOURCE_REALIZATION_PENDING','source_edge_ids':edges.tolist(),'weights':list(map(str,weights)),'weighted_feature_changes':list(map(str,weighted)),'weighted_price':str(price),'new_source_queries':0,'principal_U33':'OPEN','source_domain_and_independent_audit':'PENDING; exact algebra alone is not a promoted original-source family refutation','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('diagonal_zero_dual_numeric_checkpoint.json','diagonal_vine_graph.npz','diagonal_vine_basis.npy')}});print(json.dumps({'status':'EXACT_QUADRATIC_DUAL_FOUND_SOURCE_REALIZATION_PENDING','support':len(weights),'price':str(price)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof47_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
