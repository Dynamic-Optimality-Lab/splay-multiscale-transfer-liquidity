"""Seal this completed open research checkpoint, or verify it read-only."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');a=p.parse_args();manifest=HERE/'FINAL_MANIFEST.json'
    if a.verify:
        z=json.loads(manifest.read_text(encoding='utf-8'));errors=[x['path'] for x in z['files'] if not (HERE/x['path']).is_file() or digest(HERE/x['path'])!=x['sha256']]
        listed={x['path'] for x in z['files']}|{'FINAL_MANIFEST.json'};actual={str(p.relative_to(HERE)).replace('\\','/') for p in HERE.rglob('*') if p.is_file()};assert not errors and actual==listed
        print(json.dumps({'passed':True,'files':len(z['files']),'bytes':sum(x['bytes'] for x in z['files']),'root_status':'OPEN','notion':z['notion']['url']}));return
    assert not manifest.exists()
    proof=json.loads((HERE/'NOTION_PROOF_REFERENCE.json').read_text());independent=json.loads((HERE/'INDEPENDENT_VERIFICATION.json').read_text());preserved=json.loads((HERE/'PRESERVATION_VERIFICATION.json').read_text());checks=json.loads((HERE/'FINAL_CHECK_RESULTS.json').read_text())
    assert proof['readback_verified'] and all(x['verified'] for x in proof['workspace_updates']) and independent['passed'] and preserved['passed'] and checks['tests_exit_code']==checks['lean_exit_code']==0
    files=[{'path':str(p.relative_to(HERE)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(HERE.rglob('*')) if p.is_file()]
    result={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Exact direct-composition obstruction, valid temporal/raw sharing interfaces, global interaction equivalence and a literature-dependent nonconstant global comparison.','root_status':'OPEN','notion':proof,'files':files};manifest.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({'files':len(files),'bytes':sum(x['bytes'] for x in files),'root_status':'OPEN'}))


if __name__=='__main__':main()
