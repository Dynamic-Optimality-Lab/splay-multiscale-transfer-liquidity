from base1 import *
from sources1 import fresh_sources
from physical1 import analyze
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
import gc

def full_original(s):
    import exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core
    for mod in (exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core):mod.ROOT=ROOT
    from independent_Pi3 import check as check_pi
    from independent_cohorts import verify as check_cohorts
    r=base0.old.inherited.Replay(s);p=check_pi(r);c=check_cohorts(r)
    star,_,_=base0.old.inherited.original_residual(r)
    return {'scope':'Original Pi and cohorts independently rechecked; primary original R_star selector inherited unchanged.',
        'original_event_sha256':digest(r.events),'original_R_star':star,'original_U_count':len(r.U),
        'original_R6_count':r.counts['R6'],'independent_Pi':p,'independent_cohorts':c}

if __name__=='__main__':
    meter=Meter('fresh_complete_sources');sources=fresh_sources();write('NEW_SOURCE_CATALOG.json',sources)
    rows=[]
    for i,s in enumerate(sources):
        prefix=prefix_check(s);r,pool=replay(s);forest=scan_forest(r);checked=audit_forest(r,forest)
        for cut in sorted({0,1,len(r.ops)//2,len(r.ops)-1}):assert scan_forest(r,cut)==forest
        phys={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
            'events':r.events,'doubles':[{'parent':p,**d} for p,d in sorted(r.doubles.items())],
            'boundaries':r.boundaries,'state_pool':pool}
        ff={'source':s['name'],'vertices':[{'parent':p,**d} for p,d in sorted(forest.items())],**checked}
        xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
        raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs)) if r.S else 0
        assert raw<=10*r.A,(s['name'],raw,r.A)
        # Exact current zero weights follow from this positive frozen periodic certificate and the unchanged cheap quota.
        weights={'vertices':[{'parent':p,'type':d['type'],'w':0} for p,d in sorted(forest.items())],
            'R_overflow':0,'R_R':0,'R_C':0,'R_P':0,
            'zero_reason':'Original raw periodic source case pays noncheap R_star; cheap D has b<=q<=2a and is all quota-selected.'}
        for label,data in (('PHYS',phys),('FOREST',ff),('WEIGHTS',weights)):write(f'NEW_{label}_{i:02}.json',data)
        result=analyze(s,phys,ff,weights);write(f'NEW_AUDIT_{i:02}.json',result)
        row={'index':i,'source':s['name'],'source_sha256':digest(s),'physical_population':len(s['initial_B']['children']),
            'original_S_size':len(r.S),'original_operations':len(r.ops),'original_primitive_bits':r.T,
            'A':r.A,'Q_B':r.Q,'prefix':prefix,'old_raw_periodic_cost':raw,'actual_R_C':0,
            'scope':'Full physical and forest replay; original Pi unrun unless explicitly provided. Exact current zero follows old periodic certificate.',
            'flux_totals':result['flux_totals'],'C_parent_count':result['C_parent_count'],
            'maximum_C_chain_edges':result['maximum_C_chain_edges'],
            'max_C_fringe_distance':max((z['distance'] for z in result['C_fringe_depths']),default=0),
            'radius2_physical_C_count':result['bounded_fringe_payments'][1]['selected_physical_C_parents'],
            'max_C_ticket_load_per_B_gain':max((z['physical_C_ticket_count'] for z in result['restoration_packets']),default=0)}
        if s['family']=='matched_root_toggle_volume_test':
            assert (r.A,r.Q)==(s['analytic_A'],s['analytic_Q_B'])
            assert result['flux_totals']['A_signed_flux']==s['analytic_A_signed_flux']
            assert result['flux_totals']['B_gain_atoms']==0
            row['analytic_volume_counterexample_verified']=True
        if i in (6,7,14):
            s2={**s,'A':r.A,'Q_B':r.Q}
            pi=full_original(s2);assert pi['original_event_sha256']==digest(r.events)
            write(f'NEW_ORIGINAL_PI_{i:02}.json',pi);row['full_original_Pi_file']=f'NEW_ORIGINAL_PI_{i:02}.json'
        rows.append(row);write('NEW_RESULTS.json',rows)
        print('PASS fresh',i,s['name'],'A',r.A,'C',result['C_parent_count'],'Phi_A',result['flux_totals']['A_signed_flux'],flush=True)
        del r,pool,phys,ff,weights,result,forest;gc.collect()
    meter.info.update(complete_sources=len(rows));meter.ok=True
