from base4 import *
from fan2 import fan
from sources3 import vine
from coercion import coerce,advance

def blocks(s,mode):
    gs=list(range(2,s+2))
    if mode=='descending':return list(reversed(gs))
    if mode=='half':return list(reversed(gs[:s//2]))+list(reversed(gs[s//2:]))
    chunks=[gs[i:i+4][::-1] for i in range(0,s,4)]
    if mode=='blocks':return [g for c in chunks for g in c]
    if mode=='bit_blocks':
        width=(len(chunks)-1).bit_length()
        order=sorted(range(len(chunks)),key=lambda i:int(f'{i:0{width}b}'[::-1],2))
        return [g for i in order for g in chunks[i]]
    raise ValueError(mode)

def make(s,mode='descending',lower=0,upper=0,insert=None,forced=False,repeats=0):
    old=fan(s,'m');n0=2*s+6;n=n0+lower+upper;off=lower
    assert lower in (0,1)
    B={'root':old['initial_B']['root']+off,'children':{str(j):[None,None] for j in range(1,n+1)}}
    for k,children in old['initial_B']['children'].items():B['children'][str(int(k)+off)]=[x+off if x else None for x in children]
    if lower:B['children'][str(1+off)][0]=1
    for k in range(n0+off,n):B['children'][str(k)][1]=k+1
    b=s+5+off;x=b-1;y=b-2;ps=b+1
    A=vine(n,b);reach,rs=coerce(B,A)
    body=[b]
    if insert=='outside':body += [ps]
    elif insert=='minimum':body += [1]
    elif insert=='inside':body += [s+1+off]
    elif insert is not None:raise ValueError(insert)
    body += [z for _ in range(repeats) for z in (ps,b)]
    critical=len(body)+1
    body += [x,y]+[g+off for g in blocks(s,mode)]
    tour=list(range(1,n+1))+[1]
    state,_=advance(B,body+tour)
    if forced:
        assert lower==1 and B['root']==2 and B['children']['2'][0]==1 and B['children']['1']==[None,None]
        corner,_=advance(B,[1]);assert advance(corner,[2])[0]==B
        back,br=coerce(state,corner);back += [2]
    else:back,br=coerce(state,B)
    ks=body+tour+back
    ops=[];root=b;mapping=[]
    for kh,target in enumerate(ks,1):
        while abs(target-root)>2:
            root += 2 if target>root else -2;ops.append(['D',root])
        ops.append(['K',target]);root=target;mapping.append([kh,len(ops)])
    while root!=b:
        root += min(2,b-root) if root<b else -min(2,root-b);ops.append(['D',root])
    assert advance(A,[x for tag,x in ops])[0]==A
    assert advance(B,[x for tag,x in ops if tag=='K'])[0]==B
    name=f'M1C4_s{s}_{mode}_lo{lower}_hi{upper}_in{insert}_corner{int(forced)}_rep{repeats}'
    return {'name':name,'family':'controlled_paid_packet_deformation','s':s,'n':n,'mode':mode,
        'lower_guard_keys':lower,'upper_guard_keys':upper,'inserted_KEEP':insert,'forced_zig_corner':forced,'outside_pairs':repeats,
        'initial_A':A,'initial_B':B,'diagonal_initial':B,'reaching_prefix':[['D',x] for x in reach],
        'operations':ops,'KEEP_mapping':mapping,'critical_KEEP_index':critical,
        'critical_operation':mapping[critical-1][1],'creator_operation':mapping[0][1],
        'prefix_statistics':rs,'B_return_statistics':br,
        'scope':'New original source; all helper and restoration work measured. Original R6/R_* and frozen selectors must be recomputed.'}

def initial_sources():
    return [make(16,'blocks'),make(32,'blocks'),make(32,'bit_blocks'),
        make(16,insert='outside'),make(16,insert='minimum'),make(16,insert='inside'),
        make(16,lower=1,forced=True),make(32,lower=1,forced=True),
        make(16,lower=1,upper=4,forced=True),make(32,'blocks',lower=1,upper=4,forced=True)]
