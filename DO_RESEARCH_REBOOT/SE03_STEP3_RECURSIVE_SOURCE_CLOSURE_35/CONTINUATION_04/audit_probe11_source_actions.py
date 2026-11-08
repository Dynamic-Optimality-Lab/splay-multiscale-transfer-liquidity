"""Distinct leaf INSERTION derivation, plus fresh mutable path actions."""
import hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bare(t):return (t[0],bare(t[1]),bare(t[2])) if isinstance(t,(list,tuple)) else None
def insert(t,k):
    if t is None:return (k,None,None)
    if k<t[0]:return (t[0],insert(t[1],k),t[2])
    assert k>t[0];return (t[0],t[1],insert(t[2],k))
def relabel(t,k):return None if t is None else (t[0]+(t[0]>=k),relabel(t[1],k),relabel(t[2],k))
def leaves(t):
    if t is None:return []
    if t[1] is None and t[2] is None:return [t[0]]
    return leaves(t[1])+leaves(t[2])
def main():
    global V
    with (F/'probe11_source_actions.pkl').open('rb') as f:z=pickle.load(f)
    native=json.loads((B/'native10_source_actions.json').read_text());T=z['trees'];ids={t:i for i,t in enumerate(T)};n=len(T);assert n==58786
    old=[bare(t) for t in native['trees']];nt=len(old);LL=[leaves(t) for t in T]
    lo=np.array([v[0] for v in LL],dtype=np.int8);hi=np.array([v[-1] for v in LL],dtype=np.int8)
    remove_lo=np.full(n,-1,dtype=np.int32);remove_hi=remove_lo.copy();dest=np.full((11,nt),65535,dtype=np.uint16)
    for k in range(1,12):
        for j,t in enumerate(old):
            full=insert(relabel(t,k),k);i=ids[full];dest[k-1,j]=i
            if lo[i]==k:remove_lo[i]=j
            if hi[i]==k:remove_hi[i]=j
        assert time.process_time()-START<CAP-3
    assert np.all(remove_lo>=0) and np.all(remove_hi>=0)
    nd=np.array(native['destination'],dtype=np.uint16);nh=np.array(native['H'],dtype=np.uint8);nq=np.array(native['Q'],dtype=np.uint8)
    exceptions=[];checked=0
    for x in range(1,12):
        ex=(lo==x)&(hi==x);leaf=np.where(hi!=x,hi,lo);oldid=np.where(hi!=x,remove_hi,remove_lo);col=x-1-(leaf<x)
        col[ex]=0;oldid[ex]=0;good=~ex
        assert np.array_equal(z['destination'][good,x-1],dest[leaf[good]-1,nd[oldid[good],col[good]]])
        assert np.array_equal(z['H'][good,x-1],nh[oldid[good],col[good]]) and np.array_equal(z['Q'][good,x-1],nq[oldid[good],col[good]])
        checked+=int(good.sum());exceptions.extend((int(i),x) for i in np.flatnonzero(ex))
    assert set(exceptions)==set(z['fresh_actions']) and len(exceptions)==1024
    spec=importlib.util.spec_from_file_location('CS35_distinct_mutable_paths',B/'audit_verify79.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    for i,x in exceptions:
        t=V.Mutable(T[i]);h,q,_=t.splay(x,False)
        assert ids[bare(t.snapshot())]==int(z['destination'][i,x-1]) and (h,q)==(int(z['H'][i,x-1]),int(z['Q'][i,x-1]))
    out={'status':'PASS_COMPLETE_ELEVEN_KEY_SOURCE_ACTIONS','tree_count':n,'cached_lift_rows_checked':checked,
      'fresh_mutable_Hamiltonian_rows':len(exceptions),'total_actual_actions':checked+len(exceptions),
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'method':'independent source interval insertion maps; opposite eligible leaf choice; old native10 semantic pins; fresh mutable full-path rows',
      'JR35':'OPEN','passing_source_primitive_table_is_funding_proof':False,
      'input_sha256':{str(p):sha(p) for p in [F/'probe11_source_actions.pkl',B/'native10_source_actions.json',B/'native10_source_independent_audit.json',B/'OFF_PATH_LEAF_SOURCE_LIFT.md']}}
    with (F/'independent_probe11_source_actions.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify116_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,
          'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS},f)
