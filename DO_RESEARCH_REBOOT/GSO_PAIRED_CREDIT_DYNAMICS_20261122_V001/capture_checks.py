"""Capture final proof, physical and preservation checks before sealing."""
import sys
import ast
import json
import re
import time
import subprocess
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists() and not (HERE/'FINAL_CHECK_RESULTS.json').exists()
    syntax=[]
    for p in sorted(HERE.glob('*.py')):ast.parse(p.read_text(encoding='utf-8'),filename=p.name);syntax.append(p.name)
    jobs=[(sys.executable,'-B',s) for s in ('proofcheck.py','verify.py','verify_zero.py','normalize.py','tests.py','preserve.py')]
    jobs += [('lean','+leanprover/lean4:v4.21.0',s) for s in ('CreditKernel.lean','ExcursionKernel.lean')]
    results=[]
    for command in jobs:
        start=time.perf_counter();r=subprocess.run(command,cwd=HERE,capture_output=True,text=True,encoding='utf-8')
        record={'command':list(command),'exit_code':r.returncode,'seconds':time.perf_counter()-start,'stdout':r.stdout,'stderr':r.stderr}
        assert r.returncode==0,record
        if command[0]=='lean':
            source=(HERE/command[-1]).read_text(encoding='utf-8')
            assert 'sorryAx' not in r.stdout and not re.search(r'\b(sorry|axiom)\b',source)
        results.append(record);print(json.dumps({'check':command[-1],'passed':True,'seconds':round(record['seconds'],3)}),flush=True)
    result={'passed':True,'syntax_files':syntax,'checks':results,'prior_artifacts':5711,
        'scope':'Independent implementations and Lean components; not external peer review or an end-to-end original BST formalization.','universal_CD':'OPEN'}
    (HERE/'FINAL_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2),encoding='utf-8')


if __name__=='__main__':main()
