# G03R_PIECEWISE_POTENTIAL.py — GATE G (bounded): depth-guarded 2-piece potential.
# Guard g(s) = [b_depth_max(s) >= 6] is a pure vertex function (no H, no witness).
# Phi(s) = Phi_shallow(s) if not g(s) else Phi_deep(s); single-valued (G2).
# Pieces fit by exact LP on partitioned Step-03 seeds; combined function
# falsified on fresh grounded edges. Universal Z3: recorded OPEN (budget).
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
from G03_CANDIDATE_SYNTHESIS import fit_affine_on, RANK_FEATS


def guard(fe):
    return fe['b_depth_max'] >= 6


def joint_fit(seeds):
    """Joint LP: one affine per guard value; edge (s,t) uses piece g(s) at s,
    piece g(t) at t. Phi(s)=theta[g(s)].f(s) is single-valued (G2)."""
    import z3
    th = {(g, f): z3.Int('th%d_%s' % (g, f)) for g in (0, 1) for f in RANK_FEATS}
    s = z3.Solver()
    s.set('random_seed', 7)
    for e in seeds:
        gs = 1 if guard(e['s']) else 0
        gt = 1 if guard(e['t']) else 0
        lhs = sum(th[(gt, f)] * e['t'][f] - th[(gs, f)] * e['s'][f] for f in RANK_FEATS)
        s.add(lhs <= e['w'])
    r = s.check()
    if r != z3.sat:
        return None
    m = s.model()
    return {g: {f: m.eval(th[(g, f)], model_completion=True).as_long() for f in RANK_FEATS} for g in (0, 1)}


if __name__ == '__main__':
    import sys as _s
    if len(_s.argv) > 1 and _s.argv[1] == 'falsify':
        import time, random
        import splay as S
        from PC_TYPED_DAG import DAG
        from STRICT_LOW_COMPILER import build_slow
        from STRICT_CERTIFY import ssertify
        from PC_CONCRETIZE import serial
        from CRA_pointer_tuple_replay import replay
        sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT'))
        from G03_POTENTIAL_FEATURES import eval_all
        n = int(_s.argv[2]) if len(_s.argv) > 2 else 40
        seed = int(_s.argv[3]) if len(_s.argv) > 3 else 31
        cand = json.load(open(OUT + 'G03R_POTENTIAL_CANDIDATE_RESULTS.json'))
        J = {int(g): th for g, th in cand['joint_single_valued'].items()}

        def phi(fe):
            g = 1 if guard(fe) else 0
            return sum(v * fe.get(f, 0) for f, v in J[g].items())

        def phi_edge(fs, ft):
            return phi(ft) - phi(fs)

        rng = random.Random(seed)
        d = DAG()
        L = build_slow(d, 'SL')
        t0 = time.process_time()
        tried = ok = 0
        viol = []
        while tried < n and time.process_time() - t0 < 1400:
            keys = list(range(1, 10))
            ks = list(keys)
            rng.shuffle(ks)
            t = S.LEAF

            def ins(nn, k):
                if nn[0] == 'leaf':
                    return S.node(k, S.LEAF, S.LEAF)
                _, kk, l, rr = nn
                return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

            for k in ks:
                t = ins(t, k)
            A = t
            ks2 = list(keys)
            rng.shuffle(ks2)
            B = S.LEAF
            for k in ks2:
                B = ins(B, k)
            M = set(rng.sample(keys, 5))
            x = rng.choice(sorted(M))
            try:
                R = replay([('K', x)], serial(A), serial(B))
            except Exception:
                continue
            if not R['agree']:
                continue
            H = sum(l['a'] for l in R['legs'])
            try:
                st, info = ssertify(d, L, serial(A), serial(B), set(keys), M, [('K', x)], H)
            except Exception:
                continue
            if st != 'ok':
                continue
            env = dict(info['env'])
            fs = eval_all({k: v for k, v in env.items() if k.startswith('SLs_')}, 'SLs')
            ft = eval_all({k: v for k, v in env.items() if k.startswith('SLt_')}, 'SLt')
            if any(v is None for v in list(fs.values()) + list(ft.values())):
                continue
            tried += 1
            lhs = phi_edge(fs, ft)
            w = int(info['w'])
            if lhs is not None and lhs <= w:
                ok += 1
            else:
                viol.append({'w': w, 'lhs': lhs,
                             'gs': guard(fs), 'gt': guard(ft)})
        json.dump({'tried': tried, 'ok': ok, 'nviol': len(viol), 'violations': viol[:15],
                   'cpu_s': time.process_time() - t0},
                  open(OUT + 'G03R_PIECEWISE_FALSIFY.json', 'w'), indent=1)
        print('piecewise falsify: tried=%d ok=%d viol=%d cpu=%.1f' % (
            tried, ok, len(viol), time.process_time() - t0), flush=True)
        raise SystemExit
    seeds = json.load(open(PDIR + 'G03_CEGIS_SEEDS.json'))
    # JOINT single-valued fit (G2): Phi(s) = theta[g(s)] . f(s)
    J = joint_fit(seeds)
    print('joint fit:', 'SAT' if J else 'UNSAT', flush=True)
    if J:
        for g in (0, 1):
            print(' piece%d:' % g, {f: v for f, v in J[g].items() if v != 0}, flush=True)
    # partition by ENDPOINT-guard pair: edge belongs to piece (gs, gt)
    parts = {}
    for s in seeds:
        key = (guard(s['s']), guard(s['t']))
        parts.setdefault(key, []).append(s)
    print('partition sizes:', {k: len(v) for k, v in parts.items()}, flush=True)
    pieces = {}
    for key, ss in parts.items():
        got, why = fit_affine_on(ss, RANK_FEATS, bound=None)
        pieces[str(key)] = ({k: v for k, v in got[0].items() if v != 0} if got else None)
        print(key, '->', 'SAT' if got else ('UNSAT:' + str(why)), flush=True)
    json.dump({'guard': 'b_depth_max>=6 (vertex function; G2 single-valued by case split on s)',
               'partition_sizes': {str(k): len(v) for k, v in parts.items()},
               'pieces': pieces,
               'joint_single_valued': ({str(g): {f: v for f, v in J[g].items() if v != 0} for g in (0, 1)} if J else None),
               'note': 'piece (gs,gt) constrains edges crossing guard regions; JOINT fit gives the telescoping potential Phi(s)=theta[g(s)].f(s)'},
              open(OUT + 'G03R_POTENTIAL_CANDIDATE_RESULTS.json', 'w'), indent=1)
