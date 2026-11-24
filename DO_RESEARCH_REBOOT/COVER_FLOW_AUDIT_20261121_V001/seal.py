"""Create or read-only verify the isolated run's integrity manifest."""
import hashlib
import json
import sys
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent


def entries():
    return [{'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='FINAL_MANIFEST.json']


def main():
    path=HERE/'FINAL_MANIFEST.json'
    if '--verify' in sys.argv:
        saved=json.loads(path.read_text())
        assert saved['files']==entries()
        print(json.dumps({'passed':True,'sealed_files':len(saved['files']),'bytes':sum(x['bytes'] for x in saved['files'])}))
        return
    assert not path.exists()
    finite=json.loads((HERE/'INDEPENDENT_VERIFICATION.json').read_text())
    preserved=json.loads((HERE/'PRESERVATION_VERIFICATION.json').read_text())
    assert finite['passed'] and preserved['passed']
    out={'created_utc':datetime.now(timezone.utc).isoformat(),'local_date':'2026-11-21','timezone':'Asia/Karachi',
         'scope':'Universal original-source six-A mathematical audit and exact all-finite-K cover-policy obstruction. Universal remaining U_int/A conservation OPEN.',
         'notion_status':'Transport unavailable; no manuscript or durable memory write claimed. Unsaved update is given in final chat.',
         'files':entries()}
    path.write_text(json.dumps(out,indent=2))
    print(json.dumps({'created':True,'files':len(out['files']),'bytes':sum(x['bytes'] for x in out['files'])}))


if __name__=='__main__':
    main()
