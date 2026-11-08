"""Original-source family refuting cost-nonincreasing unary A projection.
All source operations are literal and both A/B trees close. No native
potential, CD or universal donor assertion is inferred.
"""
import json,time,sys,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    sp=importlib.util.spec_from_file_location('source_unary_projection33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('SOURCE_RESERVE')
        queries+=1;return p0(t,x)
    S.path=path
    n=10;T=S.vine(n);T=(1,'F0',(2,'F1',(4,(3,'F2','F3'),S.vine(4)))) if False else T
    # The one anonymous key3 begins as a rigid mark-free gap leaf below4.
    tail='F10'
    for k in range(10,4,-1):tail=(k,'F'+str(k-1),tail)
    T=(1,'F0',(2,'F1',(4,(3,'F2','F3'),tail)))
    marks=[1,2]+list(range(4,11));gadget=[('D',4),('D',3),('D',1),('K',4),('K',1),('D',2),('D',1),('D',5),('D',2),('D',1)]
    tour=[('K',x) for x in marks[1:]+list(reversed(marks[:-1]))];word=gadget+tour;a=b=T;rows=[]
    for t,(mode,x) in enumerate(word,1):
        before=(a,b);a,pa,ea=S.trace(a,x);pb='';eb=[]
        if mode=='K':b,pb,eb=S.trace(b,x)
        rows.append({'occurrence':t,'mode':mode,'target':x,'before':before,'after':(a,b),'A_path':pa,'BF_path':pb,'A_events':ea,'BF_events':eb,'a':len(ea),'qF':len(pb)//2,'genuine_F':mode=='K' and before[1][0]!=x})
        if t==3:assert a==S.vine(10)
        if t==7:assert a==S.vine(10)
        if t==10:assert a==b==T
    assert a==b==T and len(word)==26 and {r['target'] for r in rows if r['genuine_F']}==set(marks)
    core=S.core(T,set(marks));assert S.labels(core)==set(marks)
    def projection(t):
        if isinstance(t,str):return None
        k,l,r=t;l=projection(l);r=projection(r)
        if k==3:assert l is None or r is None;return l if r is None else r
        return (k,l,r)
    r=rows[3];projected_before=projection(r['before'][0]);projected_after=projection(r['after'][0]);assert r['a']==2
    def normalize(t,lo=1,hi=9):
        if t is None:return 'F'+str(hi)
        k,l,r=t;k=marks.index(k)+1
        return (k,normalize(l,lo,k-1),normalize(r,k+1,hi))
    initial=normalize(projected_before);target=normalize(projected_after);assert initial==S.vine(9) and target[0]==3 and target[1][0]==1 and target[1][2][0]==2
    # Exact native reachability at cost<=2 uses the saved ordinary actions;
    # no new original splay/query is called for this symbolic classification.
    def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
    cache=json.loads((B/'nine_label_native_action_cache.json').read_text());idx={fr(t):i for i,t in enumerate(cache['trees'])};src=idx[initial];dst=idx[target];best={src:0};queue=[src]
    while queue:
        v=queue.pop()
        for x in range(9):
            w=cache['H'][v][x];d=best[v]+w;t=cache['destination'][v][x]
            if d<=2 and d<best.get(t,999):best[t]=d;queue.append(t)
    assert dst not in best
    v=src;cost=0
    for x in (4,3):cost+=cache['H'][v][x-1];v=cache['destination'][v][x-1]
    assert v==dst and cost==3
    result={'status':'SOURCE_EXACT_COST_NONINCREASING_UNARY_PROJECTION_REFUTED','initial_diagonal':T,'word':word,'rows':rows,'marks':marks,'anonymous_key':3,'critical_occurrence':4,'critical_original_A_events':2,'projected_A_before':initial,'projected_A_after':target,'native_minimum_A_events':3,'native_three_event_word_normalized':[4,3],'counts':{'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows)},'paired_closed':True,'full_core_size':9,'source_queries':queries,'principal_U33':'OPEN','refuted_bridge':'projection of an active anonymous unary A ancestor can always be reproduced by Score accesses with no more A events','actual_CD_refutation':False}
    out('unary_projection_source_countercertificate.json',result);print(json.dumps({k:result[k] for k in ('status','critical_original_A_events','native_minimum_A_events','counts','source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core5_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
