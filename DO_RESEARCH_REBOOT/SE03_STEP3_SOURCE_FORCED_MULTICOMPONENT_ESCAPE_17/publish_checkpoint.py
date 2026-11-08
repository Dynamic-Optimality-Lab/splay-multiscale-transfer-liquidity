"""Resource/provenance/content publication, NOT independent certification."""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
C15=B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
e=read(B/'entry.json');total=e['prior_uniform_CPU'];groups=e['inherited_group_CPU'].copy();runs=[];calls=0
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'))
    charge=r['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge;calls+=r['source_engine_calls']
    runs.append({'phase':r['phase'],'group':r['group'],'status':r['status'],
        'child_CPU':r['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],
        'charge':charge,'source_engine_calls':r['source_engine_calls'],
        'new_finite_source_histories':r['new_finite_tests'],'old_semantic_rows_replayed':r['old_semantic_rows_replayed'],
        'peak_working_set_bytes':r['peak_working_set_bytes_observed']})
assert total<7195 and groups['symbolic']<120 and groups['independent']==299.125
assert calls==0 and all(r['group']=='symbolic' for r in runs)
required=['SOURCE_SPEC.md','DEPENDENCY_GRAPH.md','U16_RECONSTRUCTION.md','ZERO_HOLE_CLASSIFICATION.md',
    'TWO_COMPONENT_OBSTRUCTION.md','SATURATED_COMPONENT_NORMAL_FORM.md','LONG_ZERO_CHAIN_ANALYSIS.md',
    'MULTICOMPONENT_EXPANSION.md','NONLOCAL_AUGMENTATION_ASSEMBLY.md','GLOBAL_NONOVERLAP.md',
    'FROZEN_OWNER_PRESERVATION.md','SIGNED_SOURCE_ACCOUNTING.md','ABSOLUTE_PERIOD_VALIDITY.md',
    'UNIFORM_R_SOURCE_LIFTING.md','GATE_U_DISCHARGE.md','UNIFORM_TRANSFER_VERDICT.md','CASE_LEDGER.md',
    'ADVERSARIAL_AUDIT.md','INDEPENDENT_AUDIT_STATUS.md','FINAL_VERDICT.md','CHECKPOINT.md',
    'PREPARATION_TAIL_THEOREM.md','CORE_ORIGIN_BARRIER.md','EDGE_CREATOR_THEOREM.md','PERIOD_PROVENANCE_CORRECTION.md']
for name in required:assert (B/name).is_file() and (B/name).stat().st_size
for p in B.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=p.name)
assert not (B/'FULL_PROOF.md').exists() and not (B/'SOURCE_FORCED_ESCAPE.md').exists()
assert not (B/'independent_audit.json').exists() and not (C15/'partial_seal.json').exists()
out('resources_checkpoint.json',{'status':'U17_UNRESOLVED_CAPS_PRESERVED_NEW_DERIVATIONS_AUDIT_PENDING',
    'prior_cumulative_CPU':e['prior_uniform_CPU'],'campaign_CPU':total-e['prior_uniform_CPU'],
    'cumulative_CPU':total,'remaining_CPU':7200-total,'reserve':5,
    'cumulative_group_CPU':groups,'group_caps':e['group_caps'],
    'group_remaining':{g:e['group_caps'][g]-groups[g] for g in groups},
    'independent_remaining_below_unchanged_controller_reserve':True,'new_independent_runs':0,
    'C15_final_integrity_suffix':'PENDING_NOT_COMPLETED_BY_METADATA','C16_and_C17_required_audit':'PENDING',
    'campaign_source_engine_calls':calls,'inherited_C15_plus_C16_source_engine_calls':5912,
    'C15_plus_C16_plus_C17_source_engine_calls':5912+calls,
    'older_query_ledgers':'preserved in pinned predecessor receipts; no original counter reset',
    'query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'max_observed_memory_this_campaign':max(r['peak_working_set_bytes'] for r in runs),
    'wall_cap_hours':12,'Bank25':25,'general_Bank25_realization':'OPEN_NOT_PROMOTED',
    'no_cap_reset':True,'all_proof_construction_controller_runs_charged':True,'runs':runs,
    'metadata_CPU_convention':'inherited entry/publication exclusion only; no source or independent check reclassified',
    'publication_metadata_CPU_excluded':time.process_time()})
out('research_status_ledger.json',{'principal_outcome':'UNRESOLVED','U17_ESCAPE':'OPEN','Gate_U17':'U-OPEN',
    'inherited_Gate_U14':'SEALED_U-B_SUFFICIENT_IMPLICATION_UNCHANGED','CD6_I6':'SEALED_UNCHANGED',
    'Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
    'new_result_state':'PROVED-DERIVATION / AUDIT-PENDING',
    'new_mathematical_results':[
        {'claim':'Q1 macro tail after first A event gives2(H-1) distinct physical comparison-protected units','scope':'actual maximal closed source, no old-owner freedom assumption'},
        {'claim':'explicit preparation source covers all holes of two inherited families','scope':'all r/repetitions/private gaps/reflection at exact family scope; static counting/block interface'},
        {'claim':'two actual event35,2 bits repair known paired components','scope':'actual r7 erased13 source, both bits unused by f6/a, exact interval1..64'},
        {'claim':'fixed-comparison component cut equalities','scope':'not a source-complete saturated cut'},
        {'claim':'core agreement forces H>=Q; first divergent macroH>=2 and tail>=H-1','scope':'actual synchronization hypothesis; no universal repeated-component budget'},
        {'claim':'in-period edge-lifetime creators inject anonymous-parent H1 frontiers into actual bits, max2 per event','scope':'RAW candidates only; comparison collision/effective owner escape OPEN'}],
    'producer_preparation_allocations':15,'reused_source_histories':8,'reused_actual_owner_variants':7,
    'edge_lineage_old_history_profiles':8,'new_source_histories':0,'new_source_engine_calls':0,
    'period_correction':{'source':'C15 owner_image_source_audit report erased13','u':0,'L':1,
        'actual_interval':[1,64],'other_six_erasures_u':1,'frozen_files_changed':False},
    'principal_refuted':False,'universal_source_complete_exchange_relation':'OPEN',
    'universal_joint_escape_supply':'OPEN','marked_parent_and_higherH_classes':'OPEN',
    'comparison_creator_collision_repayment':'OPEN','Gate_U_source_license_and_general_working':'OPEN',
    'next_bounded_candidate':'RR7-CREATOR-PROTECTION with original source license, or exact source refutation of that candidate',
    'manifest_is_proof_seal':False})
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
assert git('rev-parse','HEAD')==e['head'] and git('branch','--show-current')==e['branch']
assert not git('status','--porcelain','--untracked-files=no')
out('publication_provenance.json',{'branch':e['branch'],'HEAD':e['head'],'tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'writes':'only SE03_STEP3_SOURCE_FORCED_MULTICOMPONENT_ESCAPE_17','no_git_mutation':True,
    'entry_dependency_hashes_matched':e['pins_verified'],'final_old_pin_independent_recheck':'NOT_RUN_PENDING_CAP',
    'publication_checks':'required artifacts, Python syntax, resource arithmetic, tracked provenance only',
    'not_a_semantic_or_independent_audit':True})
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
    for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
out('campaign_manifest.json',{'status':'UNRESOLVED_CONTENT_CHECKPOINT_NO_NEW_SEAL',
    'is_proof_seal':False,'principal_mathematical_proof_complete':False,'files':files,
    'resources_sha256':sha(B/'resources_checkpoint.json')})
print(json.dumps({'outcome':'UNRESOLVED','Gate_U17':'U-OPEN','files':len(files),
    'cumulative_CPU':total,'remaining_CPU':7200-total,'groups':groups,
    'new_source_engine_calls':calls,'new_independent_runs':0,
    'known_two_component_repair':[[[15,3],[35,2,1]],[[15,5],[35,2,0]]]}),flush=True)
