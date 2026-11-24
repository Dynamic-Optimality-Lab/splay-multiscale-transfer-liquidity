"""Seal scoped compensation without declaring full M1 closed."""
from base4 import *
from finalize3 import verify_physical
from model0 import prefix_check
from gate1 import signature,packets

MANIFEST='M1_CONT04_DELIVERY_MANIFEST.json'
REQUIRED=[
 'M1_CONT04_THEOREM_TARGET.md','PAID_WIDE_PACKET_STRUCTURE.md','SKIPPED_RANK_COMPENSATION_PROOF.md',
 'PAID_TO_UNPAID_DEFORMATION.md','CERTIFICATE_DISRUPTION_GEOMETRY.md','DISRUPTION_CONSERVATION_PROOF.md',
 'GLOBAL_MULTIPLICITY_AUDIT.md','HYBRID_COMPENSATION_THEOREM.md','RANK_LAMBDA_COUPLING.md',
 'POSTHYBRID_SURVIVOR_SEARCH.md','M1_CONT04_INDEPENDENT_VERIFICATION.md','M1_CONT04_GLOBAL_ACCOUNTING.md',
 'M1_CONT04_TO_M2_M3_INTERFACE.md','M1_CONT04_PROOF_LEDGER.md','M1_CONT04_FINAL_REPORT.md','M1_CONT04_REPRODUCTION.md']

def inventory():return {p.relative_to(ROOT).as_posix():hfile(p) for p in ROOT.rglob('*') if p.is_file() and p.name!=MANIFEST}

def check_assignments(s,p,b,f,an,acc,red):
    star=acc['native_original_R_star'];keys={digest(z['rho']) for z in star};assert len(keys)==len(star)
    r6={digest(z['rho']):z for z in b['original_R6']}
    assert keys<=set(r6)
    assigned=[]
    for kind,es in acc['disjoint_original_assignments'].items():
        for z in es:
            assert z['original_parent']==r6[digest(z['rho'])]['parent'];assigned.append(digest(z['rho']))
    assert len(assigned)==len(set(assigned))==len(star) and set(assigned)==keys
    assert not acc['disjoint_original_assignments']['overflow'] and acc['actual_S_UU']==0
    rebuilt=packets(s,p,b,f,an,acc['exact_D'],star);assert digest(rebuilt)==digest(red)
    assert red['sum_z_h']==0 and red['literal_S_UU']==[]
    refs={z['h']:z for z in acc['quota_rows']}
    assert set(refs)=={z['h'] for z in red['packets']}
    for z in red['packets']:
        ref=refs[z['h']]
        assert ref['distinct_original_parents']==z['ordered_distinct_D_parents']
        assert ref['selected']==z['selected_by_original_quota']
    assert acc['raw_periodic_certificate']<=10*acc['A']
    return len(star),len(acc['exact_D'])

def check_short(s,stem,row,critical_h):
    files={k:ROOT/f'{stem}_{k}.json' for k in ('PHYS','FOREST','WEIGHTS','M1_AUDIT','BIRTH','ORDERED','REDUCTION')}
    p,f,w,an,b,acc,red=(load(files[k]) for k in files)
    assert digest(s)==p['source_sha256']==b['source_sha256']==acc['source_sha256']==row['source_sha256']
    assert prefix_check(s)==row['prefix']
    physical=verify_physical(s,p)
    assert physical['A']==row['A']==b['A']==an['A']==acc['A']
    assert physical['Q_B']==row['Q_B']==b['Q_B']==an['Q_B']==f['vertex_count']
    assert physical['primitives']==row['primitives']==b['original_SET_and_sign_checks']
    assert p['original_S']==p['original_genuine_M']==list(range(1,s['n']+1))
    assert an['primitive_edges_and_all_complete_boundaries_verified'] and f['root_donors_injective']
    assert w['R_overflow']==0 and all(z['w']==0 for z in w['vertices'])
    sc,dc=check_assignments(s,p,b,f,an,acc,red)
    sig=signature(p,b,f,an);critical=[v for v in sig if v[0]==critical_h]
    if 'N_h' in row['critical']:assert len(critical)==row['critical']['N_h']
    else:assert len(critical)==row['critical']['physical_N_h']
    ref={'source':s['name'],'source_sha256':digest(s),'population':s['n'],'operations':len(s['operations']),
        'A':row['A'],'Q_B':row['Q_B'],'original_R_star_gaps':sc,'actual_D_gaps':dc,'literal_S_UU':[],
        'critical_h':critical_h,'critical_physical_sigma_count':len(critical),
        'certificates':{k:{'file':q.name,'sha256':hfile(q)} for k,q in files.items()},
        'native_scope':'Full original mutable/immutable and independent edge/SET/Pi/U/cohort/R6; native original R_* and literal frozen accounting.'}
    del p,f,w,an,b,acc,red;gc.collect();return ref

def audit():
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    for name in REQUIRED:assert (ROOT/name).is_file(),name
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=p.name)
    fresh=[]
    for stem in ('DEFORM','SHARED'):
        sources=load(ROOT/f'{stem}_SOURCE_CATALOG.json');rows=load(ROOT/f'{stem}_RESULTS.json')
        assert len(sources)==len(rows)==(10 if stem=='DEFORM' else 4)
        for i,(s,row) in enumerate(zip(sources,rows)):
            # Files use KIND_INDEX in ordinary catalogs; check_short accepts a
            # stable alias-independent mapping through a local explicit load.
            paths={k:ROOT/f'{stem}_{k}_{i:02}.json' for k in ('PHYS','FOREST','WEIGHTS','M1_AUDIT','BIRTH','ORDERED','REDUCTION')}
            p,f,w,an,b,acc,red=(load(paths[k]) for k in paths)
            assert row['source_sha256']==digest(s)==p['source_sha256']==b['source_sha256']==acc['source_sha256']
            assert prefix_check(s)==row['prefix']
            phy=verify_physical(s,p)
            assert (phy['A'],phy['Q_B'],phy['primitives'])==(row['A'],row['Q_B'],row['primitives'])
            assert p['original_S']==p['original_genuine_M']==list(range(1,s['n']+1))
            assert b['original_SET_and_sign_checks']==row['primitives']
            assert an['primitive_edges_and_all_complete_boundaries_verified']
            assert f['root_donors_injective'] and f['vertex_count']==row['Q_B']
            assert w['R_overflow']==0 and all(z['w']==0 for z in w['vertices'])
            sc,dc=check_assignments(s,p,b,f,an,acc,red)
            assert sc==len(row['original_R_star']) and acc['native_original_R_star']==row['original_R_star']
            sig=signature(p,b,f,an);h=s['critical_operation'];critical=[v for v in sig if v[0]==h]
            assert len(critical)==row['critical']['physical_N_h']
            assert [list(v) for v in sorted(critical)]==row['critical']['sigma_parents']
            assert row['sum_z_h']==0 and not row['actual_S_UU']
            assert {k:len(v) for k,v in acc['disjoint_original_assignments'].items()}==row['assigned_counts']
            fresh.append({'source':s['name'],'source_sha256':digest(s),'catalog':f'{stem}_SOURCE_CATALOG.json','catalog_index':i,
                'population':s['n'],'operations':len(s['operations']),'A':row['A'],'Q_B':row['Q_B'],
                'critical':row['critical'],'original_R_star_gaps':sc,'actual_D_gaps':dc,'literal_S_UU':[],
                'certificates':{k:{'file':q.name,'sha256':hfile(q)} for k,q in paths.items()},
                'native_scope':'Full original native R_* and exact original accounting; independent U/R6/Pi and full states.'})
            del p,f,w,an,b,acc,red;gc.collect()
    short=load(ROOT/'PROBE_SHORT_SOURCE.json');sr=load(ROOT/'PROBE_SHORT_RESULTS.json')
    fresh.append({**check_short(short,'PROBE_SHORT',sr,short['critical_operation']),'source_file':'PROBE_SHORT_SOURCE.json'})
    assert sr['A']==9966 and sr['critical']['N_h']==128 and len(sr['critical']['R_star_parents'])==97
    acc=load(ROOT/'PROBE_SHORT_ORDERED.json');h=short['critical_operation']
    counts={k:sum(e['consumer']==h for e in es) for k,es in acc['disjoint_original_assignments'].items()}
    assert counts=={'carrier':0,'skipped_rank':0,'E_old':192,'H_all':1,'Q_D':0,'overflow':0}
    long=load(ROOT/'PROBE_LONG_SOURCE.json');lr=load(ROOT/'PROBE_LONG_RESULTS.json');rule=load(ROOT/'PROBE_EVENT_EXPANSION.json')
    assert rule['short_source_sha256']==digest(short) and rule['long_source_sha256']==digest(long)==lr['source_sha256']
    assert long['replication']==rule['copies_in_long']==39954
    assert long['operations']==[['K',x] for _ in range(long['replication']) for x in (long['n'],1)]+short['operations'][2:]
    assert (lr['A'],lr['Q_B'],lr['operations'],lr['original_primitives'],lr['raw_periodic_cost'],lr['Lambda_A'])==(89872,3234,87518,185361,898722,811954)
    assert lr['raw_periodic_cost']>10*lr['A'] and lr['Lambda_A']>6*lr['A']
    assert lr['actual_S_UU']==0 and lr['original_R_star'] is None and not lr['full_long_native_Pi_R_star_rerun']
    for a,b in zip(sr['G_H_periodic_certificates'],lr['G_H_periodic_certificates']):
        assert a['variant']==b['variant'] and a['B_cyclic']==b['B_cyclic']==12991
        assert b['eligible_periodic'] and not any(h<=2*long['replication'] for h in b['retained_original_operations'])
        assert [h+2*(long['replication']-1) for h in a['retained_original_operations']]==b['retained_original_operations']
    fs=load(ROOT/'PROBE_LONG_FULL_STATES.json')
    assert len(fs['rows'])==len(long['operations']) and fs['all_expanded_A_B_boundaries_equal_short_state_pool'] and fs['full_long_word_incremental_replay']
    fresh.append({'source':long['name'],'source_sha256':digest(long),'source_file':'PROBE_LONG_SOURCE.json','population':long['n'],
        'operations':len(long['operations']),'A':lr['A'],'Q_B':lr['Q_B'],'critical':lr['critical'],
        'original_R_star':None,'actual_D_enumerated':False,'actual_S_UU':0,
        'certificates':{n:{'file':n,'sha256':hfile(ROOT/n)} for n in (
            'PROBE_EVENT_EXPANSION.json','PROBE_SHORT_PHYS.json','PROBE_LONG_FULL_STATES.json','PROBE_LONG_RANK.json','PROBE_LONG_CORRIDOR.json','PROBE_LONG_RESULTS.json')},
        'native_scope':'Full independent/native short original U/R6/R_*; long exact original internal Pi/U/R6 insertion law and two complete physical replay scopes. No full long native R_* rerun.',
        'exact_zero_reason':'Positive original G/H periodic certificates plus cheap original quota.'})
    assert len(fresh)==16 and len({z['source_sha256'] for z in fresh})==16
    assert max(z['population'] for z in fresh)==518 and max(z['operations'] for z in fresh)==87518
    corridors=load(ROOT/'PHYSICAL_CORRIDOR_RESULTS.json')+[load(ROOT/'PROBE_LONG_CORRIDOR.json')]
    replication=load(ROOT/'GUARDFREE_REPLICATION_RESULTS.json');assert len(corridors)==len(replication)==96
    assert len({z['source_sha256'] for z in corridors})==96
    for z in corridors:
        assert z['E_phys_count']==len(z['E_phys'])<=z['real_A_bits']<=2*z['A']
        assert z['physical_gap_bound']<=z['global_budget']==6*z['A']
        assert z['maximum_parent_load_per_actual_A_StepEv']<=2
        assert len({tuple(q['actual_A_donor']) for q in z['E_phys']})==len(z['E_phys'])
    assert {z['source_sha256'] for z in replication}=={z['source_sha256'] for z in corridors}
    transitions=load(ROOT/'EXACT_PAID_TO_ALTERNATIVE_TRANSITIONS.json')
    assert [len(z['same_original_R_star_gaps_switching_F_to_alternative']) for z in transitions]==[9,21,45]
    assert [z['identical_full_original_events_through_Ky'] for z in transitions]==[65,121,233]
    coupling=load(ROOT/'INTACT_COMPONENT_COUPLING_EXAMPLE.json')
    assert coupling['global_states_differ'] and coupling['same_old_g_double_despite_omitted_outside_access']
    paid=load(ROOT/'PC1_PAID_WINDOW_CERTIFICATES.json');assert len(paid)==12
    for z in paid:
        assert z['all_R_star_paid']
        for w in z['supporting_windows'].values():assert w['domain_size']<=2*(w['ell']-1) and w['retained'][:2]==[1,2]
    old=load(C3/'CONTROL_REFERENCE_CATALOG.json');assert len(old)==80
    inherited=[]
    for i,e in enumerate(old):
        if e['physical']:assert hfile(e['physical'])==e['physical_sha256']
        for k,sha in e.get('sealed_input_hashes',{}).items():assert hfile(e[k])==sha
        inherited.append({'source':e['source']['name'],'source_sha256':e['source_sha256'],
            'full_original_source_reference':{'catalog':str(C3/'CONTROL_REFERENCE_CATALOG.json'),'index':i},
            'physical':e['physical'],'physical_sha256':e['physical_sha256'],'origin':e['origin'],
            'scope':'Inherited exact complete source/physical/predicate scopes preserved. Current corridor/replication audits do not invent unknown native R_* or D sets.'})
    write('M1_CONT04_SOURCE_WITNESSES.json',{'fresh_complete_sources':fresh,'inherited_complete_controls':inherited,
        'fresh_full_native_sources':15,'fresh_exact_long_expansion_sources':1,'all_source_words_complete':True,
        'event_materialization':'decode_probe4.py exports every literal long original event/boundary from the exact template.',
        'finite_population_or_coverage_is_universal_proof':False})
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    return {'principal_result':'E — NEW SOURCE-UNIFORM RESTRICTED THEOREM','full_M1':'OPEN',
        'universal_K_UU':None,'approved_transfer_X':None,'original_114_161_interface_changed':False,
        'fresh_complete_sources':16,'fresh_full_native_original_R_star':15,'long_native_R_star_rerun':False,
        'new_original_source_max_population':518,'new_original_source_max_operations':87518,
        'physical_corridor_and_replication_audits':96,'PC1_inherited_paid_sources':12,
        'genuine_positive_posthybrid_survivor_certified':False,'actual_fresh_S_UU':0,
        'source_uniform_new_scoped_theorems':['Extremal-separator accepted window','Intact complete first-hit component shadow coupling',
            'First-index-noncheap epoch compensation within existing6A','Paired two-zig replication preserves existing G/H payment at block cut'],
        'not_established':['All-source priced disruption coverage','A budget for repeated noncheap F-negative demand','All-source elimination or conservation','M2 R_P'],
        'first_missing_implication':'A repeated noncheap F-negative D-tail sigma demand surviving E_old and every applicable G/H/local/quota exclusion forces a physical obligation with absolute global A load.',
        'verification_scope':'Same agent, separate original engines/edge/stack implementations; no external reviewer or formal kernel.',
        'preservation':load(ROOT/'INPUT_MANIFEST.json')}

def verify_only():
    m=load(ROOT/MANIFEST);assert inventory()==m['files'],'Exact inventory/hash mismatch'
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    assert m['full_M1']=='OPEN' and m['principal_result']=='E — NEW SOURCE-UNIFORM RESTRICTED THEOREM'
    print('PASS read-only exact C4 delivery and all inherited seals/HEAD/tracked bytes;',len(m['files']),'files; scoped E, full M1 OPEN.',flush=True)

def seal():
    assert not (ROOT/MANIFEST).exists(),'Never overwrite a sealed checkpoint.'
    t0=time.process_time();w0=time.perf_counter();ok=False;name='CPU_finalization.json';i=2
    while (ROOT/name).exists():name=f'CPU_finalization_{i}.json';i+=1
    try:
        result=audit();write('FINAL_VERIFICATION.json',result);ok=True
    finally:write(name,{'completed':ok,'cpu_seconds':time.process_time()-t0,'wall_seconds':time.perf_counter()-w0,'memory':memory(),
        'scope':'Final certificate consistency, fresh independent full edge/SET/boundary replay and transitive preservation; imports excluded.'})
    receipts={p.name:load(p) for p in ROOT.glob('CPU_*.json')};assert all(z['completed'] for z in receipts.values())
    cpu=sum(z['cpu_seconds'] for z in receipts.values());peak=max(z['memory']['peak_working_set_bytes'] for z in receipts.values())
    assert cpu<=1800 and peak<2*1024**3
    write('RESOURCE_RECORD.json',{'allocation':{'measured_script_CPU_seconds':1800,'fresh_complete_source_cap':16,
        'initial_population_cap':259,'extended_population_cap':1027,'initial_operation_cap':40000,'extended_long_operation_cap':200000,
        'extension_reason':'Proved original raw-certificate support barrier requires at least513 marked keys for raw failure; LARGE_SUPPORT_BEFORE.md records extension before construction.',
        'per_process_peak_working_set_aim_bytes':2*1024**3},
        'measured_script_CPU_seconds_total':cpu,'maximum_measured_process_peak_working_set_bytes':peak,'receipts':receipts,
        'fresh_complete_sources':16,'fresh_full_native_sources':15,'fresh_lossless_long_source':1,
        'max_fresh_population':518,'max_fresh_operations':87518,
        'failed_semantic_runs':0,'failed_survivor_deformations':'All16 remain paid; individual rank disruptions, signature loss and alternative payment are explicitly recorded, not treated as theorem successes.',
        'unmetered':['Module imports before meters','Read-only inspections and searches (including corrected filename/glob lookups)',
            'Mathematical reasoning, prose and patch authoring','Final JSON/manifest serialization and read-only post-seal verification'],
        'helper_templates':'Transient coercion/planning building blocks are computation, not additional classified experimental sources.',
        'resource_numbers_are':'Measured script scope, not total reasoning CPU or full session wall time.',
        'external_reviewers':0,'agents':0,'installations':0,'Git_mutations':0,'historical_writes':0})
    write(MANIFEST,{'principal_result':'E — NEW SOURCE-UNIFORM RESTRICTED THEOREM','full_M1':'OPEN',
        'format':'Exact relative SHA256 inventory, excludes only this manifest.',
        'C3_manifest_sha256':hfile(C3/'M1_CONT03_DELIVERY_MANIFEST.json'),'files':inventory()})
    print('PASS sealed',len(inventory()),'files;',round(cpu,3),'measured script CPU seconds; restricted E, full M1 OPEN.',flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--verify-only']:verify_only()
    else:
        assert not sys.argv[1:];seal()
