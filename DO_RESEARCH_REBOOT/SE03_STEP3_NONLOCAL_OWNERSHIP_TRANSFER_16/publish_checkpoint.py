"""Content/resource publication only. No independent proof seal is issued.
This does not resume the interrupted C15 independent pin-check suffix.
"""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
OLD=B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
entry=read(B/'entry.json');prior=read(OLD/'resources_checkpoint.json')
total=entry['prior_uniform_CPU'];groups=entry['inherited_group_CPU'].copy()
runs=[];new_calls=0
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'))
    charge=r['child_CPU']+c['whole_process_CPU_seconds']
    total+=charge;groups[r['group']]+=charge;new_calls+=r['source_engine_calls']
    runs.append({'phase':r['phase'],'group':r['group'],'status':r['status'],
        'child_CPU':r['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],
        'charge':charge,'source_engine_calls':r['source_engine_calls'],
        'peak_working_set_bytes':r['peak_working_set_bytes_observed']})
assert total<7195 and groups['symbolic']<120 and groups['independent']==299.125
assert new_calls==0
required=['SOURCE_SPEC.md','U15_RECONSTRUCTION.md','ZERO_TRANSFER_GRAMMAR.md',
    'SEVEN_KEY_OBSTRUCTION.md','WIDTH_R_MINUS_4_FAMILY.md','OWNERSHIP_TRANSFER_SYSTEM.md',
    'NONLOCAL_AUGMENTATION.md','GLOBAL_NONOVERLAP.md','FROZEN_OWNER_PRESERVATION.md',
    'ABSOLUTE_PERIOD_VALIDITY.md','SIGNED_SOURCE_ACCOUNTING.md','GROUPING_TO_NONLOCAL_BRIDGE.md',
    'GATE_U_DISCHARGE.md','UNIFORM_TRANSFER_VERDICT.md','CASE_LEDGER.md',
    'INDEPENDENT_AUDIT.md','ADVERSARIAL_AUDIT.md','FINAL_VERDICT.md','CHECKPOINT.md','IAGS_BOXES.md']
for name in required:assert (B/name).is_file() and (B/name).stat().st_size>0
for p in B.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=p.name)
assert not (B/'FULL_PROOF.md').exists() and not (B/'RESET_DONOR_THEOREM.md').exists()
assert not (OLD/'partial_seal.json').exists() and not (B/'independent_audit.json').exists()
out('resources_checkpoint.json',{
    'status':'CAPS_PRESERVED_U16_UNRESOLVED_NEW_INDEPENDENT_AUDIT_PENDING',
    'prior_cumulative_CPU':entry['prior_uniform_CPU'],'campaign_CPU':total-entry['prior_uniform_CPU'],
    'cumulative_CPU':total,'remaining_CPU':7200-total,'reserve':5,
    'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],
    'group_remaining':{g:entry['group_caps'][g]-groups[g] for g in groups},
    'independent_remaining_below_unchanged_controller_reserve':True,
    'new_independent_runs':0,'C15_integrity_seal':'PENDING_NOT_COMPLETED_BY_ENTRY_METADATA',
    'campaign_source_engine_calls':new_calls,
    'inherited_C15_source_engine_calls_including_failed_and_recovered_cutoff':5912,
    'C15_plus_C16_source_engine_calls':5912+new_calls,
    'older_query_ledgers':'preserved in pinned predecessors; no new query or counter reset',
    'query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'max_observed_memory_this_campaign':max(r['peak_working_set_bytes'] for r in runs),
    'wall_cap_hours':12,'Bank25':25,'uniform_Bank25_schedule':'OPEN_NOT_PROMOTED',
    'no_cap_reset':True,'all_proof_construction_controller_runs_charged':True,'runs':runs,
    'metadata_CPU_convention':'inherited entry/publication exclusion; no independent check reclassified',
    'metadata_anchor_failures_preserved':['prepare_dependency_ledger.py: absent anticipated C13 FULL_PROOF.md',
        'prepare_dependency_ledger_v2.py: absent anticipated C13 independent_audit.json'],
    'actual_C13_dependencies_discovered':'CORE7_FULL_FUNDING.md and core7_seal.json',
    'publication_metadata_CPU_excluded':time.process_time()})
out('research_status_ledger.json',{
    'principal_outcome':'UNRESOLVED','U16_NONLOCAL':'OPEN','Gate_U16':'U-OPEN',
    'inherited_Gate_U14':'U-B_SUFFICIENT_IMPLICATION_UNCHANGED','CD6_I6':'SEALED_UNCHANGED',
    'Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
    'new_symbolic_results':[
        {'claim':'natural zero hole iff H=c,z1,u0; one slot; r>=4H+1','status':'DERIVED_PROOF_INDEPENDENT_AUDIT_PENDING'},
        {'claim':'exact H1 source word and six A event forms','status':'DERIVED_PROOF_INDEPENDENT_AUDIT_PENDING'},
        {'claim':'comparison own image prefix min(2H,beta+z)','status':'DERIVED_PROOF_INDEPENDENT_AUDIT_PENDING'},
        {'claim':'lazy escape rank/no-repeat/all-old-owner/global nonoverlap','status':'CONDITIONAL_ON_SOURCE_RECIPE_AUDIT_PENDING'}],
    'producer_records':15,'new_source_histories':0,'reused_source_histories':8,
    'reused_actual_erased_owner_variants':7,'new_source_engine_calls':0,
    'new_candidate_failure':'two blocked actual erased13 components versus one originating deep-tail bit; MONOTONE_RESTRICTED_RULE_ONLY; new audit pending',
    'main_theorem_refuted':False,'universal_source_escape_theorem':False,
    'remaining_source_obligations':['source-derived eligible escape at each reached frontier',
        'complete ownership transition/packet/chart interface','other residual and nonmaximal-core licenses',
        'independent-full-license compatibility and Bank25 physical realization'],
    'verification_obligations':['C15 final pin/seal suffix only','new C16 distinct implementation audit'],
    'next_bounded_theorem':'FIRST-SS7-ESCAPE, exact scope in CHECKPOINT.md',
    'content_manifest_is_proof_seal':False})
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
assert git('rev-parse','HEAD')==entry['head']
assert git('branch','--show-current')==entry['branch']
assert not git('status','--porcelain','--untracked-files=no')
out('publication_provenance.json',{'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'writes':'only SE03_STEP3_NONLOCAL_OWNERSHIP_TRANSFER_16','no_git_mutation':True,
    'entry_dependency_hashes_matched':entry['pins_verified'],
    'final_all_old_pin_audit':'NOT_RUN; C15 independent suffix remains pending',
    'publication_validation':'required artifacts present, Python syntax parsed, resource arithmetic and tracked provenance only',
    'not_a_semantic_or_independent_audit':True})
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
    for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
out('campaign_manifest.json',{'status':'UNRESOLVED_CONTENT_CHECKPOINT_NEW_REQUIRED_AUDIT_PENDING',
    'is_proof_seal':False,'accepted_new_universal_source_theorem':False,'files':files,
    'resources_sha256':sha(B/'resources_checkpoint.json')})
print(json.dumps({'outcome':'UNRESOLVED','Gate_U16':'U-OPEN','files':len(files),
    'cumulative_CPU':total,'remaining_CPU':7200-total,'group_CPU':groups,
    'source_engine_calls':new_calls,'new_independent_audit':'NOT_RUN_CAP_PRESERVED'}),flush=True)
