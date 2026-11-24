"""GSO original paired-credit research and lossless DELETE-gap normalization."""
import sys
import json
import gzip
import argparse
import subprocess
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def run(name,*args):subprocess.run([sys.executable,'-B',str(HERE/name),*args],cwd=HERE,check=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('status','root','research','verify','normalize-gap'),nargs='?',default='status')
    p.add_argument('--trace',default='run/source_0_trace.json.gz')
    p.add_argument('--start',type=int,default=1);p.add_argument('--count',type=int,default=2)
    args=p.parse_args()
    if args.command in ('status','root'):
        path=HERE/'ENGINE_RESULT.json'
        print(path.read_text(encoding='utf-8') if path.exists() else json.dumps({'root_scope':'unrestricted','universal_CD':'OPEN'}));return
    if args.command=='normalize-gap':
        import normalize
        path=HERE/args.trace
        with (gzip.open(path,'rt',encoding='utf-8') if path.suffix=='.gz' else path.open(encoding='utf-8')) as f:source=json.load(f)['source']
        t=normalize.V.immutable(source['initial_A']);assert 1<=args.start and 0<=args.count
        for _,x in source['operations'][:args.start-1]:t,_=normalize.V.V.rebuild(t,x,lambda *args:None,lambda *args:None)
        gap=source['operations'][args.start-1:args.start-1+args.count];assert len(gap)==args.count
        print(json.dumps(normalize.delete_gap(t,gap),indent=2));return
    if args.command=='research':
        assert not (HERE/'FINAL_MANIFEST.json').exists() and not (HERE/'OPTIMIZATION_RESULT.json').exists(),'Use a fresh versioned checkpoint.'
        for name in ('optimize.py','attack.py','induction.py','emit_proof.py','chronology.py','zero_edge.py'):run(name)
        run('zero_edge.py','--cross-block');run('normalize.py')
    for name in ('proofcheck.py','verify.py','verify_zero.py','normalize.py','tests.py','preserve.py'):run(name)
    for name in ('CreditKernel.lean','ExcursionKernel.lean'):
        subprocess.run(['lean','+leanprover/lean4:v4.21.0',str(HERE/name)],cwd=HERE,check=True)
    if (HERE/'FINAL_MANIFEST.json').exists():run('seal.py','--verify')


if __name__=='__main__':main()
