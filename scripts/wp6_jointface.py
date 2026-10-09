"""PIVOT-25R-X §2+§6: zero-margin face diagnosis + gauge freedom.

Loads frozen rows; solves diverse LPs (max-t, minmax, random objectives);
collects persistent-near-tight rows; exact pairwise proportionality scan;
all-ones gauge proof + fix; reports rank/nullity estimates.
"""
from __future__ import annotations
import sys
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))

LOGP = Path("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/jointface.log")


def step(sid, msg):
    line = "[JFC %s] %s" % (sid, msg)
    print(line, flush=True)
    try:
        with open(LOGP, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_frozen():
    F = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                    "0909c74a" / "dual_mine" /
                    "joint_frozen7.json").read_text())
    return F["rows"]


def build_matrix(rows):
    # SPARSE: dense 41Kx3K is ~1GB and thrashes; keep csr throughout.
    import numpy as np
    from scipy.sparse import csr_matrix
    var = {}
    rd, cd, vd = [], [], []
    bv = []
    for i, r in enumerate(rows):
        for e, c in r["M"].items():
            if e not in var:
                var[e] = len(var)
            rd.append(i)
            cd.append(var[e])
            vd.append(float(c))
        bv.append(float(r["b"]))
    E, Vv = len(rows), len(var)
    M = csr_matrix((np.array(vd), (np.array(rd), np.array(cd))),
                   shape=(E, Vv))
    return M, np.array(bv), var


def solve_obj(M, bv, cobj):
    import numpy as np
    from scipy.optimize import linprog
    E, Vv = M.shape
    c = np.asarray(cobj, dtype=float)
    res = linprog(c, A_ub=-M, b_ub=-bv,
                  bounds=[(None, None)] * Vv, method="highs")
    return res


def maxslack(M, bv):
    """max t s.t. Mg - t >= b (sparse); records t*."""
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import hstack
    E, Vv = M.shape
    A1 = hstack([-M, np.ones((E, 1))]).tocsr()
    bub = -bv
    c = np.zeros(Vv + 1)
    c[-1] = -1.0
    res = linprog(c, A_ub=A1, b_ub=bub,
                  bounds=[(None, None)] * Vv + [(None, 1e6)],
                  method="highs")
    return res


def main():
    import numpy as np
    rows = load_frozen()
    M, bv, var = build_matrix(rows)
    E, Vv = M.shape
    step("M", "frozen rows=%d vars=%d brange=[%g,%g]" %
         (E, Vv, bv.min(), bv.max()))
    # gauge check: all-ones in null(M) exactly (each row sums C_pre-C_post
    # over n keys both sides => 0). Verify on integers via row sums.
    ones = np.ones(Vv)
    r = M @ ones
    step("G", "all-ones null check: max|M*1|=%g (exact 0 expected)" %
         np.abs(r).max())
    # diverse objectives
    rng = random.Random(7)
    sols = []
    res = maxslack(M, bv)
    step("O", "max-t: status=%s t*=%.3g" % (res.status, -res.fun
                                            if res.status == 0 else -1))
    if res.status == 0:
        sols.append(("maxt", res.x[:-1]))
    for k in range(4):
        cobj = np.array([rng.uniform(-1, 1) for _ in range(Vv)])
        res = solve_obj(M, bv, cobj)
        step("O", "rand%d: status=%s" % (k, res.status))
        if res.status == 0:
            sols.append(("rand%d" % k, res.x))
    # persistent-near-tight: slack < 1e-7 in EVERY solution
    tight_counts = np.zeros(E, dtype=int)
    for _, g in sols:
        sl = M @ g - bv
        tight_counts += (sl < 1e-7)
    pers = np.where(tight_counts == len(sols))[0]
    step("P", "solutions=%d persistent-tight rows=%d/%d" %
         (len(sols), len(pers), E))
    # exact pairwise proportionality among persistent (integer cross-mult)
    keys = {}
    pairs = 0
    prow = {}
    for i in pers:
        ri = M[i]
        nz = sorted(zip(ri.indices.tolist(), ri.data.tolist()))
        prow[i] = (nz, bv[i])
    sig2idx = {}
    for i, (nz, b) in prow.items():
        # canonical: scale by sign of first nonzero, reduce by content gcd
        import math as _m
        g = 0
        for _, c in nz:
            g = _m.gcd(g, int(round(c)))
        g = _m.gcd(g, int(round(b))) if b == round(b) else g
        if g == 0:
            g = 1
        first = nz[0][1]
        s = -1 if first < 0 else 1
        sig = (tuple((e, s * int(round(c)) // g) for e, c in nz),
               s * b / g)
        if sig in sig2idx:
            pairs += 1
        else:
            sig2idx[sig] = i
    step("P", "persistent classes up to scale: %d (exact dup-pairs=%d)" %
         (len(sig2idx), pairs))
    # negations: (nz,b) vs (-nz,-b) present?
    S = set()
    for i, (nz, b) in prow.items():
        S.add((tuple(nz), b))
    negs = sum(1 for (nz, b) in S
               if (tuple((e, -c) for e, c in nz), -b) in S)
    step("P", "exact negation pairs in persistent set: %d" % (negs // 2))
    # float rank of persistent block (scope for exact RREF); dense only
    # if small, else skipped with note (no OOM thrash).
    if len(pers) > 0:
        Mp = M[pers]
        if Mp.shape[0] * Mp.shape[1] <= 9000000:
            rk = np.linalg.matrix_rank(Mp.toarray())
            step("P", "persistent block: %dx%d float-rank=%d nullity~%d" %
                 (len(pers), Vv, rk, Vv - rk))
        else:
            step("P", "persistent block %dx%d too big for dense rank "
                      "(skipped)" % (len(pers), Vv))
    out = {"rows": E, "vars": Vv, "nsol": len(sols),
           "persistent": int(len(pers)),
           "prop_classes": len(sig2idx), "neg_pairs": negs // 2,
           "gauge_max": float(np.abs(r).max())}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "joint_face.json").write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    step("S", "saved joint_face.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
