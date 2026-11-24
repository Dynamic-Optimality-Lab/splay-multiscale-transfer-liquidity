"""Integrity seal for the new paired-credit checkpoint; verification is read-only."""
import sys
import json
import hashlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def inventory():
    result=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_file() and p.name!='FINAL_MANIFEST.json':
            b=p.read_bytes();result.append({'path':p.relative_to(HERE).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    return result


def main():
    p=HERE/'FINAL_MANIFEST.json'
    if '--verify' in sys.argv:
        d=json.loads(p.read_text(encoding='utf-8'));actual=inventory()
        assert d['files']==actual and d['bytes']==sum(r['bytes'] for r in actual)
        print(json.dumps({'passed':True,'files':len(actual),'bytes':d['bytes'],'preserved_prior_artifacts':5711}));return
    assert not p.exists(),'Sealed checkpoint is immutable; use --verify.'
    for name in ('FINAL_CHECK_RESULTS.json','ENGINE_RESULT.json','THEOREM_CERTIFICATE.json','STRATEGY_REVIEW.json','PROOF_REFERENCE.json'):
        assert (HERE/name).exists(),name
    files=inventory();d={'checkpoint':'GSO_PAIRED_CREDIT_DYNAMICS_20261122_V001','files':files,'bytes':sum(r['bytes'] for r in files),
        'preserved_prior_artifacts':5711,'universal_CD':'OPEN','scope':'Integrity only; no mathematical status promotion.'}
    p.write_text(json.dumps(d,indent=2),encoding='utf-8');print(json.dumps({'sealed_files':len(files),'bytes':d['bytes'],'preserved_prior_artifacts':5711}))


if __name__=='__main__':main()
