"""Read-only metadata audit of every inherited file; no mathematical queries."""
import json,time,subprocess,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent
def main():
    entry=json.loads((BASE/'entry_baseline.json').read_text());fail=[]
    for n,r in enumerate(entry['files']):
        p=Path('\\\\?\\'+str(Path(r['path']).resolve()))
        try:d=hashlib.sha256(p.read_bytes()).hexdigest()
        except Exception as ex:fail.append({'path':r['path'],'error':str(ex)});continue
        if d!=r['sha256']:fail.append({'path':r['path'],'changed':True})
        if (n+1)%5000==0:print(json.dumps({'immutable_files_verified':n+1}),flush=True)
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    tracked=subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    report={'status':'PASS' if not fail and not tracked and head==entry['head'] else 'FAIL',
      'old_files_checked':len(entry['files']),'changed_or_missing':fail,'tracked_status':tracked,
      'head':head,'entry_head':entry['head'],'extended_paths':True,
      'CPU_seconds_metadata_only_excluded_by_inherited_convention':time.process_time(),
      'mathematical_queries':0}
    with (BASE/'final_immutable_integrity.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='changed_or_missing'}),flush=True)
    assert report['status']=='PASS'
if __name__=='__main__':main()
