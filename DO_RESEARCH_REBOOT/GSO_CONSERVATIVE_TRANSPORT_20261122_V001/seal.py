"""Seal only this fresh conservative-transport checkpoint."""
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
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    manifest=HERE/'FINAL_MANIFEST.json'
    paths=sorted(p for p in HERE.rglob('*') if p.is_file() and p!=manifest)
    if args.verify:
        m=json.loads(manifest.read_text(encoding='utf-8'))
        assert {p.relative_to(HERE).as_posix() for p in paths}=={row['path'] for row in m['files']}
        assert all(digest(HERE/row['path'])==row['sha256'] and (HERE/row['path']).stat().st_size==row['bytes'] for row in m['files'])
        assert m['root_status']=='OPEN'
        print(json.dumps({'passed':True,'files':len(paths),'bytes':sum(row['bytes'] for row in m['files']),'root_status':'OPEN'}));return
    assert not manifest.exists(),'Never replace a completed seal.'
    for name in ('INDEPENDENT_VERIFICATION.json','EXTENDED_INDEPENDENT_VERIFICATION.json','PACKET_VERIFICATION.json','PRESERVATION_VERIFICATION.json','LEAN_VERIFICATION.json','FINAL_CHECK_RESULTS.json'):
        assert json.loads((HERE/name).read_text(encoding='utf-8'))['passed']
    notion=json.loads((HERE/'NOTION_PROOF_REFERENCE.json').read_text(encoding='utf-8'));assert notion['readback_verified']
    files=[{'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in paths]
    result={'created_utc':datetime.now(timezone.utc).isoformat(),'root_status':'OPEN',
            'scope':'Conservative bank teacher, source-uniform partial-payment budget and local spine renewal, exact failed entry conjecture; no universal CD proof.',
            'prior_artifacts_preserved':5403,'notion':notion,'files':files}
    manifest.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'sealed':len(files),'bytes':sum(row['bytes'] for row in files),'root_status':'OPEN'}))


if __name__=='__main__':main()
