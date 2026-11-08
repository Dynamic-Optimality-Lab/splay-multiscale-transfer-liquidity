"""Adversarial complete A grammar against both B vines; no new primitives."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,sys,fractions
from pathlib import Path
from uniform_feature_basis import metadata,features
from diagonal_zero_feature_basis import transform,quadratic
B=Path(__file__).resolve().parent;F=fractions.Fraction
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,z['trees']));idx={t:i for i,t in enumerate(T)};roots=np.array([t[0] for t in T]);dest=np.array(z['destination']);HH=np.array(z['H']);QQ=np.array(z['Q']);meta=metadata(T,10)
    def vine(lo,hi,left=False):
        if lo>hi:return 'F'+str(hi)
        k=hi if left else lo;return (k,vine(lo,k-1,left),vine(k+1,hi,left))
    records=[]
    for b in (idx[vine(1,10)],idx[vine(1,10,True)]):
        for a in np.flatnonzero(roots==T[b][0]):
            for x in range(1,11):
                if x!=T[b][0]:records.append((int(a),b,x))
    rec=np.array(records,dtype=np.int32);a,b,x=rec.T;x=x-1;before=features(meta,a,b,10);after=features(meta,dest[a,x],dest[b,x],10);w=2*HH[a,x]-QQ[b,x];candidate=json.loads((B/'diagonal_zero_result_02.json').read_text());cc=candidate['coefficients_unscaled'];coef=np.array(cc);qb=quadratic(transform(before,10));qa=quadratic(transform(after,10));margins=w+(qa-qb)@coef;bad=np.flatnonzero(margins < -1e-6);np.savez_compressed(B/'diagonal_zero_vine_full_arrays.npz',before=before,after=after,w=w,source_records=rec);result={'status':'DIAGONAL_ZERO_FORMULA_CANDIDATE_FAILURE' if len(bad) else 'NO_VINE_CORPUS_FAILURE_NOT_PROOF','source_rows':len(rec),'negative_rows':len(bad),'minimum_margin_float':float(margins.min()),'whole_source_H_used':True,'source_primitives_reused':True,'new_source_queries':0,'principal_U33':'OPEN'}
    if len(bad):
        k=int(np.argmin(margins));exact=F(int(w[k]))+sum(F(str(c))*int(v) for c,v in zip(cc,qa[k]-qb[k]));assert exact<0;result.update(failing_source_record=rec[k].tolist(),H=int(HH[a[k],x[k]]),Q=int(QQ[b[k],x[k]]),feature_before=before[k].tolist(),feature_after=after[k].tolist(),exact_margin=str(exact),formula_exact_coefficients=[str(F(str(v))) for v in cc],source_embedding='PENDING')
    out('diagonal_zero_vine_adversary.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('formula_exact_coefficients','feature_before','feature_after')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof44_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
