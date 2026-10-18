# SR02 Guard-Case Checker (arithmetic, no solver): verifies B1-B4 identities
# per edge and class counts on all stored grounded corpora.
import sys, json, os
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

if __name__ == '__main__':
    from G03_POTENTIAL_FEATURES import eval_all
    PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
    R1 = os.environ.get('RESCUE_R1', 'R:/')
    V = os.environ.get('RESCUE_OUT4', OUT)
    seeds = json.load(open(_ROOT + '/' + PDIR + 'G03_CEGIS_SEEDS.json'))
    data = [(s['s'], s['t'], s['w']) for s in seeds]
    led = json.load(open(os.path.join(R1, 'G03R_VERIFIED_EDGE_LEDGER.json')))
    for e in led['edges']:
        fs = eval_all({'SLs_' + k: v for k, v in e['source_state'].items()}, 'SLs')
        ft = eval_all({'SLt_' + k: v for k, v in e['destination_state'].items()}, 'SLt')
        if any(v is None for v in list(fs.values()) + list(ft.values())):
            continue
        data.append((fs, ft, e['weight']))
    gf = json.load(open(os.path.join(V, 'SR02_GUARDED_FALSIFY.json')))
    for v in gf['violations']:
        data.append((v['s'], v['t'], v['w']))
    C2 = lambda f: f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']
    C5 = lambda f: f['b_rank_sum'] - f['b_rank_marked']
    g = lambda f: 1 if f['b_depth_max'] >= 7 else 0
    P = lambda f: C2(f) if g(f) else C5(f)
    d = lambda f: C2(f) - C5(f)
    import collections
    pairs = collections.Counter()
    alg_ok = True
    viol = []
    for fs, ft, w in data:
        gs, gt = g(fs), g(ft)
        pairs['%d%d' % (gs, gt)] += 1
        DC5 = C5(ft) - C5(fs)
        if (gs, gt) == (0, 0):
            expect = DC5
        elif (gs, gt) == (1, 1):
            expect = C2(ft) - C2(fs)
        elif (gs, gt) == (0, 1):
            expect = DC5 + d(ft)
        else:
            expect = DC5 - d(fs)
        if expect != P(ft) - P(fs):
            alg_ok = False
        if P(ft) - P(fs) > w:
            viol.append((gs, gt, w, P(ft) - P(fs)))
    json.dump({'n': len(data), 'pairs': dict(pairs), 'algebra_identities_hold': alg_ok,
               'violations': viol}, open(OUT + 'SR02_GUARD_MATRIX.json', 'w'), indent=1)
    print('n=%d pairs=%s alg=%s viol=%s' % (len(data), dict(pairs), alg_ok, viol), flush=True)
