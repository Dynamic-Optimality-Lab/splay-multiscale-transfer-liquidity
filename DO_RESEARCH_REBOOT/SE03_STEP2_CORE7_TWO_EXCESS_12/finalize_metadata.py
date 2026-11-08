"""Refresh unsealed proof hash after final notation/word-length copyediting."""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
p=B/'two_slot_certificate.json';d=json.loads(p.read_text())
d['full_proof_sha256']=hashlib.sha256((B/'FULL_PROOF.md').read_bytes()).hexdigest()
with p.open('w',encoding='utf-8') as f:json.dump(d,f,indent=2)
