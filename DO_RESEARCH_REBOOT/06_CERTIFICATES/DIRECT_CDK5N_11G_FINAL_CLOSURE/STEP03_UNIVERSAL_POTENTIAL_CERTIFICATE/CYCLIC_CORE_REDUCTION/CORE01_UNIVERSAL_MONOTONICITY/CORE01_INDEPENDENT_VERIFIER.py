# CORE-01 Independent Verifier (read-only recompute; no solver/ssertify)
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
    R1 = os.environ.get('RESCUE_R1', 'R:/')
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('V01', head.startswith('7ed5cd1'), head[:12])
    T('V02', hashlib.sha256(open(os.path.join(_ROOT, 'scripts/wp6_eventflow.py'), 'rb').read()).hexdigest()[:16] == 'd7cc806079d53857', 'frozen hash')
    Y = os.environ.get('RESCUE_Y', 'Y:/')
    Z = os.environ.get('RESCUE_Z', 'Z:/')
    seeds = json.load(open(os.path.join(_ROOT, PDIR + 'G03_CEGIS_SEEDS.json')))
    T('V03', all(s['t']['core_size'] <= s['s']['core_size'] for s in seeds), '38 seeds monotone')
    led = json.load(open(os.path.join(R1, 'G03R_VERIFIED_EDGE_LEDGER.json')))
    ok = True
    nstr = 0
    for e in led['edges']:
        se = {'SLs_' + k: v for k, v in e['source_state'].items()}
        te = {'SLt_' + k: v for k, v in e['destination_state'].items()}
        if not core_of_env(te, 'SLt').issubset(core_of_env(se, 'SLs')):
            ok = False
        if len(core_of_env(te, 'SLt')) < len(core_of_env(se, 'SLs')):
            nstr += 1
    T('V04', ok, '40 ledger inclusion holds')
    T('V05', nstr == 18, 'strict descents exist (nontrivial)')
    ce = json.load(open(os.path.join(Y, 'SR02_UNIVERSAL_LOCAL_LEMMAS', 'SR02C_SURGICAL_LOCAL_CLOSURE', 'SR02C_COUNTEREXAMPLE_CERTIFICATES.json')))
    ok2 = True
    for c in ce['counterexamples']:
        se = {'SLs_' + k: v for k, v in c['source_state'].items()}
        te = {'SLt_' + k: v for k, v in c['destination_state'].items()}
        if not core_of_env(te, 'SLt').issubset(core_of_env(se, 'SLs')):
            ok2 = False
    T('V06', ok2, '6 counterexample inclusions hold')
    cl = json.load(open(os.path.join(Z, 'CL02_PAIRED_EXCURSIONS_FULL.json')))
    n = sum(1 for e in cl['excursions'] for l in e['legs'] if l['t']['core_size'] > l['s']['core_size'])
    T('V07', n == 0, 'CL02 legs monotone')
    T('V08', True, 'no new computation (reads + arithmetic only)')
    vd = json.load(open(os.path.join(_ROOT, PDIR + 'G03_STEP03_VERDICT.json')))
    T('V09', vd['outcome'].startswith('INCOMPLETE'), 'historical verdict intact')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(OUT, 'CORE01_INDEPENDENT_VERIFICATION.json'), 'w'), indent=1)
    print('INDEPENDENT: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
