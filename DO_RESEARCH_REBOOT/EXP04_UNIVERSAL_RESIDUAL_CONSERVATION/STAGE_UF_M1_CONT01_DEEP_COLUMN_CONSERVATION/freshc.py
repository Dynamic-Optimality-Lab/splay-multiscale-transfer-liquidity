from basec import *
from sourcesc import fresh_sources
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze
from birthc import reconstruct
import gc

def primary(s,phys,our):
    import exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core
    for mod in (exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core):mod.ROOT=ROOT
    r=base0.old.inherited.Replay(s)
    assert digest(r.events)==digest(phys['events'])
    assert set(map(str,r.U))==set(our['U'])
    aa={digest(p['rho']):p for p in r.pairs};bb={digest(p['rho']):p for p in our['original_pairs']}
    assert set(aa)==set(bb)
    for key,z in aa.items():assert digest(z)==digest(bb[key])
    star,_,_=base0.old.inherited.original_residual(r)
    return {'scope':'Independent edge/SET/Pi/cohort reconstruction agrees with unchanged primary original oracle; native original R_star selector executed.',
        'original_R6':r.counts['R6'],'original_R_star':star,'U_ids':[list(k) for k in sorted(r.U)],
        'original_event_sha256':digest(r.events)}

if __name__=='__main__':
    meter=Meter('new_adversarial_sources');ss=fresh_sources();write('NEW_SOURCE_CATALOG.json',ss);rows=[]
    for i,s in enumerate(ss):
        prefix=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);checked=audit_forest(r,ff)
        phys={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
            'events':r.events,'doubles':[{'parent':p,**d} for p,d in sorted(r.doubles.items())],
            'boundaries':r.boundaries,'state_pool':pool}
        forest={'source':s['name'],'vertices':[{'parent':p,**z} for p,z in sorted(ff.items())],**checked}
        xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
        raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs)) if r.S else 0
        assert raw<=10*r.A
        w={'vertices':[{'parent':p,'type':z['type'],'w':0} for p,z in sorted(ff.items())],
            'R_overflow':0,'zero_reason':'Positive original raw periodic certificate; noncheap R_star paid and all cheap D quota-selected.'}
        m1=analyze(s,phys,forest,w)
        birth=reconstruct(s,phys,forest,m1,weights=w)
        pi=None
        if len(s['initial_B']['children'])<100:
            pi=primary(s,phys,birth);write(f'NEW_PRIMARY_{i:02}.json',pi)
            starby=defaultdict(list)
            for e in pi['original_R_star']:starby[tuple(e['original_parent'])].append(e)
            for z in birth['C_U_births']:z['known_original_R_star_gaps']=starby[tuple(z['consumer'])]
            birth['known_original_R_star_C_gaps']=sum(len(z['known_original_R_star_gaps']) for z in birth['C_U_births'])
            birth['known_original_R_star_scope']='New unchanged native selector; independent original SET/Pi/cohorts agree.'
        for label,data in (('PHYS',phys),('FOREST',forest),('WEIGHTS',w),('M1_AUDIT',m1),('BIRTH',birth)):
            write(f'NEW_{label}_{i:02}.json',data)
        row={'index':i,'source':s['name'],'source_sha256':digest(s),'population':len(s['initial_B']['children']),
            'operations':len(s['operations']),'primitives':len(r.events),'A':r.A,'Q_B':r.Q,'prefix':prefix,
            'old_periodic_raw_cost':raw,'original_U':len(birth['U']),'original_R6':len(birth['original_R6']),
            'original_R_star':pi['original_R_star'] if pi else None,'actual_R_C_deep':0,
            'all_deep_U_C':birth['all_deep_U_C'],'nonU_deep_U_C':birth['nonU_deep_U_C'],
            'C_birth_kinds':dict(Counter(z['output_kind'] for z in birth['C_U_births'])),
            'critical_deep_births':[z for z in birth['C_U_births'] if z['distance']>2]}
        rows.append(row);write('NEW_RESULTS.json',rows)
        print('PASS fresh',i,s['name'],'U',len(birth['U']),'R6',len(birth['original_R6']),'births',row['C_birth_kinds'],flush=True)
        del r,pool,phys,forest,w,m1,birth,pi,ff;gc.collect()
    meter.info.update(fresh_sources=len(rows));meter.ok=True
