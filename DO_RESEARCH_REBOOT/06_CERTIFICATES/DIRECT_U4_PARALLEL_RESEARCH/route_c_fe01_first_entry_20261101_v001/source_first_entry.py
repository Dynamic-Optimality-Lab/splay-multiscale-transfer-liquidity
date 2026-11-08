"""FE01: final depth from ORIGINAL source geometry, without a splay call.

Trees are [key,left,right] or None. Opaque off-path subtree variables may be
used when neither queried present key lies in them. No source output tree,
future payer cost, original splay engine or mutable rotation is consulted.
"""

ENTRY = {
    'LL': dict(x=-2,p=0,g=2,A=-2,B=-1,C=1,D=2),
    'RR': dict(x=-2,p=0,g=2,A=2,B=1,C=-1,D=-2),
    'LR': dict(x=-2,p=0,g=1,A=0,B=-1,C=-1,D=1),
    'RL': dict(x=-2,p=0,g=1,A=1,B=-1,C=-1,D=0),
    'ZIG_L': dict(x=-1,p=1,A=-1,B=0,C=1),
    'ZIG_R': dict(x=-1,p=1,A=1,B=0,C=-1),
}
OUTER = {
    'LL': (-2,-1), 'RR': (-1,-2), 'LR': (-1,-1), 'RL': (-1,-1),
    'ZIG_L': (-1,0), 'ZIG_R': (0,-1),
}


def path(T,key):
    nodes=[];directions=[]
    while T is not None:
        if isinstance(T,str):raise ValueError('query entered an opaque subtree')
        nodes.append(T)
        if T[0]==key:return nodes,directions
        side=1 if key<T[0] else 2
        directions.append('L' if side==1 else 'R');T=T[side]
    raise ValueError('FE requires present keys')


def contains(T,key):
    while T is not None and not isinstance(T,str):
        if T[0]==key:return True
        T=T[1 if key<T[0] else 2]
    return False


def source_operations(T,x):
    nodes,dirs=path(T,x);d=len(dirs);ops=[]
    for top in range(d-2,-1,-2):
        ops.append(dict(case=''.join(dirs[top:top+2]),top_depth=top,
                        grandparent=nodes[top][0],parent=nodes[top+1][0]))
    if d%2:
        ops.append(dict(case='ZIG_'+dirs[0],top_depth=0,
                        grandparent=None,parent=nodes[0][0]))
    return nodes,dirs,ops


def entry_role(nodes,x,y,op,entry_index):
    """Classify from original nodes/off-path fringes, never rebuilt fringes."""
    case=op['case'];top=op['top_depth'];target=nodes[-1]
    if case.startswith('ZIG'):
        p=nodes[0]
        if y==p[0]:return 'p'
        if case=='ZIG_L':
            if contains(p[2],y):return 'C'
            inner=dict(A=target[1],B=target[2])
        else:
            if contains(p[1],y):return 'A'
            inner=dict(B=target[1],C=target[2])
        # If earlier doubles existed, nodes[1]'s original subtree was their
        # last site and would have contained y. Target fringes can enter here
        # only for an original one-edge search path.
        assert len(nodes)==2 and entry_index==0
        matches=[role for role,t in inner.items() if contains(t,y)]
    else:
        g,p=nodes[top],nodes[top+1]
        if y==g[0]:return 'g'
        if y==p[0]:return 'p'
        outside={
            'LL':dict(C=p[2],D=g[2]),
            'RR':dict(A=g[1],B=p[1]),
            'LR':dict(A=p[1],D=g[2]),
            'RL':dict(A=g[1],D=p[2]),
        }[case]
        matches=[role for role,t in outside.items() if contains(t,y)]
        if not matches:
            # y must be in the original inner site. This cannot be its FIRST
            # containing site unless this is the innermost source operation.
            assert top+2==len(nodes)-1 and entry_index==0
            inner={
                'LL':dict(A=target[1],B=target[2]),
                'RR':dict(C=target[1],D=target[2]),
                'LR':dict(B=target[1],C=target[2]),
                'RL':dict(B=target[1],C=target[2]),
            }[case]
            matches=[role for role,t in inner.items() if contains(t,y)]
    assert len(matches)==1,(case,x,y,matches)
    return matches[0]


def profile(T,x,y):
    nodes,dirs,ops=source_operations(T,x)
    h=len(path(T,y)[0])-1;d=len(dirs)
    common=dict(h=h,access_depth=d,source_path=[n[0] for n in nodes],
                directions=dirs,operations=ops)
    if y==x:
        return dict(common,boundary='accessed_key',entry_index=None,entry_case=None,entry_role='x',
                    entry_shift=0,later_double_shifts=[],terminal_zig_shift=0,H=0,PF_U=0,FI_U=0)
    if not d:
        return dict(common,boundary='root_noop',entry_index=None,entry_case=None,entry_role=None,
                    entry_shift=0,later_double_shifts=[],terminal_zig_shift=0,H=h,PF_U=h,FI_U=h)
    entry=next(j for j,op in enumerate(ops) if contains(nodes[op['top_depth']],y))
    op=ops[entry];case=op['case'];role=entry_role(nodes,x,y,op,entry)
    delta=ENTRY[case][role];side=0 if y<x else 1
    later=[o for o in ops[entry+1:] if not o['case'].startswith('ZIG')]
    shifts=[OUTER[o['case']][side] for o in later]
    terminal=sum(OUTER[o['case']][side] for o in ops[entry+1:] if o['case'].startswith('ZIG'))
    H=h+delta+sum(shifts)+terminal
    assert H>=0
    if case.startswith('ZIG'):mu=pfmu=1
    else:
        mu=0 if role=='p' else 2
        pfmu=0 if (case,role) in [('LR','A'),('RL','D')] else mu
    r=len(later);matched=sum(o['case']==('LL' if y<x else 'RR') for o in later)
    PF_U=min(h+2,max(0,h+pfmu-r-matched))
    FI_U=min(h+2,max(0,h+mu-r-matched))
    assert H<=PF_U<=FI_U
    return dict(common,boundary=None,entry_index=entry,entry_case=case,entry_role=role,
                entry_shift=delta,later_double_shifts=shifts,terminal_zig_shift=terminal,
                H=H,PF_U=PF_U,FI_U=FI_U)


def ceiling(T,first_key,y,k,protocol='FE',has_KEEP=True):
    if not has_KEEP:return 0
    if k==0:return (len(path(T,y)[0])-1)//2
    assert k>=1 and first_key is not None
    pr=profile(T,first_key,y)
    value=pr[{'FE':'H','PF':'PF_U','FI':'FI_U'}[protocol]]
    return value//2+k-1
