"""Read-only verification of all5000 prior artifacts plus selected inputs."""
import sys
import io
import json
import hashlib
import importlib.util
import contextlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PREV=HERE.parent/'GSO_COMPOSITION_AUDIT_20261121_V001'


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    spec=importlib.util.spec_from_file_location('trace_old_preservation',PREV/'preserve.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);buffer=io.StringIO()
    with contextlib.redirect_stdout(buffer):m.main()
    old=json.loads(buffer.getvalue());assert old['passed'] and old['prior_hashes']==4926
    manifest=json.loads((PREV/'FINAL_MANIFEST.json').read_text(encoding='utf-8'));assert len(manifest['files'])==74
    assert all(digest(PREV/f['path'])==f['sha256'] for f in manifest['files'])
    root=Path('\\\\?\\'+str(HERE.parent.parent));pins=json.loads((HERE/'PINNED_SOURCE_INPUTS.json').read_text(encoding='utf-8'))
    assert all(digest(root/p['path'])==p['sha256'] for p in pins)
    out={'passed':True,'prior_hashes':5000,'composition_files':74,'selected_input_pins':len(pins),'old_verification':old,'scope':'Byte integrity and tracked Git preservation; not independent reproving of all older mathematics.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'prior_hashes':5000,'selected_input_pins':len(pins)}))


if __name__=='__main__':main()
