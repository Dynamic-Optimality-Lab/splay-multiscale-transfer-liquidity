"""Seal only this new checkpoint; preserve all upstream manifests byte-for-byte."""
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args();manifest=HERE/'FINAL_MANIFEST.json'
    if args.verify:
        m=json.loads(manifest.read_text(encoding='utf-8'));expected={r['path'] for r in m['files']};actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and p!=manifest};assert actual==expected
        assert all(digest(HERE/r['path'])==r['sha256'] and (HERE/r['path']).stat().st_size==r['bytes'] for r in m['files']);print(json.dumps({'passed':True,'files':len(expected),'bytes':sum(r['bytes'] for r in m['files']),'root_status':'OPEN'}));return
    assert not manifest.exists()
    for name in ('PRESERVATION_VERIFICATION.json','INDEPENDENT_VERIFICATION.json','EXTRA_INDEPENDENT_VERIFICATION.json','JOINT_INDEPENDENT_VERIFICATION.json','FINAL_CHECK_RESULTS.json'):assert json.loads((HERE/name).read_text(encoding='utf-8'))['passed']
    notion=json.loads((HERE/'NOTION_PROOF_REFERENCE.json').read_text(encoding='utf-8'));assert notion['readback_verified']
    files=[{'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(HERE.rglob('*')) if p.is_file() and p!=manifest]
    m={'created_utc':datetime.now(timezone.utc).isoformat(),'root_status':'OPEN','scope':'Working trace/ports/joint-bank backend; cost-preserving boundary embedding and anonymous-state accounting obstruction; finite exact joint certificates; no universal CD proof.','prior_artifacts_preserved':5000,'notion':notion,'files':files};manifest.write_text(json.dumps(m,indent=2),encoding='utf-8');print(json.dumps({'sealed':len(files),'bytes':sum(r['bytes'] for r in files),'root_status':'OPEN'}))


if __name__=='__main__':main()
