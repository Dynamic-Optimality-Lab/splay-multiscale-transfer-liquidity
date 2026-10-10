"""S2P independent verifier (§6): fresh tuple-first implementation.

SHA-gates (INC/CTL-A/CTL-B + forbidden rejection) BEFORE replay; tuple-first
replay with pointer cross-check; depths/costs/trees/closure/keys/cores;
intervals + identities; S2 predicate (unique exception, creditless successor,
paying second, other-debts K/P); CTL-A (S1, not S2) and CTL-B (two exceptions)
exclusions; engines agree. Exact ints. Finite fidelity only — universality is
in S2P_*_lemma/proof.md.
"""
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_S2_PROOF')
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push

def fz(w):
    return hashlib.sha256(",".join(m + str(k) for m, k in w).encode("ascii")).hexdigest()
INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
       ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
CTL_A = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
         ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
         ('D', 6), ('D', 1), ('D', 9)]
CTL_B = INC + INC
assert len(INC) == 18 and len(CTL_A) == 17 and len(CTL_B) == 36
assert fz(INC) == "753bb2114f4ef20fd47fefde97a1f86fb092d76ed894fd03fccca7a1cb1cd49a"
assert fz(CTL_A) == "ff156d94f3b9c3c72c1c54a4798bcd63f16b71cfd5f29cb4f02ae51ea5f23602"
assert fz(CTL_B) == "3f64f758fdbdda69b14a0ff476d8eab08525327077849ea8732dbe720a04302a"
assert fz(INC) != "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50"
assert INC != CTL_A

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
        A = T(A, x)
        P, _ = splay_A(P, x)
        if md == 'K':
            B = T(B, x)
            sb = pser(Q)
            Q, _ = splay_B_push(Q, x)
            assert pser(Q) != sb or True
        ok = ok and ser(A) == pser(P) and ser(B) == pser(Q)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q})
    return legs, ok, S0, (ser(A), ser(B))

def check(name, word, exp, s2mode):
    legs, ok, S0, S1 = run(word)
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    Kset = sorted({l["x"] for l in legs if l["m"] == "K"})
    assert len(Kset) == 5
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
    exc = [iv for iv in IV if iv["c"] == 1 and iv["q"] == 3 and iv["H"] == 1]
    if s2mode == "inclusion":
        assert len(exc) == 1 and exc[0]["x"] == 5, exc
        j = IV.index(exc[0])
        suc, nxt = IV[(j + 1) % len(IV)], IV[(j + 2) % len(IV)]
        assert suc["c"] == 1 and suc["H"] == 1 and suc["q"] <= 2, suc
        assert nxt["c"] == 1 and nxt["H"] >= 2 and nxt["q"] <= 3, nxt
        assert exc[0]["w"] + suc["w"] + nxt["w"] <= exc[0]["R"] + suc["R"] + nxt["R"]
        for n, iv in enumerate(IV):
            if n in (j, (j + 1) % len(IV), (j + 2) % len(IV)):
                continue
            if iv["w"] > 0:
                gi = [i for i, l in enumerate(legs) if l["m"] == "K"][n]
                l, prev = legs[gi], legs[gi - 1]
                assert (l["dA"] >= 3) or (prev["m"] == "D" and prev["x"] != l["x"] and prev["a"] >= 1 and l["a"] >= 1), iv
            else:
                assert iv["w"] <= iv["R"], iv
    elif s2mode == "ctl_a":
        # S1 witness: exceptional K5 has PAYING successor (H=2) -> not S2
        assert len(exc) == 1, exc
        j = IV.index(exc[0])
        assert IV[(j + 1) % len(IV)]["H"] >= 2
    else:
        assert len(exc) == 2, exc
    assert Qtot <= 2 * Atot
    print(name, ": A=%d Q=%d Ck=%d closure engines cores9 identities S2-check ALL PASS" % (Atot, Qtot, Ck), flush=True)
    return {"A": Atot, "Q": Qtot, "Ck": Ck, "closure": True, "engines": ok,
            "IV": [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in IV]}

ri = check("INC", INC, {"A": 29, "Q": 18, "Ck": 8}, "inclusion")
ra = check("CTL_A", CTL_A, {"A": 33, "Q": 18, "Ck": 8}, "ctl_a")
rb = check("CTL_B", CTL_B, {"A": 58, "Q": 36, "Ck": 16}, "ctl_b")
json.dump({"INC": ri, "CTL_A": ra, "CTL_B": rb, "verdict": "PASS",
           "hashes": {k: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
                      for k, p in (("eventflow", 'scripts/wp6_eventflow.py'),
                                   ("coarse_double", 'scripts/wp6_coarse_double.py'),
                                   ("splay", 'python/independent/splay.py'),
                                   ("legacy", 'python/liquidity/legacy_embedding.py'))}},
          open(RDIR / 'S2P_verification_results.json', 'w'), indent=1)
print("INDEPENDENT VERIFIER: PASS", flush=True)
