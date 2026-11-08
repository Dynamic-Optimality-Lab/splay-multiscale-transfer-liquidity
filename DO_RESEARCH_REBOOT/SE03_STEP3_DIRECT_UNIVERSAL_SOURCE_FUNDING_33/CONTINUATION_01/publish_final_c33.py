"""Metadata-only publication: file hashes, aliases, Git provenance and ledger.
No semantic/source/symbolic execution; CPU separately recorded as metadata.
"""
import hashlib,json,subprocess,time
from pathlib import Path
START=time.process_time();B=Path(__file__).resolve().parent;F=B/'FINAL_C33';O=B/'DIRTY_OWNER_COURSE_CORRECTION';ROOT=B.parents[2]
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def md(n,s):
    with (F/n).open('x',encoding='utf-8') as f:f.write(s)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8',errors='replace').strip()

def main():
    entry=json.loads((B/'entry_authorized1440.json').read_text());old=json.loads((O/'resources_checkpoint_01.json').read_text())
    total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=entry['inherited_conservative_queries'];charges=[]
    for pp in sorted(B.glob('run_*_result.json')):
        z=json.loads(pp.read_text());cc=B/('controller_'+z['phase']+'_exit.json');c=json.loads(cc.read_text())
        charge=z['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;groups[z['group']]+=charge;queries+=z.get('source_queries',0)
        if z['phase'] in ('proof164','verify77'):
            charges.append({'phase':z['phase'],'group':z['group'],'status':z['status'],'child_CPU':z['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,'queries':z.get('source_queries',0),'run_sha256':pin(pp),'controller_exit_sha256':pin(cc)})
    assert len(charges)==2 and all(c['status']=='PASS' for c in charges)
    assert total==old['global_CPU']+sum(c['charge'] for c in charges)
    assert groups['symbolic']==old['symbolic_CPU']+sum(c['charge'] for c in charges if c['group']=='symbolic')
    assert groups['independent']==old['independent_CPU']+sum(c['charge'] for c in charges if c['group']=='independent')
    assert queries==old['source_queries'] and queries<=3000000
    # Preserve the existing course-correction dependencies, checking hashes
    # only. No old semantic certificate is re-executed.
    deps=json.loads((O/'dependency_manifest.json').read_text())['dependencies']
    for d in deps:assert pin(Path(d['path']))==d['sha256']
    extra=[(Path(r'C:\Users\Saif malik\.codex\attachments\5b97da66-d725-442a-a7ef-8677824039a5\Pasted text.txt'),'LATEST_USER_DIRECTIVE_READ_ALL_1066_LINES'),
           (O/'ARBITRARY_DIRTY_FRAME_FINAL_VERDICT.md','ENTRY_VERDICT_INSPECTED'),(O/'C33_NEXT_PARENT_BOX.md','ENTRY_BOX_INSPECTED'),
           (O/'resources_checkpoint_01.json','PRIOR_CUMULATIVE_LEDGER_REUSED'),(B/'resource_amendment_1440.json','ACTIVE_EXPLICIT_AUTHORIZATION'),
           (B/'run_phase_1440.py','UNCHANGED_ACCEPTED_CONTROLLER'),(B.parent/'SOURCE_INTEGRITY.md','ORIGINAL_R1_R4_DEFINITIONS_INSPECTED'),
           (B/'one_helper_original_source_and_owners.json','ACCEPTED_SOURCE_AND_OWNERS_REUSED_BY_HASH'),
           (B/'one_helper_original_source_independent_audit.json','ACCEPTED_PRIMITIVE_RECEIPT_REUSED_NOT_RERUN')]
    deps.extend({'path':str(p),'sha256':pin(p),'status':s,'inspected':True} for p,s in extra)
    out('dependency_manifest.json',{'dependencies':deps,'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),'frozen_files_unchanged':True,'no_semantic_dependency_replay_in_publication':True})
    aliases={
      'C33_FINAL_PARENT_TRANSFER_CONTRACT.md':('PARENT_GATE_U14_CONTRACT.md','Original immutable parent; arbitrary source premises OPEN.'),
      'EASY_HARD_SOURCE_DECOMPOSITION.md':('EASY_HARD_DECOMPOSITION.md','Exact natural/seed split retains all cross-owner and bank interactions.'),
      'JOINT_EXCESS_FRONTIER_SYSTEM.md':('JOINT_FRONTIER_FEASIBILITY_MODEL.md','Actual port quotient; no universal static-policy assumption.'),
      'GLOBAL_FRONTIER_FEASIBILITY_THEOREM.md':('JOINT_FRONTIER_FEASIBILITY_MODEL.md','Q1 is planwise exact; Q2/Q3 require an independently justified factorable policy.'),
      'MINIMAL_JOINT_FRONTIER_OBSTRUCTION.md':('MINIMAL_JOINT_OBSTRUCTION.md','Deficiency-one theorem at its exact fiber; universal source exclusion OPEN.'),
      'SOURCE_FORCED_JOINT_REPAIR_LAW.md':('SOURCE_FORCED_JOINT_REPAIR_THEOREM.md','Universal source law OPEN; conditional composition theorem only.'),
      'GLOBAL_FROZEN_OWNER_PRESERVATION.md':('GLOBAL_OWNER_PRESERVATION.md','No physical owner moves; virtual toggles are proof algebra.'),
      'GLOBAL_EXCESS_FRONTIER_NONCOLLISION.md':('GLOBAL_DONOR_NONCOLLISION.md','One licensed compatible comparison required, not a union of individual repairs.'),
      'GLOBAL_EXCESS_FRONTIER_BANK25_PROOF.md':('BANK25_SCHEDULE_PROOF.md','Seed/own merge theorem conditional on a real source trace; general hard trace OPEN.'),
      'ALL_SUPPORT_JOINT_REPAIR_LIFT.md':('ARBITRARY_SUPPORT_LIFT.md','Uniform structural implications; universal source existence not proved.'),
      'GATE_U14_E2_E3_COMPLETE_BRIDGE.md':('E2_E3_SOURCE_LICENSE_BRIDGE.md','Clause-by-clause bridge audit; E_r2/general hard E_r3 remain OPEN.')}
    for name,(target,status) in aliases.items():md(name,'# Artifact cross-reference\n\n'+status+'\n\nThe full statement, assumptions, proof and qualifications are in ['+target+']('+target+'). This index is not a separate certificate.\n')
    md('ARTIFACT_INDEX.md','''# C33 final continuation index

Principal outcome: OPEN. No universal FULL_PROOF.md exists.

* [Parent contract](PARENT_GATE_U14_CONTRACT.md)
* [Actual residual definition](GENUINE_EXCESS_FRONTIER_DEFINITION.md)
* [Easy/hard composition](EASY_HARD_DECOMPOSITION.md)
* [Joint quotient and exact policy criteria](JOINT_FRONTIER_FEASIBILITY_MODEL.md)
* [Minimal obstruction and source lift](MINIMAL_JOINT_OBSTRUCTION.md)
* [Source-law status and conditional bridge](SOURCE_FORCED_JOINT_REPAIR_THEOREM.md)
* [Frozen owners](GLOBAL_OWNER_PRESERVATION.md)
* [Noncollision](GLOBAL_DONOR_NONCOLLISION.md)
* [Bank merge theorem](BANK25_SCHEDULE_PROOF.md)
* [Uniform quantifiers](ARBITRARY_SUPPORT_LIFT.md)
* [E_r2/E_r3 bridge](E2_E3_SOURCE_LICENSE_BRIDGE.md)
* [Historical controls](INHERITED_COUNTEREXAMPLE_COMPATIBILITY.md)
* [Independent-check scope](INDEPENDENT_AUDIT_STATUS.md)
* [Proof registry](PROOF_STATUS_REGISTRY.md)
* [Gate U readiness](UNIVERSAL_GATE_U_READINESS.md)
* [Final verdict](FINAL_VERDICT.md)
* [Exact next source Box](CHECKPOINT.md)
* [Cumulative resource ledger](resources_checkpoint.json)

New executable receipts: actual_owner_quotient_certificate.json,
quotient_independent_audit.json and symbolic_shared_relay_countermodel.json.
The last is a symbolic model, NOT a source countercertificate. Per-section
alternate artifact names are cross-reference files to these primary proofs.
''')
    tracked=git('status','--porcelain','--untracked-files=no');assert not tracked
    ledger={'status':'CURRENT_C33_FINAL_OFFENSIVE_OPEN','branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),'tracked_clean':not tracked,
      'active_authorization':'../resource_amendment_1440.json','controller':'../run_phase_1440.py','prior_published_ledger':'../DIRTY_OWNER_COURSE_CORRECTION/resources_checkpoint_01.json',
      'global_CPU':total,'global_cap':7200,'symbolic_CPU':groups['symbolic'],'symbolic_cap':1440,'independent_CPU':groups['independent'],'independent_cap':600,
      'source_queries':queries,'source_query_cap':3000000,'remaining_queries':3000000-queries,'query_batch_cap':50000,'Bank25':25,
      'remaining_global_CPU':7200-total,'remaining_symbolic_CPU_including_reserve':1440-groups['symbolic'],'remaining_independent_CPU_including_reserve':600-groups['independent'],
      'global_reserve':5,'controller_reserve':1,'live_state_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,'memory_limit_bytes':34359738368,'wall_limit_hours':12,
      'phase_caps_unchanged':entry['phase_caps'],'default_new_phase_cap':20,'new_charges':charges,'all_historical_charges_including_failures_retained':True,'usage_reset':False,
      'metadata_publication_CPU':'excluded by inherited metadata convention; separately in publication_exit.json','source_execution_in_this_continuation':False,
      'resource_exhaustion_claimed':False,'new_cap_request_pending':False,'principal_C33':'OPEN','outcome':'OPEN_EXACT_JOINT_FRONTIER_SOURCE_OBLIGATION'}
    out('resources_checkpoint.json',ledger)
    files={p.name:pin(p) for p in sorted(F.iterdir()) if p.is_file()}
    scripts={p.name:pin(p) for p in (B/'audit_proof164.py',B/'audit_verify77.py',Path(__file__))}
    out('publication_manifest.json',{'files':files,'new_scripts':scripts,'no_historical_file_overwritten':True,'principal_C33':'OPEN','full_universal_proof_created':False})
    out('publication_seal.json',{'manifest_sha256':pin(F/'publication_manifest.json'),'status':'C33_FINAL_OFFENSIVE_CHECKPOINT_PUBLISHED_OPEN','metadata_only':True})
    print(json.dumps({k:ledger[k] for k in ('status','global_CPU','symbolic_CPU','independent_CPU','source_queries','remaining_queries','principal_C33')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        out('publication_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True,'error':error,'source_queries':0})
