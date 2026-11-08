import json,subprocess,hashlib
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_ACL_AUD02');out=BASE/'entry_baseline.json'
assert not out.exists()
paths=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0')
rows=[]
for s in paths:
    if not s or s.startswith(BASE.as_posix()+'/'):continue
    p=Path(s);data=Path('\\\\?\\'+str(p.resolve())).read_bytes()
    rows.append({'path':s,'sha256':hashlib.sha256(data).hexdigest()})
with out.open('x',encoding='utf-8') as f:json.dump(rows,f,indent=2)
print({'entry_files':len(rows)})
