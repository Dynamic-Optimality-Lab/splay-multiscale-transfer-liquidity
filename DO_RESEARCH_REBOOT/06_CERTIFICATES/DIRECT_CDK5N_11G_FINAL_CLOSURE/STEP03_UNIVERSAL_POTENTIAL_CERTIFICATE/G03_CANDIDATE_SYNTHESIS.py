# G03_CANDIDATE_SYNTHESIS.py — affine template fitting + universal edge-violation
# checks (CEGIS core). Template: Phi(s) = c + sum theta_i f_i(s), theta in [-B,B].
# Synthesis over grounded seeds (exact Z3 Int). Verification per (family,weight):
# EXISTS s,t,witness (E_w AND Phi(t)-Phi(s) > w); SAT=counterexample (refine or
# refute), UNSAT=certified family, UNKNOWN=recorded with reason.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import z3

FEATS = ['b_root', 'b_depth_sum', 'b_depth_max', 'b_marked_depth_sum', 'a_root_sidx',
         'a_nslots', 'a_marked_count', 'sig_sum', 'sig_nonempty', 'core_size']

RANK_FEATS = FEATS + ['b_rank_sum', 'b_rank_marked', 'b_rank_root', 'a_rank_sum', 'a_rank_root']


def fit_affine_on(seeds, feats, bound=None):
    th = {f: z3.Int('thq_' + f) for f in feats}
    s = z3.Solver()
    s.set('random_seed', 7)
    if bound is not None:
        for f in feats:
            s.add(th[f] >= -bound, th[f] <= bound)
    for e in seeds:
        try:
            lhs = sum(th[f] * (e['t'][f] - e['s'][f]) for f in feats)
        except (KeyError, TypeError):
            return None, 'badfeat'
        s.add(lhs <= e['w'])
    r = s.check()
    if r != z3.sat:
        return None, str(r)
    m = s.model()
    return ({f: m.eval(th[f], model_completion=True).as_long() for f in feats}, 0), 'sat'


def fit_affine(seeds, bound=5):
    th = {f: z3.Int('th_' + f) for f in FEATS}
    c = z3.Int('c0')
    s = z3.Solver()
    s.set('random_seed', 7)
    for f in FEATS:
        if bound is not None:
            s.add(th[f] >= -bound, th[f] <= bound)
    s.add(c >= -200, c <= 200)
    for e in seeds:
        lhs = sum(th[f] * (e['t'][f] - e['s'][f]) for f in FEATS)
        s.add(lhs <= e['w'])
    r = s.check()
    if r != z3.sat:
        return None, str(r)
    m = s.model()
    return ({f: m.eval(th[f], model_completion=True).as_long() for f in FEATS},
            m.eval(c, model_completion=True).as_long()), 'sat'


NUM = ['b_root', 'b_depth_sum', 'b_depth_max', 'b_marked_depth_sum', 'a_root_sidx',
       'a_nslots', 'a_marked_count', 'sig_sum', 'sig_nonempty', 'core_size']


def expand_poly(fe):
    """Degree<=2 monomials over numeric base features (keys 'p:i,j' i<=j)."""
    base = {a: fe.get(a, 0) for a in NUM}
    if any(v is None for v in base.values()):
        return None
    out = dict(base)
    for i, a in enumerate(NUM):
        va = base[a]
        out['p:%d,%d' % (i, i)] = va * va
        for j in range(i + 1, len(NUM)):
            out['p:%d,%d' % (i, j)] = va * base[NUM[j]]
    return out


def fit_poly(seeds, bound=None):
    """LP fit over degree<=2 monomials (linear in coefficients)."""
    ext = []
    for sd in seeds:
        a = expand_poly(sd['s'])
        b = expand_poly(sd['t'])
        if a is None or b is None:
            return None, 'badfeat'
        ext.append((a, b, sd['w']))
    keys = sorted(ext[0][0].keys())
    s = z3.Solver()
    s.set('random_seed', 7)
    th = {k: z3.Int('thp_' + k.replace(',', '_').replace(':', 'P')) for k in keys}
    for (a, b, w) in ext:
        s.add(z3.Sum([th[k] * (b[k] - a[k]) for k in keys]) <= w)
    if bound is not None:
        for k in keys:
            s.add(th[k] >= -bound, th[k] <= bound)
    r = s.check()
    if r != z3.sat:
        return None, str(r)
    m = s.model()
    return ({k: m.eval(th[k], model_completion=True).as_long() for k in keys}, 0), 'sat'


if __name__ == '__main__':
    seeds = json.load(open(PDIR + 'G03_CEGIS_SEEDS.json'))
    # exclude constant features (mu_bits always 5)
    got, why = fit_affine(seeds)
    check('affine template fits seeds', got is not None, str(got)[:200] if got else why)
    if got:
        th, c = got
        nz = {f: v for f, v in th.items() if v != 0}
        print('theta:', nz, 'c:', c, flush=True)
        J('G03_CANDIDATE_POTENTIAL.json', {'family': 'affine', 'theta': th, 'c': c, 'n_seeds': len(seeds)})
    else:
        J('G03_CANDIDATE_POTENTIAL.json', {'family': 'affine', 'status': 'UNSAT-or-UNKNOWN', 'reason': why})
    print('FAIL:', FAIL, flush=True)
