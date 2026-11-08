"""Read-only targeted integrity check after an external archive commit."""
import json,hashlib,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent;REPO=BASE.parent.parent
def main():
    entry=json.loads((BASE/'entry_baseline.json').read_text());head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    raw=subprocess.check_output(['git','diff','--name-status','-z',entry['head'],head],text=True).split('\0')
    rows=[];n=0
    while n<len(raw) and raw[n]:
        status=raw[n];name=raw[n+1];n+=2
        assert status=='A',(status,name)
        rows.append(name)
    assert all(p.startswith('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/') for p in rows)
    old={str(Path(q['path']).resolve()).casefold():q for q in entry['files']}
    checked=[];new=[]
    for name in rows:
        p=(REPO/name).resolve();q=old.get(str(p).casefold())
        if q is None:new.append(name);continue
        ext=Path('\\\\?\\'+str(p));digest=hashlib.sha256(ext.read_bytes()).hexdigest()
        assert digest==q['sha256'],name
        checked.append({'file':name,'sha256':digest})
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    report={'status':'PASS_EXTERNAL_ARCHIVE_ONLY_ALL_AFFECTED_INHERITED_BYTES_UNCHANGED',
      'entry_head':entry['head'],'current_head':head,'external_commit_subject':subprocess.check_output(['git','log','-1','--format=%s'],text=True).strip(),
      'changed_paths':len(rows),'all_changes':'additions under DIRECT_U4_PARALLEL_RESEARCH only',
      'affected_inherited_files_rehashed':len(checked),'new_external_files':len(new),
      'no_M3_mathematical_dependency_changed':True,'all_M3_campaign_Git_actions':'read-only',
      'tracked_tree_clean':True,'affected_inherited_files':checked,
      'new_math_checks':0,'metadata_CPU_excluded':time.process_time()}
    with (BASE/'concurrent_archive_integrity.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='affected_inherited_files'},indent=2),flush=True)
if __name__=='__main__':main()
