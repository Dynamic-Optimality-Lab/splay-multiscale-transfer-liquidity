"""Independent new tag reconstruction; inherited A/closure proofs are reused."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';S=C/'CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def ancestors(t,x):
    z=[]
    while t[0]!=x:z.append(t[0]);t=t[1] if x<t[0] else t[2]
    return z
def core(t,marks):return set(marks)|set().union(*(set(ancestors(t,x)) for x in marks))
def main():
    global V
    rp=F/'FP_SI34_source_countercut.json';r=json.loads(rp.read_text())
    for p,h in r['input_sha256'].items():assert sha(Path(p))==h
    sp=importlib.util.spec_from_file_location('independent_SI34_new_tags',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    rows=r['B_rows'];bf=V.Mutable(tup(rows[0]['before']))
    for row in rows:
        assert tup(bf.snapshot())==tup(row['before'])
        _,q,_=bf.splay(row['target'],False)
        assert q==row['Q'] and tup(bf.snapshot())==tup(row['after'])
    assert tup(bf.snapshot())==tup(rows[0]['before'])
    allunits=set();alldemand=set();checks=[]
    for annotation in r['new_FP_tag_annotations']:
        e=annotation['KEEP_ordinal']-1;x=annotation['target'];N=len(rows)
        prev=next((e-d)%N for d in range(1,N+1) if rows[(e-d)%N]['target']==x)
        active={x};entered={};tagcount={}
        for offset in range(1,(e-prev)%N or N):
            row=rows[(prev+offset)%N];y=row['target'];old=core(tup(row['before']),active)
            after=core(tup(row['after']),active|{y});extra=after-old
            if y in active:assert not extra
            else:
                assert len(extra)<=2
                for z in extra:entered.setdefault(z,(y,row['KEEP_ordinal']))
            active.add(y)
        pp=ancestors(tup(rows[e]['before']),x)
        for d in annotation['demands']:
            k=d['demand'][1];G,P0=pp[-2*k:-2*k+2] if k>1 else pp[-2:]
            assert [G,P0]==d['original_B_operands']
            actual=[entered[G],entered[P0]];want=[(a['proxy'],a['birth_KEEP_ordinal']) for a in d['source_tags']]
            assert actual==want and actual[0][0]==actual[1][0]==d['forced_proxy']
            y=d['forced_proxy'];assert y in (15,x-2,1)
            # The established exhaustive all-retirement pool implies the
            # same first-retirement access; all those accesses have H1.
            expected={(f'v{x}',1,b) for b in (0,1)}
            if y==15:expected|={('c',1,b) for b in (0,1)}
            assert expected=={tuple(u) for u in d['first_loss_and_own_units']}
            allunits|=expected;alldemand.add(tuple(d['demand']))
        checks.append({'target':x,'forced_proxies':annotation['forced_proxies_bottom_up']})
    assert len(alldemand)==9 and len(allunits)==8
    assert allunits=={tuple(u) for u in r['exact_cut']['neighborhood']}
    assert alldemand=={tuple(d) for d in r['exact_cut']['demands']}
    out={'status':'PASS_SOURCE_EXACT_FP_FIRST_LOSS_PLUS_OWN_COUNTERCUT',
      'genuine_support':8,'physical_keys':15,'demands':9,'eligible_units':8,'deficiency':1,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'new_tag_checks':checks,
      'full_A_Gamma_and_BE_stream':'not newly expanded; independently accepted symbolic source closure and A pool exhaustion reused',
      'FP_existence_lemmas':'RETAINED','FP_first_loss_plus_own_joint_sufficiency':'REFUTED',
      'all_joint_source_licensed_augmentation_or_JR35':'OPEN','Coarse_Double_counterexample':False,
      'input_sha256':{str(p):sha(p) for p in (rp,S/'independent_symbolic_source_audit.json',S/'independent_critical_source_audit.json')}}
    with (F/'independent_FP_SI34_source_countercut.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_verify141_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
