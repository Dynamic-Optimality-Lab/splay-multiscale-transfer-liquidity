"""Metadata-only publication of immutable receipts and explicit open status.
Does not replay source states, perform new mathematical checks or act as audit.
"""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
OLD=B.parent/'SE03_STEP3_SOURCE_FORCED_MULTICOMPONENT_ESCAPE_17'

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()

entry=read(B/'entry.json');prior=read(OLD/'resources_checkpoint.json')
groups=dict(entry['inherited_group_CPU']);total=entry['prior_uniform_CPU']
runs=[];calls=queries=backend=0;peak=0
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'))
    ex=read(B/('audit_'+r['phase']+'_exit.json'))
    charge=r['child_CPU']+c['whole_process_CPU_seconds']
    total+=charge;groups[r['group']]+=charge
    calls+=r['source_engine_calls'];backend+=ex.get('backend_source_rows_supplied',0)
    # Report direct source query counter where present; otherwise engine calls.
    queries+=ex.get('source_queries',r['source_engine_calls'])
    peak=max(peak,r['peak_working_set_bytes_observed'])
    runs.append({'phase':r['phase'],'group':r['group'],'status':r['status'],
      'child_CPU':r['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],
      'charge':charge,'source_engine_calls':r['source_engine_calls'],
      'backend_source_rows_supplied':ex.get('backend_source_rows_supplied',0),
      'peak_working_set_bytes':r['peak_working_set_bytes_observed'],
      'legacy_unused_new_finite_tests_flag':r['new_finite_tests']})

assert len(runs)==10 and total<entry['global_allowance']-entry['reserve']
assert all(groups[g]<=entry['group_caps'][g] for g in groups)
assert groups['independent']==299.125
assert calls==15969 and queries==39267 and backend==720
required=['SOURCE_SPEC.md','RR7_REFUTATION.md','MARKED_PARENT_THEOREM.md',
 'HIGH_CREATOR_REDUCTION.md','PREFIX_COLLISIONS_AND_LOW_CASES.md',
 'SOURCE_REPAIRS.md','LOW_OVERFLOW_AND_BUNDLE.md','PROOF_STATUS.md',
 'INDEPENDENT_AUDIT_STATUS.md','FINAL_VERDICT.md','CHECKPOINT.md','dependency_ledger.json']
assert all((B/n).is_file() and (B/n).stat().st_size for n in required)
for p in B.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head']
assert not git('status','--porcelain','--untracked-files=no')

resources={'status':'U18_OPEN_RR7_REFUTED_NEW_DERIVATIONS_AUDIT_PENDING',
 'prior_cumulative_CPU':entry['prior_uniform_CPU'],'campaign_CPU':total-entry['prior_uniform_CPU'],
 'cumulative_CPU':total,'remaining_CPU':entry['global_allowance']-total,
 'global_allowance':entry['global_allowance'],'reserve':entry['reserve'],
 'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],
 'group_remaining':{g:entry['group_caps'][g]-v for g,v in groups.items()},
 'independent_remaining_below_unchanged_controller_reserve':True,'new_independent_runs':0,
 'C15_final_integrity_suffix':'PENDING_NOT_COMPLETED_BY_METADATA',
 'C16_C17_C18_distinct_audits':'PENDING',
 'campaign_source_engine_calls':calls,'campaign_reported_source_queries':queries,
 'campaign_backend_source_rows_supplied':backend,
 'C15_through_C18_source_engine_calls':prior['C15_plus_C16_plus_C17_source_engine_calls']+calls,
 'older_query_ledgers':'preserved in pinned predecessors; new source queries and backend rows reported separately, no counter reset',
 'new_original_source_words':3,'new_actual_erased_owner_variants':8,
 'new_source_word_description':'80-operation word in two reflected orientations; additional82-operation LOW overflow word',
 'source_counterconstruction_states':3876,'new_finite_passing_test_promoted_to_universal_proof':False,
 'legacy_flag_correction':'new_finite_tests=0 is unused probe metadata, not zero new source histories',
 'canonical_query_cap':entry['canonical_query_cap'],'live_record_cap':entry['live_record_cap'],
 'DAG_cap':entry['DAG_cap'],'stored_edge_cap':entry['stored_edge_cap'],
 'memory_cap_bytes':entry['memory_cap_bytes'],'max_observed_memory_this_campaign':peak,
 'wall_cap_hours':entry['wall_cap_hours'],'Bank25':entry['Bank25'],
 'general_Bank25_realization':'OPEN_NOT_PROMOTED','no_cap_reset':True,
 'all_source_construction_and_controller_runs_including_failures_charged':True,'runs':runs,
 'metadata_CPU_convention':'inherited entry/publication exclusion only; no mathematical source or independent work relabeled',
 'publication_metadata_CPU_excluded':time.process_time()}
out('resources_checkpoint.json',resources)
out('research_status_ledger.json',{
 'principal_outcome':'UNRESOLVED','U18_ESCAPE':'OPEN','Gate_U18':'U-OPEN',
 'CD6_I6':'SEALED_UNCHANGED','inherited_Gate_U14':'SEALED_SUFFICIENT_IMPLICATION_UNCHANGED',
 'Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
 'RR7_CREATOR_PROTECTION':'REFUTED-DERIVATION / AUDIT-PENDING',
 'marked_creator_event_protection':'REFUTED-DERIVATION / AUDIT-PENDING',
 'all_H1_zero_watched_origins':'PROVED-DERIVATION / AUDIT-PENDING',
 'high_creator_group_tail_reduction':'PROVED-DERIVATION / AUDIT-PENDING',
 'universal_same_macro_tail_sufficiency':'REFUTED-DERIVATION / AUDIT-PENDING',
 'specific_exact_source_repairs':'PROVED-DERIVATION / AUDIT-PENDING',
 'universal_nonlocal_LOW_bundle_supply':'OPEN',
 'nonzero_higherH_and_other_core_residuals':'OPEN',
 'general_physical_Bank25_realization':'OPEN',
 'principal_refuted':False,'new_independent_audits':0,
 'failed_runs_preserved':['marked','marked_owners'],
 'corrected_runs':['marked2','marked_owners2'],
 'next_bounded_theorem':'joint signed nonlocal repayment for immediate H1 SS-to-mixed zero relay, including repeated/shared creator ancestry',
 'manifest_is_proof_seal':False})
out('publication_provenance.json',{'branch':entry['branch'],'HEAD':entry['head'],
 'tracked_status':git('status','--porcelain','--untracked-files=no'),
 'entry_untracked_inventory':'entry.json','new_write_scope':B.relative_to(ROOT).as_posix(),
 'entry_pins_reused':entry['pins_verified'],'entry_all_pin_check_not_repeated':True,
 'metadata_publication_is_independent_audit':False,'all_new_claims_audit_pending':True,
 'old_certificates_modified':False,'no_destructive_git_operation':True,
 'publication_metadata_CPU_excluded':time.process_time()})
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
       for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
out('campaign_manifest.json',{'status':'CONTENT_CHECKPOINT_NOT_PROOF_SEAL',
 'universal_source_forced_escape':'OPEN','files':files})
print(json.dumps({'status':'PUBLISHED_U_OPEN','cumulative_CPU':total,'group_CPU':groups,
 'source_engine_calls':calls,'reported_source_queries':queries,'files':len(files)}))
