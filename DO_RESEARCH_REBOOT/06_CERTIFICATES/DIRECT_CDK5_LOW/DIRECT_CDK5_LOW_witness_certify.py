"""GATE 0 Rule 4: certify the five-key witness ins1-1-K2 (both engines + recognizers)."""
import sys, copy, json, importlib.util
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW')
import splay as S
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
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def idepths(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def iserial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, iserial(l), iserial(r))
def core_of(serial, M):
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
def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t

T0 = vine_right(7)
PREFIX = [('D', 7), ('D', 6)]
WORD = [('K', 7), ('K', 2), ('D', 2), ('D', 4), ('D', 6), ('K', 1), ('K', 3),
        ('K', 5), ('K', 3), ('K', 1), ('D', 2), ('D', 4), ('D', 7), ('D', 6)]
K = {1, 2, 3, 5, 7}
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
for (md, x) in PREFIX:
    dA = pdepths(A)[x]; A, _ = splay_A(A, x)
    IA, _ = S.trace(IA, x)
S0 = (pserial(A), pserial(B))
legs, agree, mx = [], True, 0
for (md, x) in WORD:
    dA = pdepths(A).get(x, -1); a = (dA + 1) // 2
    dB = pdepths(B).get(x, -1) if md == 'K' else None
    q = dB // 2 if md == 'K' else 0
    rb = proot(B)
    sb = pserial(B)
    eA = idepths(IA).get(x); eB = idepths(IB).get(x) if md == 'K' else None
    A, _ = splay_A(A, x)
    chg = False
    if md == 'K':
        B, _ = splay_B_push(B, x)
        chg = (pserial(B) != sb)
    IA, _ = S.trace(IA, x)
    IB = IB if md == 'D' else S.trace(IB, x)[0]
    agree = agree and (dA, dB) == (eA, eB) and pserial(A) == iserial(IA) \
        and pserial(B) == iserial(IB)
    legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                 "delta": q - 2 * a, "rb": rb, "chg": chg})
    mx = max(mx, len(core_of(pserial(B), K)))
S1 = (pserial(A), pserial(B))
Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
pos = [l for l in legs if l["delta"] > 0]
print("A=%d Q=%d W=%d closure=%s/%s engines=%s maxcore=%d (<=8)" % (
    Atot, Qtot, Qtot - 2 * Atot, S1[0] == S0[0], S1[1] == S0[1], agree, mx))
print("positives:", [(l["x"], l["a"], l["q"], l["delta"], l["rb"]) for l in pos])
print("K7 succ keys:", [legs[1]["x"], legs[2]["x"], legs[3]["x"]],
      "(need !=1 for AJ/AK-AL/AM)")
print("genuine KEEP per key:", {k: any(l["m"] == "K" and l["x"] == k and l["chg"] for l in legs) for k in sorted(K)})

def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
bl = [{"key": l["x"], "keys": [l["x"]], "a": l["a"], "q": l["q"],
       "delta": l["delta"], "genuine": l["chg"], "dB": l["dB"], "rb": l["rb"],
       "keeps": [l["x"]] if l["m"] == "K" else [], "dA": l["dA"], "push": [],
       "l0": i, "l1": i + 1} for i, l in enumerate(legs)]
AO = load('ao', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AO/26AO_two_order_recognizer.py')
AP = load('ap', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AP/26AP_maximal_run_recognizer.py')
AQ = load('aq', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AQ/26AQ_mixed_cyclic_dp_recognizer.py')
AR = load('ar', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AR/26AR_mixed_exact_cover_recognizer.py')
ASS = load('ass', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS/26AS_mixed_cyclic_recognizer.py')
rec = {"26AO": bool((AO.recognize(bl) or {}).get("accepted")),
       "26AP": bool((AP.recognize(bl) or {}).get("accepted")),
       "26AQ": bool((AQ.recognize(bl) or {}).get("accepted")),
       "26AR": bool((AR.recognize(bl) or {}).get("accepted")),
       "26AS": bool((ASS.recognize(bl, {i: {} for i in range(len(legs))}) or {}).get("accepted"))}
print("recognizers:", rec)
json.dump({"word": WORD, "K": sorted(K), "A": Atot, "Q": Qtot,
           "W": Qtot - 2 * Atot, "closure": [S1[0] == S0[0], S1[1] == S0[1]],
           "engines": agree, "maxcore": mx,
           "positives": [{"x": l["x"], "a": l["a"], "q": l["q"],
                          "d": l["delta"], "rb": l["rb"]} for l in pos],
           "recognizers": rec, "legs": legs},
          open(RDIR / 'DIRECT_CDK5_LOW_five_key_witness.json', 'w'), indent=1)
