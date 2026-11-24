from base4 import *
from sources4 import initial_sources
from sources3 import vine
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze,Edges
from birthc import reconstruct
from native4 import adapter,original_star
from account2 import ordered
from gate1 import signature,packets
from residual0 import gap_costs
import exp04_core,exp04_monotone

def audit(s,i,stem='DEFORM'):
    pref=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);fc=audit_forest(r,ff)
    assert r.S==set(range(1,s['n']+1))
    edge=Edges(s['initial_A']);abits=0
    for e in r.events:
        if e['actor']=='A':
            edge.step(e);abits+=1;assert edge.code()==Edges(vine(s['n'],edge.root)).code()
    p={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
        'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],
        'boundaries':r.boundaries,'state_pool':pool}
    f={'source':s['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
    xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
    raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs))
    assert raw<=3*r.A
    w={'vertices':[{'parent':v,'type':d['type'],'w':0} for v,d in sorted(ff.items())],
        'R_overflow':0,'zero_reason':'Every real A primitive is split-vine; inherited source-uniform raw<=3A. Noncheap hybrid-paid; cheap packet quota.'}
    an=analyze(s,p,f,w);b=reconstruct(s,p,f,an,weights=w);native=adapter(s,p,b);star=original_star(native)
    acc=ordered(s,p,b,star);red=packets(s,p,b,f,an,acc['exact_D'],star)
    sig=signature(p,b,f,an);gs=gap_costs(s,p['boundaries']);h=s['critical_operation']
    critical=[v for v in sig if v[0]==h]
    r6screen=[{'rho':z['rho'],'original_parent':z['parent'],'consumer':z['parent'][0],'type':'original_R6'} for z in b['original_R6']]
    eps,psi=exp04_core.psi_episodes(native);allmono=exp04_monotone.monotone_analysis(native,r6screen,eps)
    current=[z for z in star if z['consumer']==h]
    Fstar={digest(z['rho']) for k in ('carrier','skipped_rank') for z in acc['disjoint_original_assignments'][k]}
    Fr6={digest(z['rho']) for z in allmono['paid']}
    row={'index':i,'source':s['name'],'source_sha256':digest(s),'population':s['n'],'operations':len(s['operations']),
        'A':r.A,'Q_B':r.Q,'primitives':r.T,'prefix':pref,'A_splitvine_bits':abits,'raw_periodic_cost':raw,
        'original_R6_gaps':len(b['original_R6']),'original_R_star':star,
        'critical':{'h':h,'A_gap':gs[h],'physical_N_h':len(critical),'sigma_parents':sorted(critical),
            'R6_parents':sorted({tuple(z['parent']) for z in b['original_R6'] if z['parent'][0]==h}),
            'R_star_parents':sorted({tuple(z['original_parent']) for z in current}),
            'R6_gaps':[z for z in b['original_R6'] if z['parent'][0]==h],
            'R_star_gaps':current,'R_star_gaps_outside_F':[z for z in current if digest(z['rho']) not in Fstar],
            'R6_gaps_outside_skipped':[z for z in r6screen if z['consumer']==h and digest(z['rho']) not in Fr6],
            'actual_D_parents':[v for q in red['packets'] if q['h']==h for v in q['ordered_distinct_D_parents']],
            'z_h':next((q['z_h'] for q in red['packets'] if q['h']==h),0)},
        'assigned_counts':{k:len(v) for k,v in acc['disjoint_original_assignments'].items()},
        'actual_S_UU':red['literal_S_UU'],'sum_z_h':red['sum_z_h'],
        'periodic_status':'Raw positive, local fallback inactive; no claim that G/H/local fail.'}
    for lab,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',b),('ORDERED',acc),('REDUCTION',red),('R6_MONOTONE',allmono)):
        write(f'{stem}_{lab}_{i:02}.json',z)
    assert not red['literal_S_UU']
    return row

if __name__=='__main__':
    meter=Meter('controlled_deformations');ss=initial_sources();assert len(ss)==10
    write('DEFORM_SOURCE_CATALOG.json',ss);out=[]
    for i,s in enumerate(ss):
        row=audit(s,i);out.append(row);write('DEFORM_RESULTS.json',out)
        c=row['critical'];print('PASS',i,'keys',s['n'],'h',c['h'],'N',c['physical_N_h'],'a',c['A_gap'],
            'R6parents',len(c['R6_parents']),'starparents',len(c['R_star_parents']),'starOutsideF',len(c['R_star_gaps_outside_F']),
            'R6outsideSkip',len(c['R6_gaps_outside_skipped']),'actualZ',c['z_h'],flush=True);gc.collect()
    meter.info['fresh_complete_sources']=len(out);meter.ok=True
