"""Seal or read-only verify this versioned research checkpoint."""
import sys
import json
import hashlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def inventory():
    result=[]
    for path in sorted(HERE.rglob('*')):
        if path.is_file() and path.name!='FINAL_MANIFEST.json':
            data=path.read_bytes();result.append({'path':path.relative_to(HERE).as_posix(),
                'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    return result


def main():
    target=HERE/'FINAL_MANIFEST.json'
    if '--verify' in sys.argv:
        saved=json.loads(target.read_text(encoding='utf-8'));actual=inventory()
        assert saved['files']==actual,'Checkpoint inventory or bytes changed.'
        assert saved['bytes']==sum(r['bytes'] for r in actual)
        print(json.dumps({'passed':True,'files':len(actual),'bytes':saved['bytes'],
                          'preserved_prior_artifacts':saved['preserved_prior_artifacts']}));return
    assert not target.exists(),'Use --verify; a sealed checkpoint is immutable.'
    for name in ('FINAL_CHECK_RESULTS.json','ENGINE_RESULT.json','THEOREM_CERTIFICATE.json',
                 'STRATEGY_REVIEW.json','UNIVERSAL_SOURCE_PROOF_REFERENCE.json'):
        assert (HERE/name).exists(),name
    files=inventory();saved={'version':'GSO_JOINT_PROOF_SEARCH_20261122_V001','files':files,
        'bytes':sum(row['bytes'] for row in files),'preserved_prior_artifacts':5625,
        'universal_CD':'OPEN','scope':'Integrity seal; no mathematical status upgrade.'}
    target.write_text(json.dumps(saved,indent=2),encoding='utf-8')
    print(json.dumps({'sealed_files':len(files),'bytes':saved['bytes'],'preserved_prior_artifacts':5625}))


if __name__=='__main__':main()
