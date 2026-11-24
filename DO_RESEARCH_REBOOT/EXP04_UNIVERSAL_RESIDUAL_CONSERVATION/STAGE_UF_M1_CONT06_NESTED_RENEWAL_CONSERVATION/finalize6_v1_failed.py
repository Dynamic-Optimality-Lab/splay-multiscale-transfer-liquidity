from base6 import *
from independent6 import full_physical,local_prices,original_predecessors
from model0 import prefix_check
from gate1 import packets,signature
from rn1_audit5 import audit as canonical_reduction
from residual0 import E_stream

MANIFEST='M1_CONT06_DELIVERY_MANIFEST.json'
RESULT='E — EXACT NESTED-RENEWAL REFUTATION'
REQUIRED=['M1_CONT06_THEOREM_TARGET.md','CANONICAL_RENEWAL_RESIDUAL_PARTITION.md',
 'PROMOTION_FREE_NESTED_GEOMETRY.md','NESTED_FRAME_PRIMITIVE_PROOF.md','NESTED_HYBRID_ELIGIBILITY.md',
 'PROMOTION_FREE_CONSERVATION_PROOF.md','GLOBAL_NESTED_RENEWAL_MULTIPLICITY.md',
 'EPOCHLESS_CYCLIC_PREDECESSOR_PROOF.md','PROMOTION_MEDIATED_BOUNDARY.md','NESTED_RENEWAL_COUNTEREXAMPLES.md',
 'M1_CONT06_INDEPENDENT_VERIFICATION.md','M1_CONT06_GLOBAL_ACCOUNTING.md','M1_CONT06_TO_M2_M3_INTERFACE.md',
 'M1_CONT06_PROOF_LEDGER.md','M1_CONT06_FINAL_REPORT.md','M1_CONT06_REPRODUCTION.md']

def inventory():return {p.relative_to(ROOT).as_posix():hfile(p) for p in ROOT.rglob('*') if p.is_file() and p.name!=MANIFEST}

def audit():
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    for name in REQUIRED:assert (ROOT/name).is_file(),name
    for q in ROOT.glob('*.py'):ast.parse(q.read_text(encoding='utf-8-sig'),filename=q.name)
    ss=load(ROOT/'FRESH_SOURCE_CATALOG.json');assert len(ss)==6
    fresh=[];summ=[];independent=[];principal=None;allrn=[]
    for i,s in enumerate(ss):
        paths={k:ROOT/f'FRESH_{k}_{i:02}.json' for k in ('PHYS','FOREST','WEIGHTS','M1_AUDIT','BIRTH','ORDERED','REDUCTION','RENEWAL','NESTED','RESULT')}
        p,f,w,an,b,acc,red,rn,geo,row=(load(paths[k]) for k in paths)
        n=len(s['initial_B']['children']);assert digest(s)==p['source_sha256']==b['source_sha256']==acc['source_sha256']==row['source_sha256']
        assert prefix_check(s)==row['prefix'];phy=full_physical(s,p)
        assert (phy['A'],phy['Q_B'],phy['primitives'])==(row['A'],row['Q_B'],row['primitives'])
        assert row['A']==an['A']==b['A']==acc['A'] and row['Q_B']==an['Q_B']==b['Q_B']
        assert an['primitive_edges_and_all_complete_boundaries_verified'] and b['original_SET_and_sign_checks']==row['primitives']
        assert f['root_donors_injective'] and f['vertex_count']==row['Q_B']
        assert {tuple(d['parent']) for d in p['doubles']}=={tuple(d['parent']) for d in f['vertices']}=={tuple(d['parent']) for d in w['vertices']}
        assert not w['R_overflow'] and not any(z['w'] for z in w['vertices'])
        r6={digest(e['rho']):e for e in b['original_R6']};star=acc['native_original_R_star'];ids={digest(e['rho']) for e in star}
        assert len(ids)==len(star) and star==row['original_R_star'] and ids<=set(r6)
        used=[]
        for pool in acc['disjoint_original_assignments'].values():
            for e in pool:assert e['original_parent']==r6[digest(e['rho'])]['parent'];used.append(digest(e['rho']))
        assert len(used)==len(set(used))==len(star) and set(used)==ids
        assert {k:len(v) for k,v in acc['disjoint_original_assignments'].items()}==row['assigned_counts']
        assert not acc['exact_D'] and not acc['disjoint_original_assignments']['overflow']
        assert not red['literal_S_UU'] and red['sum_z_h']==0 and row['actual_S_UU']==[]
        assert digest(packets(s,p,b,f,an,acc['exact_D'],star))==digest(red)
        assert {digest(z['rho']) for z in E_stream(p,acc['C_old'])}=={digest(z['rho']) for z in acc['E_old']}
        assert canonical_reduction(s,p,f,b,an,acc)==rn
        original=original_predecessors(p,acc,rn);prices=local_prices(s,p,geo)
        assert len(prices)==len(geo)==rn['canonical_renewals_count']==row['canonical_original_C_old_renewals']
        assert all(z['independently_checked_natural_price_refutation'] for z in prices)
        assert row['raw_periodic_cost']==acc['raw_periodic_certificate']<=10*row['A']
        sig=signature(p,b,f,an)
        for z in geo:
            assert z['promotion_free'] and not z['intervening_B_promotion_ids']
            assert tuple(z['later_parent']) in sig and tuple(z['earlier_parent']) in sig
            assert z['full_F_v']&~z['full_J_u']==0 and z['full_J_u']&~z['full_F_u']==0 and z['full_J_u']!=z['full_F_u']
        # Formula is on adjacent physical body edges; L3's canonical edge skips an F-paid use.
        if s['L']>=5:
            expected=3*s['L']+9+(s['L']+2).bit_length()
            assert len(geo)==2 and all(z['equality_F_v_J_u'] for z in geo)
            for z in prices:assert z['raw']['A']==2 and len(z['raw']['J'])==3*s['L']+7 and z['raw']['D']==expected
        independent.append({'source':s['name'],'physical':phy,'canonical_predecessor':original,'independent_local_prices':prices})
        summary={k:row[k] for k in ('source','index','population','genuine_support','operations','A','Q_B','primitives','raw_periodic_cost','canonical_original_C_old_renewals','natural_local_refutations','assigned_counts')}
        summary.update(actual_S_UU=[],actual_S_PF=[],actual_S_PM=[],natural_intervals=[{'u':z['earlier'],'v':z['later'],'A':z['raw']['A'],'J_size':len(z['raw']['J']),'D_raw_G_H':z['raw']['D'],'threshold':z['threshold_5A']} for z in prices])
        summ.append(summary);allrn.append(rn)
        fresh.append({'source':s,'source_sha256':digest(s),'catalog_index':i,
            'certificates':{k:{'file':q.name,'sha256':hfile(q)} for k,q in paths.items()},
            'native_scope':'Full original U/pairs/R6 independently matched, native R_* and exact frozen assignments; actual S_UU empty by verified periodic case.',
            'novelty_scope':'New replay/records of the inherited padded family; some small physical parameter controls are historical.'})
        if i==1:
            z=geo[0];v=tuple(z['later_parent']);u=tuple(z['earlier_parent']);ds={tuple(d['parent']):d for d in p['doubles']}
            assert (u,v)==((3,6),(5,6)) and z['equality_F_v_J_u']
            assert prices[0]['raw']['D']==27 and prices[0]['threshold_5A']==10
            principal={'principal_result':RESULT,'refuted_law':'Canonical original C_old PF nesting with later deep silent F/E-negative demand forces natural original local min(raw,G,H) price <=5A(I).',
                'scope':'Pre-H local sufficient law; NOT an actual survivor or all-interval exclusion counterexample.',
                'complete_original_source':s,'source_sha256':digest(s),'canonical_edge':z,
                'earlier_original_double':ds[u],'later_original_double':ds[v],
                'earlier_U':b['U'][str(u)],'later_U':b['U'][str(v)],
                'original_pre_A_path':p['boundaries'][v[0]-1]['A_path'],
                'earlier_actual_fringe':[d for d in an['C_fringe_depths'] if tuple(d['vertex'])==u][0],
                'later_actual_fringe':[d for d in an['C_fringe_depths'] if tuple(d['vertex'])==v][0],
                'later_original_R6':[e for e in b['original_R6'] if tuple(e['parent'])==v],
                'later_native_R_star':[e for e in star if tuple(e['original_parent'])==v],
                'independent_price':prices[0],'disjoint_native_assignment':acc['disjoint_original_assignments'],
                'periodic_cost':row['raw_periodic_cost'],'periodic_10A':10*row['A'],'actual_D':[],'actual_S_UU':[],
                'full_certificates':fresh[-1]['certificates']}
        del p,f,w,an,b,acc,red,rn,geo;gc.collect()
        print('PASS final independent full source',i,n,flush=True)
    assert sum(z['canonical_original_C_old_renewals'] for z in summ)==11
    assert principal and len(fresh)==6
    refs=load(C5/'ALL_CONTROL_REFERENCES_FINAL.json');assert len(refs)==104
    inherited=[]
    for i,e in enumerate(refs):
        assert digest(e['source'])==e['source_sha256']
        if e.get('physical'):assert hfile(e['physical'])==e['physical_sha256']
        inherited.append({'source':e['source']['name'],'source_sha256':e['source_sha256'],'origin':e['origin'],
            'complete_source_catalog':str(C5/'ALL_CONTROL_REFERENCES_FINAL.json'),'catalog_index':i,
            'physical':e.get('physical'),'physical_sha256':e.get('physical_sha256'),
            'expansion':e.get('expansion',False),'new_expansion':e.get('new_expansion',False),
            'scope':'Exact C5 sealed original-source/predicate scope inherited; not a new full native rerun.'})
    old=load(C5/'CANONICAL_REDUCTION_INVENTORY.json');assert old['complete_original_accounting_audits']==42
    sh=load(ROOT/'ONE_SIDED_SHADOW_SCOPE.json');assert not sh['fresh_pending'] and sh['intervals']==227 and sh['tested_sources']==30
    results=load(ROOT/'ONE_SIDED_SHADOW_RESULTS.json');assert len(results)==30
    for z in results:
        for e in z.get('tested_stored_PF_intervals',z.get('tested_canonical_original_C_old_intervals',[])):
            assert e['active_side_full_child_pointer_equality'] and e['independent_immutable_shadow_checks']
    write('INDEPENDENT_FRESH_VERIFICATION.json',independent)
    write('EXACT_NESTED_PAYMENT_REFUTATION.json',principal)
    write('RESULTS_SUMMARY.json',summ)
    write('CANONICAL_REDUCTION_INVENTORY.json',{'inherited_catalog':str(C5/'CANONICAL_REDUCTION_INVENTORY.json'),
        'inherited_sha256':hfile(C5/'CANONICAL_REDUCTION_INVENTORY.json'),'inherited_count':42,'fresh_count':6,'combined_count':48,'fresh_records':allrn})
    write('M1_CONT06_SOURCE_WITNESSES.json',{'principal_result':RESULT,'fresh_complete_sources':fresh,'inherited_complete_sources':inherited,
        'inherited_physical_controls':104,'fresh_full_native_replays':6,'combined_complete_source_records':110,
        'original_accounting_audits':48,'fresh_canonical_C_old_PF_edges':11,'historical_stored_shadow_intervals':216,'fresh_shadow_intervals':11,
        'long_native_scope':'No new full long native R_* run; preserve C5 exact expansion, insertion, G/H and original scopes.',
        'finite_coverage_is_universal_proof':False,'positive_actual_S_PF_certified':False})
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    return {'principal_result':RESULT,'full_M1':'OPEN','universal_PF_conservation':'OPEN','universal_K_UU':None,'universal_K_PF':None,
        'approved_completed_transfer_X':None,'new_paid_A_coefficient':0,'preserved_coefficient':'161+48 C_seq+102 C_DF',
        'actual_positive_S_UU_certified':False,'new_actual_S_UU_gaps':0,'fresh_complete_native_replays':6,'fresh_canonical_PF_edges':11,
        'exact_natural_interval_refutations':11,'one_sided_shadow_scope':sh,
        'source_uniform_proved':['Exact literal PF/PM partition','Timestamped nested F/J chains and equality conditions',
            'Monotone one-sided inside hits and full active-child coupling','Initialized monotone-shadow envelope |S_PF|<=3 C_seq M_PF, unpriced',
            'Epochless all-PF cycle and same-ID PF self-loop exclusion'],
        'exact_refutations':['Natural original local interval raw/G/H min price<=5A from eligible nested PF renewal',
            'Every inter-access inclusion F_v subset J_u is strict'],
        'first_missing_implication':'All-source initialized comparison-domain price or affordable covering family forced by actual full hybrid/quota-negative PF signature, with bounded cross-column A reuse. PM unweighted entries also lack A/complete-transfer price.',
        'verification_scope':'Same-agent mathematical component proofs and independent implementations; no external reviewer or formal kernel.',
        'preservation':load(ROOT/'INPUT_MANIFEST.json')}

def verify_only():
    m=load(ROOT/MANIFEST);assert inventory()==m['files'],'Exact delivery inventory mismatch'
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    assert m['principal_result']==RESULT and m['full_M1']=='OPEN'
    print('PASS read-only C6 exact delivery, all historical seals, HEAD/branch/tracked bytes;',len(m['files']),'files; E, M1 and PF conservation OPEN.',flush=True)

def seal():
    assert not (ROOT/MANIFEST).exists(),'Never overwrite a sealed stage.'
    cpu0=time.process_time();wall0=time.perf_counter();ok=False;name='CPU_finalization.json';i=2
    while (ROOT/name).exists():name=f'CPU_finalization_{i}.json';i+=1
    try:z=audit();write('FINAL_VERIFICATION.json',z);ok=True
    finally:write(name,{'completed':ok,'cpu_seconds':time.process_time()-cpu0,'wall_seconds':time.perf_counter()-wall0,'memory':memory(),
        'scope':'Full independent new physical/SET/sign/price/original predecessor/native assignment checks plus transitive preservation; imports excluded.'})
    receipts={q.name:load(q) for q in ROOT.glob('CPU_*.json')};failed=[n for n,z in receipts.items() if not z['completed']]
    assert not failed,failed
    cpu=sum(z['cpu_seconds'] for z in receipts.values());peak=max(z['memory']['peak_working_set_bytes'] for z in receipts.values())
    assert cpu<=1800 and peak<2*1024**3
    write('RESOURCE_RECORD.json',{'allocation':{'measured_script_CPU_seconds':1800,'fresh_complete_source_cap':6,'population_cap':600,
        'operation_cap':40000,'per_process_peak_working_set_aim_bytes':2*1024**3},
        'measured_script_CPU_seconds_total':cpu,'maximum_measured_peak_working_set_bytes':peak,'receipts':receipts,
        'fresh_complete_replays':6,'fresh_native_classifications':6,'max_fresh_population':535,'max_fresh_operations':8791,
        'failed_semantic_runs':[],'failed_survivor_attempts':'All6 targeted complete original sources have positive raw periodic certificates; not post-hybrid survivors.',
        'administrative_lookup_misses':'Read-only guessed directory/filename lookups, corrected after inventory; no data or predicates changed.',
        'unmetered':['Imports before meters','Read-only file/process searches and inspections','Mathematical reasoning and prose/patch construction',
            'One duplicate independent55-key local/predecessor prototype command; no fresh source/classification; successful results rerun under finalization meter; CPU unmeasured',
            'Final resource/manifest serialization and read-only post-seal hashing'],
        'measurement_scope':'Measured script CPU only, not total reasoning CPU or session wall time. One disclosed prototype CPU is outside total.',
        'historical_writes':0,'Git_mutations':0,'subagents':0,'installations':0,'external_reviewers':0})
    write(MANIFEST,{'principal_result':RESULT,'full_M1':'OPEN','universal_PF_conservation':'OPEN',
        'format':'Exact SHA256 relative inventory, excluding only this manifest.','C5_manifest_sha256':hfile(C5/'M1_CONT05_DELIVERY_MANIFEST.json'),'files':inventory()})
    print('PASS sealed',len(inventory()),'files;',round(cpu,3),'measured script CPU seconds; E exact local-payment refutation, M1 OPEN.',flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--verify-only']:verify_only()
    else:assert not sys.argv[1:];seal()
