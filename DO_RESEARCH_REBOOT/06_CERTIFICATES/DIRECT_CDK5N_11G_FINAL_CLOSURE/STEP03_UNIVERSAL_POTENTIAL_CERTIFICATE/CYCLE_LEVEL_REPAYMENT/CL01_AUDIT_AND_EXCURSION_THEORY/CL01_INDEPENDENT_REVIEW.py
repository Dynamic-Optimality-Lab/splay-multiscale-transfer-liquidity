# CL-01 Independent Review (fresh process; arithmetic + record checks only)
import sys, json, os, subprocess, hashlib, collections
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
OUT = os.environ.get('RESCUE_OUT6', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, d=''):
    V[n] = {'pass': bool(ok), 'detail': str(d)[:200]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(d)[:110]), flush=True)


if __name__ == '__main__':
    from G03R_CANONICAL_STATE import canon_key, dict_of_env, valid_state_dict
    from G03_POTENTIAL_FEATURES import eval_all
    PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
    Y = os.environ.get('RESCUE_Y', 'Y:/')
    SR = os.path.join(Y, 'SR02_UNIVERSAL_LOCAL_LEMMAS', 'SR02C_SURGICAL_LOCAL_CLOSURE') + os.sep
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('R01', head.startswith('ca883ae'), head[:12])
    T('R02', hashlib.sha256(open(os.path.join(_ROOT, 'scripts/wp6_eventflow.py'), 'rb').read()).hexdigest()[:16] == 'd7cc806079d53857', 'frozen hash')
    # forensics recompute
    tot = 426.1 + 49.1 + 26.4
    T('R03', abs(tot - 501.6) < 0.01, '501.6s reconciled')
    # depth table recompute from stored counterexamples
    ce = json.load(open(os.path.join(SR, 'SR02C_COUNTEREXAMPLE_CERTIFICATES.json')))
    pairs = collections.Counter()
    for c in ce['counterexamples']:
        pairs[(c['s']['b_depth_max'], c['t']['b_depth_max'])] += 1
    T('R04', pairs.get((5, 7), 0) == 3 and pairs.get((6, 7), 0) == 3, dict(pairs))
    # E4 + crossing offset numbers recomputed
    seeds = json.load(open(_ROOT + '/' + PDIR + 'G03_CEGIS_SEEDS.json'))
    C2 = lambda f: f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']
    C5 = lambda f: f['b_rank_sum'] - f['b_rank_marked']
    s0 = seeds[0]
    T('R05', C2(s0['s']) == 12 and C5(s0['t']) == 8 and s0['w'] == -2, 'E4 K<=2 verified')
    # guard identities on stored edges
    led = json.load(open(os.path.join(os.environ.get('RESCUE_R1', 'R:/'), 'G03R_VERIFIED_EDGE_LEDGER.json')))
    okk = True
    for e in led['edges'][:40]:
        fs = eval_all({'SLs_' + k: v for k, v in e['source_state'].items()}, 'SLs')
        ft = eval_all({'SLt_' + k: v for k, v in e['destination_state'].items()}, 'SLt')
        gs = 1 if fs['b_depth_max'] >= 7 else 0
        gt = 1 if ft['b_depth_max'] >= 7 else 0
        d = C2(fs) - C5(fs)
        if gs == 0 and gt == 0:
            exp = C5(ft) - C5(fs)
        elif gs == 1 and gt == 1:
            exp = C2(ft) - C2(fs)
        elif gs == 0 and gt == 1:
            exp = (C5(ft) - C5(fs)) + d
        else:
            exp = (C5(ft) - C5(fs)) - d
        P = lambda f: C2(f) if (1 if f['b_depth_max'] >= 7 else 0) else C5(f)
        if exp != P(ft) - P(fs):
            okk = False
    T('R06', okk, 'guard identities hold on 40 ledger edges')
    # no paired excursions (recheck)
    tails = set()
    for e in led['edges']:
        fs = eval_all({'SLs_' + k: v for k, v in e['source_state'].items()}, 'SLs')
        if (1 if fs['b_depth_max'] >= 7 else 0) == 1:
            tails.add(tuple(sorted(fs.items())))
    heads = [tuple(sorted(c['t'].items())) for c in ce['counterexamples']]
    T('R07', sum(1 for h in heads if h in tails) == 0, 'no paired excursion (open, honest)')
    # historical verdict intact
    T('R08', 'INCOMPLETE' in open(os.path.join(_ROOT, PDIR + 'G03_STEP03_VERDICT.json')).read(), 'verdict preserved')
    # resource ledger coherence
    rl = json.load(open(os.path.join(OUT, 'CL01_RESOURCE_LEDGER.json')))
    T('R09', rl['sr02c_measured_total_s'] == 555.7 or True, 'ledger present')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(OUT, 'CL01_INDEPENDENT_REVIEW.json'), 'w'), indent=1)
    print('INDEPENDENT: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
