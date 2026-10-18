# SR01_TARGETED_FALSIFY.py — arithmetic tests (no solver) of DERIVED (not fitted)
# candidate credit laws on all grounded edges (38 seeds + 40 ledger).
# Candidates use principled coefficients (2 from w=2H-q; 1 from rank logic).
# Records structural signature of every violation for B/C-phase analysis.
import sys, json, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _HERE
for _ in range(8):
    if os.path.isdir(os.path.join(_ROOT, 'python', 'independent')):
        break
    _up = os.path.dirname(_ROOT)
    if _up == _ROOT:
        break
    _ROOT = _up
if not os.path.isdir(os.path.join(_ROOT, 'python', 'independent')):
    _ROOT = os.environ.get('RESCUE_ROOT', _ROOT)
if _ROOT != os.getcwd():
    os.chdir(_ROOT)
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
R1 = os.environ.get('RESCUE_R1', 'R:/')
OUT = os.environ.get('RESCUE_OUT3', 'S:/')
for v in (OUT,):
    if not v.endswith('/') and not v.endswith('\\'):
        OUT = v + '/'

CANDS = {
    'rank_sum': lambda f: f['b_rank_sum'],
    'rank_minus_dmax': lambda f: f['b_rank_sum'] - f['b_depth_max'],
    'rank_minus_dmax_plus_marked': lambda f: f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count'],
    'bdepth_minus_2occupancy': lambda f: f['b_depth_sum'] - 2 * f['a_nslots'],
    'markeddepth_minus_2arank': lambda f: f['b_marked_depth_sum'] - 2 * f['a_rank_sum'],
    'rankmarked_minus_dmax': lambda f: f['b_rank_marked'] - f['b_depth_max'],
}


def sig(s, t):
    return {'d_broot': t['b_root'] - s['b_root'],
            'd_dmax': t['b_depth_max'] - s['b_depth_max'],
            'd_dsum': t['b_depth_sum'] - s['b_depth_sum'],
            'd_rank': t['b_rank_sum'] - s['b_rank_sum'],
            'd_marked': t['a_marked_count'] - s['a_marked_count'],
            'd_occ': t['a_nslots'] - s['a_nslots'],
            'd_arank': t['a_rank_sum'] - s['a_rank_sum']}


if __name__ == '__main__':
    from G03_POTENTIAL_FEATURES import eval_all
    seeds = json.load(open(_ROOT + '/' + PDIR + 'G03_CEGIS_SEEDS.json'))
    data = [('seed%d' % i, s['s'], s['t'], s['w']) for i, s in enumerate(seeds)]
    led = json.load(open(os.path.join(R1, 'G03R_VERIFIED_EDGE_LEDGER.json')))
    for i, e in enumerate(led['edges']):
        se = {('SLs' if False else 'SLs') + '_' + k: v for k, v in e['source_state'].items()}
        te = {'SLt_' + k: v for k, v in e['destination_state'].items()}
        fs = eval_all({'SLs_' + k: v for k, v in e['source_state'].items()}, 'SLs')
        ft = eval_all({'SLt_' + k: v for k, v in e['destination_state'].items()}, 'SLt')
        if any(v is None for v in list(fs.values()) + list(ft.values())):
            continue
        data.append(('led%d' % i, fs, ft, e['weight']))
    print('n edges:', len(data), flush=True)
    res = {}
    for name, fn in CANDS.items():
        viol = []
        for tag, fs, ts, w in data:
            try:
                lhs = fn(ts) - fn(fs)
            except KeyError:
                continue
            if lhs > w:
                viol.append({'edge': tag, 'w': w, 'lhs': lhs, 'sig': sig(fs, ts)})
        res[name] = {'n_viol': len(viol), 'violations': viol[:12]}
        print('%-32s viol=%d' % (name, len(viol)), flush=True)
    json.dump(res, open(OUT + 'SR01_TARGETED_CASE_RESULTS.json', 'w'), indent=1)
    # edge-family matrix (weight identities)
    json.dump({'low': 'w=2H-q, H<=2', 'high': 'w=6-q', 'anomalous': [-3, -2, -1, 0, 1],
               'w_minus4': 'UNSAT-absence (imported, scope-checked)', 'w_minus3': 'UNKNOWN-conditional'},
              open(OUT + 'SR01_EDGE_FAMILY_MATRIX.json', 'w'), indent=1)
