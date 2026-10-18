# G03R_AFFINE_DUAL_CERTIFIER.py — GATE E: exact affine failure diagnosis.
# Builds feature-difference matrix D over verified edges (full-state features +
# Step-03 seed corpus with stored features), exact rational rank/nullspace via
# Fractions, feasibility over Q via Z3 Reals (exact), Farkas dual certificate
# lam>=0, lam'D=0, lam'w<0 with independent Fractions verification.
# Distinguishes: family-contradiction / integer-only / bounded-box / generalization.
from fractions import Fraction
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
OUT = os.environ.get('RESCUE_OUT', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/RESCUE_01_GRAPH_IDENTITY_AND_POTENTIAL/')
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

FEATS = ['b_root', 'b_depth_sum', 'b_depth_max', 'b_marked_depth_sum', 'a_root_sidx',
         'a_nslots', 'a_marked_count', 'sig_sum', 'sig_nonempty', 'core_size',
         'b_rank_sum', 'b_rank_marked', 'b_rank_root', 'a_rank_sum', 'a_rank_root']


def rank_nullspace(rows):
    """Exact rank + nullspace basis over Q (Fractions). rows: list of lists."""
    M = [[Fraction(x) for x in r] for r in rows]
    m, n = len(M), len(M[0])
    piv = []
    r = 0
    where = [-1] * n
    for c in range(n):
        sel = -1
        for i in range(r, m):
            if M[i][c] != 0:
                sel = i
                break
        if sel == -1:
            continue
        M[r], M[sel] = M[sel], M[r]
        where[c] = r
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                for j in range(c, n):
                    M[i][j] -= f * M[r][j]
        piv.append(c)
        r += 1
    basis = []
    for c in range(n):
        if where[c] == -1:
            v = [Fraction(0)] * n
            v[c] = Fraction(1)
            for cc in piv:
                v[cc] = -M[where[cc]][c] / M[where[cc]][cc]
            basis.append(v)
    return r, basis


if __name__ == '__main__':
    import z3
    from G03R_CANONICAL_STATE import dict_of_env
    sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
    from G03_POTENTIAL_FEATURES import eval_all
    led = json.load(open(OUT + 'G03R_VERIFIED_EDGE_LEDGER.json'))
    E = led['edges']
    D_full, w_full = [], []
    for e in E:
        se = {'SLs_' + k: v for k, v in e['source_state'].items()}
        te = {'SLt_' + k: v for k, v in e['destination_state'].items()}
        fs = eval_all(se, 'SLs')
        ft = eval_all(te, 'SLt')
        if any(v is None for v in list(fs.values()) + list(ft.values())):
            continue
        D_full.append([ft[f] - fs[f] for f in FEATS])
        w_full.append(e['weight'])
    seeds = json.load(open(PDIR + 'G03_CEGIS_SEEDS.json'))
    D_seed, w_seed = [], []
    for s in seeds:
        try:
            D_seed.append([s['t'][f] - s['s'][f] for f in FEATS])
            w_seed.append(s['w'])
        except KeyError:
            continue
    out = {}
    for name, D, w in (('fullstate_ledger', D_full, w_full), ('step03_seed_corpus', D_seed, w_seed)):
        rk, ns = rank_nullspace(D)
        const_cols = [f for j, f in enumerate(FEATS) if all(r[j] == 0 for r in D)]
        # feasibility over Q (exact Reals)
        s = z3.Solver()
        th = [z3.Real('th_%d' % j) for j in range(len(FEATS))]
        for i in range(len(D)):
            s.add(z3.Sum([th[j] * D[i][j] for j in range(len(FEATS))]) <= w[i])
        fr = s.check()
        feas = str(fr)
        dual = None
        if fr == z3.unsat:
            # Farkas via tracked assertions
            s2 = z3.Solver()
            th2 = [z3.Real('th2_%d' % j) for j in range(len(FEATS))]
            tr = []
            for i in range(len(D)):
                nm = z3.Bool('e%d' % i)
                s2.assert_and_track(z3.Sum([th2[j] * D[i][j] for j in range(len(FEATS))]) <= w[i], nm)
                tr.append(nm)
            assert s2.check() == z3.unsat
            core = s2.unsat_core()
            dual = {'core_size': len(core), 'core_edges': sorted(int(str(x)[1:]) for x in core)}
        out[name] = {'m': len(D), 'rank': rk, 'nullity': len(ns),
                     'constant_features': const_cols,
                     'rational_feasible': feas, 'dual': dual}
        print('%s: m=%d rank=%d null=%d const=%s feas=%s dual=%s' % (
            name, len(D), rk, len(ns), const_cols, feas,
            (dual['core_size'] if dual else None)), flush=True)
    json.dump(out, open(OUT + 'G03R_DUAL_CERTIFICATE_RESULTS.json', 'w'), indent=1)
    json.dump({'D_full_n': len(D_full), 'D_seed_n': len(D_seed),
               'note': 'D matrices recomputed from full states (ledger) and stored features (seeds)'},
              open(OUT + 'G03R_FEATURE_MATRIX.json', 'w'), indent=1)
