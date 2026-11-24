"""Seal this new version once, or verify every sealed artifact read-only."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent


def sha(file):return hashlib.sha256(file.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    path=HERE/'FINAL_MANIFEST.json'
    if args.verify:
        manifest=json.loads(path.read_text())
        for item in manifest['files']:
            file=HERE/item['path'];assert file.stat().st_size==item['bytes'] and sha(file)==item['sha256'],item['path']
        actual={str(f.relative_to(HERE)).replace('\\','/') for f in HERE.rglob('*') if f.is_file() and f!=path}
        assert actual=={x['path'] for x in manifest['files']}
        print(json.dumps({'seal_verified':True,'files':len(actual),'bytes':sum(x['bytes'] for x in manifest['files'])}));return
    assert not path.exists()
    files=[{'path':str(f.relative_to(HERE)).replace('\\','/'),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(HERE.rglob('*')) if f.is_file()]
    manifest={'created_utc':datetime.now(timezone.utc).isoformat(),'local_date':'2026-11-21','timezone':'Asia/Karachi',
              'scope':'New first-hit Hall obstruction and scoped bounded-alignment conservation only; the unrestricted original aggregate target remains open.',
              'notion_proof':'https://app.notion.com/p/41f6251839be81a1ab00fe1038effc58','files':files}
    path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'sealed_files':len(files),'bytes':sum(x['bytes'] for x in files)}))


if __name__=='__main__':main()
