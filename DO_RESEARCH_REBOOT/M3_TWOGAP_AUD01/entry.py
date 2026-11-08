from pathlib import Path
import json,hashlib,subprocess
BASE=Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01')
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()
def main():
    out=BASE/'entry_baseline.json';assert not out.exists()
    files=[{'path':p.as_posix(),'sha256':sha(p)} for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents]
    status=subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True);assert not status
    obj={'files':files,'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'tracked_status':status}
    with out.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
    print(json.dumps({'old_files':len(files),'head':obj['head']}),flush=True)
if __name__=='__main__':main()
