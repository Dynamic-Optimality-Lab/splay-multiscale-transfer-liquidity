"""Resume only publication metadata after concurrent archive verification."""
import json,hashlib,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(n):return json.loads((BASE/n).read_text())
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    a=read('step4_audit.json');s=read('step4_scope_audit.json');c=read('STEP4_CERTIFICATE.json');r=read('resources_final.json')
    assert a['missing_obligations']==0 and a['required_clause_word_obligations']==a['covered_clause_word_obligations']==36972
    assert a['status']=='INDEPENDENT_COMPLETE_STEP4_CERTIFICATE_AUDIT_PASS'
    assert s['status']=='INDEPENDENT_TWO_SORT_AND_HIGH_H0_SCOPE_AUDIT_PASS'
    for n in ('certificate','scope','final_source'):assert read('run_'+n+'_result.json')['status']=='PASS'
    ext=read('concurrent_archive_integrity.json')
    assert ext['status']=='PASS_EXTERNAL_ARCHIVE_ONLY_ALL_AFFECTED_INHERITED_BYTES_UNCHANGED'
    assert ext['no_M3_mathematical_dependency_changed']
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==ext['current_head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    text=(BASE/'RESULT.md').read_text()
    text=text.replace('All14704 inherited files, HEAD and the tracked tree are unchanged.',
      'All14704 inherited file bytes remain unchanged. HEAD advanced by an external archive-only commit; its750 affected inherited files were rehashed successfully. The tracked tree is clean; see INTEGRITY_ADDENDUM.md.')
    text+='\nThis version and final_manifest.json supersede the first metadata publication attempt.\n'
    with (BASE/'RESULT_v2.md').open('x',encoding='utf-8') as f:f.write(text)
    write('CURRENT_STATE_v2.json',{'Step4':'PROVED_UNIVERSAL_CLOSED','remaining_Step4_cases':0,
      'M3':'OPEN_PENDING_REMAINING_POSITIVE_LOW_AND_FULL_COMPOSITION','debt':'STEP4_CERTIFICATE.json',
      'audit':'step4_audit.json','result':'RESULT_v2.md','current_head':ext['current_head'],
      'concurrent_archive_only':True,'all_old_M3_dependencies_unchanged':True,
      'CPU':r['cumulative_uniform_CPU'],'CPU_remaining':r['remaining_CPU_including_reserve']})
    write('publication_attempts.json',{'first_finalize':'stopped at entry-HEAD assertion after external archive commit; mathematical outputs unaffected; no manifest emitted',
      'first_targeted_metadata_audit':'wrong guessed directory prefix; stopped before hashing; corrected in v2',
      'mathematical_checks_replayed':0,'new_CPU_allowance':0,'metadata_only':True})
    pins=[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(BASE.iterdir()) if p.is_file()]
    write('final_manifest.json',{'status':'STEP4_CLOSED_ALL_PUBLICATION_GATES_PASS','files':pins,
      'entry_head':ext['entry_head'],'current_head':ext['current_head'],
      'old_complete_integrity':'final_immutable_integrity.json','concurrent_archive_integrity':'concurrent_archive_integrity.json',
      'old_entry_files':14704,'old_M3_mathematical_dependencies_unchanged':True,
      'Step4_complete':True,'M3_complete':False,'Dynamic_Optimality_proved':False,
      'resources':'resources_final.json','result':'RESULT_v2.md','metadata_CPU_excluded':time.process_time()})
    print(json.dumps({'status':'STEP4_CLOSED_ALL_PUBLICATION_GATES_PASS','clauses':len(c['clauses']),
      'covered_universal_clause_word_obligations':a['covered_clause_word_obligations'],'remaining_Step4_cases':0,
      'CPU':r['cumulative_uniform_CPU'],'remaining_CPU':r['remaining_CPU_including_reserve'],
      'files_pinned':len(pins),'M3_complete':False},indent=2),flush=True)
if __name__=='__main__':main()
