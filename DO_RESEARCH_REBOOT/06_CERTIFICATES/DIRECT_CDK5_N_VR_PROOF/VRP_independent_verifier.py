"""VRP independent verifier (§6): fresh tuple-first implementation.

SHA-gates (INC/CTL-A/CTL-B + forbidden rejection) BEFORE replay; tuple-first
replay with pointer cross-check per access (depths, serials); closure/keys/
cores/intervals/identities; S2-style VR predicate (unique exception, maximal
relay, payer, other-debts K/P); CTL-A (S1: successor H=2) and CTL-B (S1 word)
exclusions; engines agree. Exact ints. Finite fidelity only — universality is
in VRP_*_lemma/proof.md.
"""
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_VR_PROOF')
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push

def fz(w):
    return hashlib.sha256(",".join(m + str(k) for m, k in w).encode("ascii")).hexdigest()
INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
CTL_A = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
         ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
         ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
CTL_B = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
         ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
         ('D', 6), ('D', 1), ('D', 9)]
assert len(INC) == 18 and len(CTL_A) == 18 and len(CTL_B) == 17
assert fz(INC) == "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7"
assert fz(CTL_A) == "753bb2114f4ef20fd47fefde97a1f86fb092d76ed894fd03fccca7a1cb1cd49a"
assert fz(CTL_B) == "ff156d94f3b9c3c72c1c54a4798bcd63f16b71cfd5f29cb4f02ae51ea5f23602"
assert fz(INC) != "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50"
assert INC != CTL_A and INC != CTL_B

def T(t, x):
    return S.trace(t, x)[0]
def dep(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def ser(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, ser(l), ser(r))
def totup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], totup(t[1]), totup(t[2]))
def pser(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def pdepths(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d; go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def core(s, M):
    c = set()
    def path(nd, x, p):
        if nd == '.':
            return None
        k, l, r = nd
        p = p + [k]
        if k == x:
            return p
        return path(l, x, p) or path(r, x, p)
    for m in M:
        c.update(path(s, m, []))
    return c

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
M = {1, 3, 5, 7, 9}

def run(word):
    A = totup(copy.deepcopy(T0)); B = totup(copy.deepcopy(T0))
    P = to_ptr(copy.deepcopy(T0)); Q = to_ptr(copy.deepcopy(T0))
    S0 = (ser(A), ser(B))
    legs, ok = [], True
    for (md, x) in word:
        da = dep(A).get(x, -1); assert da >= 0
        a = (da + 1) // 2
        db = dep(B).get(x, -1) if md == 'K' else None
        q = db // 2 if md == 'K' else 0
        dAp, dBp = pdepths(P).get(x, -1), (pdepths(Q).get(x, -1) if md == 'K' else None)
        assert (da, db) == (dAp, dBp), ("engine depth mismatch", md, x)
        A = T(A, x)
        P, _ = splay_A(P, x)
        chg = False
        if md == 'K':
            B = T(B, x)
            sb = pser(Q)
            Q, _ = splay_B_push(Q, x)
            chg = (pser(Q) != sb)
        ok = ok and ser(A) == pser(P) and ser(B) == pser(Q)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q, "chg": chg,
                     "Apost": ser(A), "Bpost": ser(B)})
    return legs, ok, S0, (ser(A), ser(B))

def check(name, word, exp, mode):
    legs, ok, S0, S1 = run(word)
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    Kset = sorted({l["x"] for l in legs if l["m"] == "K"})
    assert len(Kset) == 5 and all(
        any(l["m"] == "K" and l["x"] == k and l["chg"] for l in legs) for k in Kset)
    B = totup(copy.deepcopy(T0))
    cores = [len(core(ser(B), M))]
    for (md, x) in word:
        if md == 'K':
            B = T(B, x)
        cores.append(len(core(ser(B), M)))
    assert all(v == 9 for v in cores)
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
    assert Atot == exp["A"] and Qtot == exp["Q"] and Ck == exp["Ck"]
    assert S0[0] == S1[0] and S0[1] == S1[1] and ok
    assert sum(iv["H"] for iv in IV) == Atot
    assert sum(iv["w"] for iv in IV) == Qtot - 2 * Ck
    assert sum(iv["R"] for iv in IV) == 2 * (Atot - Ck)
    assert all(iv["H"] >= iv["c"] for iv in IV)
    assert all(l["Apost"] != l["Bpost"] for l in legs if l["m"] == "K")
    exc = [iv for iv in IV if iv["c"] == 1 and iv["q"] == 3 and iv["H"] == 1]
    if mode == "inclusion":
        assert len(exc) == 1 and exc[0]["x"] == 5, exc
        j = IV.index(exc[0])
        m = len(IV)
        runb, h = [], 1
        while True:
            b = IV[(j + h) % m]
            if b["c"] == 1 and b["H"] == 1 and b["q"] <= 2:
                runb.append(b); h += 1
            else:
                break
        t = len(runb)
        pay = IV[(j + h) % m]
        assert 2 <= t <= m - 2, t
        assert pay["c"] == 1 and pay["H"] >= 2 and pay["q"] <= 3, pay
        assert exc[0]["w"] + sum(b["w"] for b in runb) + pay["w"] <= \
            exc[0]["R"] + sum(b["R"] for b in runb) + pay["R"]
        special = {(j + hh) % m for hh in range(t + 2)}
        for n, iv in enumerate(IV):
            if n in special:
                continue
            if iv["w"] > 0:
                gi = [i for i, l in enumerate(legs) if l["m"] == "K"][n]
                l, prev = legs[gi], legs[gi - 1]
                assert (l["dA"] >= 3) or (prev["m"] == "D" and prev["x"] != l["x"] and prev["a"] >= 1 and l["a"] >= 1), iv
    elif mode == "ctl_a":
        # S2 word: unique (H=1,q=3) exception but maximal creditless relay is
        # t==1 (single bridge), violating VR-H3 (t>=2) -> outside VR
        assert len(exc) == 1 and exc[0]["x"] == 5, exc
        j = IV.index(exc[0])
        m = len(IV)
        t = 0
        while True:
            b = IV[(j + 1 + t) % m]
            if b["c"] == 1 and b["H"] == 1 and b["q"] <= 2:
                t += 1
            else:
                break
        assert t == 1, t
    else:
        # S1 word: K5's successor already H=2 -> not VR
        assert len(exc) == 1, exc
        j = IV.index(exc[0])
        assert IV[(j + 1) % len(IV)]["H"] >= 2
    assert Qtot <= 2 * Atot
    print(name, ": A=%d Q=%d Ck=%d closure engines cores9 identities VR-check ALL PASS" % (Atot, Qtot, Ck), flush=True)
    return {"A": Atot, "Q": Qtot, "Ck": Ck, "closure": True, "engines": ok,
            "IV": [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in IV]}

ri = check("INC", INC, {"A": 31, "Q": 18, "Ck": 8}, "inclusion")
ra = check("CTL_A", CTL_A, {"A": 29, "Q": 18, "Ck": 8}, "ctl_a")
rb = check("CTL_B", CTL_B, {"A": 33, "Q": 18, "Ck": 8}, "ctl_b")
json.dump({"INC": ri, "CTL_A": ra, "CTL_B": rb, "verdict": "PASS",
           "hashes": {k: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
                      for k, p in (("eventflow", 'scripts/wp6_eventflow.py'),
                                   ("coarse_double", 'scripts/wp6_coarse_double.py'),
                                   ("splay", 'python/independent/splay.py'),
                                   ("legacy", 'python/liquidity/legacy_embedding.py'))}},
          open(RDIR / 'VRP_verification_results.json', 'w'), indent=1)
print("INDEPENDENT VERIFIER: PASS", flush=True)
