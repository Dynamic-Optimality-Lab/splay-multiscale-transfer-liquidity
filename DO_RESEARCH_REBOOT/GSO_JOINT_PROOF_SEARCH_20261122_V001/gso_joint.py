"""Joint GSO accounting/invariant/induction search and scope-safe acceptance."""
import sys
import json
import argparse
import subprocess
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('status','root','verify','accept','search'),nargs='?',default='status')
    parser.add_argument('--certificate',default='run_005/CONTROL_CERTIFICATE.json')
    parser.add_argument('--scope',choices=('two_targets','unrestricted'),default='unrestricted')
    parser.add_argument('--output-prefix',default='fresh_search')
    parser.add_argument('--cold',action='store_true',help='Learn without reusing prior inductive counterconstraints.')
    args=parser.parse_args()
    if args.command=='status':
        path=HERE/'ENGINE_RESULT.json';print(path.read_text(encoding='utf-8') if path.exists() else json.dumps({'engine':'WORKING_BOUNDED_JOINT_PROOF_SEARCH','universal_CD':'OPEN'}));return
    if args.command=='root':
        import global_energy
        print(json.dumps(global_energy.verify(),indent=2));return
    if args.command=='accept':
        import proofcheck
        result=proofcheck.check(json.loads((HERE/args.certificate).read_text(encoding='utf-8')),args.scope)
        accepted=result['requested_scope_accepted'] and (args.scope!='unrestricted' or result['root_acceptance'])
        print(json.dumps({'accepted_for_requested_scope':accepted,'requested_scope':args.scope,
                          'certificate_scope':result['scope'],'constant':result['constant'],
                          'universal_CD':'PROVED' if accepted and args.scope=='unrestricted' else 'OPEN'}))
        return
    if args.command=='search':
        assert not (HERE/'FINAL_MANIFEST.json').exists(),'Use a fresh versioned checkpoint.'
        import joint
        result=joint.synthesize(args.scope,True,use_cache=not args.cold);joint.write(args.output_prefix+'/CERTIFICATE.json',result)
        print(json.dumps({'status':result['status'],'scope':args.scope,'constant':result.get('constant'),'universal_CD':'OPEN'}));return
    for name in ('proofcheck.py','verify_barrier.py','verify_audit.py','verify_metric.py','global_energy.py','tests.py','preserve.py'):
        subprocess.run([sys.executable,'-B',str(HERE/name)],cwd=str(HERE),check=True)
    subprocess.run(['lean','+leanprover/lean4:v4.21.0',str(HERE/'JointLearnedProof.lean')],cwd=str(HERE),check=True)
    subprocess.run(['lean','+leanprover/lean4:v4.21.0',str(HERE/'MetricKernel.lean')],cwd=str(HERE),check=True)
    if (HERE/'FINAL_MANIFEST.json').exists():
        subprocess.run([sys.executable,'-B',str(HERE/'seal.py'),'--verify'],cwd=str(HERE),check=True)


if __name__=='__main__':main()
