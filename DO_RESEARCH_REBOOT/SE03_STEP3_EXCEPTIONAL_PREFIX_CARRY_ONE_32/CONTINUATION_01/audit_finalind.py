"""Distinct forward-closure verification, not producer path search.
All rows are re-enumerated from the accepted syntax and audited cold/H1
relations. No source compiler, access, splay, private-population sample.
"""
import json,time,collections,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;O=P/'SE03_STEP2_UNARY_A_LIFT_14'
def rd(p):return json.loads(p.read_text())
def freeze(t):return tuple(map(freeze,t)) if isinstance(t,list) else t
def main():
    g=rd(O/'branch_grammar2.json');c=rd(O/'branch_core11_mask0.json');z=rd(B/'threephase2_analysis.json')
    assert z['status']=='COMPLETE_EXCLUSION' and not z['abstract_failures'] and not z['halt']
    A,T,M=g['states'],c['BF_trees'],c['marks'];ai={freeze(t):i for i,t in enumerate(A)}
    roots={r:[a for a,t in enumerate(A) if t[0]==r*1000] for r in range(1,7)};debt={};o=0
    for b,t in enumerate(T):
        for a in roots[M.index(t[0])+1]:debt[a,b]=c['debt'][o];o+=1
    assert o==len(c['debt'])
    labels=[{(v['A'],v['BF']):v['slack'] for v in z[k]} for k in ('old_states','new_states')]
    canon={tuple(v['key']):v['slack'] for v in z['canonical_states']}
    assert len(canon)==52 and len(labels[0])==1167 and len(labels[1])==2853
    cold=rd(B/'cold_source_relation_complete.json');assert cold['status']=='PASS_COMPLETE_SOURCE_UNION_AGREEMENT'
    for n,h in cold['input_sha256'].items():assert hashlib.sha256((B/n).read_bytes()).hexdigest()==h
    cr={h:collections.defaultdict(list) for h in (1,2)}
    for h in (1,2):
        for a,t in cold['LOW'][str(h)]:cr[h][a].append(t)
    h1=rd(B/'cold013_h1_relation.json');h1ind=rd(B/'verify014_h1_relation.json')
    assert h1['status']==h1ind['status']=='COMPLETE_H1_CLOSURE' and h1['H1']==h1ind['H1'] and h1['states']==h1ind['states']
    assert set(h1['completed_A_states'])==set(h1['reached_A_states'])
    A7=h1['states'];R7=collections.defaultdict(list)
    for a,x,t in h1['H1']:
        assert a in h1['completed_A_states'] and A7[t][0]==x*1000
        if x!=4:assert t in h1['completed_A_states']
        R7[a,x].append(t)
    def project(t,keep):
        if t is None:return None
        L,R=project(t[1],keep),project(t[2],keep)
        if t[0] in keep:return (1000*(1+keep.index(t[0])),L,R)
        if L is None or R is None:return L if R is None else R
        return (500+1000*len([v for v in keep if v<t[0]]),L,R)
    A6={}
    for ph,keep in [(0,[1000,2000,3000,4000,6000,7000]),(1,[1000,2000,3000,5000,6000,7000])]:
        for a,t in enumerate(A7):
            if t[0] in keep:A6[ph,a]=ai[project(t,keep)]
    R={h:collections.defaultdict(list) for h in (1,2)}
    for h in (1,2):
        for a,x,t in g['H'+str(h)]:R[h][a,x].append(t)
    adj=collections.defaultdict(list)
    for b,t,x,q in c['BF_relation']:adj[b].append((t,M.index(x)+1,q))
    def find(t,x):
        if isinstance(t,str):return None
        return t if t[0]==x else find(t[1 if x<t[0] else 2],x)
    coldB={}
    for b,t in enumerate(T):
        n=find(t,7)
        if n[1]=='F6' and n[2]=='F7' and t[0]!=7:
            rr=[(u,q+1) for u,x,q in adj[b] if x==4]
            if rr:coldB[b]=rr[0]
    gm=99
    for b,(dest,q) in coldB.items():
        for a in roots[M.index(T[b][0])+1]:
            for h in (1,2):
                for ta in cr[h][a]:gm=min(gm,2*h-q+debt[ta,dest]-debt[a,b])
            for ta in roots[4]:gm=min(gm,6-q+debt[ta,dest]-debt[a,b])
    assert gm==-2 and z['old_cutoff']==4
    counts=collections.Counter()
    def included(ph,a,b,bound,kind):
        counts[kind]+=1
        if bound<=(4 if ph==0 else 2):assert (a,b) in labels[ph] and labels[ph][a,b]<=bound,(kind,ph,a,b,bound)
    def cincluded(ph,a,b,bound):
        counts['canonical_edges']+=1
        if bound<=(4 if ph==0 else 2):assert (ph,a,b) in canon and canon[ph,a,b]<=bound
    def high(ph,a,b,value,dest,price,kind):
        for ta in roots[M.index(T[dest][0])+1]:included(ph,ta,dest,value+price+debt[ta,dest]-debt[a,b],kind)
    # Original entry inclusion.
    for a in h1['initial']:
        rows=[(k,v) for k,v in canon.items() if k[0]==0 and k[1]==a and v==debt[A6[0,a],k[2]]]
        assert rows
    for (ph,a,b),value in canon.items():
        aa=A6[ph,a];ds=debt[aa,b]
        if ph==0 and b in coldB:
            dest,q=coldB[b]
            for ta in R7[a,5]:cincluded(1,ta,dest,value+2-q+debt[A6[1,ta],dest]-ds)
            for ta in cr[2][aa]:included(1,ta,dest,value+4-q+debt[ta,dest]-ds,'canonical_cold_H2')
            for ta in roots[4]:included(1,ta,dest,value+6-q+debt[ta,dest]-ds,'canonical_cold_HIGH')
        for dest,x,q in adj[b]:
            if ph==0 and x==4:continue
            actual=x if x<=3 else x+1
            if q<=4:
                for ta in R7[a,actual]:
                    w=2-q+debt[A6[ph,ta],dest]-ds;assert w>=0;cincluded(ph,ta,dest,value+w)
                for ta in R[2][aa,x]:included(ph,ta,dest,value+4-q+debt[ta,dest]-ds,'canonical_H2')
                high(ph,aa,b,value,dest,6-q,'canonical_HIGH')
            else:
                assert q==5
                for end,y,q1 in adj[dest]:
                    if q1!=1 or y not in (1,6):continue
                    ay=y if y<=3 else y+1
                    for mid7 in R7[a,actual]:
                        for ta7 in R7[mid7,ay]:
                            w=-2+debt[A6[ph,ta7],end]-ds;assert w>=0;cincluded(ph,ta7,end,value+w)
                        for ta in R[2][A6[ph,mid7],y]:included(ph,ta,end,value+debt[ta,end]-ds,'canonical_PAIR_H1_H2')
                    for mid in R[2][aa,x]:
                        for ta in R[1][mid,y]:included(ph,ta,end,value+debt[ta,end]-ds,'canonical_PAIR_H2_H1')
                    high(ph,aa,b,value,end,2,'canonical_HIGH_PAIR')
    for ph,dist in enumerate(labels):
        for (a,b),value in dist.items():
            ds=debt[a,b]
            if ph==0:
                n=find(T[b],7);assert n[1]=='F6' and n[2]=='F7'
                if b in coldB:
                    dest,q=coldB[b]
                    for h in (1,2):
                        for ta in cr[h][a]:included(1,ta,dest,value+2*h-q+debt[ta,dest]-ds,'general_cold_LOW')
                    for ta in roots[4]:included(1,ta,dest,value+6-q+debt[ta,dest]-ds,'general_cold_HIGH')
            for dest,x,q in adj[b]:
                if ph==0 and x==4:continue
                if q<=4:
                    for h in (1,2):
                        for ta in R[h][a,x]:
                            w=2*h-q+debt[ta,dest]-ds;assert w>=0;included(ph,ta,dest,value+w,'general_LOW')
                    high(ph,a,b,value,dest,6-q,'general_HIGH')
                else:
                    for end,y,q1 in adj[dest]:
                        if q1!=1 or y not in (1,6):continue
                        for h,j in ((1,1),(1,2),(2,1)):
                            for mid in R[h][a,x]:
                                for ta in R[j][mid,y]:
                                    w=2*(h+j)-6+debt[ta,end]-ds;assert w>=0;included(ph,ta,end,value+w,'general_PAIR')
                        high(ph,a,b,value,end,2,'general_HIGH_PAIR')
    # Independently recompute full terminal syntax, including nonnegative M.
    def marks(v):
        if v is None:return set()
        return marks(v[1])|marks(v[2])|({v[0]} if v[0]%1000==0 else set())
    def hidden7depth(t,lo=0,hi=7000,d=0):
        if not lo<3500<hi:return 99
        if t is None:return d
        mm=marks(t);here=d if t[0]==3500 or max(mm)<3500 or min(mm)>3500 else 99
        return min(here,hidden7depth(t[1],lo,t[0],d+1),hidden7depth(t[2],t[0],hi,d+1))
    depths=[hidden7depth(t) for t in A];minimum=99;terminal_checks=0;canonical_checks=0
    for b,t in enumerate(T):
        if find(t,7)[1]!='F6' or not any(x==4 for _,x,_ in adj[b]):continue
        children={m:[] for m in M};pa={}
        def walk(v,p):
            if isinstance(v,str):return
            if v[0] in children:
                pa[v[0]]=p
                if p is not None:children[p].append(v[0])
                p=v[0]
            walk(v[1],p);walk(v[2],p)
        walk(t,None)
        E=sum(not v for v in children.values())-sum(len(v)>=2 for v in children.values())-1
        k=0;p=pa[7]
        while p is not None:k+=int(len(children[p])>=3);p=pa[p]
        for a in roots[M.index(t[0])+1]:
            h=min(3,(depths[a]+1)//2);margin=2*h-2+E-k-debt[a,b];minimum=min(minimum,margin);terminal_checks+=1
            if (a,b) in labels[1]:assert labels[1][a,b]+margin>=0
        for (ph,a,bb),value in canon.items():
            if ph!=1 or bb!=b:continue
            v=A7[a];d=0
            while v[0]!=4000:v=v[1 if 4000<v[0] else 2];d+=1
            h=min(3,(d+1)//2);assert h>=1
            margin=2*h-2+E-k-debt[A6[1,a],b];assert value+margin>=0;canonical_checks+=1
    assert minimum==-3
    result={'status':'PASS_COMPLETE_FR32_CARRY_ONE_STATIC_CERTIFICATE','canonical_states':len(canon),'old_general_states':len(labels[0]),'new_general_states':len(labels[1]),
        'minimum_cold_gamma':gm,'minimum_terminal_margin':minimum,'terminal_syntax_checked':terminal_checks,'canonical_terminals_checked':canonical_checks,
        'inclusion_checks':dict(counts),'new_source_queries':0,'trust':'distinct forward closure and terminal arithmetic; same research agent; symbolic source lifting required; no external or kernel verification',
        'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('threephase2_analysis.json','cold_source_relation_complete.json','cold013_h1_relation.json','verify014_h1_relation.json')}}
    with (B/'FR32_COMPLETE_INDEPENDENT_AUDIT.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_finalind_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
