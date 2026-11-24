"""Seal the reviewed open continuation; --verify-only performs no writes."""
from basec import *
import ast,gc,re

MANIFEST='M1_CONT01_DELIVERY_MANIFEST.json'
REQUIRED=['M1_CONT01_THEOREM_TARGET.md','M1_DEEP_RESIDUAL_GEOMETRY.md','M1_DEEP_CHAIN_LIFECYCLES.md',
    'M1_RESIDUAL_SENSITIVE_INVARIANT.md','M1_GLOBAL_CONSERVATION_PROOF.md','M1_PHYSICAL_TRANSFER_PROOF.md',
    'M1_ADVERSARIAL_COUNTEREXAMPLES.md','M1_DEEP_SOURCE_WITNESSES.json','M1_GLOBAL_ACCOUNTING_AUDIT.md',
    'M1_INDEPENDENT_VERIFICATION.md','M1_UPDATED_TO_M2_M3_INTERFACE.md','M1_CONT01_PROOF_LEDGER.md',
    'M1_CONT01_FINAL_REPORT.md','M1_CONT01_REPRODUCTION.md']

def files():return {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!=MANIFEST}

def git_state():
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert head=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and branch=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    return head,branch

def verify_only():
    m=load(ROOT/MANIFEST);assert files()==set(m['files'])
    for n,h in m['files'].items():assert hfile(ROOT/n)==h,n
    assert all((ROOT/n).is_file() for n in REQUIRED)
    assert git_state()==(m['HEAD'],m['branch'])
    p=preserve();assert p==load(ROOT/'INPUT_MANIFEST.json')
    assert p['M1_manifest_sha256']==m['M1_manifest_sha256']
    print('PASS read-only exact continuation seal:',len(m['files']),'files; historical M1/M0 and all transitive pins unchanged; full M1 OPEN',flush=True)

def build():
    assert not (ROOT/MANIFEST).exists(),'Already sealed; use --verify-only or a new sibling.'
    cpu=time.process_time();wall=time.perf_counter();pins=preserve()
    assert pins==load(ROOT/'INPUT_MANIFEST.json');head,branch=git_state()
    catalog=load(ROOT/'SOURCE_CATALOG.json');historical=controls()
    assert len(catalog)==len(historical)==36
    frontier=load(ROOT/'FRONTIER_RESULTS.json');assert len(frontier)==52
    front={(z['group'],z['index']):z for z in frontier}
    totals=Counter();scopes=Counter();witnesses=[]
    for i,(e,z) in enumerate(zip(historical,catalog)):
        assert e['source']==z['source'] and digest(e['source'])==z['source_sha256']
        for k in ('physical','forest','weights','M1_audit'):assert hfile(e[k])==z['input_sha256'][k]
        b=load(ROOT/f'BIRTH_{i:02}.json');assert b['source_sha256']==z['source_sha256']
        assert b['actual_R_C']==b['actual_R_C_deep']==0
        assert front['historical',i]['source_sha256']==digest(e['source'])
        totals['measured_operations']+=len(e['source']['operations'])
        totals['primitive_SET_sign_checks']+=b['original_SET_and_sign_checks']
        totals['physical_C_vertices']+=b['all_physical_C'];totals['all_original_U']+=len(b['U'])
        totals['original_R6_gaps']+=len(b['original_R6'])
        scopes[b['known_original_R_star_scope']]+=1
        witnesses.append({'group':'historical','index':i,'source':b['source'],'source_sha256':digest(e['source']),
            'source_catalog':'SOURCE_CATALOG.json','source_entry':i,
            'sealed_inputs':{k:{'path':e[k],'sha256':hfile(e[k])} for k in ('physical','forest','weights','M1_audit')},
            'birth_evidence':f'BIRTH_{i:02}.json','birth_sha256':hfile(ROOT/f'BIRTH_{i:02}.json'),
            'original_R_star_scope':b['known_original_R_star_scope'],'actual_R_C_deep':0})
    for group,stem,catname,rowname in (('fresh','NEW','NEW_SOURCE_CATALOG.json','NEW_RESULTS.json'),
                                      ('guarded','GUARDED','GUARDED_SOURCES.json','GUARDED_RESULTS.json')):
        ss=load(ROOT/catname);rows=load(ROOT/rowname);assert len(ss)==len(rows)==(12 if group=='fresh' else 4)
        for i,(s,row) in enumerate(zip(ss,rows)):
            sh=digest(s);declared=row['source_sha256'];assert sh==front[group,i]['source_sha256']
            if group=='guarded':
                provenance=load(ROOT/'SOURCE_HASH_PROVENANCE.json')[i]
                assert provenance['canonical_loaded_JSON_source_sha256']==sh
                assert provenance['recorded_evidence_source_sha256']==declared
                assert provenance['difference_only_numeric_metadata_key_sorting']
            else:assert declared==sh
            b=load(ROOT/f'{stem}_BIRTH_{i:02}.json');assert b['source_sha256']==declared
            assert b['actual_R_C']==b['actual_R_C_deep']==row['actual_R_C_deep']==0
            p=load(ROOT/f'{stem}_PHYS_{i:02}.json')
            assert p['source_sha256']==declared and len(p['events'])==b['original_SET_and_sign_checks']
            assert len(p['boundaries'])==len(s['operations'])
            assert row['prefix']['complete_reached_pair_verified']
            xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(p['original_S'])}
            raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs)) if rank else 0
            recorded=row['old_periodic_raw_cost'] if group=='fresh' else row['old_raw_periodic_cost']
            assert raw==recorded<=10*b['A']
            w=load(ROOT/f'{stem}_WEIGHTS_{i:02}.json');f=load(ROOT/f'{stem}_FOREST_{i:02}.json')
            ids={tuple(v['parent']) for v in p['doubles']}
            assert ids=={tuple(v['parent']) for v in f['vertices']}=={tuple(v['parent']) for v in w['vertices']}
            assert all(v['w']==0 for v in w['vertices']) and w['R_overflow']==0
            if group=='guarded':
                k=s['k'];assert len(p['original_S'])==len(s['initial_B']['children'])==4*k+3
                assert row['critical_U_C_R6_chain_edges']==len(b['original_R6'])==k-1
                assert row['deep_critical_U_C_R6_vertices']==k-2
            totals['measured_operations']+=len(s['operations'])
            totals['primitive_SET_sign_checks']+=len(p['events'])
            totals['physical_C_vertices']+=b['all_physical_C'];totals['all_original_U']+=len(b['U'])
            totals['original_R6_gaps']+=len(b['original_R6'])
            evidence={label:{'file':f'{stem}_{label}_{i:02}.json','sha256':hfile(ROOT/f'{stem}_{label}_{i:02}.json')}
                      for label in ('PHYS','FOREST','WEIGHTS','M1_AUDIT','BIRTH')}
            later='NEW_PRIMARY_'+f'{i:02}.json' if group=='fresh' and i<8 else (
                'NATIVE_SELECTOR_RESULTS.json' if group=='fresh' else 'GUARDED_RESULTS.json')
            scope='Native original R_star executed' if (group=='fresh' or s['k']<=16) else 'Original R_star NOT_CLASSIFIED; native U/R6 agrees'
            witnesses.append({'group':group,'index':i,'source_name':s['name'],'source':s,'source_sha256':sh,
                'catalog':catname,'evidence':evidence,'later_selector_file':later,'later_selector_scope':scope,
                'evidence_recorded_source_sha256':declared,
                'source_hash_provenance_file':'SOURCE_HASH_PROVENANCE.json' if group=='guarded' else None,
                'all_physical_C':b['all_physical_C'],'all_U_C':b['all_U_C'],'original_R6':len(b['original_R6']),
                'actual_R_C_deep':0,'raw_periodic_cost':raw,
                'current_zero_reason':'Original positive periodic certificate pays noncheap gaps; all cheap D parents quota-selected.'})
            del p,b,w,f;gc.collect()
    native=load(ROOT/'NATIVE_SELECTOR_RESULTS.json');assert len(native)==5 and native[0]['sealed_R_star_matches']
    for row in native[1:]:
        b=load(ROOT/f'NEW_BIRTH_{row["index"]:02}.json');valid={digest(z['rho']) for z in b['original_R6']}
        assert all(digest(z['rho']) in valid for z in row['original_R_star'])
    counter=load(ROOT/'CREATOR_CLOSURE_COUNTEREXAMPLE.json')
    assert counter['rho']==[4680,[68,6],[4676,3]] and counter['actual_R_C_deep']==0
    refs=load(ROOT/'EXACT_REFERENCE_PAIR_CHECKS.json');assert len(refs)==8 and all(z['exact_full_fields_match'] for z in refs)
    counts=Counter(z['new_scope'] for r in frontier for z in r['deep_birth_frontier'])
    assert counts=={'B0_nonU_creator':90,'silent_UU':356}
    assert all(z['actual_R_C_deep']==0 for z in frontier)
    write('M1_DEEP_SOURCE_WITNESSES.json',{'date':'2026-11-11','principal_outcome':'F','full_M1':'OPEN',
        'sources':witnesses,'total_complete_sources':52,'historical_complete_sources':36,'fresh_complete_sources':16,
        'physical_states':'Every PHYS state pool is a collision-free full child-pointer tree encoding, not a hash-only substitute.',
        'IDs':{'double':'source-scoped original(h,j)','primitive':'(actor,h,j,bit)',
               'gap':'source-scoped original rho=(consumer h,inner original double,outer original double)'},
        'actual_positive_prescribed_deep_witness':False,
        'native_missingness':'Guarded k64,k256 original R_star is unrun, not empty. Full U/R6 is checked.',
        'counterexample':'CREATOR_CLOSURE_COUNTEREXAMPLE.json'})
    assert all((ROOT/n).is_file() for n in REQUIRED)
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    for p in ROOT.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' not in link:assert (ROOT/link).exists(),(p.name,link)
    write('FINAL_VERIFICATION.json',{'date':'2026-11-11','principal_outcome':'F — OPEN CHECKPOINT','full_M1':'OPEN',
        'Universal_Relaxed_Coarse_Double':'OPEN','Dynamic_Optimality':'OPEN','approved_physical_transfer_X':None,
        'inherited_interface':'Q_B <= (83+48 C_seq+102 C_DF) A + R_C,>2 + R_P',
        'new_scoped_interface':'Q_B <= (161+48 C_seq+102 C_DF) A + |S_UU| + R_P',
        'new_scoped_deep_payment':'B0<=72A, B1<=6A; R_C,>2<=78A+|S_UU|, not complete M1',
        'first_missing_implication':'Globally price original post-hybrid silent U-to-U deep C mass, or prove it necessarily earlier-paid.',
        'gate_status':{'A':'Necessary original exclusions/geometry established; survivor existence or elimination OPEN',
            'B':'Exact arbitrary-depth birth law PROVED; full weighted chain law OPEN',
            'C':'B0/B1 scoped payments PROVED; silent class OPEN',
            'D':'Global B0/B1 composition PROVED; complete residual composition OPEN',
            'E':'Complete c_deep/X quantitative interface OPEN'},
        'supporting_counterexamples':{'creator_U_closure':'Native original R_star 577-key complete source; periodic-paid',
            'bounded_U_R6_chain_height':'Parameterized full-support paired-closed guarded source'},
        'counts':dict(totals),'complete_sources':52,'historical_sources':36,'fresh_sources':16,
        'physical_deep_U_C_frontier_counts':dict(counts),'earlier_exact_full_pair_crosschecks':8,
        'prescribed_positive_R_C_deep_witness':False,'universal_emptiness_inferred':False,
        'all_original_R_star_empty_claimed':False,'all_C_birth_O_impossibility_claimed':False,
        'same_agent_independent_implementations':True,'formal_proof_assistant':False,'external_review':False,
        'preservation':pins,'HEAD':head,'branch':branch,'tracked_files_unchanged':True})
    write('CPU_finalization.json',{'stage':'finalization','completed':True,'cpu_seconds':time.process_time()-cpu,
        'wall_seconds':time.perf_counter()-wall,'memory':base0.old.inherited.memory()})
    receipts=[{'file':p.name,**load(p)} for p in sorted(ROOT.glob('CPU_*.json'))]
    measured=sum(z['cpu_seconds'] for z in receipts);peak=max(z['memory']['peak_working_set_bytes'] for z in receipts)
    assert measured<=1200 and peak<=2*(1<<30)
    write('RESOURCE_RECORD.json',{'timed_stage_receipts':receipts,'measured_stage_CPU_seconds':measured,
        'observed_per_process_peak_working_set_bytes':peak,'CPU_allocation_seconds':1200,
        'observed_per_process_peak_aim_bytes':2*(1<<30),'fresh_source_cap_after_recorded_addendum':16,
        'fresh_complete_sources':16,'fresh_physical_population_cap':1027,'fresh_max_population':1027,
        'unmetered':'Imports before meters; short shell inspections and analysis/prose/file editing; first failed finalization source-hash check (no CPU receipt captured); final manifest hash pass and independent read-only seal check; tool overhead.',
        'failed_adapter_receipt_included':True,'not_a_host_quota_or_theorem_hypothesis':True,
        'resource_limit_is_not_a_mathematical_reason_theorem_is_open':True})
    hashes={n:hfile(ROOT/n) for n in sorted(files())}
    write(MANIFEST,{'date':'2026-11-11','principal_outcome':'F','full_M1':'OPEN','HEAD':head,'branch':branch,
        'M1_manifest_sha256':pins['M1_manifest_sha256'],'M0_manifest_sha256':pins['transitive']['M0_manifest_sha256'],
        'excluded_self':MANIFEST,'files':hashes})
    print('SEALED',len(hashes),'files; F, full M1 OPEN; measured CPU',measured,'peak bytes',peak,flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--verify-only']:verify_only()
    else:
        assert not sys.argv[1:],'Use no arguments or --verify-only.'
        build()
