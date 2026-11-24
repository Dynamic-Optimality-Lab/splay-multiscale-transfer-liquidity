"""Trace-aware extension of sealed GSO v1; semantic acceptance gate."""
import sys
import json
import argparse
import subprocess
sys.dont_write_bytecode=True
import trace as X
import trace_teacher as T


REQUIRED=T.induction_contract()['required_proofs']


def accept(candidate,proofs):
    missing=[k for k in REQUIRED if k not in proofs or proofs[k].get('status')!='PROVED_UNIVERSAL']
    # A string supplied by the learner is not a proof. Approved dependencies
    # must be bound to exact verifier receipts and a physical source model.
    unchecked=[k for k in REQUIRED if k in proofs and not proofs[k].get('verifier_receipt')]
    return {'status':'OPEN' if missing or unchecked else 'REQUIRES_INDEPENDENT_PROOF_REVIEW','missing':missing,'unchecked':unchecked,'candidate':candidate,'universal_CD':'OPEN','reason':'No finite computation or self-declared proof label may set PROVED_UNIVERSAL.'}


def status():
    p=X.HERE/'ENGINE_RESULT.json'
    if p.exists():return X.K.load(p)
    return {'engine':'WORKING_TRACE_PORT_BACKEND','universal_CD':'OPEN','acceptance':accept({'mechanism':'trace+ports+cyclic-bank'},{}),'prior_engine':str(X.C.C.PREVIOUS)}


def verify():
    for script in ('verify.py','extra_verify.py','verify_joint.py','tests.py','preserve.py'):
        subprocess.run([sys.executable,'-B',str(X.HERE/script)],check=True,cwd=str(X.HERE))


def research():
    assert not (X.HERE/'FINAL_MANIFEST.json').exists(),'Sealed outputs are read-only; use a fresh versioned copy.'
    stages=[('PINNED_SOURCE_INPUTS.json','pin_inputs.py'),('bootstrap/WORKING_UPGRADE.json','trace.py'),('INDUCTION_INTERFACE.json','trace_teacher.py'),('run_001/SUMMARY.json','research.py'),('run_001/PADDING_PUMP_CERTIFICATE.json','padding_attack.py'),('original_event_companions/trace_17.json.gz','prepare_checks.py'),('SYMBOLIC_MACRO_CERTIFICATE.json','trace_symbolic.py'),('resources_001/SUMMARY.json','resource_audit.py'),('bank_relax_001/SUMMARY.json','bank_relax.py'),('bank_relax_001/resources_15_H5.json.gz','finish_relaxed_resources.py'),('joint_001/CERTIFICATE.json.gz','joint_synthesis.py')]
    report=[]
    for marker,script in stages:
        cached=(X.HERE/marker).exists()
        if not cached:subprocess.run([sys.executable,'-B',str(X.HERE/script)],check=True,cwd=str(X.HERE))
        report.append({'script':script,'reused_existing_artifact':cached})
    verify();print(json.dumps({'stages':report,'root_status':'OPEN','message':'Source/induction acceptance is separate from finite pipeline success.'}))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('status','verify','research','legacy-status'),nargs='?',default='status');args=parser.parse_args()
    if args.command=='status':print(json.dumps(status(),indent=2))
    elif args.command=='verify':verify()
    elif args.command=='research':research()
    else:subprocess.run([sys.executable,'-B',str(X.C.C.PREVIOUS/'gso.py'),'status'],check=True,cwd=str(X.C.C.PREVIOUS))


if __name__=='__main__':main()
