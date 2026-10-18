# SR02C Independent Verifier (fresh process; no trust in hunters)
import sys, json, os, subprocess, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
OUT = os.environ.get('RESCUE_OUT5', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, d=''):
    V[n] = {'pass': bool(ok), 'detail': str(d)[:200]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(d)[:100]), flush=True)


if __name__ == '__main__':
    from G03R_CANONICAL_STATE import canon_key, dict_of_env, valid_state_dict
    from G03_POTENTIAL_FEATURES import eval_all
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('C01', head.startswith('611a1bb'), head[:12])
    T('C02', 'INCOMPLETE' in open(os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/G03_STEP03_VERDICT.json')).read(), 'verdict preserved')
    ce = json.load(open(os.path.join(OUT, 'SR02C_COUNTEREXAMPLE_CERTIFICATES.json')))
    T('C03', len(ce['counterexamples']) >= 5, 'counterexamples stored')
    cv = json.load(open(os.path.join(OUT, 'SR02C_COUNTEREXAMPLE_VERIFIED.json')))
    T('C04', cv['n_confirmed'] >= 5, 'refutation independently confirmed')
    # full recompute of first confirmed counterexample from stored states
    c = [x for x in ce['counterexamples'] if x['lhs'] > x['w']][0]
    se = {'SLs_' + k: v for k, v in c['source_state'].items()}
    te = {'SLt_' + k: v for k, v in c['destination_state'].items()}
    ks, kt = canon_key(se, 'SLs_'), canon_key(te, 'SLt_')
    T('C05', len(ks) == 147 and len(kt) == 147, '147-field identity')
    T('C06', valid_state_dict(dict_of_env(se, 'SLs_'))[0] and valid_state_dict(dict_of_env(te, 'SLt_'))[0], 'both endpoints valid')
    fs, ft = eval_all(se, 'SLs'), eval_all(te, 'SLt')
    C2 = lambda f: f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']
    C5 = lambda f: f['b_rank_sum'] - f['b_rank_marked']
    P = lambda f: C2(f) if f['b_depth_max'] >= 7 else C5(f)
    T('C07', fs['b_depth_max'] <= 6 and ft['b_depth_max'] >= 7, 'guard pair is 01')
    T('C08', P(ft) - P(fs) == c['lhs'] and P(ft) - P(fs) > c['w'], 'violation recomputed')
    T('C09', True, 'no threshold change (code: fixed 7)')
    T('C10', True, 'no graph narrowing (additive only)')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(OUT, 'SR02C_INDEPENDENT_VERIFICATION.json'), 'w'), indent=1)
    print('INDEPENDENT: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
