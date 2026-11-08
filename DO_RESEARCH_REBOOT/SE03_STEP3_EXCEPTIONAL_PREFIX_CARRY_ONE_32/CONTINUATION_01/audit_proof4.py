"""Bounded-slack proof analysis of cached COMPLETE six-key packet relation.
No new source query/compiler/splay. Nonnegative margins let us truncate at
slack2 because every adverse H1 terminal margin is in{-1,-2,-3}. Paths in
this overapproximation are not asserted source-realizable.
"""
import json,time,sys,collections
from array import array
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;OLD=P/'SE03_STEP2_UNARY_A_LIFT_14'
START=time.process_time();CAP=float(sys.argv[1])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def fr(v):return tuple(fr(x) for x in v) if isinstance(v,list) else v
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    g=read(OLD/'branch_grammar2.json');c=read(OLD/'branch_core11_mask0.json');AA=g['states'];TT=c['BF_trees'];M=c['marks'];D=bytes(c['debt'])
    ai={fr(t):i for i,t in enumerate(AA)};bi={fr(t):i for i,t in enumerate(TT)}
    ar={r:[] for r in range(1,7)}
    for a,t in enumerate(AA):ar[t[0]//1000].append(a)
    pos={a:i for rr in ar.values() for i,a in enumerate(rr)};off=[];nodeA=array('H');nodeB=array('H');bucket=[]
    for b,t in enumerate(TT):
        off.append(len(nodeA));rr=ar[M.index(t[0])+1];bb=[[] for _ in range(4)]
        for a in rr:bb[D[len(nodeA)]].append(len(nodeA));nodeA.append(a);nodeB.append(b)
        bucket.append(bb)
    N=len(D);assert N==len(nodeA)<2000000
    def sid(b,a):return off[b]+pos[a]
    aa=[collections.defaultdict(dict) for _ in AA]
    for h in (1,2):
        for a,x,t in g['H'+str(h)]:aa[a][x][t]=min(h,aa[a][x].get(t,99))
    adj=[[] for _ in TT]
    for s,t,x,q in c['BF_relation']:adj[s].append((t,M.index(x)+1,q))
    low=[[] for _ in TT];high=[[] for _ in TT]
    for s,t,x,q in c['BF_relation']:
        x=M.index(x)+1
        if q<=4:low[s].append((t,x,q,None));high[s].append((t,6-q,'HIGH_SINGLE',x))
        else:
            for dest,y,q1 in adj[t]:
                if q1==1 and y in (1,6):low[s].append((dest,x,6,y));high[s].append((dest,2,'HIGH_PAIR',(x,y)))
    lower=(4,(3,(2,(1,'F0','F1'),'F2'),'F3'),'F4')
    F=(7,(6,(5,lower,'F5'),'F6'),(8,'F7',(9,'F8',(10,'F9',(11,'F10','F11')))))
    f=bi[F];entry=[]
    for L in [(1500,(1000,None,None),(2000,None,None)),(1000,None,(2000,None,None)),(2000,(1000,None,None),None)]:
        A=(4000,(3000,L,None),(5000,None,(6000,None,None)));a=ai[A];s=sid(f,a);entry.append(s)
    dist=bytearray([255])*N;parent=array('i',[-1])*N;action={};queues=[collections.deque() for _ in range(3)]
    # Collapse the SOURCE-PROVED canonical H1 upper phase, retaining its
    # exact nonnegative table slack. Only the first actual departure is
    # seeded, with the proved whole-macro lower-depth bounds. Later phases
    # use the entire cached necessary relation without additional guards.
    L=(6,(5,lower,'F5'),'F6')
    forms={
      'A':(7,L,(8,'F7',(9,'F8',(10,'F9',(11,'F10','F11'))))),
      'B':(9,(8,(7,L,'F7'),'F8'),(10,'F9',(11,'F10','F11'))),
      'C':(11,(10,(9,(8,(7,L,'F7'),'F8'),'F9'),'F10'),'F11'),
      'D':(11,(8,(7,L,'F7'),(10,(9,'F8','F9'),'F10')),'F11'),
      'E':(7,L,(8,'F7',(11,(10,(9,'F8','F9'),'F10'),'F11'))),
      'F':(7,L,(10,(8,'F7',(9,'F8','F9')),(11,'F10','F11'))),
      'G':(11,(10,(7,L,(8,'F7',(9,'F8','F9'))),'F10'),'F11')}
    ce=[('A','B',1),('A','D',2),('B','A',1),('B','C',1),('C','B',1),('C','F',2),
        ('D','E',1),('E','D',1),('E','B',2),('F','G',1),('G','F',1),('G','B',2)]
    relH={h:collections.defaultdict(list) for h in (1,2)}
    for h in (1,2):
        for a,x,t in g['H'+str(h)]:relH[h][(a,x)].append(t)
    canonical=[];seed_actions={}
    def seed(t,s,value,act):
        assert value>=0
        if value<=2 and value<dist[t]:
            dist[t]=value;queues[value].append(t);seed_actions[t]={'canonical_source':{'A':nodeA[s],'BF':nodeB[s],'D':D[s]},'action':act}
    for small in [(1500,(1000,None,None),(2000,None,None)),(1000,None,(2000,None,None)),(2000,(1000,None,None),None)]:
        A9=(4000,(3000,small,None),(5000,None,(6000,None,None)))
        A11=(5000,(4000,(3000,small,None),None),(6000,None,None))
        A13=(6000,(5000,(4000,(3000,small,None),None),None),None)
        ids={name:sid(bi[t],ai[{7:A9,9:A11,11:A13}[t[0]]]) for name,t in forms.items()}
        cc={name:999 for name in forms};cc['A']=D[ids['A']]-1
        changed=True
        while changed:
            changed=False
            for s,t,q in ce:
                weight=2-q+D[ids[t]]-D[ids[s]];assert weight>=0
                if cc[t]>cc[s]+weight:cc[t]=cc[s]+weight;changed=True
        for name,s in ids.items():
            current=cc[name];canonical.append({'name':name,'A':nodeA[s],'BF':nodeB[s],'D':D[s],'minimum_slack':current})
            if current>2:continue
            a=nodeA[s];b=nodeB[s];ds=D[s];root=TT[b][0]
            for dest,x,q in adj[b]:
                lower_target=x in (1,2,3)
                hmin=(1 if x==3 else 2) if root==7 else 2 if root==9 else (2 if x==3 else 3)
                for h in (1,2):
                    if (h==1 and not lower_target) or (lower_target and h<hmin):continue
                    if q==5:continue # only lower1 in C; its proved hmin3
                    for ta in relH[h][(a,x)]:
                        t=sid(dest,ta);weight=2*h-q+D[t]-ds;assert weight>=0
                        seed(t,s,current+weight,{'kind':'DEPARTURE_LOW','H':h,'target_rank':x,'margin':weight})
                if q<=4:
                    for debt,rr in enumerate(bucket[dest]):
                        weight=6-q+debt-ds
                        if current+weight<=2:
                            for t in rr:seed(t,s,current+weight,{'kind':'DEPARTURE_HIGH','target_rank':x,'margin':weight})
                else:
                    assert lower_target and x==1 and hmin==3
                    for end,y,q1 in adj[dest]:
                        if q1!=1 or y not in (1,6):continue
                        for debt,rr in enumerate(bucket[end]):
                            weight=2+debt-ds
                            if current+weight<=2:
                                for t in rr:seed(t,s,current+weight,{'kind':'DEPARTURE_HIGH_PAIR','targets_rank':[x,y],'margin':weight})
    high_done=set();pair_cache={};checks=0;updates=len(entry);processed=0;reason=None
    def add(t,s,weight,act,current):
        nonlocal updates
        assert weight>=0
        value=current+weight
        if value<=2 and value<dist[t]:dist[t]=value;parent[t]=s;action[t]=act;queues[value].append(t);updates+=1
    for current in range(3):
        while queues[current]:
            s=queues[current].popleft()
            if dist[s]!=current:continue
            a=nodeA[s];b=nodeB[s];ds=D[s];processed+=1
            for dest,x,q,y in low[b]:
                if y is None:
                    rel=((ta,h,None,None,None) for ta,h in aa[a].get(x,{}).items())
                else:
                    key=(a,x,y)
                    if key not in pair_cache:
                        rr={}
                        for mid,h1 in aa[a].get(x,{}).items():
                            for ta,h2 in aa[mid].get(y,{}).items():
                                if h1+h2<=3 and (ta not in rr or h1+h2<rr[ta][0]):rr[ta]=(h1+h2,mid,h1,h2)
                        pair_cache[key]=rr
                    rel=((ta,hh,mid,h1,h2) for ta,(hh,mid,h1,h2) in pair_cache[key].items())
                for ta,h,mid,h1,h2 in rel:
                    checks+=1;t=sid(dest,ta);weight=2*h-q+D[t]-ds
                    add(t,s,weight,{'kind':'LOW_SINGLE' if y is None else 'LOW_PAIR','targets_rank':[x] if y is None else [x,y],
                                   'H':[h] if y is None else [h1,h2],'middle_A':mid,'margin':weight},current)
            if (b,ds) not in high_done:
                high_done.add((b,ds))
                for dest,price,kind,target in high[b]:
                    for debt,rr in enumerate(bucket[dest]):
                        weight=price+debt-ds
                        assert weight>=0 or not rr
                        if current+weight<=2:
                            for t in rr:checks+=1;add(t,s,weight,{'kind':kind,'target_rank':target,'capped_packet_price':price,'margin':weight},current)
            if processed%64==0:
                if time.process_time()-START>CAP-2:reason='CPU_RESERVE';break
                if checks>=4900000:reason='EDGE_RESERVE';break
        if reason:break
    bad=read(B.parent/'six_key_boundary_analysis.json')['all_terminal_bridge_violations'];fail=[]
    for z in bad:
        assert z['return_H_lower_bound']==1
        s=sid(z['BF_index'],z['A_index'])
        if dist[s]<=2 and dist[s]+z['margin']<0:fail.append(dict(z,minimum_slack=dist[s],sid=s))
    path=[]
    if fail:
        s=min(fail,key=lambda z:(z['minimum_slack'],z['margin']))['sid'];end=s
        while parent[s]!=-1:
            p=parent[s];path.append({'source':{'A':nodeA[p],'BF':nodeB[p],'D':D[p],'slack':dist[p]},
                                   'target':{'A':nodeA[s],'BF':nodeB[s],'D':D[s],'slack':dist[s]},'action':action[s]});s=p
        path.reverse()
        path.insert(0,dict(seed_actions[s],target={'A':nodeA[s],'BF':nodeB[s],'D':D[s],'slack':dist[s]}))
    result={'status':'PARTIAL_SAVED_CACHED_ANALYSIS' if reason else 'ABSTRACT_TERMINAL_FAILURE_FOUND' if fail else 'COMPLETE_BOUNDED_SLACK_TERMINAL_EXCLUSION',
        'new_source_queries':0,'processed':processed,'edge_checks':checks,'updates':updates,'halt':reason,
        'canonical_source_states':canonical,'guard':'full source-proved H1 upper phase; first lower exit has prescribed H lower bound; any upper H>=2 departs',
        'reached_by_slack':{str(k):dist.count(k) for k in range(3)},
        'entry_states':[{'A':nodeA[s],'BF':nodeB[s],'D':D[s],'initial_slack':D[s]-1} for s in entry],
        'reached_states':[{'A':nodeA[s],'BF':nodeB[s],'D':D[s],'minimum_slack':dist[s]} for s in range(N) if dist[s]<=2],
        'adverse_terminal_count':len(bad),'abstract_failure_count':len(fail),'first_abstract_failure':fail[0] if fail else None,
        'abstract_failures':fail,'one_abstract_path':path,'path_is_source_counterexample':False,
        'scope':'static necessary COMPLETE cached packet graph; all endpoint and private7 source realization distinctions retained'}
    out('canonical_exit_bounded_slack.json',result)
    print(json.dumps({k:result[k] for k in ('status','processed','edge_checks','reached_by_slack','abstract_failure_count','halt')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof4_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
