"""Actual-ID partial exchange; no source/debt/cardinality oracle.
Caller supplies an independently valid partial full map h and fixed common
map locked. Unknown h values produce explicit blocked roots, never PASS.
"""
def exchange(full_demands,physical_units,locked,h):
    D=set(full_demands);U=set(physical_units)
    if not set(locked)<=D or not set(h)<=D:raise ValueError('outside demand domain')
    for m in (locked,h):
        if len(set(m.values()))!=len(m) or not set(m.values())<=U:raise ValueError('duplicate or outside donor')
    inverse={u:d for d,u in locked.items()};answer=dict(locked);paths=[];blocked={}
    for root in sorted(set(h)-set(locked)):
        demand=root;seen=set();path=[]
        while True:
            if demand in seen:raise AssertionError('injective maps cannot create an entered common cycle')
            seen.add(demand);u=h[demand];path.append((demand,u))
            if u not in inverse:
                answer[root]=u;paths.append({'root':root,'steps':path,'terminal_unit':u});break
            owner=inverse[u]
            if owner not in h:
                blocked[root]={'owner':owner,'steps':path};break
            demand=owner
    assert len(set(answer.values()))==len(answer)
    assert len({v['owner'] for v in blocked.values()})==len(blocked)
    assert all(answer[k]==v for k,v in locked.items())
    uncovered=D-set(answer)
    return {'allocation':answer,'paths':paths,'blocked':blocked,'uncovered':uncovered,
        'total':not uncovered,'complete_h_input':set(h)==D}
