"""FE02 original-source root-departure and cyclic return budgets; no splay."""


def path(T,key):
    nodes=[];dirs=[]
    while T is not None:
        if isinstance(T,str):raise ValueError('present core query entered opaque subtree')
        nodes.append(T)
        if T[0]==key:return nodes,dirs
        side=1 if key<T[0] else 2;dirs.append('L' if side==1 else 'R');T=T[side]
    raise ValueError('present key required')


def old_root_departure(T,x):
    nodes,dirs=path(T,x);d=len(dirs)
    if not d:return dict(access_depth=0,original_first_directions=[],old_root_depth=0,eta=None,reason='root_noop')
    same_even=d%2==0 and dirs[0]==dirs[1]
    epsilon=2 if same_even else 1
    return dict(access_depth=d,original_first_directions=dirs[:2],old_root_depth=epsilon,
        eta=1-epsilon//2,reason='even_outer_same_side' if same_even else 'final_zig_or_outer_cross')


def return_budget(rows):
    N=len(rows);result=[]
    for j,row in enumerate(rows):
        L=next(k for k in range(1,N+1) if rows[(j-k)%N]['key']==row['key'])
        assert L>=2,'nontrivial cyclic root blocks must have different adjacent keys'
        prev=(j-L)%N;departure=(prev+1)%N;depart=rows[departure]
        assert depart['source_B'][0]==row['key'] and depart['key']!=row['key']
        pr=old_root_departure(depart['source_B'],depart['key'])
        eta=pr['eta'];bound=L-1-eta;C=2*row['a']
        result.append(dict(block=j,key=row['key'],previous_same_block=prev,cyclic_gap=L,
            departure_block=departure,departure_source_profile=pr,eta=eta,
            B_double_source_bound=bound,actual_a=row['a'],actual_q=row['q'],capacity=C,
            forced_unused_capacity=C-min(C,bound),short_gap_donor=bound<C))
    assert sorted(r['departure_block'] for r in result)==list(range(N))
    assert sum(r['cyclic_gap'] for r in result)==len({r['key'] for r in rows})*N
    assert all(r['actual_q']<=r['B_double_source_bound'] for r in result)
    return result
