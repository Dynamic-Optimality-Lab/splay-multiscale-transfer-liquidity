"""Mutable full physical BST replay with original carrier and full cyclic Pi."""
import bisect
from collections import Counter,defaultdict


class Tree:
    def __init__(self,state,support):
        self.keys=sorted(map(int,state['children']))
        self.ch={int(k):list(v) for k,v in state['children'].items()}
        self.root=state['root'];self.parent={k:None for k in self.keys}
        self.support=list(support);self.rank={k:i+1 for i,k in enumerate(support)}
        for k,cs in self.ch.items():
            for c in cs:
                if c is not None:
                    assert self.parent[c] is None;self.parent[c]=k
        assert self.parent[self.root] is None
        self.lo={};self.hi={};self.sl={};self.sh={};self.counts=Counter()
        stack=[(self.root,False)];seen=set()
        while stack:
            k,done=stack.pop()
            if done:
                self.update(k)
                if self.label(k):self.counts[self.label(k)]+=1
            else:
                assert k not in seen;seen.add(k);stack.append((k,True))
                stack.extend((c,False) for c in self.ch[k] if c is not None)
        assert seen==set(self.keys)
        assert self.lo[self.root]==self.keys[0] and self.hi[self.root]==self.keys[-1]

    def label(self,k):
        return (self.sl[k],self.sh[k]) if self.sl.get(k) else None

    def update(self,k):
        l,r=self.ch[k]
        self.lo[k]=self.lo[l] if l is not None else k
        self.hi[k]=self.hi[r] if r is not None else k
        own=self.rank.get(k)
        self.sl[k]=next((z for z in [self.sl.get(l),own,self.sl.get(r)] if z is not None),None)
        self.sh[k]=next((z for z in [self.sh.get(r),own,self.sh.get(l)] if z is not None),None)

    def state(self):
        return {'root':self.root,'children':{str(k):list(self.ch[k]) for k in self.keys}}

    def path(self,x):
        p=[];k=self.root
        while True:
            assert k is not None;p.append(k)
            if k==x:return p
            k=self.ch[k][x>k]

    def rotate(self,x):
        p=self.parent[x];g=self.parent[p]
        assert p is not None
        C,H=self.label(x),self.label(p)
        old_span=(self.lo[x],self.hi[x])
        side=int(self.ch[p][1]==x);middle=self.ch[x][1-side]
        self.ch[p][side]=middle
        if middle is not None:self.parent[middle]=p
        self.ch[x][1-side]=p;self.parent[p]=x;self.parent[x]=g
        if g is None:self.root=x
        else:self.ch[g][int(self.ch[g][1]==p)]=x
        self.update(p);self.update(x)
        D=self.label(p);new_span=(self.lo[p],self.hi[p])
        candidates={z for z in (C,D) if z is not None}
        before={z:self.counts[z] for z in candidates}
        if C is not None:self.counts[C]-=1
        if D is not None:self.counts[D]+=1
        assert all(self.counts[z]>=0 for z in candidates)
        lost=[z for z in candidates if before[z]>0 and self.counts[z]==0]
        born=[z for z in candidates if before[z]==0 and self.counts[z]>0]
        assert len(lost)<=1 and len(born)<=1
        return {'p':x,'g':p,'Cspan':old_span,'Dspan':new_span,'CH_different':C!=H,'DH_different':D!=H,
                'lost':lost,'born':born}


def plain(tree,target):
    total=0
    while tree.parent[target] is not None:
        p=tree.parent[target];g=tree.parent[p]
        if g is None:pivots=[target]
        else:pivots=[p,target] if (p<g)==(target<p) else [target,target]
        for x in pivots:tree.rotate(x);total+=1
    return total


def carrier(source):
    root=source['initial_B']['root'];genuine=set()
    for mode,x in source['operations']:
        if mode=='K':
            if root!=x:genuine.add(x)
            root=x
    init=Tree(source['initial_B'],[]);support=set()
    for x in genuine:support.update(init.path(x))
    return sorted(support)


def eligible(bit,a,b):
    p,g=bit['p'],bit['g']
    if a<=p<=b and a<=g<=b:return True
    lo,hi=bit['Cspan']
    if bit['CH_different'] and a<=p<=b and lo<=a and b<=hi:return True
    lo,hi=bit['Dspan']
    return bit['DH_different'] and a<=g<=b and lo<=a and b<=hi


def replay(source,limits=None):
    keys=sorted(map(int,source['initial_A']['children']))
    assert keys==sorted(map(int,source['initial_B']['children']))
    reach_rot=0
    if source.get('diagonal') is not None:
        reach={a:Tree(source['diagonal'],keys) for a in ('A','B')}
        for mode,x in source['prefix']:
            reach_rot+=plain(reach['A'],x)
            if mode=='K':reach_rot+=plain(reach['B'],x)
        assert reach['A'].state()==source['initial_A'] and reach['B'].state()==source['initial_B']
    else:
        assert source['initial_A']==source['initial_B'] and not source['prefix']
    support=carrier(source);full=len(support);full_carrier=support==keys
    trees={a:Tree(source['initial_'+a],support) for a in ('A','B')}
    initial_A={z for z,v in trees['A'].counts.items() if v}
    birth,death,achanges=defaultdict(list),defaultdict(list),defaultdict(list)
    events=[];units=[];doubles=[];clock=A=Q=R=0;psi=0
    for op,(mode,target) in enumerate(source['operations'],1):
        clock+=1
        for actor in ('A','B') if mode=='K' else ('A',):
            if actor=='B':clock+=1;postA=clock
            tree=trees[actor];step=0
            if actor=='B' and tree.parent[target] is not None:assert set(tree.path(target))<=set(support)
            while tree.parent[target] is not None:
                step+=1;p=tree.parent[target];g=tree.parent[p]
                if g is None:typ='ZIG';pivots=[target];frame=None
                else:
                    typ=('L' if p<g else 'R')+('L' if target<p else 'R')
                    pivots=[p,target] if typ in ('LL','RR') else [target,target]
                    frame=tree.label(g)
                if actor=='A':A+=1;unit={'id':['A',op,step,0],'bits':[]};units.append(unit)
                elif g is not None:Q+=1
                signs=[]
                for bit,pivot in enumerate(pivots):
                    clock+=1;R+=1
                    b=tree.rotate(pivot);identifier=[actor,op,step,bit]
                    fixed=trees['B' if actor=='A' else 'A']
                    if actor=='A':
                        delta=sum(fixed.counts[z]>0 for z in b['lost'])-sum(fixed.counts[z]>0 for z in b['born'])
                        for z in b['lost']:achanges[z].append((clock,False,identifier))
                        for z in b['born']:achanges[z].append((clock,True,identifier))
                        unit['bits'].append(b)
                    else:
                        assert len(b['lost'])==len(b['born'])==1
                        out=b['born'][0];delta=-int(fixed.counts[out]>0)
                        birth[out].append((clock,identifier));death[b['lost'][0]].append((clock,identifier))
                        assert delta in (0,-1)
                    signs.append(delta)
                    if limits is not None:limits(R,reach_rot)
                if actor=='B' and frame is not None:
                    doubles.append({'id':[op,step],'F':frame,'neutral':signs==[0,0],'postA':postA})
        if mode!='K':clock+=1
        clock+=1
    assert trees['A'].state()==source['initial_A'] and trees['B'].state()==source['initial_B']
    if source.get('expected_A') is not None:assert A==source['expected_A'],(source['name'],A,source['expected_A'])
    if source.get('expected_Q') is not None:assert Q==source['expected_Q'],(source['name'],Q,source['expected_Q'])
    period=clock
    def prev(seq,end):
        lap,local=divmod(end,period);i=bisect.bisect_left([t for t,_ in seq],local)-1
        if i<0:lap-=1;i=len(seq)-1
        t,eid=seq[i];return t+lap*period,eid
    demands=[]
    for d in doubles:
        F=d['F']
        if not d['neutral'] or F[0]<=1 or F[1]>=full:continue
        end=d['postA'];gamma,gid=prev(birth[F],end);kap,kid=prev(death[F],gamma)
        assert 0<end-kap<=period
        local=kap%period;i=bisect.bisect_right([t for t,_,_ in achanges[F]],local)-1
        present=achanges[F][i][1] if i>=0 else F in initial_A
        exposure=present or any(flag and kap<t+lap*period<=end for t,flag,_ in achanges[F] for lap in (-1,0))
        if not exposure:
            demands.append({'id':d['id'],'span':[support[F[0]-1],support[F[1]-1]],'F':F,'Gamma':gid,'Gamma_clock':gamma,'kappa':kid,'kappa_clock':kap,'postA':end})
    root_only=all(min(bit['Cspan'][0],bit['Dspan'][0])==keys[0] and max(bit['Cspan'][1],bit['Dspan'][1])==keys[-1] for u in units for bit in u['bits'])
    return {'source':source,'S':support,'keys':keys,'full_carrier':full_carrier,'root_rotations_only':root_only,'A':A,'Q_B':Q,'rotations':R,'reach_rotations':reach_rot,'period_clock':period,'units':units,'demands':demands}
