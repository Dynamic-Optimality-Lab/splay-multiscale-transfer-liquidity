"""Core7 one-slot physical algorithm; no tree/debt/matching oracle.
Source membership and actual event rows are independently certified.
Maps use actual(t,k) demands and(t,j,bit) units of ONE actual period.
"""
def macros(rows):
    if not rows or len({r['occurrence'] for r in rows})!=len(rows):raise ValueError('source occurrence inventory')
    ends=[i for i,r in enumerate(rows) if r['genuine_F']]
    if not ends:raise ValueError('no genuine source boundary')
    result=[]
    for j,end in enumerate(ends):
        prev=ends[j-1]
        inds=list(range(prev+1,end+1)) if prev<end else list(range(prev+1,len(rows)))+list(range(end+1))
        seg=[rows[i] for i in inds]
        if any(r['qF'] for r in seg[:-1]):raise ValueError('nonterminal full demand')
        uu=[(r['occurrence'],k,b) for r in seg for k in range(1,r['a']+1) for b in (0,1)]
        dd=[(r['occurrence'],k) for r in seg for k in range(1,r['qF']+1)]
        result.append({'occurrences':[r['occurrence'] for r in seg],
            'H':len(uu)//2,'Q':len(dd),'units':uu,'demands':dd})
    assert sorted(t for v in result for t in v['occurrences'])==sorted(r['occurrence'] for r in rows)
    return result
def independent_full(rows):
    mm=macros(rows);h0={};R=[];spares=[];D=set();U=set();critical=[]
    for i,m in enumerate(mm):
        if m['H']<1 or m['Q']>3:raise ValueError('not certified core7 macro costs')
        n=min(len(m['units']),len(m['demands']))
        h0.update(zip(m['demands'][:n],m['units'][:n]));R+=m['demands'][n:]
        D.update(m['demands']);U.update(m['units'])
        if len(m['units'])>len(m['demands']):spares.append((i,m['units'][len(m['demands'])]))
        if len(m['demands'])>len(m['units']):critical.append(i)
    if len(R)!=1 or len(critical)!=1:raise ValueError('requires EXACTLY one actual excess slot')
    k=critical[0]
    if (mm[k]['H'],mm[k]['Q'])!=(1,3):raise ValueError('wrong one-slot class')
    if mm[(k-1)%len(mm)]['Q']>1:raise ValueError('violates proved actual-source Hamiltonian predecessor condition')
    if not spares:raise ValueError('zero-surplus contradicts actual core7 source theorem')
    # Choose the FIRST positive packet in the given cyclic macro order,
    # not necessarily the preceding one, and keep exact event/bit identity.
    spare_packet,spare=spares[0];h=dict(h0);h[R[0]]=spare
    assert set(h)==D and len(set(h.values()))==len(h) and set(h.values())<=U
    return {'D':D,'U':U,'h0':h0,'R':R[0],'h':h,'macros':mm,
        'critical_macro':k,'preceding_macro':(k-1)%len(mm),'seed_spare_macro':spare_packet,'seed_spare':spare,
        'source_positive_surplus':sum(max(2*m['H']-m['Q'],0) for m in mm)}
def extend_one(D,U,paid,h):
    D=set(D);U=set(U)
    if set(h)!=D or not set(paid)<=D:raise ValueError('demand domain')
    for mapping in (paid,h):
        if len(set(mapping.values()))!=len(mapping) or not set(mapping.values())<=U:raise ValueError('donor duplicate or outside actual period')
    missing=D-set(paid)
    if not missing:return {'allocation':dict(paid),'missing':None,'unit':None,'path':[]}
    if len(missing)!=1:raise ValueError('one-hole theorem only')
    p=next(iter(missing));inverse={u:d for d,u in paid.items()};d=p;seen=set();path=[]
    while True:
        if d in seen:raise AssertionError('injective source maps forbid entered cycles')
        seen.add(d);u=h[d];path.append((d,u))
        if u not in inverse:break
        d=inverse[u]
    answer=dict(paid);answer[p]=u
    assert set(answer)==D and len(set(answer.values()))==len(answer)
    assert all(answer[d]==v for d,v in paid.items())
    return {'allocation':answer,'missing':p,'unit':u,'path':path}
def from_frozen_auxiliary(rows,fE):
    """Use a SUPPLIED certified actual fE; never synthesize its debt/owners.
    Actual source membership, BE rows, alignment and Step1 certificate are
    input premises. This validates the physical ID interface and preserves
    every pulled-back common value, then freezes ALL partial full owners.
    """
    import importlib.util
    from pathlib import Path
    build=independent_full(rows);D,U=build['D'],build['U']
    E={(r['occurrence'],k) for r in rows for k in range(1,r['qE']+1)}
    if set(fE)!=E or len(set(fE.values()))!=len(fE) or not set(fE.values())<=U:
        raise ValueError('not the certified actual auxiliary physical map on this period')
    common=D&E;locked={d:fE[d] for d in common}
    old=Path(__file__).resolve().parent.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py'
    spec=importlib.util.spec_from_file_location('accepted_partial_exchange10',old)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    prior=m.exchange(D,U,locked,build['h0']);a=prior['allocation']
    assert len(prior['uncovered'])<=1
    extension=extend_one(D,U,a,build['h'])
    if extension['missing'] is not None:
        missing=extension['missing']
        anchor=missing if missing==build['R'] else prior['blocked'][missing]['owner']
        assert anchor==build['R']
    else:anchor=None
    assert all(extension['allocation'][d]==fE[d] for d in common)
    return {'build':build,'prior':prior,'extension':extension,'anchor':anchor,'common':common,
        'auxiliary_only':E-D,'full_only':D-E,'frozen_fE_modified':False}
