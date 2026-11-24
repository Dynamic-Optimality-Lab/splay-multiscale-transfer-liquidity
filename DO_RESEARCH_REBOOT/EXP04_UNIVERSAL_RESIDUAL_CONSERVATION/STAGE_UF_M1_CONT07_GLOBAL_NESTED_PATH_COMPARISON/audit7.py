from base7 import *
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze
from birthc import reconstruct
from native7 import adapter,original_star
from account2 import ordered
from gate1 import packets,signature
from rn1_audit5 import audit as predecessor
from workload7 import canonical_edges,paths_from_edges,path_workload,merged_replay

def audit(s,i):
    pref=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);fc=audit_forest(r,ff)
    p={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
        'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],'boundaries':r.boundaries,'state_pool':pool}
    f={'source':s['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
    xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
    raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs));assert raw<=10*r.A
    w={'vertices':[{'parent':v,'type':d['type'],'w':0} for v,d in sorted(ff.items())],'R_overflow':0,'zero_reason':'Exact positive original raw periodic certificate; cheap quota.'}
    an=analyze(s,p,f,w);b=reconstruct(s,p,f,an,weights=w);native=adapter(s,p,b);star=original_star(native)
    acc=ordered(s,p,b,star);red=packets(s,p,b,f,an,acc['exact_D'],star);rn=predecessor(s,p,f,b,an,acc)
    edges=canonical_edges(s,p,acc);paths=paths_from_edges(edges);details=[path_workload(s,p,path) for path in paths]
    keyunion=sorted({k for z in details for domain in z['full_initial_domains'] for k in domain})
    result={'source':s['name'],'source_sha256':digest(s),'index':i,'population':s['n'],'operations':len(s['operations']),
        'A':r.A,'Q_B':r.Q,'primitives':r.T,'prefix':pref,'raw_periodic_cost':raw,'original_R6':len(b['original_R6']),
        'original_R_star':star,'assigned_counts':{k:len(v) for k,v in acc['disjoint_original_assignments'].items()},
        'C_old_gaps':len(acc['C_old']),'canonical_edges':edges,'maximal_PF_paths':details,'PF_path_count':len(paths),
        'M_PF':sum(z['M_PF'] for z in details),'distinct_domain_key_union':keyunion,'KEY_UNION_2_refuted':sum(z['M_PF'] for z in details)>2*len(keyunion),
        'actual_S_UU':red['literal_S_UU'],'sum_z_h':red['sum_z_h']}
    if s['family']=='outside_attachment_two_side_merge_kernel':
        u=(s['producer_operation'],s['producer_double_index']);v=(s['critical_operation'],s['critical_double_index']);ds={tuple(d['parent']):d for d in p['doubles']}
        physical=path_workload(s,p,[u,v]);sig=signature(p,b,f,an)
        assert ds[u]['g']==ds[v]['g']==s['critical_g']
        lo=p['boundaries'][u[0]-1]['end_time'];hi=p['boundaries'][v[0]-1]['post_A_time'];g=s['critical_g']
        assert not any(e['actor']=='A' and (e['pivot']==g or e['promoted']==g) or e['actor']=='B' and e['promoted']==g for e in p['events'][lo:hi])
        result['physical_kernel']={'u':u,'v':v,'full_physical_PF_path_test':physical,
            'u_U':str(u) in b['U'],'v_U':str(v) in b['U'],'v_sigma':v in sig,
            'u_C_old':any(tuple(e['original_parent'])==u for e in acc['C_old']),
            'v_C_old':any(tuple(e['original_parent'])==v for e in acc['C_old']),
            'v_original_R6':[e for e in b['original_R6'] if tuple(e['parent'])==v],
            'v_R_star':[e for e in star if tuple(e['original_parent'])==v],
            'u_double':ds[u],'v_double':ds[v],'u_forest_type':ff[u]['type'],'v_forest_type':ff[v]['type']}
    if s['family']=='explicit_epochless_old_g_column':
        g=s['critical_g'];uses=[(v,d) for v,d in r.doubles.items() if d['g']==g]
        resets=[e['id'] for e in r.events if e['actor']=='A' and (e['pivot']==g or e['promoted']==g)]
        assert len(uses)==1 and not resets and ff[uses[0][0]]['type']=='P'
        result['epochless']={'old_g':g,'all_double_column':[list(v) for v,d in uses],
            'A_reset_or_promotion_ids':resets,'forest_entries':[ff[v] for v,d in uses],
            'original_B_non_target_promotions':[e['id'] for e in r.events if e['actor']=='B' and e['promoted']==g],
            'canonical_C_old_uses':[e for e in acc['C_old'] if r.doubles[tuple(e['original_parent'])]['g']==g],
            'scope':'Nonempty physical epochless singleton old-g column; C_old/actual residual not inferred.'}
    for lab,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',b),('ORDERED',acc),('REDUCTION',red),('RENEWAL',rn),('RESULT',result)):
        write(f'FRESH_{lab}_{i:02}.json',z)
    return result

if __name__=='__main__':
    unsealed();i=int(sys.argv[1]);m=Meter(f'fresh_{i:02}')
    ss=load(ROOT/'FRESH_SOURCE_CATALOG.json')+(load(ROOT/'PROTECTED_SOURCE_CATALOG.json') if (ROOT/'PROTECTED_SOURCE_CATALOG.json').exists() else [])+(load(ROOT/'EPOCHLESS_SOURCE_CATALOG.json') if (ROOT/'EPOCHLESS_SOURCE_CATALOG.json').exists() else [])
    s=ss[i];z=audit(s,i)
    m.info['fresh_complete_sources']=1;m.ok=True
    print('PASS',i,s['name'],'A',z['A'],'C_old',z['C_old_gaps'],'paths',z['PF_path_count'],'M',z['M_PF'],'KEY_UNION_2',z['KEY_UNION_2_refuted'],
        'physical merge failed',bool(z.get('physical_kernel',{}).get('full_physical_PF_path_test',{}).get('merged_inside_shadow',{}).get('full_g_component_failure')),flush=True)
