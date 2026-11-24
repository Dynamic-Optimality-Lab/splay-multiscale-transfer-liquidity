from base4 import *
from residual0 import gap_costs
from gate1 import signature
from expand_events2 import expanded as oldexpanded

def stream_audit(source,gs,doubles,event_factory,A,sigma=()):
    last={};seen={};chosen={};sigma=set(sigma);RA=0;noncheap=set();parentg={tuple(z['parent']):z['g'] for z in doubles}
    for lap in range(2):
        if lap:RA=0
        for e in event_factory():
            if e['actor']=='A':
                last[e['pivot']]=tuple(e['id']);seen[e['pivot']]=False;RA+=1
            elif e['case']!='ZIG' and e['id'][3]==0:
                v=tuple(e['id'][1:3]);g=parentg[v]
                if v[1]<=2*gs[v[0]]:continue
                if lap:noncheap.add(v)
                if lap and g in last and not seen.get(g,False):chosen[v]=last[g]
                seen[g]=True
    donors=list(chosen.values());assert len(donors)==len(set(donors))
    loads=Counter(q[:3] for q in donors);assert max(loads.values(),default=0)<=2
    assert len(chosen)<=RA<=2*A
    late_sigma={v for v in sigma if v in noncheap}
    return {'source':source['name'],'source_sha256':digest(source),'A':A,'real_A_bits':RA,'B_doubles':len(parentg),
        'E_phys':[{'parent':v,'g':parentg[v],'actual_A_donor':chosen[v]} for v in sorted(chosen)],
        'E_phys_count':len(chosen),'maximum_parent_load_per_actual_A_bit':1 if chosen else 0,
        'maximum_parent_load_per_actual_A_StepEv':max(loads.values(),default=0),'physical_gap_bound':3*len(chosen),'global_budget':6*A,
        'physical_late_sigma_parents':sorted(late_sigma),'late_sigma_not_first_noncheap':sorted(late_sigma-set(chosen)),
        'actual_residual_claim':'No actual S_UU membership inferred from a physical column count.'}

def standard(e):
    s=e['source'];p=load(e['physical']);ds=p['doubles'];gs=gap_costs(s,p['boundaries']);A=sum(z['a'] for z in p['boundaries'])
    def path(key,suffix):return Path(e.get(key,str(e['physical']).replace('PHYS',suffix)))
    bp,fp,ap=path('birth','BIRTH'),path('forest','FOREST'),path('M1_audit','M1_AUDIT')
    sigma=()
    if all(q.exists() for q in (bp,fp,ap)):
        b,f,an=load(bp),load(fp),load(ap);sigma=signature(p,b,f,an)
    r=stream_audit(s,gs,ds,lambda:iter(p['events']),A,sigma);r['origin']=e['origin'];r['signature_available']=bool(sigma) or all(q.exists() for q in (bp,fp,ap))
    if e.get('critical_h'):
        h=e['critical_h'];selected={tuple(z['parent']) for z in r['E_phys']}
        relevant={v for v in sigma if v[0]==h and v[1]>2*gs[h]}
        assert relevant<=selected,(s['name'],relevant-selected)
        r['critical_deep_UU_late_parents']=sorted(relevant)
        if e.get('ordered'):
            acc=load(e['ordered']);F={digest(z['rho']) for k in ('carrier','skipped_rank') for z in acc['disjoint_original_assignments'][k]}
            E={digest(z['rho']) for z in acc['E_old']}
            for z in acc['native_original_R_star']:
                if tuple(z['original_parent']) in selected and digest(z['rho']) not in F:
                    assert digest(z['rho']) in E
            r['known_original_star_E_phys_implication_checked']=True
    del p;gc.collect();return r

if __name__=='__main__':
    m=Meter('global_physical_corridor_audit');catalog=load(C3/'CONTROL_REFERENCE_CATALOG.json');out=[]
    for e in catalog:
        if e.get('expansion'):
            s=e['source'];p=load(C2/'BOOST_SHORT_PHYS.json');rule=load(C2/'BOOST_EVENT_EXPANSION.json')
            fast=load(C2/'BOOST_LONG_FAST_STATES.json');gs={z['t']:z['A_gap'] for z in fast['rows'] if z['tag']=='K'}
            r=stream_audit(s,gs,p['doubles'],lambda:oldexpanded(p,rule),sum(z['a'] for z in fast['rows']))
            r.update(origin=e['origin'],signature_available=False,scope='Exact inherited long event expansion; no new long native classification.')
        else:r=standard(e)
        out.append(r);write('PHYSICAL_CORRIDOR_RESULTS.json',out)
    for stem in ('DEFORM','SHARED'):
        for i,s in enumerate(load(ROOT/f'{stem}_SOURCE_CATALOG.json')):
            e={'source':s,'physical':str(ROOT/f'{stem}_PHYS_{i:02}.json'),'origin':'C4_'+stem,
                'critical_h':s['critical_operation'],'ordered':str(ROOT/f'{stem}_ORDERED_{i:02}.json')}
            r=standard(e);out.append(r);write('PHYSICAL_CORRIDOR_RESULTS.json',out)
    s=load(ROOT/'PROBE_SHORT_SOURCE.json')
    e={'source':s,'physical':str(ROOT/'PROBE_SHORT_PHYS.json'),'origin':'C4_probe_short',
        'critical_h':s['critical_operation'],'ordered':str(ROOT/'PROBE_SHORT_ORDERED.json')}
    out.append(standard(e));write('PHYSICAL_CORRIDOR_RESULTS.json',out)
    m.info['complete_source_audits']=len(out);m.ok=True
    print('PASS physical first-noncheap corridor on',len(out),'complete original words, all literal A donor loads<=2 per StepEv',flush=True)
