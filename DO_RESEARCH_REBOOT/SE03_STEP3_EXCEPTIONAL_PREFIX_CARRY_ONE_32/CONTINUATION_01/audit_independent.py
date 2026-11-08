"""Distinct static CERTIFICATE verifier, not another producer shortest path.
Checks every bounded-cost outgoing old packet edge, canonical departure
inclusion and a separately recomputed terminal predicate. No source query,
splay, source-frame compiler or abstract-path realization is performed.
"""
import json,time,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;OLD=P/'SE03_STEP2_UNARY_A_LIFT_14'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    g=read(OLD/'branch_grammar2.json');c=read(OLD/'branch_core11_mask0.json');z=read(B/'canonical_exit_bounded_slack.json')
    assert z['status']=='COMPLETE_BOUNDED_SLACK_TERMINAL_EXCLUSION' and z['abstract_failure_count']==0
    A=g['states'];T=c['BF_trees'];M=c['marks'];roots={r:[a for a,t in enumerate(A) if t[0]==r*1000] for r in range(1,7)}
    debt={};o=0
    for b,t in enumerate(T):
        for a in roots[M.index(t[0])+1]:debt[(a,b)]=c['debt'][o];o+=1
    assert o==len(c['debt'])
    dist={(v['A'],v['BF']):v['minimum_slack'] for v in z['reached_states']};assert len(dist)==1528
    R={h:collections.defaultdict(list) for h in (1,2)}
    for h in (1,2):
        for a,x,t in g['H'+str(h)]:R[h][(a,x)].append(t)
    adj=collections.defaultdict(list)
    for s,t,key,q in c['BF_relation']:adj[s].append((t,M.index(key)+1,q))
    checks=0
    def included(a,b,limit):
        nonlocal checks
        checks+=1
        if limit<=2:assert (a,b) in dist and dist[(a,b)]<=limit,(a,b,limit)
    def high_included(a,b,base,price,dest):
        ds=debt[(a,b)]
        for ta in roots[M.index(T[dest][0])+1]:
            w=price+debt[(ta,dest)]-ds;assert w>=0
            if base+w<=2:included(ta,dest,base+w)
    # Check the actual FORWARD-CLOSED certificate, not inferred shortest
    # paths or finite source examples. Both H1 and H2 rows are retained.
    for (a,b),value in dist.items():
        ds=debt[(a,b)]
        for dest,x,q in adj[b]:
            if q<=4:
                for h in (1,2):
                    for ta in R[h][(a,x)]:
                        w=2*h-q+debt[(ta,dest)]-ds;assert w>=0
                        if value+w<=2:included(ta,dest,value+w)
                high_included(a,b,value,6-q,dest)
            else:
                assert q==5
                for end,y,q1 in adj[dest]:
                    if q1!=1 or y not in (1,6):continue
                    for h1,h2 in ((1,1),(1,2),(2,1)):
                        for mid in R[h1][(a,x)]:
                            for ta in R[h2][(mid,y)]:
                                w=2*(h1+h2)-6+debt[(ta,end)]-ds;assert w>=0
                                if value+w<=2:included(ta,end,value+w)
                    high_included(a,b,value,2,end)
    # Independently check all canonical-phase and departure inclusions.
    canon=z['canonical_source_states'];assert len(canon)==21
    def find(t,key):
        if t is None:return None
        if t[0]==key:return t
        return find(t[1],key) or find(t[2],key)
    sig=lambda a:json.dumps(find(A[a],3000)[1],separators=(',',':'))
    groups=collections.defaultdict(dict)
    for v in canon:
        assert debt[(v['A'],v['BF'])]==v['D'];groups[sig(v['A'])][v['name']]=v
    assert len(groups)==3 and all(set(v)==set('ABCDEFG') for v in groups.values())
    edges=read(B.parent/'upper_seven_form_arithmetic.json')['source_derived_edges']
    for group in groups.values():
        first=group['A'];assert first['minimum_slack']==first['D']-1
        for s,t,key,q,original_sigma in edges:
            ss,tt=group[s],group[t];x=M.index({9:7,11:9,13:11}[key])+1
            assert (tt['BF'],x,q) in adj[ss['BF']]
            assert tt['A'] in R[1][(ss['A'],x)]
            w=2-q+tt['D']-ss['D'];assert w>=0 and tt['minimum_slack']<=ss['minimum_slack']+w
        for v in group.values():
            a,b=v['A'],v['BF'];base=v['minimum_slack'];ds=v['D']
            if base>2:continue
            root=T[b][0]
            for dest,x,q in adj[b]:
                lower=x<=3
                hmin=(1 if x==3 else 2) if root==7 else 2 if root==9 else (2 if x==3 else 3)
                if q<=4:
                    for h in (1,2):
                        if h==1 and not lower:continue
                        if lower and h<hmin:continue
                        for ta in R[h][(a,x)]:
                            w=2*h-q+debt[(ta,dest)]-ds;assert w>=0
                            if base+w<=2:included(ta,dest,base+w)
                    high_included(a,b,base,6-q,dest)
                else:
                    assert lower and x==1 and hmin==3
                    for end,y,q1 in adj[dest]:
                        if q1==1 and y in (1,6):high_included(a,b,base,2,end)
    # Recompute the necessary A-gap predicate by interval recursion over
    # saved ASTs, not an actual private7 source search or tree operation.
    def marked_set(t):
        if t is None:return set()
        return marked_set(t[1])|marked_set(t[2])|({t[0]} if t[0]%1000==0 else set())
    def lower_depth(t,lo=0,hi=7000,d=0):
        if not lo<3500<hi:return 99
        if t is None:return d
        mm=marked_set(t)
        here=d if t[0]==3500 or max(mm)<3500 or min(mm)>3500 else 99
        return min(here,lower_depth(t[1],lo,t[0],d+1),lower_depth(t[2],t[0],hi,d+1))
    depth=[lower_depth(t) for t in A];adverse=0;terminal_checks=0
    cached9={b:(t,q) for b,t,key,q in c['BF_relation'] if key==7}
    for b,t in enumerate(T):
        nodes={};children={m:[] for m in M};pa={}
        def walk(v,p):
            if isinstance(v,str):return
            nodes[v[0]]=v
            if v[0] in children:
                pa[v[0]]=p
                if p is not None:children[p].append(v[0])
                p=v[0]
            walk(v[1],p);walk(v[2],p)
        walk(t,None)
        if nodes[7][1]!='F6' or b not in cached9:continue
        E=sum(not v for v in children.values())-sum(len(v)>=2 for v in children.values())-1
        k=0;p=pa[7]
        while p is not None:k+=int(len(children[p])>=3);p=pa[p]
        for a in roots[M.index(t[0])+1]:
            lb=min(3,(depth[a]+1)//2);margin=2*lb-2+E-k-debt[(a,b)];terminal_checks+=1
            if margin<0:
                adverse+=1
                assert margin>=-3
                if (a,b) in dist:assert dist[(a,b)]+margin>=0,(a,b,dist[(a,b)],margin)
    assert adverse==1493
    out('immediate_branch_independent_audit.json',{'status':'PASS_COMPLETE_IMMEDIATE_BRANCH_STATIC_CERTIFICATE','new_source_queries':0,
        'closure_states':len(dist),'slack_counts':dict(collections.Counter(dist.values())),'canonical_states':21,
        'inclusion_checks':checks,'terminal_syntax_states_checked':terminal_checks,'adverse_terminal_tuples':adverse,
        'principal_immediate_H1_activation_result':'D_out<=1 for every actual continuation through first7',
        'source_induction_kernel_or_external_audit':False,'trust':'distinct static verifier, same research agent; old complete source grammar reused',
        'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('canonical_exit_bounded_slack.json','IMMEDIATE_ACTIVATION_THEOREM.md')}})
    print(json.dumps({'status':'IMMEDIATE_BRANCH_INDEPENDENT_PASS','closure':len(dist),'adverse_checked':adverse,'queries':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
