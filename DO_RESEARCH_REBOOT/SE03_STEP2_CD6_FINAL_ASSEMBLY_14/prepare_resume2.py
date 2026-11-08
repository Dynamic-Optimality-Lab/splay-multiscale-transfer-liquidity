"""Append-only correction of exec namespace; completed receipts reused."""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/'audit_resume.py').read_text()
old="""def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)"""
new="""def out(n,v):
    if (B/n).exists():
        assert json.loads((B/n).read_text())==json.loads(json.dumps(v));return
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)"""
assert old in s;s=s.replace(old,new)
old="exec(compile(tail,str(B/'audit_final.py')+':UNEXECUTED_REMAINING_SUFFIX','exec'),V.__dict__,namespace)"
new="V.__dict__.update(namespace)\n    exec(compile(tail,str(B/'audit_final.py')+':UNEXECUTED_REMAINING_SUFFIX','exec'),V.__dict__)"
assert old in s;s=s.replace(old,new)
s=s.replace("'audit_resume.py','AUDIT_CONTINUATION.md'","'audit_resume.py','audit_resume2.py','AUDIT_CONTINUATION.md'")
s=s.replace("'audit_resume_exit.json'","'audit_resume2_exit.json'")
with (B/'audit_resume2.py').open('x',encoding='utf-8') as f:f.write(s)
