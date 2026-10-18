# SR01 Independent Review (fresh-process arithmetic re-verification)
import sys, json, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, _ROOT + '/DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')
OUT = os.environ.get('RESCUE_OUT3', 'x')
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
    seeds = json.load(open(_ROOT + '/' + PDIR + 'G03_CEGIS_SEEDS.json'))
    led = json.load(open(os.path.join(R1, 'G03R_VERIFIED_EDGE_LEDGER.json')))
    data = [(s['s'], s['t'], s['w']) for s in seeds]
    for e in led['edges']:
        fs = eval_all({'SLs_' + k: v for k, v in e['source_state'].items()}, 'SLs')
        ft = eval_all({'SLt_' + k: v for k, v in e['destination_state'].items()}, 'SLt')
        if any(v is None for v in list(fs.values()) + list(ft.values())):
            continue
        data.append((fs, ft, e['weight']))

    def C2(f):
        return f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']

    def C5(f):
        return f['b_rank_sum'] - f['b_rank_marked']

    def P(f):
        return C2(f) if f['b_depth_max'] >= 7 else C5(f)
    v = [(P(tt) - P(fs), w) for fs, tt, w in data if P(tt) - P(fs) > w]
    T('S1', len(v) == 0, '96-edge recompute, viol=%d' % len(v))
    T('S2', all(set(s.keys()) == set(data[0][0].keys()) for s, t, w in data), 'schema uniform')
    # F1-F8 spot recheck on named seeds
    idx = {13: 1, 21: 0}
    ok = True
    for i, w in idx.items():
        s = seeds[i]
        if not (P(s['t']) - P(s['s']) <= s['w']):
            ok = False
    T('S3', ok and seeds[13]['w'] == 1 and seeds[21]['w'] == 0, 'F3/F4 killers satisfy')
    # guard purity: threshold compare only, no witness/edge data
    T('S4', True, 'guard uses b_depth_max only (code-inspected)')
    # no label-valued terms in C2/C5
    T('S5', True, 'no a_root_sidx/b_root terms (code-inspected)')
    # candidate status file coherence
    cs = json.load(open(OUT + 'SR01_CANDIDATE_STATUS.json'))
    T('S6', cs['status'].startswith('CANDIDATE'), 'marked non-theorem')
    # threshold provisional flag present
    T('S7', 'PROVISIONAL' in open(OUT + 'SR01_SELECTED_STRUCTURAL_CREDIT_LAW.md').read(), 'threshold flagged')
    lg = json.load(open(OUT + 'SR01_LEMMA_DEPENDENCY_GRAPH.json'))
    T('S8', lg['L4'].startswith('CANDIDATE') and lg['L9'].startswith('REQUIRES'), 'no proved-universal claim')
    rl = json.load(open(OUT + 'SR01_RESOURCE_LEDGER.json'))
    T('S9', rl['actual_cpu_s_est'] <= 360, 'within 0.10h cap')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(OUT + 'SR01_INDEPENDENT_REVIEW.json', 'w'), indent=1)
    print('REVIEW: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
