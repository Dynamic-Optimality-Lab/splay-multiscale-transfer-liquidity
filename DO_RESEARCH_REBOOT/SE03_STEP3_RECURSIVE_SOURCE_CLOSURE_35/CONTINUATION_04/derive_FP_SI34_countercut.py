"""Use the established SI34 closed source; annotate its new FP tags."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';S=C/'CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def path(t,x):
    z=[]
    while True:
        z.append(t[0])
        if t[0]==x:return z
        t=t[1] if x<t[0] else t[2]
def core(t,marks):return set().union(*(set(path(t,x)) for x in marks))
def main():
    global V
    accepted=json.loads((S/'independent_symbolic_source_audit.json').read_text())
    for p,h in accepted['input_sha256'].items():assert sha(S/p)==h
    cert=json.loads((S/'SI34_source_countercertificate.json').read_text())
    word=[15]+[v for x in range(3,14,2) for v in (1,x)]+[v for x in range(11,2,-2) for v in (1,x)]+[1]
    assert len(word)==24 and cert['source']['genuine_full_keys']==list(range(1,16,2))
    sp=importlib.util.spec_from_file_location('new_SI34_tag_B_source',B/'audit_core39.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    initial=tup(cert['source']['initial_full_B']);BF=initial;rows=[]
    for i,x in enumerate(word):
        before=BF;BF,_,q,events=V.splay(BF,x,True)
        rows.append({'KEEP_ordinal':i+1,'target':x,'before':before,'after':BF,'Q':q,'events':events})
    assert BF==initial and sum(r['Q'] for r in rows)==46
    reports=[];graph={};N=len(rows)
    for i,x in ((2,5),(4,9),(6,13)):
        e=2*i;assert word[e]==x
        prev=next((e-d)%N for d in range(1,N+1) if word[(e-d)%N]==x)
        marks={x};current={x};tags={}
        for offset in range(1,(e-prev)%N):
            j=(prev+offset)%N;r=rows[j];y=r['target'];assert core(r['before'],marks)==current
            first=y not in marks
            after=core(r['after'],marks|{y});growth=after-current
            if first:
                assert len(growth)<=2
                for z in growth:tags.setdefault(z,{'proxy':y,'birth_KEEP_ordinal':j+1})
            else:assert not growth
            marks.add(y);current=after
        pp=path(rows[e]['before'],x);assert len(pp)==7 and rows[e]['Q']==3
        forced=[];demand_data=[];own={(f'v{x}',1,b) for b in (0,1)}
        for k in range(1,4):
            operands=pp[-2*k-1:-2*k+1];tt=[tags[z] for z in operands];keys={a['proxy'] for a in tt}
            assert len(keys)==1;y=next(iter(keys));forced.append(y)
            pool=own|({('c',1,b) for b in (0,1)} if y==15 else set())
            d=(f'v{x}',k);graph[d]=pool
            demand_data.append({'demand':d,'original_B_operands':operands,'source_tags':tt,'forced_proxy':y,
              'first_loss_and_own_units':sorted(pool)})
        assert forced==[15,x-2,1]
        reports.append({'target':x,'KEEP_ordinal':e+1,'H':1,'Q':3,'forced_proxies_bottom_up':forced,'demands':demand_data})
    neighborhood=set().union(*graph.values());assert len(graph)==9 and len(neighborhood)==8
    r={'status':'FP_FIRST_LOSS_PLUS_OWN_REFUTED_ON_ESTABLISHED_SI34_SOURCE',
      'mathematical_source_scope':'original reachable eight-genuine-key closed SI34 construction, all canonical Gamma costs retained',
      'B_rows':rows,'new_FP_tag_annotations':reports,
      'exact_cut':{'demands':sorted(graph),'neighborhood':sorted(neighborhood),'deficiency':1},
      'absolute_identifiers':{'c':'b+2','v_(2i+1)':'b+ell+2+2i; i=2,4,6','ell':'actual length of canonical original Gamma_low'},
      'closure':'reused independent symbolic source proof, not newly expanded Gamma/BE replay',
      'A_first_loss_exhaustion':'reused EXACT_NEGATIVE_CUT: proxy15 only c; proxy1 and x-2 only v_x',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'JR35':'OPEN','Coarse_Double_counterexample':False,
      'claim_limit':'refutes this exact proxy/first-loss+own eligibility rule, even before frozen-owner constraints; FP existence lemmas remain valid',
      'input_sha256':{str(p):sha(p) for p in (S/'SI34_source_countercertificate.json',S/'independent_symbolic_source_audit.json',
        S/'independent_critical_source_audit.json',S/'SOURCE_CONSTRUCTION.md',S/'EXACT_NEGATIVE_CUT.md',
        S/'SYMBOLIC_B_CLOSURE.md',F/'FRESH_PROXY_LOSS_THEOREM.md')}}
    with (F/'FP_SI34_source_countercut.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k not in ('B_rows','new_FP_tag_annotations','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_core49_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
