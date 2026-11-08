import json,hashlib,subprocess
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_TWOGAP01')
def digest(p):
    return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()
def main():
    out=BASE/'entry_baseline.json';assert not out.exists()
    rows=[{'path':p.as_posix(),'sha256':digest(p)} for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents]
    obj={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
         'tracked_status':subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True),'files':rows}
    assert not obj['tracked_status'];out.write_text(json.dumps(obj,indent=2),encoding='utf-8')
    print(json.dumps({'old_files':len(rows),'head':obj['head']}),flush=True)
if __name__=='__main__':main()
