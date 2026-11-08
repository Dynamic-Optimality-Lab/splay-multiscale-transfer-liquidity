"""Necessary BF source comparison; does NOT assert abstract cheap A realization.
Exact density/pruning lifting precedes any use as a universal certificate.
"""
import collections,functools,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('original_rotations13',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
calls=0
@functools.lru_cache(None)
def trees(lo,hi):
    if lo>hi:return ('F'+str(hi),)
    return tuple((k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi))
@functools.lru_cache(None)
def frames(t):
    if isinstance(t,str):return (0,())
    a,aa=frames(t[1]);b,bb=frames(t[2]);s=a|b|(1<<(t[0]-1))
    return s,aa+bb+((s,1<<(t[0]-1)),)
def valid(t,mask):
    return bool(mask&(1<<(t[0]-1))) and all(2*(s&mask).bit_count()-s.bit_count()>=bool(root&mask) for s,root in frames(t)[1])
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main(k,cap):
    global calls
    start=time.process_time();limit=min(float(cap)-3,40)
    partition=json.loads((B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/source_partition_certificate.json').read_text())
    row=next(v for v in partition['rows'] if v['core']==k)
    masks=[tuple(v['marks']) for v in row['necessary_masks']];allts=trees(1,k)
    all_nodes=[];all_edges=[];all_potential=[];summaries=[];failures=[];cache={}
    for marks in masks:
        mask=sum(1<<(v-1) for v in marks);ts=[t for t in allts if valid(t,mask)];ids={t:i for i,t in enumerate(ts)}
        edges=[];adj=[[] for _ in ts]
        for i,t in enumerate(ts):
            for x in marks:
                if x==t[0]:continue
                key=(t,x)
                if key not in cache:
                    calls+=1;assert calls<2000000 and time.process_time()-start<limit
                    dest,path,ev=p.trace(t,x);q=sum(v['kind']=='DOUBLE' for v in ev);cache[key]=(dest,q)
                dest,q=cache[key]
                if dest not in ids:continue
                e=(i,ids[dest],x,q);edges.append(e);adj[i].append(len(edges)-1)
        # Exact integer longest-path inequalities D(t)>=D(s)+Q-2.
        # A repeated improving predecessor chain witnesses a positive cycle.
        d=[0]*len(ts);pred=[None]*len(ts);ql=collections.deque(range(len(ts)));inside=[True]*len(ts);length=[0]*len(ts);cycle=None
        while ql and cycle is None:
            a=ql.popleft();inside[a]=False
            for ei in adj[a]:
                a,b,x,q=edges[ei];nd=d[a]+q-2
                if nd<=d[b]:continue
                d[b]=nd;pred[b]=ei;length[b]=length[a]+1
                if length[b]>=len(ts):
                    v=b
                    for _ in ts:v=edges[pred[v]][0]
                    vv=v;cc=[]
                    while True:
                        ei=pred[v];cc.append(ei);v=edges[ei][0]
                        if v==vv:break
                    cc.reverse();assert sum(edges[e][3]-2 for e in cc)>0
                    cycle=cc;break
                if not inside[b]:ql.append(b);inside[b]=True
            if time.process_time()-start>=limit:raise RuntimeError('bounded BF comparison CPU stop')
        if cycle is None:
            assert all(2-q+d[b]-d[a]>=0 for a,b,x,q in edges)
        else:
            failures.append({'marks':marks,'states':ts,'cycle_edges':[edges[e] for e in cycle],
                'BF_price':sum(2-edges[e][3] for e in cycle),
                'status':'BF_ONLY_SUFFICIENT_COMPARISON_REFUTED; no cheap A or all-support cycle realization assumed'})
        offset=len(all_nodes);all_nodes.extend(ts)
        all_edges.extend((a+offset,b+offset,x,q) for a,b,x,q in edges)
        all_potential.extend(d)
        summaries.append({'marks':marks,'states':len(ts),'edges':len(edges),'max_debt':max(d,default=0),
            'status':'EXACT_INEQUALITIES_VERIFIED' if cycle is None else 'BF_ONLY_NEGATIVE_CYCLE'})
        # A failure is sufficient to reject the COMMON B-only certificate;
        # do not waste remaining caps enumerating masks for a refuted template.
        if cycle is not None:break
    result={'status':'PROVED_COMPLETE_NECESSARY_BF_COMPARISON' if not failures else 'REFUTED_BF_ONLY_SUFFICIENT_TEMPLATE',
        'core':k,'all_necessary_mask_count':len(masks),'processed_masks':len(summaries),'mask_summaries':summaries,
        'trees':all_nodes,'edges':all_edges,'debt':all_potential,'failures':failures,'source_engine_calls':calls,
        'lifting':'fixed full labeled core + original subtree density + arbitrary rigid ordered gaps; actual source maps into graph, no reverse realization claimed',
        'potential_scope':'Q per genuine BF macro against exactly two abstract budget units; not yet source A-dependent funding',
        'original_A_semantics':'all original operations/events must still be replayed for any source counterexample'}
    out('bf'+str(k)+'_comparison.json',result)
    print(json.dumps({'status':result['status'],'core':k,'mask_count':len(summaries),'states':len(all_nodes),
        'edges':len(all_edges),'max_debt':max(all_potential,default=0),'negative_cycles':len(failures),'source_calls':calls}),flush=True)
