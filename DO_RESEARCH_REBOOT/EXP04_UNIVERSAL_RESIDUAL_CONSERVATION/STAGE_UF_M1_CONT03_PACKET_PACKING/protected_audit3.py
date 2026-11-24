from base3 import *
from protected3 import sources
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze,Edges
from birthc import reconstruct
from native3 import adapter,original_star
from account2 import ordered
from gate1 import signature,packets
from residual0 import gap_costs
from fast_physics import physical_replay,skeleton_cost
import gc

if __name__=='__main__':
    meter=Meter('protected_fan_audit');ss=sources();write('PROTECTED_SOURCE_CATALOG.json',ss);out=[]
    for i,s in enumerate(ss):
        pref=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);fc=audit_forest(r,ff)
        assert r.S==set(range(1,s['n']+1))
        a=Edges(s['initial_A']);bad=set(s['protected_labels']);extreme=1|(1<<(s['n']-1));internal_snapshots=0
        for e in r.events:
            if e['actor']!='A':continue
            a.step(e);assert not (set(a.m[1:])&bad)
            internal_snapshots+=any(lab and not lab&extreme for lab in a.m[1:])
        p={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
            'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],
            'boundaries':r.boundaries,'state_pool':pool}
        f={'source':s['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
        xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
        raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs))
        if raw>10*r.A:
            fast=physical_replay(s);norms=[skeleton_cost(fast,variant=v) for v in ('G','H')]
            write(f'PROTECTED_PERIODIC_SCREEN_{i:02}.json',norms)
            if not any(z['eligible_periodic'] for z in norms):
                write(f'PROTECTED_UNCLASSIFIED_PHYS_{i:02}.json',p)
                raise RuntimeError('No positive periodic certificate at tested cut; residual remains unclassified, not zero.')
            # Full ordered() below uses the inherited raw-positive case only.
            raise RuntimeError('Positive normalized case needs a distinct exact ordered-selector adapter; do not misuse raw case.')
        w={'vertices':[{'parent':v,'type':d['type'],'w':0} for v,d in sorted(ff.items())],
            'R_overflow':0,'zero_reason':'Positive original raw periodic certificate; noncheap paid, cheap D quota-selected.'}
        an=analyze(s,p,f,w);b=reconstruct(s,p,f,an,weights=w);native=adapter(s,p,b);star=original_star(native)
        acc=ordered(s,p,b,star);red=packets(s,p,b,f,an,acc['exact_D'],star)
        sig=signature(p,b,f,an);gs=gap_costs(s,p['boundaries']);critical=[v for v in sig if v[0]==2]
        assert gs[2]==1 and len(critical)==s['s']//2
        r6ps={tuple(z['parent']) for z in b['original_R6'] if z['parent'][0]==2};assert len(r6ps)>=s['s']//4
        for lab,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',b),('ORDERED',acc),('REDUCTION',red)):
            write(f'PROTECTED_{lab}_{i:02}.json',z)
        row={'index':i,'source':s['name'],'source_sha256':digest(s),'s':s['s'],'reflection':s['full_reflection'],
            'population':s['n'],'operations':len(s['operations']),'A':r.A,'Q_B':r.Q,'primitives':r.T,'prefix':pref,
            'original_U':len(b['U']),'original_R6':len(b['original_R6']),'original_R_star':star,
            'critical':{'h':2,'A_gap':gs[2],'N_h':len(critical),'physical_silent_UU_parents':sorted(critical),
                'R6_parents':sorted(r6ps),'R_star_parents':sorted({tuple(e['original_parent']) for e in star if e['consumer']==2}),
                'actual_D_parents':[v for z in red['packets'] if z['h']==2 for v in z['ordered_distinct_D_parents']],
                'z_h':next((z['z_h'] for z in red['packets'] if z['h']==2),0)},
            'raw_periodic_cost':raw,'A_internal_label_snapshots':internal_snapshots,
            'assigned_counts':{k:len(v) for k,v in acc['disjoint_original_assignments'].items()},
            'actual_S_UU':red['literal_S_UU'],'sum_z_h':red['sum_z_h']}
        assert row['sum_z_h']==0
        out.append(row);write('PROTECTED_RESULTS.json',out)
        print('PASS protected',s['s'],s['full_reflection'],'A',r.A,'raw',raw,'N',len(critical),
            'Rstar',len(row['critical']['R_star_parents']),'internal snapshots',internal_snapshots,flush=True)
        del r,pool,p,f,w,an,b,native,acc,red,a,ff;gc.collect()
    meter.info.update(fresh_complete_sources=len(out));meter.ok=True
