"""GATE 0 Rule 4: hunt a five-key core-<=8 closed walk outside all prior domains.

Seeds from the Gate-0 four-key witness (vine-7, prefix D7,D6, S0 fixed).
Mutations: substitute <=1 head key; insert <=2 KEEPs (5th key K2 or K4...).
Filters: exact closure, 5 KEEP keys all genuinely used, core<=8 throughout,
novelty screen (single positive + non-return successors), recognizer sweep.
"""
import sys, copy, json, itertools, importlib.util
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW')
from wp6_eventflow import to_ptr, splay_A, splay_B_push

def pdepths(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d
        go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def pserial(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t["k"]
def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
def core_of_serial(serial, M):
    core = set()
    def path_to(nd, x, path):
        if nd == '.':
            return None
        k, l, r = nd
        path = path + [k]
        if k == x:
            return path
        return path_to(l, x, path) or path_to(r, x, path)
    for m in M:
        core.update(path_to(serial, m, []))
    return core

T0 = vine_right(7)
PREFIX = [('D', 7), ('D', 6)]
BASE = [('K', 7), ('D', 2), ('D', 4), ('D', 6), ('K', 1), ('K', 3), ('K', 5),
        ('K', 3), ('K', 1), ('D', 2), ('D', 4), ('D', 7), ('D', 6)]
A0 = to_ptr(copy.deepcopy(T0)); B0 = to_ptr(copy.deepcopy(T0))
def step(A, B, md, x):
    dA = pdepths(A).get(x, -1)
    if dA < 0:
        return None
    a = (dA + 1) // 2
    if md == 'K':
        dB = pdepths(B).get(x, -1)
        if dB < 0:
            return None
        q = dB // 2
    else:
        dB = None; q = 0
    ra, rb = proot(A), proot(B)
    sb = pserial(B)
    A, _ = splay_A(A, x)
    chg = False
    if md == 'K':
        B, _ = splay_B_push(B, x)
        chg = (pserial(B) != sb)
    return A, B, {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                  "delta": q - 2 * a, "ra": ra, "rb": rb, "chg": chg}
S = to_ptr(copy.deepcopy(T0)); Bb = to_ptr(copy.deepcopy(T0))
for (md, x) in PREFIX:
    S, Bb, _ = step(S, Bb, md, x)
SA0, SB0 = pserial(S), pserial(Bb)

def replay(word):
    A = copy.deepcopy(SA0); B = copy.deepcopy(SB0)
    # rebuild live trees from serials? easier: replay prefix fresh each time
    A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
    for (md, x) in PREFIX:
        A, B, _ = step(A, B, md, x)
    legs = []
    for (md, x) in word:
        r = step(A, B, md, x)
        if r is None:
            return None
        A, B, lg = r
        legs.append(lg)
    if (pserial(A), pserial(B)) != (SA0, SB0):
        return None
    return legs

def trial(word):
    legs = replay(word)
    if legs is None:
        return None
    K = sorted({l["x"] for l in legs if l["m"] == "K"})
    if len(K) != 5:
        return None
    # genuine participation: each KEEP key changes B at least once
    for k in K:
        if not any(l["m"] == "K" and l["x"] == k and l["chg"] for l in legs):
            return None
    # core <= 8 throughout (need B serials per step -> recompute)
    A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
    for (md, x) in PREFIX:
        A, B, _ = step(A, B, md, x)
    mx = 0
    for (md, x) in word:
        A, B, lg = step(A, B, md, x)
        mx = max(mx, len(core_of_serial(pserial(B), set(K))))
    if mx > 8:
        return None
    pos = [l for l in legs if l["delta"] > 0]
    return {"word": word, "legs": legs, "K": K, "maxcore": mx,
            "pos": [(l["x"], l["a"], l["q"], l["delta"], l["rb"]) for l in pos],
            "A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs)}

cands = []
# insertions of K2/K4 (5th key) at all slots, 1-2 insertions
FIFTH = [2, 4]
def gen():
    yield ("base", list(BASE))
    for i in range(len(BASE) + 1):
        for k in FIFTH:
            w = list(BASE); w.insert(i, ('K', k))
            yield ("ins1-%d-K%d" % (i, k), w)
    for i in range(len(BASE) + 1):
        for j in range(i, len(BASE) + 1):
            for k1 in FIFTH:
                for k2 in FIFTH:
                    w = list(BASE)
                    w.insert(i, ('K', k1))
                    w.insert(j + 1, ('K', k2))
                    yield ("ins2-%d-%d-K%dK%d" % (i, j, k1, k2), w)
    for i in range(6):
        for k in range(1, 8):
            if k == BASE[i][1]:
                continue
            w = list(BASE); w[i] = ('K', k)
            yield ("sub-%d-K%d" % (i, k), w)

tested = 0
for tag, w in gen():
    tested += 1
    r = trial(w)
    if r is not None:
        r["tag"] = tag
        cands.append(r)
        print("CANDIDATE:", tag, "K=", r["K"], "core<=", r["maxcore"],
              "pos=", r["pos"], "A=", r["A"], "Q=", r["Q"], flush=True)
print("tested=%d candidates=%d" % (tested, len(cands)), flush=True)
json.dump([{"tag": c["tag"], "word": c["word"], "K": c["K"],
            "maxcore": c["maxcore"], "pos": c["pos"], "A": c["A"], "Q": c["Q"]}
           for c in cands],
          open(RDIR / 'DIRECT_CDK5_LOW_witness_hunt.json', 'w'), indent=1)
