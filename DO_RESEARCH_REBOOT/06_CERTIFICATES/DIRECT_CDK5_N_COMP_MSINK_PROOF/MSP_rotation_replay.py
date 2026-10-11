# MSP Gate-B cyclic reaudit: fresh independent rotation machinery.
# No imports from Gate-0 MSINK_* modules. Source engines only.
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S

PDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_PROOF')
PDIR.mkdir(parents=True, exist_ok=True)
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
MSET = {1, 3, 5, 7, 9}
IN_CANON = ("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,"
            "K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
IN_SHA = "19ff110a7c6087256e5348454aa0d1da084a4b544a7904cc82c111af3c8783df"
VR_CANON = ("D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
VR_SHA = "b416525925db8824740cfa81c75f36226806f45e409efb2a5a5ea18a37547dd7"

def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)

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

def replay(word, A0=None, B0=None):
    A = to_ptr(copy.deepcopy(T0 if A0 is None else A0))
    Bp = to_ptr(copy.deepcopy(T0 if B0 is None else B0))
    S0 = (pserial(A), pserial(Bp))
    legs, pairs = [], [S0]
    agree = True
    import splay as _S
    IA = _S.LEAF if False else None
    # tuple cross-check trees from same start: rebuild pointer->tuple via serials
    def tup_of(ps):
        if ps == '.':
            return _S.LEAF
        k, l, r = ps
        return _S.node(k, tup_of(l), tup_of(r))
    IA = tup_of(S0[0]); IB = tup_of(S0[1])
    for (md, x) in word:
        dA = pdepths(A).get(x, -1)
        assert dA >= 0, ("absent A", x)
        a = (dA + 1) // 2
        sb = pserial(Bp)
        if md == 'K':
            dB = pdepths(Bp).get(x, -1)
            assert dB >= 0, ("absent B", x)
            q = dB // 2
        else:
            dB = None; q = 0
        eA = _dep(IA).get(x)
        eB = _dep(IB).get(x) if md == 'K' else None
        A, _ = splay_A(A, x)
        push = []
        if md == 'K':
            Bp, outB = splay_B_push(Bp, x)
            for s in outB:
                push += list(s)
        IA = _S.trace(IA, x)[0]
        if md == 'K':
            IB = _S.trace(IB, x)[0]
        chg = (pserial(Bp) != sb) if md == 'K' else False
        agree = agree and (dA, dB) == (eA, eB) and pserial(A) == _ser(IA) \
            and pserial(Bp) == _ser(IB)
        pairs.append((pserial(A), pserial(Bp)))
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "ra": None, "rb": None, "chg": chg,
                     "push": sorted(set(push))})
    return {"legs": legs, "pairs": pairs, "S0": S0, "S1": pairs[-1],
            "agree": agree}

def _dep(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def _ser(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, _ser(l), _ser(r))
def core_of(ps, M):
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
        pp = path(ps, m, [])
        if pp is None:
            return None
        c.update(pp)
    return c

def intervals(legs):
    ki = [i for i, l in enumerate(legs) if l["m"] == "K"]
    out = []
    for n, i in enumerate(ki):
        prev = ki[n - 1]
        if prev < i:
            segi = list(range(prev + 1, i + 1))
        else:
            segi = list(range(prev + 1, len(legs))) + list(range(0, i + 1))
        H = sum(legs[k]["a"] for k in segi)
        x = legs[i]["x"]; xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        out.append({"x": x, "H": H, "c": c, "q": legs[i]["q"],
                    "w": legs[i]["q"] - 2 * c, "R": 2 * (H - c), "gi": i,
                    "segi": segi})
    return out

def strict_K(ivj, legs):
    return legs[ivj["gi"]]["dA"] >= 3
def strict_P(ivj, legs):
    # immediately preceding original access: last leg before the KEEP in interval
    x = ivj["x"]
    if ivj["H"] < 2:
        return False
    kl = ivj["segi"][-2] if len(ivj["segi"]) >= 2 else None
    if kl is None:
        return False
    p = legs[kl]
    k = legs[ivj["gi"]]
    return p["m"] == "D" and p["x"] != x and p["a"] >= 1 and k["a"] >= 1

def E_slots(iv):
    return [j for j in range(len(iv))
            if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]

def s1_member(legs, pairs):
    iv = intervals(legs)
    s = len(iv)
    if s < 5:
        return False, "s<5"
    E = E_slots(iv)
    if len(E) != 1:
        return False, "E=%s" % E
    e = E[0]
    js = (e + 1) % s
    if not (iv[js]["c"] == 1 and iv[js]["q"] <= 3 and iv[js]["H"] >= 2):
        return False, "successor"
    for j in range(s):
        if j in (e, js) or iv[j]["w"] <= 0:
            continue
        if strict_K(iv[j], legs) or strict_P(iv[j], legs):
            continue
        return False, "other-%d" % j
    gk = sorted({l["x"] for l in legs if l["m"] == "K" and l["chg"]})
    if gk != [1, 3, 5, 7, 9]:
        return False, "gkeys=%s" % gk
    for t in range(len(pairs)):
        c = core_of(pairs[t][1], MSET)
        if c is None or len(c) != 9:
            return False, "core@%d" % t
    if pairs[0] != pairs[-1]:
        return False, "not-closed"
    return True, "S1-member"

def relay_len(iv, e):
    s = len(iv)
    k = 1
    while k < s:
        j = (e + k) % s
        if iv[j]["c"] == 1 and iv[j]["H"] == 1 and iv[j]["q"] <= 2:
            k += 1
        else:
            break
    return k - 1

def vr_member(legs, pairs):
    iv = intervals(legs)
    s = len(iv)
    if s < 5:
        return False, "s<5"
    E = E_slots(iv)
    if len(E) != 1:
        return False, "E=%s" % E
    e = E[0]
    t = relay_len(iv, e)
    if not (2 <= t <= s - 2):
        return False, "t=%d" % t
    p = (e + t + 1) % s
    if not (iv[p]["c"] == 1 and iv[p]["H"] >= 2 and iv[p]["q"] <= 3):
        return False, "payer"
    used = {(e + k) % s for k in range(t + 2)}
    for j in range(s):
        if j in used or iv[j]["w"] <= 0:
            continue
        if strict_K(iv[j], legs) or strict_P(iv[j], legs):
            continue
        return False, "other-%d" % j
    gk = sorted({l["x"] for l in legs if l["m"] == "K" and l["chg"]})
    if gk != [1, 3, 5, 7, 9]:
        return False, "gkeys=%s" % gk
    for t2 in range(len(pairs)):
        c = core_of(pairs[t2][1], MSET)
        if c is None or len(c) != 9:
            return False, "core@%d" % t2
    if pairs[0] != pairs[-1]:
        return False, "not-closed"
    return True, "VR-member t=%d p=%d" % (t, p)

if __name__ == "__main__":
    out = {}
    assert hashlib.sha256(IN_CANON.encode("ascii")).hexdigest() == IN_SHA
    assert hashlib.sha256(VR_CANON.encode("ascii")).hexdigest() == VR_SHA
    out["fixture_sha"] = {"IN": True, "VR": True}
    IN_W = parse(IN_CANON); VR_W = parse(VR_CANON)
    R = replay(IN_W)
    n = len(IN_W)
    A = sum(l["a"] for l in R["legs"]); Q = sum(l["q"] for l in R["legs"])
    out["IN_totals"] = {"A": A, "Q": Q, "closed": R["S1"] == R["S0"],
                        "agree": R["agree"], "n": n}
    print("IN: A=%d Q=%d closed=%s agree=%s" % (A, Q, R["S1"] == R["S0"], R["agree"]), flush=True)
    P = R["pairs"]
    out["P1_eq_P17"] = (P[1] == P[17])
    print("P1==P17:", P[1] == P[17], flush=True)
    # seg1 [1,17)
    seg1 = IN_W[1:17]
    out["seg1_canon"] = canon(seg1)
    # replay seg1 from ACTUAL P1 trees: recover trees = replay prefix, take live objects
    Ap = to_ptr(copy.deepcopy(T0)); Bp = to_ptr(copy.deepcopy(T0))
    for (md, x) in IN_W[:1]:
        Ap, _ = splay_A(Ap, x)
        if md == 'K':
            Bp, _ = splay_B_push(Bp, x)
    # snapshot start serials
    start = (pserial(Ap), pserial(Bp))
    out["seg1_start_is_P1"] = (start == P[1])
    print("seg1 start==P1:", start == P[1], flush=True)
    # replay seg1 from ACTUAL P1 trees: replay prefix to get live P1 objects,
    # then continue with seg1 accesses recording legs (deterministic engines).
    legs1, pairs1 = [], [start]
    IA1t = None
    A2 = Ap; B2 = Bp
    def tup_of2(ps):
        if ps == '.':
            return S.LEAF
        k, l, r = ps
        return S.node(k, tup_of2(l), tup_of2(r))
    IA = tup_of2(start[0]); IB = tup_of2(start[1])
    ok1 = True
    for (md, x) in seg1:
        dA = pdepths(A2).get(x, -1); assert dA >= 0
        a = (dA + 1) // 2
        sb = pserial(B2)
        if md == 'K':
            dB = pdepths(B2).get(x, -1); assert dB >= 0
            q = dB // 2
        else:
            dB = None; q = 0
        A2, _ = splay_A(A2, x)
        if md == 'K':
            B2, _ = splay_B_push(B2, x)
        IA = S.trace(IA, x)[0]
        if md == 'K':
            IB = S.trace(IB, x)[0]
        chg = (pserial(B2) != sb) if md == 'K' else False
        pairs1.append((pserial(A2), pserial(B2)))
        legs1.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                      "delta": q - 2 * a, "chg": chg})
    out["seg1_closed"] = (pairs1[-1] == pairs1[0])
    out["seg1_end_is_P17"] = (pairs1[-1] == P[17])
    print("seg1: closed=%s end==P17=%s A=%d Q=%d" % (
        pairs1[-1] == pairs1[0], pairs1[-1] == P[17],
        sum(l["a"] for l in legs1), sum(l["q"] for l in legs1)), flush=True)
    m1, why1 = s1_member(legs1, pairs1)
    out["seg1_S1"] = {"member": m1, "why": why1}
    print("seg1 S1-member:", m1, why1, flush=True)
    out["seg1_totals"] = {"A": sum(l["a"] for l in legs1),
                          "Q": sum(l["q"] for l in legs1)}
    # ---- seg2 = [17,34) + [0,1), replayed from live P17 trees ----
    seg2 = IN_W[17:34] + IN_W[0:1]
    out["seg2_canon"] = canon(seg2)
    out["seg2_is_VR_rotated"] = (canon(seg2) == canon(VR_W[1:] + VR_W[:1]))
    print("seg2 == VR-rotated-string:", out["seg2_is_VR_rotated"], flush=True)
    A17 = to_ptr(copy.deepcopy(T0)); B17 = to_ptr(copy.deepcopy(T0))
    for (md, x) in IN_W[:17]:
        A17, _ = splay_A(A17, x)
        if md == 'K':
            B17, _ = splay_B_push(B17, x)
    start2 = (pserial(A17), pserial(B17))
    out["seg2_start_is_P17"] = (start2 == P[17])
    out["seg2_start_is_P1"] = (start2 == P[1])
    print("seg2 start==P17==P1:", start2 == P[17], start2 == P[1], flush=True)
    # VR-tail reference: replay VR_W from T0, take legs[1:] + P1-start check
    RV = replay(VR_W)
    out["VR_totals"] = {"A": sum(l["a"] for l in RV["legs"]),
                        "Q": sum(l["q"] for l in RV["legs"]),
                        "closed": RV["S1"] == RV["S0"], "agree": RV["agree"]}
    out["P1_eq_VR_postD5"] = (P[1] == RV["pairs"][1])
    print("P1(IN) == post-D5(VR):", P[1] == RV["pairs"][1], flush=True)
    legs2, pairs2 = [], [start2]
    IA = tup_of2(start2[0]); IB = tup_of2(start2[1])
    A3 = A17; B3 = B17
    for (md, x) in seg2:
        dA = pdepths(A3).get(x, -1); assert dA >= 0
        a = (dA + 1) // 2
        sb = pserial(B3)
        if md == 'K':
            dB = pdepths(B3).get(x, -1); assert dB >= 0
            q = dB // 2
        else:
            dB = None; q = 0
        A3, _ = splay_A(A3, x)
        if md == 'K':
            B3, _ = splay_B_push(B3, x)
        IA = S.trace(IA, x)[0]
        if md == 'K':
            IB = S.trace(IB, x)[0]
        chg = (pserial(B3) != sb) if md == 'K' else False
        pairs2.append((pserial(A3), pserial(B3)))
        legs2.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                      "delta": q - 2 * a, "chg": chg})
    out["seg2_closed"] = (pairs2[-1] == pairs2[0])
    out["seg2_end_is_P1"] = (pairs2[-1] == P[1])
    A2t = sum(l["a"] for l in legs2); Q2t = sum(l["q"] for l in legs2)
    out["seg2_totals"] = {"A": A2t, "Q": Q2t}
    print("seg2: closed=%s end==P1=%s A=%d Q=%d" % (
        pairs2[-1] == pairs2[0], pairs2[-1] == P[1], A2t, Q2t), flush=True)
    # transition agreement with VR tail: legs2[0:17] vs RV legs[1:18]
    tag = [(l2["dA"], l2["dB"], l2["a"], l2["q"]) for l2 in legs2[:17]]
    vtag = [(l2["dA"], l2["dB"], l2["a"], l2["q"]) for l2 in RV["legs"][1:18]]
    out["seg2_tail_eq_VR_tail"] = (tag == vtag)
    print("seg2[0:17] transitions == VR[1:18]:", tag == vtag, flush=True)
    m2, why2 = vr_member(legs2, pairs2)
    out["seg2_VR"] = {"member": m2, "why": why2}
    print("seg2 VR-member:", m2, why2, flush=True)
    out["B4"] = {"A1": sum(l["a"] for l in legs1), "Q1": sum(l["q"] for l in legs1),
                 "A2": A2t, "Q2": Q2t, "A": A, "Q": Q,
                 "additive": (sum(l["a"] for l in legs1) + A2t == A
                              and sum(l["q"] for l in legs1) + Q2t == Q)}
    print("B4 additive:", out["B4"]["additive"], flush=True)
    json.dump(out, open(PDIR / "MSP_cyclic_decomposition_certificate.json", "w"), indent=1, default=str)
