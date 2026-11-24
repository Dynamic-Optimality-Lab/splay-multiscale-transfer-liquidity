from base7 import *
from exp01_oracle import Tree
from coercion import coerce,advance
from sources7 import reflect
from collections import deque

def code(st):return (st['root'],)+tuple(x or 0 for k in range(1,len(st['children'])+1) for x in st['children'][str(k)])
def state(c):return {'root':c[0],'children':{str(k):[c[2*k-1] or None,c[2*k] or None] for k in range(1,(len(c)+1)//2)}}

def build():
    old=load(ROOT/'FRESH_SOURCE_CATALOG.json')[0];p=load(ROOT/'FRESH_PHYS_00.json');n=old['n'];bits={k:1<<(k-1) for k in range(1,n+1)};extreme=1|(1<<(n-1));bad=set()
    for d in p['doubles']:
        if tuple(d['parent']) in ((1,1),(4,1),(5,1)):
            assert not d['F']&extreme;bad.update((d['F'],d['J'],d['P_output']))
    assert bad and all(z and not z&extreme for z in bad)
    def probe(st,x):
        t=Tree(st)
        while t.par[x] is not None:
            pp=t.par[x];g=t.par[pp]
            if g is None:rot=[(pp,int(x>pp))]
            else:
                side=int(x>pp);direction=int(pp>g);rot=[(g,direction),(pp,side)] if side==direction else [(pp,side),(g,direction)]
            for u,side in rot:
                t.rotate(u,side)
                if set(t.labels(bits).values())&bad:return None
        return t.state()
    vine={'root':1,'children':{str(k):[None,k+1 if k<n else None] for k in range(1,n+1)}}
    initial=code(vine);parents={initial:None};queue=deque([initial]);goal=None;start=time.process_time()
    while queue:
        c=queue.popleft();st=state(c)
        if st['root']==9 and st['children']['5']==[None,None]:goal=c;break
        for x in range(1,n+1):
            if x==st['root']:continue
            nxt=probe(st,x)
            if nxt is None:continue
            cc=code(nxt)
            if cc not in parents:parents[cc]=(c,x);queue.append(cc)
        assert len(parents)<=58786 and time.process_time()-start<=300,'Bounded protected closure synthesis failed; preserve attempt.'
    write('PROTECTED_SYNTHESIS.json',{'states_visited':len(parents),'cpu_seconds':time.process_time()-start,'goal_found':goal is not None,'protected_labels':sorted(bad)})
    assert goal is not None,'No protected closed starting state with fixed leaf found.'
    opening=[];c=goal
    while parents[c] is not None:c,x=parents[c];opening.append(x)
    opening.reverse();a0=state(goal);a=Tree(a0);word=[];mapping=[];stats=Counter()
    assert not set(a.labels(bits).values())&bad
    def perform(tag,x):
        nonlocal a
        while True:
            st=probe(a.state(),x)
            if st is not None:word.append([tag,x]);a=Tree(st);break
            path=a.path(x);assert len(path)>3;helper=path[2];before=len(path);st=probe(a.state(),helper);assert st is not None
            word.append(['D',helper]);a=Tree(st);assert len(a.path(x))<before;stats['helpers']+=1
    ks=[x for tag,x in old['operations'] if tag=='K']
    for j,x in enumerate(ks,1):perform('K',x);mapping.append([j,len(word)])
    for x in range(n,0,-1):perform('D',x)
    assert a.state()==vine
    for x in opening:perform('D',x)
    assert a.state()==a0
    reach,rstats=coerce(old['initial_B'],a0);mp=dict(mapping)
    result={**old,'name':'M1C7_protected_merge_kernel11','family':'outside_attachment_two_side_merge_kernel','initial_A':a0,
        'reaching_prefix':[['D',x] for x in reach],'operations':word,'protected_labels':sorted(bad),'safe_closure_opening':opening,
        'original_KEEP_mapping':mapping,'planner_statistics':dict(stats),'prefix_stats':rstats,
        'A_return_stats':{'method':'Protected descending A closure to full right vine, then the recorded safe opening word.','descending_targets':n,'opening_word':opening},
        'producer_operation':mp[1],'right_inside_operation':mp[4],'critical_operation':mp[5],
        'scope':'All chosen internal F/J/P labels of the three kernel doubles are physically A-absent throughout the full measured word. Original R6/C_old still tested, not assumed.'}
    assert advance(a0,[x for tag,x in word])[0]==a0 and advance(result['initial_B'],[x for tag,x in word if tag=='K'])[0]==result['initial_B']
    return result

if __name__=='__main__':
    unsealed();m=Meter('protected_kernel_synthesis');s=build();out=[s,reflect(s)];write('PROTECTED_SOURCE_CATALOG.json',out)
    m.info['fresh_complete_sources']=2;m.ok=True;print('PASS protected complete sources',[(s['name'],len(s['operations'])) for s in out],flush=True)
