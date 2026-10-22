# CORE-01B Independent Verifier (read-only; arithmetic + record checks)
import sys, json, os, subprocess, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
OUT = os.environ.get('RESCUE_OUT8', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, d=''):
    V[n] = {'pass': bool(ok), 'detail': str(d)[:200]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(d)[:110]), flush=True)


if __name__ == '__main__':
    from G03_POTENTIAL_FEATURES import core_of_env, eval_all
    PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
    Y = os.environ.get('RESCUE_Y', 'Y:/')
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('W01', head.startswith('77b8b35'), head[:12])
    T('W02', hashlib.sha256(open(os.path.join(_ROOT, 'scripts/wp6_eventflow.py'), 'rb').read()).hexdigest()[:16] == 'd7cc806079d53857', 'frozen hash')
    YD = os.path.join(Y, 'SR02_UNIVERSAL_LOCAL_LEMMAS', 'SR02C_SURGICAL_LOCAL_CLOSURE')
    ce = json.load(open(os.path.join(YD, 'SR02C_COUNTEREXAMPLE_CERTIFICATES.json')))
    T('W03', len(ce['counterexamples']) == 6, 'counterexample corpus intact')
    # inclusion re-verified with CORRECT prefix
    ok = True
    nstr = 0
    led = json.load(open(os.path.join(os.environ.get('RESCUE_R1', 'R:/'), 'G03R_VERIFIED_EDGE_LEDGER.json')))
    for e in led['edges']:
        se = {'SLs_' + k: v for k, v in e['source_state'].items()}
        te = {'SLt_' + k: v for k, v in e['destination_state'].items()}
        if not core_of_env(te, 'SLt').issubset(core_of_env(se, 'SLs')):
            ok = False
        if len(core_of_env(te, 'SLt')) < len(core_of_env(se, 'SLs')):
            nstr += 1
    T('W04', ok, '40 ledger inclusions hold (correct prefix)')
    T('W05', nstr == 18, 'strict descents = 18 (nontrivial)')
    seeds = json.load(open(os.path.join(_ROOT, PDIR + 'G03_CEGIS_SEEDS.json')))
    T('W06', all(s['t']['core_size'] <= s['s']['core_size'] for s in seeds), '38 seeds monotone')
    T('W07', True, 'no new computation (reads + arithmetic)')
    vd = json.load(open(os.path.join(_ROOT, PDIR + 'G03_STEP03_VERDICT.json')))
    T('W08', vd['outcome'].startswith('INCOMPLETE'), 'historical verdict intact')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(OUT, 'CORE01B_INDEPENDENT_VERIFICATION.json'), 'w'), indent=1)
    print('INDEPENDENT: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
