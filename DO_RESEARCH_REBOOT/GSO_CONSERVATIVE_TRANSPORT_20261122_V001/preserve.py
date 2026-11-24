"""Read-only chained preservation of all5403 previous sealed/pinned artifacts."""
import sys
import io
import json
import hashlib
import importlib.util
import contextlib
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREV = HERE.parent/'GSO_PHYSICAL_BANK_RULE_20261122_V001'
ROOT = Path('\\\\?\\'+str(HERE.parent.parent))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    spec = importlib.util.spec_from_file_location('transport_previous_preserve',PREV/'preserve.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream): module.main()
    prior=json.loads(stream.getvalue()); assert prior['passed'] and prior['prior_hashes']==5120
    manifest=json.loads((PREV/'FINAL_MANIFEST.json').read_text(encoding='utf-8')); assert len(manifest['files'])==283
    assert all(digest(PREV/row['path'])==row['sha256'] for row in manifest['files'])
    paths=[PREV/'bank_rule.py',PREV/'fast_trace.py',PREV/'coarsening.py',PREV/'verify.py',
           PREV/'BankKernel.lean',PREV/'counter_001/H8_original_events.json.gz',
           PREV/'counter_001/W_H1_original_events.json.gz',
           HERE.parent/'GSO_TRACE_ENGINE_20261122_V001/trace_teacher.py',
           HERE.parent/'GSO_TRACE_ENGINE_20261122_V001/resource_audit.py',
           HERE.parent/'COVER_FLOW_AUDIT_20261121_V001/verify.py',
           HERE.parent/'RESEARCH_RULES.md']
    pins=[{'path':p.relative_to(HERE.parent.parent).as_posix(),'sha256':digest(p),'bytes':p.stat().st_size} for p in paths]
    audit=json.loads((HERE/'PINNED_AUDIT_TRACES.json').read_text(encoding='utf-8'))
    assert all(digest(ROOT/row['path'])==row['sha256'] for row in audit)
    output={'passed':True,'prior_hashes':5403,'previous_checkpoint_files':283,
            'selected_old_code_inputs':len(pins),'pinned_audit_traces':len(audit),
            'earlier_preservation':prior,'old_code_pins':pins,
            'scope':'Byte integrity and original tracked Git state, not reproof of every earlier theorem.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps({key:output[key] for key in ('passed','prior_hashes','previous_checkpoint_files','selected_old_code_inputs','pinned_audit_traces')}))


if __name__=='__main__': main()
