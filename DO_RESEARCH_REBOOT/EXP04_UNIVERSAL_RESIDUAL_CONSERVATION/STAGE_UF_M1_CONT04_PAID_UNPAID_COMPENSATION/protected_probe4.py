from base4 import *
from sources4 import make
from sources3 import vine
from coercion import advance,coerce
from exp01_oracle import Tree,Replay
from physical1 import Edges

def kernel_labels(B,targets):
    a=Tree(B);n=len(a.keys);bits={j:1<<(j-1) for j in a.keys};bad=set();extreme=1|(1<<(n-1))
    for x in targets:
        old=[]
        while a.par[x] is not None:
            pp=a.par[x];g=a.par[pp];side=int(x>pp)
            if g is None:a.rotate(pp,side);continue
            z=int(pp>g);F=a.labels(bits)[g];old.append((g,pp,F))
            for u,ss in ((g,z),(pp,side)) if side==z else ((pp,side),(g,z)):a.rotate(u,ss)
        labs=a.labels(bits)
        for g,pp,F in old:
            if not F&extreme:bad.update((F,labs[g],labs[pp]))
    # Exactly the internal labels that C_n or its full-vine synthesis uses.
    def allowed_exception(lab):
        keys=[j for j in a.keys if lab>>(j-1)&1]
        return keys[-1]==n-1 or (len(keys)==1 and keys[0]%2==0)
    exceptions=sorted(lab for lab in bad if allowed_exception(lab))
    bad-=set(exceptions)
    return sorted(bad),exceptions

def make_short():
    template=make(256,'half');n=template['n'];assert n==518 and n%2==0
    B=template['initial_B'];b=template['initial_A']['root'];ks=[x for tag,x in template['operations'] if tag=='K']
    C,_=advance(vine(n,1),[n,1]);assert C['root']==1 and C['children']['1'][1]==n
    bad,exceptions=kernel_labels(B,ks[:3]);bad=set(bad);bits={j:1<<(j-1) for j in range(1,n+1)}
    a=Tree(C);assert not bad.intersection(a.labels(bits).values());word=[['K',n],['K',1]];stats=Counter()
    # The two actual paired zigs return C before the preparation.
    assert advance(C,[n,1])[0]==C and advance(B,[n,1])[0]==B
    def probe(x):
        t=Tree(a.state())
        while t.par[x] is not None:
            pp=t.par[x];g=t.par[pp]
            if g is None:rot=[(pp,int(x>pp))]
            else:
                side=int(x>pp);z=int(pp>g)
                rot=[(g,z),(pp,side)] if side==z else [(pp,side),(g,z)]
            for u,ss in rot:
                t.rotate(u,ss)
                if bad.intersection(t.labels(bits).values()):return None
        return t
    def perform(tag,x):
        nonlocal a
        while True:
            t=probe(x)
            if t is not None:word.append([tag,x]);a=t;return
            path=a.path(x);assert len(path)>3;tt=probe(path[2]);assert tt is not None
            before=len(path);word.append(['D',path[2]]);a=tt;stats['shallow_helpers']+=1
            assert len(a.path(x))<before
    for x in range(n,0,-1):perform('D',x)
    assert a.state()==vine(n,1)
    while a.root!=b:perform('D',a.root+min(2,b-a.root))
    assert a.state()==vine(n,b)
    mapping=[]
    for j,x in enumerate(ks,1):perform('K',x);mapping.append([j,len(word)])
    for x in range(n,0,-1):perform('D',x)
    assert a.state()==vine(n,1)
    # Every primitive of this synthesis must also pass exact protection.
    perform('D',n);perform('D',1);assert a.state()==C
    prefix,ps=coerce(B,C)
    return {'name':'M1C4_protected_half_s256_extreme_identity_T1','family':'protected_wide_packet_extreme_replication',
        's':256,'n':n,'initial_A':C,'initial_B':B,'diagonal_initial':B,'reaching_prefix':[['D',x] for x in prefix],
        'operations':word,'replication':1,'rootzig_loop_start':1,'critical_operation':mapping[1][1],
        'creator_operation':mapping[0][1],'protected_labels':sorted(bad),'explicit_unprotected_kernel_labels':exceptions,
        'planner_statistics':dict(stats),'prefix_statistics':ps,'original_B_KEEP_mapping':mapping,
        'scope':'All safe helpers and exact A/B closures are measured. Full original predicates must be recomputed.'}

if __name__=='__main__':
    m=Meter('protected_large_planning');s=make_short();write('PROBE_SHORT_SOURCE.json',s);m.ok=True
    print('PLANNED exact protected518 source, operations',len(s['operations']),'critical',s['critical_operation'],flush=True)
