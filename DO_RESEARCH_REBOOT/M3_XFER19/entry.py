"""Read-only extended-path immutable baseline; no mathematical execution."""
import hashlib,json,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
def lp(p):return Path('\\\\?\\'+str(Path(p).resolve()))
def normal(p):
    s=str(p)
    return Path(s[4:] if s.startswith('\\\\?\\') else s)
def sha(p):return hashlib.sha256(lp(p).read_bytes()).hexdigest()
def main():
    assert not (BASE/'entry_baseline.json').exists()
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    files=[]
    for ext in lp(BASE.parent).rglob('*'):
        if not ext.is_file():continue
        p=normal(ext)
        if BASE in p.parents:continue
        files.append({'path':p.as_posix(),'sha256':sha(p)})
        if len(files)%5000==0:print(json.dumps({'prior_files_pinned':len(files)}),flush=True)
    result={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
      'extended_path_traversal':True,'files':files}
    with (BASE/'entry_baseline.json').open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2)
    print(json.dumps({'old_files':len(files),'extended_paths':True,'head':result['head']}),flush=True)
if __name__=='__main__':main()
