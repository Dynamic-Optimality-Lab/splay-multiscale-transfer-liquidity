from exp04_core import *
from itertools import product


def protect_fringe(base,tail=5,cut=0):
    n=len(base['initial_B']['children']);diag=vine(range(1,n+tail+1));found=None
    trials=[(n+2,),(n+4,),(n+2,n+4),(n+4,n+2),(n+3,n+1,n+4)]
    for pattern in trials:
        a=Tree(diag);b=Tree(diag);prefix=ops('D',pattern)+ops('K',range(1,n+1))+ops('K',range(n-1,0,-1))
        for tag,x in prefix:
            Replay.plain_splay(a,x)
            if tag=='K':Replay.plain_splay(b,x)
        def corestate(tree):
            st=tree.state();return {'root':st['root'],'children':{str(k):[v if v is None or v<=n else None for v in st['children'][str(k)]] for k in range(1,n+1)}}
        if corestate(a)==corestate(b)==vine(range(1,n+1)) and a.state()!=b.state():
            found=(a,b,prefix,pattern);break
    assert found is not None,'no untouched-fringe discrepancy found'
    a,b,prefix,pattern=found
    # Restore this base's actual common core start, not an assumed vine.
    assert base['initial_A']==base['initial_B']
    root=base['initial_B']['root']
    Replay.plain_splay(a,root);Replay.plain_splay(b,root);prefix=prefix+[['K',root]]
    assert corestate(a)==corestate(b)==base['initial_B']
    word=base['operations'];cut%=len(word)
    for tag,x in word[:cut]:
        Replay.plain_splay(a,x)
        if tag=='K':Replay.plain_splay(b,x)
    return {'name':base['name']+f'_protected{tail}_cut{cut}','family':'protected_fringe',
        'base_name':base['name'],'tail':tail,'cut':cut,'tail_preparation':list(pattern),
        'diagonal_initial':diag,'initial_A':a.state(),'initial_B':b.state(),
        'reaching_prefix':prefix+word[:cut],'operations':word[cut:]+word[:cut],
        'reachability':'saved actual prefix from complete common diagonal; prefix excluded'}


def missing_ranks(p=4,holes=(3,),interrupt=(1,),repeat=1):
    n=2**(p+2)+1;base=omitted_family(p,3,interrupt)
    word=base['operations'];start=2*n-1+3+len(interrupt)
    # Replace only the forward scan's selected KEEP ranks with genuine DELETEs.
    for i in range(start,start+n-3):
        if word[i][1] in holes:word[i][0]='D'
    # Full later reverse is unchanged, so both full trees restore the right vine.
    return source(f"holes_p{p}_h{'-'.join(map(str,holes))}_z{'-'.join(map(str,interrupt))}_r{repeat}",n,word*repeat,
        family='missing_rank_barriers',p=p,holes=list(holes),interrupt=list(interrupt),repeat=repeat)


def arbitrary_word_cycle(n,word,diagonal=None,max_warm=64,name='warm'):
    diag=diagonal or vine(range(1,n+1));a=Tree(diag);b=Tree(diag);seen={};states=[]
    for k in range(max_warm+1):
        key=digest([a.state(),b.state()])
        if key in seen:
            j=seen[key];aa,bb=states[j]
            return {'name':name,'family':'exact_warmed_cycle','diagonal_initial':diag,'initial_A':aa,'initial_B':bb,
                'reaching_prefix':word*j,'operations':word*(k-j),'warmup_copies':j,'cycle_copies':k-j}
        seen[key]=k;states.append((a.state(),b.state()))
        for tag,x in word:
            Replay.plain_splay(a,x)
            if tag=='K':Replay.plain_splay(b,x)
    return None


def first_corpus():
    out=[]
    for p in (3,4,5):
        n=2**(p+2)+1
        for holes in ((4,),(7,),(11,),(4,7),(7,11,19)):
            for targets in ((1,n),(5,)):
                out.append(missing_ranks(p,holes,targets))
    for p in (3,4):
        n=2**(p+2)+1
        for base in (omitted_family(p,2,(5,),copies=2),mixed_closed(p,2),outside_probe(p,3,separate_boundary=True)):
            out.append(protect_fringe(base,cut=0))
            out.append(protect_fringe(base,cut=len(omitted_family(p,2,(5,))['operations'])-1 if base['family']=='mixed_complete_periods' else len(base['operations'])-1))
    return out


def oscillation(p=4,m=32,where='inside',high_offset=0):
    n=2**(p+2)+1;base=omitted_family(p,2,(5,));word=base['operations'];loop=ops('K',[1,n-high_offset])*m
    if where=='inside':word=word[:2*n+1]+loop+[['K',2]]+word[2*n+1:]
    elif where=='outside':word=word+loop+ops('K',range(n,0,-1))
    else:raise ValueError(where)
    return source(f'osc_p{p}_m{m}_{where}_off{high_offset}',n,word,family='extreme_oscillations',p=p,m=m,where=where,high_offset=high_offset)


def scramble(p=4,style='bitreverse'):
    n=2**(p+2)+1;base=omitted_family(p,2,(5,));targets=list(range(3,n+1))
    if style=='bitreverse':
        width=(n-1).bit_length();targets.sort(key=lambda x:int(f'{x:0{width}b}'[::-1],2))
    elif style=='alternating':
        original=targets;targets=[]
        while original:
            targets.append(original.pop(0))
            if original:targets.append(original.pop())
    elif style=='dyadic':targets.sort(key=lambda x:((x&-x).bit_length(),x),reverse=True)
    else:raise ValueError(style)
    word=base['operations'][:2*n+2]+ops('K',targets)+ops('K',range(n-1,0,-1))
    return source(f'scramble_p{p}_{style}',n,word,family='scrambled_continuations',p=p,style=style)


def second_corpus():
    out=[]
    for p in (3,4,5):
        for m in (4,32,256):
            for where in ('inside','outside'):out.append(oscillation(p,m,where))
    for p in (4,5,6):
        for where in ('inside','outside'):out.append(oscillation(p,1024,where))
    for p in (3,4,5):
        for style in ('bitreverse','alternating','dyadic'):out.append(scramble(p,style))
    for p in (4,5,6):out.append(oscillation(p,64,'inside',1))
    return out


def warmed_sparse_H(p=3,hits=(5,),hole=None):
    from exp03_sources import separated_private
    base=separated_private(p,hits=hits);a=Tree(base['initial_A']);b=Tree(base['initial_B']);word=base['operations']
    if hole is not None:
        core_n=(len(a.keys)+1)//2;start=2*core_n+1+len(hits)
        for i in range(start,min(start+core_n-2,len(word))):
            if word[i]==['K',2*(hole-1)]:word[i][0]='D'
    seen={};states=[]
    for k in range(17):
        key=digest([a.state(),b.state()])
        if key in seen:
            j=seen[key];aa,bb=states[j]
            return {'name':f"sparseH_p{p}_hits{'-'.join(map(str,hits))}_hole{hole}",'family':'warmed_sparse_H',
                'diagonal_initial':base['diagonal_initial'],'initial_A':aa,'initial_B':bb,
                'operations':word*(k-j),'reaching_prefix':base['reaching_prefix']+word*j,
                'warmup_copies':j,'cycle_copies':k-j,'p':p,'hole':hole,'hits':list(hits)}
        seen[key]=k;states.append((a.state(),b.state()))
        for tag,x in word:
            Replay.plain_splay(a,x)
            if tag=='K':Replay.plain_splay(b,x)
    raise AssertionError('no exact sparse paired cycle within16 warms')


def third_corpus():
    return [warmed_sparse_H(p,hits,hole) for p in (3,4,5) for hits,hole in (((5,),None),((7,),None),((5,),4),((5,3,7),None))]


def composed(p,style,where,m=256):
    base=scramble(p,style);n=2**(p+2)+1;word=base['operations'];loop=ops('K',[1,n])*m
    if where=='outside':word=word+loop+ops('K',range(n,0,-1))
    else:word=word[:2*n+1]+loop+[['K',2]]+word[2*n+1:]
    return source(f'composed_p{p}_{style}_{where}_m{m}',n,word,family='composed_scramble_oscillations',p=p,style=style,where=where,m=m)


def leaf_scan(p=2,style='forward'):
    from exp03_sources import separated_private
    base=separated_private(p);core=list(range(0,len(base['initial_B']['children']),2))
    if style=='forward':word=ops('K',core)+[['K',0]]
    elif style=='sweep':word=ops('K',core)+ops('K',core[-2::-1])
    elif style=='alternating':
        xs=list(core);ys=[]
        while xs:
            ys.append(xs.pop(0))
            if xs:ys.append(xs.pop())
        word=ops('K',ys)+[['K',0]]
    elif style=='delete_marks':word=[['D' if i%3==1 else 'K',x] for i,x in enumerate(core)]+ops('K',core[::-1])
    elif style=='interrupt':word=ops('K',core[:2])+ops('K',[core[4],core[1]])+ops('K',core[2:])+[['K',0]]
    elif style=='helpers':word=ops('D',[core[-1],core[len(core)//2]])+ops('K',core)+[['K',0]]
    else:raise ValueError(style)
    a=Tree(base['initial_A']);b=Tree(base['initial_B']);seen={};states=[]
    for k in range(33):
        key=digest([a.state(),b.state()])
        if key in seen:
            j=seen[key];aa,bb=states[j]
            return {'name':f'leafscan_p{p}_{style}','family':'sparse_leaf_cycles','p':p,'style':style,
                'diagonal_initial':base['diagonal_initial'],'initial_A':aa,'initial_B':bb,
                'reaching_prefix':base['reaching_prefix']+word*j,'operations':word*(k-j),
                'warmup_copies':j,'cycle_copies':k-j}
        seen[key]=k;states.append((a.state(),b.state()))
        for tag,x in word:
            Replay.plain_splay(a,x)
            if tag=='K':Replay.plain_splay(b,x)
    raise AssertionError('leafscan warming did not close')


def last_corpus():
    out=[composed(p,style,where) for p in (4,5,6) for style in ('alternating','bitreverse') for where in ('outside','inside')]
    out += [leaf_scan(p,style) for p in (1,2,3) for style in ('forward','sweep','alternating','delete_marks','interrupt','helpers')]
    return out
