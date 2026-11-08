"""Distinct mutable-source control plus explicit review of the parameterized proof.

The finite control is not the proof of the all-m statement. No new source
engine is hidden behind the static recurrence checks.
"""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def path(t,x):
    out=[]
    while True:
        out.append(t[0])
        if t[0]==x:return out
        t=t[1] if x<t[0] else t[2]
def main():
    global V
    p=F/'USR35_m4_control.json';r=json.loads(p.read_text())
    for s,h in r['input_sha256'].items():assert sha(Path(s))==h
    assert r['m']==4 and r['forward_count']==13 and r['M']==92 and r['Q']==158
    # Formal coefficient identities in independent variables m and E=2^(m+1).
    # M=(4m-2)+(8m)+E+(4m-2); Q=2M-2(3m+1).
    parts=[(4,-2,0),(8,0,0),(0,0,1),(4,-2,0)]
    M=tuple(sum(p[i] for p in parts) for i in range(3));assert M==(16,-4,1)
    assert tuple(2*a-b for a,b in zip(M,(6,2,0)))==(26,-10,2)
    assert (2*(16)-26,2*(-4)-(-10),2*1-2)==(6,2,0)
    spec=importlib.util.spec_from_file_location('USR35_distinct_source',B/'audit_verify79.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    b=V.Mutable(tup(r['initial']));marks=set(range(1,r['size']+1,2));fw=r['B_rows'][:r['forward_count']]
    for row in fw:
        assert tup(b.snapshot())==tup(row['before'])
        _,q,events=b.splay(row['target'],True)
        assert q==row['Q'] and tup(b.snapshot())==tup(row['after'])
        assert all(e['pattern'] in ('LL','RR') and e['grandparent'] in marks and e['parent'] not in marks for e in events)
    claims=[]
    for c in r['critical']:
        G,X=c['G'],c['X'];a=V.Mutable(tup(c['A_before']));h,_,ev=a.splay(X,True)
        assert h==1 and tup(a.snapshot())==tup(c['A_after']) and ev[0]['pattern']=='RR'
        z=ev[0]['rotations'][0];assert z['pivot']==G
        assert all(G in path(tup(z['before']),x)[:-1] and G not in path(tup(z['after']),x)[:-1] for x in (X,r['y']))
        begin=next(j for j,z in enumerate(fw) if z['target']==G);end=next(j for j in range(2*r['m']+1,len(fw)) if fw[j]['target']==G)
        assert [z['target'] for z in fw[begin+1:end] if G in z['ancestors'] and z['target']>G]==[X,r['y']]
        assert len(path(tup(c['prep_start']),G))-1==c['prep_depth']
        Q=1 if G==2*r['m']-1 else 2
        assert 2*((c['prep_depth']+1)//2)-Q==c['tail_lower']>=1
        claims.append((X,3))
    a=V.Mutable(tup(r['A_contact']));losses={G:[] for G in range(1,2*r['m'],2)}
    for ordinal,row in enumerate(r['controls']):
        assert tup(a.snapshot())==tup(row['before']);h,_,ev=a.splay(row['target'],True)
        assert h==row['H'] and tup(a.snapshot())==tup(row['after'])
        for e in ev:
            for z in e['rotations']:
                for G in losses:
                    if r['y'] in path(tup(z['before']),G)[:-1] and r['y'] not in path(tup(z['after']),G)[:-1]:
                        assert z['pivot']==r['y'];losses[G].append((ordinal,e['j'],z['bit']))
    assert all(v==[(0,1,0)] for v in losses.values()) and len(set(claims))==4 and V.CALLS==22
    paths=[p,F/'UNBOUNDED_SHARED_RETURN_SOURCE_FAMILY.md',F/'audit_USR35.py',F/'SS_SPLAY_INVERSE_SOURCE_THEOREM.md',
      F/'independent_MFR35_unpaid_source_countercut.json',F/'independent_return_countercut_repair.json',B/'STREAMED_BLOCK_THEOREM.md',B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md']
    out={'status':'PASS_USR35_UNIFORM_PROOF_REVIEW_WITH_M4_SOURCE_CONTROL',
      'uniform_scope':'every integer m>=3 in the displayed exact source family; r=3m+2; reflection; arbitrary original Gamma length and repetitions',
      'reviewed_uniform_bridges':['base Bprev inverse LL; G/X free-tree stage recurrence including all D/T subtrees',
        'right-vine contact and low-reset induction; all marked actual grandparent paths; inverse letters visit every odd mark',
        'SSI literal inverse closure and exact M/Q formal identities, not exhaustive coverage of original words',
        'A one-RR formula; unique next-contact B demotions; sole zig return event; all later resets leave y rigid',
        'original prep depth bounds 2 and 2i+1; all m distinct last-tail donors outside natural h0',
        'fixed-owner even selector, full source margin6m+2, static bank2 and both-endpoint legal-period transport',
        'erased/chart recurrence and Gamma remain symbolic existence bridges, all their actual costs retained'],
      'finite_control':{'m':4,'physical_keys':27,'genuine_support':14,'BF_forward_operations_replayed':13,'critical_A_operations_replayed':9,'complete_B_operations_producer_cached':92,'complete_B_Q':158,'selected_unpaid_claims':4,'return_units_relaxed':2,'deficiency':2},
      'not_numerically_replayed':['complete inverse B trajectory in distinct mutable implementation','canonical Gamma words','complete inverse A trajectory','numeric erased/chart recurrence'],
      'arbitrary_active_private_ancestor_lifting':False,'return_only_rule':'UNBOUNDED_DEFICIENCY','CD_counterexample':False,'JR35':'OPEN','reservation':'DEFERRED',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'independent_is_same_agent_distinct_implementation':True,'input_sha256':{str(p):sha(p) for p in paths}}
    with (F/'independent_USR35.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('input_sha256','reviewed_uniform_bridges')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/'audit_verify156_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
