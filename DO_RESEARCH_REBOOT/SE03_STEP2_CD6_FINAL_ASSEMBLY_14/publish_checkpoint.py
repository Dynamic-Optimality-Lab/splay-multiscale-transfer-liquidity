"""Metadata-only publication after accepted CD6 proof/dependency seal."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
entry=read('entry.json');cert=read('CD6_FINAL_CERTIFICATE.json')
assert cert['outcome']=='A' and cert['status']=='PROVED_COMPLETE_ORIGINAL_SIX_KEY_COARSE_DOUBLE'
assert read('run_resume3_result.json')['status']=='PASS'
for p in cert['files']:assert sha(B/p['path'])==p['sha256'],p['path']
total=entry['prior_uniform_CPU'];groups=entry['inherited_group_CPU'].copy();runs=[];queries=0;rows=0
for p in sorted(B.glob('run_*_result.json')):
    r=json.loads(p.read_text());c=read('controller_'+r['phase']+'_exit.json');charge=r['child_CPU']+c['whole_process_CPU_seconds']
    total+=charge;groups[r['group']]+=charge;queries+=r['source_engine_calls'];rows+=r['old_semantic_rows_replayed']
    runs.append({'phase':r['phase'],'group':r['group'],'status':r['status'],'child_CPU':r['child_CPU'],
        'controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,'source_engine_calls':r['source_engine_calls'],
        'old_semantic_rows_replayed':r['old_semantic_rows_replayed'],'peak_working_set_bytes':r['peak_working_set_bytes_observed']})
assert total<7195 and all(groups[g]<entry['group_caps'][g] for g in groups) and queries==4850 and rows==3328
out('resources_checkpoint.json',{'status':'ALL_CURRENT_CAPS_PRESERVED_NO_RESET','prior_cumulative_CPU':entry['prior_uniform_CPU'],
    'campaign_CPU':total-entry['prior_uniform_CPU'],'cumulative_CPU':total,'remaining_CPU':7200-total,'reserve':5,
    'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],'group_remaining':{g:entry['group_caps'][g]-groups[g] for g in groups},
    'source_engine_calls':queries,'original_source_rows_replayed_once':rows,'resumed_semantic_replays':0,
    'query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'max_observed_memory':max(r['peak_working_set_bytes'] for r in runs),'wall_cap_hours':12,
    'no_new_exhaustive_graph_or_table_run':True,'Bank25':25,'full_witness_working_bound':11,
    'all_failed_runs_and_controllers_charged':True,'runs':runs,
    'metadata_CPU_convention':'inherited entry/publication-only exclusion; every proof/construction/replay/audit/seal and controller charged',
    'publication_metadata_CPU_excluded':time.process_time()})
out('research_status_ledger.json',{'outcome':'A','CD6':'PROVED_COMPLETE_ORIGINAL_SOURCE_DOMAIN',
    'Step2':'COMPLETE_AT_FULL_STATED_SIX_KEY_SOURCE_SCOPE','support_at_most6_scalar':'CD5_PLUS_CD6',
    'six_core_funding_import':'ALL_COMPLETE_AT_EXACT_CERTIFIED_DOMAINS','necessary_masks':57,'global_injection':'EXPLICIT_TOTAL_INJECTIVE_ACTUAL_PERIOD_MAP',
    'frozen_owners':'original common fE and prior natural h0/l a unchanged on their SAME certified aligned domain',
    'special_Step1_allocator_scope':'UNCHANGED_FIVE_KEY_CORE9; no unsupported smaller-core extension assumed',
    'Gate_U14':'U-B','uniform_local_transfer':'PROVED_NONCIRCULAR_SUFFICIENT_INTERFACE',
    'uniform_anonymous_ancestor_source_quotient':'PROVED_BOUND_2r_PLUS_2H_MINUS_3',
    'unchanged_width3_paired_transfer':'REFUTED_BY_INHERITED_MODIFIED_GAMMA_r_FOR_r_AT_LEAST8',
    'uniform_source_supply_and_signed_hypotheses':'OPEN','strong_physical_I5_all_domain_base':'OPEN_UNLESS_SEPARATELY_ASSEMBLED',
    'Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
    'old_refuted_chart_debt_and_adjacent_donor_rule':'REFUTED_STATUSES_PRESERVED',
    'initial_seal_run':'FAILED_AUXILIARY_METADATA_ERASED_KEEP_CONDITION',
    'first_resume':'FAILED_EXEC_NAMESPACE_HARNESS','second_resume':'FAILED_RECEIPT_INDEX_GLOB_HARNESS',
    'accepted_sealing_run':'resume3_PASS; completed source/owner checks reused',
    'next_bounded_theorem':'Source-defined preparation/recovery grouping for arbitrary-r maximal-core deep/q1 packets, globally distinct donors under repeated packets, same frozen owners/period and Bank25'})
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
out('publication_provenance.json',{'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),
    'tracked_status':git('status','--porcelain','--untracked-files=no'),'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'writes':'only SE03_STEP2_CD6_FINAL_ASSEMBLY_14','no_git_mutation':True,'accepted_certificate':'CD6_FINAL_CERTIFICATE.json',
    'accepted_sealing_run':'run_resume3_result.json','original_directive':'USER_DIRECTIVE.txt'})
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
out('campaign_manifest.json',{'status':'OUTCOME_A_AFTER_ACCEPTED_INDEPENDENT_SEAL','files':files,
    'CD6_certificate_sha256':sha(B/'CD6_FINAL_CERTIFICATE.json'),'resource_checkpoint_sha256':sha(B/'resources_checkpoint.json')})
print(json.dumps({'outcome':'A','CD6':'PROVED','Step2':'COMPLETE_SIX_KEY_SOURCE_SCOPE','Gate_U14':'U-B',
    'CPU':total,'groups':groups,'remaining_CPU':7200-total,'files':len(files),'source_rows_replayed_once':rows}),flush=True)
