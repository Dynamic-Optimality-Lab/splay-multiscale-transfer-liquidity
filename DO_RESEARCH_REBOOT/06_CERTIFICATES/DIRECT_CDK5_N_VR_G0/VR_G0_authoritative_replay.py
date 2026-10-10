"""VR-G0: SHA-pinned replay INC(18)+CTL-A(18)+CTL-B(17) + primitivity + 43758 cross-check."""
import sys, copy, json, hashlib, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_VR_G0')
RDIR.mkdir(parents=True, exist_ok=True)
LOG = open(RDIR / 'VR_G0_replay.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush(); print(s, flush=True)

def fz(word):
    return hashlib.sha256(",".join(m + str(k) for m, k in word).encode("ascii")).hexdigest()

INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
CTL_A = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
         ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
         ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
CTL_B = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
         ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
         ('D', 6), ('D', 1), ('D', 9)]
FORBIDDEN = "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50"
assert len(INC) == 18 and len(CTL_A) == 18 and len(CTL_B) == 17
assert fz(INC) == "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7"
assert fz(CTL_A) == "753bb2114f4ef20fd47fefde97a1f86fb092d76ed894fd03fccca7a1cb1cd49a"
assert fz(CTL_B) == "ff156d94f3b9c3c72c1c54a4798bcd63f16b71cfd5f29cb4f02ae51ea5f23602"
assert fz(INC) != FORBIDDEN and fz(CTL_A) != FORBIDDEN and fz(CTL_B) != FORBIDDEN
assert INC != CTL_A and INC != CTL_B
log("fixture gates: PASS (INC b4165259, CTL-A 753bb211, CTL-B ff156d94)")
json.dump({"INC": fz(INC), "CTL_A": fz(CTL_A), "CTL_B": fz(CTL_B),
           "lengths": [18, 18, 17], "gates": "PASS"},
          open(RDIR / 'VR_G0_fixture_manifest.json', 'w'), indent=1)

from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S
import wp6_cycle_ratio as O

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
M = {1, 3, 5, 7, 9}

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
    blocks = []
    for lg in legs:
        if lg["a"] >= 1:
            blocks.append([lg])
        else:
            assert blocks and lg["x"] == blocks[-1][0]["x"], ("stray no-op", lg)
            blocks[-1].append(lg)
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
    log("%s: A=%d Q=%d Ck=%d Q-2Ck=%d Q-2A=%d closure=%s/%s engines=%s nblocks=%d K=%s cores=%s" % (
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

ri = analyze("INCLUSION", INC, {"A": 31, "Q": 18, "Ck": 8, "n": 18, "nb": 18})
ra = analyze("CTL-A", CTL_A, {"A": 29, "Q": 18, "Ck": 8, "n": 18, "nb": 18})
rb = analyze("CTL-B", CTL_B, {"A": 33, "Q": 18, "Ck": 8, "n": 17, "nb": 17})
log("K-order inclusion: %s" % [l["x"] for l in ri["legs"] if l["m"] == "K"])
log("IV inclusion: %s" % [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in ri["IV"]])
exc = [iv for iv in ri["IV"] if iv["H"] == 1 and iv["q"] == 3 and iv["w"] == 1 and iv["R"] == 0]
log("exceptions: %s" % [iv["x"] for iv in exc])
assert len(exc) == 1 and exc[0]["x"] == 5
j = ri["IV"].index(exc[0])
m = len(ri["IV"])
# maximal creditless bridge run (c=1,H=1,q<=2), then payer (c=1,H>=2,q<=3)
run = []
h = 1
while True:
    b = ri["IV"][(j + h) % m]
    if b["c"] == 1 and b["H"] == 1 and b["q"] <= 2:
        run.append(b); h += 1
    else:
        break
t = len(run)
pay = ri["IV"][(j + h) % m]
log("relay t=%d bridges=%s payer=%s" % (
    t, [(b["x"], b["H"], b["q"], b["w"], b["R"]) for b in run],
    {k: pay[k] for k in ("x", "H", "q", "w", "R")}))
assert 2 <= t <= m - 2, t
assert pay["c"] == 1 and pay["H"] >= 2 and pay["q"] <= 3
assert exc[0]["w"] + sum(b["w"] for b in run) + pay["w"] <= \
    exc[0]["R"] + sum(b["R"] for b in run) + pay["R"]
special = {(j + hh) % m for hh in range(t + 2)}
# primitivity: no repeated INTERMEDIATE pair state (start=end is closure itself),
# no proper closed subcycle, aperiodic word
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
pairs = [(pserial(A), pserial(B))]
for (md, x) in INC:
    A, _ = splay_A(A, x)
    if md == 'K':
        B, _ = splay_B_push(B, x)
    pairs.append((pserial(A), pserial(B)))
assert pairs[-1] == pairs[0], "closure"
assert len(set(pairs[:-1])) == len(pairs) - 1, "repeated intermediate pair state"
n = len(INC)
proper = False
for L in range(1, n):
    if n % L == 0:
        words = [tuple(INC[i:i + L]) for i in range(0, n, L)]
        if len(set(words)) == 1:
            proper = True
assert not proper, "periodic word"
log("primitivity: 19 distinct boundary states, word aperiodic")
# other positive debts need Type K/P (outside exception+relay+payer packet)
for nn, iv in enumerate(ri["IV"]):
    if nn in special:
        continue
    if iv["w"] > 0:
        gi = [i for i, l in enumerate(ri["legs"]) if l["m"] == "K"][nn]
        l = ri["legs"][gi]; prev = ri["legs"][gi - 1]
        tk = l["dA"] >= 3
        tp = (prev["m"] == "D" and prev["x"] != l["x"] and prev["a"] >= 1 and l["a"] >= 1)
        assert tk or tp, iv
        log("other debt %s %s" % (iv["x"], "TypeK" if tk else "TypeP"))
json.dump(ri, open(RDIR / 'VR_G0_inclusion_witness.json', 'w'), indent=1)
json.dump({"CTL_A": ra, "CTL_B": rb}, open(RDIR / 'VR_G0_excluded_controls.json', 'w'), indent=1)

# cross-engine regression: all 9-key shapes x all 9 splays
CACHE = {}
shapes = O.shapes_of(list(range(1, 10)))
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def idepths2(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def iser2(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, iser2(l), iser2(r))
bad = tot = 0
for T0s in shapes:
    for x in range(1, 10):
        tot += 1
        P = to_ptr(copy.deepcopy(T0s))
        d0 = pdepths(P)
        P2, _ = splay_A(P, x)
        Tt = to_tup(copy.deepcopy(T0s))
        e0 = idepths2(Tt)
        T2 = S.trace(Tt, x)[0]
        if not (pserial(P2) == iser2(T2) and d0 == e0 and pdepths(P2) == idepths2(T2)):
            bad += 1
log("cross-engine: %d transitions, %d disagreements" % (tot, bad))
assert tot == 43758 and bad == 0
json.dump({"transitions": tot, "disagreements": bad},
          open(RDIR / 'VR_G0_cross_engine_regression.json', 'w'), indent=1)
log("done")
LOG.close()
