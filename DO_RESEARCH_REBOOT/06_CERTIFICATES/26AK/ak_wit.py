"""26AK witness hunt: bounded random closed-walk sampling with triple filter."""
import sys, copy, json, random
sys.path.insert(0, 'scripts')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AK')
LOG = open(RDIR / 'ak_wit.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush()
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
ev = load('wp6_eventflow')
adv = load('wp6_adv')
import wp6_cycle_ratio as O
def serial(t):
    if t is None:
        return '.'
    return (t['k'], serial(t.get('l')), serial(t.get('r')))
def run_word(T0, word):
    A = ev.to_ptr(copy.deepcopy(T0))
    B = ev.to_ptr(copy.deepcopy(T0))
    legs = []
    for (md, x) in word:
        dA = adv.depths_of(copy.deepcopy(A)).get(x, -1)
        if dA is None or dA < 0:
            return None
        a = (dA + 1) // 2
        if md == 'K':
            dB = adv.depths_of(copy.deepcopy(B)).get(x, -1)
            if dB is None or dB < 0:
                return None
            q, z = dB // 2, dB % 2
        else:
            dB = None; q = z = 0
        ra = ev.root_key(A)
        rb = ev.root_key(B)
        A, _ = ev.splay_A(A, x)
        if md == 'K':
            B, _ = ev.splay_B_push(B, x)
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "ra": ra, "rb": rb})
    return legs, serial(A), serial(B)
def analyze(legs):
    m = len(legs)
    leaders = [i for i in range(m) if legs[i]['a'] > 0]
    if not leaders:
        return None
    # blocks
    L = sorted(leaders)
    bs = []
    for k, s in enumerate(L):
        e = L[(k + 1) % len(L)]
        idx = []
        i = s
        while True:
            idx.append(i)
            if (i + 1) % m == e:
                break
            i = (i + 1) % m
        bs.append(idx)
    info = []
    for b in bs:
        ks = {legs[i]['x'] for i in b}
        if len(ks) != 1:
            return None
        nk = [(i, legs[i]['dB']) for i in b if legs[i]['m'] == 'K' and (legs[i]['dB'] or 0) > 0]
        dd = sum(legs[i]['q'] - 2 * legs[i]['a'] for i in b)
        info.append({"key": list(ks)[0], "ntriv": nk, "delta": dd, "a": sum(legs[i]['a'] for i in b),
                     "q": sum(legs[i]['q'] for i in b)})
    return info
rng = random.Random(11)
tried = closed = 0
found = None
CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]
# need B-state per block: re-run winners fully; filter first on legs + roots captured above
for trial in range(15000):
    n = rng.choice([7, 8])
    Sh = shapes(n)
    T0 = copy.deepcopy(Sh[rng.randrange(len(Sh))])
    L = rng.randint(5, 11)
    word = []
    for _ in range(L):
        md = 'K' if rng.random() < 0.7 else 'D'
        word.append((md, rng.randint(1, n)))
    r = run_word(T0, word)
    if r is None:
        continue
    tried += 1
    legs, sA, sB = r
    # closed? need start serials
    A0 = ev.to_ptr(copy.deepcopy(T0)); B0 = ev.to_ptr(copy.deepcopy(T0))
    import pickle
    # serial compare via fresh builds
    def srl(t):
        return serial(t)
    if sA != srl(A0) or sB != srl(B0):
        continue
    closed += 1
    info = analyze(legs)
    if info is None:
        continue
    m = len(info)
    # triple filter: positive i, genuine intervening (ntriv>=1, key!=x,r?), delayed r
    # need r_i = B-root before block i first KEEP: approximate via legs rb at block start
    # (rb recorded pre-access). Reconstruct per-block B-root-before-first-KEEP:
    # use legs ra/rb fields: rb at first KEEP index of block.
    starts = []
    Lsorted = sorted([i for i in range(m) if legs[i]['a'] > 0])
    for k, s in enumerate(Lsorted):
        e = Lsorted[(k + 1) % len(Lsorted)]
        idx = []
        i = s
        while True:
            idx.append(i)
            if (i + 1) % m == e:
                break
            i = (i + 1) % m
        starts.append(idx)
    for k in range(len(starts)):
        b = starts[k]
        if info[k]['delta'] <= 0:
            continue
        # positive block: key x, former root = rb at first KEEP of block
        kb = [i for i in b if legs[i]['m'] == 'K']
        if not kb:
            continue
        rkey = legs[kb[0]]['rb']
        xkey = info[k]['key']
        if rkey == xkey:
            continue
        # successor block must NOT access r (genuine delay) and must B-change
        nb = starts[(k + 1) % len(starts)]
        if legs[nb[0]]['x'] == rkey:
            continue
        if not [i for i in nb if legs[i]['m'] == 'K' and (legs[i]['dB'] or 0) > 0]:
            continue
        # next-next block accesses r?
        nn = starts[(k + 2) % len(starts)]
        if legs[nn[0]]['x'] != rkey:
            continue
        # opposite-branch (key order) + nonpositive intervening
        ykey = legs[nb[0]]['x']
        if (rkey - xkey) * (ykey - xkey) >= 0:
            continue
        if info[(k + 1) % len(starts)]['delta'] > 0:
            continue
        found = {"trial": trial, "n": n, "word": word, "block": k,
                 "x": xkey, "r": rkey, "y": ykey, "delta": info[k]['delta']}
        break
    if found:
        break
    if trial % 3000 == 0:
        log(f"[AKW] trial={trial} closed={closed}")
log(f"[AKW] tried={tried} closed={closed} found={found is not None}")
if found:
    log(f"[AKW] WITNESS: {found}")
    json.dump(found, open(RDIR / "26AK_witness.json", "w"), indent=1, default=str)
log("[AKW] done")
LOG.close()
