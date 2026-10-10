"""ERRATUM replay: SHA-pinned INC/CTL fixtures, hard gates BEFORE engine init."""
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_S1_G0_ERRATUM')
RDIR.mkdir(parents=True, exist_ok=True)

def fixture_sha256(word):
    canonical = ",".join(mode + str(key) for mode, key in word)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()

# --- fixtures from literals (never imported, never reconstructed) ---
INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
       ('D', 6), ('D', 1), ('D', 9)]
CTL = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
       ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
EXPECTED_INC_SHA256 = "ff156d94f3b9c3c72c1c54a4798bcd63f16b71cfd5f29cb4f02ae51ea5f23602"
EXPECTED_CTL_SHA256 = "753bb2114f4ef20fd47fefde97a1f86fb092d76ed894fd03fccca7a1cb1cd49a"
FORBIDDEN_SHA256 = "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50"

# --- hard gates (STOP BEFORE REPLAY on any failure) ---
assert len(INC) == 17
assert len(CTL) == 18
assert fixture_sha256(INC) == EXPECTED_INC_SHA256
assert fixture_sha256(CTL) == EXPECTED_CTL_SHA256
assert fixture_sha256(INC) != FORBIDDEN_SHA256
assert INC[4] == ("D", 5)
assert INC[7] == ("K", 9)
assert INC[8] == ("K", 5)
assert INC[12] == ("D", 2)
assert INC[13] == ("D", 5)
assert INC[14] == ("D", 6)
assert INC[15] == ("D", 1)
assert INC[16] == ("D", 9)
assert CTL[4] == ("D", 9)
assert CTL[5] == ("D", 5)
assert CTL[9] == ("K", 5)
assert CTL[10] == ("K", 7)
assert INC != CTL
print("fixture gates: PASS (INC ff156d94.., CTL 753bb211.., forbidden excluded)", flush=True)
json.dump({"INC_sha": fixture_sha256(INC), "CTL_sha": fixture_sha256(CTL),
           "lengths": [len(INC), len(CTL)], "gates": "PASS"},
          open(RDIR / 'ERRATUM_frozen_fixture_manifest.json', 'w'), indent=1)

from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S

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
    print("%s: A=%d Q=%d Ck=%d Q-2Ck=%d Q-2A=%d closure=%s/%s engines=%s nblocks=%d K=%s cores=%s" % (
        name, Atot, Qtot, Ck, Qtot - 2 * Ck, Qtot - 2 * Atot,
        S1[0] == S0[0], S1[1] == S0[1], agree, len(blocks), Kset,
        "all9" if all(v == 9 for v in cores) else cores), flush=True)
    for k, v in exp.items():
        got = {"A": Atot, "Q": Qtot, "Ck": Ck, "n": len(legs),
               "nb": len(blocks)}[k]
        assert got == v, (name, k, got, v)
    return {"word": word, "legs": legs, "A": Atot, "Q": Qtot, "Ck": Ck,
            "closure": [S1[0] == S0[0], S1[1] == S0[1]], "engines": agree,
            "K": Kset, "genuine": gen, "cores": cores, "nblocks": len(blocks),
            "IV": IV,
            "nonshadow": all(l["Apost"] != l["Bpost"] for l in legs if l["m"] == "K")}

ri = analyze("INCLUSION", INC, {"A": 33, "Q": 18, "Ck": 8, "n": 17, "nb": 17})
rc = analyze("EXCLUSION", CTL, {"A": 29, "Q": 18, "Ck": 8, "n": 18, "nb": 18})
json.dump(ri, open(RDIR / 'ERRATUM_inclusion_witness.json', 'w'), indent=1)
json.dump(rc, open(RDIR / 'ERRATUM_excluded_control.json', 'w'), indent=1)
print("witness/control JSONs written", flush=True)
print("IV inclusion:", [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in ri["IV"]], flush=True)
k5iv = [iv for iv in ri["IV"] if iv["x"] == 5][0]
k7next = ri["IV"][(ri["IV"].index(k5iv) + 1) % len(ri["IV"])]
print("exception check: K5", {k: k5iv[k] for k in ("H", "q", "w", "R")},
      "succ K7", {k: k7next[k] for k in ("H", "q", "w", "R")}, flush=True)
k5c = [iv for iv in rc["IV"] if iv["x"] == 5][0]
k7c = rc["IV"][(rc["IV"].index(k5c) + 1) % len(rc["IV"])]
print("control check: K5", {k: k5c[k] for k in ("H", "q", "w", "R")},
      "succ K7", {k: k7c[k] for k in ("H", "q", "w", "R")}, flush=True)
json.dump(ri, open(RDIR / 'ERRATUM_inclusion_witness.json', 'w'), indent=1)
json.dump(rc, open(RDIR / 'ERRATUM_excluded_control.json', 'w'), indent=1)
