"""Zero-margin reachability using ONLY the already audited cached relation.
No splay, root/path query or source-frame compiler. An abstract path is
explicitly NOT an original-source counterexample. Whole original packet
forward inclusion is justified by the existing source/packet bridge.
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
                if q1==1 and y in (1,6):
                    low[s].append((dest,x,6,y));high[s].append((dest,2,'HIGH_PAIR',(x,y)))
    lower=(4,(3,(2,(1,'F0','F1'),'F2'),'F3'),'F4')
    F=(7,(6,(5,lower,'F5'),'F6'),(8,'F7',(9,'F8',(10,'F9',(11,'F10','F11')))))
    f=bi[F];entry=[]
    for L in [(1500,(1000,None,None),(2000,None,None)),(1000,None,(2000,None,None))]:
        A=(4000,(3000,L,None),(5000,None,(6000,None,None)));a=ai[A];s=sid(f,a);assert D[s]==1;entry.append(s)
    targets={sid(b,381) for b in (1060,1063)};assert all(D[s]==3 for s in targets)
    seen=bytearray(N);parent=array('i',[-1])*N;action={};queue=collections.deque();high_done=set();pair_cache={};edge_checks=0;zero_edges=0
    for s in entry:seen[s]=1;queue.append(s)
    def add(t,s,act):
        nonlocal zero_edges
        zero_edges+=1
        if not seen[t]:seen[t]=1;parent[t]=s;action[t]=act;queue.append(t)
    found=None;reason=None;processed=0
    while queue:
        s=queue.popleft();a=nodeA[s];b=nodeB[s];ds=D[s];processed+=1
        if s in targets:found=s;break
        for dest,x,q,y in low[b]:
            if y is None:
                for ta,h in aa[a].get(x,{}).items():
                    edge_checks+=1;t=sid(dest,ta)
                    margin=2*h-q+D[t]-ds;assert margin>=0
                    if margin==0:add(t,s,{'kind':'LOW_SINGLE','H':h,'target_rank':x})
            else:
                key=(a,x,y)
                if key not in pair_cache:
                    rel={}
                    for mid,h1 in aa[a].get(x,{}).items():
                        for ta,h2 in aa[mid].get(y,{}).items():
                            if h1+h2<=3 and (ta not in rel or h1+h2<rel[ta][0]):rel[ta]=(h1+h2,mid,h1,h2)
                    pair_cache[key]=rel
                for ta,(hh,mid,h1,h2) in pair_cache[key].items():
                    edge_checks+=1;t=sid(dest,ta);margin=2*hh-6+D[t]-ds;assert margin>=0
                    if margin==0:add(t,s,{'kind':'LOW_PAIR','targets_rank':[x,y],'H':[h1,h2],'middle_A':mid})
        if (b,ds) not in high_done:
            high_done.add((b,ds))
            for dest,price,kind,target in high[b]:
                value=ds-price
                if 0<=value<=3:
                    for t in bucket[dest][value]:edge_checks+=1;add(t,s,{'kind':kind,'capped_packet_price':price,'target_rank':target})
        if processed%32==0:
            if time.process_time()-START>CAP-2:reason='CPU_RESERVE';break
            if edge_checks>=4900000:reason='EDGE_RESERVE';break
    path=[]
    if found is not None:
        t=found
        while parent[t]!=-1:
            s=parent[t];path.append({'source':{'A':nodeA[s],'BF':nodeB[s],'D':D[s]},'target':{'A':nodeA[t],'BF':nodeB[t],'D':D[t]},'action':action[t]});t=s
        path.reverse()
    result={'status':'ABSTRACT_ZERO_PATH_FOUND' if found is not None else 'COMPLETE_ZERO_REACHABILITY_EXCLUSION' if not queue and reason is None else 'PARTIAL_SAVED_CACHED_ANALYSIS',
        'new_source_queries':0,'source_engine_calls':0,'states_total':N,'processed':processed,'reachable':sum(seen),'frontier':len(queue),
        'edge_checks':edge_checks,'zero_edges':zero_edges,'halt':reason,'entry_states':[{'A':nodeA[s],'BF':nodeB[s],'D':D[s]} for s in entry],
        'targets':[{'A':nodeA[s],'BF':nodeB[s],'D':D[s]} for s in targets],'abstract_path':path,
        'path_is_source_counterexample':False,'source_scope':'necessary complete six-key cached packet relation; actual private7 geometry not yet imposed'}
    out('zero_slack_reachability.json',result)
    print(json.dumps({k:result[k] for k in ('status','processed','reachable','frontier','edge_checks','halt')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
