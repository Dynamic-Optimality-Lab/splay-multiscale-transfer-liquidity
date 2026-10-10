"""26AL-G closed-cycle enumeration from diagonal + triple filter. Tuple engine."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
from collections import deque
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AL')
LOG = open(RDIR / 'akG_cyc.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush()
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
import wp6_cycle_ratio as O
import splay as S
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def depths(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d
        go(l, d + 1)
        go(r, d + 1)
    go(t, 0)
    return out
def serial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, serial(l), serial(r))
def step(A, B, md, x):
    dA = depths(A).get(x, -1)
    if dA < 0:
        return None
    a = (dA + 1) // 2
    if md == 'K':
        dB = depths(B).get(x, -1)
        if dB < 0:
            return None
        q = dB // 2
    else:
        dB = None; q = 0
    ra, rb = A[1], B[1]
    A2, _ = S.trace(A, x)
    B2 = B if md == 'D' else S.trace(B, x)[0]
    return (A2, B2, {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "ra": ra, "rb": rb})
def vine(n):
    t = S.LEAF
    for k in range(n, 0, -1):
        t = S.node(k, S.LEAF, t)
    return t
def check_triple(legs):
    # legs: full closed cycle accesses; find positive block with G-triple
    m = len(legs)
    leaders = [i for i in range(m) if legs[i]['a'] > 0]
    if not leaders:
        return None
    Lsorted = sorted(leaders)
    bs = []
    for k, s in enumerate(Lsorted):
        e = Lsorted[(k + 1) % len(Lsorted)]
        idx = []
        i = s
        while True:
            idx.append(i)
            if (i + 1) % m == e:
                break
            i = (i + 1) % m
        ks = {legs[i]['x'] for i in idx}
        if len(ks) != 1:
            return None
        nk = sum(1 for i in idx if legs[i]['m'] == 'K' and (legs[i]['dB'] or 0) > 0)
        if nk > 1:
            return None
        bs.append(idx)
    info = []
    for b in bs:
        kb = [i for i in b if legs[i]['m'] == 'K']
        dd = sum(legs[i]['q'] - 2 * legs[i]['a'] for i in b)
        info.append({"key": legs[b[0]]['x'], "delta": dd,
                     "a": sum(legs[i]['a'] for i in b),
                     "q": sum(legs[i]['q'] for i in b),
                     "rb0": legs[kb[0]]['rb'] if kb else None})
    nb = len(bs)
    for k in range(nb):
        if info[k]['delta'] <= 0:
            continue
        xk = info[k]['key']
        rk = info[k]['rb0']
        if rk is None or rk == xk:
            continue
        # need B-root==xk at intervening block's first KEEP: approximate via block start
        n1 = (k + 1) % nb
        # intervening must access y!=xk,rk, opposite side, genuine (has nontrivial KEEP)
        yk = info[n1]['key']
        if yk == xk or yk == rk:
            continue
        if (rk - xk) * (yk - xk) <= 0:
            continue
        kb1 = [i for i in bs[n1] if legs[i]['m'] == 'K' and (legs[i]['dB'] or 0) > 0]
        if not kb1:
            continue
        n2 = (k + 2) % nb
        if legs[bs[n2][0]]['x'] != rk:
            continue
        if info[n1]['delta'] > 0:
            continue
        # capacity with c=2 worst
        cap = (2 * info[n1]['a'] - info[n1]['q']) + (2 * sum(legs[i]['a'] for i in bs[n2]) - 2)
        if info[k]['delta'] > cap:
            continue
        return {"k": k, "x": xk, "r": rk, "y": yk,
                "deltas": [info[k]['delta'], info[n1]['delta'],
                           sum(legs[i]['q'] - 2 * legs[i]['a'] for i in bs[n2])]}
    return None
CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]
found = None
import random
rng = random.Random(7)
found = []
for n in (7, 8):
    T0s = [vine(n)] + [to_tup(copy.deepcopy(s)) for s in shapes(n)[:3]]
    for ti, T0 in enumerate(T0s):
        S0 = (serial(T0), serial(T0))
        prev = {S0: None}; act = {S0: None}
        states = {S0: (T0, T0)}
        plen = {S0: 0}
        dq = deque([S0]); exp = 0
        while dq and exp < 15000:
            s = dq.popleft()
            Ac, Bc = states[s]
            order = list(range(1, n + 1))
            rng.shuffle(order)
            for md in ('K', 'D'):
                for z in order:
                    rr = step(Ac, Bc, md, z)
                    if rr is None:
                        continue
                    A2, B2, lg = rr
                    ns = (serial(A2), serial(B2))
                    if ns not in states:
                        states[ns] = (A2, B2)
                        prev[ns] = s; act[ns] = (md, z)
                        plen[ns] = plen[s] + 1
                        dq.append(ns); exp += 1
                        if ns == S0 and plen[ns] >= 4:
                            w = []
                            t = ns
                            while prev[t] is not None:
                                w.append(act[t]); t = prev[t]
                            w = list(reversed(w))
                            found.append((n, ti, w))
                    if exp >= 15000:
                        break
                if exp >= 15000:
                    break
        log(f"[AKGC] T0 done exp={exp} closedFound={len(found)}")
log(f"[AKGC] closed walks total: {len(found)}")
best = None
for (n, ti, word) in found:
    T0s = [vine(n)] + [to_tup(copy.deepcopy(s)) for s in shapes(n)[:3]]
    T0 = T0s[ti]
    A, B = T0, T0
    legs = []
    for (md, x) in word:
        r = step(A, B, md, x)
        A, B = r[0], r[1]
        legs.append(r[2])
    tr = check_triple(legs)
    if tr is not None:
        best = (n, ti, word, tr)
        break
log(f"[AKGC] triple-match: {best is not None}")
if best is not None:
    n, ti, word, tr = best
    log(f"[AKGC] {json.dumps({'n': n, 'ti': ti, 'word': word, 'triple': tr}, default=str)[:500]}")
    json.dump({"n": n, "ti": ti, "word": word, "triple": tr}, open(RDIR / "26AL_Gwitness.json", "w"), indent=1, default=str)
log("[AKGC] done")
LOG.close()
