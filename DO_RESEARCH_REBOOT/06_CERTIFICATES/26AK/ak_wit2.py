"""26AK witness hunt v2: tuple engine, divergence-biased sampling, triple filter."""
import sys, copy, json, random
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AK')
LOG = open(RDIR / 'ak_wit2.log', 'w')
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
def root(t):
    return t[1]
def run_word(A0, B0, word):
    A, B = A0, B0
    legs = []
    for (md, x) in word:
        dA = depths(A).get(x, -1)
        if dA < 0:
            return None
        a = (dA + 1) // 2
        if md == 'K':
            dB = depths(B).get(x, -1)
            if dB < 0:
                return None
            q, z = dB // 2, dB % 2
        else:
            dB = None; q = z = 0
        ra, rb = root(A), root(B)
        A, _ = S.trace(A, x)
        if md == 'K':
            B, _ = S.trace(B, x)
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "ra": ra, "rb": rb, "sA": A, "sB": B})
    return legs
def serial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, serial(l), serial(r))
rng = random.Random(2026)
tried = closed = 0
found = None
CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]
for trial in range(120000):
    n = rng.choice([7, 8])
    mode = rng.random()
    if mode < 0.5:
        T0 = to_tup([k, None, None] for k in []) if False else None
        t = S.LEAF
        for k in range(n, 0, -1):
            t = S.node(k, S.LEAF, t)
        T0 = t
    else:
        Sh = shapes(n)
        T0 = to_tup(copy.deepcopy(Sh[rng.randrange(len(Sh))]))
    # divergence-biased prefix: 1-3 DELETEs (freeze B, move A-root around)
    pre = []
    for _ in range(rng.randint(1, 3)):
        pre.append(('D', rng.randint(1, n)))
    L = rng.randint(5, 10)
    body = []
    for _ in range(L):
        md = 'K' if rng.random() < 0.75 else 'D'
        body.append((md, rng.randint(1, n)))
    r = run_word(T0, T0, pre + body)
    if r is None:
        continue
    tried += 1
    # closed w.r.t. post-prefix state: recompute prefix end states
    rp = run_word(T0, T0, pre)
    sA0, sB0 = serial(rp[-1]['sA']), serial(rp[-1]['sB'])
    if serial(r[-1]['sA']) != sA0 or serial(r[-1]['sB']) != sB0:
        # check cycle over body only: legs[Lpre:]
    # NOTE closed means body returns to post-prefix state
        pass
    legs = r[len(pre):]
    if serial(legs[-1]['sA']) != sA0 or serial(legs[-1]['sB']) != sB0:
        if trial % 20000 == 0:
            log(f"[AKW2] trial={trial}")
        continue
    closed += 1
    m = len(legs)
    leaders = [i for i in range(m) if legs[i]['a'] > 0]
    if not leaders:
        continue
    Lsorted = sorted(leaders)
    bs = []
    okstruct = True
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
            okstruct = False; break
        nk = sum(1 for i in idx if legs[i]['m'] == 'K' and (legs[i]['dB'] or 0) > 0)
        if nk > 1:
            okstruct = False; break
        bs.append(idx)
    if not okstruct:
        continue
    info = []
    for b in bs:
        dd = sum(legs[i]['q'] - 2 * legs[i]['a'] for i in b)
        info.append({"key": legs[b[0]]['x'], "delta": dd,
                     "a": sum(legs[i]['a'] for i in b), "q": sum(legs[i]['q'] for i in b),
                     "broot": legs[b[0]]['rb']})
    nb = len(bs)
    for k in range(nb):
        if info[k]['delta'] <= 0:
            continue
        # former root r = B-root before block k first KEEP: rb at first KEEP index
        kb = [i for i in bs[k] if legs[i]['m'] == 'K']
        if not kb:
            continue
        rk = legs[kb[0]]['rb']
        xk = info[k]['key']
        if rk == xk:
            continue
        n1 = (k + 1) % nb
        if legs[bs[n1][0]]['x'] == rk:
            continue  # immediate repayment: 26AJ case, skip
        # intervening must B-change genuinely
        if not [i for i in bs[n1] if legs[i]['m'] == 'K' and (legs[i]['dB'] or 0) > 0]:
            continue
        yk = info[n1]['key']
        if yk == xk or yk == rk:
            continue
        if (rk - xk) * (yk - xk) >= 0:
            continue
        n2 = (k + 2) % nb
        if legs[bs[n2][0]]['x'] != rk:
            continue
        if info[n1]['delta'] > 0:
            continue
        found = {"trial": trial, "n": n, "pre": pre,
                 "word": body, "k": k, "x": xk, "r": rk, "y": yk,
                 "delta": info[k]['delta']}
        break
    if found:
        break
log(f"[AKW2] tried={tried} closed={closed} found={found is not None}")
if found:
    log(f"[AKW2] CANDIDATE: {found}")
    json.dump(found, open(RDIR / "26AK_candidate.json", "w"), indent=1, default=str)
log("[AKW2] done")
LOG.close()
