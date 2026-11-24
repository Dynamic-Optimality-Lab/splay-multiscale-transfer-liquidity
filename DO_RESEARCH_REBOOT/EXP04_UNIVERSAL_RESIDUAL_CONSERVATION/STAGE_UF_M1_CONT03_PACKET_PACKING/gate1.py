from base3 import *
from residual0 import gap_costs
import gc

def signature(p,b,f,an):
    U={ast.literal_eval(k):v for k,v in b['U'].items()};V={tuple(z['parent']):z for z in f['vertices']}
    depth={tuple(z['vertex']):z['distance'] for z in an['C_fringe_depths']}
    return {v for v,u in U.items() if V[v]['type']=='C' and depth[v]>2 and
        tuple(u['creator']) in U and not U[tuple(u['creator'])]['exposed']}

def packets(source,p,b,f,an,D,earlier_star=None,quota_reference=None):
    sigma=signature(p,b,f,an);gs=gap_costs(source,p['boundaries']);groups=defaultdict(lambda:defaultdict(list));ids=set()
    original_pairs={digest(z['rho']):z for z in b['original_R6']}
    for e in D:
        key=digest(e['rho']);assert key not in ids and key in original_pairs;ids.add(key)
        v=tuple(e['original_parent']);assert v==tuple(original_pairs[key]['parent'])
        groups[e['consumer']][v].append(e)
    if earlier_star is not None:assert ids<={digest(e['rho']) for e in earlier_star}
    rows=[];exactS=[];late=[];N={h:sum(v[0]==h for v in sigma) for h in gs}
    for h,gr in sorted(groups.items()):
        parents=sorted(gr);assert all(v[0]==h for v in parents)
        eligible=[];selected=[]
        for i,v in enumerate(parents,1):
            assert 1<=len(gr[v])<=3
            if i<=2*gs[h]:selected.append(v)
            if i>2*gs[h] and v in sigma:
                eligible.append(v);exactS.extend(e['rho'] for e in gr[v])
            if v[1]>2*gs[h] and i<=2*gs[h]:late.append({'parent':v,'D_rank':i,'A_gap':gs[h]})
        zh=len(eligible);weight=sum(len(gr[v]) for v in eligible)
        assert zh<=weight<=3*zh and zh<=N[h]
        rows.append({'h':h,'A_gap':gs[h],'ordered_distinct_D_parents':parents,
            'fiber_weights':{str(v):len(gr[v]) for v in parents},'sigma_parents_in_packet':[v for v in parents if v in sigma],
            'selected_by_original_quota':selected,'Z_h':eligible,'z_h':zh,'weighted_S_UU':weight,'N_h_all_physical':N[h]})
    if quota_reference is not None:
        ref={z['h']:z for z in quota_reference}
        assert set(ref)=={z['h'] for z in rows}
        for z in rows:
            q=ref[z['h']];ps=q.get('parents',q.get('distinct_original_parents'))
            assert z['ordered_distinct_D_parents']==ps and z['selected_by_original_quota']==q['selected']
    assert len(exactS)==sum(z['weighted_S_UU'] for z in rows)
    return {'source':source['name'],'source_sha256':digest(source),'literal_D_original_rho':[e['rho'] for e in D],
        'packets':rows,'sum_z_h':sum(z['z_h'] for z in rows),'literal_S_UU':exactS,
        'original_index_late_but_original_D_rank_selected':late}

if __name__=='__main__':
    m=Meter('gate1_exact_packet_reduction');out=[]
    records=load(M0/'RESIDUAL_AUDIT.json');old=load(M0/'SOURCE_CATALOG.json')
    for i,z in enumerate(records):
        if 'exact_D' not in z:continue
        s=old[i]['source'];p=load(M0/f'PHYS_{i:02}.json');b=load(C1/f'BIRTH_{i:02}.json')
        f=load(M0/f'FOREST_{i:02}.json');an=load(M1/f'HISTORICAL_AUDIT_{i:02}.json')
        row=packets(s,p,b,f,an,z['exact_D'],z['original_R_star'],z['quota_rows'])
        assert row['literal_S_UU']==[];out.append({'scope':'Exact sealed M0 D, not prehybrid R_star','index':i,**row})
        del p,b,f,an;gc.collect()
    ss=load(C2/'RUN_B_SOURCE_CATALOG.json')
    for i in (0,1,2):
        z=load(C2/f'ORDERED_{i:02}.json');s=ss[i]
        p=load(C2/f'RUN_B_PHYS_{i:02}.json');b=load(C2/f'RUN_B_BIRTH_{i:02}.json')
        f=load(C2/f'RUN_B_FOREST_{i:02}.json');an=load(C2/f'RUN_B_M1_AUDIT_{i:02}.json')
        row=packets(s,p,b,f,an,z['exact_D'],z['native_original_R_star'],z['quota_rows'])
        assert row['literal_S_UU']==[];out.append({'scope':'Exact sealed C2 original D after frozen selectors','index':i,**row})
    write('GATE1_AUDIT.json',{'exact_source_packet_audits':out,'D_gaps_total':sum(len(z['literal_D_original_rho']) for z in out),
        'original_index_late_but_D_selected_total':sum(len(z['original_index_late_but_original_D_rank_selected']) for z in out),
        'universal_proof':'GATE1_EXACT_REDUCTION.md','weighted_identity_passed':True,
        'packing_proved':False,'positive_S_UU_claimed':False})
    m.ok=True;print('PASS Gate1 exact original D/order/fiber reduction',len(out),'source audits',flush=True)
