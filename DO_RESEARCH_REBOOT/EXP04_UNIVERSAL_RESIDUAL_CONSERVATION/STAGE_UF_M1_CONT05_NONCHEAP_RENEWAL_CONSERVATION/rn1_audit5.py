from base5 import *
from residual0 import E_stream,gap_costs
from gate1 import signature

def audit(s,p,f,b,an,acc):
    C=acc['C_old'];E={digest(z['rho']) for z in acc['E_old']};assert E=={digest(z['rho']) for z in E_stream(p,C)}
    ds={tuple(z['parent']):z for z in p['doubles']};vs={tuple(z['parent']):z for z in f['vertices']}
    sig=signature(p,b,f,an);gs=gap_costs(s,p['boundaries']);T=len(p['events'])
    groups=defaultdict(list)
    for z in C:groups[tuple(z['original_parent'])].append(z)
    lastA={};lastC={};out=[]
    for lap in range(2):
        for row in p['boundaries']:
            for e in p['events'][row['start_time']:row['post_A_time']]:lastA[e['pivot']]=tuple(e['id']);lastC.pop(e['pivot'],None)
            for v in sorted(v for v in groups if v[0]==row['t']):
                g=ds[v]['g'];earlier=lastC.get(g);has=g in lastA
                if lap:
                    selected=all(digest(z['rho']) in E for z in groups[v])
                    assert selected==(has and earlier is None)
                    if not selected:
                        assert earlier is not None # no-reset cyclic singleton is a preceding-lap same-ID copy
                        u,oldlap=earlier;assert ds[u]['g']==g and u[1]>2*gs[u[0]]
                        out.append({'later_parent':v,'earlier_parent':u,'old_g':g,'A_epoch_donor':lastA.get(g),
                            'earlier_lap_offset':oldlap-lap,'same_original_parent_copy':u==v,
                            'earlier_forest_type':vs[u]['type'],'later_forest_type':vs[v]['type'],
                            'earlier_sigma':u in sig,'later_sigma':v in sig,
                            'later_original_C_old_rhos':[z['rho'] for z in groups[v]],
                            'earlier_original_C_old_rhos':[z['rho'] for z in groups[u]],
                            'actual_later_D_rhos':[z['rho'] for z in acc['exact_D'] if tuple(z['original_parent'])==v]})
                lastC[g]=(v,lap)
    return {'source':s['name'],'source_sha256':digest(s),'C_old_parents':len(groups),'C_old_gaps':len(C),
        'E_old_gaps':len(E),'canonical_renewals':out,'canonical_renewals_count':len(out),
        'resetless_renewals':sum(z['A_epoch_donor'] is None for z in out),
        'scope':'Exact ORIGINAL C_old and E_old, before H/quota; no positive actual S_UU inferred.'}

if __name__=='__main__':
    m=Meter('RN1_exact_predecessor_reduction');entries=[]
    for i,z in enumerate(load(M0/'RESIDUAL_AUDIT.json')):
        if 'C_old' in z:
            s=load(M0/'SOURCE_CATALOG.json')[i]['source']
            entries.append((s,M0/f'PHYS_{i:02}.json',M0/f'FOREST_{i:02}.json',C1/f'BIRTH_{i:02}.json',M1/f'HISTORICAL_AUDIT_{i:02}.json',z))
    for i in range(3):
        s=load(C2/'RUN_B_SOURCE_CATALOG.json')[i]
        entries.append((s,C2/f'RUN_B_PHYS_{i:02}.json',C2/f'RUN_B_FOREST_{i:02}.json',C2/f'RUN_B_BIRTH_{i:02}.json',C2/f'RUN_B_M1_AUDIT_{i:02}.json',load(C2/f'ORDERED_{i:02}.json')))
    for root,stem in ((C3,'NEW'),(C3,'PROTECTED'),(C4,'DEFORM'),(C4,'SHARED')):
        for i,s in enumerate(load(root/f'{stem}_SOURCE_CATALOG.json')):
            entries.append((s,root/f'{stem}_PHYS_{i:02}.json',root/f'{stem}_FOREST_{i:02}.json',root/f'{stem}_BIRTH_{i:02}.json',root/f'{stem}_M1_AUDIT_{i:02}.json',load(root/f'{stem}_ORDERED_{i:02}.json')))
    s=load(C4/'PROBE_SHORT_SOURCE.json');entries.append((s,C4/'PROBE_SHORT_PHYS.json',C4/'PROBE_SHORT_FOREST.json',C4/'PROBE_SHORT_BIRTH.json',C4/'PROBE_SHORT_M1_AUDIT.json',load(C4/'PROBE_SHORT_ORDERED.json')))
    out=[]
    for s,pp,fp,bp,ap,z in entries:
        out.append(audit(s,load(pp),load(fp),load(bp),load(ap),z));gc.collect()
    write('RN1_REDUCTION_AUDIT.json',out);m.info['complete_original_accounting_audits']=len(out);m.ok=True
    print('PASS exact original C_old/E_old canonical reduction on',len(out),'sources; renewals',sum(z['canonical_renewals_count'] for z in out),flush=True)
