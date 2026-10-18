# SR02C_COUNTEREXAMPLE_REPLAY.py — independent verification of 0->1 refutations.
# Recomputes from stored FULL states (own code paths): canon keys, validity,
# features, C2/C5/Phi, guard pair, violation. No trust in the hunter's numbers.
import sys, json, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
sys.path.insert(0, _HERE)
OUT = os.environ.get('RESCUE_OUT5', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

if __name__ == '__main__':
    from G03R_CANONICAL_STATE import canon_key, dict_of_env, valid_state_dict, FIELD_ORDER
    from G03_POTENTIAL_FEATURES import eval_all
    ce = json.load(open(os.path.join(OUT, 'SR02C_COUNTEREXAMPLE_CERTIFICATES.json')))
    res = []
    for i, c in enumerate(ce['counterexamples']):
        se = {'SLs_' + k: v for k, v in c['source_state'].items()}
        te = {'SLt_' + k: v for k, v in c['destination_state'].items()}
        try:
            sk = canon_key(se, 'SLs_')
            tk = canon_key(te, 'SLt_')
            okv1, why1 = valid_state_dict(dict_of_env(se, 'SLs_'))
            okv2, why2 = valid_state_dict(dict_of_env(te, 'SLt_'))
        except Exception as e:
            res.append({'idx': i, 'error': str(e)[:120]})
            continue
        fs = eval_all(se, 'SLs')
        ft = eval_all(te, 'SLt')
        C2 = lambda f: f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']
        C5 = lambda f: f['b_rank_sum'] - f['b_rank_marked']
        P = lambda f: C2(f) if f['b_depth_max'] >= 7 else C5(f)
        lhs = P(ft) - P(fs)
        assert lhs == C2(ft) - C5(fs), 'guard-pair must be 01'
        assert fs['b_depth_max'] <= 6 and ft['b_depth_max'] >= 7, 'guard pair must be 01'
        res.append({'idx': i, 'keys_147': len(sk) == 147 and len(tk) == 147,
                    's_valid': bool(okv1), 't_valid': bool(okv2),
                    'C2s': C2(fs), 'C2t': C2(ft), 'C5s': C5(fs), 'C5t': C5(ft),
                    'Phi_s': P(fs), 'Phi_t': P(ft), 'w': c['w'], 'lhs': lhs,
                    'violation': lhs - c['w'], 'confirmed': bool(lhs > c['w']),
                    'provenance': c.get('provenance')})
    nconf = sum(1 for r in res if r.get('confirmed'))
    json.dump({'verified': res, 'n_confirmed': nconf,
               'conclusion': 'CANDIDATE REFUTED' if nconf else 'no confirmed violation'},
              open(os.path.join(OUT, 'SR02C_COUNTEREXAMPLE_VERIFIED.json'), 'w'), indent=1)
    print('confirmed violations: %d/%d' % (nconf, len(res)), flush=True)
    for r in res:
        print({k: r.get(k) for k in ('idx', 'w', 'lhs', 'violation', 'confirmed', 's_valid', 't_valid')}, flush=True)
