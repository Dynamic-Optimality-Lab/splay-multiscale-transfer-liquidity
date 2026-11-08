"""Actual-ID arbitrary finite owner exchange and core7 source constructor."""
import importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=load('sealed11_macros13',B.parent/'SE03_STEP2_CORE7_SINGLE_EXCESS_11/single_slot_allocator.py')
X=load('sealed10_exchange13',B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py')
def own_map(rows):
    mm=M.macros(rows);D=set();U=set();h0={};R=set()
    for m in mm:
        n=min(len(m['units']),len(m['demands']));h0.update(zip(m['demands'][:n],m['units'][:n]))
        D.update(m['demands']);U.update(m['units']);R.update(m['demands'][n:])
    return {'D':D,'U':U,'h0':h0,'R':R,'macros':mm}
def core7(rows):
    v=own_map(rows);mm=v['macros'];h=dict(v['h0']);seeds=[]
    for c,m in enumerate(mm):
        if m['H']<1 or m['Q']>3:raise ValueError('not natural core7 source costs')
        if m['Q']<=2*m['H']:continue
        b=(c-1)%len(mm);pre=mm[b]
        if (m['H'],m['Q'])!=(1,3) or pre['Q']>1:raise ValueError('actual Hamiltonian predecessor condition')
        r=m['demands'][2];u=pre['units'][pre['Q']];h[r]=u
        seeds.append({'critical_macro':c,'predecessor_macro':b,'slot':r,'seed':u})
    assert len(seeds)==len(v['R']) and len({s['predecessor_macro'] for s in seeds})==len(seeds)
    assert len({s['seed'] for s in seeds})==len(seeds)
    assert set(h)==v['D'] and len(set(h.values()))==len(h) and set(h.values())<=v['U']
    assert all(h[d]==u for d,u in v['h0'].items())
    v.update({'h':h,'seeds':seeds,'Splus':sum(max(2*m['H']-m['Q'],0) for m in mm)})
    return v
def extend(D,U,a,h):
    D,U=set(D),set(U)
    if set(h)!=D or not set(a)<=D:raise ValueError('demand domain')
    for f in (a,h):
        if len(set(f.values()))!=len(f) or not set(f.values())<=U:raise ValueError('duplicate/outside actual physical unit')
    inverse={u:d for d,u in a.items()};paths=[];add={};seen=set()
    for p in sorted(D-set(a)):
        d=p;path=[]
        while True:
            if d in seen:raise AssertionError('injectivity forbids entered cycle/meeting')
            seen.add(d);u=h[d];path.append((d,u))
            if u not in inverse:break
            d=inverse[u]
        add[p]=u;paths.append({'root':p,'steps':path,'terminal_unit':u})
    ans={**a,**add};assert set(ans)==D and len(set(ans.values()))==len(ans)
    return {'allocation':ans,'additions':add,'paths':paths,'old_values_fixed':True}
def with_owners(v,E,fE):
    D,U=v['D'],v['U'];E=set(E)
    if set(fE)!=E or len(set(fE.values()))!=len(fE) or not set(fE.values())<=U:raise ValueError('actual certified fE IDs')
    C=D&E;l={d:fE[d] for d in C};prior=X.exchange(D,U,l,v['h0']);a=prior['allocation']
    result=extend(D,U,a,v['h']);licensed=X.exchange(D,U,l,v['h'])
    assert result['allocation']==licensed['allocation'] and licensed['total']
    pp={z['root']:z for z in licensed['paths']};assert all(pp[z['root']]==z for z in prior['paths'])
    alpha={p:p if p in v['R'] else prior['blocked'][p]['owner'] for p in D-set(a)}
    assert set(alpha.values())<=v['R'] and len(set(alpha.values()))==len(alpha)
    return {'prior':prior,'extension':result,'anchors':alpha,'common':C,'licensed':licensed}
