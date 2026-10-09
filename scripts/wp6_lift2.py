"""Lift2 transfer: vine-ray c_k trajectory + D_L2 symbolic vectors;
rho second-difference dual translates; old-core defect corpus.
Usage: python scripts/wp6_lift2.py [vineray|rhodual|oldcore]
"""
import sys, copy, json
from pathlib import Path
from collections import Counter, defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
tw = load('wp6_twins')
import wp6_cycle_ratio as O
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def rowatoms(B, y):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    ms = Counter()
    for z in dB:
        if z == y:
            continue
        ms[('t', j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])] += 1
    c, _ = R_coeffs(B, y)
    ms[('r', c)] += 1
    return ms

def vine_lift_chain(klist, q=0, tag="K2"):
    """Chain Twin(k,q) for k in klist + Lift2 links; return per-step data."""
    fn = tw.Twin2 if tag == "K2" else tw.Twin1
    out = []
    prev = None
    for k in klist:
        B, T, S, y, z = fn(k, q)
        dB = depths_list(B)
        c, _ = R_coeffs(B, y)
        _, lam = R_coeffs(B, y)
        ftop = lam.get(z, 0)
        out.append({"k": k, "n": len(dB), "dy": dB[y], "c": c, "ftop": ftop,
                    "B": json.dumps(B), "y": y})
    return out

def mode_vineray():
    rep = {}
    for tag in ("K2", "K3"):
        chain = vine_lift_chain([1, 3, 5, 7], q=0, tag=tag)
        print(f"[L2] {tag} vine ray (q=0):", flush=True)
        for e in chain:
            print(f"    k={e['k']} n={e['n']} dy={e['dy']} c={e['c']} ftop={e['ftop']}", flush=True)
        rep[tag] = [{k2: e[k2] for k2 in ("k", "n", "dy", "c", "ftop")} for e in chain]
    json.dump(rep, open(OUT / "j4_lift2ray.json", "w"), indent=1, default=str)
    print("[L2] saved ray", flush=True)

def mode_rhodual():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    import numpy as np
    Z = np.load(OUT / "j4_sh567_A.npz")
    Amat = sp.csr_matrix(Z["A"].astype(float))
    spec = importlib.util.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4b = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4b)
    raw, info = j4b.build_shared([5, 6, 7])
    A2, rhs, metas, vmap = j4b.assemble(raw)
    E, V = Amat.shape
    # UG equalities: 6 gaps + NONE ids + 2 gauge
    from collections import defaultdict as dd
    fams = dd(list)
    for k, i in vmap.items():
        t = k
        if t[0] == 't' and t[1][0] == ('NONE',):
            fams[t[1][3]].append((t[1][2], i))
    er, ec, ev, beq = [], [], [], []
    for dy, lst in sorted(fams.items()):
        base = [i for (dl, i) in lst if dl == -1][0]
        for (dl, i) in lst:
            if dl != -1:
                er += [len(beq), len(beq)]; ec += [i, base]; ev += [1.0, -1.0]
                beq.append(0.0)
    tk = [k for k in vmap if k[0] == 't'][0]; rk = [k for k in vmap if k[0] == 'r'][0]
    er += [len(beq), len(beq) + 1]; ec += [vmap[tk], vmap[rk]]; ev += [1.0, 1.0]
    beq += [0.0, 0.0]
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    for (k, dl, d) in dom["overlap"]:
        key1 = ('t', (('F', k), 1, dl, d)); key2 = ('t', (('F', k), 2, dl, d))
        er += [len(beq), len(beq)]; ec += [vmap[key2], vmap[key1]]; ev += [1.0, -1.0]
        beq.append(1.0)
    beq = np.array(beq); nEQ = len(beq)
    Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
    rkeys = sorted({k[1] for k in vmap if k[0] == 'r'})
    print(f"[L2] root domain: {rkeys}", flush=True)
    out = []
    for c in rkeys:
        a, b, cc = c - 1, c, c + 1
        ka, kb, kc = ('r', a), ('r', b), ('r', cc)
        if ka not in vmap or kb not in vmap or kc not in vmap:
            print(f"[L2] D2rho({c}): triple not co-realized", flush=True)
            out.append({"c": c, "status": "unrealized"})
            continue
        obj = np.zeros(V); obj[vmap[ka]] = 1.0; obj[vmap[kb]] = -2.0; obj[vmap[kc]] = 1.0
        r1 = linprog(obj, A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * V, method="highs")
        r2 = linprog(-obj, A_ub=-Amat, b_ub=-rhs, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * V, method="highs")
        mn = float(r1.fun) if r1.status == 0 else None
        mx = float(-r2.fun) if r2.status == 0 else None
        print(f"[L2] D2rho({c}): [{mn},{mx}]", flush=True)
        out.append({"c": c, "min": mn, "max": mx})
    json.dump(out, open(OUT / "j4_rhodual.json", "w"), indent=1, default=str)
    print("[L2] saved rhodual", flush=True)

def mode_oldcore():
    # Lift2 on non-vine T with old L/R/F claims: C_old grouped by fold state.
    # Build T with richer structure: take n=5 shapes, embed y-rows, lift by 2 above T-root.
    groups = defaultdict(list)
    ntest = 0
    for T in O.shapes_of(list(range(1, 6)))[:60]:
        dT = depths_list(T)
        for y in range(1, 6):
            Py = path_nodes(T, y); d = len(Py) - 1
            if d < 1 or d > 3:
                continue
            sx = 0 if Py[0][1] is Py[1] else 1
            # old non-NONE claims present?
            _, lam = R_coeffs(T, y)
            kinds = set()
            for z in range(1, 6):
                if z == y:
                    continue
                s_ = j4.slot_of(T, y, z)
                if s_[0] in ('L', 'R'):
                    kinds.add((s_[0], lam.get(z, 0)))
            if not kinds:
                continue
            # Lift2 above T-root preserving side: prepend two max keys as left spine top?
            # Use Pad_L twice on whole T (empty sibling): T2 = LL(T); compare old-claim transitions.
            T2 = [0, None, [-1, None, copy.deepcopy(T)]]
            # locate y in T2 (same key)
            _, lam2 = R_coeffs(T2, y)
            dT2 = depths_list(T2)
            trans = []
            for z in range(1, 6):
                if z == y:
                    continue
                s0 = j4.slot_of(T, y, z)
                if s0[0] not in ('L', 'R'):
                    continue
                s1 = j4.slot_of(T2, y, z)
                trans.append((str(s0), lam.get(z, 0), dT[z] - dT[y],
                              str(s1), lam2.get(z, 0), dT2[z] - dT2[y]))
            key = (d % 2, sx)
            groups[key].append({"T": json.dumps(T), "y": y, "trans": [list(t) for t in trans]})
            ntest += 1
    print(f"[L2] old-core corpus: {ntest} rows in {len(groups)} (parity,sx) classes", flush=True)
    summ = {}
    for key, lst in sorted(groups.items(), key=str):
        # distinct transition patterns within class?
        pats = set()
        for e in lst:
            pats.add(json.dumps(e["trans"], sort_keys=True))
        summ[str(key)] = {"n": len(lst), "distinct_patterns": len(pats)}
        print(f"    class parity={key[0]} sx={key[1]}: n={len(lst)} distinct={len(pats)}", flush=True)
        if len(pats) <= 3:
            for e in lst[:2]:
                print(f"      e.g. y={e['y']} {e['trans']}", flush=True)
    json.dump(summ, open(OUT / "j4_oldcore.json", "w"), indent=1, default=str)
    print("[L2] saved oldcore", flush=True)

def main():
    modes = sys.argv[1:] or ["vineray"]
    if "vineray" in modes:
        mode_vineray()
    if "rhodual" in modes:
        mode_rhodual()
    if "oldcore" in modes:
        mode_oldcore()
    return 0

if __name__ == "__main__":
    sys.exit(main())
