"""Independent complete original A/B replay of the reconstructed C20 word."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def core(t,M):
    out=set()
    def go(u):
        if u is None:return False
        a,b=go(u[1]),go(u[2]);yes=a or b or u[0] in M
        if yes:out.add(u[0])
        return yes
    go(t);return out
def main():
    global V
    rp=F/'C20_hybrid_source_control.json';r=json.loads(rp.read_text())
    for p,h in r['input_sha256'].items():assert sha(Path(p))==h
    sp=importlib.util.spec_from_file_location('C20_hybrid_distinct_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    a0,b0=tup(r['initial_A']),tup(r['initial_BF']);A=V.Mutable(a0);BF=V.Mutable(b0);M=set(range(1,14,2))
    cc=();a=q=0;Q=core(b0,M);assert len(Q)==13
    for t,row in enumerate(r['period_rows'],1):
        ab,bb=tup(A.snapshot()),tup(BF.snapshot());assert (ab,bb)==(tup(row['A_before']),tup(row['BF_before']))
        h,_,_=A.splay(row['key'],False);qq=0
        if row['kind']=='K':
            _,qq,_=BF.splay(row['key'],False)
            if bb[0]!=row['key']:cc=(row['key'],)+tuple(x for x in cc if x!=row['key'])
        assert (h,qq)==(row['a'],row['qF'])
        assert tup(A.snapshot())==tup(row['A_after']) and tup(BF.snapshot())==tup(row['BF_after'])
        assert core(tup(BF.snapshot()),M)==Q;a+=h;q+=qq
    assert tup(A.snapshot())==a0 and tup(BF.snapshot())==b0 and (a,q)==(232,66) and set(cc)==M
    startcc=cc
    for row in r['period_rows']:
        if row['genuine_F']:cc=(row['key'],)+tuple(x for x in cc if x!=row['key'])
    assert cc==startcc
    out={'status':'PASS_FULL_C20_ORIGINAL_A_B_SOURCE_REPLAY_AND_MAXIMAL_CORE',
      'operations':167,'A':a,'QF':q,'physical_keys':13,'genuine_support':7,'fixed_full_core':13,
      'full_chart_recurrence_after_warmup':True,'BE_closed_period':'inherited exact finite recurrence, not numerically selected here',
      'reachability':'ordinary A-only transformation from common diagonal, no prefix donor',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'full_cost_comparison':'already covered at the exact full-source scope by the accepted maximal-seven/core13 theorem',
      'new_hybrid_universal_funding_claimed':False,'JR35':'OPEN','reservation':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in (rp,F/'SEVEN_KEY_MAXIMAL_CORE_FULL_PROOF.md',F/'independent_paired_branch_certificate.json')}}
    with (F/'independent_C20_hybrid_source.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_verify144_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
