from base3 import *
from fan2 import fan
from coercion import advance

def vine(n,r):
    ch={str(j):[None,None] for j in range(1,n+1)}
    for j in range(2,r+1):ch[str(j)][0]=j-1
    for j in range(r,n):ch[str(j)][1]=j+1
    return {'root':r,'children':ch}

def guarded_fan(s,reflection=False):
    old=fan(s,'m');n=len(old['initial_A']['children']);initialroot=old['initial_A']['root']
    assert old['initial_A']==vine(n,initialroot)
    ks=[(i,x) for i,(tag,x) in enumerate(old['operations'],1) if tag=='K'];r=initialroot;ops=[];mapping=[]
    for oldh,x in ks:
        while abs(x-r)>2:
            r+=2 if x>r else -2;ops.append(['D',r])
        ops.append(['K',x]);r=x;mapping.append([oldh,len(ops)])
    while r!=initialroot:
        r+=min(2,initialroot-r) if r<initialroot else -min(2,r-initialroot)
        ops.append(['D',r])
    source={'name':f'M1C3_splitvine_fan_s{s}_mirror{int(reflection)}','family':'globally_internal_A_blind_column_fan',
        's':s,'n':n,'initial_A':old['initial_A'],'initial_B':old['initial_B'],
        'diagonal_initial':old['diagonal_initial'],'reaching_prefix':old['reaching_prefix'],
        'operations':ops,'base_C2_style_source_sha256':digest(old),'original_KEEP_mapping':mapping,
        'critical_KEEP':2,'full_reflection':reflection,
        'A_invariant':'Every primitive snapshot is the full labelled split-vine at its current root; every nonempty subtree touches an extreme.'}
    if reflection:
        def refl(st):return {'root':n+1-st['root'],'children':{str(n+1-int(j)):[n+1-v[1] if v[1] else None,n+1-v[0] if v[0] else None] for j,v in st['children'].items()}}
        for k in ('initial_A','initial_B','diagonal_initial'):source[k]=refl(source[k])
        for k in ('operations','reaching_prefix'):source[k]=[[tag,n+1-x] for tag,x in source[k]]
    assert advance(source['initial_A'],[x for tag,x in source['operations']])[0]==source['initial_A']
    assert advance(source['initial_B'],[x for tag,x in source['operations'] if tag=='K'])[0]==source['initial_B']
    return source

def sources():return [guarded_fan(s,ref) for s,ref in ((8,False),(16,False),(32,False),(64,False),(16,True),(32,True))]
