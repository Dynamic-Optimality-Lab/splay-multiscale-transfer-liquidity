"""Exactly-two-slot core7 source funding, no matching/debt oracle.
Source membership, original replay, certified fE and legal I are premises.
All donor/demand labels are actual source IDs in ONE actual aligned I.
"""
import importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
_one=load('sealed11_macro_partition',B.parent/'SE03_STEP2_CORE7_SINGLE_EXCESS_11/single_slot_allocator.py')
_exchange=load('sealed10_actual_exchange',B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py')
def independent_full(rows):
    mm=_one.macros(rows);h0={};R=[];critical=[];D=set();U=set()
    for i,m in enumerate(mm):
        if m['H']<1 or m['Q']>3:raise ValueError('outside core7 natural-macro source costs')
        n=min(len(m['units']),len(m['demands']))
        h0.update(zip(m['demands'][:n],m['units'][:n]));R+=m['demands'][n:]
        D.update(m['demands']);U.update(m['units'])
        if m['Q']>2*m['H']:critical.append(i)
    if len(R)!=2 or len(critical)!=2:raise ValueError('requires EXACTLY TWO physical excess slots on actual I')
    seeds=[];h=dict(h0)
    for i in critical:
        m=mm[i];j=(i-1)%len(mm);prev=mm[j]
        if (m['H'],m['Q'])!=(1,3) or prev['Q']>1:
            raise ValueError('violates actual-source Hamiltonian predecessor condition')
        r=m['demands'][2];v=prev['units'][prev['Q']]
        assert v not in set(h0.values()) and r not in h0
        seeds.append({'critical_macro':i,'predecessor_macro':j,'anchor_slot':r,'seed_bit':v})
        h[r]=v
    assert len({s['predecessor_macro'] for s in seeds})==2
    assert len({s['seed_bit'] for s in seeds})==2
    assert not ({s['predecessor_macro'] for s in seeds}&set(critical))
    assert set(h)==D and set(h.values())<=U and len(set(h.values()))==len(h)
    return {'D':D,'U':U,'h0':h0,'R':set(R),'h':h,'macros':mm,'seeds':seeds,
        'source_positive_surplus':sum(max(2*m['H']-m['Q'],0) for m in mm)}
def extend_two(D,U,paid,h):
    """Walk against FIXED paid, then add all roots simultaneously.
    General graph fact is independent of source eligibility. For the actual
    partial10 map eligibility is licensed by the original-common exchange.
    """
    D=set(D);U=set(U)
    if set(h)!=D or not set(paid)<=D:raise ValueError('actual demand domain')
    for m in (h,paid):
        if len(set(m.values()))!=len(m) or not set(m.values())<=U:
            raise ValueError('duplicate or outside-period physical unit')
    missing=D-set(paid)
    if len(missing)>2:raise ValueError('two-residual theorem scope')
    inverse={u:d for d,u in paid.items()};paths=[];additions={};visited=set()
    for p in sorted(missing):
        d=p;local=set();path=[]
        while True:
            if d in local or d in visited:raise AssertionError('entered cycle or merging paths contradict injectivity')
            local.add(d);u=h[d];path.append((d,u))
            if u not in inverse:break
            d=inverse[u]
        visited|=local;additions[p]=u;paths.append({'root':p,'steps':path,'terminal_unit':u})
    assert not(set(additions.values())&set(paid.values()))
    assert len(set(additions.values()))==len(missing)
    result={**paid,**additions}
    assert set(result)==D and len(set(result.values()))==len(result)
    assert all(result[d]==u for d,u in paid.items())
    return {'allocation':result,'additions':additions,'missing':missing,'paths':paths,
        'all_old_values_fixed':True,'simultaneous_endpoints_distinct':True}
def from_frozen_auxiliary(rows,fE):
    """Caller supplies ACTUAL certified fE. Logical fixtures are not fE proofs."""
    build=independent_full(rows);D,U=build['D'],build['U']
    E={(r['occurrence'],k) for r in rows for k in range(1,r['qE']+1)}
    if set(fE)!=E or len(set(fE.values()))!=len(fE) or not set(fE.values())<=U:
        raise ValueError('not an actual auxiliary physical map on I')
    C=D&E;locked={d:fE[d] for d in C}
    prior=_exchange.exchange(D,U,locked,build['h0'])
    extension=extend_two(D,U,prior['allocation'],build['h'])
    anchors={p:p if p in build['R'] else prior['blocked'][p]['owner'] for p in extension['missing']}
    assert set(anchors.values())<=build['R'] and len(set(anchors.values()))==len(anchors)
    licensed=_exchange.exchange(D,U,locked,build['h'])
    assert licensed['total'] and licensed['allocation']==extension['allocation']
    newpaths={v['root']:v for v in licensed['paths']}
    assert all(newpaths[v['root']]==v for v in prior['paths'])
    assert all(extension['allocation'][d]==fE[d] for d in C)
    return {'build':build,'prior':prior,'extension':extension,'licensed':licensed,'anchors':anchors,
        'common':C,'full_only':D-E,'auxiliary_only':E-D,'frozen_fE_modified':False,
        'all_old_common_exchange_paths_identical':True}
