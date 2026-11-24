from base4 import *
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze,Edges
from birthc import reconstruct
from native4 import adapter,original_star
from account2 import ordered
from gate1 import signature,packets
from residual0 import gap_costs
from fast_physics import physical_replay,skeleton_cost

if __name__=='__main__':
    m=Meter('protected_large_original_audit');s=load(ROOT/'PROBE_SHORT_SOURCE.json');pref=prefix_check(s)
    r,pool=replay(s);ff=scan_forest(r);fc=audit_forest(r,ff)
    p={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
        'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],
        'boundaries':r.boundaries,'state_pool':pool}
    f={'source':s['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
    a=Edges(s['initial_A']);bad=set(s['protected_labels']);internal=0;extreme=1|(1<<(s['n']-1))
    assert not bad.intersection(a.m[1:])
    for e in r.events:
        if e['actor']=='A':a.step(e);assert not bad.intersection(a.m[1:]);internal+=any(lab and not lab&extreme for lab in a.m[1:])
    xs=[x for tag,x in s['operations'] if tag=='K'];raw=sum((x!=xs[j-1])+abs(x-xs[j-1]).bit_length() for j,x in enumerate(xs))
    assert raw<=10*r.A
    w={'vertices':[{'parent':v,'type':d['type'],'w':0} for v,d in sorted(ff.items())],'R_overflow':0,
        'zero_reason':'Short source has a positive original raw periodic certificate; cheap quota unchanged.'}
    an=analyze(s,p,f,w);b=reconstruct(s,p,f,an,weights=w);native=adapter(s,p,b)
    for lab,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',b)):write('PROBE_SHORT_'+lab+'.json',z)
    print('PASS protected518 independent physical/Pi/U/cohort/R6, A',r.A,'R6',len(b['original_R6']),flush=True)
    star=original_star(native);acc=ordered(s,p,b,star);red=packets(s,p,b,f,an,acc['exact_D'],star)
    sig=signature(p,b,f,an);h=s['critical_operation'];gs=gap_costs(s,p['boundaries'])
    critical=[v for v in sig if v[0]==h]
    for lab,z in (('ORDERED',acc),('REDUCTION',red)):write('PROBE_SHORT_'+lab+'.json',z)
    fast=physical_replay(s);norms=[skeleton_cost(fast,variant=v) for v in ('G','H')]
    assert all(z['eligible_periodic'] for z in norms)
    result={'source':s['name'],'source_sha256':digest(s),'prefix':pref,'A':r.A,'Q_B':r.Q,'operations':len(s['operations']),
        'primitives':r.T,'raw_periodic_cost':raw,'original_R_star':star,'original_R6':len(b['original_R6']),
        'critical':{'h':h,'A_gap':gs[h],'N_h':len(critical),'sigma_parents':critical,
            'R6_parents':sorted({tuple(z['parent']) for z in b['original_R6'] if z['parent'][0]==h}),
            'R_star_parents':sorted({tuple(z['original_parent']) for z in star if z['consumer']==h})},
        'G_H_periodic_certificates':norms,'A_internal_label_snapshots':internal,'actual_S_UU':red['literal_S_UU'],
        'assigned_counts':{k:len(v) for k,v in acc['disjoint_original_assignments'].items()},'full_native_original_R_star':True}
    write('PROBE_SHORT_RESULTS.json',result);m.ok=True
    print('PASS protected518 native R_star',len(star),'N',len(critical),'criticalR6parents',len(result['critical']['R6_parents']),flush=True)
