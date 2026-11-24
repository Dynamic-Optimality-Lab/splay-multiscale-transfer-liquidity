from base7 import *
from rooted7 import rooted_test
from catalog7 import known_inputs,accounting

def fresh_sources():return load(ROOT/'FRESH_SOURCE_CATALOG.json')+load(ROOT/'PROTECTED_SOURCE_CATALOG.json')+load(ROOT/'EPOCHLESS_SOURCE_CATALOG.json')

def root_account(p,acc,edges,paths,A,Q):
    ds={tuple(d['parent']):d for d in p['doubles']};T=len(p['events']);E={tuple(z['original_parent']) for z in acc['E_old']};incoming={tuple(z['v']):z for z in edges};origins=[];loads=Counter();P_origins=[];hits=[]
    for b in paths:
        u=tuple(b['path'][0]);g=b['old_g'];k=sum(bool(z) for z in (b['left_inside_hits'],b['right_inside_hits']));hits+=list(map(tuple,b['unique_original_inside_pivot_bits']))
        if u in E:
            hi=p['boundaries'][u[0]-1]['post_A_time'];aa=[e for e in p['events'] if e['actor']=='A' and e['pivot']==g];assert aa
            donor=min(aa,key=lambda e:(hi-e['time'])%T);loads[tuple(donor['id'])]+=k
            origins.append({'path_start':u,'old_g':g,'kind':'A_epoch_first_C_old','original_donor_bit':donor['id'],'root_atoms':k})
        else:
            edge=incoming[u];assert not edge['PF'] and edge['mediating_promotions'];beta=edge['mediating_promotions'][-1]
            P_origins.append(tuple(beta));origins.append({'path_start':u,'old_g':g,'kind':'last_SS_promotion','original_B_mediator':beta,'root_atoms':k})
    assert len(hits)==len(set(hits))
    byid={tuple(e['id']):e for e in p['events']}
    assert all(byid[e]['actor']=='B' and byid[e]['case']!='ZIG' for e in hits)
    assert len(hits)<=2*Q
    assert max(loads.values(),default=0)<=2
    step_load=Counter()
    for eid,k in loads.items():step_load[eid[1:3]]+=k
    assert max(step_load.values(),default=0)<=4 and sum(loads.values())<=4*A
    assert len(P_origins)==len(set(P_origins))
    return {'root_origins':origins,'A_bit_root_loads':[[list(e),k] for e,k in sorted(loads.items())],
        'maximum_A_bit_load':max(loads.values(),default=0),'maximum_A_StepEv_root_load':max(step_load.values(),default=0),
        'A_funded_root_atoms':sum(loads.values()),'A_root_atom_budget':4*A,
        'B_mediated_root_atoms':sum(z['root_atoms'] for z in origins if z['kind']=='last_SS_promotion'),
        'original_inside_hit_pivot_bits':hits,'M_hit':len(hits),'unpriced_B_bit_budget_2Q':2*Q}

if __name__=='__main__':
    unsealed();m=Meter('global_root_scan_and_fresh_rooted_audit');old=load(ROOT/'INHERITED_PATH_WORKLOADS.json');inputs={e['source']['name']:e for e in known_inputs()};out=[];fresh= fresh_sources();profiles=[]
    for i,s in enumerate(fresh):
        z=load(ROOT/f'FRESH_RESULT_{i:02}.json');old.append({**z,'physical':str(ROOT/f'FRESH_PHYS_{i:02}.json'),'origin':'C7_fresh'})
        inputs[s['name']]={'source':s,'physical':str(ROOT/f'FRESH_PHYS_{i:02}.json'),'accounting_path':str(ROOT/f'FRESH_ORDERED_{i:02}.json')}
    for z in old:
        if not z['maximal_PF_paths'] and not z['source'].startswith('M1C7_'):continue
        e=inputs[z['source']];acc=accounting(e);p=load(e['physical'])
        roots=root_account(p,acc,z['canonical_edges'],z['maximal_PF_paths'],z['A'],z['Q_B'])
        rooted=[]
        if z['source'].startswith('M1C7_'):
            for b in z['maximal_PF_paths']:rooted.append({'path':b['path'],'original_C_old':True,'shadows':rooted_test(p,b)})
            if 'physical_kernel' in z:
                b=z['physical_kernel']['full_physical_PF_path_test'];rooted.append({'path':b['path'],'original_C_old':False,'shadows':rooted_test(p,b)})
        Mhit=sum(b['M_hit'] for b in z['maximal_PF_paths']);assert Mhit==roots['M_hit']
        Mroot=sum(b['component_rooted_workload'] for b in z['maximal_PF_paths']);Minside=sum(b['M_inside'] for b in z['maximal_PF_paths'])
        rootunits=sum(k['root_atoms'] for k in roots['root_origins']);assert Mroot==Minside+rootunits
        out.append({'source':z['source'],'source_sha256':z['source_sha256'],'M_PF':z['M_PF'],'M_component_rooted':Mroot,
            'M_inside':Minside,'M_hit':Mhit,'M_padding':Minside-Mhit,'external_stem_removed':z['M_PF']-Mroot,
            'global_original_root_and_scan_account':roots,'fresh_rooted_tests':rooted,
            'actual_hard_selected_family':[],'actual_hard_selected_workload':0,
            'hard_family_empty_reason':'Verified positive original periodic case plus cheap quota; not inferred from path census.'})
        if z['source'].startswith('M1C7_nested55_periods'):
            T=int(z['source'].split('periods')[-1]);N=871
            normalize=lambda rho: [(rho[0]-1)%N+1,[(rho[1][0]-1)%N+1,rho[1][1]],[(rho[2][0]-1)%N+1,rho[2][1]]]
            base=load(C6/'FRESH_ORDERED_01.json');baseIDs={digest(e['rho']) for e in base['C_old']};normal=Counter(digest(normalize(e['rho'])) for e in acc['C_old'])
            assert set(normal)==baseIDs and set(normal.values())=={T}
            assert z['M_PF']==28*T and z['A']==1082*T and z['Q_B']==274*T
            profiles.append({'source':z['source'],'T':T,'M_PF':z['M_PF'],'A':z['A'],'key_union_size':28,
                'native_original_C_old_copies':dict(normal),'actual_full_pair_equality_boundaries':sum(r['post_A_state']==r['post_B_state'] for r in p['boundaries']),
                'scope':'Exact finite native source; no all-T F/C_old invariance theorem inferred.'})
        gc.collect()
    write('GLOBAL_ROOT_AND_SCAN_AUDIT.json',out);write('REPETITION_PROFILE_AUDIT.json',profiles)
    z=load(ROOT/'FRESH_RESULT_05.json');assert z['KEY_UNION_2_refuted'] and z['M_PF']==112 and len(z['distinct_domain_key_union'])==28
    write('EXACT_GLOBAL_KEY_UNION_REFUTATION.json',{'candidate':'KEY-UNION-2: M_PF <= 2 |union of physical keys in all initialized canonical PF domains|',
        'complete_original_source':fresh[5],'source_sha256':digest(fresh[5]),'M_PF':112,'union_physical_keys':z['distinct_domain_key_union'],'candidate_bound':56,
        'maximal_original_C_old_PF_paths':z['maximal_PF_paths'],'A':z['A'],'Q_B':z['Q_B'],
        'original_accounting_file':'FRESH_ORDERED_05.json','actual_S_PF':[],'actual_S_PM':[],
        'scope':'Refutes this exact label-union overlap rule; does NOT refute M_PF=O(A), every key-only constant, or actual PF conservation.'})
    m.info.update(sources_with_new_root_scan_or_component_checks=len(out),fresh_complete_sources=10);m.ok=True
    print('PASS source-wide actual root/scan incidences and rooted fresh comparisons;',len(out),'sources; exact112>56 key-union counterexample',flush=True)
