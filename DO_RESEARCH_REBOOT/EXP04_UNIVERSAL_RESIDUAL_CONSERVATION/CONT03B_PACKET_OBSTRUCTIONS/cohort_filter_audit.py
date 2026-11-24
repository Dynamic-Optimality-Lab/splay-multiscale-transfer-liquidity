from campaign3b import *


def label(r,v):
    xs=r.label_keys(v)
    return {'min':min(xs),'max':max(xs),'size':len(xs)} if xs else {'size':0}


if __name__=='__main__':
    meter=Meter('cohort_filter_audit')
    s=json.loads((ROOT/'COHORT_SOURCES.json').read_text())[0];r=Replay(s)
    pairs=[p for p in r.pairs if p['rho'][0] in (646,649,652)]
    details=[]
    for p in pairs:
        ds=[]
        for key in map(tuple,p['rho'][1:]):
            d=r.U[key];lo,hi=d['nu'],d['hit_time'];hits=[]
            for ev in r.events:
                if ev['actor']=='A' and d['J'] in ev['created']:
                    lifted=ev['time'] if ev['time']>lo else ev['time']+r.T
                    if lo<lifted<=hi:hits.append(ev['id'])
            ds.append({'id':key,'g':d['g'],'F':label(r,d['F']),'J':label(r,d['J']),
                'future_hit':d['h'],'exposed':d['exposed'],'actual_A_creations_of_J_before_hit':hits})
        parent=tuple(p['parent']);d=r.U.get(parent)
        details.append({'pair':p,'endpoint_certificates':ds,'parent_g':r.doubles[parent]['g'],
            'parent_in_U':d is not None,'parent_future_hit':d['h'] if d else None,
            'parent_future_cohort':[list(k) for k in r.cohorts[d['h']]] if d else [],
            'actual_A_path':r.boundaries[parent[0]-1]['A_path'],
            'actual_B_path':r.boundaries[parent[0]-1]['B_path']})
    write('COHORT_FILTER_AUDIT.json',{'source':s['name'],'details':details,'all_pair_classes':dict(r.counts),
        'full_original_source_replayed':True,'independent_original_operations':r.independent_checks})
    print('packet classes',[(p['pair']['rho'],p['pair']['class'],p['parent_g']) for p in details],flush=True)
    for p in details:
        if p['pair']['rho'][0]==652:print(p,flush=True)
    meter.success=True
