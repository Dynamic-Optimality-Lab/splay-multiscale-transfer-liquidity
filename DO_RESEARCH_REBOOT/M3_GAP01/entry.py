import json,subprocess,hashlib
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_GAP01');out=BASE/'entry_baseline.json';assert not out.exists()
rows=[]
for p in subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0'):
    if not p or p.startswith(BASE.as_posix()+'/'):continue
    q=Path('\\\\?\\'+str(Path(p).resolve()));rows.append({'path':p,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
with out.open('x',encoding='utf-8') as f:json.dump(rows,f,indent=2)
print({'entry_files':len(rows)})
