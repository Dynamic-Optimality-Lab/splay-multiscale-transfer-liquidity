import json,hashlib,subprocess
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_POP4_RISK03')
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()
def main():
    out=BASE/'entry_baseline.json';assert not out.exists()
    assert json.loads(Path('DO_RESEARCH_REBOOT/M3_POP4_RISK02/certificate.json').read_text())['new_original_signatures']==236
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    obj={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
      'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents]}
    with out.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
    print(json.dumps({'old_files':len(obj['files']),'head':obj['head']}),flush=True)
if __name__=='__main__':main()
