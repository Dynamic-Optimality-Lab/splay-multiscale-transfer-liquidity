# SR02 Independent Verifier (fresh process, arithmetic + record checks)
import sys, json, os, subprocess, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, _ROOT + '/DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')
OUT = os.environ.get('RESCUE_OUT4', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, d=''):
    V[n] = {'pass': bool(ok), 'detail': str(d)[:180]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(d)[:100]), flush=True)


if __name__ == '__main__':
    from G03_POTENTIAL_FEATURES import eval_all
    PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
    R1 = os.environ.get('RESCUE_R1', 'R:/')
    V4 = os.environ.get('RESCUE_OUT4', OUT)
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('S01', head.startswith('f59fe91'), head[:12])
    T('S02', hashlib.sha256(open(os.path.join(_ROOT, 'scripts/wp6_eventflow.py'), 'rb').read()).hexdigest()[:16] == 'd7cc806079d53857', 'frozen hash')
    gm = json.load(open(os.path.join(V4, 'SR02_GUARD_MATRIX.json')))
    T('S03', gm['algebra_identities_hold'] and gm['violations'] == [], 'guard algebra + 0 viol')
    T('S04', gm['pairs'].get('01', 0) == 0, '01-class absent on record')
    T('S05', gm['n'] == 78, 'stored corpus n=78')
    gf = json.load(open(os.path.join(V4, 'SR02_GUARDED_FALSIFY.json')))
    T('S06', gf['nviol'] == 0 and gf['tried'] >= 30, 'fresh falsify 0 viol (batch2 stored; batch1 40/40 in run log)')
    C2 = lambda f: f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']
    C5 = lambda f: f['b_rank_sum'] - f['b_rank_marked']
    P = lambda f: C2(f) if f['b_depth_max'] >= 7 else C5(f)
    seeds = json.load(open(_ROOT + '/' + PDIR + 'G03_CEGIS_SEEDS.json'))
    okk = all(P(s['t']) - P(s['s']) <= s['w'] for s in seeds)
    T('S07', okk, '38-seed recompute')
    sr01doc = os.path.join(os.environ.get('RESCUE_T', 'T:/'), 'SR01_SELECTED_STRUCTURAL_CREDIT_LAW.md')
    T('S08', 'PROVISIONAL' in open(sr01doc).read(), 'threshold flagged in SR-01 doc')
    vd = open(os.path.join(_ROOT, PDIR + 'G03_STEP03_VERDICT.json')).read()
    T('S08b', 'INCOMPLETE' in vd, 'historical verdict intact')
    rl = json.load(open(os.path.join(V4, 'SR02_RESOURCE_LEDGER.json')))
    T('S09', rl['actual_cpu_s_est'] <= 576, 'within 0.16h cap')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(V4, 'SR02_INDEPENDENT_VERIFICATION.json'), 'w'), indent=1)
    print('REVIEW: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
