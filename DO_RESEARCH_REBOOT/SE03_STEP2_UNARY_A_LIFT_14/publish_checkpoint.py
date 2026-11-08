"""Metadata-only publication; all mathematical checks are already sealed."""
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
    total+=charge;groups[r['group']]+=charge;queries+=r['source_engine_calls']
    runs.append({'phase':r['phase'],'group':r['group'],'status':r['status'],'child_CPU':r['child_CPU'],
        'controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge,'source_engine_calls':r['source_engine_calls'],
        'peak_working_set_bytes_observed':r['peak_working_set_bytes_observed']})
assert total<7195 and all(groups[g]<entry['group_caps'][g] for g in groups) and queries<2000000
assert read('run_final_result.json')['status']=='PASS'
seal=read('funding_seal.json');assert seal['status']=='PROVED_SOURCE_UNIFORM_CORE9_10_11_PHYSICAL_FUNDING'
out('resources_checkpoint.json',{'status':'ALL_CAPS_PRESERVED_NO_RESET','prior_cumulative_CPU':entry['prior_uniform_CPU'],
    'campaign_CPU':total-entry['prior_uniform_CPU'],'cumulative_CPU':total,'remaining_CPU':7200-total,
    'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],'group_remaining':{g:entry['group_caps'][g]-groups[g] for g in groups},
    'reserve':5,'query_cap':2000000,'campaign_source_engine_calls_including_failed_and_superseded':queries,
    'max_observed_phase_memory':max(r['peak_working_set_bytes_observed'] for r in runs),'memory_cap_bytes':32*1024**3,
    'live_record_cap':2000000,'largest_direct_pair_state_table':max(r['synchronized_states'] for r in read('branch_all_independent_audit.json')['receipts'] if 'synchronized_states' in r),
    'legacy_first_mask_dense_array_cells':879522,'tables_processed_sequentially':True,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'wall_cap_hours':12,'Bank25':25,'proved_working_bank':11,'new_finite_tests':0,'old_semantic_rows_replayed_in_new_owner_audit':0,
    'failed_and_superseded_work_charged':True,'runs':runs,
    'metadata_CPU_excluded_convention':'inherited; entry/publication-only metadata excluded, all proof/construction/replay/audit/seal and controller CPU charged',
    'publication_metadata_CPU_seconds':time.process_time()})
out('research_status_ledger.json',{'outcome':'PROVED_CORE9_10_11_PHYSICAL_SOURCE_FUNDING',
    'unary_lift':{'status':'PROVED','correction':0,'seal':'unary_seal.json'},
    'core9':{'status':'PROVED','masks':21,'A_boundary_population':'arbitrary','max_debt':2},
    'core10':{'status':'PROVED','masks':16,'A_boundary_population':'arbitrary','max_debt':3},
    'core11':{'status':'PROVED','masks':1,'A_boundary_population':'arbitrary','max_debt':3,'actual_q5_q1_sectors':62},
    'source_quotient':{'states':974,'H1':2090,'H2':10198,'source_uniform_lift':'FULL_PROOF.md sections2–3'},
    'owners':'all original natural h0/a/common fE values fixed under original licensed interface','boundary_carry':3,'working_bank':11,
    'Step2_final_all_domain_assembly':'OPEN','CD6_final_assembly':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
    'old_global_normalized_width_two_debt':'REFUTED_UNCHANGED','old_B_only_template':'REFUTED_UNCHANGED',
    'superseded_branch_revision1':'INCOMPLETE_SOURCE_SYNTAX_NOT_A_PROOF','independent_revision1':'FAILED_TUPLE_LIST_COMPARISON_NOT_ACCEPTED',
    'accepted_branch_revision2':'PROVED_COMPLETE_SOURCE_SYNTAX_AND_ALL_SIGNED_ROWS',
    'next_bounded_theorem':'Compose source-normalized core6, sealed7/8 and new9–11 into one source-exact Step2/CD6 base certificate, independently audit all domains/cost/period interfaces before promotion'})
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
out('publication_provenance.json',{'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),
    'tracked_status':git('status','--porcelain','--untracked-files=no'),
    'worktree_status':git('status','--porcelain','--untracked-files=all'),'no_git_mutation':True,
    'writes':'only campaign14 directory','proof_seal':'funding_seal.json'})
# This is a content manifest, not an additional mathematical audit.
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
out('campaign_manifest.json',{'status':'PUBLISHED_AFTER_SUCCESSFUL_PROOF_SEAL','files':files,
    'funding_seal_sha256':sha(B/'funding_seal.json'),'resources_checkpoint_sha256':sha(B/'resources_checkpoint.json')})
print(json.dumps({'outcome':'PROVED_CORE9_10_11_PHYSICAL_FUNDING','CPU':total,'groups':groups,'queries_this_campaign':queries,
    'files':len(files),'stats':seal['stats'],'next':'source-exact Step2/CD6 all-domain assembly'}),flush=True)
