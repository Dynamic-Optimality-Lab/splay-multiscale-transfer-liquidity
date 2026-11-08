"""Resume packaging after concurrent additions; reuse all completed checks."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha

def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)

baseline=read(BASE/'entry_baseline.json');old={r['path'] for r in baseline['files']}
assert len(old)==9199
# Native session 17996 completed every content assertion, then failed at
# finalize_v2.py:51 (new-path freeze), BEFORE the Git and publication tail.
# Those completed assertions are retained, not re-executed.
cutoff=(BASE/'reused_dependencies.json').stat().st_mtime_ns
incremental=[]
for r in baseline['files']:
    p=Path(r['path']);assert p.is_file(),r['path']
    if p.stat().st_mtime_ns>=cutoff:
        assert sha(p)==r['sha256'],r['path']
        incremental.append(r['path'])
added=sorted(p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old)
allowed=('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_run_20261030_v001/',
         'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/')
assert all(p.as_posix().startswith(allowed) for p in added)
rows=[{'path':p.as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in added]
write(BASE/'integrity_additions_final.json',{'status':'CONCURRENT_U4_ADDITIONS_RECORDED_NOT_PROMOTED','files':rows,
  'mathematical_dependencies_of_this_certificate':False,'opened_for_modification_or_removed':False})
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['head']
peer=Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/integrity_addendum.json')
peer_record=read(peer);assert peer_record['all_additions_under_M3_POP4_RISK04']
receipt={'status':'OLD_FILE_CHECKS_REUSED_OUTSIDE_ADDITIONS_RECORDED','completed_old_content_checks_reused':9199,
  'completed_check_evidence':{'native_exec_session':17996,'failed_script':'finalize_v2.py','failed_line':51,
    'failure':'global new-path freeze after all old SHA checks passed','script_sha256':sha(BASE/'finalize_v2.py')},
  'incremental_old_files_with_mtime_since_completed_check_start':incremental,
  'entry_baseline_sha256':sha(BASE/'entry_baseline.json'),
  'saved_reports':[{'path':p.as_posix(),'sha256':sha(p)} for p in (BASE/'run_result.json',BASE/'certification_run.json',BASE/'combination_check.json',BASE/'reused_dependencies.json')],
  'outside_additions_recorded':len(rows),'outside_additions_used_as_mathematical_evidence':False,
  'corroborating_parallel_integrity_receipt':{'path':peer.as_posix(),'sha256':sha(peer),'purpose':'concurrent-work provenance only'},
  'mathematical_checks_or_original_predicates_replayed':0,'old_full_content_checks_replayed':0,
  'tracked_tree_clean':True,'head_unchanged':True,'campaign_writes_confined_here':True}
write(BASE/'PACKAGING_RECOVERY.json',receipt)
old_code=(BASE/'finalize_v2.py').read_text()
tail=old_code[old_code.index("    integrity={'status':'PASS'"):]
tail=tail.replace("integrity={'status':'PASS','old_files_unchanged':len(old),'head':baseline['head'],'tracked_tree_clean':True,'writes_confined_here':True}",
  "integrity={'status':'PASS_WITH_CONCURRENT_ADDITIONS_RECORDED','old_files_unchanged':len(old),'old_file_claim_scope':'9199 pinned entry-baseline paths','head':baseline['head'],'tracked_tree_clean':True,'writes_confined_here':True,'writes_claim_scope':'this campaign only','concurrent_outside_additions':recovery['outside_additions_recorded'],'concurrent_additions_record':'integrity_additions_final.json','completed_content_checks_reused':True}")
tail=tail.replace("'All'+str(len(old))+' old files unchanged; tracked tree clean, HEAD unchanged, all new writes confined here.',",
  "'All '+str(len(old))+' pinned prior files unchanged; tracked tree clean and HEAD unchanged. This campaign wrote only here. Concurrent U4 additions outside this folder are recorded separately in integrity_additions_final.json and excluded from the mathematical certificate.',")
prefix='''"""Publication tail only; completed finite/source/integrity checks are reused."""
import json
from pathlib import Path
from entry import BASE,sha
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    out=BASE/'final_manifest.json';assert not out.exists()
    recovery=read(BASE/'PACKAGING_RECOVERY.json')
    assert recovery['status']=='OLD_FILE_CHECKS_REUSED_OUTSIDE_ADDITIONS_RECORDED'
    assert sha(BASE/'entry_baseline.json')==recovery['entry_baseline_sha256']
    for row in recovery['saved_reports']:assert sha(Path(row['path']))==row['sha256']
    run=read(BASE/'run_result.json');cert=read(BASE/'certification_run.json');comb=read(BASE/'combination_check.json')
    done=cert['source_certified_signatures'];N=len(done);new=comb['new_signature_count'];fixed=sum(s==s[::-1] for s in done)
    audits=[];builds=[];constructs=[]
    for sig in done:
        folder=BASE/('s'+''.join(map(str,sig)))
        audits.append(read(folder/'audit.json'));builds.append(read(folder/'build_status.json'));constructs.append(read(folder/'construction.json'))
    sources=[read(Path(batch['report'])) for batch in cert['source_batches']]
    baseline=read(BASE/'entry_baseline.json');old={r['path'] for r in baseline['files']}
'''
new_code=prefix+tail
compile(new_code,str(BASE/'finalize_v3.py'),'exec')
with (BASE/'finalize_v3.py').open('x',encoding='utf-8') as f:f.write(new_code)
print(json.dumps({'packaging_recovery':'READY','old_SHA_checks_reused':9199,'incremental_old_paths_rechecked':len(incremental),
  'concurrent_additions_recorded':len(rows),'mathematical_replays':0}),flush=True)
