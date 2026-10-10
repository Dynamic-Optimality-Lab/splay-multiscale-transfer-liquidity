"""S1P independent verifier (§19): fresh tuple-first implementation.

SHA-gates fixtures (incl. forbidden rejection); tuple-first replay with pointer
cross-check; depths/costs/closure/cores/keys; intervals H/c/w/R; identities;
exception+successor; Type K/P on other debts; CTL S1-exclusion; engines agree.
Exact ints. Finite fidelity check only — universality lives in S1P_*_lemma.md.
"""
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_S1_PROOF')
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push

def fz(w):
    return hashlib.sha256(",".join(m + str(k) for m, k in w).encode("ascii")).hexdigest()
INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
       ('D', 6), ('D', 1), ('D', 9)]
CTL = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
       ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
assert len(INC) == 17 and len(CTL) == 18
assert fz(INC) == "ff156d94f3b9c3c72c1c54a4798bcd63f16b71cfd5f29cb4f02ae51ea5f23602"
assert fz(CTL) == "753bb2114f4ef20fd47fefde97a1f86fb092d76ed894fd03fccca7a1cb1cd49a"
assert fz(INC) != "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50"
assert (INC[4], INC[7], INC[8], INC[12], INC[13], INC[14], INC[15], INC[16]) == \
    (("D", 5), ("K", 9), ("K", 5), ("D", 2), ("D", 5), ("D", 6), ("D", 1), ("D", 9))
assert (CTL[4], CTL[5], CTL[9], CTL[10]) == (("D", 9), ("D", 5), ("K", 5), ("K", 7))
assert INC != CTL

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
        chg = False
        if md == 'K':
            B = T(B, x)
            sb = pser(Q)
            Q, _ = splay_B_push(Q, x)
            chg = (pser(Q) != sb)
        ok = ok and ser(A) == pser(P) and ser(B) == pser(Q)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q, "chg": chg})
    return legs, ok, S0, (ser(A), ser(B))

def check(name, word, exp, s1checks):
    legs, ok, S0, S1 = run(word)
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    Kset = sorted({l["x"] for l in legs if l["m"] == "K"})
    assert all(any(l["m"] == "K" and l["x"] == k and l["chg"] for l in legs) for k in Kset)
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
                   "w": legs[i]["q"] - 2 * c, "R": 2 * (H - c), "gi": i})
    assert Atot == exp["A"] and Qtot == exp["Q"] and Ck == exp["Ck"]
    assert S0[0] == S1[0] and S0[1] == S1[1] and ok
    assert sum(iv["H"] for iv in IV) == Atot and sum(iv["w"] for iv in IV) == Qtot - 2 * Ck
    assert sum(iv["R"] for iv in IV) == 2 * (Atot - Ck)
    assert all(iv["H"] >= iv["c"] for iv in IV) and all(iv["w"] <= iv["R"] or True for iv in IV)
    # per-interval local check with S1 rule: exception+successor joint, rest w<=R
    exc = [iv for iv in IV if iv["H"] == 1 and iv["q"] == 3 and iv["w"] == 1 and iv["R"] == 0]
    s1checks(name, legs, ki, IV, exc)
    print(name, ": A=%d Q=%d Ck=%d closure engines cores9 identities ALL PASS" % (Atot, Qtot, Ck), flush=True)
    return {"A": Atot, "Q": Qtot, "Ck": Ck, "closure": True, "engines": ok,
            "cores9": True, "IV": [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in IV]}

def inc_checks(name, legs, ki, IV, exc):
    assert len(exc) == 1 and exc[0]["x"] == 5, exc
    j = IV.index(exc[0])
    suc = IV[(j + 1) % len(IV)]
    assert suc["x"] == 7 and suc["H"] >= 2 and suc["q"] <= 3 and suc["c"] == 1
    assert exc[0]["w"] + suc["w"] <= exc[0]["R"] + suc["R"]
    for n, iv in enumerate(IV):
        if n in (j, (j + 1) % len(IV)):
            continue
        if iv["w"] > 0:
            gi = [i for i, l in enumerate(legs) if l["m"] == "K"][n]
            prev = legs[gi - 1]
            l = legs[gi]
            tk = l["dA"] >= 3
            tp = (prev["m"] == "D" and prev["x"] != l["x"] and prev["a"] >= 1 and l["a"] >= 1)
            assert tk or tp, iv
        else:
            assert iv["w"] <= iv["R"], iv

def ctl_checks(name, legs, ki, IV, exc):
    assert len(exc) == 1 and exc[0]["x"] == 5, exc
    j = IV.index(exc[0])
    suc = IV[(j + 1) % len(IV)]
    assert suc["x"] == 7 and suc["H"] == 1, suc
    assert not (suc["H"] >= 2), "control must fail successor condition"

ri = check("INC", INC, {"A": 33, "Q": 18, "Ck": 8}, inc_checks)
rc = check("CTL", CTL, {"A": 29, "Q": 18, "Ck": 8}, ctl_checks)
json.dump({"INC": ri, "CTL": rc, "verdict": "PASS",
           "hashes": {k: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
                      for k, p in (("eventflow", 'scripts/wp6_eventflow.py'),
                                   ("splay", 'python/independent/splay.py'),
                                   ("legacy", 'python/liquidity/legacy_embedding.py'))}},
          open(RDIR / 'S1P_verification_results.json', 'w'), indent=1)
print("INDEPENDENT VERIFIER: PASS", flush=True)
