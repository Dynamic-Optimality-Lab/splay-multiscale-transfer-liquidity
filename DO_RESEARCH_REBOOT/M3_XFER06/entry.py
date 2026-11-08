"""Read-only immutable baseline; not mathematical execution."""
import hashlib,json,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(Path('\\\\?\\'+str(Path(path).resolve())).read_bytes()).hexdigest()

def main():
    assert not (BASE/'entry_baseline.json').exists()
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    old={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
         'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in BASE.parent.rglob('*')
                  if p.is_file() and BASE not in p.parents]}
    with (BASE/'entry_baseline.json').open('x',encoding='utf-8') as stream:json.dump(old,stream,indent=2)
    print(json.dumps({'old_files':len(old['files']),'head':old['head']}),flush=True)

if __name__=='__main__':main()
