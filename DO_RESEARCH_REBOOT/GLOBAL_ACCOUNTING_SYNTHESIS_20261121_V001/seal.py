import hashlib
import json
import sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent


def files():
    return [{'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='FINAL_MANIFEST.json']


def main():
    path=HERE/'FINAL_MANIFEST.json'
    if '--verify' in sys.argv:
        saved=json.loads(path.read_text(encoding='utf-8'));assert saved['files']==files()
        print(json.dumps({'passed':True,'files':len(saved['files']),'bytes':sum(z['bytes'] for z in saved['files'])}));return
    assert not path.exists()
    for name in ['INDEPENDENT_VERIFICATION.json','SYMBOLIC_KERNEL_VERIFICATION.json','PRESERVATION_VERIFICATION.json']:
        assert json.loads((HERE/name).read_text(encoding='utf-8'))['passed']
    ref=json.loads((HERE/'NOTION_PROOF_REFERENCE.json').read_text(encoding='utf-8'))
    assert ref['readback_verified'] and all(z['verified'] and z['old_preserved'] for z in ref['workspace_updates'])
    out={'date':'2026-11-21','created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Exact obstruction to the declared whole-operation ten-feature fixed linear potential grammar for every finite C. Universal CD and original residual conservation OPEN.','notion':ref,'files':files()}
    path.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'created':True,'files':len(out['files']),'bytes':sum(z['bytes'] for z in out['files'])}))


if __name__=='__main__':main()
