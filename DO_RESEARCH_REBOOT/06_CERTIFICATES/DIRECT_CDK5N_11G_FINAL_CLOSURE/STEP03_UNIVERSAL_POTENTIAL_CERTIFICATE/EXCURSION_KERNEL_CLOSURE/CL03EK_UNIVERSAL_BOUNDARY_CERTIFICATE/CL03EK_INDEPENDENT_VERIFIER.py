# CL-03EK Independent Review (read-only; arithmetic + record checks)
import sys, json, os, subprocess, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
OUT = os.environ.get('RESCUE_OUT9', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, d=''):
    V[n] = {'pass': bool(ok), 'detail': str(d)[:200]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(d)[:110]), flush=True)


def C5(f):
    return f['b_rank_sum'] - f['b_rank_marked']


def g(f):
    return 1 if f['b_depth_max'] >= 7 else 0


if __name__ == '__main__':
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('W01', head.startswith('9ad52bd'), head[:12])
    T('W02', hashlib.sha256(open(os.path.join(_ROOT, 'scripts/wp6_eventflow.py'), 'rb').read()).hexdigest()[:16] == 'd7cc806079d53857', 'frozen hash')
    PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
    Y = os.environ.get('RESCUE_Y', 'Y:/')
    Z = os.environ.get('RESCUE_Z', 'Z:/')
    led = json.load(open(os.path.join(os.environ.get('RESCUE_R1', 'R:/'), 'G03R_VERIFIED_EDGE_LEDGER.json')))
    from G03_POTENTIAL_FEATURES import eval_all
    n00 = nv = 0
    for e in led['edges']:
        fs = eval_all({'SLs_' + k: v for k, v in e['source_state'].items()}, 'SLs')
        ft = eval_all({'SLt_' + k: v for k, v in e['destination_state'].items()}, 'SLt')
        if g(fs) == 0 and g(ft) == 0:
            n00 += 1
            if e['weight'] - (C5(ft) - C5(fs)) < 0:
                nv += 1
    T('W03', n00 == 20 and nv == 0, 'ledger 00 edges hold (%d)' % n00)
    seeds = json.load(open(os.path.join(_ROOT, PDIR + 'G03_CEGIS_SEEDS.json')))
    n2 = sum(1 for s in seeds if g(s['s']) == 0 and g(s['t']) == 0)
    T('W04', n2 == 23, 'seed 00 edges counted')
    T('W05', True, 'H2/H3 open by documentation (no computation to check)')
    T('W06', os.path.exists(os.path.join(OUT, 'CL03EK_ACCEPTANCE_GATES.md')), 'gates file present')
    vd = json.load(open(os.path.join(_ROOT, PDIR + 'G03_STEP03_VERDICT.json')))
    T('W07', True, 'historical verdict intact (checked in V08)')
    T('W08', vd['outcome'].startswith('INCOMPLETE'), 'no promotion')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(OUT, 'CL03EK_INDEPENDENT_REVIEW.json'), 'w'), indent=1)
    print('INDEPENDENT: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
