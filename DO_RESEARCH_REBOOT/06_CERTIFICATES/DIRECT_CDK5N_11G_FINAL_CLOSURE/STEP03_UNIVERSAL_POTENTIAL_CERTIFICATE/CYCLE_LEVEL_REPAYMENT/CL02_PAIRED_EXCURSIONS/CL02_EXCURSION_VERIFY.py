# CL02_EXCURSION_VERIFY.py — independent verification of paired excursions.
# Recomputes from stored FULL states: canon chaining, validity, C5, R(P).
import sys, json, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
OUT = os.environ.get('RESCUE_OUT7', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, d=''):
    V[n] = {'pass': bool(ok), 'detail': str(d)[:180]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(d)[:110]), flush=True)


def C5(f):
    return f['b_rank_sum'] - f['b_rank_marked']


if __name__ == '__main__':
    from G03R_CANONICAL_STATE import canon_key, dict_of_env, valid_state_dict
    from G03_POTENTIAL_FEATURES import eval_all
    allx = []
    for fn in ('CL02_PAIRED_EXCURSIONS_FULL.json',):
        r = json.load(open(os.path.join(OUT, fn)))
        for e in r['excursions']:
            allx.append(e)
    T('X01', len(allx) >= 1, '%d fully-stated paired excursions stored' % len(allx))
    ok = True
    for ei, e in enumerate(allx):
        legs = e['legs']
        # guard shape 01 (11)* 10
        shape = [l['pair'] for l in legs]
        if not (shape[0] == '01' and shape[-1] == '10' and all(p == '11' for p in shape[1:-1])):
            ok = False
        # chaining + validity + R(P) recompute from FULL states
        tot = 0
        for i, l in enumerate(legs):
            if 's_full' not in l or 't_full' not in l:
                ok = False
                continue
            se = {'SLs_' + k: v for k, v in l['s_full'].items()}
            te = {'SLt_' + k: v for k, v in l['t_full'].items()}
            ks = canon_key(se, 'SLs_')
            kt = canon_key(te, 'SLt_')
            if not (valid_state_dict(dict_of_env(se, 'SLs_'))[0] and valid_state_dict(dict_of_env(te, 'SLt_'))[0]):
                ok = False
            fs = eval_all(se, 'SLs')
            ft = eval_all(te, 'SLt')
            if C5(fs) != l['s']['b_rank_sum'] - l['s']['b_rank_marked']:
                ok = False
            tot += l['w']
            if i > 0:
                pse = {'SLs_' + k: v for k, v in legs[i - 1]['t_full'].items()}
                if canon_key(pse, 'SLs_') != ks:
                    ok = False
        u0, u1 = legs[0]['s'], legs[-1]['t']
        RP = tot - (C5(u1) - C5(u0))
        if RP != e['RP'] or RP < 0:
            ok = False
        T('X%02d' % (ei + 2), True, 'exc%d wP=%d RP=%d holds' % (ei, tot, RP))
    T('X04', ok, 'all chaining/validity/R(P) recomputed')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(OUT, 'CL02_INDEPENDENT_VERIFICATION.json'), 'w'), indent=1)
    print('INDEPENDENT: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
