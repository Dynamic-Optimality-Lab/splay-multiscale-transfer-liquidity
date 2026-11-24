"""Finite falsification screen for a separate B-core gap hypothesis."""
from base1 import *
from functools import lru_cache
from itertools import combinations
sys.path.insert(0,str(REPO/'python'))
from independent import splay as ind

@lru_cache(None)
def shapes(lo,hi):
    if lo>hi:return (ind.LEAF,)
    return tuple(ind.node(k,l,r) for k in range(lo,hi+1) for l in shapes(lo,k-1) for r in shapes(k+1,hi))

def path(t,x):
    out=[]
    while t!=ind.LEAF:
        _,k,l,r=t;out.append(k)
        if x==k:return out
        t=r if x>k else l
    raise AssertionError

def components(edges,rev):
    seen=set();order=[]
    for root in range(len(edges)):
        if root in seen:continue
        stack=[(root,False)]
        while stack:
            v,done=stack.pop()
            if done:order.append(v);continue
            if v in seen:continue
            seen.add(v);stack.append((v,True))
            stack.extend((w,False) for w in edges[v] if w not in seen)
    seen=set()
    for root in reversed(order):
        if root in seen:continue
        group=[];stack=[root];seen.add(root)
        while stack:
            v=stack.pop();group.append(v)
            for w in rev[v]:
                if w not in seen:seen.add(w);stack.append(w)
        yield group

if __name__=='__main__':
    meter=Meter('core_gap_screen');rows=[];counter=[];total=0
    for n in range(3,9):
        ts=shapes(1,n);ids={t:i for i,t in enumerate(ts)}
        action=[[ids[ind.trace(t,x)[0]] for x in range(1,n+1)] for t in ts]
        checked=0;max_gap=0;max_record=None
        for size in range(2,min(4,n)+1):
            for M in combinations(range(1,n+1),size):
                es=[[action[i][x-1] for x in M] for i in range(len(ts))];rev=[[] for _ in ts]
                for i,vs in enumerate(es):
                    for v in vs:rev[v].append(i)
                for group in components(es,rev):
                    if len(group)==1:continue
                    G=set(group)
                    if not all(any(action[i][x-1] in G for i in group) for x in M):continue
                    checked+=1;i=group[0];S=set().union(*(path(ts[i],x) for x in M))
                    gap=max((sum(a<k<b for k in S) for a,b in zip(M,M[1:])),default=0)
                    if gap>max_gap:
                        max_gap=gap;max_record={'M':M,'state_index':i,'S':sorted(S),'component_size':len(group)}
                    if gap>1:
                        counter.append({'n':n,**max_record,'scope':'Finite recurrent B-state component; source word not yet extracted.'})
                        break
                if counter:break
            if counter:break
        rows.append({'n':n,'BST_states':len(ts),'active_sets_sizes':[2,min(4,n)],
            'recurrent_components_checked':checked,'maximum_observed_open_gap_core_keys':max_gap,'example':max_record})
        write('CORE_GAP_SCREEN.json',{'scope':'Finite B-state screen only; not a universal theorem or paired-source certificate.',
            'hypothesis':'At most one unrequested original core key between consecutive distinct KEEP targets in a B-closed period.',
            'rows':rows,'candidate_countercomponents':counter})
        print('SCREEN n',n,'recurrent',checked,'max gap',max_gap,flush=True)
        if counter:break
    meter.info.update(status='candidate countercomponent' if counter else 'finite pass only');meter.ok=True
