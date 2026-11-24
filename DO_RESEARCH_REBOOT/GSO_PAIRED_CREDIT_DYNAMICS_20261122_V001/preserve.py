"""Read-only verification of all5711 previous pinned/sealed artifacts."""
import sys
import io
import json
import hashlib
import contextlib
import importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PREV=HERE.parent/'GSO_JOINT_PROOF_SEARCH_20261122_V001'


def main():
    spec=importlib.util.spec_from_file_location('paired_credit_previous_preservation',PREV/'preserve.py')
    previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
    output=io.StringIO()
    with contextlib.redirect_stdout(output):previous.main()
    prior=json.loads(output.getvalue());assert prior['passed'] and prior['prior_hashes']==5625
    manifest=json.loads((PREV/'FINAL_MANIFEST.json').read_text(encoding='utf-8'));assert len(manifest['files'])==86
    for row in manifest['files']:
        data=(PREV/row['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes']
    pins=[]
    for rel in ('GSO_CONSERVATIVE_TRANSPORT_20261122_V001/role_synthesis.py',
                'GSO_PHYSICAL_BANK_RULE_20261122_V001/bank_rule.py',
                'H3Q_ANALYSIS_20261120_V001/SYMBOLIC_BLOCK_CERTIFICATE.json',
                'GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001/F2_s2.json.gz'):
        p=HERE.parent/rel;pins.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    result={'passed':True,'prior_hashes':5711,'previous_checkpoint_files':86,'inputs':pins,'inherited':prior,
        'scope':'Byte integrity and inherited tracked Git-state checks, not a reproof of every prior mathematical result.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        p=HERE/'PRESERVATION_VERIFICATION.json'
        if p.exists():assert json.loads(p.read_text())==result
        else:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('passed','prior_hashes','previous_checkpoint_files')}))


if __name__=='__main__':main()
