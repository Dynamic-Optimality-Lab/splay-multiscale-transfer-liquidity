"""Seek an EXACT finite dual obstruction, with ten-anchor scope kept separate."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,sys,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1]);F=fractions.Fraction
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def exactsolve(rows,rhs):
    M=[[F(v) for v in row]+[F(b)] for row,b in zip(rows,rhs)];n=len(rows[0]);rank=0;piv=[]
    for c in range(n):
        k=next((k for k in range(rank,len(M)) if M[k][c]),None)
        if k is None:continue
        M[rank],M[k]=M[k],M[rank];p=M[rank][c];M[rank]=[v/p for v in M[rank]]
        for k in range(len(M)):
            if k!=rank and M[k][c]:p=M[k][c];M[k]=[a-p*b for a,b in zip(M[k],M[rank])]
        piv.append(c);rank+=1
    assert all(any(row[:n]) or row[n]==0 for row in M);assert rank==n
    ans=[F(0)]*n
    for i,c in enumerate(piv):ans[c]=M[i][n]
    return ans
def main():
    import numpy as np
    from scipy.optimize import linprog
    z=np.load(B/'uniform_feature_extended_arrays.npz');off=int(z['native7_count']);X=z['X'][off:].astype(np.float64);w=z['w'][off:].astype(np.float64);chosen=set(np.flatnonzero(w<0)[::max(1,int((w<0).sum())//20)].tolist());history=[];certificate=None
    for iteration in range(100):
        ids=sorted(chosen);xx=X[ids];ww=w[ids];res=linprog(np.zeros(20),A_ub=-xx,b_ub=ww,bounds=[(None,None)]*20,method='highs')
        if res.status==2:
            dual=linprog(ww,A_eq=np.concatenate((xx.T,np.ones((1,len(ids))))),b_eq=np.array([0.]*20+[1.]),bounds=(0,None),method='highs');assert dual.success and dual.fun<0;active=np.flatnonzero(dual.x>1e-9);edges=[ids[i] for i in active];intX=z['X'][off+np.array(edges)];weights=exactsolve(intX.T.tolist()+[[1]*len(edges)],[0]*20+[1]);assert all(v>0 for v in weights);delta=[sum(weight*int(row[k]) for weight,row in zip(weights,intX)) for k in range(20)];weighted=sum(weight*int(z['w'][off+edge]) for weight,edge in zip(weights,edges));assert not any(delta) and weighted<0
            certificate={'edge_indices_native10':edges,'weights':[str(v) for v in weights],'weighted_price':str(weighted),'weighted_feature_change':[str(v) for v in delta],'native10_source_records':z['native10_records'][edges].tolist()};break
        assert res.success;val=X@res.x+w;bad=np.flatnonzero(val < -1e-7);history.append({'iteration':iteration,'constraints':len(ids),'violations':len(bad),'minimum_margin':float(val.min())})
        if not len(bad):break
        worst=bad[np.argsort(val[bad])[:20]];chosen.update(worst.tolist())
        if time.process_time()-START>CAP-3:break
    result={'status':'EXACT_NATIVE10_FEATURE_FARKAS_CANDIDATE' if certificate else ('FINITE_NATIVE10_FEATURE_CANDIDATE' if res.success and not len(bad) else 'CONSTRAINT_GENERATION_CHECKPOINT'),'feature_count':20,'certificate':certificate,'history':history,'feasible_coefficients':res.x.tolist() if res.success else None,'source_embeddings_and_independent_audit':'PENDING, no source theorem refutation promoted yet','new_source_queries':0,'principal_U33':'OPEN'};out('uniform_feature_exact_dual.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof34_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
