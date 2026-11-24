"""Read-only verification of all5120 prior sealed/pinned artifacts."""
import sys
import io
import json
import hashlib
import importlib.util
import contextlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PREV=HERE.parent/'GSO_TRACE_ENGINE_20261122_V001'


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    spec=importlib.util.spec_from_file_location('physical_bank_previous_preservation',PREV/'preserve.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):m.main()
    previous=json.loads(buf.getvalue());assert previous['passed'] and previous['prior_hashes']==5000
    manifest=json.loads((PREV/'FINAL_MANIFEST.json').read_text(encoding='utf-8'));assert len(manifest['files'])==120
    assert all(digest(PREV/r['path'])==r['sha256'] for r in manifest['files'])
    root=Path('\\\\?\\'+str(HERE.parent.parent));pins=json.loads((HERE/'PINNED_SOURCE_INPUTS.json').read_text(encoding='utf-8'));assert all(digest(root/r['path'])==r['sha256'] for r in pins)
    out={'passed':True,'prior_hashes':5120,'previous_trace_files':120,'selected_input_pins':len(pins),'earlier_preservation':previous,'scope':'Byte integrity and old tracked Git-state preservation, not reproof of every earlier theorem.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='earlier_preservation'}))


if __name__=='__main__':main()
