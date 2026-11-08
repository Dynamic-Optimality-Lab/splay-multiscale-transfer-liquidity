"""Restrict receipt discovery to source cases, excluding the recovery index."""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/'audit_resume2.py').read_text()
old="reports=[json.loads(p.read_text()) for p in sorted(B.glob('source_*.json'))]"
new="reports=[json.loads(p.read_text()) for p in sorted(B.glob('source_*.json')) if p.name!='source_receipt_recovery.json']"
assert old in s;s=s.replace(old,new)
s=s.replace("'audit_resume2.py','AUDIT_CONTINUATION.md'","'audit_resume2.py','audit_resume3.py','AUDIT_CONTINUATION.md'")
s=s.replace("'audit_resume2_exit.json'","'audit_resume3_exit.json'")
with (B/'audit_resume3.py').open('x',encoding='utf-8') as f:f.write(s)
