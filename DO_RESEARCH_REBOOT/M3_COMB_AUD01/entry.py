import hashlib,json,subprocess
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_COMB_AUD01');out=BASE/'entry_baseline.json';assert not out.exists()
rows=[]
for name in subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0'):
    if not name or name.startswith(BASE.as_posix()+'/'):continue
    p=Path('\\\\?\\'+str(Path(name).resolve()))
    rows.append({'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no']).strip()
with out.open('x',encoding='utf-8') as f:json.dump(rows,f,indent=2)
print({'entry_research_files':len(rows)})
