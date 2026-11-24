"""Correct JSON list/tuple normalization in the reference comparison only."""
from gate1 import *

def audited(s,p,b,f,an,z,star):
    row=packets(s,p,b,f,an,z['exact_D'],star)
    refs={q['h']:q for q in z['quota_rows']}
    assert set(refs)=={q['h'] for q in row['packets']}
    for q in row['packets']:
        ref=refs[q['h']];ps=ref.get('parents',ref.get('distinct_original_parents'))
        assert [list(v) for v in q['ordered_distinct_D_parents']]==ps
        assert [list(v) for v in q['selected_by_original_quota']]==ref['selected']
    assert row['literal_S_UU']==[]
    return row

if __name__=='__main__':
    m=Meter('gate1_exact_packet_reduction');out=[]
    records=load(M0/'RESIDUAL_AUDIT.json');old=load(M0/'SOURCE_CATALOG.json')
    for i,z in enumerate(records):
        if 'exact_D' not in z:continue
        s=old[i]['source'];p=load(M0/f'PHYS_{i:02}.json');b=load(C1/f'BIRTH_{i:02}.json')
        f=load(M0/f'FOREST_{i:02}.json');an=load(M1/f'HISTORICAL_AUDIT_{i:02}.json')
        row=audited(s,p,b,f,an,z,z['original_R_star'])
        out.append({'scope':'Exact sealed M0 D, not prehybrid R_star','index':i,**row})
        del p,b,f,an;gc.collect()
    ss=load(C2/'RUN_B_SOURCE_CATALOG.json')
    for i in (0,1,2):
        z=load(C2/f'ORDERED_{i:02}.json');s=ss[i]
        p=load(C2/f'RUN_B_PHYS_{i:02}.json');b=load(C2/f'RUN_B_BIRTH_{i:02}.json')
        f=load(C2/f'RUN_B_FOREST_{i:02}.json');an=load(C2/f'RUN_B_M1_AUDIT_{i:02}.json')
        row=audited(s,p,b,f,an,z,z['native_original_R_star'])
        out.append({'scope':'Exact sealed C2 original D after frozen selectors','index':i,**row})
    write('GATE1_AUDIT.json',{'exact_source_packet_audits':out,'D_gaps_total':sum(len(z['literal_D_original_rho']) for z in out),
        'original_index_late_but_D_selected_total':sum(len(z['original_index_late_but_original_D_rank_selected']) for z in out),
        'universal_proof':'GATE1_EXACT_REDUCTION.md','weighted_identity_passed':True,
        'packing_proved':False,'positive_S_UU_claimed':False,
        'administrative_correction':'Reference JSON arrays normalized from reconstructed Python tuples; no order or selector changed.'})
    m.ok=True;print('PASS Gate1 exact original D/order/fiber reduction',len(out),'source audits',flush=True)
