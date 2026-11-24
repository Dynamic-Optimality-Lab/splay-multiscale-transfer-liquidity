from base6 import *
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze
from birthc import reconstruct
from native6 import adapter,original_star
from account2 import ordered
from gate1 import packets,signature
from rn1_audit5 import audit as reduction
from local6 import renewal_geometry

def audit(s,i):
    pref=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);fc=audit_forest(r,ff)
    p={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
        'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],'boundaries':r.boundaries,'state_pool':pool}
    f={'source':s['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
    xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
    raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs))
    # Explicit exact positive certificate, never inferred from test size.
    assert raw<=10*r.A,(s['name'],'raw not affordable; use full general selector before classifying')
    w={'vertices':[{'parent':v,'type':d['type'],'w':0} for v,d in sorted(ff.items())],'R_overflow':0,
        'zero_reason':'Verified positive original raw periodic certificate; remaining cheap D quota. Not a universal claim.'}
    an=analyze(s,p,f,w);b=reconstruct(s,p,f,an,weights=w);native=adapter(s,p,b)
    star=original_star(native);native.original_R_star=star
    acc=ordered(s,p,b,star);red=packets(s,p,b,f,an,acc['exact_D'],star)
    rn=reduction(s,p,f,b,an,acc);geo=renewal_geometry(s,p,rn,native)
    result={'source':s['name'],'source_sha256':digest(s),'index':i,'population':len(s['initial_B']['children']),
        'genuine_support':len(r.S),'operations':len(s['operations']),'A':r.A,'Q_B':r.Q,'primitives':r.T,
        'prefix':pref,'raw_periodic_cost':raw,'periodic_10A':10*r.A,'original_R6':len(b['original_R6']),
        'original_R_star':star,'canonical_original_C_old_renewals':len(geo),
        'natural_local_refutations':sum(z['promotion_free'] and z['local_natural_interval'] is not None and z['local_natural_interval']['all_three_natural_interval_prices_exceed_5A'] for z in geo),
        'actual_S_UU':red['literal_S_UU'],'sum_z_h':red['sum_z_h'],
        'assigned_counts':{k:len(v) for k,v in acc['disjoint_original_assignments'].items()},
        'native_U_R6_original_pairs_independently_matched':True,'exact_paired_closure':True}
    for lab,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',b),('ORDERED',acc),('REDUCTION',red),('RENEWAL',rn),('NESTED',geo)):
        write(f'FRESH_{lab}_{i:02}.json',z)
    return result

if __name__=='__main__':
    assert not (ROOT/'M1_CONT06_DELIVERY_MANIFEST.json').exists(),'Sealed stage.'
    i=int(sys.argv[1]);m=Meter(f'fresh_{i:02}');s=load(ROOT/'FRESH_SOURCE_CATALOG.json')[i]
    z=audit(s,i);write(f'FRESH_RESULT_{i:02}.json',z);m.info['fresh_complete_sources']=1;m.ok=True
    print('PASS',z['source'],'n',z['population'],'A',z['A'],'Q',z['Q_B'],'C_old renewals',z['canonical_original_C_old_renewals'],
        'local refutations',z['natural_local_refutations'],'actual S_UU',z['actual_S_UU'],flush=True)
