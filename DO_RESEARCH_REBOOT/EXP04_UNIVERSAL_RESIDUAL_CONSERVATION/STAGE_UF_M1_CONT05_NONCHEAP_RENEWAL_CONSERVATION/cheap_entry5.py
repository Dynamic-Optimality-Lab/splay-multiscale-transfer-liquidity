from base5 import *
from sources4 import make as B_template
from coercion import coerce,advance,flatten
from sources3 import vine
from exp01_oracle import Tree
from collections import deque

def labels_kernel(B,targets):
    t=Tree(B);n=len(t.keys);bits={j:1<<(j-1) for j in t.keys};bad=set();extreme=1|(1<<(n-1));excluded=set()
    for x in targets:
        ds=[]
        while t.par[x] is not None:
            pp=t.par[x];g=t.par[pp];side=int(x>pp)
            if g is None:t.rotate(pp,side);continue
            z=int(pp>g);F=t.labels(bits)[g];ds.append((g,pp,F))
            for u,ss in ((g,z),(pp,side)) if side==z else ((pp,side),(g,z)):t.rotate(u,ss)
        labs=t.labels(bits)
        for g,pp,F in ds:
            if not F&extreme:
                for lab in (F,labs[g],labs[pp]):
                    if lab&2:excluded.add(lab)
                    else:bad.add(lab)
    return bad,excluded

def make(s,mode='half',protect=True):
    template=B_template(s,mode);n=template['n'];b=s+5;x=b-1
    B=template['initial_B'];ks=[z for tag,z in template['operations'] if tag=='K']+[n]
    ch={str(j):[None,None] for j in range(1,n+1)};ch[str(b)][0]=1;ch['1'][1]=x
    for j in range(3,x+1):ch[str(j)][0]=j-1
    for j in range(b,n):ch[str(j)][1]=j+1
    A1={'root':b,'children':ch};A0=advance(A1,[1])[0];assert advance(A0,[b])[0]==A1
    bad,excluded=labels_kernel(B,ks[:3]);bad=bad if protect else set();bits={j:1<<(j-1) for j in range(1,n+1)}
    a=Tree(A0);ops=[];stats=Counter();assert not bad.intersection(a.labels(bits).values())
    def trial(state,target):
        t=Tree(state)
        while t.par[target] is not None:
            pp=t.par[target];g=t.par[pp]
            if g is None:rot=[(pp,int(target>pp))]
            else:
                side=int(target>pp);z=int(pp>g);rot=[(g,z),(pp,side)] if side==z else [(pp,side),(g,z)]
            for u,ss in rot:
                t.rotate(u,ss)
                if bad.intersection(t.labels(bits).values()):return None
        return t
    def perform(tag,target):
        nonlocal a
        while True:
            t=trial(a.state(),target)
            if t is not None:ops.append([tag,target]);a=t;return
            path=a.path(target);assert len(path)>3
            h=path[2];t=trial(a.state(),h);assert t is not None
            before=len(path);ops.append(['D',h]);a=t;stats['safe_shallow_helpers']+=1;assert len(a.path(target))<before
    mapping=[]
    for j,target in enumerate(ks,1):perform('K',target);mapping.append([j,len(ops)])
    # Safe universal closure to a known vine, BEFORE the final B KEEP.
    for target in range(n,0,-1):perform('D',target)
    assert a.state()==vine(n,1)
    todo=[(u,ss) for u,ss,v in flatten(a.state())]+[(v,1-ss) for u,ss,v in reversed(flatten(A1))]
    macros=[]
    for mi,(u,ss) in enumerate(todo):
        want=Tree(a.state());v=want.ch[u][ss];want.rotate(u,ss)
        assert not bad.intersection(want.labels(bits).values()),('forbidden desired elementary state',mi)
        J=set(a.path(v));assert len(J)<=3
        while len(J)<4:J.add(min(c for j in J for c in a.ch[j] if c is not None and c not in J))
        def key(t):return tuple((j,*t.ch[j]) for j in sorted(J))+(('root',t.root),)
        start=a.state();goal=key(want);queue=deque([(a,[])]);seen={key(a)};answer=None
        while queue:
            t,word=queue.popleft()
            if key(t)==goal:answer=word;break
            for target in sorted(J):
                nxt=trial(t.state(),target)
                if nxt is None:continue
                kk=key(nxt)
                if kk not in seen:seen.add(kk);queue.append((nxt,word+[target]))
        if answer is None:
            write('FAILED_FOUR_KEY_SYNTHESIS.json',{'s':s,'mode':mode,'macro':mi,'start':start,'desired':want.state(),'hull':sorted(J),'visited_shapes':len(seen),'protected_labels':sorted(bad)})
            raise RuntimeError('Exact safe four-key macro unreachable; do not assume arbitrary synthesis.')
        for target in answer:
            t=trial(a.state(),target);assert t is not None;ops.append(['D',target]);a=t
        assert a.state()==want.state();macros.append({'hull':sorted(J),'actual_D_targets':answer,'visited_shapes':len(seen)})
    assert a.state()==A1
    perform('K',1);assert a.state()==A0
    assert advance(B,[z for tag,z in ops if tag=='K'])[0]==B
    reach,pr=coerce(B,A0)
    return {'name':f'M1C5_cheap_entry_s{s}_{mode}_protect{int(protect)}','family':'cheap_entry_repeated_noncheap_attempt',
        's':s,'n':n,'mode':mode,'protected':protect,'initial_A':A0,'initial_B':B,'diagonal_initial':B,
        'reaching_prefix':[['D',z] for z in reach],'operations':ops,'creator_operation':mapping[0][1],
        'critical_operation':mapping[1][1],'KEEP_mapping':mapping,'protected_labels':sorted(bad),
        'unprotected_kernel_labels':sorted(excluded),'safe_synthesis_macros':macros,'planner_statistics':dict(stats),
        'scope':'All A restoration is measured BEFORE last B KEEP1; first creator and consumer A gaps predicted1. Original earlier C_old is NOT assumed.'}

if __name__=='__main__':
    m=Meter('cheap_entry_planning');ss=[make(16,'half'),make(32,'half')];write('NEW_SOURCE_CATALOG.json',ss);m.ok=True
    print('PLANNED',[(s['s'],len(s['operations'])) for s in ss],'complete cheap-entry sources',flush=True)
