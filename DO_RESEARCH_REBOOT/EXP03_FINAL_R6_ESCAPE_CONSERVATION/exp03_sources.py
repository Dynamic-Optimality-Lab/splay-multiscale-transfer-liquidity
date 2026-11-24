from exp03_core import *


def outside_probe(p=4,L=3,hit=None,separate_boundary=False):
    """Common vine -> common left vine -> reflected prepared short wave ->
    full decreasing sweep. Last sweep closes BOTH complete original trees.
    No invented inverse rotations or shadow closure is used.
    """
    n=2**(p+2)+1
    h=H(p);prefix=h["operations"][:2*n-1]
    mp=lambda k:n+1-k
    word=ops("K",range(1,n+1))+[[tag,mp(x)] for tag,x in prefix]
    word+=ops("K",range(n,n-L,-1))
    if hit is not None:word.append(["K",hit])
    word+=ops("K",range(n,0,-1))
    state=None
    if separate_boundary:
        initial=Tree(vine(range(1,n+1)));Replay.plain_splay(initial,2)
        state=initial.state();word.append(["K",2])
    return source(f"Xprobe_p{p}_L{L}_hit{hit}_boundary{int(separate_boundary)}",n,word,state=state,
        family="outside_probe",p=p,L=L,hit=hit,separate_boundary=separate_boundary)


def omitted_family(p=4,L=2,hits=(5,),copies=1,q=1):
    s=interrupted_H(p,L,hits,q,copies)
    s.update(name=f"O_p{p}_q{q}_L{L}_hits{'-'.join(map(str,hits))}_c{copies}",family="O")
    return s


def separated_private(p=3,L=2,hits=(5,),copies=1):
    core=omitted_family(p,L,hits,copies)
    n=len(core["initial_B"]["children"]);maximum=2*n-2
    diagonal=vine(range(maximum+1));a=Tree(diagonal)
    prefix=ops("D",[maximum-1,maximum])+ops("D",range(maximum-2,-1,-2))
    for _,x in prefix:Replay.plain_splay(a,x)
    desired={"root":0,"children":{}}
    for i in range(n):
        desired["children"][str(2*i)]=[2*i-1 if i else None,2*i+2 if i<n-1 else None]
        if i:desired["children"][str(2*i-1)]=[None,None]
    assert a.state()==desired,"private-leaf reaching prefix failed"
    word=[[tag,2*(x-1)] for tag,x in core["operations"]]
    return {"name":f"private_p{p}_L{L}_hits{'-'.join(map(str,hits))}_c{copies}","family":"private_separation",
        "p":p,"L":L,"hits":list(hits),"copies":copies,"initial_A":desired,"initial_B":diagonal,
        "operations":word,"diagonal_initial":diagonal,"reaching_prefix":prefix,
        "reachability":"explicit A-only prefix from saved common diagonal; prefix excluded from period cost"}


def closed_private(p=3,L=2,hits=(5,),copies=1):
    """Private leaves during the core, followed by an explicit full physical
    decreasing restoration. Unlike separated_private this closes the full B.
    The preparatory prefix is inside the measured period here.
    """
    candidate=separated_private(p,L,hits,copies)
    maximum=max(map(int,candidate['initial_B']['children']))
    word=candidate['reaching_prefix']+candidate['operations']+ops('K',range(maximum,-1,-1))
    return source(f"closed_private_p{p}_L{L}_hits{'-'.join(map(str,hits))}_c{copies}",maximum+1,[],family='private_hangers') | {
        'initial_A':candidate['diagonal_initial'],'initial_B':candidate['diagonal_initial'],
        'operations':word,'p':p,'L':L,'hits':list(hits),'copies':copies}


def many_interruptions(p=4,cycles=4,style='alternate'):
    n=2**(p+2)+1;prefix=H(p)['operations'][:2*n-1]
    if style=='alternate':piece=ops('K',[1,2,5,n,3,1,2,7,n-1])
    elif style=='nested':piece=ops('K',[1,2,5,3,n,4,7,1,n-1,2,11,3])
    else:raise ValueError(style)
    word=prefix+piece*cycles+ops('K',range(1,n+1))+ops('K',range(n-1,0,-1))
    return source(f"multi_p{p}_c{cycles}_{style}",n,word,family='multi_interruptions',p=p,cycles=cycles,style=style)


def mixed_closed(p=4,copies=2):
    n=2**(p+2)+1
    a=omitted_family(p,2,(5,))['operations']
    b=omitted_family(p,3,(1,n),copies)['operations']
    return source(f"mixed_p{p}_Gcopies{copies}",n,a+b,family='mixed_complete_periods',p=p,copies=copies)


def corpus():
    out=[]
    for p in (3,4,5,6):
        n=2**(p+2)+1
        for L,hits in ((2,(5,)),(2,(7,)),(3,(5,)),(5,(11,)),(2,(5,3,7)),(3,(1,n))):
            out.append(omitted_family(p,L,hits))
    for c in (2,4,8):out.append(omitted_family(4,2,(5,),c))
    for q in (2,3):out.append(omitted_family(4,2,(5,),q=q))
    for p in (4,5,6):
        n=2**(p+2)+1
        for boundary in (False,True):out.append(outside_probe(p,3,separate_boundary=boundary))
        out.append(outside_probe(p,2,n-4,True))
    out.extend(reflect(s) for s in (out[1],out[12],outside_probe(4,3,separate_boundary=True)))
    for p in (2,3,4):
        for hits in ((5,),(5,3,7)):out.append(closed_private(p,hits=hits))
    for p in (4,5):
        for style in ('alternate','nested'):
            for cycles in (1,4,16):out.append(many_interruptions(p,cycles,style))
    for p in (4,5):
        for copies in (2,4):out.append(mixed_closed(p,copies))
    assert len(out)<=100 and len({s['name'] for s in out})==len(out)
    assert all(len(s['initial_A']['children'])<=513 and len(s['operations'])<=20000 for s in out)
    return out


def warmed_private(p=3,pattern=(0,8,4),helpers=False):
    """Exact eventual paired cycle, reached by the saved physical prefix.
    Odd connector keys are never requested in the measured cycle.
    A repeat is detected, not assumed; initial words are NOT called closed.
    """
    base=separated_private(p);diag=base['diagonal_initial']
    a=Tree(base['initial_A']);b=Tree(base['initial_B'])
    word=[]
    for i,x in enumerate(pattern):
        if helpers and i%2==0:word.append(['D',2*x+1])
        word.append(['K',2*x])
    assert all(x in a.keys for _,x in word)
    seen={};states=[]
    for k in range(65):
        key=digest([a.state(),b.state()])
        if key in seen:
            j=seen[key];initial_A,initial_B=states[j]
            name=f"warm_private_p{p}_w{'-'.join(map(str,pattern))}_D{int(helpers)}"
            return {'name':name,'family':'warmed_private','p':p,'pattern':list(pattern),'helpers':helpers,
                'diagonal_initial':diag,'initial_A':initial_A,'initial_B':initial_B,
                'reaching_prefix':base['reaching_prefix']+word*j,'operations':word*(k-j),
                'warmup_periods':j,'cycle_periods':k-j,
                'reachability':'explicit saved common diagonal and genuine K/D prefix, excluded from period cost'}
        seen[key]=k;states.append((a.state(),b.state()))
        for tag,x in word:
            Replay.plain_splay(a,x)
            if tag=='K':Replay.plain_splay(b,x)
    raise AssertionError('bounded warming did not find a cycle')


def additional_corpus():
    out=[mixed_closed(6,2),mixed_closed(7,2)]
    patterns=((0,8,4),(0,8,2,6,4),(0,16,4,12,8),(0,16,2,14,4,12,6,10,8),
        (0,8,1,7,2,6,3,5,4),(0,4,8,2,6,1,7,3,5))
    for p in (3,4):
        for pat in patterns:
            for helpers in (False,True):out.append(warmed_private(p,pat,helpers))
    return out
