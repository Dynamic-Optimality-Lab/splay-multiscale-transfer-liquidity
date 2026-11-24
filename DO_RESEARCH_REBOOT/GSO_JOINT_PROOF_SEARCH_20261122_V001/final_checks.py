"""Capture final independent verification receipts before sealing."""
import sys
import ast
import json
import re
import time
import hashlib
import platform
import subprocess
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    assert not (HERE/'FINAL_CHECK_RESULTS.json').exists()
    parsed=[]
    for path in sorted(HERE.glob('*.py')):
        ast.parse(path.read_text(encoding='utf-8'),filename=path.name);parsed.append(path.name)
    results=[];lean=[]
    jobs=[(sys.executable,'-B',name) for name in
          ('proofcheck.py','verify_barrier.py','verify_audit.py','verify_metric.py','global_energy.py','tests.py','preserve.py')]
    jobs += [('lean','+leanprover/lean4:v4.21.0',name) for name in ('JointLearnedProof.lean','MetricKernel.lean')]
    for command in jobs:
        started=time.perf_counter()
        r=subprocess.run(command,cwd=HERE,capture_output=True,text=True,encoding='utf-8')
        record={'command':list(command),'exit_code':r.returncode,'seconds':time.perf_counter()-started,
                'stdout':r.stdout,'stderr':r.stderr}
        assert r.returncode==0,record
        if command[0]=='lean':
            assert 'sorryAx' not in r.stdout and 'error:' not in r.stdout
            source=(HERE/command[-1]).read_text(encoding='utf-8')
            assert not re.search(r'\b(sorry|axiom)\b',source)
            record['source_sha256']=hashlib.sha256(source.encode()).hexdigest()
            record['new_axioms_or_error_recovery']=False;lean.append(record)
        results.append(record)
        print(json.dumps({'check':command[-1],'passed':True,'seconds':round(record['seconds'],3)}),flush=True)
    versions=subprocess.run(['lean','+leanprover/lean4:v4.21.0','--version'],cwd=HERE,capture_output=True,text=True,check=True).stdout.strip()
    output={'passed':True,'syntax_files':parsed,'checks':results,'python':platform.python_version(),
            'Lean':versions,'preserved_prior_artifacts':5625,
            'scope':'Independent implementations and Lean proof components, not external peer review or a full original-model formalization.',
            'universal_CD':'OPEN'}
    (HERE/'FINAL_CHECK_RESULTS.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    (HERE/'LEAN_VERIFICATION.json').write_text(json.dumps({'passed':True,'builds':lean,'scope':output['scope']},indent=2),encoding='utf-8')


if __name__=='__main__':main()
