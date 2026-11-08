"""Distinct primitive controls + symbolic free-port exact-return identities.
The universal argument is the written finite graph/source proof, not
an extrapolation from the following controls.
"""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def balanced(ks):
    if not ks:return None
    i=len(ks)//2;return (ks[i],balanced(ks[:i]),balanced(ks[i+1:]))
def depths(t):
    out={}
    def go(u,d):
        if u is not None:out[u[0]]=d;go(u[1],d+1);go(u[2],d+1)
    go(t,0);return out
def prefix(t,d):return 'hidden' if d<0 and t is not None else (None if t is None else (t[0],prefix(t[1],d-1),prefix(t[2],d-1)))
def main():
    global V
    spec=importlib.util.spec_from_file_location('FD35_independent_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    # Two previously checked H1 root identities, now with FREE payloads.
    original=(20,'L',(30,'C',(40,'D','E')))
    rr=(40,(30,(20,'L','C'),'D'),'E')
    def right_right(t):
        g,A=t[0],t[1];p,B=t[2][0],t[2][1];x,C,D=t[2][2];return (x,(p,(g,A,B),C),D)
    def left_left(t):
        g,D=t[0],t[2];p,C=t[1][0],t[1][2];x,A,B=t[1][1];return (x,A,(p,B,(g,C,D)))
    assert right_right(original)==rr and left_left(rr)==original
    K=list(range(1,1028));M=set(K);g=2;v=3;E=list(range(4,1028));assert len(E)==1024
    BF=(g,(1,None,None),balanced(list(range(3,1028))));dd=depths(BF);deep=min(E,key=lambda k:(-dd[k],k));assert dd[deep]>=10
    def Aof(x):return (g,(1,None,None),(v,None,(x,balanced([k for k in E if k<x]),balanced([k for k in E if k>x]))))
    def mirror(t):return None if t is None else (1028-t[0],mirror(t[2]),mirror(t[1]))
    expected=prefix(Aof(deep),1);controls=[]
    for x in (deep,max(E)):
        assert prefix(Aof(x),1)==expected
        for orientation,aa,bb,xx,gg in [('LR',Aof(x),BF,x,g),('RL',mirror(Aof(x)),mirror(BF),1028-x,1028-g)]:
            A,Bf=V.Mutable(aa),V.Mutable(bb);H=Q=0;rows=[]
            for t,k in enumerate((xx,gg),1):
                ab,b0=A.snapshot(),Bf.snapshot();h,_,ev=A.splay(k,True);_,q,_=Bf.splay(k,False);H+=h;Q+=q
                assert h==1 and len(ev)==1 and ev[0]['pattern'] in ('RR','LL')
                rows.append({'t':t,'kind':'K','key':k,'a':h,'qF':q,'A_before':ab,'BF_before':b0,
                  'A_after':A.snapshot(),'BF_after':Bf.snapshot(),'A_events':ev})
            assert tup(A.snapshot())==aa and H==2
            if x==deep:assert Q>=5
            controls.append({'orientation':orientation,'physical_genuine_keys':len(M),'target':xx,'g':gg,
              'A_prefix_depth1':prefix(aa,1),'A_returns_exactly':True,'H':H,'Q':Q,'price':4-Q,'rows':rows,
              'numeric_full_period_claimed':False})
    report={'status':'PASS_FREE_PORT_IDENTITIES_AND_DISTINCT_SOURCE_CONTROLS','formal_free_port_identities':2,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'controls':controls,
      'universal_theorem_basis':'written proof with fixed-backbone Gamma, sink SCC, all-key walk, and prescribed-state source embedding',
      'proof_scope':'failure of ANY bounded A-prefix potential for all natural root-return source packets',
      'JR35':'OPEN','Coarse_Double_refuted':False,'not_one_negative_original_source_cycle':True,
      'input_sha256':{str(p):sha(p) for p in [F/'FIXED_DEPTH_SOURCE_INFORMATION_THEOREM.md',F/'SEPARABLE_SOURCE_POTENTIAL_OBSTRUCTION.md',
        B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',B/'audit_verify79.py']}}
    with (F/'independent_fixed_depth_controls.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('controls','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify115_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,
          'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS},f)
