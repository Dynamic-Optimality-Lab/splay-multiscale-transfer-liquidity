"""Metadata-only C34 entry; preserve accepted controller and cumulative usage."""
import hashlib,json,subprocess,time
from pathlib import Path
START=time.process_time();F=Path(__file__).resolve().parent;P=F.parent;ROOT=P.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';C=B/'SOURCE_JOINT_REPAIR_03'
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT).decode('utf-8',errors='replace').strip()
def main():
    old=json.loads((C/'resources_checkpoint.json').read_text());e=json.loads((B/'entry_authorized1440.json').read_text())
    total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);queries=e['inherited_conservative_queries'];runs=[]
    for rp in sorted(B.glob('run_*_result.json')):
        r=json.loads(rp.read_text());ep=B/('controller_'+r['phase']+'_exit.json');c=json.loads(ep.read_text());amount=r['child_CPU']+c['whole_process_CPU_seconds'];total+=amount;groups[r['group']]+=amount;queries+=r.get('source_queries',0)
        runs.append({'phase':r['phase'],'group':r['group'],'status':r['status'],'charge':amount,'queries':r.get('source_queries',0),'run_sha256':pin(rp),'controller_exit_sha256':pin(ep)})
    assert (total,groups['symbolic'],groups['independent'],queries)==(old['global_CPU'],old['symbolic_CPU'],old['independent_CPU'],old['source_queries'])
    assert e['group_caps']=={'symbolic':1440,'independent':600} and not git('status','--porcelain','--untracked-files=no')
    directive=Path(r'C:\Users\Saif malik\.codex\attachments\6febd06b-f1ed-4ed7-b016-d4605ad37423\Pasted text.txt')
    with (F/'USER_DIRECTIVE.txt').open('x',encoding='utf-8') as f:f.write(directive.read_text(encoding='utf-8-sig'))
    deps=json.loads((C/'dependency_manifest.json').read_text())['dependencies']
    for d in deps:assert pin(Path(d['path']))==d['sha256']
    extra=[(C/'RESULTS_AND_LIMITS.md','LATEST_C33_RESULTS_READ'),(C/'CHECKPOINT.md','LATEST_C33_BOX_READ'),
      (C/'ANCESTOR_RETIREMENT_LEMMA.md','AR_SOURCE_PROOF_INSPECTED'),(C/'MONOTONE_RETURN_SOURCE_FUNDING.md','MR_PROOF_INSPECTED'),
      (C/'EXTREME_TARGET_JOINT_TICKETS.md','EXTREME_PROOF_INSPECTED_SCOPE_MAXIMAL'),(C/'INTERIOR_TICKET_COLLISION.md','SOURCE_COLLISION_AND_EMBEDDING_SCOPE_INSPECTED'),
      (C/'independent_source_audit.json','ACCEPTED_VERIFY79_RECEIPT_READ_REUSED'),(C/'actual_monotone_return_source.json','PINNED_ACTUAL_SOURCE'),
      (C/'actual_auxiliary_owner_extension.json','PINNED_ARCHIVED32_CURRENT36_OWNERS'),(C/'actual_interior_ticket_collision.json','PINNED_LOCAL_SOURCE_COLLISION'),
      (B/'FINAL_C33/PROOF_STATUS_REGISTRY.md','PREVIOUS_REGISTRY_SUPPLEMENTED_BY_LATER_SOURCE03_RESULTS'),
      (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md','ORIGINAL_GATE_CONTRACT_READ'),
      (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CARRY_STORAGE_SEAM.md','ORIGINAL_BANK_CONTRACT_READ'),
      (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md','ORIGINAL_PERIOD_AND_LEGAL_CUT_CONTRACT_READ'),
      (directive,'CURRENT_USER_DIRECTIVE_READ_ALL1211_LINES'),(B/'run_phase_1440.py','UNCHANGED_ACCEPTED_SUCCESSOR_IDENTIFIED_BY_CURRENT_CHECKPOINT')]
    deps.extend({'path':str(p),'sha256':pin(p),'status':s,'inspected':True} for p,s in extra)
    out('entry.json',{'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),'tracked_clean':True,'global_CPU':total,'symbolic_CPU':groups['symbolic'],'independent_CPU':groups['independent'],'source_queries':queries,'caps':{'global':7200,'symbolic':1440,'independent':600,'queries':3000000,'batch':50000,'Bank25':25},'controller':str(B/'run_phase_1440.py'),'active_authorization':str(B/'resource_amendment_1440.json'),'usage_reset':False,'old_failed_charges_retained':True,'historical_charges':runs,'new_cap_request_pending':False})
    out('dependency_manifest.json',{'dependencies':deps,'no_inherited_file_modified':True,'source_status_distinctions_retained':True})
    print(json.dumps({'status':'C34_ENTRY_FROZEN','global_CPU':total,'symbolic_CPU':groups['symbolic'],'independent_CPU':groups['independent'],'queries':queries,'remaining_queries':3000000-queries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('entry_metadata_exit.json',{'metadata_only':True,'whole_process_CPU_seconds':time.process_time(),'error':error})
