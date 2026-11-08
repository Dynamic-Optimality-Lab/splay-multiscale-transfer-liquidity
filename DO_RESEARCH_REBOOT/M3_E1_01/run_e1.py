"""E1 gate. Stop on first failure; no retries or later phase after failure."""
import json, subprocess, sys, time
from pathlib import Path
BASE = Path(__file__).resolve().parent

def write(name, obj):
    with (BASE / name).open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2)

def main():
    prior = 755.203125
    cap = min(120.0, 7200-prior-time.process_time()-5)
    assert cap > 0 and not (BASE/'e1_audit_exit.json').exists()
    with (BASE/'log_e1_audit.txt').open('x', encoding='utf-8') as stream:
        process = subprocess.run([sys.executable, '-B', str(BASE/'audit_e1.py'), str(cap)], stdout=stream, stderr=subprocess.STDOUT)
    exit_result = json.loads((BASE/'e1_audit_exit.json').read_text())
    audit = json.loads((BASE/'e1_audit.json').read_text()) if (BASE/'e1_audit.json').exists() else {}
    passed = process.returncode == 0 and exit_result['error'] is None and audit.get('status') == 'UNIVERSAL_E1_AUGMENTATION_AUDIT_PASS'
    write('e1_run_result.json', {'status': 'PASS' if passed else 'FAILED_OR_UNKNOWN_STOP', 'prior_uniform_CPU_charge': prior, 'child_CPU': exit_result['whole_process_CPU_seconds'], 'allocated_cap': cap, 'returncode': process.returncode, 'error': exit_result['error'], 'outside_phase_authorized_by_gate': passed})
    print(json.dumps({'E1_audit': 'PASS' if passed else 'FAILED_OR_UNKNOWN_STOP', 'child_CPU': exit_result['whole_process_CPU_seconds']}), flush=True)
    assert passed

if __name__ == '__main__':
    error = None
    try:
        main()
    except BaseException as exception:
        error = {'type': type(exception).__name__, 'message': str(exception)}
        raise
    finally:
        write('e1_controller_exit.json', {'whole_process_CPU_seconds': time.process_time(), 'error': error})
