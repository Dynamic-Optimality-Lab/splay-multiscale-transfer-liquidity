"""S1-G0: authoritative replay of inclusion (17) + exclusion (18) words."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_S1_G0')
RDIR.mkdir(parents=True, exist_ok=True)
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S

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
        p = path_to(serial, m, [])
        assert p is not None
        core.update(p)
    return core

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
M = {1, 3, 5, 7, 9}

def replay(word):
    A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
    assert pserial(A) == pserial(B)
    IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
    S0 = (pserial(A), pserial(B))
    legs, agree = [], True
    for (md, x) in word:
        dA = pdepths(A).get(x, -1); assert dA >= 0, ("absent A", x)
        a = (dA + 1) // 2
        ra, rb = proot(A), proot(B)
        sb = pserial(B)
        if md == 'K':
            dB = pdepths(B).get(x, -1); assert dB >= 0, ("absent B", x)
            q = dB // 2
        else:
            dB = None; q = 0
        eA = idepths(IA).get(x); eB = idepths(IB).get(x) if md == 'K' else None
        A, _ = splay_A(A, x)
        push = []
        if md == 'K':
            B, outB = splay_B_push(B, x)
            for s in outB:
                push += list(s)
        IA = S.trace(IA, x)[0]
        IB = IB if md == 'D' else S.trace(IB, x)[0]
        chg = (pserial(B) != sb) if md == 'K' else False
        agree = agree and (dA, dB) == (eA, eB) and pserial(A) == iserial(IA) \
            and pserial(B) == iserial(IB)
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": ra, "rb": rb, "chg": chg,
                     "push": sorted(set(push)), "Apost": pserial(A),
                     "Bpost": pserial(B)})
    return legs, agree, S0, (pserial(A), pserial(B))

def analyze(name, word, exp):
    legs, agree, S0, S1 = replay(word)
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    Kset = sorted({l["x"] for l in legs if l["m"] == "K"})
    gen = {k: any(l["m"] == "K" and l["x"] == k and l["chg"] for l in legs) for k in Kset}
    A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
    cores = [len(core_of(pserial(B), set(Kset)))]
    for (md, x) in word:
        A, _ = splay_A(A, x)
        if md == 'K':
            B, _ = splay_B_push(B, x)
        cores.append(len(core_of(pserial(B), set(Kset))))
    # blocks
    blocks = []
    for lg in legs:
        if lg["a"] >= 1:
            blocks.append([lg])
        else:
            assert blocks and lg["x"] == blocks[-1][0]["x"], ("stray no-op", lg)
            blocks[-1].append(lg)
    # intervals
    ki = [i for i, l in enumerate(legs) if l["m"] == "K"]
    IV = []
    for n, i in enumerate(ki):
        prev = ki[n - 1]
        seg = legs[prev + 1:i + 1] if prev < i else legs[prev + 1:] + legs[:i + 1]
        H = sum(l["a"] for l in seg)
        x = legs[i]["x"]; xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        IV.append({"x": x, "H": H, "c": c, "q": legs[i]["q"],
                   "w": legs[i]["q"] - 2 * c, "R": 2 * (H - c)})
    print("%s: A=%d Q=%d Ck=%d Q-2Ck=%d Q-2A=%d closure=%s/%s engines=%s nblocks=%d K=%s cores=%s" % (
        name, Atot, Qtot, Ck, Qtot - 2 * Ck, Qtot - 2 * Atot,
        S1[0] == S0[0], S1[1] == S0[1], agree, len(blocks), Kset,
        "all9" if all(v == 9 for v in cores) else cores))
    for k, v in exp.items():
        got = {"A": Atot, "Q": Qtot, "Ck": Ck, "n": len(legs),
               "nb": len(blocks)}[k]
        assert got == v, (name, k, got, v)
    return {"word": word, "legs": legs, "A": Atot, "Q": Qtot, "Ck": Ck,
            "closure": [S1[0] == S0[0], S1[1] == S0[1]], "engines": agree,
            "K": Kset, "genuine": gen, "cores": cores, "nblocks": len(blocks),
            "IV": IV,
            "nonshadow": all(l["Apost"] != l["Bpost"] for l in legs if l["m"] == "K")}

INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('K', 1), ('D', 4), ('K', 9),
       ('D', 6), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 2),
       ('D', 1), ('D', 6), ('D', 9)]
CTL = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
       ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
ri = analyze("INCLUSION", INC, {"A": 33, "Q": 18, "Ck": 8, "n": 17, "nb": 17})
rc = analyze("EXCLUSION", CTL, {"A": 29, "Q": 18, "Ck": 8, "n": 18, "nb": 18})
print("K-order inclusion:", [l["x"] for l in ri["legs"] if l["m"] == "K"])
print("IV inclusion:", [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in ri["IV"]])
print("IV exclusion K5/K7:", [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in rc["IV"] if iv["x"] in (5, 7)][:4])
json.dump(ri, open(RDIR / 'S1_inclusion_witness.json', 'w'), indent=1)
json.dump(rc, open(RDIR / 'S1_exclusion_control.json', 'w'), indent=1)
json.dump({"inclusion": 17, "exclusion": 18, "engines": "agree all",
           "verdict": "PASS"},
          open(RDIR / 'S1_independent_verification.json', 'w'), indent=1)
