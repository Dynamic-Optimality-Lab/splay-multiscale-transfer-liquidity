import json,hashlib,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()

def main():
    assert not (BASE/'entry_baseline.json').exists()
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    obj={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in BASE.parent.rglob('*') if p.is_file() and BASE not in p.parents]}
    with (BASE/'entry_baseline.json').open('x',encoding='utf-8') as stream:
        json.dump(obj,stream,indent=2)
    print(json.dumps({'old_files':len(obj['files']),'head':obj['head']}),flush=True)

if __name__=='__main__':main()
