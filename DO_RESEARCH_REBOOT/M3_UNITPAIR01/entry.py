from pathlib import Path
import json,hashlib,subprocess
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()
def main():
    assert json.loads(Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01/final_manifest.json').read_text())['step3_complete']
    out=BASE/'entry_baseline.json';assert not out.exists();status=subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True);assert not status
    obj={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'tracked_status':status,
      'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents]}
    with out.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
    print(json.dumps({'old_files':len(obj['files']),'head':obj['head']}),flush=True)
if __name__=='__main__':main()
