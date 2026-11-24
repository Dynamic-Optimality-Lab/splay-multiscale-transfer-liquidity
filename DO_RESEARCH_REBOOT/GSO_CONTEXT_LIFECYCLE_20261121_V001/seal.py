"""Seal only this versioned checkpoint, or verify it without writing."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args();target=HERE/'FINAL_MANIFEST.json'
    if args.verify:
        z=json.loads(target.read_text(encoding='utf-8'));errors=[x['path'] for x in z['files'] if not (HERE/x['path']).is_file() or digest(HERE/x['path'])!=x['sha256']]
        listed={x['path'] for x in z['files']}|{'FINAL_MANIFEST.json'};actual={str(p.relative_to(HERE)).replace('\\','/') for p in HERE.rglob('*') if p.is_file()}
        assert not errors and actual==listed,(errors,actual-listed,listed-actual)
        print(json.dumps({'passed':True,'files':len(z['files']),'bytes':sum(x['bytes'] for x in z['files']),'root_status':z['root_status'],'notion':z['notion']['url']}));return
    assert not target.exists(),'already sealed'
    proof=json.loads((HERE/'NOTION_PROOF_REFERENCE.json').read_text(encoding='utf-8'));assert proof['readback_verified'] and all(x['verified'] for x in proof['workspace_updates'])
    assert json.loads((HERE/'INDEPENDENT_VERIFICATION.json').read_text())['passed'] and json.loads((HERE/'PRESERVATION_VERIFICATION.json').read_text())['passed']
    checks=json.loads((HERE/'FINAL_CHECK_RESULTS.json').read_text());assert checks['tests_exit_code']==0 and checks['lean_exit_code']==0
    files=[{'path':str(p.relative_to(HERE)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(HERE.rglob('*')) if p.is_file()]
    out={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'GSO physical-context compiler, source-uniform restricted core5 theorem, universal core-drop budget and all-scalar equal-core obstruction. Not the unrestricted global bound.','root_status':'OPEN','notion':proof,'files':files}
    target.write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({'files':len(files),'bytes':sum(x['bytes'] for x in files),'root_status':'OPEN'}))


if __name__=='__main__':main()
