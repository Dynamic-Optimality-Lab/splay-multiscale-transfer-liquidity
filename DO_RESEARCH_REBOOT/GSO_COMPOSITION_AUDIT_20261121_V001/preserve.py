"""Check all4926 older artifacts and all previous input/seal pins read-only."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'GSO_CONTEXT_LIFECYCLE_20261121_V001'


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    spec=importlib.util.spec_from_file_location('composition_old_preservation',OLD/'preserve.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    output=io.StringIO()
    with contextlib.redirect_stdout(output):module.main()
    prior=json.loads(output.getvalue());assert prior['passed'] and prior['prior_hashes']==4877
    manifest=json.loads((OLD/'FINAL_MANIFEST.json').read_text(encoding='utf-8'));errors=[x['path'] for x in manifest['files'] if digest(OLD/x['path'])!=x['sha256']];assert not errors and len(manifest['files'])==49
    pins=json.loads((HERE/'PINNED_SOURCE_INPUTS.json').read_text(encoding='utf-8')) if (HERE/'PINNED_SOURCE_INPUTS.json').exists() else []
    root=Path('\\\\?\\'+str(HERE.parent.parent));assert all(digest(root/x['path'])==x['sha256'] for x in pins)
    result={'passed':True,'prior_hashes':4926,'earlier_preservation':prior,'previous_context_files':49,'previous_context_bytes':sum(x['bytes'] for x in manifest['files']),'current_input_pins':len(pins),'errors':errors,'scope':'Byte integrity and tracked Git preservation, not independent reproving of all earlier mathematics.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
