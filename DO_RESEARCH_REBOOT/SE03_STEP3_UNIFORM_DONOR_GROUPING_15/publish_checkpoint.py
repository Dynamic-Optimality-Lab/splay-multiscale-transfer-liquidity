"""Metadata-only incomplete-campaign publication. NOT a final proof seal."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
entry=read('entry.json');total=entry['prior_uniform_CPU'];groups=entry['inherited_group_CPU'].copy();runs=[];queries=0
for p in sorted(B.glob('run_*_result.json')):
    r=json.loads(p.read_text());c=read('controller_'+r['phase']+'_exit.json');charge=r['child_CPU']+c['whole_process_CPU_seconds']
    q=r['source_engine_calls'];recovered=None
    if r['phase']=='independent' and not (B/'audit_independent_exit.json').exists():
        q=read('independent_audit.json')['source_engine_calls'];recovered='completed pre-cut source-check receipt; controller0 was missing-exit fallback'
    total+=charge;groups[r['group']]+=charge;queries+=q
    runs.append({'phase':r['phase'],'group':r['group'],'status':r['status'],'termination':r['termination'],
        'child_CPU':r['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,
        'source_engine_calls':q,'query_count_recovery':recovered,'reported_probe_quota_not_completed_certificate_count':r['new_finite_tests'],
        'peak_working_set_bytes':r['peak_working_set_bytes_observed']})
assert total<7195 and groups['symbolic']<120 and groups['independent']==299.125 and queries==5912
assert read('independent_audit.json')['status']=='PASS_STATED_UNIFORM_PARTIAL_LEMMAS_FAMILY_PROOF_AND_EXACT_COUNTERCERTIFICATES'
assert not (B/'partial_seal.json').exists() and not (B/'FULL_PROOF.md').exists()
out('resources_checkpoint.json',{'status':'ORIGINAL_CUMULATIVE_CAPS_PRESERVED_INDEPENDENT_GUARD_INTERRUPTED_FINAL_SEAL',
    'prior_cumulative_CPU':entry['prior_uniform_CPU'],'campaign_CPU':total-entry['prior_uniform_CPU'],'cumulative_CPU':total,
    'remaining_CPU':7200-total,'reserve':5,'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],
    'group_remaining':{g:entry['group_caps'][g]-groups[g] for g in groups},'independent_remaining_below_controller_reserve':True,
    'source_engine_calls_including_failed_attempts_and_recovered_cutoff_receipt':queries,'query_cap':2000000,
    'new_complete_source_histories_audited':8,'additional_actual_erased_owner_cases_audited':7,
    'initial_nonfalsifying_probe':'FAILED_EXPECTED_COUNTEREXAMPLE_ASSERTION; no completed certificate promoted',
    'final_source_checks':'PASS_RECEIPT_EXISTS','final_integrity_seal':'INTERRUPTED_CAP_NO_SEAL_ISSUED',
    'controller_internal_child_allocation':2.84375,'observed_child_CPU':2.875,'internal_poll_guard_overshoot':0.03125,
    'original_independent_group_cap_exceeded':False,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'max_observed_memory':max(r['peak_working_set_bytes'] for r in runs),'wall_cap_hours':12,
    'Bank25':'UNCHANGED; no unsupported arbitrary-r working reserve promoted','no_cap_reset':True,
    'all_failed_and_cutoff_runs_charged':True,'runs':runs,
    'metadata_CPU_convention':'inherited entry/publication exclusion; every proof/construction/source/audit/controller charge retained',
    'publication_metadata_CPU_excluded':time.process_time()})
out('research_status_ledger.json',{'principal_outcome':'UNRESOLVED','U_DEEP_GROUP':'OPEN','Gate_U15':'U-OPEN','inherited_Gate_U14':'U-B_UNCHANGED',
    'new_symbolic_results':['uniform path-to-star leaf/branch identity','global raw per-key leaf channels cover every maximal deep pair',
        'fixed-owner partial reduction to distinct ordinary branch frontiers','explicit reset-containing family full physical counting maps for arbitrary r/repetition',
        'r-4 consecutive zero transfers and bounded-own-spare-lookback candidate obstruction'],
    'new_result_publication_status':'SOURCE_CHECKS_COMPLETED; FINAL_PIN_SEAL_PENDING_CAP',
    'candidate_failures':['plain D=L on exact H1Q2 zero edge','specified forward partial leaf-owner completion','fixed bounded-lookback repair using only candidate-unused bits'],
    'unrefuted_not_proved':['unrestricted post-owner candidate-image supply; all seven concrete erasures pass only'],
    'actual_7_key_owner_witness':{'deep_root':[15,4],'first_family_frontier':[39,2],'zero_run_frontier':[41,2],'six_key_owner_map':'actual sealed-CD6 source instantiation'},
    'main_not_refuted':True,'CD6':'SEALED_UNCHANGED','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
    'resume_mechanical':'reuse completed8+7 source checks; finish only final pin/partial-seal suffix when audit allowance exists',
    'resume_mathematical':'source-derived nonlocal repair/reassignment for repeated beta2/z1 zero transfers, exact old owners and Bank25; no assumed image-capacity inequality'})
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
out('publication_provenance.json',{'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),
    'tracked_status':git('status','--porcelain','--untracked-files=no'),'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'writes':'only new SE03_STEP3_UNIFORM_DONOR_GROUPING_15','no_git_mutation':True,
    'entry_pins':2823,'final_full_pin_pass':'INTERRUPTED_NOT_CLAIMED','publication':'checkpoint/content manifest, NOT a proof seal'})
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
out('campaign_manifest.json',{'status':'UNRESOLVED_CHECKPOINT_AFTER_COMPLETED_SOURCE_CHECKS_AND_INTERRUPTED_FINAL_SEAL',
    'is_proof_seal':False,'files':files,'resources_sha256':sha(B/'resources_checkpoint.json'),
    'source_check_receipt_sha256':sha(B/'independent_audit.json')})
print(json.dumps({'principal':'UNRESOLVED','U15':'U-OPEN','source_checks':'8 histories +7 actual owner cases PASS','final_seal':'PENDING_CAP',
    'CPU':total,'remaining_CPU':7200-total,'groups':groups,'queries':queries,'files':len(files)}),flush=True)
