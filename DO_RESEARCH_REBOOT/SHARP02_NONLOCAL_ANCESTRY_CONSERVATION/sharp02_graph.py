"""Exact grouped integral flows, nonempty Hall minima and reservation exchange."""
from collections import defaultdict,deque
from itertools import combinations

class Network:
    def __init__(self,n):self.g=[[] for _ in range(n)]
    def edge(self,u,v,c):
        a=[v,len(self.g[v]),c,c];b=[u,len(self.g[u]),0,0]
        self.g[u].append(a);self.g[v].append(b);return a
    def flow(self,s,t):
        result=0
        while True:
            level=[-1]*len(self.g);level[s]=0;q=deque([s])
            while q:
                u=q.popleft()
                for v,rev,c,old in self.g[u]:
                    if c and level[v]<0:level[v]=level[u]+1;q.append(v)
            if level[t]<0:break
            it=[0]*len(self.g)
            def dfs(u,amt):
                if u==t:return amt
                while it[u]<len(self.g[u]):
                    e=self.g[u][it[u]];v,rev,c,old=e
                    if c and level[v]==level[u]+1:
                        moved=dfs(v,min(c,amt))
                        if moved:e[2]-=moved;self.g[v][rev][2]+=moved;return moved
                    it[u]+=1
                return 0
            while True:
                moved=dfs(s,10**18)
                if not moved:break
                result+=moved
        return result
    def reachable(self,s):
        seen={s};q=[s]
        for u in q:
            for v,rev,c,old in self.g[u]:
                if c and v not in seen:seen.add(v);q.append(v)
        return seen

def solve(weights,adj,units,group_capacity=None,tight=True):
    """units is index->physical unit. group_capacity=None means fixed free units.
    With per-gap c, units contains ALL original units and the gap partition
    permits optimized choice of c free units. No source matching is assumed.
    """
    weights={str(k):v for k,v in weights.items() if v};adj={str(k):set(v) for k,v in adj.items()}
    names=list(weights);total=sum(weights.values())
    if not names:return {'demand':0,'flow':0,'unmatched':0,'tight_nonempty_margin':None,'tight_subset':[],
                          'deficient_subset':[],'assignment':[],'neighbor_units':{},'vacuous':True}
    memberships=defaultdict(list)
    for i in names:
        for j in adj.get(i,()):memberships[j].append(i)
    patterns=defaultdict(list)
    for j,ii in memberships.items():
        key=(tuple(sorted(ii)),units[j]['gap_index'] if group_capacity is not None else None)
        patterns[key].append(j)
    groups=list(patterns.items());di={i:k+1 for k,i in enumerate(names)}
    po=1+len(names);gaps={} if group_capacity is None else {j:po+len(groups)+k for k,j in enumerate(group_capacity)}
    sink=po+len(groups)+len(gaps);INF=total+len(units)+1
    def build(force=None,assign=False):
        net=Network(sink+1);refs=[]
        for i,w in weights.items():net.edge(0,di[i],w)
        if force is not None:net.edge(0,di[force],INF)
        for k,((ii,gap),js) in enumerate(groups):
            for i in ii:refs.append((i,k,net.edge(di[i],po+k,INF)))
            net.edge(po+k,sink if group_capacity is None else gaps[gap],len(js))
        if group_capacity is not None:
            for j,gn in gaps.items():net.edge(gn,sink,group_capacity[j])
        f=net.flow(0,sink);reach=net.reachable(0);ds=[i for i in names if di[i] in reach]
        assignment=[]
        if assign:
            pools=[list(js) for key,js in groups]
            for i,k,e in refs:
                used=e[3]-e[2]
                for _ in range(used):assignment.append([i,pools[k].pop(),1])
        return f,ds,assignment
    f,ds,assignment=build(assign=True)
    def neighbor(D):return set().union(*(adj.get(i,set()) for i in D)) if D else set()
    def capacity(D):
        ns=neighbor(D)
        if group_capacity is None:return len(ns)
        counts=defaultdict(int)
        for j in ns:counts[units[j]['gap_index']]+=1
        return sum(min(group_capacity[g],c) for g,c in counts.items())
    def margin(D):return capacity(D)-sum(weights[i] for i in D)
    best=None;bestD=[]
    if tight:
        # Exact minimum over NONEMPTY subsets, including a positive margin.
        # Forcing each demand to the source side covers every nonempty set.
        for i in names:
            ff,dd,_=build(force=i);m=ff-total
            assert i in dd and m==margin(dd)
            if best is None or m<best:best=m;bestD=dd
    minimum=False
    if f<total:
        assert ds and margin(ds)<0
        for i in list(ds):
            trial=[j for j in ds if j!=i]
            if margin(trial)<0:ds=trial
        if len(names)<=14:
            for k in range(1,len(names)+1):
                found=next((list(D) for D in combinations(names,k) if margin(D)<0),None)
                if found is not None:ds=found;minimum=True;break
    else:ds=[]
    consumed=defaultdict(int);paid=defaultdict(int)
    for i,j,n in assignment:consumed[j]+=n;paid[i]+=n;assert j in adj[i]
    assert all(v==1 for v in consumed.values()) and all(v<=weights[i] for i,v in paid.items())
    if group_capacity is not None:
        use=defaultdict(int)
        for j,n in consumed.items():use[units[j]['gap_index']]+=n
        assert all(v<=group_capacity[g] for g,v in use.items())
    return {'demand':total,'flow':f,'unmatched':total-f,'tight_nonempty_margin':best,'tight_subset':bestD,
            'deficient_subset':ds,'deficiency':-margin(ds) if ds else 0,'deficient_neighbor_units':sorted(neighbor(ds)),
            'minimum_cardinality_deficient_set':minimum,'assignment':assignment,'vacuous':False,
            'neighbor_units':{i:len(adj.get(i,())) for i in names},'compressed_resource_patterns':len(groups)}

def graph_data(ledger):
    events={tuple(e['id']):e for e in ledger['events']};by_step=defaultdict(list)
    for e in ledger['events']:
        if e['id'][0]=='A':by_step[tuple(e['id'][:3])].append(e)
    units={};free={};gaps=ledger['gaps'];caps={};uid=0
    for g in gaps:
        reserve=min(g['q'],2*g['p']);caps[g['gap_index']]=g['c'];seq=[]
        for sid in g['A_StepEv_ids']:
            ee=by_step[tuple(sid)]
            for bit in range(2):
                e=ee[min(bit,len(ee)-1)];y,xx=e['ancestry_added']
                u={'id':sid+[bit],'gap_index':g['gap_index'],'rotation_witness':e['id'],
                   'virtual':bit==1 and len(ee)==1,'created_ancestor':y,'created_targets':xx,
                   'reserved_chronological':len(seq)<reserve}
                units[uid]=u
                if len(seq)>=reserve:free[uid]=u
                seq.append(uid);uid+=1
        assert len(seq)-reserve==g['c']
    weights={str(g['gap_index']):g['u'] for g in gaps if g['u']};adj={};alladj={};token_models={m:({}, {}) for m in ('outermost','innermost','extra_double')};tokens={}
    for g in gaps:
        if not g['u']:continue
        i=str(g['gap_index']);x=g['target'];Y=set(g['B_only_ancestors'])
        assert len(Y)>=2*g['u']+2*g['p']
        def eligible(us,yy):return {j for j,u in us.items() if u['created_ancestor'] in yy and x in u['created_targets']}
        adj[i]=eligible(free,Y);alladj[i]=eligible(units,Y)
        ordered=[y for y in g['B_path'][:-1] if y in Y]
        tok_lists={'outermost':ordered[:g['u']],'innermost':ordered[-g['u']:],'extra_double':[]}
        for sid in g['B_double_ids'][2*g['p']:]:
            e0=events[tuple(sid+[0])];e1=events[tuple(sid+[1])]
            pair=[e0['pivot'],e0['promoted']] if e0['case'] in ('RR','LL') else [e1['pivot'],e0['pivot']]
            tok_lists['extra_double'].append(next((v for v in pair if v in Y),None))
        assert len(tok_lists['extra_double'])==g['u']
        for mode,ys in tok_lists.items():
            ww,aa=token_models[mode]
            for k,y in enumerate(ys):
                tid=f'{i}:{k+1}';ww[tid]=1;aa[tid]=eligible(free,{y}) if y is not None else set()
                tokens[f'{mode}:{tid}']={'gap_index':g['gap_index'],'target':x,'ancestor':y,
                    'physical_explanation':'specific B-only ancestor' if y is not None else 'extra double has no B-only original path pivot'}
    return {'weights':weights,'adj':adj,'all_adj':alladj,'units':units,'free':free,'capacities':caps,'token_models':token_models,'tokens':tokens}
