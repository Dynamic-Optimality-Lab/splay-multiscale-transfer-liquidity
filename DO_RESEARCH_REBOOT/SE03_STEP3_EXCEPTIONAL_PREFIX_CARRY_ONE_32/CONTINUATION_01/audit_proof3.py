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
    # Exact initial source guard, with NO new source operation: immediately
    # after activation9, physical1/3 have depth>=3 below9->7->5. Their
    # whole next genuine macro cannot have H1. H2/HIGH stay overapproximated.
    seed_actions={};seed_count=0
    relH={h:collections.defaultdict(list) for h in (1,2)}
    for h in (1,2):
        for a,x,t in g['H'+str(h)]:relH[h][(a,x)].append(t)
    def seed(t,s,weight,act):
        nonlocal seed_count
        assert weight>=0
        value=D[s]-1+weight
        if value<=2 and value<dist[t]:dist[t]=value;parent[t]=-1;queues[value].append(t);seed_actions[t]={'source_entry':{'A':nodeA[s],'BF':nodeB[s],'D':D[s],'initial_slack':D[s]-1},'action':act};seed_count+=1
    for s in entry:
        a=nodeA[s];b=nodeB[s];ds=D[s]
        for dest,x,q in adj[b]:
            assert q<=4
            for h in (1,2):
                if h==1 and x in (1,2):continue
                for ta in relH[h][(a,x)]:
                    t=sid(dest,ta);weight=2*h-q+D[t]-ds
                    seed(t,s,weight,{'kind':'INITIAL_LOW','H':h,'target_rank':x,'margin':weight})
            for debt,rr in enumerate(bucket[dest]):
                weight=6-q+debt-ds
                if D[s]-1+weight<=2:
                    for t in rr:seed(t,s,weight,{'kind':'INITIAL_HIGH','target_rank':x,'margin':weight})
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
        'new_source_queries':0,'processed':processed,'edge_checks':checks,'updates':updates,'halt':reason,'seed_updates':seed_count,
        'source_guard':'only FIRST H1 macro after activation9 excludes targets1/3; H2/HIGH use all old cached endpoints. No initial7 return is source-valid.',
        'reached_by_slack':{str(k):dist.count(k) for k in range(3)},
        'entry_states':[{'A':nodeA[s],'BF':nodeB[s],'D':D[s],'initial_slack':D[s]-1} for s in entry],
        'reached_states':[{'A':nodeA[s],'BF':nodeB[s],'D':D[s],'minimum_slack':dist[s]} for s in range(N) if dist[s]<=2],
        'adverse_terminal_count':len(bad),'abstract_failure_count':len(fail),'first_abstract_failure':fail[0] if fail else None,
        'abstract_failures':fail,'one_abstract_path':path,'path_is_source_counterexample':False,
        'scope':'static necessary COMPLETE cached packet graph; all endpoint and private7 source realization distinctions retained'}
    out('guarded_bounded_slack_reachability.json',result)
    print(json.dumps({k:result[k] for k in ('status','processed','edge_checks','reached_by_slack','abstract_failure_count','halt')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
