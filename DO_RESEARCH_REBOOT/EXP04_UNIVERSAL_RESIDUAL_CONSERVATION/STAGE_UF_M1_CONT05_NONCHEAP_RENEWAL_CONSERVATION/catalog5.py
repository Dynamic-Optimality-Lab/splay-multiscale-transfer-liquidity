from base5 import *
from expand_events2 import expanded as expand_old
from replication_audit4 import old_boundaries
from probe_long4 import expanded as expand_new,expanded_boundaries
from residual0 import gap_costs

def entries(include_new=True):
    out=load(C3/'CONTROL_REFERENCE_CATALOG.json')
    for stem in ('DEFORM','SHARED'):
        for i,s in enumerate(load(C4/f'{stem}_SOURCE_CATALOG.json')):
            out.append({'source':s,'physical':str(C4/f'{stem}_PHYS_{i:02}.json'),'origin':'C4_'+stem})
    out.append({'source':load(C4/'PROBE_SHORT_SOURCE.json'),'physical':str(C4/'PROBE_SHORT_PHYS.json'),'origin':'C4_probe_short'})
    out.append({'source':load(C4/'PROBE_LONG_SOURCE.json'),'physical':None,'origin':'C4_probe_long','new_expansion':True})
    if include_new:
        for stem in ('NEW','RENEW'):
            for i,s in enumerate(load(ROOT/f'{stem}_SOURCE_CATALOG.json')):
                out.append({'source':s,'physical':str(ROOT/f'{stem}_PHYS_{i:02}.json'),'origin':'C5_'+stem})
    return out

def data(e):
    delta=0
    if e.get('new_expansion'):
        pp=C4/'PROBE_SHORT_PHYS.json';p=load(pp);rule=load(C4/'PROBE_EVENT_EXPANSION.json');delta=2*(rule['copies_in_long']-1)
        rows=list(expanded_boundaries(p,rule));events=lambda:expand_new(p,rule)
    elif e.get('expansion'):
        pp=C2/'BOOST_SHORT_PHYS.json';p=load(pp);rule=load(C2/'BOOST_EVENT_EXPANSION.json')
        rows=list(old_boundaries(p,rule));events=lambda:expand_old(p,rule)
    else:pp=Path(e['physical']);p=load(pp);rows=p['boundaries'];events=lambda:iter(p['events'])
    fp=Path(e.get('forest',str(pp).replace('PHYS','FOREST')));f=load(fp)
    ds={tuple(z['parent']):z for z in p['doubles']};vs={tuple(z['parent']):z for z in f['vertices']}
    if delta:
        ds={(v[0]+delta,v[1]):{**z,'parent':[v[0]+delta,v[1]]} for v,z in ds.items()}
        vs={(v[0]+delta,v[1]):{**z,'parent':[v[0]+delta,v[1]]} for v,z in vs.items()}
    gs=gap_costs(e['source'],rows);A=sum(z['a'] for z in rows)
    return p,rows,events,ds,vs,gs,A
