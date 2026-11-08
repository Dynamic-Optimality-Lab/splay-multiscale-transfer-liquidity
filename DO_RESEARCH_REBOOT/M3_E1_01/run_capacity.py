"""Outside-E1 phase, allowed only after the independent E1 PASS."""
import json, subprocess, sys, time
from pathlib import Path
BASE = Path(__file__).resolve().parent

def read(name):
    return json.loads((BASE/name).read_text())

def write(name, obj):
    with (BASE/name).open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2)

def main():
    first, first_exit = read('e1_run_result.json'), read('e1_controller_exit.json')
    assert first['status']=='PASS' and first_exit['error'] is None
    prior = 755.203125+first['child_CPU']+first_exit['whole_process_CPU_seconds']
    cap = min(120.0, 7200-prior-time.process_time()-5)
    assert cap>0 and not (BASE/'capacity_audit_exit.json').exists()
    with (BASE/'log_capacity_audit.txt').open('x', encoding='utf-8') as stream:
        process = subprocess.run([sys.executable, '-B', str(BASE/'audit_capacity.py'), str(cap)], stdout=stream, stderr=subprocess.STDOUT)
    exit_result = read('capacity_audit_exit.json')
    audit = read('capacity_audit.json') if (BASE/'capacity_audit.json').exists() else {}
    passed = process.returncode==0 and exit_result['error'] is None and audit.get('status')=='UNIVERSAL_PUBLIC_CAPACITY_AUDIT_PASS'
    write('capacity_run_result.json', {'status':'PASS' if passed else 'FAILED_OR_UNKNOWN_STOP','prior_uniform_CPU_charge':prior,'child_CPU':exit_result['whole_process_CPU_seconds'],'allocated_cap':cap,'returncode':process.returncode,'error':exit_result['error']})
    print(json.dumps({'outside_E1_audit':'PASS' if passed else 'FAILED_OR_UNKNOWN_STOP','child_CPU':exit_result['whole_process_CPU_seconds']}), flush=True)
    assert passed

if __name__=='__main__':
    error = None
    try:
        main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:
        write('capacity_controller_exit.json', {'whole_process_CPU_seconds':time.process_time(),'error':error})
