"""Seal this new checkpoint and verify its exact file inventory read-only."""
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    manifest = HERE / 'FINAL_MANIFEST.json'
    inventory = sorted(p for p in HERE.rglob('*') if p.is_file() and p != manifest)
    if args.verify:
        data = json.loads(manifest.read_text(encoding='utf-8'))
        actual = {p.relative_to(HERE).as_posix() for p in inventory}
        assert actual == {row['path'] for row in data['files']}
        assert all(digest(HERE / row['path']) == row['sha256'] and
                   (HERE / row['path']).stat().st_size == row['bytes']
                   for row in data['files'])
        assert data['root_status'] == 'OPEN'
        print(json.dumps({'passed': True, 'files': len(inventory),
                          'bytes': sum(row['bytes'] for row in data['files']), 'root_status': 'OPEN'}))
        return
    assert not manifest.exists(), 'Never overwrite a completed seal.'
    for name in ('PRESERVATION_VERIFICATION.json', 'INDEPENDENT_VERIFICATION.json',
                 'AUDIT_INDEPENDENT_VERIFICATION.json', 'LEAN_VERIFICATION.json',
                 'FINAL_CHECK_RESULTS.json'):
        assert json.loads((HERE / name).read_text(encoding='utf-8'))['passed']
    notion = json.loads((HERE / 'NOTION_PROOF_REFERENCE.json').read_text(encoding='utf-8'))
    assert notion['readback_verified']
    files = [{'path': p.relative_to(HERE).as_posix(), 'bytes': p.stat().st_size,
              'sha256': digest(p)} for p in inventory]
    data = {'created_utc': datetime.now(timezone.utc).isoformat(), 'root_status': 'OPEN',
            'scope': 'Physical monotone bank seam/budget and all-finite-capacity frozen-policy obstruction; no universal CD proof.',
            'prior_artifacts_preserved': 5120, 'notion': notion, 'files': files}
    manifest.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps({'sealed': len(files), 'bytes': sum(row['bytes'] for row in files),
                      'root_status': 'OPEN'}))


if __name__ == '__main__':
    main()
