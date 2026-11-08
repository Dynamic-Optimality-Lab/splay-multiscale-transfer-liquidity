"""One cold seam, complete cached packet arithmetic. No source queries.
An abstract path here is NEVER asserted to be an original source witness.
"""
import json,time,sys,collections,heapq
from array import array
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;O=P/'SE03_STEP2_UNARY_A_LIFT_14'
START=time.process_time();CAP=float(sys.argv[1])
def read(p):return json.loads(p.read_text())
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    g=read(O/'branch_grammar2.json');c=read(O/'branch_core11_mask0.json');cold=read(B/'cold_source_relation_complete.json')
    A=g['states'];T=c['BF_trees'];M=c['marks'];D=bytes(c['debt']);ai={fr(t):i for i,t in enumerate(A)};bi={fr(t):i for i,t in enumerate(T)}
    roots={r:[i for i,t in enumerate(A) if t[0]==r*1000] for r in range(1,7)};pos={a:i for rr in roots.values() for i,a in enumerate(rr)}
    off=[];na=array('H');nb=array('H');buckets=[]
    for b,t in enumerate(T):
        off.append(len(na));bb=[[] for _ in range(4)]
        for a in roots[M.index(t[0])+1]:bb[D[len(na)]].append(len(na));na.append(a);nb.append(b)
        buckets.append(bb)
    def sid(b,a):return off[b]+pos[a]
    N=len(D);assert len(na)==N
    lowA=[collections.defaultdict(dict) for _ in A]
    for h in (1,2):
        for a,x,t in g['H'+str(h)]:lowA[a][x][t]=min(h,lowA[a][x].get(t,99))
    adj=[[] for _ in T]
    for b,t,key,q in c['BF_relation']:adj[b].append((t,M.index(key)+1,q))
    low=[[] for _ in T];high=[[] for _ in T]
    for b,rr in enumerate(adj):
        for t,x,q in rr:
            if q<=4:low[b].append((t,x,q,None));high[b].append((t,6-q,[x]))
            else:
                assert q==5
                for dest,y,q1 in adj[t]:
                    if q1==1 and y in (1,6):low[b].append((dest,x,6,y));high[b].append((dest,2,[x,y]))
    paircache={};checks=0
    def lowedges(s,old=False):
        a,b=na[s],nb[s]
        for dest,x,q,y in low[b]:
            if old and (x==4 or y==4):continue
            if y is None:rel=((ta,h,None,None,None) for ta,h in lowA[a].get(x,{}).items())
            else:
                k=(a,x,y)
                if k not in paircache:
                    zz={}
                    for mid,h1 in lowA[a].get(x,{}).items():
                        for ta,h2 in lowA[mid].get(y,{}).items():
                            if h1+h2<=3 and (ta not in zz or h1+h2<zz[ta][0]):zz[ta]=(h1+h2,mid,h1,h2)
                    paircache[k]=zz
                rel=((ta,h,mid,h1,h2) for ta,(h,mid,h1,h2) in paircache[k].items())
            for ta,h,mid,h1,h2 in rel:
                t=sid(dest,ta);w=2*h-q+D[t]-D[s];assert w>=0
                yield t,w,{'kind':'LOW','targets':[x] if y is None else [x,y],'H':[h] if y is None else [h1,h2],'mid':mid,'Q':q}
    leaf7=[];coldBF={}
    def node(t,x):
        if isinstance(t,str):return None
        return t if t[0]==x else node(t[1 if x<t[0] else 2],x)
    for b,t in enumerate(T):
        n=node(t,7);leaf7.append(n[1]=='F6' and n[2]=='F7')
        if leaf7[-1] and t[0]!=7:
            rr=[(dest,q+1) for dest,x,q in adj[b] if x==4]
            if rr:coldBF[b]=rr[0]
    cr=[[] for _ in A]
    for h in (1,2):
        for a,t in cold['LOW'][str(h)]:cr[a].append((t,h))
    gm=99
    for b,(dest,q) in coldBF.items():
        for a in roots[M.index(T[b][0])+1]:
            s=sid(b,a)
            for ta,h in cr[a]:gm=min(gm,2*h-q+D[sid(dest,ta)]-D[s])
            gm=min(gm,6-q+min(D[sid(dest,ta)] for ta in roots[4])-D[s])
    cutoff=2-gm;assert cutoff<20
    lower=(4,(3,(2,(1,'F0','F1'),'F2'),'F3'),'F4')
    F0=(9,(8,(5,lower,(6,'F5',(7,'F6','F7'))),'F8'),(10,'F9',(11,'F10','F11')))
    olddist=array('h',[999])*N;newdist=array('h',[999])*N;parent={};pq=[];seeds=[]
    for small in [(1500,(1000,None,None),(2000,None,None)),(1000,None,(2000,None,None)),(2000,(1000,None,None),None)]:
        a=ai[(5000,(4000,(3000,small,None),None),(6000,None,None))];s=sid(bi[F0],a)
        seeds.append(s)
    def add(dist,heap,t,v,prev,act,phase,limit):
        nonlocal checks
        checks+=1
        if v<=limit and v<dist[t]:dist[t]=v;heapq.heappush(heap,(v,t));parent[(phase,t)]=(prev,act)
    coldqueue=[];processed=[0,0];reason=None
    hh=read(B/'cold013_h1_relation.json');ii=read(B/'verify014_h1_relation.json')
    assert hh['status']==ii['status']=='COMPLETE_H1_CLOSURE' and hh['H1']==ii['H1'] and hh['states']==ii['states']
    A7=hh['states'];r7=collections.defaultdict(list)
    for a,x,t in hh['H1']:r7[a,x].append(t)
    def proj(v,marks):
        if v is None:return None
        l,r=proj(v[1],marks),proj(v[2],marks)
        if v[0] in marks:return (1000*(marks.index(v[0])+1),l,r)
        if l is None:return r
        if r is None:return l
        return (500+1000*sum(m<v[0] for m in marks),l,r)
    a6={ph:[None if v[0]==(5000 if ph==0 else 4000) else ai[proj(v,([1000,2000,3000,4000,6000,7000] if ph==0 else [1000,2000,3000,5000,6000,7000]))] for v in A7] for ph in (0,1)}
    can={};cq=[];cp={};can_terminal=[];departures=[]
    def cadd(key,value,prev,act):
        ph,a,b=key
        if value<can.get(key,999) and value<=(cutoff if ph==0 else 2):can[key]=value;heapq.heappush(cq,(value,key));cp[key]=(prev,act)
    for a in hh['initial']:
        b=bi[F0];s=sid(b,a6[0][a]);cadd((0,a,b),D[s],None,{'kind':'INITIAL'})
    def depart(ph,t,value,key,act):
        departures.append({'phase':ph,'A':na[t],'BF':nb[t],'slack':value,'canonical_source':list(key),'action':act})
        add(newdist if ph else olddist,coldqueue if ph else pq,t,value,('CAN',key),act,ph,2 if ph else cutoff)
    # Exact H1 phase from the original entry, through the one cold switch.
    # Only after the FIRST H>=2 macro is the physical7/9 location forgotten.
    while cq:
        value,key=heapq.heappop(cq)
        if can[key]!=value:continue
        ph,a,b=key;aold=a6[ph][a];s=sid(b,aold);ds=D[s]
        if ph==0 and b in coldBF:
            dest,q=coldBF[b]
            for ta in r7[a,5]:
                t=sid(dest,a6[1][ta]);w=2-q+D[t]-ds;cadd((1,ta,dest),value+w,key,{'kind':'H1_COLD','Q':q,'margin':w})
            for ta,h in cr[aold]:
                if h!=2:continue
                t=sid(dest,ta);w=4-q+D[t]-ds;depart(1,t,value+w,key,{'kind':'FIRST_H2_COLD','Q':q,'gamma':w})
            for ta in roots[4]:
                t=sid(dest,ta);w=6-q+D[t]-ds;depart(1,t,value+w,key,{'kind':'FIRST_HIGH_COLD','Q':q,'gamma':w})
        for dest,x,q in adj[b]:
            if ph==0 and x==4:continue
            actual=x if x<=3 else (x+1 if ph==0 else x+1)
            # Both charts' ranks5/6 map to original six/seven; new rank4 maps5.
            if ph==0 and x==4:raise AssertionError()
            if q<=4:
                for ta in r7[a,actual]:
                    t=sid(dest,a6[ph][ta]);w=2-q+D[t]-ds;assert w>=0
                    cadd((ph,ta,dest),value+w,key,{'kind':'H1_FIXED','target':actual,'Q':q,'margin':w})
                for ta,h in lowA[aold].get(x,{}).items():
                    # A row also present in H1 must retain its H2 realization.
                    pass
                for aa,x2,ta in []:pass
                for aa,x2,ta in g['H2']:
                    if aa!=aold or x2!=x:continue
                    t=sid(dest,ta);w=4-q+D[t]-ds;depart(ph,t,value+w,key,{'kind':'FIRST_H2_FIXED','target':actual,'Q':q,'margin':w})
                for ta in roots[M.index(T[dest][0])+1]:
                    t=sid(dest,ta);w=6-q+D[t]-ds;depart(ph,t,value+w,key,{'kind':'FIRST_HIGH_FIXED','target':actual,'Q':q,'margin':w})
            else:
                assert q==5
                for end,y,q1 in adj[dest]:
                    if q1!=1 or y not in (1,6):continue
                    ay=y if y<=3 else y+1
                    for mid7 in r7[a,actual]:
                        for ta7 in r7[mid7,ay]:
                            t=sid(end,a6[ph][ta7]);w=-2+D[t]-ds;assert w>=0
                            cadd((ph,ta7,end),value+w,key,{'kind':'H1_PAIR','targets':[actual,ay],'margin':w})
                        for aa,x2,ta in g['H2']:
                            if aa==a6[ph][mid7] and x2==y:
                                t=sid(end,ta);w=D[t]-ds;depart(ph,t,value+w,key,{'kind':'FIRST_H2_PAIR_SECOND','targets':[actual,ay],'margin':w})
                    # First H2 macro followed by one-event successor.
                    for aa,x2,mid in g['H2']:
                        if aa!=aold or x2!=x:continue
                        for ta,h in lowA[mid].get(y,{}).items():
                            if h!=1:continue
                            t=sid(end,ta);w=D[t]-ds;depart(ph,t,value+w,key,{'kind':'FIRST_H2_PAIR_FIRST','targets':[actual,ay],'margin':w})
                    for ta in roots[M.index(T[end][0])+1]:
                        t=sid(end,ta);w=2+D[t]-ds;depart(ph,t,value+w,key,{'kind':'FIRST_HIGH_PAIR','targets':[actual,ay],'margin':w})
    for ph,dist,heap,limit in [(0,olddist,pq,cutoff),(1,newdist,coldqueue,2)]:
        highdone=set();colddone=set()
        while heap:
            value,s=heapq.heappop(heap)
            if value!=dist[s]:continue
            a,b=na[s],nb[s];ds=D[s];processed[ph]+=1
            if ph==0:
                assert leaf7[b]
                if b in coldBF:
                    dest,q=coldBF[b]
                    for ta,h in cr[a]:
                        t=sid(dest,ta);w=2*h-q+D[t]-ds
                        add(newdist,coldqueue,t,value+w,(0,s),{'kind':'COLD_LOW','H':h,'Q':q,'gamma':w},1,2)
                    if (b,ds) not in colddone:
                        colddone.add((b,ds))
                        for ta in roots[4]:
                            t=sid(dest,ta);w=6-q+D[t]-ds
                            add(newdist,coldqueue,t,value+w,(0,s),{'kind':'COLD_HIGH','Q':q,'gamma':w},1,2)
            for t,w,act in lowedges(s,ph==0):
                if ph==0:assert leaf7[nb[t]]
                add(dist,heap,t,value+w,(ph,s),act,ph,limit)
            if (b,ds) not in highdone:
                highdone.add((b,ds))
                for dest,price,targets in high[b]:
                    if ph==0 and 4 in targets:continue
                    for dt,rr in enumerate(buckets[dest]):
                        w=price+dt-ds;assert w>=0 or not rr
                        if value+w<=limit:
                            for t in rr:
                                if ph==0:assert leaf7[nb[t]]
                                add(dist,heap,t,value+w,(ph,s),{'kind':'HIGH','targets':targets,'price':price},ph,limit)
            if processed[ph]%64==0 and (checks>4800000 or time.process_time()-START>CAP-2):reason='EDGE_OR_CPU_RESERVE';break
        if reason:break
    # Full terminal arithmetic, including nonnegative margins when the cold entry is negative.
    def ml(t):
        if t is None:return set()
        return ml(t[1])|ml(t[2])|({t[0]} if t[0]%1000==0 else set())
    def lb(t,d=0):
        if t is None:return d
        mm=ml(t)
        if t[0]==3500 or max(mm)<3500 or min(mm)>3500:return d
        return lb(t[1 if 3500<t[0] else 2],d+1)
    depth=[lb(t) for t in A];fail=[];minR=999;terminal=0
    for b,t in enumerate(T):
        if node(t,7)[1]!='F6' or not any(x==4 for _,x,_ in adj[b]):continue
        deg={x:0 for x in M};pa={}
        def walk(v,p):
            if isinstance(v,str):return
            if v[0] in deg:
                if p is not None:deg[p]+=1
                pa[v[0]]=p;p=v[0]
            walk(v[1],p);walk(v[2],p)
        walk(t,None);E=sum(max(x-2,0) for x in deg.values());k=0;p=pa[7]
        while p is not None:k+=int(deg[p]>=3);p=pa[p]
        for a in roots[M.index(t[0])+1]:
            s=sid(b,a);h=min(3,(depth[a]+1)//2);margin=2*h-2+E-k-D[s];assert margin>=-3;terminal+=1
            if newdist[s]!=999:
                rr=newdist[s]+margin;minR=min(minR,rr)
                if rr<0:fail.append({'sid':s,'A':a,'BF':b,'slack':newdist[s],'margin':margin,'H_return_lb':h,'R_lower_bound':rr})
    # Canonical states can terminate before their first H2 nonreturn macro.
    # Use ACTUAL seven-key quotient depth, not a freely placed hidden7.
    for key,value in can.items():
        ph,a,b=key
        if ph==0:continue # FR32-N9 handles all preactivation returns
        if node(T[b],7)[1]!='F6' or not any(x==4 for _,x,_ in adj[b]):continue
        deg={x:0 for x in M};pa={}
        def walk2(v,p):
            if isinstance(v,str):return
            if v[0] in deg:
                if p is not None:deg[p]+=1
                pa[v[0]]=p;p=v[0]
            walk2(v[1],p);walk2(v[2],p)
        walk2(T[b],None);E=sum(max(z-2,0) for z in deg.values());k=0;p=pa[7]
        while p is not None:k+=int(deg[p]>=3);p=pa[p]
        v=A7[a];dd=0
        while v[0]!=4000:v=v[1 if 4000<v[0] else 2];dd+=1
        h=max(1,min(3,(dd+1)//2));ss=sid(b,a6[1][a]);margin=2*h-2+E-k-D[ss]
        rr=value+margin;can_terminal.append({'key':key,'slack':value,'H_lb':h,'margin':margin,'R':rr})
        if rr<0:fail.append({'canonical_key':key,'slack':value,'margin':margin,'R_lower_bound':rr})
        minR=min(minR,rr)
    path=[]
    if fail:
        z=min(fail,key=lambda z:(z['R_lower_bound'],z['slack']));p=('CAN',z['canonical_key']) if 'canonical_key' in z else (1,z['sid'])
        while p[0]!='CAN' and p in parent:
            old,act=parent[p];path.append({'phase':p[0],'A':na[p[1]],'BF':nb[p[1]],'slack':(newdist if p[0] else olddist)[p[1]],'action':act});p=old
        if p[0]=='CAN':
            key=p[1]
            while key is not None:
                prev,act=cp[key];ph,a,b=key;path.append({'phase':'CAN'+str(ph),'A7':a,'A6':a6[ph][a],'BF':b,'slack':can[key],'action':act});key=prev
        path.reverse()
    result={'status':'PARTIAL' if reason else 'ABSTRACT_FAILURE' if fail else 'COMPLETE_EXCLUSION','halt':reason,'minimum_cold_gamma':gm,'old_cutoff':cutoff,
        'processed':processed,'edge_checks':checks,'terminal_checks':terminal,'minimum_terminal_bound':minR,'abstract_failures':fail,'abstract_path':path,
        'path_is_source_counterexample':False,'new_source_queries':0,
        'canonical_states':[{'key':key,'slack':v} for key,v in sorted(can.items())],'canonical_terminals':can_terminal,'departures':departures,
        'old_states':[{'A':na[s],'BF':nb[s],'slack':olddist[s]} for s in range(N) if olddist[s]!=999],
        'new_states':[{'A':na[s],'BF':nb[s],'slack':newdist[s]} for s in range(N) if newdist[s]!=999]}
    out('threephase2_analysis.json',result);print(json.dumps({k:result[k] for k in ('status','minimum_cold_gamma','old_cutoff','processed','edge_checks','minimum_terminal_bound')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_threephase2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
