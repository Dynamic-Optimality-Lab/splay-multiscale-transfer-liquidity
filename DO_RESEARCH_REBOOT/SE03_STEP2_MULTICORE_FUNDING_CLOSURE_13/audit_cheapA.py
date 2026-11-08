"""A-dependent recursion: H1 words with six-node marked A core.
Finite source comparison of cheap marked A splays and actual BF sectors.
One-way arbitrary-gap lifting is restricted explicitly; no all-core claim.
"""
import collections,functools,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
s=importlib.util.spec_from_file_location('immutable_cheapA13',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(s);s.loader.exec_module(I);calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
@functools.lru_cache(None)
def trees(lo,hi):
    if lo>hi:return (('leaf',),)
    return tuple(I.node(k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi))
def packA(t):return None if t[0]=='leaf' else (t[1],packA(t[2]),packA(t[3]))
def cheap():
    global calls
    ts=trees(1,6);ids={t:i for i,t in enumerate(ts)};adj={}
    for a,t in enumerate(ts):
        for x in range(1,7):
            depth=I.lookup(t,x)[1]
            if not 1<=depth<=2:continue
            calls+=1;d,e=I.trace(t,x);assert len(e)==1;adj[a,x]=ids[d]
    return ts,adj
def main():
    aa,cheap_edges=cheap();reports=[]
    for k in (9,10,11):
        cert=json.loads((B/('bf'+str(k)+'_comparison.json')).read_text());marks=cert['mask_summaries'][0]['marks']
        nn=cert['mask_summaries'][0]['states'];bt=cert['trees'][:nn];rank={x:i+1 for i,x in enumerate(marks)}
        be={(a,rank[x]):(b,q) for a,b,x,q in cert['edges'] if a<nn};states=[(a,b) for b,t in enumerate(bt) for a,at in enumerate(aa) if at[1]==rank[t[0]]]
        ix={v:i for i,v in enumerate(states)};edges=[];adj=[[] for v in states]
        for i,(a,b) in enumerate(states):
            for x in range(1,7):
                if (a,x) not in cheap_edges or (b,x) not in be:continue
                bb,q=be[b,x];dest=ix[cheap_edges[a,x],bb];adj[i].append(len(edges));edges.append((i,dest,x,q))
        d=[0]*len(states);pred=[None]*len(states);queue=collections.deque(range(len(states)));inside=set(queue);bad=None
        while queue and bad is None:
            a=queue.popleft();inside.remove(a)
            for ei in adj[a]:
                a,b,x,q=edges[ei]
                if d[b]>=d[a]+q-2:continue
                d[b]=d[a]+q-2;pred[b]=ei
                if d[b]>8:
                    v=b;seen={};chain=[]
                    while pred[v] is not None and v not in seen:
                        seen[v]=len(chain);e=pred[v];chain.append(e);v=edges[e][0]
                    if v in seen:
                        cc=chain[seen[v]:];cc.reverse()
                        if sum(2-edges[e][3] for e in cc)<0:bad=cc;break
                if b not in inside:queue.append(b);inside.add(b)
        if bad is None:assert all(2-q+d[b]-d[a]>=0 for a,b,x,q in edges)
        reports.append({'core':k,'marked_A_core':6,'all_macros_H':1,'BF_marks':marks,
            'scope':'only first BF mask except11 whose single mask is complete; every other A core and mixed H remain OPEN',
            'states':states,'A_trees':[packA(t) for t in aa],'BF_trees':bt,'edges':edges,'debt':d,
            'max_debt':max(d),'negative_cycle':None if bad is None else [edges[e] for e in bad],
            'status':'EXACT_RESTRICTED_A_DEPENDENT_INEQUALITIES' if bad is None else 'RESTRICTED_COMPARISON_NEGATIVE_CYCLE',
            'private_lifting':'A marked core6 means all its search paths contain only marked keys, arbitrary private gaps rigid; BF separate actual fixed full core/free gaps',
            'not_claimed':'arbitrary A inventories/cores during mixed-cost sources, diagonal reachability of an adverse abstract pair, or complete multicore funding'})
        assert len(states)<2000000 and len(edges)<5000000
    out('cheap_A_comparison.json',{'status':'A_DEPENDENT_RECURSION_RECORDED','reports':reports,'source_engine_calls':calls})
    print(json.dumps({'status':'PASS_RESTRICTED_ROUTE_AUDIT','reports':[{'core':r['core'],'states':len(r['states']),'edges':len(r['edges']),'max_debt':r['max_debt'],'status':r['status']} for r in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_cheapA_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
