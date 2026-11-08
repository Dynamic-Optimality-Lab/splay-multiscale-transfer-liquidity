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
    precise=read(B/'cold012_source_relation.json');ind=read(B/'verify013_source_relation.json')
    assert precise['LOW']==ind['LOW'] and precise['status']==ind['status']=='COMPLETE_BATCH'
    # Immediate H1 cold is already proved by IMMEDIATE_ACTIVATION_THEOREM.
    # Exact source entry frame for immediate H2, conservative HIGH endpoints.
    initcr=collections.defaultdict(list)
    for a,t in precise['LOW']['2']:initcr[a].append(t)
    for s in seeds:
        a,b=na[s],nb[s];value=D[s];dest,q=coldBF[b]
        for ta in initcr[a]:
            t=sid(dest,ta);w=4-q+D[t]-D[s]
            add(newdist,coldqueue,t,value+w,(-1,s),{'kind':'INITIAL_COLD_H2','Q':q,'gamma':w},1,2)
        for ta in roots[4]:
            t=sid(dest,ta);w=6-q+D[t]-D[s]
            add(newdist,coldqueue,t,value+w,(-1,s),{'kind':'INITIAL_COLD_HIGH','Q':q,'gamma':w},1,2)
        for t,w,act in lowedges(s,True):
            # At frozen u11, depths1/3>=3: their first whole macros H>=2.
            if len(act['targets'])==1 and act['targets'][0] in (1,2) and act['H']==[1]:continue
            if len(act['targets'])==2 and act['targets'][0] in (1,2) and act['H'][0]==1:continue
            add(olddist,pq,t,value+w,(-1,s),dict(act,entry_guard=True),0,cutoff)
        for dest,price,targets in high[b]:
            if 4 in targets:continue
            for dt,rr in enumerate(buckets[dest]):
                for t in rr:add(olddist,pq,t,value+price+dt-D[s],(-1,s),{'kind':'INITIAL_HIGH','targets':targets,'price':price},0,cutoff)
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
    path=[]
    if fail:
        z=min(fail,key=lambda z:(z['R_lower_bound'],z['slack']));p=(1,z['sid'])
        while p in parent:
            old,act=parent[p];path.append({'phase':p[0],'A':na[p[1]],'BF':nb[p[1]],'slack':(newdist if p[0] else olddist)[p[1]],'action':act});p=old
        path.append({'phase':p[0],'A':na[p[1]],'BF':nb[p[1]],'slack':olddist[p[1]],'action':{'kind':'INITIAL'}});path.reverse()
    result={'status':'PARTIAL' if reason else 'ABSTRACT_FAILURE' if fail else 'COMPLETE_EXCLUSION','halt':reason,'minimum_cold_gamma':gm,'old_cutoff':cutoff,
        'processed':processed,'edge_checks':checks,'terminal_checks':terminal,'minimum_terminal_bound':minR,'abstract_failures':fail,'abstract_path':path,
        'path_is_source_counterexample':False,'new_source_queries':0,
        'old_states':[{'A':na[s],'BF':nb[s],'slack':olddist[s]} for s in range(N) if olddist[s]!=999],
        'new_states':[{'A':na[s],'BF':nb[s],'slack':newdist[s]} for s in range(N) if newdist[s]!=999]}
    out('twochart_guarded_analysis.json',result);print(json.dumps({k:result[k] for k in ('status','minimum_cold_gamma','old_cutoff','processed','edge_checks','minimum_terminal_bound')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_twochart2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
