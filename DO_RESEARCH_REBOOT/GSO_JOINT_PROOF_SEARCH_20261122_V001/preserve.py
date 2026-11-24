"""Read-only preservation chain for every5625 previous sealed/pinned artifacts."""
import sys
import io
import json
import hashlib
import importlib.util
import contextlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PREV=HERE.parent/'GSO_CONSERVATIVE_TRANSPORT_20261122_V001'


def main():
    spec=importlib.util.spec_from_file_location('joint_previous_preserve',PREV/'preserve.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream):module.main()
    prior=json.loads(stream.getvalue());assert prior['passed'] and prior['prior_hashes']==5403
    manifest=json.loads((PREV/'FINAL_MANIFEST.json').read_text(encoding='utf-8'));assert len(manifest['files'])==222
    assert all(hashlib.sha256((PREV/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in manifest['files'])
    pins=[]
    for rel in ('verify.py','transport.py','role_synthesis.py','GLOBAL_OVERFLOW_RULE_ADMISSION.json'):
        path=PREV/rel if rel!='GLOBAL_OVERFLOW_RULE_ADMISSION.json' else HERE/rel
        pins.append({'path':path.relative_to(HERE.parent.parent).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    old_files=[HERE.parent/'COVER_FLOW_AUDIT_20261121_V001/verify.py',
               HERE.parent/'GSO_PHYSICAL_BANK_RULE_20261122_V001/BankKernel.lean',
               HERE.parent/'GSO_TRACE_ENGINE_20261122_V001/run_001/trace_00.json.gz',
               HERE.parent/'GSO_PHYSICAL_BANK_RULE_20261122_V001/scaling_001/trace_16.json.gz']
    for path in old_files:pins.append({'path':path.relative_to(HERE.parent.parent).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    result={'passed':True,'prior_hashes':5625,'previous_checkpoint_files':222,'pins':pins,
            'earlier_preservation':prior,'scope':'Byte integrity and inherited tracked Git-state checks, not reproof of every historical theorem.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('passed','prior_hashes','previous_checkpoint_files')}))


if __name__=='__main__':main()
