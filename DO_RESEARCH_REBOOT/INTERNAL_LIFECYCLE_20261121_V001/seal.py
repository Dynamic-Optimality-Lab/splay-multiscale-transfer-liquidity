"""Seal new artifacts once, or verify the immutable seal without writing."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
HERE = Path(__file__).resolve().parent


def sha(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    path = HERE/'FINAL_MANIFEST.json'
    if args.verify:
        manifest = json.loads(path.read_text(encoding='utf-8'))
        for item in manifest['files']:
            f = HERE/item['path']
            assert f.stat().st_size == item['bytes'] and sha(f) == item['sha256'], item['path']
        assert {str(f.relative_to(HERE)).replace('\\','/') for f in HERE.rglob('*') if f.is_file() and f != path} == {x['path'] for x in manifest['files']}
        print(json.dumps({'seal_verified':True,'files':len(manifest['files']),'bytes':sum(x['bytes'] for x in manifest['files'])}))
        return
    assert not path.exists()
    files = [{'path':str(f.relative_to(HERE)).replace('\\','/'),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(HERE.rglob('*')) if f.is_file()]
    manifest = {'created_utc':datetime.now(timezone.utc).isoformat(),'local_date':'2026-11-21',
                'scope':'New scoped internal-lifecycle proof audit only; universal CD and DO remain open.',
                'notion_proof':'https://app.notion.com/p/41e6251839be81e58078e7d4ebcb3986', 'files':files}
    path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'sealed_files':len(files),'bytes':sum(x['bytes'] for x in files)}))


if __name__ == '__main__':
    main()
