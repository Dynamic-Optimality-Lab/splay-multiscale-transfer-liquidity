from base3 import *
from sources3 import vine
from coercion import advance
from exp01_oracle import Tree

def reflected(s):
    s=copy.deepcopy(s);n=s['n']
    def state(st):return {'root':n+1-st['root'],'children':{str(n+1-int(j)):[n+1-v[1] if v[1] else None,n+1-v[0] if v[0] else None] for j,v in st['children'].items()}}
    for key in ('initial_A','initial_B','diagonal_initial'):s[key]=state(s[key])
    for key in ('operations','reaching_prefix'):s[key]=[[tag,n+1-x] for tag,x in s[key]]
    s['protected_labels']=sorted(sum(1<<(n-k) for k in range(1,n+1) if lab>>(k-1)&1) for lab in s['protected_labels'])
    s['name']=s['name'].replace('mirror0','mirror1');s['full_reflection']=True
    return s

def make(index):
    old=load(ROOT/'NEW_SOURCE_CATALOG.json')[index];p=load(ROOT/f'NEW_PHYS_{index:02}.json');n=old['n']
    extreme=1|(1<<(n-1));bad=set()
    for d in p['doubles']:
        if d['parent'][0]<=3 and not d['F']&extreme:bad.update((d['F'],d['J'],d['P_output']))
    assert bad and all(lab and not lab&extreme for lab in bad)
    bits={j:1<<(j-1) for j in range(1,n+1)}
    a=Tree(old['initial_A']);word=[];stats=Counter();blocked=Counter();mapping=[]
    def probe(x):
        t=Tree(a.state());depth=0
        while t.par[x] is not None:
            pp=t.par[x];g=t.par[pp]
            if g is None:rotations=[(pp,int(x>pp))]
            else:
                side=int(x>pp);z=int(pp>g)
                rotations=[(g,z),(pp,side)] if side==z else [(pp,side),(g,z)]
            for u,side in rotations:
                t.rotate(u,side);depth+=1
                hit=set(t.labels(bits).values())&bad
                if hit:return None,hit
        return t,set()
    def perform(tag,x):
        nonlocal a
        while True:
            t,hit=probe(x)
            if t is not None:
                word.append([tag,x]);a=t;break
            stats['blocked_trials']+=1
            for lab in hit:blocked[lab]+=1
            path=a.path(x);assert len(path)>3
            helper=path[2];before=len(path)-1;tt,hh=probe(helper);assert tt is not None and not hh
            word.append(['D',helper]);a=tt;stats['shallow_helpers']+=1
            assert len(a.path(x))-1<before
    for h,(tag,x) in enumerate(old['operations'],1):
        if tag=='K':perform('K',x);mapping.append([h,len(word)])
    for x in range(n,0,-1):perform('D',x)
    assert a.state()==vine(n,1),'Safe descending closure failed; do not substitute another return.'
    dest=old['initial_A']['root']
    while a.root!=dest:
        x=a.root+min(2,dest-a.root) if a.root<dest else a.root-min(2,a.root-dest)
        perform('D',x)
    assert a.state()==old['initial_A']
    result={'name':f'M1C3_protected_fan_s{old["s"]}_mirror0','family':'finite_protected_label_safe_access_fan',
        's':old['s'],'n':n,'full_reflection':False,'initial_A':old['initial_A'],'initial_B':old['initial_B'],
        'diagonal_initial':old['diagonal_initial'],'reaching_prefix':old['reaching_prefix'],'operations':word,
        'critical_KEEP':2,'base_splitvine_source_sha256':digest(old),'original_KEEP_mapping':mapping,
        'protected_labels':sorted(bad),'planner_statistics':dict(stats),
        'blocked_label_counts':[[k,v] for k,v in sorted(blocked.items())],
        'scope':'Forbidden-label trials are computation only; every emitted D/K and complete restoration is measured original work.'}
    assert advance(result['initial_A'],[x for tag,x in word])[0]==result['initial_A']
    assert advance(result['initial_B'],[x for tag,x in word if tag=='K'])[0]==result['initial_B']
    return result

def sources():
    originals=[make(i) for i in range(4)]
    return originals+[reflected(originals[i]) for i in (1,2)]
