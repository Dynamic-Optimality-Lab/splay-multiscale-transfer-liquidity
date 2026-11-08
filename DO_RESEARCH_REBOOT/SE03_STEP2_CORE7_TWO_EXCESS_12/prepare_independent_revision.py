"""Preserve syntax-failed draft; produce a corrected, versioned checker."""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/'audit_independent.py').read_text()
s=s.replace("'trust':'same-agent distinct immutable engine and backwards checker; no external or formal peer certification'})",
            "'trust':'same-agent distinct immutable engine and backwards checker; no external or formal peer certification'}")
s=s.replace("'audit_independent_exit.json'","'audit_independent2_exit.json'")
compile(s,'audit_independent2.py','exec')
with (B/'audit_independent2.py').open('x',encoding='utf-8') as f:f.write(s)
