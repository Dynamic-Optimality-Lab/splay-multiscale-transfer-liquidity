"""Fresh bounded original-source audit and exact fixed-policy optimizer.

No old producer is called. The independent checker imports none of this code.
"""
import gzip
import json
import math
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
START = time.process_time()
TOTAL = 0


class Tree:
    def __init__(self, n, reflected=False):
        self.n = n
        self.root = n if reflected else 1
        self.left = [0]*(n+1)
        self.right = [0]*(n+1)
        self.parent = [0]*(n+1)
        self.lo = list(range(n+1))
        self.hi = list(range(n+1))
        for x in range(1, n+1):
            if reflected:
                self.left[x] = x-1
                self.parent[x] = x+1 if x<n else 0
                self.lo[x] = 1
            else:
                self.right[x] = x+1 if x<n else 0
                self.parent[x] = x-1
                self.hi[x] = n

    def rotate(self, x):
        p = self.parent[x]
        g = self.parent[p]
        old = (self.lo[x], self.hi[x])
        if self.left[p] == x:
            middle = self.right[x]
            self.left[p] = middle
            self.right[x] = p
        else:
            assert self.right[p] == x
            middle = self.left[x]
            self.right[p] = middle
            self.left[x] = p
        if middle:
            self.parent[middle] = p
        self.parent[p] = x
        self.parent[x] = g
        if not g:
            self.root = x
        elif self.left[g] == p:
            self.left[g] = x
        else:
            assert self.right[g] == p
            self.right[g] = x
        for k in (p,x):
            self.lo[k] = self.lo[self.left[k]] if self.left[k] else k
            self.hi[k] = self.hi[self.right[k]] if self.right[k] else k
        return p, old, (self.lo[p], self.hi[p])

    def closed(self, reflected):
        order = range(self.n,0,-1) if reflected else range(1,self.n+1)
        x = self.root
        for k in order:
            assert x == k
            assert (self.right[x] if reflected else self.left[x]) == 0
            x = self.left[x] if reflected else self.right[x]
        assert not x


def source(p,q,reflected):
    n = 2**(p+1)*(q+1)+1
    keep = {n+1-2**j for j in range(p+1)}
    word = [('prep','D',x) for x in range(2,n+1)]
    word += [('critical','K' if x in keep else 'D',x) for x in range(n,0,-1)]
    word += [('forward','K',x) for x in range(1,n+1)]
    word += [('reverse','K',x) for x in range(n-1,0,-1)]
    if reflected:
        word = [(phase,mode,n+1-x) for phase,mode,x in word]
    return n,word


def present(lab,root,n):
    a,b = lab
    return lab == (1,n) or a == 1 and b < root or b == n and a > root


def cover(lab,root,n):
    a,b = lab
    return (a,n) if root < a else (1,b) if root > b else (1,n)


def flow(donors,capacity):
    """Integral Dinic; a returned assignment is independently checked."""
    units = sorted({tuple(a) for ns in donors for a in ns})
    lookup = {a:i for i,a in enumerate(units)}
    m,r = len(donors),len(units)
    src,sink = m+r,m+r+1
    graph = [[] for _ in range(sink+1)]
    def edge(u,v,c):
        graph[u].append([v,c,len(graph[v])])
        graph[v].append([u,0,len(graph[u])-1])
    for d,ns in enumerate(donors):
        edge(src,d,1)
        for a in ns:
            edge(d,m+lookup[tuple(a)],1)
    for a in range(r):
        edge(m+a,sink,capacity)
    value = 0
    while True:
        levels = [-1]*len(graph)
        levels[src] = 0
        queue = deque([src])
        while queue:
            u = queue.popleft()
            for v,c,_ in graph[u]:
                if c and levels[v]<0:
                    levels[v] = levels[u]+1
                    queue.append(v)
        if levels[sink]<0:
            break
        ptr = [0]*len(graph)
        def dfs(u,amount):
            if u == sink:
                return amount
            while ptr[u]<len(graph[u]):
                e = graph[u][ptr[u]]
                v,c,rev = e
                if c and levels[v] == levels[u]+1:
                    sent = dfs(v,min(amount,c))
                    if sent:
                        e[1] -= sent
                        graph[v][rev][1] += sent
                        return sent
                ptr[u] += 1
            return 0
        while True:
            sent = dfs(src,10**9)
            if not sent:
                break
            value += sent
    assignment = []
    for d in range(m):
        for v,c,_ in graph[d]:
            if m <= v < m+r and c == 0:
                assignment.append([d,list(units[v-m])])
    return value,assignment


def run(p,q,reflected):
    global TOTAL
    n,word = source(p,q,reflected)
    trees = {a:Tree(n,reflected) for a in ('A','B')}
    bset = {(1,k) if reflected else (k,n) for k in range(1,n+1)}
    events,rows,doubles = [],[],[]
    births,deaths,achanges = defaultdict(list),defaultdict(list),defaultdict(list)
    clock = A = Q = psi = 0
    for op,(phase,mode,target) in enumerate(word,1):
        clock += 1
        ac = qc = 0
        for actor in ('A','B') if mode=='K' else ('A',):
            if actor == 'B':
                clock += 1
                postA = clock
            tree = trees[actor]
            step = 0
            while tree.parent[target]:
                step += 1
                pr = tree.parent[target]
                gp = tree.parent[pr]
                if gp:
                    side0 = 'L' if tree.left[gp] == pr else 'R'
                    side1 = 'L' if tree.left[pr] == target else 'R'
                    typ = side0+side1
                    frame = (tree.lo[gp],tree.hi[gp])
                    pivots = (pr,target) if side0==side1 else (target,target)
                else:
                    typ,frame,pivots = 'ZIG',None,(target,)
                if actor=='A':
                    A += 1; ac += 1
                    assert typ == 'ZIG' and step == 1 and abs(target-pr)==1
                elif gp:
                    Q += 1; qc += 1
                signs = []
                for bit,pivot in enumerate(pivots):
                    clock += 1
                    TOTAL += 1
                    assert TOTAL <= 500000 and time.process_time()-START <= 240
                    demoted,lost,born = tree.rotate(pivot)
                    identifier = [actor,op,step,bit]
                    e = {'id':identifier,'clock':clock,'type':typ,'target':target,
                         'promoted':pivot,'demoted':demoted,'removed':lost,'created':born}
                    if actor=='A':
                        delta = int(lost in bset)-int(born in bset)
                        achanges[lost].append((clock,False,identifier))
                        achanges[born].append((clock,True,identifier))
                        e['old_root'],e['new_root'] = pr,target
                    else:
                        delta = -int(present(born,trees['A'].root,n))
                        assert lost[0] <= target <= lost[1] and not born[0] <= target <= born[1]
                        e['psi_delta'] = delta
                        signs.append(delta)
                        assert lost in bset and born not in bset
                        bset.remove(lost); bset.add(born)
                        births[born].append((clock,identifier))
                        deaths[lost].append((clock,identifier))
                    e['psi_delta'] = delta
                    psi += delta
                    assert psi >= 0
                    events.append(e)
                if actor=='B' and frame is not None:
                    doubles.append({'id':[op,step],'frame':frame,'type':typ,
                                    'postA_clock':postA,'neutral':signs==[0,0]})
        if mode!='K':
            clock += 1
            postA = clock
        clock += 1
        rows.append({'op':op,'a':ac,'q_B':qc,'postA_clock':postA,'end_clock':clock})
    for t in trees.values():
        t.closed(reflected)
    assert A == 4*(n-1) and psi == 0
    period = clock
    kinds = Counter()
    alpha,beta = [],[]
    for d in doubles:
        if not d['neutral']:
            d['class'] = 'nonneutral'; kinds[d['class']] += 1
            continue
        lab,end = d['frame'],d['postA_clock']
        assert lab != (1,n)
        gamma,gid = max((c+lap*period,eid) for c,eid in births[lab] for lap in (-1,0) if c+lap*period<end)
        kap,kid = max((c+lap*period,eid) for c,eid in deaths[lab] for lap in (-2,-1,0) if c+lap*period<gamma)
        assert 0 < end-kap <= period
        d.update(Gamma=gid,Gamma_clock=gamma,kappa=kid,kappa_clock=kap)
        creations = [(c+lap*period,eid) for c,flag,eid in achanges[lab] for lap in (-1,0) if flag and kap<c+lap*period<=end]
        if creations:
            ca,aid = max(creations)
            cb,bid = min((c+lap*period,eid) for c,flag,eid in achanges[lab] for lap in (-1,0) if not flag and ca<c+lap*period<=end)
            d['class'] = 'exposed'; d['alpha'],d['beta'] = aid,bid
            alpha.append(tuple(aid)); beta.append(tuple(bid))
        else:
            d['class'] = 'U_bd' if lab[0]==1 or lab[1]==n else 'U_int'
        kinds[d['class']] += 1
    assert len(alpha)==len(set(alpha)) and len(beta)==len(set(beta))
    D_B = -sum(e['psi_delta'] for e in events if e['id'][0]=='B')
    K_B = len({e['id'][1] for e in events if e['id'][0]=='B'})
    P_A,N_A,T_A = (sum(e['psi_delta']==v for e in events if e['id'][0]=='A') for v in (1,-1,0))
    assert P_A-N_A == D_B and P_A+N_A+T_A == A
    assert kinds['nonneutral'] <= D_B <= 2*A
    assert kinds['exposed'] <= len([e for e in events if e['id'][0]=='A']) <= 2*A
    assert kinds['U_bd'] <= 2*K_B <= 2*A
    assert Q <= 6*A+kinds['U_int']
    byid = {tuple(d['id']):d for d in doubles}
    selected,donors = [],[]
    aevents = [e for e in events if e['id'][0]=='A']
    for j in range(1,p+1):
        for i in range(1,q+1):
            a = n+2-2**(p+1)*(i+1)
            b = n-2**(j-1)
            lab = (a,b) if not reflected else (n+1-b,n+1-a)
            ident = (n-1+2**j,2**(p-j)*(i+1)-1)
            d = byid[ident]
            assert d['frame']==lab and d['class']=='U_int'
            ns = [e['id'] for e in aevents if cover(lab,e['old_root'],n)!=cover(lab,e['new_root'],n)]
            assert len(ns)==8
            selected.append({'id':ident,'i':i,'j':j,'frame':lab,'Gamma':d['Gamma'],'kappa':d['kappa'],'donors':ns})
            donors.append(ns)
    neighbors = {tuple(a) for ns in donors for a in ns}
    assert len(neighbors) == 4*(p+q)
    optimal = math.ceil(p*q/(4*(p+q)))
    value,assignment = flow(donors,optimal)
    assert value == p*q
    if optimal>1:
        failed,_ = flow(donors,optimal-1)
        assert failed < p*q
    result = {'p':p,'q':q,'reflected':reflected,'n':n,'length':len(word),'A':A,'Q_B':Q,
              'partition':dict(kinds),'D_B':D_B,'K_B':K_B,'P_A':P_A,'N_A':N_A,'T_A':T_A,'real_rotations':len(events),
              'selected_demand_count':p*q,'neighbor_A_units':len(neighbors),
              'optimal_capacity':optimal,'assignment':assignment,'selected':selected,
              'policy':'All A StepEv units changing the minimal S-cover of this original whole frame, anywhere in W; cost one per StepEv.'}
    full = {'source':{'family':'H_pq','p':p,'q':q,'reflected':reflected,'n':n,'prefix':[],'initial':'full left vine' if reflected else 'full right vine','word':word},
            'period_clock':period,'rows':rows,'real_rotations':events,'all_B_double_records':doubles,'result':result}
    name = f'H_p{p}_q{q}'+('_mirror' if reflected else '')
    with gzip.open(HERE/(name+'.json.gz'),'wt',encoding='utf-8') as f:
        json.dump(full,f,separators=(',',':'))
    print(json.dumps({k:result[k] for k in ('p','q','reflected','n','A','Q_B','real_rotations','selected_demand_count','neighbor_A_units','optimal_capacity')}),flush=True)
    return {k:v for k,v in result.items() if k not in ('assignment','selected')}


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    spec = json.loads((HERE/'EXPERIMENT_SPEC.json').read_text())
    results = [run(*c) for c in spec['cases']]
    (HERE/'FINITE_OPTIMIZATION.json').write_text(json.dumps({'cases':results,'total_real_rotations':TOTAL,'producer_cpu_seconds':time.process_time()-START},indent=2))


if __name__=='__main__':
    main()
