"""MRP independent verifier: tuple-first, raise-based fail-closed checks (v2 clean).

SHA-gates (INC/CTL-A/CTL-B/CTL-C + forbidden) BEFORE replay. Fresh
implementation; no imports from historical replay modules. Exact ints. Finite
fidelity only — universality lives in MRP_*_lemma/proof.md.
"""
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_MR_PROOF')
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push

def need(cond, msg):
    if not cond:
        raise CertificationError(msg)
class CertificationError(Exception):
    pass

def fz(word):
    return hashlib.sha256(",".join(m + str(k) for m, k in word).encode("ascii")).hexdigest()
INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 5),
       ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9), ('D', 8),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 4),
       ('D', 2), ('D', 5), ('D', 6), ('D', 1), ('D', 9)]
CTL_A = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
         ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
         ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
CTL_B = CTL_A + CTL_A
S2BASE = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
          ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
          ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
CTL_C = S2BASE + S2BASE
need(len(INC) == 33, "INC length")
need(len(CTL_A) == 18, "CTL_A length")
need(len(CTL_B) == 36, "CTL_B length")
need(len(CTL_C) == 36, "CTL_C length")
need(fz(INC) == "f647667922643558a8f8eed34d58293fc7bda27d053fd56fec35354cdcb2521d", "INC SHA")
need(fz(CTL_A) == "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7", "CTL_A SHA")
need(fz(CTL_B) == "90eec8ce0b332e90b06bee41edcc1b60be4328c9d0ca0f0eb52f57c1ff9aa3f4", "CTL_B SHA")
need(fz(CTL_C) == "3f64f758fdbdda69b14a0ff476d8eab08525327077849ea8732dbe720a04302a", "CTL_C SHA")
need(fz(INC) != "c9203dc7045d4c339c1fab5cf5c4c9c84614f4a936417fee83a577ce68428f50", "forbidden SHA")
need(INC != CTL_A and INC != CTL_B, "fixtures distinct")
print("SHA gates: PASS", flush=True)
json.dump({"INC": fz(INC), "CTL_A": fz(CTL_A), "CTL_B": fz(CTL_B),
           "CTL_C": fz(CTL_C), "lengths": [33, 18, 36, 36], "gates": "PASS"},
          open(RDIR / 'MRP_fixture_integrity.json', 'w'), indent=1)

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
        pp = path(s, m, [])
        need(pp is not None, "marked key missing")
        c.update(pp)
    return c

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
M = {1, 3, 5, 7, 9}

def vrun(word, name):
    A = totup(copy.deepcopy(T0)); B = totup(copy.deepcopy(T0))
    P = to_ptr(copy.deepcopy(T0)); Q = to_ptr(copy.deepcopy(T0))
    need(ser(A) == ser(B), name + " diagonal start")
    S0 = (ser(A), ser(B))
    legs, ok, pairs = [], True, [S0]
    for (md, x) in word:
        da = dep(A).get(x, -1)
        need(da >= 0, "%s absent A %s %s" % (name, md, x))
        a = (da + 1) // 2
        db = dep(B).get(x, -1) if md == 'K' else None
        q = db // 2 if md == 'K' else 0
        A = T(A, x)
        P, _ = splay_A(P, x)
        if md == 'K':
            B = T(B, x)
            sb = pser(Q)
            Q, _ = splay_B_push(Q, x)
        ok = ok and ser(A) == pser(P) and ser(B) == pser(Q)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q})
        pairs.append((ser(A), ser(B)))
    need(ok, name + " engine agreement")
    return legs, S0, (ser(A), ser(B)), pairs

def vcheck(name, word, exp, mode):
    legs, S0, S1, pairs = vrun(word, name)
    need(pairs[-1] == pairs[0], name + " closure")
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    ks = [l["x"] for l in legs if l["m"] == "K"]
    Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
    need((Atot, Qtot, Ck) == (exp["A"], exp["Q"], exp["Ck"]),
         "%s totals %s vs %s" % (name, (Atot, Qtot, Ck), exp))
    Kset = sorted({l["x"] for l in legs if l["m"] == "K"})
    need(len(Kset) == 5, name + " five keys")
    B = totup(copy.deepcopy(T0))
    cores = [len(core(ser(B), M))]
    for (md, x) in word:
        if md == 'K':
            B = T(B, x)
        cores.append(len(core(ser(B), M)))
    need(all(v == 9 for v in cores), name + " core9")
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
    need(sum(iv["H"] for iv in IV) == Atot, name + " sumH")
    need(sum(iv["w"] for iv in IV) == Qtot - 2 * Ck, name + " sumw")
    need(sum(iv["R"] for iv in IV) == 2 * (Atot - Ck), name + " sumR")
    need(all(iv["H"] >= iv["c"] for iv in IV), name + " baseline")
    need(Qtot <= 2 * Atot, name + " Q<=2A")
    if mode == "inclusion":
        exc = [n for n, iv in enumerate(IV) if iv["c"] == 1 and iv["q"] == 3 and iv["H"] == 1]
        need(exc == [4, 12], "%s exceptions %s" % (name, exc))
        m = len(IV)
        for e in exc:
            br, h = [], 1
            while True:
                b = IV[(e + h) % m]
                if b["c"] == 1 and b["H"] == 1 and b["q"] <= 2:
                    br.append(b); h += 1
                else:
                    break
            need(len(br) == 2, "%s relay t" % name)
            pay = IV[(e + h) % m]
            need(pay["c"] == 1 and pay["H"] >= 2 and pay["q"] <= 3, "%s payer" % name)
            need([b["x"] for b in br] == [7, 1], "%s bridge keys" % name)
            need(pay["x"] == 9, "%s payer key" % name)
        need({4, 5, 6, 7}.isdisjoint({12, 13, 14, 15}), name + " disjoint")
        special = {4, 5, 6, 7, 12, 13, 14, 15}
        for n, iv in enumerate(IV):
            if n in special:
                continue
            if iv["w"] > 0:
                gi = [i for i, l in enumerate(legs) if l["m"] == "K"][n]
                l, prev = legs[gi], legs[gi - 1]
                need((l["dA"] >= 3) or (prev["m"] == "D" and prev["x"] != l["x"] and prev["a"] >= 1 and l["a"] >= 1),
                     "%s other debt K/P at %d" % (name, n))
    print("%s: A=%d Q=%d Ck=%d closure engines cores9 identities MR-check ALL PASS" % (
        name, Atot, Qtot, Ck), flush=True)
    return {"A": Atot, "Q": Qtot, "Ck": Ck, "closure": True, "engines": True,
            "IV": [(iv["x"], iv["H"], iv["q"], iv["w"], iv["R"]) for iv in IV],
            "pairs": len(pairs)}

ri = vcheck("INC", INC, {"A": 55, "Q": 36, "Ck": 16}, "inclusion")
ra = vcheck("CTL_A", CTL_A, {"A": 31, "Q": 18, "Ck": 8}, "other")
rb = vcheck("CTL_B", CTL_B, {"A": 62, "Q": 36, "Ck": 16}, "other")
rc = vcheck("CTL_C", CTL_C, {"A": 58, "Q": 36, "Ck": 16}, "other")
json.dump({"INC": ri, "CTL_A": ra, "CTL_B": rb, "CTL_C": rc, "verdict": "PASS",
           "hashes": {k: __import__("hashlib").sha256(open(p, 'rb').read()).hexdigest()[:12]
                      for k, p in (("eventflow", 'scripts/wp6_eventflow.py'),
                                   ("coarse_double", 'scripts/wp6_coarse_double.py'),
                                   ("splay", 'python/independent/splay.py'),
                                   ("legacy", 'python/liquidity/legacy_embedding.py'))}},
          open(RDIR / 'MRP_verification_results.json', 'w'), indent=1)
print("INDEPENDENT VERIFIER: PASS", flush=True)
