"""Exact sufficient branch-quotient construction; sequential immutable cases.
No populations are bounded. Mirrors use an explicit order-reversal lift.
"""
import collections,functools,importlib.util,json,time
from array import array
from pathlib import Path
B=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('branch_all_source14',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,separators=(',',':'))
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
@functools.lru_cache(None)
def density_trees(lo,hi,marks):
    if lo>hi:return ('F'+str(hi),)
    mass=2*sum(lo<=m<=hi for m in marks)-(hi-lo+1)
    return tuple((x,l,r) for x in range(lo,hi+1) if mass>=int(x in marks)
        for l in density_trees(lo,x-1,marks) for r in density_trees(x+1,hi,marks))
def bf_graph(k,marks,K=p):
    global calls
    ts=tuple(t for t in density_trees(1,k,tuple(marks)) if t[0] in marks);ix={t:i for i,t in enumerate(ts)}
    edges=[]
    for a,t in enumerate(ts):
        for x in marks:
            if x==t[0]:continue
            calls+=1;assert calls<2000000
            dest,path,ev=K.trace(t,x)
            if dest not in ix:continue
            if k==11 and any(e['kind']!='DOUBLE' or e['case'] not in ('LL','RR') or e['G'] not in marks or e['P'] in marks for e in ev):continue
            edges.append((a,ix[dest],x,sum(e['kind']=='DOUBLE' for e in ev)))
    return ts,edges
def prepare(G,ts,edges,marks,k):
    rank={x:i+1 for i,x in enumerate(marks)};ar={r:[] for r in range(1,7)}
    for a,t in enumerate(G['states']):ar[t[0]//1000].append(a)
    apos={a:j for rr in ar.values() for j,a in enumerate(rr)}
    offsets=[];nodeA=array('H');nodeB=array('H')
    for b,t in enumerate(ts):
        offsets.append(len(nodeA));aa=ar[rank[t[0]]];nodeA.extend(aa);nodeB.extend([b]*len(aa))
    N=len(nodeA);assert N<2000000
    aa=[collections.defaultdict(dict) for _ in G['states']]
    for H,name in ((1,'H1'),(2,'H2')):
        for a,x,t in G[name]:aa[a][x][t]=min(H,aa[a][x].get(t,9))
    adj=[[] for _ in ts]
    for s,t,x,q in edges:adj[s].append((t,rank[x],q))
    pairs={};low=[[] for _ in ts];high=[[] for _ in ts]
    for s,t,x,q in edges:
        xx=rank[x]
        if q<=4:low[s].append((t,xx,q,False));high[s].append((t,q-6))
        else:
            assert k==11 and q==5
            for end,yy,q1 in adj[t]:
                if q1!=1 or yy not in (1,6):continue
                key=(xx,yy)
                if key not in pairs:
                    rel=[]
                    for a in range(len(aa)):
                        rr={}
                        for mid,h1 in aa[a].get(xx,{}).items():
                            for dest,h2 in aa[mid].get(yy,{}).items():
                                if h1+h2<=3:rr[dest]=min(h1+h2,rr.get(dest,9))
                        rel.append(tuple(rr.items()))
                    pairs[key]=rel
                low[s].append((end,key,6,True));high[s].append((end,-2))
    return ar,apos,offsets,nodeA,nodeB,aa,low,high,pairs
def solve(G,ts,edges,marks,k,deadline):
    ar,apos,off,na,nb,aa,low,high,pairs=prepare(G,ts,edges,marks,k)
    N=len(na);nB=len(ts);d=bytearray(N);inq=bytearray(N);queue=collections.deque();maximum=[0]*nB
    updates=0;stop=None
    # The only constraints violated by zero debt have positive gain. Seed
    # just those; thereafter every raised source is processed, including HIGH.
    def raise_to(t,new):
        nonlocal updates,stop
        if new<=d[t]:return
        if new>19:stop={'kind':'RANGE_EXCEEDED','required':new,'target':t};return
        d[t]=new;updates+=1
        if not inq[t]:queue.append(t);inq[t]=1
    def lows(sid):
        a=na[sid];b=nb[sid];ds=d[sid]
        for dest,x,q,pair in low[b]:
            rel=pairs[x][a] if pair else aa[a].get(x,{}).items()
            for target,H in rel:raise_to(off[dest]+apos[target],ds+q-2*H)
    for b,ee in enumerate(low):
        if any(q>2 for dest,x,q,pair in ee):
            for j in range(off[b],off[b]+len(ar[ts[b][0] and marks.index(ts[b][0])+1])):lows(j)
        if time.process_time()>deadline:stop={'kind':'CPU_RESERVE_STOP','stage':'initialization'};break
    while queue and stop is None:
        sid=queue.popleft();inq[sid]=0;lows(sid);b=nb[sid];ds=d[sid]
        if ds>maximum[b]:
            maximum[b]=ds
            for dest,gain in high[b]:
                floor=ds+gain
                if floor>0:
                    rootrank=marks.index(ts[dest][0])+1
                    for j in range(off[dest],off[dest]+len(ar[rootrank])):raise_to(j,floor)
        if updates%1024==0 and time.process_time()>deadline:stop={'kind':'CPU_RESERVE_STOP','stage':'propagation'}
    if stop:return {'status':'UNRESOLVED_SUFFICIENT_COMPARISON','stop':stop,'states':N,'updates':updates}
    # Independent verifier regenerates ALL inequalities, not just propagation.
    return {'status':'CANDIDATE_COMPLETE','states':N,'debt':list(d),'max_debt':max(d),'updates':updates,
        'working_bank_bound':(6 if k==11 else 4)+max(d),
        'state_order':'BF density_trees order; within BF state, branch A indices of same marked root, increasing'}
def main(cap):
    start=time.process_time();deadline=start+float(cap)-3
    G=json.loads((B/'branch_grammar2.json').read_text());part=json.loads((B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/source_partition_certificate.json').read_text())
    reports=[];halt=None
    for k in (9,10,11):
        row=next(v for v in part['rows'] if v['core']==k);masks=[tuple(v['marks']) for v in row['necessary_masks']]
        for i,M in enumerate(masks):
            mirror=tuple(sorted(k+1-x for x in M))
            if M>mirror:reports.append({'core':k,'marks':M,'status':'MIRROR_TRANSPORT','representative':mirror});continue
            name='branch_core'+str(k)+'_mask'+str(i)+'.json'
            ts,edges=bf_graph(k,M)
            if k==9 and i==0:
                old=json.loads((B/'branch9_candidate2.json').read_text())['attempts'][-1]
                # Reindex existing certified comparison, without rerunning it.
                oldbf=json.loads((B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/bf9_comparison.json').read_text())
                assert ts==tuple(map(freeze,oldbf['trees'][:len(ts)])) and edges==list(map(tuple,oldbf['edges']))
                vals=dict(zip(old['valid_states'],old['debt']));ar=collections.defaultdict(list)
                for a,t in enumerate(G['states']):ar[t[0]//1000].append(a)
                debt=[vals[a*len(ts)+b] for b,t in enumerate(ts) for a in ar[M.index(t[0])+1]]
                r={'status':'CANDIDATE_COMPLETE','states':len(debt),'debt':debt,'max_debt':max(debt),'working_bank_bound':4+max(debt),'reused':'branch9_candidate2.json'}
            else:r=solve(G,ts,edges,M,k,deadline)
            r.update({'core':k,'marks':M,'BF_states':len(ts),'BF_edges':len(edges),'BF_trees':ts,'BF_relation':edges,'source_engine_calls_total':calls})
            out(name,r);reports.append({'core':k,'marks':M,'file':name,'status':r['status'],'max_debt':r.get('max_debt'),'states':r['states']})
            print(json.dumps({q:v for q,v in reports[-1].items() if q!='marks'}),flush=True)
            if r['status']!='CANDIDATE_COMPLETE' or time.process_time()>deadline:
                halt={'core':k,'mask_index':i,'marks':M,'reason':r.get('stop',{'kind':'CPU_RESERVE_STOP_AFTER_SAVED_CASE'})};break
        if halt:break
    out('branch_all_construction.json',{'status':'ALL_CANDIDATES_CONSTRUCTED' if halt is None else 'PARTIAL_SAVED_CONSTRUCTION','reports':reports,'halt':halt,'source_engine_calls':calls,
        'scope':'source-uniform branch quotient if every lifting lemma and independent inequality audit succeeds; no source realization of adverse quotient paths assumed'})
