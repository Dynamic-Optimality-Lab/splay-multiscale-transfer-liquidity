"""Exact original-unit flow; range graph is an index, not extra A credit."""
import bisect
from collections import defaultdict,deque,Counter
from replay import eligible


class Network:
    def __init__(self):self.g=[]
    def node(self):self.g.append([]);return len(self.g)-1
    def add(self,u,v,c):
        self.g[u].append([v,c,len(self.g[v]),c])
        self.g[v].append([u,0,len(self.g[u])-1,0])
    def maxflow(self,s,t):
        value=0;g=self.g
        while True:
            level=[-1]*len(g);level[s]=0;q=deque([s])
            while q:
                u=q.popleft()
                for v,c,_,_ in g[u]:
                    if c and level[v]<0:level[v]=level[u]+1;q.append(v)
            if level[t]<0:return value
            ptr=[0]*len(g)
            def send(u,a):
                if u==t:return a
                while ptr[u]<len(g[u]):
                    e=g[u][ptr[u]];v,c,rev,_=e
                    if c and level[v]==level[u]+1:
                        got=send(v,min(a,c))
                        if got:e[1]-=got;g[v][rev][1]+=got;return got
                    ptr[u]+=1
                return 0
            while True:
                got=send(s,10**12)
                if not got:break
                value+=got
    def reachable(self,s):
        seen={s};q=[s]
        for u in q:
            for v,c,_,_ in self.g[u]:
                if c and v not in seen:seen.add(v);q.append(v)
        return seen


def footprint(unit):return tuple(sorted({b[k] for b in unit['bits'] for k in ('p','g')}))


def key(unit,full):
    if full:return footprint(unit)
    return tuple((b['p'],b['g'],tuple(b['Cspan']),tuple(b['Dspan']),b['CH_different'],b['DH_different']) for b in unit['bits'])


def grouping(rep):
    ds=defaultdict(list);us=defaultdict(list)
    for i,d in enumerate(rep['demands']):ds[tuple(d['span'])].append(i)
    for u in rep['units']:us[key(u,rep['full_carrier'] and rep['root_rotations_only'])].append(u)
    return list(ds.items()),list(us.items())


def build(rep,K,groups):
    demands,units=groups;D=len(rep['demands']);infty=D+1
    net=Network();src=net.node();sink=net.node()
    dn=[net.node() for _ in demands];un=[net.node() for _ in units]
    for node,(_,ids) in zip(dn,demands):net.add(src,node,len(ids))
    for node,(_,members) in zip(un,units):net.add(node,sink,K*len(members))
    if rep['full_carrier'] and rep['root_rotations_only']:
        keys=rep['keys'];leaves={};seg={}
        def make(l,r):
            node=net.node();seg[node]=(l,r)
            if l==r:leaves[keys[l]]=node
            else:
                mid=(l+r)//2;left=make(l,mid);right=make(mid+1,r)
                seg[node]=(l,r,left,right);net.add(node,left,infty);net.add(node,right,infty)
            return node
        root=make(0,len(keys)-1)
        def link(d,node,l,r):
            a,b,*kids=seg[node]
            if l<=a and b<=r:net.add(d,node,infty);return
            if a==b:return
            mid=(a+b)//2
            if l<=mid:link(d,kids[0],l,r)
            if r>mid:link(d,kids[1],l,r)
        for node,((a,b),_) in zip(dn,demands):
            link(node,root,bisect.bisect_left(keys,a),bisect.bisect_right(keys,b)-1)
        for node,(fp,_) in zip(un,units):
            for x in fp:net.add(leaves[x],node,infty)
    else:
        # Exact range index on existing demand endpoints. A resource bit has
        # three eligibility rectangles. No point incidence assumption is used.
        xs=sorted({a for (a,b),_ in demands});outer={}
        def inner_make(values):
            nodes={}
            def rec(l,r):
                z=net.node()
                if l==r:nodes[z]=(l,r)
                else:
                    mid=(l+r)//2;left=rec(l,mid);right=rec(mid+1,r)
                    nodes[z]=(l,r,left,right);net.add(left,z,infty);net.add(right,z,infty)
                return z
            root=rec(0,len(values)-1)
            return values,nodes,root
        def outer_make(l,r,indices):
            values=sorted({demands[i][0][1] for i in indices})
            inner=inner_make(values);outer[(l,r)]=inner
            # Every actual point connects to its leaf in each ancestor's
            # secondary tree. All secondary edges point UP the range tree.
            leaves={values[data[0]]:node for node,data in inner[1].items() if data[0]==data[1]}
            for i in indices:net.add(dn[i],leaves[demands[i][0][1]],infty)
            if l<r:
                mid=(l+r)//2
                left=[i for i in indices if demands[i][0][0]<=xs[mid]]
                right=[i for i in indices if demands[i][0][0]>xs[mid]]
                if left:outer_make(l,mid,left)
                if right:outer_make(mid+1,r,right)
        outer_make(0,len(xs)-1,list(range(len(demands))))
        def inside_nodes(inner,low,high):
            values,nodes,root=inner
            lo=bisect.bisect_left(values,low);hi=bisect.bisect_right(values,high)-1
            if lo>hi:return []
            result=[]
            def visit(z):
                l,r,*kids=nodes[z]
                if lo<=l and r<=hi:result.append(z);return
                mid=(l+r)//2
                if lo<=mid:visit(kids[0])
                if hi>mid:visit(kids[1])
            visit(root);return result
        def rectangle(alo,ahi,blo,bhi):
            lo=bisect.bisect_left(xs,alo);hi=bisect.bisect_right(xs,ahi)-1
            if lo>hi:return []
            result=[]
            def visit(l,r):
                if (l,r) not in outer:return
                if lo<=l and r<=hi:result.extend(inside_nodes(outer[(l,r)],blo,bhi));return
                mid=(l+r)//2
                if lo<=mid:visit(l,mid)
                if hi>mid:visit(mid+1,r)
            visit(0,len(xs)-1);return result
        low,high=rep['keys'][0],rep['keys'][-1]
        for other,(_,members) in zip(un,units):
            ranges=set()
            for bit in members[0]['bits']:
                p,g=bit['p'],bit['g']
                ranges.update(rectangle(low,min(p,g),max(p,g),high))
                if bit['CH_different']:
                    clo,chi=bit['Cspan'];ranges.update(rectangle(clo,p,p,chi))
                if bit['DH_different']:
                    dlo,dhi=bit['Dspan'];ranges.update(rectangle(dlo,g,g,dhi))
            for z in ranges:net.add(z,other,infty)
    edges=sum(len(z) for z in net.g)
    assert edges<=2000000,('graph budget',edges)
    return net,src,sink,dn,un


def neighbors(rep,selected):
    spans=[rep['demands'][i]['span'] for i in selected]
    if not spans:return []
    if rep['full_carrier'] and rep['root_rotations_only']:
        merged=[]
        for a,b in sorted(spans):
            if merged and a<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],b)
            else:merged.append([a,b])
        starts=[a for a,_ in merged]
        def contains(x):
            i=bisect.bisect_right(starts,x)-1
            return i>=0 and x<=merged[i][1]
        return [u['id'] for u in rep['units'] if any(contains(x) for x in footprint(u))]
    return [u['id'] for u in rep['units'] if any(eligible(bit,a,b) for a,b in set(map(tuple,spans)) for bit in u['bits'])]


def optimize(rep):
    D=len(rep['demands'])
    if not D:return {'K':0,'assignment':[],'lower_cut':None,'graph_nodes':0,'graph_edges':0}
    groups=grouping(rep)
    def trial(K):
        n,s,t,dn,un=build(rep,K,groups);value=n.maxflow(s,t)
        return value,(n,s,t,dn,un)
    K=1;last_fail=0;lower=None
    while True:
        val,network=trial(K)
        if val==D:break
        n,s,t,dn,un=network;seen=n.reachable(s)
        selected=[i for node,(_,indices) in zip(dn,groups[0]) if node in seen for i in indices]
        ns=neighbors(rep,selected)
        assert len(selected)>K*len(ns)
        lower={'capacity':K,'demand_indices':selected,'neighbor_ids':ns,'deficiency':len(selected)-K*len(ns)}
        last_fail=K;K*=2
        assert K<=2*D,('nonempty-neighbor failure',rep['source']['name'])
    lo=last_fail+1;hi=K
    while lo<hi:
        mid=(lo+hi)//2;val,trialnet=trial(mid)
        if val==D:hi=mid;network=trialnet
        else:lo=mid+1
    K=lo
    val,network=trial(K);assert val==D
    if K>1:
        val,low_net=trial(K-1);assert val<D
        n,s,t,dn,un=low_net;seen=n.reachable(s)
        selected=[i for node,(_,indices) in zip(dn,groups[0]) if node in seen for i in indices]
        ns=neighbors(rep,selected)
        assert len(selected)>(K-1)*len(ns)
        lower={'capacity':K-1,'demand_indices':selected,'neighbor_ids':ns,'deficiency':len(selected)-(K-1)*len(ns)}
    n,s,t,dn,un=network;g=n.g;unit_node={node:i for i,node in enumerate(un)};ptr=[0]*len(g)
    used=Counter();assignment=[]
    def take(node):
        if node in unit_node:
            group=unit_node[node]
            e=next(e for e in g[node] if e[0]==t and e[3]>0)
            assert g[t][e[2]][1]>0;e[1]+=1;g[t][e[2]][1]-=1
            return group
        while ptr[node]<len(g[node]):
            e=g[node][ptr[node]];v,c,rev,original=e
            if original and g[v][rev][1]>0:
                chosen=take(v);e[1]+=1;g[v][rev][1]-=1;return chosen
            ptr[node]+=1
        raise AssertionError(('flow decomposition',node))
    for node,(_,indices) in zip(dn,groups[0]):
        for i in indices:
            group=take(node);members=groups[1][group][1]
            donor=members[used[group]//K];used[group]+=1
            assignment.append([i,donor['id']])
    assert len(assignment)==D
    return {'K':K,'assignment':assignment,'lower_cut':lower,'graph_nodes':len(g),'graph_edges':sum(len(z) for z in g)}


def interval_cut(rep,C=1):
    """Complete all-interval test for split pivot copies in full-carrier cases."""
    if not rep['full_carrier']:return None
    keys=rep['keys'];m=len(keys);counts=Counter(x for u in rep['units'] for x in footprint(u))
    prefix=[0]
    for x in keys:prefix.append(prefix[-1]+counts[x])
    size=4*m;value=[0]*size;lazy=[0]*size;arg=[0]*size
    def build(node,l,r):
        if l==r:value[node]=C*prefix[l];arg[node]=l;return
        mid=(l+r)//2;build(2*node,l,mid);build(2*node+1,mid+1,r);pull(node)
    def pull(node):
        child=2*node if value[2*node]>=value[2*node+1] else 2*node+1
        value[node]=value[child]+lazy[node];arg[node]=arg[child]
    def add(node,l,r,end,w):
        if r<=end:value[node]+=w;lazy[node]+=w;return
        mid=(l+r)//2;add(2*node,l,mid,end,w)
        if end>mid:add(2*node+1,mid+1,r,end,w)
        pull(node)
    def query(node,l,r,end,carry=0):
        if r<=end:return value[node]+carry,arg[node]
        carry+=lazy[node];mid=(l+r)//2;out=query(2*node,l,mid,end,carry)
        if end>mid:out=max(out,query(2*node+1,mid+1,r,end,carry))
        return out
    build(1,0,m-1);ending=defaultdict(Counter)
    for d in rep['demands']:
        a,b=d['span'];ending[bisect.bisect_left(keys,b)][bisect.bisect_left(keys,a)]+=1
    worst=None
    for r in range(m):
        for l,w in ending[r].items():add(1,0,m-1,l,w)
        score,l=query(1,0,m-1,r);gap=score-C*prefix[r+1]
        if worst is None or gap>worst['deficiency']:
            count=sum(l<=bisect.bisect_left(keys,d['span'][0]) and bisect.bisect_left(keys,d['span'][1])<=r for d in rep['demands']) if gap>0 else None
            worst={'C':C,'span':[keys[l],keys[r]],'deficiency':gap,'pivot_copies':prefix[r+1]-prefix[l],'contained_demands':count}
    return {'all_intervals_pass':worst['deficiency']<=0,'worst':worst,'total_pivot_copies':prefix[-1],
            'scope':'Exact split-resource theta_1 model only when all A rotations are at the physical global root; otherwise a pivot-incidence supergraph diagnostic.',
            'exact_for_theta_1_split_resources':rep['root_rotations_only']}
