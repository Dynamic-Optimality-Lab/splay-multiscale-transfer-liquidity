"""GSO physical-bank continuation: exact policy, fixed-point and source adversary."""
import sys
import json
import argparse
import subprocess
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def run(script):subprocess.run([sys.executable,'-B',str(HERE/script)],check=True,cwd=str(HERE))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('status','verify','research'),nargs='?',default='status');args=parser.parse_args()
    if args.command=='status':
        p=HERE/'ENGINE_RESULT.json';print(p.read_text(encoding='utf-8') if p.exists() else json.dumps({'engine':'WORKING_PHYSICAL_BANK_RULE_BACKEND','source_proof_status':'PENDING_DURABLE_PROOF_REFERENCE','universal_CD':'OPEN'}));return
    if args.command=='research':
        assert not (HERE/'FINAL_MANIFEST.json').exists(),'Sealed checkpoint; use a fresh versioned directory.'
        stages=[('PINNED_SOURCE_INPUTS.json','pin_inputs.py'),('audit_001/SUMMARY.json','bank_rule.py'),('scaling_001/SUMMARY.json','fast_trace.py'),('SYMBOLIC_COARSENING_CERTIFICATE.json','coarsening.py'),('counter_001/SUMMARY.json','family.py'),('counter_001/W_H1_original_events.json.gz','original_events.py'),('SOURCE_INDUCTION_CERTIFICATE.json','source_induction.py'),('REAL_CAPACITY_CERTIFICATE.json','real_capacity.py')]
        for marker,script in stages:
            if not (HERE/marker).exists():run(script)
    for script in ('verify.py','verify_audit.py','tests.py','preserve.py'):run(script)
    subprocess.run(['lean','+leanprover/lean4:v4.21.0',str(HERE/'BankKernel.lean')],check=True,cwd=str(HERE))


if __name__=='__main__':main()
